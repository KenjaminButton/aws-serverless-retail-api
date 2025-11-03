import os
import json
import urllib.parse
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key

# --------------------------
# Response + event utilities
# --------------------------

def _resp(status: int, body) -> dict:
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        },
        "body": json.dumps(body, default=str),
    }

def _parse_method_path(event: dict):
    # HTTP API (payload v2.0) fields
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    raw_path = event.get("rawPath", "")
    return method, raw_path

def _qs(event: dict) -> dict:
    return event.get("queryStringParameters") or {}

def _path_params(event: dict) -> dict:
    return event.get("pathParameters") or {}

def _decimal_to_native(obj):
    if isinstance(obj, list):
        return [_decimal_to_native(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _decimal_to_native(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return float(obj)
    return obj

# --------------------------
# DynamoDB lazy singleton
# --------------------------

_dynamo = None
_table = None

def _table_ref():
    global _dynamo, _table
    if _table is None:
        table_name = os.environ["CARDS_TABLE"]  # <- matches your template
        _dynamo = boto3.resource("dynamodb")
        _table = _dynamo.Table(table_name)
    return _table

# --------------------------
# Domain helpers
# --------------------------

def _card_id_to_keys(card_id: str):
    """
    cardId format:
      "Shohei Ohtani|2018|Bowman Chrome|Prospects|#1|PSA10"

    PK = player#<PlayerName>
    SK = card#<Year>#<Brand>#<Set>#<CardNo>#PSA10
    """
    parts = card_id.split("|")
    if len(parts) != 6:
        raise ValueError("Invalid cardId format. Expected 6 parts separated by '|'.")
    player, year, brand, set_name, card_no, grade = parts
    pk = f"player#{player}"
    sk = f"card#{year}#{brand}#{set_name}#{card_no}#{grade}"
    return pk, sk

# --------------------------
# Route handlers
# --------------------------

def route_hello():
    return _resp(200, {"message": "hello world"})

def route_get_all_cards():
    table = _table_ref()
    items = []
    kwargs = {}
    while True:
        out = table.scan(**kwargs)
        items.extend(out.get("Items", []))
        last = out.get("LastEvaluatedKey")
        if not last:
            break
        kwargs["ExclusiveStartKey"] = last
    return _resp(200, _decimal_to_native(items))

def route_get_card_by_id(card_id: str):
    try:
        pk, sk = _card_id_to_keys(card_id)
    except ValueError as e:
        return _resp(400, {"message": str(e)})
    table = _table_ref()
    out = table.get_item(Key={"PK": pk, "SK": sk})
    item = out.get("Item")
    if not item:
        return _resp(404, {"message": "Card not found"})
    return _resp(200, _decimal_to_native(item))

def route_get_top3_by_player(player: str):
    if not player:
        return _resp(400, {"message": "Missing required query param 'player'"})
    table = _table_ref()
    pk = f"player#{player}"
    out = table.query(KeyConditionExpression=Key("PK").eq(pk))
    items = out.get("Items", [])
    # Sort by price (Decimal) descending, then take top 3
    items_sorted = sorted(items, key=lambda x: x.get("price", Decimal("0")), reverse=True)
    return _resp(200, _decimal_to_native(items_sorted[:3]))

def route_seed_cards(event: dict):
    """
    Protected by API Gateway Cognito Authorizer at the route mapping.
    Writes a tiny curated dataset (PSA10 only). Overwrites by PK/SK.
    """
    seed_items = [
        {
            "PK": "player#Shohei Ohtani",
            "SK": "card#2018#Bowman Chrome#Prospects#%231#PSA10".replace("%23", "#"),
            "player": "Shohei Ohtani",
            "year": 2018,
            "brand": "Bowman Chrome",
            "set": "Prospects",
            "cardNo": "#1",
            "grade": "PSA10",
            "price": Decimal("1599.99"),
            "currency": "USD",
        },
        {
            "PK": "player#Ichiro Suzuki",
            "SK": "card#2001#Topps Chrome#Base#%23596#PSA10".replace("%23", "#"),
            "player": "Ichiro Suzuki",
            "year": 2001,
            "brand": "Topps Chrome",
            "set": "Base",
            "cardNo": "#596",
            "grade": "PSA10",
            "price": Decimal("799.00"),
            "currency": "USD",
        },
        {
            "PK": "player#Hideki Matsui",
            "SK": "card#2003#Topps Chrome#Base#%23111#PSA10".replace("%23", "#"),
            "player": "Hideki Matsui",
            "year": 2003,
            "brand": "Topps Chrome",
            "set": "Base",
            "cardNo": "#111",
            "grade": "PSA10",
            "price": Decimal("249.50"),
            "currency": "USD",
        },
    ]

    table = _table_ref()
    with table.batch_writer(overwrite_by_pkeys=["PK", "SK"]) as bw:
        for it in seed_items:
            bw.put_item(Item=it)

    return _resp(200, {"message": "Seed complete", "count": len(seed_items)})

# --------------------------
# Router
# --------------------------

def lambda_handler(event, context):
    method, raw_path = _parse_method_path(event)
    qs = _qs(event)
    params = _path_params(event)

    try:
        # Keep /hello online for sanity checks
        if method == "GET" and raw_path == "/hello":
            return route_hello()

        # Public routes
        if method == "GET" and raw_path == "/cards":
            return route_get_all_cards()

        if method == "GET" and raw_path.startswith("/cards/") and params and "cardId" in params:
            # cardId may be URL-encoded; decode it
            encoded = params["cardId"]
            card_id = urllib.parse.unquote(encoded)
            return route_get_card_by_id(card_id)

        if method == "GET" and raw_path == "/cards/top3":
            player = qs.get("player")
            return route_get_top3_by_player(player)

        # Protected route (JWT enforced by API Gateway mapping)
        if method == "POST" and raw_path == "/cards/seed":
            return route_seed_cards(event)

        return _resp(404, {"message": "Not found"})

    except Exception as e:
        # Surface a simple error; keep internals private
        return _resp(500, {"message": "Internal error", "detail": str(e)})
