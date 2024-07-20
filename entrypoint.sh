#!/bin/bash
set -e

# Выполняем миграции
python manage.py migrate

# Сбор статических файлов (если требуется)
python manage.py collectstatic --noinput

# Запускаем сервер Django
exec "$@"
