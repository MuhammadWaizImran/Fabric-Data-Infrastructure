# Monitoring setup

Enable Fabric workspace monitoring for provider and consumer independently and
record the monitoring Eventhouse/item created by the service. Use its current
schema to build failure, duration and capacity views; do not assume all item types
emit identical records. Use Monitoring Hub for individual pipeline/notebook runs
and Capacity Metrics for CU pressure. ADX, Event Hubs and other Azure resources
have Azure diagnostics distinct from Fabric workspace monitoring.

`alerts.json` defines desired alerts and ownership; instantiate notifications in
your approved monitoring system after real destinations and service identities
exist. The Bicep budget only sends notifications when contact emails are configured.
It is not a spending cap. Check the cost of provider/consumer capacities, storage,
Azure source services, ML compute, model usage, Purview and external-cloud traffic.
