import copy
import json
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from analytics_platform.contracts import validate_event, validate_order
from analytics_platform.pipeline import transform


class ProcessingTests(unittest.TestCase):
    def setUp(self):
        self.rows = [json.loads(x) for x in (ROOT / "data/sample/orders.jsonl").read_text().splitlines()]

    def test_totals_and_quarantine(self):
        silver, gold, bad = transform(self.rows)
        self.assertEqual(len(silver), 3)
        self.assertEqual([x["revenue"] for x in gold], ["159.85", "200.00"])
        self.assertEqual(len(bad), 1)

    def test_replays_and_order_do_not_change_results(self):
        first = transform(self.rows)[0:2]
        self.assertEqual(first, transform(list(reversed(self.rows)) * 2)[0:2])

    def test_latest_means_timestamp_not_string_order(self):
        old = copy.deepcopy(self.rows[0])
        new = copy.deepcopy(old)
        old["updated_at"] = "2026-09-01T11:00:00+02:00"
        new["updated_at"] = "2026-09-01T10:00:00Z"
        new["quantity"] = 5
        self.assertEqual(transform([old, new])[0][0]["quantity"], 5)

    def test_invalid_prices_and_quantities(self):
        for price in ("NaN", "Infinity", "-1", None):
            row = {**self.rows[0], "unit_price": price}
            self.assertTrue(validate_order(row))
        self.assertTrue(validate_order({**self.rows[0], "quantity": True}))
        self.assertTrue(validate_order({**self.rows[0], "currency": "PKR"}))

    def test_event_contract(self):
        row = json.loads((ROOT / "data/sample/telemetry.jsonl").read_text().splitlines()[0])
        self.assertEqual(validate_event(row), [])
        self.assertTrue(validate_event({**row, "temperature_c": float("nan")}))
        self.assertTrue(validate_event({**row, "event_time": "2026-09-01"}))


if __name__ == "__main__":
    unittest.main()
