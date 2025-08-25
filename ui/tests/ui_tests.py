from selene import browser, have, be, by

BARCODE = '737628064502'
BAD_BARCODE = '0000000000000'


# 1) карточка по валидному штрихкоду
def test_product_card_opens_by_barcode():
    browser.open(f'/product/{BARCODE}')
    browser.element('body').should(have.text(BARCODE))


# 2) продукт не найден по невалидному штрихкоду
def test_product_not_found_shows_error():
    browser.open(f'/product/{BAD_BARCODE}')
    browser.element('body').should(have.text('Error'))


# 3) поиск по названию через поле на главной
def test_search_by_name_shows_results():
    browser.open('/')
    browser.element('input[name="search_terms"]').type('noodle').press_enter()
    browser.element('body').should(have.text('noodle'))


# 4) результаты поиска содержат ссылки на продукты
def test_search_results_have_product_links():
    browser.open('/cgi/search.pl?search_terms=noodle&search_simple=1&action=process')
    browser.all('a[href*="/product/"]').should(have.size_greater_than(0))


# 5) открытие категории "noodles"
def test_open_category_noodles():
    browser.open('/category/noodles')
    browser.element('body').should(have.text('noodles'))
    browser.all('a[href*="/product/"]').should(have.size_greater_than(0))


# 6) смена страны/языка через клик по подсказке: France
def test_switch_country_to_france_by_click():
    browser.open('/')
    browser.element('span.select2-selection__placeholder').click()
    browser.element('input.select2-search__field').type('fra')
    browser.element('span.select2-results').element(by.text('France')).click()
    browser.should(have.url_containing('//fr.openfoodfacts.org'))
    browser.element('body').should(have.text('Découvrir'))


# 7) поиск по штрихкоду с главной → редирект на карточку
def test_search_by_barcode_redirects_to_product():
    browser.open('/')
    browser.element('input[name="search_terms"]').type(BARCODE).press_enter()
    browser.should(have.url_containing(f'{BARCODE}'))