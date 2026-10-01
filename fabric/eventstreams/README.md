# Streaming branches

The REST definition implements Event Hubs → Eventstream → Lakehouse Delta table.
It requires an already-created, authorized Fabric source connection. After import,
add the Eventhouse destination using the provider telemetry database and existing
`Telemetry` table/mapping from `../kql/001_schema.kql`. Publish in the eventstream
editor, then verify ingestion independently at both destinations.

For diagram parity, add IoT Hub, Kinesis and Pub/Sub sources following
`../connections/catalog.json`. Configure mappings to the same event contract.
Do not connect the same source twice without deliberate event_id deduplication.
`topology.json` is the complete binding contract, not an API payload. Export the
validated native Eventstream definition for your environment after those bindings
exist. No placeholder destination is represented as already configured.

Use an Event Hubs consumer group dedicated to this stream. Kinesis/PubSub need
external cloud permissions and may create cross-cloud traffic charges. Check
private network support for each source before blocking all public endpoints.
The consumer tenant's Eventstream needs its own source connection; external data
sharing provides read-only data access, not automatic stream replication.
