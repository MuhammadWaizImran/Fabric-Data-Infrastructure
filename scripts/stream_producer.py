"""Local JSONL by default; --send explicitly sends to configured Azure Event Hubs."""
import argparse
from datetime import datetime, timezone, timedelta
import json
import os
from pathlib import Path
import random
import sys
import uuid
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from analytics_platform.contracts import validate_event


def events(count, seed=42):
    rng = random.Random(seed)
    start = datetime(2026, 9, 1, tzinfo=timezone.utc)
    for index in range(count):
        yield {"event_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, f"fabric-demo:{seed}:{index}")),
               "device_id": f"D{index % 10:02d}",
               "event_time": (start + timedelta(seconds=index)).isoformat(),
               "temperature_c": round(rng.uniform(20, 95), 2),
               "vibration_mm_s": round(rng.uniform(0.1, 9), 2), "schema_version": 1}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "build/telemetry.jsonl")
    args = parser.parse_args()
    if not 1 <= args.count <= 100000:
        parser.error("--count must be between 1 and 100000")
    rows = list(events(args.count, args.seed))
    if args.send:
        # Live timestamps; stable IDs allow deliberate replay/deduplication exercises.
        for row in rows:
            row["event_time"] = datetime.now(timezone.utc).isoformat()
    for row in rows:
        if validate_event(row):
            raise ValueError("Invalid generated event")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    if args.send:
        from azure.identity import DefaultAzureCredential
        from azure.eventhub import EventData, EventHubProducerClient
        namespace = os.environ["EVENTHUB_FULLY_QUALIFIED_NAMESPACE"]
        hub = os.environ["EVENTHUB_NAME"]
        with DefaultAzureCredential() as credential:
            with EventHubProducerClient(fully_qualified_namespace=namespace, eventhub_name=hub, credential=credential) as producer:
                batch = producer.create_batch()
                for row in rows:
                    event = EventData(json.dumps(row))
                    try:
                        batch.add(event)
                    except ValueError:
                        producer.send_batch(batch)
                        batch = producer.create_batch()
                        batch.add(event)
                if len(batch):
                    producer.send_batch(batch)
        print(f"Sent {len(rows)} events; duplicate-safe consumption is required.")
    else:
        print(f"Wrote {len(rows)} events locally to {args.output}")


if __name__ == "__main__":
    main()
