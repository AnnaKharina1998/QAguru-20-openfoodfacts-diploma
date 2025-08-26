# API-тесты (OpenFoodFacts)

## Технологии
- Python, Pytest
- Requests
- Allure (шаги, feature/story/severity)
- dotenv (авторизация через переменные окружения)

## Структура
```
api/
└─ tests/
   └─ api_tests.py
```

## Запуск
Запуск тестов осуществляется джобой в jenkins
https://jenkins.autotests.cloud/job/AnnaKharina1998-QAguru-20-diploma-api/

## Переменные окружения
Для авторизационных тестов при локальном запуске нужны логин и пароль в `.env`:
```
OFF_USER=your_login
OFF_PASSWORD=your_password
```

## Покрытые сценарии
- `GET /api/v2/product/{barcode}`
  - позитив (валидный штрихкод → статус 200, есть product, keywords содержат "noodle")
  - негатив (невалидный штрихкод → status=0, корректное сообщение)
- `GET /cgi/search.pl`
  - поиск по ключевому слову `noodle` возвращает непустой список продуктов
- `POST /cgi/product_jqm2.pl`
  - добавление комментария с валидными логином/паролем
  - ошибка при неверном пароле

## Особенности
- В запросах используется `verify=False` (для диплома допустимо).
- Авторизационные тесты помечены `@pytest.mark.skipif` — если данные для авторизации не заданы, они будут пропущены.
- Severity:
  - CRITICAL — тесты на продукт и комментарии
  - NORMAL — тест на поиск
