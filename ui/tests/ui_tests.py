# ui/tests/test_ui_suite.py
from selene import browser, have
import allure
from ui.pages.product_page import ProductPage
from ui.pages.search_page import SearchPage
from ui.pages.category_page import CategoryPage

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