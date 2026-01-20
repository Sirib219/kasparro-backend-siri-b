# -------- BUILDER STAGE --------
FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# -------- RUNTIME STAGE --------
FROM python:3.10-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY --from=builder /install /usr/local
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
