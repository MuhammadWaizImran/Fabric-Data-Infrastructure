"""Run without Azure, credentials, pip installs, or network access."""
import argparse
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from analytics_platform.pipeline import run

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=ROOT / "data/sample/orders.jsonl")
    parser.add_argument("--output", type=Path, default=ROOT / "build/local-demo")
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), indent=2))
