-- Run against analytics_warehouse, NOT a Lakehouse SQL analytics endpoint.
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'analytics')
    EXEC('CREATE SCHEMA analytics');
GO
IF OBJECT_ID('analytics.daily_sales', 'U') IS NULL
CREATE TABLE analytics.daily_sales (
    sales_date date NOT NULL,
    currency varchar(3) NOT NULL,
    orders bigint NOT NULL,
    quantity bigint NOT NULL,
    revenue decimal(18,2) NOT NULL
);
GO
IF OBJECT_ID('analytics.daily_sales_stage', 'U') IS NULL
CREATE TABLE analytics.daily_sales_stage (
    sales_date date NOT NULL,
    currency varchar(3) NOT NULL,
    orders bigint NOT NULL,
    quantity bigint NOT NULL,
    revenue decimal(18,2) NOT NULL
);
GO
