from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from core.database import Base
from datetime import datetime


class RawData(Base):
    __tablename__ = "raw_data"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    payload = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class NormalizedAsset(Base):
    __tablename__ = "normalized_assets"

    asset_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    symbol = Column(String)
    price_usd = Column(Float)
    source = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class ETLCheckpoint(Base):
    __tablename__ = "etl_checkpoints"

    source = Column(String, primary_key=True)
    last_run_at = Column(DateTime)
    status = Column(String)
