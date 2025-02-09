FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN apt update && apt install -y libpq-dev gcc

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

CMD python main.py