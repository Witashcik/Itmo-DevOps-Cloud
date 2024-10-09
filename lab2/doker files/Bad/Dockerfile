# Использование слишком тяжёлых базовых образов
FROM ubuntu:latest

# Установка зависимостей без очистки кэша
RUN apt-get update && apt-get install -y python3

# Отсутствие указания конкретных версий пакетов
RUN pip install flask