"""Deterministic batch reference: validate, quarantine, deduplicate and aggregate."""
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
from .contracts import validate_order


def timestamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def transform(rows):
    latest, rejected = {}, []
    for row in rows:
        errors = validate_order(row)
        if errors:
            rejected.append({"row": row, "errors": errors})
            continue
        key = row["order_id"]
        # Stable tie-break: equal source timestamps do not depend on input order.
        rank = (timestamp(row["updated_at"]), json.dumps(row, sort_keys=True))
        if key not in latest or rank > latest[key][0]:
            latest[key] = (rank, row)
    silver = []
    daily = defaultdict(lambda: {"orders": 0, "quantity": 0, "revenue": Decimal("0")})
    for key in sorted(latest):
        row = dict(latest[key][1])
        revenue = (Decimal(str(row["unit_price"])) * row["quantity"]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        row["revenue"] = str(revenue)
        row["date"] = timestamp(row["order_date"]).date().isoformat()
        silver.append(row)
        aggregate = daily[row["date"]]
        aggregate["orders"] += 1
        aggregate["quantity"] += row["quantity"]
        aggregate["revenue"] += revenue
    gold = [{"date": day, **values, "revenue": str(values["revenue"]), "currency": "USD"}
            for day, values in sorted(daily.items())]
    return silver, gold, rejected


def run(source, output):
    source, output = Path(source), Path(output)
    rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
    silver, gold, rejected = transform(rows)
    output.mkdir(parents=True, exist_ok=True)
    for name, value in (("silver_orders", silver), ("gold_daily_sales", gold), ("quarantine", rejected)):
        (output / f"{name}.json").write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return {"input": len(rows), "silver": len(silver), "gold": len(gold), "rejected": len(rejected)}
