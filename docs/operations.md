# Operations and recovery

| Failure | Diagnosis | Recovery |
|---|---|---|
| Mirroring lag | Source permissions, replication/CDC state, network and Fabric capacity | Restore source access; verify checkpoint/snapshot state before restart |
| Batch notebook fails | Monitoring Hub, input schema, quarantine and Spark error | Fix source/logic; rerun full fixture snapshot; do not blindly overwrite production partial feeds |
| Invalid rows | Inspect restricted quarantine and compare source contract | Correct source, record remediation, replay approved data |
| Duplicate telemetry | Replay or multiple ingestion routes | Query deduplicated event_id view; verify producer IDs and consumer groups |
| Empty dashboard | Event timestamps, query window, table mapping and model binding | Use current events or adjust the investigation time range |
| Warehouse publish fails | Staging refresh status and procedure quality errors | Keep last published snapshot; repair staging and rerun serialized publication |
| Capacity throttling | Capacity Metrics and overlapping jobs | Stagger work or resize after workload measurement |
| Share stops working | Revocation, tenant settings, consumer permissions | Confirm intentional revocation; restore only authorized access |
| API 401/403 | Token audience/expiry, identity support and item permissions | Obtain correct token/grants; never log the token |

## Reliability requirements to select for production

Define actual freshness SLO, RPO/RTO, retention and workload concurrency. Configure
replay retention, immutable raw retention where needed, source backups and restore
tests. A Delta table, mirror or shortcut is not automatically a disaster-recovery
copy. Preserve infrastructure/source definitions and sanitized native Fabric exports.
Use separate data/identity boundaries for dev/test/prod. Introduce schema versions
and downstream compatibility checks before changing business fields.

Local JSON transformations use Decimal arithmetic; Spark/M/SQL use declared decimal
or currency types. Validate rounding and precision against the chosen real contract.
The fixture has two decimal places and USD only; other currencies need explicit
FX/date logic. Snapshot overwrite is intentional for the demo. Production incremental
loads require source-qualified upsert keys, deletion handling and bounded concurrency.

## Costs and cleanup

Inventory running capacities and source services separately. Pausing Fabric does not
stop Azure SQL, PostgreSQL, ADX, IoT, storage, Foundry model usage or external-cloud
charges. Budget alerts do not enforce a cap. There is no automatic destroy script.
Before later cleanup, identify exact resources, preserve required data and obtain
the owner's authorization for data loss. AWS bucket templates retain source data;
Key Vault purge protection intentionally prevents immediate permanent removal.
