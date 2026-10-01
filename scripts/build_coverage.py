"""Inventory the actual SVG labels and map each to an explicit artifact/status."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]

GROUPS = [
    (["AWS Kinesis", "Amazon S3", "Amazon Web Services"], "template+binding", ["infra/aws/sources.cloudformation.json", "fabric/connections/catalog.json", "fabric/eventstreams/topology.json"]),
    (["Google Cloud", "Google Cloud Pub/Sub", "Google Cloud Storage"], "template+binding", ["infra/gcp/main.tf", "fabric/connections/catalog.json", "fabric/eventstreams/topology.json"]),
    (["Azure Cosmos DB"], "template+binding", ["infra/azure/modules/sources.bicep", "sources/cosmos/orders.json", "fabric/connections/mirroring.md"]),
    (["Azure Databse for PostgresSQL"], "template+binding", ["infra/azure/modules/sources.bicep", "sources/postgresql/schema.sql", "fabric/connections/mirroring.md"]),
    (["Azure SQL Database"], "template+binding", ["infra/azure/modules/sources.bicep", "sources/azure-sql/schema.sql", "fabric/connections/mirroring.md"]),
    (["Azure Databricks"], "template+binding", ["infra/azure/modules/sources.bicep", "sources/databricks/seed_orders.py", "fabric/connections/mirroring.md"]),
    (["Snowflake"], "code+binding", ["sources/snowflake/setup.sql", "fabric/connections/mirroring.md"]),
    (["On-premises datacenter"], "template+binding", ["sources/onprem/compose.yaml", "sources/azure-sql/schema.sql", "fabric/connections/catalog.json"]),
    (["Azure Data Explorer"], "template+binding", ["infra/azure/modules/intelligence.bicep", "fabric/kql/003_onelake.md"]),
    (["Azure Event Hubs", "IoT Hub"], "template+binding", ["infra/azure/modules/platform.bicep", "fabric/eventstreams/topology.json", "scripts/stream_producer.py"]),
    (["Blob storage", "Data Lake Storage"], "template+binding", ["infra/azure/modules/platform.bicep", "fabric/connections/shortcuts.md"]),
    (["Dataverse"], "configuration-contract", ["sources/dataverse/README.md"]),
    (["Azure DevOps"], "validation-ci", ["azure-pipelines.yml"]),
    (["GitHub"], "validation-ci", [".github/workflows/validate.yml"]),
    (["Azure Key Vault"], "template+binding", ["infra/azure/modules/platform.bicep", "docs/deployment.md"]),
    (["Azure Policy"], "template", ["infra/azure/policy.bicep", "infra/azure/modules/policy-assignment.bicep"]),
    (["Microsoft Entra ID"], "configuration-contract", ["governance/access-matrix.csv", "docs/deployment.md"]),
    (["Microsoft Purview"], "template+binding", ["infra/azure/modules/platform.bicep", "governance/purview.md"]),
    (["Cost Management"], "template+configuration", ["infra/azure/main.bicep", "monitoring/README.md"]),
    (["Workspace monitoring"], "configuration-contract", ["monitoring/README.md", "monitoring/alerts.json"]),
    (["Consumer tenant", "Cross-tenant OneLake data share"], "template+configuration", ["fabric/manifests/consumer.json", "fabric/consumer/README.md"]),
    (["Provider tenant"], "template+configuration", ["fabric/manifests/provider.json", "docs/deployment.md"]),
    (["Copilot", "Copilot in Fabric"], "configuration-contract", ["docs/deployment.md", "ai/data-agent/instructions.md"]),
    (["Data agent(preview)"], "configuration-contract", ["ai/data-agent/instructions.md", "ai/data-agent/evaluation.json"]),
    (["Microsoft Foundry"], "template+configuration", ["infra/azure/modules/intelligence.bicep", "ai/foundry/README.md"]),
    (["Machine Learning", "Data Science", "Enrich"], "code+template", ["ml/train.py", "ml/job.yml", "fabric/notebooks/04_ml_telemetry.py", "ai/foundry/README.md"]),
    (["Data Engineer", "Notebook", "Process"], "code+template", ["fabric/notebooks/01_bronze_orders.py", "fabric/notebooks/02_silver_orders.py", "fabric/notebooks/03_gold_sales.py"]),
    (["Data Factory", "Ingest"], "code+template", ["fabric/definitions/pipelines/orders.json", "fabric/connections/catalog.json"]),
    (["Dataflow Gen2 in Fabric"], "code+binding", ["fabric/dataflows/daily_sales.pq", "fabric/dataflows/README.md"]),
    (["Data Warehouse", "Stored procedure"], "code+template", ["fabric/manifests/provider.json", "fabric/sql/warehouse/001_tables.sql", "fabric/sql/warehouse/002_publish.sql"]),
    (["SQL database in Fabric", "Databases"], "code+template", ["fabric/manifests/provider.json", "fabric/sql/operations/001_tables.sql"]),
    (["SQL analytics endpoint"], "service-managed+code", ["fabric/sql/lakehouse/quality_checks.sql", "docs/architecture.md"]),
    (["Eventhouse", "Real-Time Intelligence"], "code+template", ["fabric/manifests/provider.json", "fabric/kql/001_schema.kql", "fabric/kql/002_dashboard_queries.kql"]),
    (["Real-Time Intelligence dashboard"], "authoring-contract", ["fabric/reports/realtime-dashboard-spec.json", "fabric/kql/002_dashboard_queries.kql"]),
    (["Eventstream", "Streaming data"], "template+binding", ["fabric/manifests/streaming.json", "fabric/eventstreams/eventstream.json", "fabric/eventstreams/topology.json"]),
    (["Power BI"], "authoring-contract", ["fabric/reports/report-spec.json", "fabric/reports/theme.json", "fabric/manifests/serving.json"]),
    (["Semantic model (Direct Lake)"], "template", ["fabric/semantic-model/model.bim", "fabric/manifests/serving.json"]),
    (["GraphQL API"], "query+configuration-contract", ["fabric/graphql/queries.graphql", "fabric/graphql/README.md"]),
    (["Mirrored database", "Mirroring", "Mirror"], "configuration-contract", ["fabric/connections/mirroring.md", "fabric/connections/catalog.json"]),
    (["Shortcuts"], "configuration-contract", ["fabric/connections/shortcuts.md", "fabric/consumer/README.md"]),
    (["Lakehouse", "OneLake", "Store"], "template+service-managed", ["fabric/manifests/provider.json", "scripts/upload_onelake.py", "docs/architecture.md"]),
    (["Data source", "Structured andsemistructured data"], "fixtures+configuration", ["fabric/connections/catalog.json", "data/sample/orders.jsonl", "data/sample/telemetry.jsonl"]),
    (["Platform", "Serve"], "cross-cutting-design", ["docs/architecture.md", "governance/access-matrix.csv", "docs/deployment.md"]),
]


def main():
    tree = ET.parse(ROOT / "docs/architecture/azure-analytics-end-to-end.svg")
    labels = set("".join(node.itertext()).strip() for node in tree.iter("{http://www.w3.org/2000/svg}text"))
    mapped = {}
    for names, status, paths in GROUPS:
        for name in names:
            if name in mapped:
                raise ValueError(f"Duplicate mapping: {name}")
            mapped[name] = {"label": name, "status": status, "artifacts": paths}
    if labels != set(mapped):
        raise ValueError(f"Missing={labels-set(mapped)}; extra={set(mapped)-labels}")
    rows = [mapped[label] for label in sorted(labels)]
    (ROOT / "docs/coverage.json").write_text(json.dumps({"uniqueLabelCount": len(labels), "components": rows}, indent=2) + "\n", encoding="utf-8")
    lines = ["# Original architecture coverage", "", f"All **{len(labels)} unique text labels** in the supplied SVG are mapped below.",
             "Repeated occurrences remain visible in the unchanged original diagram. A mapped", "label means repository representation, **not completed cloud deployment**.", "",
             "`template` requires environment bindings; `configuration-contract`/`authoring-contract`",
             "means explicit setup instructions/specification, not a native deployed artifact.", "", "| Original diagram label | Artifact status | Repository artifacts |", "|---|---|---|"]
    for row in rows:
        links = ", ".join(f"[{path}](../{path})" for path in row["artifacts"])
        lines.append(f"| {row['label']} | {row['status']} | {links} |")
    (ROOT / "docs/coverage.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Mapped {len(labels)} original SVG labels.")


if __name__ == "__main__":
    main()
