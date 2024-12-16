# Использование легковесных образов
FROM Python:3.9-alpine

# Очистка кэша после установки пакетов
RUN apt-get update && apt-get install -y python3 && rm -rf /var/lib/apt/lists*

# Указание конкретных версий пакетов
RUN pip install flask==2.0.1