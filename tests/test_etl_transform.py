from services.normalizer import normalize_record

def test_normalize_record():
    record = normalize_record(
        asset_id="btc",
        name="Bitcoin",
        symbol="BTC",
        price_usd=50000,
        source="test"
    )

    assert record.asset_id == "btc"
    assert record.name == "Bitcoin"
    assert record.symbol == "BTC"
    assert record.price_usd == 50000
    assert record.source == "test"
    assert record.timestamp is not None
