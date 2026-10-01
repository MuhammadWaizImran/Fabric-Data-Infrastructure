# Mirror setup and verification

For each mirroring entry in catalog.json, first validate the source-specific
Microsoft prerequisites linked in docs/references.md. Provision the source schema,
source authentication, replication requirements, private connectivity, and Fabric
connection. Create a **Mirrored database** item using the correct connector. Select
only the listed demonstration tables and start replication. Record its item ID and
SQL endpoint in local environment inventory. This procedure is per connector;
there is deliberately no invented generic `start mirroring` request here.

Verify initial counts, then insert, update and delete one test row. Record observed
latency and type mapping. Test reconnect after a source interruption. Add a Lakehouse
shortcut to the mirrored tables for Spark enrichment. Query replicas read-only;
write transformations to separate Silver/Gold destinations. Treat Databricks as
metadata mirroring and verify direct source storage permissions separately.

Do not load duplicate demo orders from every source into one fact table unchanged:
namespace keys by source or select one system of record. Mirroring source tables
does not automatically run the sample order notebook pipeline, which reads staged
JSONL files. Add a normalization notebook or Copy activity for the chosen mirror.

SQL database in Fabric has its own managed analytical replica. Verify that replica
instead of creating an unnecessary second mirror of the same operational item.
