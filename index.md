Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# BroyhillGOP Political Operating System Index

## SYSTEM ROLE

Enterprise multi-tenant Republican campaign CRM and intelligence engine serving North Carolina GOP operations across 58+ ecosystems, 657 database tables, and 59 million rows of voter, donor, and political intelligence data.

## CORE OBJECTS

| Object | Description | Primary Table(s) |
|--------|-------------|-------------------|
| Donor_State | Lifecycle position of each donor (prospect → first-gift → repeat → major → lapsed) | donor_profiles, donor_state_transitions |
| Campaign_Context | Active campaign environment including election cycle, district, and candidate | campaigns, campaign_finance_summary |
| District_Personality | Composite behavioral/demographic profile of a geographic district | district_personality_scores, nc_voters |
| Authority_Index | Measure of a candidate's institutional credibility and endorsement weight | authority_scores, endorsement_tracking |
| Volatility_Index | Measure of how likely a district or donor segment is to shift behavior | volatility_scores, swing_analysis |
| Behavioral_Profile | Cross-channel engagement fingerprint for each contact | person_master (7.6M rows), contact_enrichment |

## PRIMARY ENGINES

1. **Intelligence Brain (E20)** — Centralized decision layer that scores, routes, and prioritizes across all ecosystems
2. **Fundraising Optimization Engine (E01/E02/E03)** — Donor import, processing, scoring, and campaign-candidate matching
3. **Machine Learning Layer (E21)** — Clustering, propensity modeling, lookalike audiences, and predictive donor scoring
4. **Linear Programming Allocation Engine** — Optimizes budget allocation across channels (mail, digital, events, phone) to maximize ROI per dollar
5. **Trigger Funnel Orchestration (E40)** — Event-driven automation that fires multi-channel sequences based on donor/voter behavior signals

## DATA SOURCES

| Source | Table | Rows | Columns | Description |
|--------|-------|------|---------|-------------|
| DataTrust Voter File | nc_datatrust | 7,654,883 | 251 | Full NC voter universe with modeled scores |
| NC Voter Registration | nc_voters | 9,049,588 | 71 | Official NCSBE voter registration file |
| NCBOE Donations | nc_boe_donations_raw | 652,532 | 61 | NC Board of Elections campaign finance records |
| FEC Enriched | fec_donations | 1,132,719 | 24 | Federal Election Commission individual contributions |
| FEC GOD Contributions | fec_god_contributions | 226,451 | 127 | Fully enriched FEC records with 127 derived fields |
| RNC Voter Core | rnc_voter_core | 1,105,946 | 62 | Republican National Committee voter file |
| WinRed Feedback | winred_donors | 194,279 | 26 | WinRed online donation platform data |
| Person Master | person_master | 7,656,550 | 37 | Golden record identity spine |
| Acxiom Consumer | acxiom_consumer_data | 7,655,559 | 152 | Commercial consumer/demographic overlay |

## MODELING OBJECTIVE

Maximize:
- **Revenue Velocity** — Reduce time-to-first-gift and increase donation frequency
- **Repeat Donation Intensity** — Drive single-gift donors into recurring giving patterns
- **Escalation Yield** — Move donors up the giving ladder ($25 → $100 → $500 → $2,800 max-out)
- **Strategic Authority Leverage** — Deploy high-authority endorsements to districts where volatility creates opportunity

## PLATFORM STATS

- **58 ecosystems** spanning data, outreach, intelligence, compliance, and automation
- **657 PostgreSQL tables** in Supabase (100 populated, 557 staged for build-out)
- **59,098,347 total rows** of political data
- **11,498 columns** across all tables
- **4,071 indexed files** in the GOD FILE document search engine

## NAVIGATION

- [00_OVERVIEW/](00_OVERVIEW/) — Mission, Architecture, Data Governance, Canonical Objects, Control Layer, Data Firewall, System State Graph, Failure Modes
- [01_DATA-COMMITTEE/](01_DATA-COMMITTEE/) — GOD File, Master Schema, Donor State Model, District Personality, Model Registry, Feature Lineage, Compatibility Matrix
- [02_INTELLIGENCE-BRAIN/](02_INTELLIGENCE-BRAIN/) — Authority Index, Volatility Index, Policy Domain Vector
- [03_FUNDRAISING-ENGINE/](03_FUNDRAISING-ENGINE/) — Donor scoring, ML models, LP optimization, revenue forecasting
- [04_CANDIDATE-PORTAL/](04_CANDIDATE-PORTAL/) — Activation pipeline, core donor files, volunteer matching
- [05_AUTOMATION/](05_AUTOMATION/) — Trigger Logic, Channel Weighting, Surge Detection, Resource Constraint Spec
- [99_CHANGELOG/](99_CHANGELOG/) — Version history
