#!/bin/sh
set -e

echo "[STARTUP] Checking DATABASE_URL..."

python - <<EOF
import os
assert os.getenv("DATABASE_URL"), "DATABASE_URL not set"
print("[STARTUP] DATABASE_URL found")
EOF

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
exec uvicorn api.main:app --host 0.0.0.0 --port "${PORT:-8000}"
