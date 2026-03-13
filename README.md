Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# SYSTEM ROLE

Enterprise multi-tenant Republican campaign CRM and optimization engine serving North Carolina GOP operations.

## CORE GUARANTEE

- No candidate-to-candidate data leakage (RLS-enforced)
- Centralized model training on shared data
- Siloed execution per candidate
- Compliance-aligned architecture (FEC + NCBOE rules embedded in data model)

## PRIMARY OBJECTIVE

Maximize revenue velocity for registered Republican campaign committees before election day.

## PLATFORM STATS

- 58 ecosystems | 657 tables | 59,098,347 rows | 11,498 columns
- 100 populated tables (15.2%) | 557 staged (84.8%)
- 4,071 indexed files across 83 categories

## SEARCH ENGINE

Live: https://broyhill.github.io/broyhillgop-index/

## NAVIGATION

| Section | Path | Contents |
|---------|------|----------|
| Overview | [00_OVERVIEW/](00_OVERVIEW/) | Mission, Architecture, Data Governance, Canonical Objects, Control Layer |
| Data Committee | [01_DATA-COMMITTEE/](01_DATA-COMMITTEE/) | GOD File, Master Schema, Donor State Model, District Personality, Model Registry |
| Intelligence Brain | [02_INTELLIGENCE-BRAIN/](02_INTELLIGENCE-BRAIN/) | Authority Index, Volatility Index, Policy Domain Vector |
| Fundraising Engine | [03_FUNDRAISING-ENGINE/](03_FUNDRAISING-ENGINE/) | Donor Scoring, ML Models, LP Optimization, Revenue Forecast |
| Candidate Portal | [04_CANDIDATE-PORTAL/](04_CANDIDATE-PORTAL/) | Activation Pipeline, Core Donor File, Volunteer Matching |
| Automation | [05_AUTOMATION/](05_AUTOMATION/) | Trigger Logic, Channel Weighting, Surge Detection |
| Changelog | [99_CHANGELOG/](99_CHANGELOG/) | Version History |

## DATA SOURCES

| Source | Table | Rows | Columns |
|--------|-------|------|---------|
| NC Voter Registration | nc_voters | 9,049,588 | 71 |
| DataTrust Voter File | nc_datatrust | 7,654,883 | 251 |
| Person Master (Golden Record) | person_master | 7,656,550 | 37 |
| Acxiom Consumer | acxiom_consumer_data | 7,655,559 | 152 |
| FEC Donations | fec_donations | 1,132,719 | 24 |
| FEC GOD Contributions | fec_god_contributions | 226,451 | 127 |
| RNC Voter Core | rnc_voter_core | 1,105,946 | 62 |
| NCBOE Donations | nc_boe_donations_raw | 652,532 | 61 |
| WinRed | winred_donors | 194,279 | 26 |
