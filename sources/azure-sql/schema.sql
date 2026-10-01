-- Azure SQL source and SQL Server on-premises sample schema.
IF OBJECT_ID('dbo.Orders', 'U') IS NULL
CREATE TABLE dbo.Orders (
    order_id varchar(64) NOT NULL PRIMARY KEY,
    customer_id varchar(64) NOT NULL,
    product_id varchar(64) NOT NULL,
    order_date datetime2 NOT NULL,
    updated_at datetime2 NOT NULL,
    quantity int NOT NULL,
    unit_price decimal(18,2) NOT NULL,
    currency char(3) NOT NULL
);
IF NOT EXISTS (SELECT 1 FROM dbo.Orders WHERE order_id = 'O100')
    INSERT INTO dbo.Orders VALUES ('O100', 'C01', 'P01', '2026-09-01T10:00:00', '2026-09-01T11:00:00', 3, 19.95, 'USD');
