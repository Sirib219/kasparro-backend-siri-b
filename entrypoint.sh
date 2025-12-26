#!/bin/sh
set -e

echo "[STARTUP] Waiting for DB..."

until python - <<EOF
import psycopg2, os
psycopg2.connect(os.environ["DATABASE_URL"])
print("[STARTUP] DB is ready")
EOF
do
  sleep 2
done

echo "[STARTUP] Creating database tables..."
python - <<EOF
from core.database import Base, engine
from core.models import RawData, NormalizedAsset, ETLCheckpoint
Base.metadata.create_all(bind=engine)
print("[STARTUP] Tables created")
EOF

echo "[STARTUP] Running ETL..."
python ingestion/etl_runner.py || echo "[WARN] ETL failed"

echo "[STARTUP] Starting API..."
PORT=${PORT:-8000}
exec uvicorn api.main:app --host 0.0.0.0 --port $PORT
