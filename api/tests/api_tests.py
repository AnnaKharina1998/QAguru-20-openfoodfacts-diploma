import requests
import pytest
import os

from dotenv import load_dotenv
load_dotenv()

BARCODE = "0737628064502"  # это суп из лапши

def test_get_product_ok():
    url = f"https://world.openfoodfacts.org/api/v2/product/{BARCODE}"
    r = requests.get(url, timeout=10)
    data = r.json()

    assert r.status_code == 200
    assert data["code"] == BARCODE
    assert "product" in data

    product = data["product"]

    # проверка на ключевые слова
    keywords = product.get("_keywords", [])
    assert any("noodle" in kw.lower() for kw in keywords), f"noodle not found in {keywords}"



BAD_BARCODE = "00000000"

def test_product_not_found_status_zero():
    r = requests.get(f"https://world.openfoodfacts.org/api/v2/product/{BAD_BARCODE}", timeout=10)
    r.raise_for_status()
    data = r.json()
    assert data["code"] == BAD_BARCODE
    assert data["status"] == 0
    assert data.get("status_verbose") == 'no code or invalid code'



def test_search_noodle_returns_results():
    r = requests.get(
        "https://world.openfoodfacts.org/cgi/search.pl",
        params={"search_terms": "noodle", "search_simple": 1, "action": "process", "json": 1},
        timeout=15, verify=False,
    )
    r.raise_for_status()
    data = r.json()
    products = data.get("products", [])
    assert isinstance(products, list)
    assert len(products) > 0
    # хотя бы у одного встречается "noodle" в keywords/name
    assert any(
        ("keywords" in p and any("noodle" in k.lower() for k in p.get("keywords", [])))
        or ("product_name" in p and "noodle" in (p.get("product_name") or "").lower())
        for p in products
    )


BARCODE = "737628064502"

user_id = os.getenv("OFF_USER")
password = os.getenv("OFF_PASSWORD")
has_creds = bool(user_id and password)

@pytest.mark.skipif(not has_creds, reason="need OFF_USER and OFF_PASSWORD")
def test_add_comment_ok():
    url = "https://world.openfoodfacts.org/cgi/product_jqm2.pl"
    data = {
        "code": BARCODE,
        "comment": "automated test note",
        "user_id": user_id,
        "password": password,
        "action": "edit",
    }
    r = requests.post(url, data=data, timeout=15, verify=False)
    assert r.status_code == 200
    # Проверим, что не вернулось явное сообщение об ошибке
    assert "invalid" not in r.text.lower()


@pytest.mark.skipif(not has_creds, reason="need OFF_USER and OFF_PASSWORD")
def test_add_comment_wrong_password():
    url = "https://world.openfoodfacts.org/cgi/product_jqm2.pl"
    data = {
        "code": BARCODE,
        "comment": "should fail",
        "user_id": os.getenv("OFF_USER"),
        "password": "definitely_wrong",
        "action": "edit",
    }
    r = requests.post(url, data=data, timeout=15, verify=False)
    assert r.status_code == 403
    assert "invalid" in r.text.lower() or "error" in r.text.lower()