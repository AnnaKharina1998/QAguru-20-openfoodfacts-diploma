import os
import requests
import pytest
import allure
from dotenv import load_dotenv

load_dotenv()
BASE = "https://world.openfoodfacts.org"

# --- 1. Позитив: GET продукт по штрихкоду ---
BARCODE_OK = "0737628064502"  # суп из лапши

@allure.feature("API")
@allure.story("GET /api/v2/product/{barcode}")
@allure.title("Получение продукта по валидному штрих-коду")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_product_ok():
    with allure.step(f'GET запрос с верным штрих-кодом {BARCODE_OK}'):
        url = f"{BASE}/api/v2/product/{BARCODE_OK}"
        r = requests.get(url, timeout=10, verify=False)
    with allure.step('Проверить статус-код 200'):
        assert r.status_code == 200
    with allure.step('Разобрать JSON-ответ'):
        data = r.json()
    with allure.step('Проверить, что штрих-код совпадает и есть поле product'):
        assert data["code"] == BARCODE_OK
        assert "product" in data
    with allure.step("Проверить, что среди ключевых слов есть 'noodle'"):
        product = data["product"]
        keywords = product.get("_keywords", [])
        assert any("noodle" in kw.lower() for kw in keywords), f"noodle not found in {keywords}"


# --- 2. Негатив: невалидный штрихкод ---
BAD_BARCODE = "00000000"

@allure.feature("API")
@allure.story("GET /api/v2/product/{barcode}")
@allure.title("Невалидный штрих-код: статус=0 и корректное сообщение")
@allure.severity(allure.severity_level.CRITICAL)
def test_product_not_found_status_zero():
    with allure.step('GET запрос с неверным штрих-кодом'):
        r = requests.get(f"{BASE}/api/v2/product/{BAD_BARCODE}", timeout=10, verify=False)
    with allure.step('Статус-код 200 и корректный JSON'):
        r.raise_for_status()
        data = r.json()
    with allure.step("Проверить сообщение об ошибке с неверным штрих-кодом"):
        assert data["code"] == BAD_BARCODE
        assert data["status"] == 0
        assert data.get("status_verbose") == "no code or invalid code"


# --- 3. Поиск по ключевому слову ---
@allure.feature("API")
@allure.story("GET /cgi/search.pl")
@allure.title("Поиск по ключевому слову 'noodle' возвращает результаты")
@allure.severity(allure.severity_level.NORMAL)
def test_search_noodle_returns_results():
    with allure.step('GET запрос на поиск noodle'):
        r = requests.get(
            f"{BASE}/cgi/search.pl",
            params={"search_terms": "noodle", "search_simple": 1, "action": "process", "json": 1},
            timeout=15,
            verify=False,
        )
    with allure.step('Статус-код 200 и разбор JSON'):
        r.raise_for_status()
        data = r.json()
    with allure.step('Проверить, что список products не пуст'):
        products = data.get("products", [])
        assert isinstance(products, list)
        assert len(products) > 0
    with allure.step("Проверить, что хотя бы в одном продукте встречается 'noodle'"):
        assert any(
            ("keywords" in p and any("noodle" in k.lower() for k in p.get("keywords", [])))
            or ("product_name" in p and "noodle" in (p.get("product_name") or "").lower())
            for p in products
        )


# --- 4. Write-API: комментарий (авторизация) ---
BARCODE_WRITE = "737628064502"
user_id = os.getenv("OFF_USER")
password = os.getenv("OFF_PASSWORD")
has_creds = bool(user_id and password)

@allure.feature("API")
@allure.story("POST /cgi/product_jqm2.pl")
@allure.title("Добавление комментария: валидные логин и пароль")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.skipif(not has_creds, reason="need OFF_USER and OFF_PASSWORD")
def test_add_comment_ok():
    with allure.step('POST запрос (валидные логин и пароль)'):
        url = f"{BASE}/cgi/product_jqm2.pl"
        data = {
            "code": BARCODE_WRITE,
            "comment": "automated test note",
            "user_id": user_id,
            "password": password,
            "action": "edit",
        }
        r = requests.post(url, data=data, timeout=15, verify=False)
    with allure.step('Проверить успешный ответ (без указания на ошибку)'):
        assert r.status_code == 200
        assert "invalid" not in r.text.lower() and "error" not in r.text.lower()


@allure.feature("API")
@allure.story("POST /cgi/product_jqm2.pl")
@allure.title("Добавление комментария: неверный пароль → ошибка")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.skipif(not has_creds, reason="need OFF_USER and OFF_PASSWORD")
def test_add_comment_wrong_password():
    with allure.step('POST запрос (неверный пароль)'):
        url = f"{BASE}/cgi/product_jqm2.pl"
        data = {
            "code": BARCODE_WRITE,
            "comment": "should fail",
            "user_id": user_id,
            "password": "definitely_wrong",
            "action": "edit",
        }
        r = requests.post(url, data=data, timeout=15, verify=False)
    with allure.step('Проверить, что сервер вернул ошибку'):
        assert r.status_code in (401, 403)
        assert ("invalid" in r.text.lower()) or ("error" in r.text.lower())