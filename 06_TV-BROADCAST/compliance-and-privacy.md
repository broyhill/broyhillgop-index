# Compliance, Privacy, and Safety Controls

## Non-negotiable design principles

- Political advertising requires jurisdiction-specific legal review. This system must support compliance workflow; it must not make unsupported legal determinations.
- Use only properly licensed inventory, voter, consumer, identity, CRM, and measurement data.
- Do not ingest, expose, or activate sensitive data unless the law, data contract, consent model, platform policy, and internal review explicitly permit it.
- Maintain immutable audit records for audience creation, access, export, campaign changes, creative approvals, disclosure review, and activation.
- Separate public political research data from protected personal data.

## Compliance package per campaign

- Advertiser/client legal entity
- Sponsor identity and contact information
- Campaign/committee relationship
- Required disclaimer text and presentation evidence
- Jurisdictions and contest/election context
- Creative identifiers, versions, upload source, and review status
- Authorized approver(s), timestamps, review decisions, and reasons
- Billing/invoice entity
- Supply-platform policy acceptance and exception record

## Audience governance

- Segment owner, approved purpose, source contract, consent/legal basis, creation time, expiration, and renewal workflow.
- Explicit suppression and deletion processing.
- No unrestricted raw PII in dashboards, URLs, logs, error messages, exports, model features, or search indexes.
- Encrypt protected data in transit and at rest; use scoped service credentials and per-tenant access controls.
- Enforce minimum audience thresholds where required by policy or contract.
- Maintain access and export logs containing actor, object, purpose, time, destination, and approval context.

## High-risk controls

- Dual approval for bulk exports, sensitive segment activation, and production policy overrides.
- Kill switch for campaigns, integrations, and creative assets.
- Spend caps at organization, client, campaign, strategy, and supply-source levels.
- Rate limits, fraud/invalid-traffic controls, reconciliation jobs, and anomaly alerts.
- Data retention schedules, incident response plan, and documented processor/subprocessor inventory.

## Clean-room boundary

This project may use publicly observable product claims and independently developed specifications. It must not obtain or reproduce Vibe.co's private code, proprietary data, credentialed APIs, private audience graph, auction logic, nonpublic documentation, trade secrets, or protected creative/interface assets.
