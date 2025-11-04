import os
import pytest
import requests
from urllib.parse import quote

pytestmark = pytest.mark.integration

API_BASE = os.getenv("API_BASE")

@pytest.mark.skipif(not API_BASE, reason="Set API_BASE env var first")
def test_list_cards_count_is_10():
    r = requests.get(f"{API_BASE}/cards", timeout=30)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) == 10, f"Expected 10 curated items, got {len(data)}"

@pytest.mark.skipif(not API_BASE, reason="Set API_BASE env var first")
def test_top3_by_player_ohtani():
    r = requests.get(f"{API_BASE}/cards/top3", params={"player": "Shohei Ohtani"}, timeout=30)
    assert r.status_code == 200
    arr = r.json()
    assert isinstance(arr, list)
    assert 1 <= len(arr) <= 3
    # all items are Ohtani and sorted desc by price
    assert all(it["player"] == "Shohei Ohtani" for it in arr)
    prices = [it.get("price", 0) for it in arr]
    assert prices == sorted(prices, reverse=True)

@pytest.mark.skipif(not API_BASE, reason="Set API_BASE env var first")
def test_get_card_by_id_hideo_nomo():
    card_id = "Hideo Nomo|1995|Topps|Base|#2|PSA10"
    enc = quote(card_id, safe="")
    r = requests.get(f"{API_BASE}/cards/{enc}", timeout=30)
    assert r.status_code == 200
    obj = r.json()
    assert obj["player"] == "Hideo Nomo"
    assert obj["brand"] == "Topps"
    # year may be int or float depending on json conversion
    assert obj["year"] in (1995, 1995.0)
