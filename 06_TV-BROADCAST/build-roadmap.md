# Build Roadmap

## Phase 0 — Product and governance foundation

- Confirm commercial model: directory-only, intelligence platform, managed media, licensed DSP integration, or full ad-tech platform.
- Identify legal counsel and policy owners for political advertising, privacy, data licensing, and election-specific requirements.
- Define source registry, data classification, tenant model, threat model, and audit requirements.
- Establish clean-room research policy and vendor due diligence checklist.

## Phase 1 — Political intelligence MVP

- Build organizations, roles, access policies, and audit events.
- Implement core entities: people, offices, districts, elections, contests, committees, issues, and sources.
- Add keyword search, filters, profiles, saved searches, source citations, and verification states.
- Load public/licensed reference data with provenance and versioning.

**Exit criterion:** authorized users can research a race, navigate entity relationships, and export defensible, source-backed summaries.

## Phase 2 — Campaign operations and compliance

- Add advertiser/client accounts, campaign workflow, budget, dates, strategies, creative library, and approval gates.
- Implement compliance package, required fields, review queue, exception process, and full audit history.
- Add aggregate reporting shell with manual or partner-supplied delivery feeds.

**Exit criterion:** teams can create a reviewable political CTV media plan with reliable change tracking.

## Phase 3 — Audience and geo activation

- Implement consent-aware first-party audience ingest, segmenting, suppression, expiration, and approvals.
- Add PostGIS geography engine, district versions, county/DMA/ZIP targeting and overlap rules.
- Integrate only approved voter/audience providers under contract.

**Exit criterion:** authorized users can create policy-valid segments and attach them to approved strategies.

## Phase 4 — Licensed media delivery and attribution

- Integrate with a licensed DSP, supply path, or managed-service partner.
- Implement event collection, pacing, delivery reconciliation, creative status, frequency controls, and reporting exports.
- Add web/app conversion event pipeline where consent and contracts permit.

**Exit criterion:** production campaigns can be activated, monitored, paused, reconciled, and reported through a controlled operating model.

## Phase 5 — Scale and optimization

- Introduce event streaming, analytics warehouse, forecasting, anomaly detection, and approved bid/pacing optimization.
- Expand API/webhook platform and partner marketplace.
- Add controlled experimentation and incrementality measurement methodology.

## Dependency risks

- Political/voter data licensing and activation agreements.
- CTV inventory and DSP/supply integration agreements.
- Legal/policy review across jurisdiction and election cycles.
- Identity resolution quality and privacy-safe measurement.
- Data freshness, redistricting/version control, and source provenance.
- Operational capacity for campaign support, billing, reconciliation, and incident response.
