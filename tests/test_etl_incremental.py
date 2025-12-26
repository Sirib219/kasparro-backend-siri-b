from core.models import ETLCheckpoint

def test_checkpoint_write(db_session):
    checkpoint = ETLCheckpoint(
        source="coingecko",
        status="success"
    )

    # ✅ merge instead of add (idempotent write)
    db_session.merge(checkpoint)
    db_session.commit()

    saved = db_session.get(ETLCheckpoint, "coingecko")
    assert saved is not None
    assert saved.status == "success"
