FROM python:3.9-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN apt update
RUN apt install -y libpq-dev gcc
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD python main.py