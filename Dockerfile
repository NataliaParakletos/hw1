# Використовуємо базовий образ з підтримкою Python
FROM python:3.12

# Встановлюємо системні залежності, які можуть бути потрібні для застосунку
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Створюємо робочу директорію для копіювання файлів застосунку
WORKDIR /app

# Копіюємо файли застосунку у робочу директорію контейнера
COPY . /app

# Встановлюємо залежності Python за допомогою pip
RUN pip install --no-cache-dir -r requirements.txt

# Запускаємо застосунок при старті контейнера
CMD ["python", "chat_bot.py"]