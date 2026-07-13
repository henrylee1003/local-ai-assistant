FROM python:3.11-slim

WORKDIR /app

COPY . .

CMD ["python3", "app.py"]
RUN apt-get update && apt-get install -y tzdata && rm -rf /var/lib/apt/lists/*
