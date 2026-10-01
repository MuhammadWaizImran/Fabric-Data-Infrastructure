-- Read-only queries through the automatically provisioned Lakehouse SQL endpoint.
SELECT order_id, COUNT(*) AS duplicates
FROM dbo.silver_orders
GROUP BY order_id HAVING COUNT(*) > 1;

SELECT COUNT(*) AS rejected_rows FROM dbo.quarantine_orders;

SELECT SUM(revenue) AS revenue_usd, SUM(orders) AS order_count
FROM dbo.gold_daily_sales;
-- Fixture expectation: 359.85 USD and 3 orders. No INSERT/UPDATE/DELETE here.
