# WeatherApp

WeatherApp - это веб-приложение на Django для предоставления информации о погоде.

### Требования

- Python 3.12
- pip
- Docker (опционально, для контейнеризации)

### Шаги установки

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/HamfriLegend/WeatherApp.git
    cd WeatherApp
    ```

2. Создайте и активируйте виртуальное окружение (опционально):

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Для Windows: `.venv\Scripts\activate`
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Примените миграции базы данных:

    ```bash
    python manage.py migrate
    ```

5. Создайте суперпользователя (опционально):

    ```bash
    python manage.py createsuperuser
    ```

6. Запустите сервер разработки:

    ```bash
    python manage.py runserver
    ```

7. Откройте браузер и перейдите по адресу `http://127.0.0.1:8000`.

### Docker

Для развертывания приложения с использованием Docker:

### Docker Compose

Для развертывания приложения с использованием Docker Compose:

1. Запустите Docker Compose:

    ```bash
    docker-compose up --build
    ```

2. Откройте браузер и перейдите по адресу `http://127.0.0.1:8000`.
