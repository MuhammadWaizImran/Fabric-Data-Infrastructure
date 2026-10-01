"""Data rules shared by the local reference pipeline and its tests."""
from datetime import datetime
from decimal import Decimal, InvalidOperation
import math


def validate_order(row):
    errors = []
    for key in ("order_id", "customer_id", "product_id", "updated_at", "order_date"):
        if not isinstance(row.get(key), str) or not row[key].strip():
            errors.append(f"{key}: required string")
    for key in ("order_date", "updated_at"):
        try:
            value = datetime.fromisoformat(str(row.get(key, "")).replace("Z", "+00:00"))
            if value.tzinfo is None:
                errors.append(f"{key}: timezone required")
        except ValueError:
            errors.append(f"{key}: invalid timestamp")
    quantity = row.get("quantity")
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        errors.append("quantity: positive integer required")
    try:
        amount = Decimal(str(row.get("unit_price")))
        if not amount.is_finite() or amount < 0:
            errors.append("unit_price: finite non-negative amount required")
    except InvalidOperation:
        errors.append("unit_price: invalid amount")
    if row.get("currency") != "USD":
        errors.append("currency: this sample aggregates USD only")
    return errors


def validate_event(row):
    errors = []
    for key in ("event_id", "device_id"):
        if not isinstance(row.get(key), str) or not row[key].strip():
            errors.append(f"{key}: required string")
    try:
        stamp = datetime.fromisoformat(str(row.get("event_time", "")).replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            errors.append("event_time: timezone required")
    except ValueError:
        errors.append("event_time: invalid timestamp")
    for key in ("temperature_c", "vibration_mm_s"):
        value = row.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            errors.append(f"{key}: finite number required")
    if row.get("schema_version") != 1:
        errors.append("schema_version: expected 1")
    return errors
