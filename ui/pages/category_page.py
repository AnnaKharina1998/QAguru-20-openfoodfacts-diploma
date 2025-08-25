from selene import browser, have
import allure

class CategoryPage:
    def open(self, category: str):
        with allure.step(f'Открыть страницу категории "{category}"'):
            browser.open(f'/category/{category}')
        return self

    def should_have_text(self, text: str):
        with allure.step(f'Проверка наличия на странице текста "{text}"'):
            browser.element('body').should(have.text(text))

    def should_have_product_links(self):
        with allure.step(f'Проверка ненулевого количества продуктов в категории'):
            browser.all('a[href*="/product/"]').should(have.size_greater_than(0))