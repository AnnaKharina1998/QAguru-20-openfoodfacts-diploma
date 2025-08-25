from selene import browser, have
from ui.pages.product_page import ProductPage
from ui.pages.search_page import SearchPage
from ui.pages.category_page import CategoryPage

BARCODE = '737628064502'
BAD_BARCODE = '0000000000000'


# 1) карточка по валидному штрихкоду
def test_product_card_opens_by_barcode():
    page = ProductPage()
    page.open_product(BARCODE)
    page.should_have_barcode(BARCODE)


# 2) продукт не найден по невалидному штрихкоду
def test_product_not_found_shows_error():
    page = ProductPage()
    page.open_product(BAD_BARCODE)
    page.should_show_error()


# 3) поиск по названию через поле на главной
def test_search_by_name_shows_results():
    page = SearchPage()
    page.open().search('noodle')
    page.should_have_results_with_text('noodle')


# 4) результаты поиска содержат ссылки на продукты
def test_search_results_have_product_links():
    browser.open('/cgi/search.pl?search_terms=noodle&search_simple=1&action=process')
    page = SearchPage()
    page.should_have_product_links()


# 5) открытие категории "noodles"
def test_open_category_noodles():
    page = CategoryPage()
    page.open('noodles')
    page.should_have_text('noodles')
    page.should_have_product_links()


# 6) смена страны/языка через клик по подсказке: France
def test_switch_country_to_france_by_click():
    page = ProductPage()
    page.open()
    page.choose_country('fra', 'France')
    page.should_redirect_to('//fr.openfoodfacts.org')
    page.should_have_text('Découvrir')


# 7) поиск по штрихкоду с главной → редирект на карточку
def test_search_by_barcode_redirects_to_product():
    page = SearchPage()
    page.open().search(BARCODE)
    browser.should(have.url_containing(f'{BARCODE}'))