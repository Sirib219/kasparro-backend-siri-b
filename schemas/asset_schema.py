from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AssetSchema(BaseModel):
    asset_id: str
    name: str
    symbol: str
    price_usd: float
    source: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
