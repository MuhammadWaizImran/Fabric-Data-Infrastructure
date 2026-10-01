# Eventhouse to OneLake

In the provider Eventhouse, enable OneLake availability on the chosen KQL table(s).
Record the generated OneLake location. Create an internal shortcut in the analytics
lakehouse and confirm a notebook can read the Delta representation. This is an
additional serving path; it does not turn KQL tables into a Fabric Warehouse.

Validate latency separately from direct KQL queries. Use the KQL path for the
freshness-sensitive dashboard. The Azure Data Explorer source can be represented
by a supported KQL database shortcut; configure its source cluster URI/database
and authorized identity before enabling the shortcut. A shortcut is not a backup.
