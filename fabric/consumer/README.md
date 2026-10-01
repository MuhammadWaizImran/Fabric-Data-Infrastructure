# Consumer tenant: preserve the second tenant in the original diagram

1. Enable Fabric and provision/assign a consumer capacity in the **consumer Entra
   tenant**. Its capacity and workspace are separate from the provider. Reuse the
   Azure capacity module if creating it through Azure; use the correct subscription.
2. Inspect `fabric/manifests/consumer.json`: it includes `shared_analytics`, consumer
   Warehouse, SQL database, Eventhouse/KQL database and the shared-data notebook.
   Apply with a consumer token/workspace. Never reuse the provider token across tenants.
3. Enable external data sharing on both sides. The provider selects specific
   supported OneLake files/tables and creates an external share for the consumer.
4. Accept the share into `shared_analytics` Lakehouse. Verify the read-only shortcut.
   This is the supported acceptance target; the diagram's other consumer stores do
   not imply direct share acceptance into every type of item.
5. Bind the provisioned consumer stores/notebook and author consumer Dataflow Gen2
   and Power BI items for the consumer's own processing/serving requirements. Name
   the accepted Gold shortcut `shared_daily_sales` for the provided read notebook.
   The same artifact templates can be rebound, but consumer-owned write targets must
   never point into the read-only provider share.
6. For consumer SQL database analytics, use its managed mirror; provision additional
   mirrored databases only for actual consumer-owned sources. Configure consumer
   Eventstream with its own connection. The share is not an event subscription.
7. Apply consumer workspace/item/OneLake/semantic-model permissions. Test provider
   revocation and consumer access separately. Provider labels and all governance
   rules do not automatically carry across tenant boundaries.

Acceptance evidence: both tenant IDs; share ID; selected source table; consumer
shortcut; authorized read; unauthorized failure; provider-change visibility;
revocation failure. No external invitation has been sent by this repository.
