FROM python:3.10-slim

WORKDIR /app

COPY ./src /app
COPY ./src/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "bot/telegramBot.py"]
