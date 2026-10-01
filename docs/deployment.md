# Future deployment runbook

This is documentation for later use. Repository creation/validation does not deploy.
Proceed branch by branch and record evidence in `docs/acceptance.md`.

## 1. Choose environments and confirm prerequisites

- Azure subscription and an Entra tenant with Fabric enabled; proper Azure resource
  management/RBAC permissions and Fabric admin or delegated capacity permissions.
- Supported region/quota for Fabric, PostgreSQL, Cosmos, IoT, ADX, Databricks, ML,
  Purview and Foundry. A single example region is not a compatibility guarantee.
- Separate consumer tenant/capacity/workspace for the external-sharing branch.
- AWS, GCP, Snowflake, Dataverse and on-premises connectivity for their exact branches.
- Python 3.10+, Azure CLI/Bicep; optional SDK extras via `pip install -e ".[azure,ml]"`.
- Appropriate Power BI author/viewer licensing; AI capacity/settings if using AI.

Choose dev/test/prod workspaces or capacities based on isolation requirements. Git
branches alone are not data or identity isolation. Use workload identity federation
for future CI deployment; no deployment credentials are required by included CI.

## 2. Prepare Azure parameters

Create a resource group explicitly in the chosen subscription. Copy
`infra/azure/main.parameters.example.json` to `config/azure.local.json`. Replace
all `REPLACE_` markers. The password references must point to an **existing bootstrap
Key Vault**, with valid secrets and ARM template deployment access; they cannot
refer to the new vault being created in the same deployment. Follow the Key Vault
template-deployment prerequisites in Microsoft's documentation or supply secure
parameters using an approved equivalent. Never commit plaintext passwords.

Set administrator UPNs and the operator object ID. The included role assignment
grants storage reader only; ingest writers/stream producers/consumers need their
separate least-privilege roles. Pick budget period dates in UTC according to the
budget API's valid monthly period; 250 is an alert threshold example, not a forecast.

Local compilation:

```powershell
az bicep build --file infra/azure/main.bicep --outfile build/main.json
az bicep build --file infra/azure/network.bicep --outfile build/network.json
az bicep build --file infra/azure/policy.bicep --outfile build/policy.json
```

Authenticated plan (no resource deployment):

```powershell
./scripts/azure_plan.ps1 -ResourceGroup YOUR_RG -SubscriptionId YOUR_SUBSCRIPTION -ParameterFile config/azure.local.json
```

Only a later intentional invocation with `-Apply` creates Azure resources. The plan
wrapper requires a specific subscription instead of trusting a previous CLI default.

## 3. Finish networking and platform configuration

Deploy `network.bicep` separately with actual storage/vault/Event Hubs names.
It creates an Azure VNet and DFS/Blob/Key Vault/Event Hubs endpoints and DNS links.
Add appropriate endpoints/DNS/routes for SQL, PostgreSQL, Cosmos, IoT, Purview, ADX,
ML and Foundry. Configure Databricks connectivity/Unity Catalog separately. Use
the generalized private endpoint module where appropriate after confirming the
service's group ID and supported private-access mode.

An Azure private endpoint does not configure Fabric outbound connectivity. Depending
on connector support, configure managed private endpoints, approved gateway/private
connectivity, or a reviewed service-supported network path. Do not just enable a
broad public firewall to make a failed connector work. ML additionally needs storage
and Key Vault identity access; Foundry models need network and quota configuration.

`policy.bicep` deploys at subscription scope and assigns its audit policy to the chosen
resource group. Fabric tenant permissions, source access grants, Purview scans and
Copilot settings remain separate tasks. No role in this repo is a blanket tenant admin.

## 4. Create Fabric workspaces and bind capacity

Create provider/consumer workspaces in the appropriate tenant, assign their Fabric
capacity, and give the execution identity Contributor or the required item-specific
permissions. Allow service-principal APIs only when needed and supported by each
item type. A Fabric capacity's Azure ARM resource ID is not its Fabric REST GUID.

Generate notebook definitions and inspect the offline plan:

```powershell
python scripts/build_definitions.py
python scripts/fabric_items.py
```

For an intentional future apply, obtain a current Fabric-audience token without
printing it. One interactive method is:

```powershell
$env:FABRIC_TOKEN = az account get-access-token --resource https://api.fabric.microsoft.com --query accessToken -o tsv
Copy-Item config/bindings.example.json config/provider.local.json
python scripts/fabric_items.py --workspace YOUR_PROVIDER_WORKSPACE_GUID --bindings config/provider.local.json --apply
```

The base manifest needs no source connection binding; its generated IDs are wired
in dependency order and written to ignored `build/fabric-bindings-<workspace>.json`.
Missing bindings used by an artifact fail preflight before writes. Existing items
are reused; `--update-definitions` explicitly updates their supplied definitions.
There is no delete/recreate fallback. After ambiguous network failure, inspect the
workspace before retrying. Long-running provisioning operations can take minutes.

## 5. Validate the sample batch path

Assign an authorized uploader to the provider Lakehouse. Set
`ONELAKE_WORKSPACE_ID` and `ONELAKE_LAKEHOUSE_ID` from actual IDs. Run the uploader
without flags to view the plan; `--apply` uploads the fixture to OneLake.

Run the `orders_end_to_end` pipeline in Fabric. It executes Bronze → Silver → Gold.
Confirm the expected sample totals and quarantine count. Wait for SQL endpoint
metadata synchronization, then run `fabric/sql/lakehouse/quality_checks.sql`.
The notebook sources are full-snapshot examples, not an arbitrary CDC engine.

## 6. Add all source branches

Use `fabric/connections/catalog.json`, the source schemas and mirroring/shortcut
runbooks. Configure one source at a time; verify updates, deletes and interruption
recovery before downstream usage. For AWS/GCP, review and deploy the supplied
templates in those accounts only if those branches are required. The GCP project
must exist, required APIs must be enabled and provider credentials must be external.
Snowflake and Dataverse require separate service setup; Azure cannot provision their
accounts through the Azure Bicep deployment.

## 7. Build SQL and low-code publishing branches

Execute Warehouse SQL scripts in numeric order. Configure Dataflow Gen2 from its
M source and destination instructions. Extend orchestration to refresh the dataflow
and then execute `analytics.publish_daily_sales`. Run the operational SQL script
against the Fabric SQL database's transactional endpoint and verify its analytical
replica separately.

## 8. Enable streaming and dashboards

Create the Event Hubs cloud connection with the supported authentication/network
path. Merge its ID into generated provider bindings. Apply `streaming.json` using
`--manifest fabric/manifests/streaming.json` after reviewing its definition. Run the
KQL schema commands individually and add the Eventhouse destination in the editor.
Add IoT/Kinesis/PubSub source branches, normalize events and publish. Configure the
ADX shortcut and Eventhouse OneLake availability where needed. Follow the streaming
README for reconciliation and dashboard refresh expectations.

The producer's `--send` uses Entra authentication and current timestamps. Grant its
identity Event Hubs Data Sender on the hub; the consumer needs receiver permissions.
The script does not create or enroll IoT devices and does not publish to AWS/GCP.

## 9. Bind serving and AI

Fill `SQL_ENDPOINT` and `SQL_DATABASE` using the Lakehouse SQL endpoint host and
database GUID. Apply `fabric/manifests/serving.json`. Confirm Direct Lake partitions
and the model connection/SSO behavior before report authoring. Implement report
visuals using report-spec.json and theme.json; export the native report afterwards.
Create GraphQL using its runbook and confirm actual generated field names.

Configure the Fabric data agent, scoped Copilot settings and optional Foundry
connection. Run evaluation cases. For ML, use the local job or Fabric notebook
instructions and verify model/data lineage. Do not equate synthetic validation with
production model quality.

## 10. Complete consumer, governance and operational acceptance

Follow `fabric/consumer/README.md` using a consumer-tenant identity. Test shared-data
read and revocation. Implement consumer-owned processing without writing into shared
read-only locations. Configure Purview, workspace monitoring and actual alert
destinations; choose GitHub or Azure DevOps for CI. Complete the acceptance checklist
before claiming full implementation. No setup step in this document has been run
against cloud accounts during repository creation.
