# Dataverse source branch

Prerequisites: licensed Dataverse environment, appropriate Power Platform admin
and table permissions, compatible Fabric tenant/capacity and regional setup.
Use Link to Microsoft Fabric for selected tables such as Account and Contact.
Select/create the provider workspace and validate the resulting lakehouse/table
shortcuts. Dataverse manages this linkage; do not treat it as an ordinary Azure
SQL mirror or create a duplicate ingestion pipeline by default.

Record the environment URL, table logical names and target item IDs in a local
connection inventory. For the sample domain, map Account to customer_id using an
explicit mapping table; never join unrelated source IDs merely because they have
the same field name. Test new/updated/deleted rows before enabling downstream use.
