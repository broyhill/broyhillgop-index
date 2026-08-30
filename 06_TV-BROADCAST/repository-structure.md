# Production Repository Structure

```text
political-ctv-platform/
├── apps/
│   ├── web/
│   ├── admin/
│   ├── developer-portal/
│   ├── public-directory/
│   └── docs/
├── services/
│   ├── api-gateway/
│   ├── auth/
│   ├── organizations/
│   ├── political-directory/
│   ├── elections/
│   ├── geography/
│   ├── search/
│   ├── knowledge-graph/
│   ├── crm/
│   ├── audiences/
│   ├── identity-resolution/
│   ├── campaigns/
│   ├── creatives/
│   ├── compliance/
│   ├── budgets/
│   ├── inventory/
│   ├── bidder/
│   ├── pacing/
│   ├── event-collector/
│   ├── attribution/
│   ├── reporting/
│   ├── integrations/
│   ├── billing/
│   └── notifications/
├── workers/
│   ├── audience-import/
│   ├── entity-resolution/
│   ├── voter-file-normalization/
│   ├── district-mapping/
│   ├── creative-transcoding/
│   ├── event-enrichment/
│   ├── report-generation/
│   └── source-verification/
├── packages/
│   ├── ui/
│   ├── database/
│   ├── contracts/
│   ├── event-schemas/
│   ├── permissions/
│   ├── geography/
│   ├── compliance-rules/
│   ├── observability/
│   └── test-fixtures/
├── data/
│   ├── schemas/
│   ├── migrations/
│   ├── seeds/
│   ├── dbt/
│   ├── source-registry/
│   └── quality-tests/
├── ml/
│   ├── reach-forecasting/
│   ├── propensity-models/
│   ├── pacing-models/
│   ├── bid-optimization/
│   ├── identity-matching/
│   ├── anomaly-detection/
│   └── model-registry/
├── integrations/
│   ├── voter-data/
│   ├── crm/
│   ├── analytics/
│   ├── ad-supply/
│   ├── payment/
│   └── government-data/
├── infrastructure/
│   ├── terraform/
│   ├── kubernetes/
│   ├── environments/
│   ├── monitoring/
│   └── disaster-recovery/
├── security/
│   ├── threat-models/
│   ├── data-classification/
│   ├── retention-policies/
│   ├── incident-response/
│   └── privacy-impact-assessments/
├── tests/
│   ├── contract/
│   ├── integration/
│   ├── end-to-end/
│   ├── load/
│   └── compliance/
└── .github/
    ├── workflows/
    ├── CODEOWNERS
    └── pull_request_template.md
```

## Delivery recommendation

Begin with a modular monolith for the directory, CRM, campaign workflow, compliance, and reporting domains. Isolate sensitive data and the event-delivery path early. Do not introduce separate services merely to mimic a large ad-tech architecture; use operational scale, latency, security boundaries, and independent deployment needs as the trigger.
