import pytest
from services.normalizer import normalize_record

def test_etl_failure_invalid_price():
    with pytest.raises(Exception):
        normalize_record(
            asset_id="btc",
            name="Bitcoin",
            symbol="BTC",
            price_usd="INVALID",  # should fail
            source="test"
        )
