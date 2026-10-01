# GraphQL serving branch

Create `analytics_api` in the provider workspace using Fabric API for GraphQL.
Select the Lakehouse SQL endpoint and expose `gold_daily_sales`. Assign a unique
key supported by the API metadata; for this USD-only sample, `date` is unique.
For multiple currencies use a stable composite/business key. Do not expose
Bronze or quarantine data. Add Warehouse or SQL database objects only when needed.

Use the generated schema to confirm the entity/field names in `queries.graphql`.
Grant access to a test caller, execute a read, and verify an unauthorized caller
cannot read the data. Export the definition into the excluded `fabric/exports`
folder for review and source-control sanitization. No credential or fake API URL
is embedded here. Eventhouse has its own KQL interface; this branch does not
assume a native Eventhouse-to-GraphQL connector.
