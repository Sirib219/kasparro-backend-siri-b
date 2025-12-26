from schemas.asset_schema import AssetSchema
from datetime import datetime


def normalize_record(
    asset_id: str,
    name: str,
    symbol: str,
    price_usd: float,
    source: str
) -> AssetSchema:
    """
    Converts raw API/CSV data into a unified schema
    """
    return AssetSchema(
        asset_id=str(asset_id),
        name=name,
        symbol=symbol.upper(),
        price_usd=float(price_usd),
        source=source,
        timestamp=datetime.utcnow()
    )
