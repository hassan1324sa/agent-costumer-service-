FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r src/requirements.txt

CMD ["python", "src/bot/telegramBot.py"]
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r src/requirements.txt

CMD ["python", "src/bot/telegramBot.py"]
