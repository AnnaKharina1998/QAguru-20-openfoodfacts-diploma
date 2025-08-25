from selene import browser, have
import allure

class SearchPage:
    def open(self):
        browser.open('/')
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