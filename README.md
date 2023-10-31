![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Selenium](https://img.shields.io/badge/Selenium-3.141%2B-brightgreen)
![Allure](https://img.shields.io/badge/Allure-reporting-brightgreen)

# Тестирование TENSOR

Эта программа для автоматизированного тестирования веб-приложений с использованием Selenium WebDriver и Allure Framework.

## Используемые библиотеки

- Python 3.x
- Selenium WebDriver: для взаимодействия с веб-страницами и элементами на них.
- pytest: для организации и запуска тестов.
- requests: для выполнения HTTP-запросов (например, скачивания файлов).
- Allure Framework: для генерации красочных отчетов о выполнении тестов.

## Установка

Для установки необходимых зависимостей выполните следующие шаги:

1. Установите Python 3.x, если у вас его еще нет.
2. Установите браузер Chrome.
3. Установите ChromeDriver отсюда: [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/).
4. Склонируйте репозиторий с тестами с помощью команды:
   ```bash
   git clone https://github.com/nasretdinovs/tensor_autotest.git
   ```

5. Перейдите в папку с проектом:
    ```bash
    cd tensor_autotest
    ```

6. Установите необходимые Python-зависимости:

    ```bash
    pip install -r requirements.txt
    ```

## Запуск

Вы можете запустить тесты с помощью команды pytest в корневой папке проекта. Вот пример:
```bash
pytest -v test_example.py
```

или с уже предустановленными настройками просто запустить из python:
```bash
python test_example.py
```

## Генерация отчета Allure

Чтобы сгенерировать отчет Allure, выполните следующие шаги:

1. Установите Allure CLI (если у вас его еще нет). Инструкции можно найти здесь: [Allure Command Line](https://docs.qameta.io/allure/#_installing_a_commandline).

2. Запустите ваши тесты с ключем --alluredir для сохранения результатов в формате, понимаемом Allure:

```bash
pytest --alluredir=./allure-results
```

3. Сгенерируйте отчет Allure с помощью следующей команды:

```bash
allure generate ./allure-results
```

4. Посмотрите отчет Allure, открыв полученный HTML-файл в браузере:

```bash
allure open
```