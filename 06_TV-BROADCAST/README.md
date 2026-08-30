# TV Broadcast Ecosystem

## Political CTV Platform Research Package

This section captures a clean-room architecture brief for a political intelligence, audience activation, connected-TV advertising, compliance, attribution, and reporting platform. It is informed by publicly available information about Vibe.co and is not a copy of Vibe's proprietary software, data, identity graph, models, inventory relationships, or user interface.

## Contents

- `platform-architecture.md` — category definition, modules, services, and backend stack
- `political-hierarchy.md` — political, electoral, geographic, organizational, and permissions models
- `product-requirements.md` — user roles, core workflows, MVP scope, and KPIs
- `compliance-and-privacy.md` — political-ad controls, privacy requirements, auditability, and prohibited shortcuts
- `build-roadmap.md` — phased plan, dependencies, and engineering sequence
- `repository-structure.md` — proposed production monorepo structure
- `research/vibe-public-analysis.md` — public-capability analysis and clean-room boundary
- `data/schema-outline.md` — canonical entities, relationships, provenance, and versioning

## Product thesis

**Political Intelligence and CTV Campaign Operating System**: a platform that unifies political search and directory intelligence; voter, donor, and first-party audience activation; CTV media planning and delivery; creative and compliance workflow; outcome measurement; and an API-first reporting layer.

## Operating principles

1. Use public and licensed sources with recorded provenance.
2. Keep protected voter, donor, and household data outside general-purpose search indexes.
3. Use versioned geography and election-cycle-aware relationships.
4. Design for organization, campaign, and agency isolation from the beginning.
5. Treat political-ad compliance, consent, review, and audit logging as first-class product functions.
6. Build a clean-room system: do not reverse engineer, scrape protected systems, or reproduce proprietary assets.

## Initial architecture decision

Start with a modular monolith for directory, CRM, campaign workflow, compliance, and reporting. Operate real-time event collection and bidding/pacing as separately deployable services only when the product has licensed inventory, scale requirements, and the requisite operational controls.
