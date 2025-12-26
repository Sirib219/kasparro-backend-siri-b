import time
import uuid
from fastapi import APIRouter, Query
from sqlalchemy import text

from core.database import SessionLocal
from core.models import NormalizedAsset, ETLCheckpoint

router = APIRouter()


@router.get("/data")
def get_data(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    source: str | None = None
):
    start_time = time.time()
    db = SessionLocal()

    try:
        query = db.query(NormalizedAsset)

        if source:
            query = query.filter(NormalizedAsset.source == source)

        records = query.offset(offset).limit(limit).all()

        latency_ms = int((time.time() - start_time) * 1000)

        return {
            "request_id": str(uuid.uuid4()),
            "api_latency_ms": latency_ms,
            "count": len(records),
            "data": records
        }

    finally:
        db.close()


@router.get("/health")
def health_check():
    db = SessionLocal()

    try:
        # DB connectivity check
        db.execute(text("SELECT 1"))

        last_etl = (
            db.query(ETLCheckpoint)
            .order_by(ETLCheckpoint.last_run_at.desc())
            .first()
        )

        return {
            "database": "connected",
            "etl_last_run_status": last_etl.status if last_etl else "not_run",
            "etl_last_run_at": last_etl.last_run_at if last_etl else None
        }

    finally:
        db.close()


@router.get("/stats")
def etl_stats():
    db = SessionLocal()

    try:
        checkpoints = db.query(ETLCheckpoint).all()

        return {
            "sources": [
                {
                    "source": c.source,
                    "last_run_at": c.last_run_at,
                    "status": c.status
                }
                for c in checkpoints
            ]
        }

    finally:
        db.close()
