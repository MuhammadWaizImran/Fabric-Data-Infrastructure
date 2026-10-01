# Original architecture coverage

All **66 unique text labels** in the supplied SVG are mapped below.
Repeated occurrences remain visible in the unchanged original diagram. A mapped
label means repository representation, **not completed cloud deployment**.

`template` requires environment bindings; `configuration-contract`/`authoring-contract`
means explicit setup instructions/specification, not a native deployed artifact.

| Original diagram label | Artifact status | Repository artifacts |
|---|---|---|
| AWS Kinesis | template+binding | [infra/aws/sources.cloudformation.json](../infra/aws/sources.cloudformation.json), [fabric/connections/catalog.json](../fabric/connections/catalog.json), [fabric/eventstreams/topology.json](../fabric/eventstreams/topology.json) |
| Amazon S3 | template+binding | [infra/aws/sources.cloudformation.json](../infra/aws/sources.cloudformation.json), [fabric/connections/catalog.json](../fabric/connections/catalog.json), [fabric/eventstreams/topology.json](../fabric/eventstreams/topology.json) |
| Amazon Web Services | template+binding | [infra/aws/sources.cloudformation.json](../infra/aws/sources.cloudformation.json), [fabric/connections/catalog.json](../fabric/connections/catalog.json), [fabric/eventstreams/topology.json](../fabric/eventstreams/topology.json) |
| Azure Cosmos DB | template+binding | [infra/azure/modules/sources.bicep](../infra/azure/modules/sources.bicep), [sources/cosmos/orders.json](../sources/cosmos/orders.json), [fabric/connections/mirroring.md](../fabric/connections/mirroring.md) |
| Azure Data Explorer | template+binding | [infra/azure/modules/intelligence.bicep](../infra/azure/modules/intelligence.bicep), [fabric/kql/003_onelake.md](../fabric/kql/003_onelake.md) |
| Azure Databricks | template+binding | [infra/azure/modules/sources.bicep](../infra/azure/modules/sources.bicep), [sources/databricks/seed_orders.py](../sources/databricks/seed_orders.py), [fabric/connections/mirroring.md](../fabric/connections/mirroring.md) |
| Azure Databse for PostgresSQL | template+binding | [infra/azure/modules/sources.bicep](../infra/azure/modules/sources.bicep), [sources/postgresql/schema.sql](../sources/postgresql/schema.sql), [fabric/connections/mirroring.md](../fabric/connections/mirroring.md) |
| Azure DevOps | validation-ci | [azure-pipelines.yml](../azure-pipelines.yml) |
| Azure Event Hubs | template+binding | [infra/azure/modules/platform.bicep](../infra/azure/modules/platform.bicep), [fabric/eventstreams/topology.json](../fabric/eventstreams/topology.json), [scripts/stream_producer.py](../scripts/stream_producer.py) |
| Azure Key Vault | template+binding | [infra/azure/modules/platform.bicep](../infra/azure/modules/platform.bicep), [docs/deployment.md](../docs/deployment.md) |
| Azure Policy | template | [infra/azure/policy.bicep](../infra/azure/policy.bicep), [infra/azure/modules/policy-assignment.bicep](../infra/azure/modules/policy-assignment.bicep) |
| Azure SQL Database | template+binding | [infra/azure/modules/sources.bicep](../infra/azure/modules/sources.bicep), [sources/azure-sql/schema.sql](../sources/azure-sql/schema.sql), [fabric/connections/mirroring.md](../fabric/connections/mirroring.md) |
| Blob storage | template+binding | [infra/azure/modules/platform.bicep](../infra/azure/modules/platform.bicep), [fabric/connections/shortcuts.md](../fabric/connections/shortcuts.md) |
| Consumer tenant | template+configuration | [fabric/manifests/consumer.json](../fabric/manifests/consumer.json), [fabric/consumer/README.md](../fabric/consumer/README.md) |
| Copilot | configuration-contract | [docs/deployment.md](../docs/deployment.md), [ai/data-agent/instructions.md](../ai/data-agent/instructions.md) |
| Copilot in Fabric | configuration-contract | [docs/deployment.md](../docs/deployment.md), [ai/data-agent/instructions.md](../ai/data-agent/instructions.md) |
| Cost Management | template+configuration | [infra/azure/main.bicep](../infra/azure/main.bicep), [monitoring/README.md](../monitoring/README.md) |
| Cross-tenant OneLake data share | template+configuration | [fabric/manifests/consumer.json](../fabric/manifests/consumer.json), [fabric/consumer/README.md](../fabric/consumer/README.md) |
| Data Engineer | code+template | [fabric/notebooks/01_bronze_orders.py](../fabric/notebooks/01_bronze_orders.py), [fabric/notebooks/02_silver_orders.py](../fabric/notebooks/02_silver_orders.py), [fabric/notebooks/03_gold_sales.py](../fabric/notebooks/03_gold_sales.py) |
| Data Factory | code+template | [fabric/definitions/pipelines/orders.json](../fabric/definitions/pipelines/orders.json), [fabric/connections/catalog.json](../fabric/connections/catalog.json) |
| Data Lake Storage | template+binding | [infra/azure/modules/platform.bicep](../infra/azure/modules/platform.bicep), [fabric/connections/shortcuts.md](../fabric/connections/shortcuts.md) |
| Data Science | code+template | [ml/train.py](../ml/train.py), [ml/job.yml](../ml/job.yml), [fabric/notebooks/04_ml_telemetry.py](../fabric/notebooks/04_ml_telemetry.py), [ai/foundry/README.md](../ai/foundry/README.md) |
| Data Warehouse | code+template | [fabric/manifests/provider.json](../fabric/manifests/provider.json), [fabric/sql/warehouse/001_tables.sql](../fabric/sql/warehouse/001_tables.sql), [fabric/sql/warehouse/002_publish.sql](../fabric/sql/warehouse/002_publish.sql) |
| Data agent(preview) | configuration-contract | [ai/data-agent/instructions.md](../ai/data-agent/instructions.md), [ai/data-agent/evaluation.json](../ai/data-agent/evaluation.json) |
| Data source | fixtures+configuration | [fabric/connections/catalog.json](../fabric/connections/catalog.json), [data/sample/orders.jsonl](../data/sample/orders.jsonl), [data/sample/telemetry.jsonl](../data/sample/telemetry.jsonl) |
| Databases | code+template | [fabric/manifests/provider.json](../fabric/manifests/provider.json), [fabric/sql/operations/001_tables.sql](../fabric/sql/operations/001_tables.sql) |
| Dataflow Gen2 in Fabric | code+binding | [fabric/dataflows/daily_sales.pq](../fabric/dataflows/daily_sales.pq), [fabric/dataflows/README.md](../fabric/dataflows/README.md) |
| Dataverse | configuration-contract | [sources/dataverse/README.md](../sources/dataverse/README.md) |
| Enrich | code+template | [ml/train.py](../ml/train.py), [ml/job.yml](../ml/job.yml), [fabric/notebooks/04_ml_telemetry.py](../fabric/notebooks/04_ml_telemetry.py), [ai/foundry/README.md](../ai/foundry/README.md) |
| Eventhouse | code+template | [fabric/manifests/provider.json](../fabric/manifests/provider.json), [fabric/kql/001_schema.kql](../fabric/kql/001_schema.kql), [fabric/kql/002_dashboard_queries.kql](../fabric/kql/002_dashboard_queries.kql) |
| Eventstream | template+binding | [fabric/manifests/streaming.json](../fabric/manifests/streaming.json), [fabric/eventstreams/eventstream.json](../fabric/eventstreams/eventstream.json), [fabric/eventstreams/topology.json](../fabric/eventstreams/topology.json) |
| GitHub | validation-ci | [.github/workflows/validate.yml](../.github/workflows/validate.yml) |
| Google Cloud | template+binding | [infra/gcp/main.tf](../infra/gcp/main.tf), [fabric/connections/catalog.json](../fabric/connections/catalog.json), [fabric/eventstreams/topology.json](../fabric/eventstreams/topology.json) |
| Google Cloud Pub/Sub | template+binding | [infra/gcp/main.tf](../infra/gcp/main.tf), [fabric/connections/catalog.json](../fabric/connections/catalog.json), [fabric/eventstreams/topology.json](../fabric/eventstreams/topology.json) |
| Google Cloud Storage | template+binding | [infra/gcp/main.tf](../infra/gcp/main.tf), [fabric/connections/catalog.json](../fabric/connections/catalog.json), [fabric/eventstreams/topology.json](../fabric/eventstreams/topology.json) |
| GraphQL API | query+configuration-contract | [fabric/graphql/queries.graphql](../fabric/graphql/queries.graphql), [fabric/graphql/README.md](../fabric/graphql/README.md) |
| Ingest | code+template | [fabric/definitions/pipelines/orders.json](../fabric/definitions/pipelines/orders.json), [fabric/connections/catalog.json](../fabric/connections/catalog.json) |
| IoT Hub | template+binding | [infra/azure/modules/platform.bicep](../infra/azure/modules/platform.bicep), [fabric/eventstreams/topology.json](../fabric/eventstreams/topology.json), [scripts/stream_producer.py](../scripts/stream_producer.py) |
| Lakehouse | template+service-managed | [fabric/manifests/provider.json](../fabric/manifests/provider.json), [scripts/upload_onelake.py](../scripts/upload_onelake.py), [docs/architecture.md](../docs/architecture.md) |
| Machine Learning | code+template | [ml/train.py](../ml/train.py), [ml/job.yml](../ml/job.yml), [fabric/notebooks/04_ml_telemetry.py](../fabric/notebooks/04_ml_telemetry.py), [ai/foundry/README.md](../ai/foundry/README.md) |
| Microsoft Entra ID | configuration-contract | [governance/access-matrix.csv](../governance/access-matrix.csv), [docs/deployment.md](../docs/deployment.md) |
| Microsoft Foundry | template+configuration | [infra/azure/modules/intelligence.bicep](../infra/azure/modules/intelligence.bicep), [ai/foundry/README.md](../ai/foundry/README.md) |
| Microsoft Purview | template+binding | [infra/azure/modules/platform.bicep](../infra/azure/modules/platform.bicep), [governance/purview.md](../governance/purview.md) |
| Mirror | configuration-contract | [fabric/connections/mirroring.md](../fabric/connections/mirroring.md), [fabric/connections/catalog.json](../fabric/connections/catalog.json) |
| Mirrored database | configuration-contract | [fabric/connections/mirroring.md](../fabric/connections/mirroring.md), [fabric/connections/catalog.json](../fabric/connections/catalog.json) |
| Mirroring | configuration-contract | [fabric/connections/mirroring.md](../fabric/connections/mirroring.md), [fabric/connections/catalog.json](../fabric/connections/catalog.json) |
| Notebook | code+template | [fabric/notebooks/01_bronze_orders.py](../fabric/notebooks/01_bronze_orders.py), [fabric/notebooks/02_silver_orders.py](../fabric/notebooks/02_silver_orders.py), [fabric/notebooks/03_gold_sales.py](../fabric/notebooks/03_gold_sales.py) |
| On-premises datacenter | template+binding | [sources/onprem/compose.yaml](../sources/onprem/compose.yaml), [sources/azure-sql/schema.sql](../sources/azure-sql/schema.sql), [fabric/connections/catalog.json](../fabric/connections/catalog.json) |
| OneLake | template+service-managed | [fabric/manifests/provider.json](../fabric/manifests/provider.json), [scripts/upload_onelake.py](../scripts/upload_onelake.py), [docs/architecture.md](../docs/architecture.md) |
| Platform | cross-cutting-design | [docs/architecture.md](../docs/architecture.md), [governance/access-matrix.csv](../governance/access-matrix.csv), [docs/deployment.md](../docs/deployment.md) |
| Power BI | authoring-contract | [fabric/reports/report-spec.json](../fabric/reports/report-spec.json), [fabric/reports/theme.json](../fabric/reports/theme.json), [fabric/manifests/serving.json](../fabric/manifests/serving.json) |
| Process | code+template | [fabric/notebooks/01_bronze_orders.py](../fabric/notebooks/01_bronze_orders.py), [fabric/notebooks/02_silver_orders.py](../fabric/notebooks/02_silver_orders.py), [fabric/notebooks/03_gold_sales.py](../fabric/notebooks/03_gold_sales.py) |
| Provider tenant | template+configuration | [fabric/manifests/provider.json](../fabric/manifests/provider.json), [docs/deployment.md](../docs/deployment.md) |
| Real-Time Intelligence | code+template | [fabric/manifests/provider.json](../fabric/manifests/provider.json), [fabric/kql/001_schema.kql](../fabric/kql/001_schema.kql), [fabric/kql/002_dashboard_queries.kql](../fabric/kql/002_dashboard_queries.kql) |
| Real-Time Intelligence dashboard | authoring-contract | [fabric/reports/realtime-dashboard-spec.json](../fabric/reports/realtime-dashboard-spec.json), [fabric/kql/002_dashboard_queries.kql](../fabric/kql/002_dashboard_queries.kql) |
| SQL analytics endpoint | service-managed+code | [fabric/sql/lakehouse/quality_checks.sql](../fabric/sql/lakehouse/quality_checks.sql), [docs/architecture.md](../docs/architecture.md) |
| SQL database in Fabric | code+template | [fabric/manifests/provider.json](../fabric/manifests/provider.json), [fabric/sql/operations/001_tables.sql](../fabric/sql/operations/001_tables.sql) |
| Semantic model (Direct Lake) | template | [fabric/semantic-model/model.bim](../fabric/semantic-model/model.bim), [fabric/manifests/serving.json](../fabric/manifests/serving.json) |
| Serve | cross-cutting-design | [docs/architecture.md](../docs/architecture.md), [governance/access-matrix.csv](../governance/access-matrix.csv), [docs/deployment.md](../docs/deployment.md) |
| Shortcuts | configuration-contract | [fabric/connections/shortcuts.md](../fabric/connections/shortcuts.md), [fabric/consumer/README.md](../fabric/consumer/README.md) |
| Snowflake | code+binding | [sources/snowflake/setup.sql](../sources/snowflake/setup.sql), [fabric/connections/mirroring.md](../fabric/connections/mirroring.md) |
| Store | template+service-managed | [fabric/manifests/provider.json](../fabric/manifests/provider.json), [scripts/upload_onelake.py](../scripts/upload_onelake.py), [docs/architecture.md](../docs/architecture.md) |
| Stored procedure | code+template | [fabric/manifests/provider.json](../fabric/manifests/provider.json), [fabric/sql/warehouse/001_tables.sql](../fabric/sql/warehouse/001_tables.sql), [fabric/sql/warehouse/002_publish.sql](../fabric/sql/warehouse/002_publish.sql) |
| Streaming data | template+binding | [fabric/manifests/streaming.json](../fabric/manifests/streaming.json), [fabric/eventstreams/eventstream.json](../fabric/eventstreams/eventstream.json), [fabric/eventstreams/topology.json](../fabric/eventstreams/topology.json) |
| Structured andsemistructured data | fixtures+configuration | [fabric/connections/catalog.json](../fabric/connections/catalog.json), [data/sample/orders.jsonl](../data/sample/orders.jsonl), [data/sample/telemetry.jsonl](../data/sample/telemetry.jsonl) |
| Workspace monitoring | configuration-contract | [monitoring/README.md](../monitoring/README.md), [monitoring/alerts.json](../monitoring/alerts.json) |
