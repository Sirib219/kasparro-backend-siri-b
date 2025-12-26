import json
from datetime import datetime

from core.database import SessionLocal
from core.models import RawData, NormalizedAsset, ETLCheckpoint
from ingestion.coingecko_ingest import fetch_coingecko_data
from ingestion.coinpaprika_ingest import fetch_coinpaprika_data
from ingestion.csv_ingest import fetch_csv_data
from ingestion.schema_drift import detect_schema_drift
from services.normalizer import normalize_record


EXPECTED_SCHEMAS = {
    "coingecko": {
        "id",
        "name",
        "symbol",
        "current_price",
    },
    "coinpaprika": {
        "id",
        "name",
        "symbol",
        "quotes",
    },
    "csv": {
        "asset_id",
        "name",
        "symbol",
        "price_usd",
    },
}


def get_checkpoint(db, source: str):
    return (
        db.query(ETLCheckpoint)
        .filter(ETLCheckpoint.source == source)
        .first()
    )


def update_checkpoint(db, source: str, status: str):
    checkpoint = ETLCheckpoint(
        source=source,
        last_run_at=datetime.utcnow(),
        status=status,
    )
    db.merge(checkpoint)


def run_source_etl(source: str, records: list):
    db = SessionLocal()
    processed = 0
    schema_checked = False  # ✅ schema drift logged only once per source

    try:
        if not records:
            print(f"[ETL] No records found for source: {source}")
            update_checkpoint(db, source, "empty")
            db.commit()
            return 0

        # -------------------------
        # Raw data ingestion
        # -------------------------
        for record in records:
            # 🔍 Schema drift detection (once per source)
            if not schema_checked:
                detect_schema_drift(
                    source=source,
                    expected_fields=EXPECTED_SCHEMAS[source],
                    incoming_record=record,
                )
                schema_checked = True

            raw = RawData(
                source=source,
                payload=json.dumps(record),
            )
            db.add(raw)

        db.commit()

        # -------------------------
        # Normalization
        # -------------------------
        for record in records:
            if source == "coingecko":
                normalized = normalize_record(
                    asset_id=record["id"],
                    name=record["name"],
                    symbol=record["symbol"],
                    price_usd=record["current_price"],
                    source=source,
                )

            elif source == "coinpaprika":
                normalized = normalize_record(
                    asset_id=record["id"],
                    name=record["name"],
                    symbol=record["symbol"],
                    price_usd=record["quotes"]["USD"]["price"],
                    source=source,
                )

            elif source == "csv":
                normalized = normalize_record(
                    asset_id=record["asset_id"],
                    name=record["name"],
                    symbol=record["symbol"],
                    price_usd=float(record["price_usd"]),
                    source=source,
                )

            db.merge(
                NormalizedAsset(
                    asset_id=normalized.asset_id,
                    name=normalized.name,
                    symbol=normalized.symbol,
                    price_usd=normalized.price_usd,
                    source=normalized.source,
                    timestamp=normalized.timestamp,
                )
            )
            processed += 1

        update_checkpoint(db, source, "success")
        db.commit()

        print(f"[ETL] {source} → {processed} records processed")

    except Exception as e:
        db.rollback()
        update_checkpoint(db, source, "failed")
        db.commit()
        print(f"[ETL] ERROR in {source}: {e}")
        raise

    finally:
        db.close()

    return processed


def run_etl():
    print("[ETL] Starting ETL process")

    cg = fetch_coingecko_data()
    print("CoinGecko records:", len(cg))

    cp = fetch_coinpaprika_data()
    print("CoinPaprika records:", len(cp))

    csv = fetch_csv_data()
    print("CSV records:", len(csv))

    run_source_etl("coingecko", cg)
    run_source_etl("coinpaprika", cp)
    run_source_etl("csv", csv)

    print("[ETL] ETL process completed successfully")


if __name__ == "__main__":
    run_etl()
