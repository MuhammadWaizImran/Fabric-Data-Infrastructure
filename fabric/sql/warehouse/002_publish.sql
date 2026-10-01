-- Dataflow Gen2 must REPLACE the staging snapshot before calling this procedure.
-- Serialize writers; schedule this branch after gold tables are committed.
CREATE OR ALTER PROCEDURE analytics.publish_daily_sales
AS
BEGIN
    SET NOCOUNT ON;
    IF NOT EXISTS (SELECT 1 FROM analytics.daily_sales_stage)
        THROW 50001, 'Refusing to replace reporting data with an empty staging snapshot.', 1;
    IF EXISTS (SELECT 1 FROM analytics.daily_sales_stage WHERE revenue < 0 OR orders < 0 OR currency <> 'USD')
        THROW 50002, 'Daily sales quality validation failed.', 1;
    IF EXISTS (SELECT sales_date, currency FROM analytics.daily_sales_stage GROUP BY sales_date, currency HAVING COUNT(*) > 1)
        THROW 50003, 'Duplicate daily sales keys.', 1;
    BEGIN TRY
        BEGIN TRANSACTION;
        DELETE FROM analytics.daily_sales;
        INSERT INTO analytics.daily_sales (sales_date, currency, orders, quantity, revenue)
        SELECT sales_date, currency, orders, quantity, revenue FROM analytics.daily_sales_stage;
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO
