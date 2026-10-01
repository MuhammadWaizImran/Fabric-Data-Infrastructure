# Cloud acceptance checklist — all pending until actually deployed

- [ ] Provider and consumer capacity/workspace/tenant IDs recorded independently.
- [ ] Every required regional SKU, quota and license confirmed.
- [ ] Network/DNS and identity tests pass for every required source connection.
- [ ] Azure SQL/PostgreSQL/Cosmos/Snowflake mirrors propagate insert/update/delete.
- [ ] Databricks metadata mirror resolves authorized Delta tables.
- [ ] On-premises gateway ingestion and reconnect tested.
- [ ] ADLS/Blob/S3/GCS source paths reconcile and access revocation is enforced.
- [ ] Dataverse Link tables and changes are visible.
- [ ] Orders pipeline produces 3 orders, 359.85 USD and one invalid fixture row.
- [ ] Dataflow staging and Warehouse publication match Gold with no duplicate keys.
- [ ] Fabric operational SQL database and its analytics replica are verified.
- [ ] Event Hubs/IoT/Kinesis/PubSub produce normalized events in both destinations.
- [ ] Replay does not double-count dashboard business metrics.
- [ ] ADX shortcut and Eventhouse OneLake availability tested.
- [ ] Direct Lake model, BI permissions, report measures and RT dashboard validated.
- [ ] GraphQL authorized read succeeds; unauthorized read fails.
- [ ] ML model/version/feature contract recorded; synthetic data not called production evidence.
- [ ] Foundry/data-agent evaluation and scoped Copilot settings verified.
- [ ] External share accepted into consumer Lakehouse; provider revocation tested.
- [ ] Consumer-owned processing/serving and governance tested independently.
- [ ] Purview scans/lineage coverage and actual monitoring alerts reviewed.
- [ ] Failure/retry/recovery/load tests meet agreed SLOs and cost envelope.

Record date, operator, workspace/resource ID and evidence link for each completed
item. Offline unit tests do not mark any of these cloud acceptance items complete.
