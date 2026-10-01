// Paste into a Dataflow Gen2 query. Define SqlEndpoint and SqlDatabaseId text parameters.
let
    Source = Sql.Database(SqlEndpoint, SqlDatabaseId),
    Gold = Source{[Schema="dbo", Item="gold_daily_sales"]}[Data],
    Selected = Table.SelectColumns(Gold, {"date", "currency", "orders", "quantity", "revenue"}),
    Renamed = Table.RenameColumns(Selected, {{"date", "sales_date"}}),
    Typed = Table.TransformColumnTypes(Renamed, {{"sales_date", type date}, {"currency", type text}, {"orders", Int64.Type}, {"quantity", Int64.Type}, {"revenue", Currency.Type}}),
    Validated = Table.SelectRows(Typed, each [revenue] >= 0 and [currency] = "USD")
in
    Validated
