# Используем официальный образ Python в качестве базового
FROM python:3.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы проекта в контейнер
COPY . /app/

# Открываем порт для Django
EXPOSE 8000
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Команда для запуска Django сервера
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
