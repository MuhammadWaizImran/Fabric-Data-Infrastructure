-- Run in SQL database in Fabric (transactional endpoint).
IF OBJECT_ID('dbo.DeviceRegistry', 'U') IS NULL
CREATE TABLE dbo.DeviceRegistry (
    device_id varchar(64) NOT NULL PRIMARY KEY,
    site_id varchar(64) NOT NULL,
    installed_at datetime2 NOT NULL DEFAULT SYSUTCDATETIME(),
    enabled bit NOT NULL DEFAULT 1
);
IF NOT EXISTS (SELECT 1 FROM dbo.DeviceRegistry WHERE device_id = 'D01')
    INSERT INTO dbo.DeviceRegistry(device_id, site_id) VALUES ('D01', 'SITE01');
-- Fabric-managed mirroring exposes analytics replicas. Do not create a second independent mirror of this item.
