# Implementation status and honest boundaries

## Included and executable locally

- Deterministic order validation, quarantine, deduplication, exact decimal totals.
- Synthetic telemetry generator and event contract checks.
- Offline Fabric item planning and definition generation/parameter substitution.
- REST helper with pagination, 429 handling, asynchronous operations, origin checks,
  preflight validation, reuse of existing items and explicit definition updates.
- Unit tests with mock cloud responses. No live cloud calls in unit tests.
- Optional sklearn ML demonstration; no production accuracy claim.

## Templates and code that require a configured cloud environment

- Azure Bicep modules and separate network/policy deployment entry points.
- AWS CloudFormation and GCP Terraform source infrastructure.
- Fabric Lakehouse/Warehouse/SQL database/Eventhouse/KQL database creation manifests.
- Importable notebook definitions and sequential orders DataPipeline definition.
- Event Hubs → Eventstream → Lakehouse definition; requires a source connection.
- Direct Lake TMSL semantic model; requires populated Gold and SQL endpoint bindings.
- SQL/KQL/M scripts, source schemas and sample records.
- Azure ML job/compute configuration.

These artifacts have not been integration-tested against Azure/Fabric/AWS/GCP.
Compiler/schema/syntax validation does not verify quota, regional availability,
permissions, connector authentication or service provisioning success.

## Tenant-bound/manual authoring included as explicit contracts

| Branch | Remaining environment work |
|---|---|
| Mirroring | Source credentials/prerequisites, table selection, source connection and replication startup |
| External shortcuts | Authorized source connections, paths, data format and shortcut creation |
| Dataflow Gen2 | M import, destination binding and publishing pipeline extension |
| Full streaming topology | IoT/Kinesis/PubSub connections, Eventhouse binding and publish validation |
| Power BI report | Author visuals from report-spec.json, bind model, save native PBIR/PBIP |
| RT dashboard | Author dashboard tiles with provided KQL and export native definition |
| GraphQL | Create API item, select keyed objects, grant access, confirm generated schema |
| Cross-tenant sharing | Admin settings, real recipient, share acceptance and access tests |
| Consumer processing | Bind each needed consumer-owned store/pipeline to accepted data |
| Foundry/data agent/Copilot | Model/agent deployment, connections, permissions, instructions, evaluation and tenant settings |
| Governance/monitoring | Scan registration, labels, access assignments, real alert destinations and monitoring activation |
| Networking | Remaining source/service private endpoints, gateways, DNS, Fabric outbound paths and supported source authentication |

No native report/dashboard export, real source connection, or cross-tenant share is
fabricated. The native-definition export workflow is documented in `fabric/exports`.
This is a full **repository representation** of the diagram with a working sample
core, not a fully automated implementation of every connection.

## Development defaults

Single-region resources, LRS storage, one Event Hub unit, small source databases,
development ADX SKU, and F2 capacity are demonstration defaults. They do not satisfy
an unspecified production SLO. Source services mostly start with public access
disabled and need the networking steps before data can flow. Databricks has no
compute cluster/catalog granted by the resource module. Azure ML has no compute
created by Bicep. Foundry has no paid model deployment. No full DR topology is created.
