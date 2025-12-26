import logging
from typing import Set, Dict, Union

logger = logging.getLogger("schema_drift")


def detect_schema_drift(
    source: str,
    expected_fields: Set[str],
    incoming_record: Union[Dict, Set]
) -> float:
    """
    Detect schema drift between expected fields and incoming record.

    Returns:
        confidence score between 0.0 and 1.0
    """

    # ✅ Support both dict and set (required for tests)
    if isinstance(incoming_record, dict):
        incoming_fields = set(incoming_record.keys())
    else:
        incoming_fields = set(incoming_record)

    missing = expected_fields - incoming_fields
    extra = incoming_fields - expected_fields

    total_expected = len(expected_fields)
    matched = total_expected - len(missing)

    confidence = matched / total_expected if total_expected > 0 else 1.0

    if missing or extra:
        logger.warning(
            "[SCHEMA DRIFT] Source=%s | Confidence=%.2f | Missing=%s | Extra=%s",
            source,
            confidence,
            list(missing),
            list(extra),
        )

    return confidence
