# Dataflow Gen2 branch

Create `daily_sales_publish` in the provider workspace. Add text parameters
`SqlEndpoint` and `SqlDatabaseId`; use the Lakehouse SQL endpoint values after
metadata synchronization. Paste `daily_sales.pq` in the advanced editor and bind
an authorized organizational connection. Set the data destination to Warehouse
`analytics.daily_sales_stage`, **replace** mode, fixed mapping.

After refresh succeeds, run `analytics.publish_daily_sales` through a Warehouse
Script activity. Add these two activities after `03_gold_sales` in a separate
production publishing pipeline. The supplied orders pipeline ends at Gold and
does not claim to configure this connection-bound branch. Test failure behavior:
the published table must stay intact when refresh or validation fails.

Export the tenant-authored definition after validation where the item's supported
Git/API integration permits it; do not fabricate connection IDs in source control.
