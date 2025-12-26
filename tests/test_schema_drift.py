from ingestion.schema_drift import detect_schema_drift

def test_schema_drift_detection():
    expected = {"id", "name", "symbol", "price"}
    incoming = {"id", "symbol", "price_usd"}

    confidence = detect_schema_drift("test", expected, incoming)

    assert confidence < 1.0
