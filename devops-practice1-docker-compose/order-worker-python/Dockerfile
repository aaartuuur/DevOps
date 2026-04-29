FROM debian:trixie-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pika \
    python3-psycopg2 \
    python3-yaml \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python3", "worker.py"]