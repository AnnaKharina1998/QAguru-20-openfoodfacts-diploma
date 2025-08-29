# OpenFoodFacts — дипломный проект (Python + Selene + Pytest + Allure)

Набор автотестов на базе **OpenFoodFacts**:
- **UI** (Selene/Selenium, PageObject, Allure-шаги)
- **API** (requests, Allure-шаги)
- **CI/CD** (Jenkins, Allure Reports, Telegram notifications)

---

## 🚀 Быстрый старт

### 0) Подготовка окружения
```bash
# в корне проекта
python -m venv .venv
# Linux/Mac:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 1) Запуск UI-тестов
```bash
pytest -q ui/tests --alluredir=allure-results
```

### 2) Запуск API-тестов
```bash
pytest -q api/tests --alluredir=allure-results
```
Более подробно про условия и способы запуска - в readme файлах конкретных проектов.

### 3) Просмотр отчёта Allure
```bash
allure serve allure-results
```

---

## 📂 Структура проекта

```
openfoodfacts-diploma/
├─ ui/
│  ├─ pages/                 # PageObjects с Allure-шагами
│  │  ├─ product_page.py
│  │  ├─ search_page.py
│  │  └─ category_page.py
│  └─ tests/
│     └─ test_ui_suite.py
├─ api/
│  └─ tests/
│     └─ test_api_suite.py
├─ requirements.txt
├─ pytest.ini                # содержит --alluredir=allure-results
└─ README.md                 # этот файл
```

---

## 🔍 UI тесты
- **Карточка товара**: валидный штрихкод, ошибка при невалидном  
- **Поиск**: по названию, по штрихкоду, результаты поиска содержат ссылки  
- **Категории**: открытие категории `noodles`  
- **Смена страны**: переключение на France (редирект, французский текст)

## 🔗 API тесты
- `GET /api/v2/product/{barcode}`: позитив и негатив  
- `GET /cgi/search.pl`: поиск по ключевому слову `noodle`  
- `POST /cgi/product_jqm2.pl`: добавление комментария (валидный/невалидный пароль)  

📌 Для авторизационных тестов нужны креды в `.env`:
```
OFF_USER=your_login
OFF_PASSWORD=your_password
```
## Ручные тесты
Ручные тест-кейсы добавлены в проект в allure
https://allure.autotests.cloud/project/4895/dashboards

---

## ⚙️ CI/CD
- Jenkins pipelines 
https://jenkins.autotests.cloud/job/AnnaKharina1998-QAguru-20-diploma-UI/
https://jenkins.autotests.cloud/job/AnnaKharina1998-QAguru-20-diploma-api/
- Allure reports  
- Telegram notifications  
Уведомления приходят в чат https://t.me/krasnokutakaia_bot_notifications

---

## 🛠️ Стек
- Python, Pytest  
- Selene (Selenium)  
- Requests  
- Allure  
- Jenkins  
  

---

## ⭐ Особенности
- Авторизационные тесты пропускаются, если нет переменных окружения  
