FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN apt update && apt install -y libpq-dev gcc

RUN pip install uv && uv pip install --system -r requirements.txt && pip cache purge && uv cache clean

COPY . .

CMD python main.py