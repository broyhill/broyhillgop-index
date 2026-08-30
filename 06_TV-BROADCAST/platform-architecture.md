# Platform Architecture

## Category

**Political Intelligence and CTV Campaign Operating System**

The platform is not only an ad-buying tool. It is a political search, directory, audience, media-activation, compliance, attribution, and reporting system.

| Layer | Product responsibility |
|---|---|
| Political directory | Search offices, candidates, officials, committees, races, districts, ballot measures, vendors, and issues |
| Political CRM | Manage campaigns, contacts, supporters, donors, volunteers, organizations, and vendors |
| Audience intelligence | Build voter, donor, first-party, geographic, contextual, suppression, and modeled segments |
| Media activation | Configure CTV campaigns, inventory, geography, audience, budgets, schedules, and frequency |
| Creative operations | Ingest, transcode, version, approve, and assign video assets |
| Compliance | Capture sponsor, disclaimer, authorization, jurisdiction, review, and invoice records |
| Measurement | Report delivery, completion, reach, frequency, visits, donations, sign-ups, and modeled lift |
| Knowledge graph | Link people, offices, elections, districts, committees, organizations, issues, sources, and campaigns |
| Developer platform | Expose secure APIs, webhooks, exports, and approved embedded workflows |

## Major application modules

### Discovery and directory

- Global entity search, filters, saved searches, watchlists, source citations, and verification timestamps.
- Entity profiles for people, organizations, offices, races, districts, committees, ballot measures, issues, and media assets.
- Versioned district maps, election calendars, filing deadlines, and jurisdiction lookup.

### Audience builder

- First-party CRM and consented web audiences.
- Licensed voter and consumer segments through contractual activation partners.
- Geographic, district, county, DMA, ZIP, contextual, and device strategies.
- Suppression, overlap, size/reach estimates, approval, expiration, and version controls.

### Campaign builder

```text
Organization
└── Advertiser account
    └── Political client
        └── Campaign
            ├── Strategy / line item
            │   ├── Audience segments
            │   ├── Geography
            │   ├── Inventory and devices
            │   ├── Schedule / dayparts
            │   ├── Bid / CPM and frequency rules
            │   └── Budget pacing
            ├── Creatives
            ├── Compliance package
            ├── Conversion goals
            └── Reports
```

### Delivery and decisioning

- Inventory catalog and supply integrations.
- Bid-request ingestion, eligibility filtering, audience matching, bid calculation, pacing, frequency caps, and creative selection.
- Win, impression, quartile, completion, spend, invalid-traffic, and reconciliation processing.
- Campaign pause controls, spend guardrails, anomaly detection, and emergency kill switches.

### Measurement

- Impressions, completed views, reach, frequency, CPM, cost per completed view, delivery pacing, and geo/audience/creative performance.
- Site visits, donations, sign-ups, volunteer actions, events, conversion paths, and modeled incrementality where valid methodology and consent allow.
- Scheduled reporting, CSV/API exports, executive dashboards, and immutable audit trails.

## Recommended clean-room stack

| Layer | Recommended implementation |
|---|---|
| Web | Next.js, React, TypeScript, Tailwind, shadcn/ui |
| Application APIs | NestJS or FastAPI |
| Low-latency decisioning | Go or Rust |
| Transactional data | PostgreSQL and PostGIS |
| Keyword search | OpenSearch |
| Semantic retrieval | pgvector initially |
| Graph | PostgreSQL relationship model; Neo4j only if justified |
| Cache / fast control state | Redis |
| Event streaming | Kafka or Redpanda |
| Analytics | ClickHouse |
| Orchestration | Temporal for operational workflows; Dagster for data pipelines |
| Object storage | S3-compatible object store |
| ML | Python, Polars, LightGBM/XGBoost, FastAPI model serving |
| Auth | Keycloak, Auth0, or Clerk; organization-scoped RBAC |
| Observability | OpenTelemetry, Prometheus, Grafana, Loki, Sentry |
| Infrastructure | AWS, Terraform, GitHub Actions, managed secrets |

## Service boundaries

```text
API Gateway
├── Identity and Access
├── Organizations
├── Political Directory
├── Elections
├── Geography
├── Search
├── Knowledge Graph
├── CRM
├── Audiences
├── Identity Resolution
├── Campaigns
├── Creatives
├── Compliance
├── Budgets
├── Inventory
├── Bidder and Pacing
├── Event Collector
├── Attribution
├── Reporting
├── Integrations
├── Billing
└── Notifications
```

## Data separation

Public political entities and approved aggregate metadata can be indexed for search. Protected records—voter files, household identity keys, raw donor data, CRM PII, event IDs, and match keys—must remain in restricted stores behind explicit permissions, retention policies, and purpose controls. Search should return authorized entity references, not unrestricted raw records.
