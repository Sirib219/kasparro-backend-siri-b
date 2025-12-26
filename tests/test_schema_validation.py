import pytest
from services.normalizer import normalize_record

def test_schema_mismatch_missing_field():
    with pytest.raises(TypeError):
        normalize_record(
            asset_id="btc",
            name="Bitcoin",
            # symbol missing
            price_usd=100,
            source="test"
        )
