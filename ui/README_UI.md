# UI-тесты (OpenFoodFacts)

## Технологии
- Python, Pytest  
- Selene (Selenium wrapper)  
- PageObject  
- Allure (шаги, feature/story/severity)  

## Структура
```
ui/
├─ pages/                # PageObjects
│  ├─ product_page.py
│  ├─ search_page.py
│  └─ category_page.py
└─ tests/
   └─ test_ui_suite.py
```

## Запуск

Запуск тестов осуществляется джобой в jenkins
https://jenkins.autotests.cloud/job/AnnaKharina1998-QAguru-20-diploma-UI/

Для локального запуска тестов через селеноид нужны логин, пароль и url от него в `.env`:
```
S_LOGIN=your_login
S_PASSWORD=your_password
S_URL=selenoid_url
```
Для локального запуска тестов в браузере измените фикстуру на:
```
import pytest
from selene import browser
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

BASE_URL = 'https://world.openfoodfacts.org'

@pytest.fixture(scope='session', autouse=True)
def setup_browser():
    opts = Options()
    opts.add_argument('--window-size=1280,800')

    driver = Chrome(options=opts) 
    browser.config.driver = driver
    browser.config.base_url = BASE_URL
    browser.config.timeout = 6

    yield
    browser.quit()
```

## Покрытые сценарии
- **Карточка товара**
  - открытие по валидному штрихкоду
  - ошибка при невалидном штрихкоде
- **Поиск**
  - поиск по названию
  - поиск по штрихкоду с главной
  - результаты поиска содержат ссылки
- **Категории**
  - открытие категории `noodles`
- **Смена страны**
  - переключение на France (проверка редиректа и текста)

## Особенности
- Все действия и проверки вынесены в PageObject.  
- Каждый шаг описан через `allure.step`, отчёты читаются как живые сценарии.  
- Severity для критичных сценариев отмечена как `CRITICAL`.  
