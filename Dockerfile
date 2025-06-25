# Використовуємо офіційний образ Python
FROM python:3.10

# Створюємо папку в контейнері
WORKDIR /app

# Копіюємо всі файли у контейнер
COPY . /app

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Запускаємо бота
CMD ["python", "bot.py"]
