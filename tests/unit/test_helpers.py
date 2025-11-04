from HelloWorldFunction import app
from decimal import Decimal
import pytest

def test_card_id_to_keys_happy():
    pk, sk = app._card_id_to_keys("Shohei Ohtani|2018|Bowman Chrome|Prospects|#1|PSA10")
    assert pk == "player#Shohei Ohtani"
    assert sk == "card#2018#Bowman Chrome#Prospects##1#PSA10"

def test_card_id_to_keys_invalid_parts():
    with pytest.raises(ValueError):
        app._card_id_to_keys("bad|input|only|four|parts")

def test_decimal_to_native_basic():
    data = {"price": Decimal("12.50"), "nested": [Decimal("1"), {"v": Decimal("2.2")}]}
    out = app._decimal_to_native(data)
    assert out == {"price": 12.5, "nested": [1.0, {"v": 2.2}]}
