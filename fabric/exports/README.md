# Environment exports

Put native definitions exported from your validated Fabric tenant here temporarily.
Exports are ignored by Git because they can contain IDs, URLs and connection
metadata. Review and sanitize them, replace environment-specific bindings, then
promote approved definitions into `fabric/definitions` and extend the manifest.
Do not commit tokens, connection secrets, data extracts, or customer information.
