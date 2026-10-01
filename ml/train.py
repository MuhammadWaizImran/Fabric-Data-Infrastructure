"""Optional local/Azure ML demonstration. No model is deployed by training."""
import argparse
import json
from pathlib import Path


def train(source, output):
    import joblib
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import IsolationForest
    data = pd.read_json(source, lines=True)
    features = ["temperature_c", "vibration_mm_s"]
    data = data.sort_values("event_time").drop_duplicates("event_id").dropna(subset=features)
    data = data[np.isfinite(data[features]).all(axis=1)]
    if len(data) < 50:
        raise ValueError("Need at least 50 distinct finite telemetry records")
    cutoff = int(len(data) * 0.8)
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(data.iloc[:cutoff][features])
    holdout = model.decision_function(data.iloc[cutoff:][features])
    metrics = {"train_rows": cutoff, "holdout_rows": len(data) - cutoff,
               "holdout_mean_score": float(holdout.mean()), "holdout_flag_rate": float((holdout < 0).mean()),
               "interpretation": "Unsupervised demonstration on synthetic data; no labeled accuracy claim."}
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output / "model.joblib")
    (output / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    (output / "feature-contract.json").write_text(json.dumps({"features": features, "schema_version": 1}), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    train(args.input, args.output)
