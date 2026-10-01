# Purview and data governance

Register the Fabric tenant and supported source systems using the appropriate
Purview Data Map/Unified Catalog experience and scan identity. The Bicep account
does not by itself configure scans, domains, data products or labels. Verify the
tenant's current Purview onboarding/licensing requirements.

Business glossary:

| Term | Definition | Owner |
|---|---|---|
| Revenue USD | quantity times unit price after order deduplication, USD only | Sales owner |
| Order | Latest valid record per source-qualified order ID | Operations owner |
| Telemetry event | Versioned observation uniquely identified by event_id | IoT owner |
| Data freshness | Observation time to consumer-visible time | Platform owner |

Apply classification to customer and device identifiers. Capture lineage from
sources through transformations to semantic models; where connector coverage is
incomplete, document the gap. Label Gold assets and restrict raw/quarantine access.
Azure Policy governs Azure resources; it does not replace Fabric item permissions
or consumer-tenant governance. Validate SQL, Spark, direct file and BI access paths
independently rather than assuming one layer's row rules protect every path.
