# Data Schema Outline

## Core tenant and control tables

- `organizations`
- `organization_memberships`
- `roles`
- `permissions`
- `clients`
- `api_applications`
- `api_keys`
- `audit_events`
- `data_access_requests`
- `exports`

## Political directory tables

- `persons`
- `organizations_political`
- `offices`
- `government_bodies`
- `elections`
- `contests`
- `candidacies`
- `committees`
- `committee_relationships`
- `ballot_measures`
- `issues`
- `endorsements`
- `filings`
- `sources`
- `entity_source_assertions`
- `entity_aliases`
- `entity_merge_decisions`

## Geography tables

- `geographies`
- `geography_versions`
- `geography_geometries`
- `geography_relationships`
- `postal_mappings`
- `media_markets`

## Media operations tables

- `advertiser_accounts`
- `campaigns`
- `campaign_strategies`
- `campaign_targeting_rules`
- `budgets`
- `flights`
- `creatives`
- `creative_versions`
- `creative_reviews`
- `compliance_packages`
- `compliance_reviews`
- `inventory_sources`
- `delivery_events_aggregate`
- `delivery_reconciliation`

## Audience and measurement tables

- `audience_sources`
- `audience_segments`
- `audience_segment_versions`
- `audience_segment_policies`
- `audience_approvals`
- `audience_suppressions`
- `identity_match_jobs`
- `conversion_definitions`
- `conversion_events_restricted`
- `attribution_models`
- `attribution_results_aggregate`
- `reports`
- `report_exports`

## Required shared fields

Use immutable UUID primary keys. Major tables should carry `organization_id`, lifecycle status, created/updated metadata, soft-deletion policy where appropriate, and audit correlation IDs. Assertions and relationships require provenance fields: `source_id`, `source_locator`, `observed_at`, `recorded_at`, `valid_from`, `valid_to`, `confidence`, `verification_status`, and reviewer attribution.

## Privacy boundary

Restricted PII and household matching keys should reside in separately governed schemas/datastores with minimal service access. The primary application database should operate on internal references, policy status, aggregates, and authorized derived attributes rather than raw matching material.
