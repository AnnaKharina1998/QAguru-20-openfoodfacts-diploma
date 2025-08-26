from selene import browser, have
import allure

class SearchPage:


    def open_results(self, query: str):
        with allure.step(f'Открыть страницу поиска по запросу "{query}"'):
            browser.open(f'/cgi/search.pl?search_terms={query}&search_simple=1&action=process')
        return self

    def search(self, query: str):
        with allure.step(f'Начать поиск по запросу "{query}"'):
            browser.element('input[name="search_terms"]').type(query).press_enter()
        return self

    def should_have_results_with_text(self, text: str):
        with allure.step(f'Проверка наличия "{text}" в результатах поиска'):
            browser.element('body').should(have.text(text))

    def should_have_product_links(self):
        with allure.step(f'Проверка ненулевого количества ссылок в результатах поиска'):
            browser.all('a[href*="/product/"]').should(have.size_greater_than(0))

    def open(self):
        with allure.step('Открыть главную страницу'):
            browser.open('/')
        return self