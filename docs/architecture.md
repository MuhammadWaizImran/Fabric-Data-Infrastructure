# Architecture decisions

## Scope and fidelity

The supplied SVG is a reference architecture, not a complete business specification.
Every named technology and both tenant boundaries are retained. Some boxes repeat
because the same technology appears at several lifecycle stages; they are not
necessarily separate resources. `coverage.json` maps unique labels and the original
diagram preserves their position and arrows. Representation coverage is not proof
of tested end-to-end connectivity.

The illustrative data domain is sales orders plus device telemetry. This provides
concrete fixtures, transformations and measures without inventing a real customer's
requirements. Monetary aggregation is USD-only. Source-qualified keys are required
when combining independent real source systems. The file-based demo is a full
snapshot pipeline; a production CDC integration needs explicit deletion semantics,
watermarks, replay and schema-evolution handling.

## Source and ingestion paths

- Azure SQL/PostgreSQL/Cosmos/Snowflake: supported database mirroring into OneLake.
- Databricks: Unity Catalog metadata mirroring and access to underlying data.
- On-premises: a gateway-backed ingestion path; use source-supported mirroring only
  after validating the actual engine/version. The local SQL Server container is a
  source simulator, not an on-premises gateway.
- ADLS/Blob/S3/GCS: source-appropriate copy or shortcut connections.
- Dataverse: Link to Fabric and managed shortcuts.
- Event Hubs/IoT/Kinesis/PubSub: independent Eventstream connections into Eventhouse
  and Lakehouse destinations.
- Azure Data Explorer: external KQL source accessed by a supported database shortcut.

None of these integrations makes unrelated source schemas interchangeable. Normalize
names, types, timezones, keys and deletions before combining data.

## Storage and processing

OneLake is Fabric-managed, not another storage account to provision through Bicep.
Azure ADLS in `infra/azure` is an external source/integration store. A Lakehouse
holds Bronze, Silver and Gold Delta tables in the sample. Mirrored data stays
read-only; enrichment writes into separate tables. A Warehouse serves structured
SQL transformations; SQL database in Fabric stores operational state such as the
device registry. Its managed analytical replica is separate from the transactional
endpoint. Eventhouse owns time-series queries and telemetry retention.

The provided notebook pipeline processes orders. Dataflow Gen2 maps Gold into a
Warehouse staging table; the stored procedure validates and publishes it in one
transaction. That connection-bound extension is configured after the base pipeline.
Notebook writes use OneLake paths, avoiding a dependency on an attached default
lakehouse. Lakehouse SQL endpoints query Delta data; they cannot modify those rows.

## Serving and AI

Direct Lake model → Power BI report for sales; KQL queries → real-time dashboard
for telemetry. GraphQL exposes selected supported tabular sources, with valid keys
and explicit permissions. It does not assume direct Eventhouse support.

Fabric ML and Azure ML are alternative execution paths for the sample enrichment.
Foundry orchestrates approved AI functionality and a governed Fabric data agent.
Copilot is a tenant/capacity feature configured for the appropriate users. These
features require data, access, evaluation and service settings beyond resource shells.
The diagram's preview label is retained in coverage but current docs describe the
data agent as generally available; deployment should recheck actual tenant availability.

## Provider and consumer tenants

External sharing exposes selected OneLake data read-only. The consumer accepts it
into a Lakehouse shortcut, then uses consumer-owned processing/serving items as
needed. Consumer SQL/Warehouse/Eventhouse/Eventstream boxes do not imply that a
share can be directly accepted by every store or that a share is a stream transport.
The consumer must manage its own permissions and governance. Provider-side policies
do not all transfer. Both environments need independent identity/capacity configuration.

## Platform services

Entra controls identity; Fabric permissions control workspaces/items and data access.
Key Vault holds secrets where a connector supports that integration; other connectors
use approved managed connection storage. Purview handles cataloging/classification
and supported lineage. Azure Policy audits Azure resource tags and cannot replace
Fabric governance. GitHub and Azure DevOps are supplied as alternative CI systems.
Workspace monitoring, Azure diagnostics and Capacity Metrics cover different scopes.
Cost Management budgets alert; they do not cap spending or stop services.
