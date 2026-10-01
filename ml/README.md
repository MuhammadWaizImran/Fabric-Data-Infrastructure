# ML enrichment

Two execution paths represent the diagram: Fabric notebook training/MLflow
(`fabric/notebooks/04_ml_telemetry.py`) and a separate Azure ML command job here.
Use the same event feature contract; avoid training both by default.

Local demonstration (optional ML dependencies required):

```powershell
python scripts/stream_producer.py --count 1000
python ml/train.py --input build/telemetry.jsonl --output build/ml
```

The data is synthetic. A temporal holdout measures score distribution, not business
accuracy. Before production: use real history, labeled incidents where available,
fit preprocessing only on training data, evaluate device/time leakage, choose an
alert threshold, and monitor drift. Scoring is separate from device control.

For Fabric, upload JSONL to `Files/landing/telemetry`, select an MLflow experiment,
run the notebook and inspect `telemetry_scores`. For Azure ML, configure managed
networking, storage/Key Vault RBAC, compute and job input paths before submission.
`job.yml` uses a local URI upload for demonstration. Link approved ADLS/OneLake
locations for shared production data. Register/version a validated model and add
an endpoint only after an actual serving requirement is defined.
