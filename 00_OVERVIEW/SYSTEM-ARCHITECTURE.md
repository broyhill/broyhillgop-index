Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# SYSTEM ARCHITECTURE

## Technology Stack

| Layer | Technology | Role |
|-------|-----------|------|
| Database | Supabase PostgreSQL | 657 tables, 59M rows, Row Level Security |
| Backend | Supabase Edge Functions | API layer, triggers, real-time subscriptions |
| Frontend | Inspinia Admin (planned) | Campaign management dashboard |
| Identity | Custom resolution engine | Deterministic + probabilistic person matching |
| ML/AI | Python + Supabase | Clustering, propensity scoring, lookalikes |
| File Index | GOD FILE v4 (HTML) | 4,071 files searchable via browser |

## Database Architecture

### Top Tables by Row Count

| Table | Rows | Columns | Indexes | Domain |
|-------|------|---------|---------|--------|
| nc_voters | 9,049,588 | 71 | 29 | Voter registration |
| person_master | 7,656,550 | 37 | 9 | Identity spine |
| acxiom_consumer_data | 7,655,559 | 152 | 10 | Consumer overlay |
| nc_datatrust | 7,654,883 | 251 | 15 | Voter file + scores |
| datatrust_profiles | 7,654,624 | 73 | 24 | Processed profiles |
| fec_party_committee_donations | 2,574,992 | 28 | 11 | PAC/committee donations |
| donor_contribution_map | 2,523,766 | 7 | 9 | Donor-to-contribution links |
| person_source_links | 1,850,683 | 6 | 3 | Cross-source identity links |
| fec_donations | 1,132,719 | 24 | 6 | Federal donations |
| rnc_voter_core | 1,105,946 | 62 | 19 | RNC voter file |
| nc_boe_donations_raw | 652,532 | 61 | 28 | State donations |
| fec_god_contributions | 226,451 | 127 | 22 | Enriched FEC records |
| winred_donors | 194,279 | 26 | 5 | Online donations |

### Ecosystem Distribution
- 63 ecosystem groups across 657 tables
- 100 tables populated (15.2%), 557 staged empty (84.8%)
- Data concentrated in CORE Data/Identity and Fundraising ecosystems

## 7-Layer Perplexity Blueprint

Every ecosystem follows a standardized 7-layer documentation format:

1. **DDL** — Table definitions, columns, types, constraints
2. **Indexes** — Performance indexes, unique constraints, composite keys
3. **RLS** — Row Level Security policies for multi-tenant access
4. **API** — Supabase Edge Function endpoints and REST patterns
5. **Triggers** — Database triggers for automation and data integrity
6. **Brain Integration** — How the ecosystem feeds/receives from E20 Intelligence Brain
7. **Inspinia Admin** — Dashboard UI components and admin interface specs
