import pytest
from selene import browser
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope='session', autouse=True)
def setup_browser():
    opts = Options()
    # opts.add_argument('--headless=new')     # убери, если хочешь видеть окно
    opts.add_argument('--window-size=1280,800')

    driver = Chrome(options=opts)

    browser.config.driver = driver
    browser.config.base_url = 'https://world.openfoodfacts.org'
    browser.config.timeout = 6

    yield
    browser.quit()