import os
import pytest
import requests

pytestmark = pytest.mark.integration

def test_hello_endpoint():
    api_base = os.getenv("API_BASE")
    if not api_base:
        pytest.skip("Set API_BASE env var to your deployed endpoint first")

    r = requests.get(f"{api_base}/hello", timeout=20)
    assert r.status_code == 200
    assert "hello" in r.text.lower()
