# Shortcut inventory

Create internal shortcuts for mirrored tables and curated shared datasets. Use
external shortcuts for supported ADLS, S3 and Google Cloud Storage paths. Place
Delta tables in the Lakehouse Tables area and ordinary files under Files. For a
Blob source that does not match supported shortcut semantics, use a Copy activity.

For each shortcut capture: source cloud, endpoint/bucket/container, object prefix,
Fabric connection ID, target workspace/item/path, expected schema, data owner and
access test. Use a separate read-only connection for each trust boundary. Data at
the source must have a compatible layout; a shortcut does not convert CSV to Delta.

Check that SQL/Direct Lake can discover intended Delta tables; file visibility alone
is insufficient. Revoke the source grant and verify access stops. Shortcuts are not
independent backups and do not automatically transfer source governance policies.
