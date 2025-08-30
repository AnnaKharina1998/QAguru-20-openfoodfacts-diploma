from selene import browser, have
import allure
from ui.pages.product_page import ProductPage
from ui.pages.search_page import SearchPage
from ui.pages.category_page import CategoryPage
import os
import time
import requests
import pytest
from dotenv import load_dotenv
from selene import browser, have


load_dotenv()


BARCODE = '737628064502'
BAD_BARCODE = '0000000000000'


@allure.feature("UI")
@allure.story("Карточка товара")
@allure.title("Открытие карточки по валидному штрихкоду")
@allure.severity(allure.severity_level.CRITICAL)
def test_product_card_opens_by_barcode():
    page = ProductPage()
    page.open_product(BARCODE)
    page.should_have_barcode(BARCODE)


@allure.feature("UI")
@allure.story("Карточка товара")
@allure.title("Невалидный штрихкод → отображается ошибка")
@allure.severity(allure.severity_level.CRITICAL)
def test_product_not_found_shows_error():
    page = ProductPage()
    page.open_product(BAD_BARCODE)
    page.should_show_error()


@allure.feature("UI")
@allure.story("Поиск")
@allure.title("Поиск по названию 'noodle' через главную страницу")
@allure.severity(allure.severity_level.NORMAL)
def test_search_by_name_shows_results():
    page = SearchPage()
    page.open()
    page.search('noodle')
    page.should_have_results_with_text('noodle')


@allure.feature("UI")
@allure.story("Поиск")
@allure.title("Результаты поиска содержат ссылки на продукты")
@allure.severity(allure.severity_level.NORMAL)
def test_search_results_have_product_links():
    page = SearchPage()
    page.open_results('noodle')
    page.should_have_product_links()


@allure.feature("UI")
@allure.story("Категории")
@allure.title("Открытие категории 'noodles'")
@allure.severity(allure.severity_level.NORMAL)
def test_open_category_noodles():
    page = CategoryPage()
    page.open('noodles')
    page.should_have_text('noodles')
    page.should_have_product_links()


@allure.feature("UI")
@allure.story("Смена страны/языка")
@allure.title("Переключение страны на France")
@allure.severity(allure.severity_level.CRITICAL)
def test_switch_country_to_france_by_click():
    page = ProductPage()
    page.open()
    page.choose_country('fra', 'France')
    page.should_redirect_to('//fr.openfoodfacts.org')
    page.should_have_text('Découvrir')


@allure.feature("UI")
@allure.story("Поиск")
@allure.title("Поиск по штрихкоду через главную страницу → редирект на карточку")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_by_barcode_redirects_to_product():
    page = SearchPage()
    page.open()
    page.search(BARCODE)
    browser.should(have.url_containing(f'{BARCODE}'))



BASE = "https://world.openfoodfacts.org"
BARCODE = "737628064502"  # тестовый продукт

user_id = os.getenv("OFF_USER")
password = os.getenv("OFF_PASSWORD")
has_creds = bool(user_id and password)

@allure.feature("Integration API + UI")
@allure.story("API подготавливает данные (barcode), UI проверяет карточку")
@allure.title("Поиск товара через API → открытие карточки в UI по штрихкоду")
def test_api_search_provides_barcode_then_ui_opens_product():
    with allure.step('API: выполнить поиск по keyword "noodle" и взять первый валидный продукт'):
        r = requests.get(
            f"{BASE}/cgi/search.pl",
            params={"search_terms": "noodle", "search_simple": 1, "action": "process", "json": 1},
            timeout=15,
            verify=False,
        )
        r.raise_for_status()
        data = r.json()
        products = data.get("products", [])
        assert products, "Пустая выдача поиска API"

        # берём первый продукт, у которого есть и штрихкод (code), и имя (product_name)
        first = next(
            (p for p in products if p.get("code") and (p.get("product_name") or "").strip()),
            None,
        )
        assert first, "Не найден продукт с code и product_name"
        barcode = first["code"]
        name = first["product_name"].strip()

    with allure.step(f'UI: открыть карточку товара по штрихкоду {barcode}'):
        page = ProductPage()
        page.open_product(barcode)

    with allure.step(f'UI: проверить, что название товара "{name}" присутствует на странице'):
        browser.element("body").should(have.text(name))

@pytest.mark.skipif(not has_creds, reason="need OFF_USER and OFF_PASSWORD")
@allure.feature("Integration API + UI")
@allure.story("Комментарий через API → проверка в UI после логина")
@allure.title("Комментарий отображается на странице редактирования после логина")
def test_add_comment_api_then_check_ui():
    comment_text = "integration test comment"

    with allure.step("API: добавить комментарий к товару"):
        url = f"{BASE}/cgi/product_jqm2.pl"
        data = {
            "code": BARCODE,
            "comment": comment_text,
            "user_id": user_id,
            "password": password,
            "action": "edit",
        }
        r = requests.post(url, data=data, timeout=15, verify=False)
        assert r.status_code == 200
        assert "invalid" not in r.text.lower()

    time.sleep(3)

    with allure.step("UI: залогиниться под тем же пользователем"):
        page = ProductPage()
        page.login(user_id, password)

    with allure.step("UI: открыть карточку товара"):
        page.open_product(BARCODE)

    with allure.step("UI: перейти в режим редактирования"):
        page.open_edit_page()

    with allure.step("UI: проверить, что комментарий отображается"):
        page.should_have_comment(comment_text)