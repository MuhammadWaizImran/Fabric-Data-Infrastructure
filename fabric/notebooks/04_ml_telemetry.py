from pyspark.sql import functions as F
from sklearn.ensemble import IsolationForest
import mlflow
import mlflow.sklearn

# Upload generated JSONL to Files/landing/telemetry first. Bounded demo, not distributed training.
source = spark.read.json(lakehouse_root + "/Files/landing/telemetry/*.jsonl")
frame = source.select("event_id", "event_time", "temperature_c", "vibration_mm_s").dropna().orderBy("event_time").limit(100000).toPandas()
if len(frame) < 50:
    raise ValueError("At least 50 telemetry records are required for this demonstration")
cutoff = int(len(frame) * 0.8)
features = ["temperature_c", "vibration_mm_s"]
with mlflow.start_run(run_name="telemetry-isolation-forest"):
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(frame.iloc[:cutoff][features])
    holdout_scores = model.decision_function(frame.iloc[cutoff:][features])
    mlflow.log_params({"train_rows": cutoff, "holdout_rows": len(frame) - cutoff, "seed": 42})
    mlflow.log_metric("holdout_mean_score", float(holdout_scores.mean()))
    mlflow.sklearn.log_model(model, artifact_path="model")
    # Demonstration anomaly scores; no claim of validated predictive accuracy.
    frame["anomaly_score"] = model.decision_function(frame[features])
spark.createDataFrame(frame).write.format("delta").mode("overwrite").save(lakehouse_root + "/Tables/telemetry_scores")
