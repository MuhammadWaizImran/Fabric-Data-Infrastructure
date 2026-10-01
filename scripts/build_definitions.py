"""Generate reviewable Fabric notebook and pipeline files locally; no network access."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main():
    items = [
        {"name": "analytics_lakehouse", "type": "Lakehouse", "idBinding": "LAKEHOUSE_ID"},
        {"name": "analytics_warehouse", "type": "Warehouse", "idBinding": "WAREHOUSE_ID"},
        {"name": "analytics_operations", "type": "SQLDatabase", "idBinding": "SQL_DATABASE_ID"},
        {"name": "analytics_eventhouse", "type": "Eventhouse", "idBinding": "EVENTHOUSE_ID"},
        {"name": "telemetry", "type": "KQLDatabase", "idBinding": "KQL_DATABASE_ID", "creationPayload": {"databaseType": "ReadWrite", "parentEventhouseItemId": "{{EVENTHOUSE_ID}}"}},
    ]
    activities = []
    previous = None
    for index, source in enumerate(sorted((ROOT / "fabric/notebooks").glob("*.py")), 1):
        name = source.stem
        relative = f"fabric/definitions/notebooks/{name}.ipynb"
        def code_cell(text, metadata=None):
            return {"id": "parameters" if metadata else "implementation", "cell_type": "code", "execution_count": None, "metadata": metadata or {}, "outputs": [], "source": text.splitlines(keepends=True)}
        notebook = {"nbformat": 4, "nbformat_minor": 5,
            "metadata": {"language_info": {"name": "python"}, "kernelspec": {"name": "synapse_pyspark", "display_name": "Synapse PySpark"}},
            "cells": [code_cell('lakehouse_root = "abfss://{{WORKSPACE_ID}}@onelake.dfs.fabric.microsoft.com/{{LAKEHOUSE_ID}}"\n', {"tags": ["parameters"]}), code_cell(source.read_text(encoding="utf-8"))]}
        write(ROOT / relative, notebook)
        binding = f"NOTEBOOK_{index}_ID"
        items.append({"name": name, "type": "Notebook", "idBinding": binding, "format": "ipynb", "parts": [{"path": "artifact.content.ipynb", "source": relative}]})
        if index <= 3:
            activities.append({"name": name, "type": "TridentNotebook", "dependsOn": [] if previous is None else [{"activity": previous, "dependencyConditions": ["Succeeded"]}],
                "policy": {"timeout": "0.01:00:00", "retry": 2, "retryIntervalInSeconds": 30, "secureInput": False, "secureOutput": False},
                "typeProperties": {"notebookId": "{{" + binding + "}}", "workspaceId": "{{WORKSPACE_ID}}"}})
            previous = name
    write(ROOT / "fabric/definitions/pipelines/orders.json", {"properties": {"description": "Ordered full-snapshot demo: bronze, silver and gold. No schedule enabled by this definition.", "activities": activities}})
    items.append({"name": "orders_end_to_end", "type": "DataPipeline", "idBinding": "ORDERS_PIPELINE_ID", "parts": [{"path": "pipeline-content.json", "source": "fabric/definitions/pipelines/orders.json"}]})
    write(ROOT / "fabric/manifests/provider.json", {"scope": "provider", "items": items})
    consumer_notebook = {"nbformat": 4, "nbformat_minor": 5,
        "metadata": {"language_info": {"name": "python"}, "kernelspec": {"name": "synapse_pyspark", "display_name": "Synapse PySpark"}},
        "cells": [code_cell('lakehouse_root = "abfss://{{WORKSPACE_ID}}@onelake.dfs.fabric.microsoft.com/{{CONSUMER_LAKEHOUSE_ID}}"\n', {"tags": ["parameters"]}),
                  code_cell((ROOT / "fabric/consumer/read_shared_sales.py").read_text(encoding="utf-8"))]}
    write(ROOT / "fabric/definitions/consumer/read_shared_sales.ipynb", consumer_notebook)
    write(ROOT / "fabric/manifests/consumer.json", {"scope": "consumer", "items": [
        {"name": "shared_analytics", "type": "Lakehouse", "idBinding": "CONSUMER_LAKEHOUSE_ID"},
        {"name": "consumer_warehouse", "type": "Warehouse", "idBinding": "CONSUMER_WAREHOUSE_ID"},
        {"name": "consumer_operations", "type": "SQLDatabase", "idBinding": "CONSUMER_SQL_DATABASE_ID"},
        {"name": "consumer_eventhouse", "type": "Eventhouse", "idBinding": "CONSUMER_EVENTHOUSE_ID"},
        {"name": "consumer_telemetry", "type": "KQLDatabase", "creationPayload": {"databaseType": "ReadWrite", "parentEventhouseItemId": "{{CONSUMER_EVENTHOUSE_ID}}"}},
        {"name": "read_shared_sales", "type": "Notebook", "format": "ipynb", "parts": [{"path": "artifact.content.ipynb", "source": "fabric/definitions/consumer/read_shared_sales.ipynb"}]}
    ]})
    print(f"Generated {len(items)} provider item specifications and consumer manifest.")


if __name__ == "__main__":
    main()
