from selene import browser, have, by
import allure
class ProductPage:
    def open(self):
        with allure.step('Открыть страницу https://world.openfoodfacts.org'):
            browser.open('/')
        return self

    def open_product(self, barcode: str):
        with allure.step(f"Открыть страницу товара со штрихкодом {barcode}"):
            browser.open(f'/product/{barcode}')
        return self

    def should_have_barcode(self, barcode: str):
        with allure.step(f"Проверить, что открылась карточка товара со штрихкодом {barcode}"):
            browser.element('body').should(have.text(barcode))
        return self

    def should_show_error(self):
        with allure.step(f"Проверить, что отображается ошибка"):
            browser.element('body').should(have.text('Error'))
        return self

    # --- Country selector (элемент страницы) ---
    def choose_country(self, name_part: str, full_name: str):
        with allure.step(f"Выбрать страну"):
            with allure.step(f"Кликнуть по кнопке выбора страны"):
                browser.element('span.select2-selection__placeholder').click()
            with allure.step(f"Ввести в открывшееся поле текст {name_part}"):
                browser.element('input.select2-search__field').type(name_part)
            with allure.step(f"Кликнуть по полсказке с текстом {full_name}"):
                browser.element('span.select2-results').element(by.text(full_name)).click()
        return self

    def should_redirect_to(self, subdomain: str):
        with allure.step(f"Проверка редиректа на страницу с поддоменом {subdomain}"):
            browser.should(have.url_containing(subdomain))
        return self

    def should_have_text(self, text: str):
        with allure.step(f'Проверка наличия на странице текста "{text}"'):
            browser.element('body').should(have.text(text))
        return self