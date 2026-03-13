Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# DATA GOVERNANCE

## Data Sources and Refresh Cadence

| Source | Refresh | Format | Rows | Authority |
|--------|---------|--------|------|-----------|
| NCSBE Voter File | Weekly | CSV | 9.0M | Official state voter registration |
| DataTrust | Monthly | Flat file | 7.6M | RNC-affiliated voter file vendor |
| FEC Bulk Data | Daily | CSV | 1.1M+ | Federal campaign finance records |
| NCBOE Campaign Finance | Weekly | CSV | 652K | State campaign finance filings |
| RNC Voter Core | Quarterly | Flat file | 1.1M | Republican National Committee |
| Acxiom Consumer | Annual | Licensed | 7.6M | Commercial demographic overlay |
| WinRed | Real-time API | JSON | 194K | Online fundraising platform |

## Identity Resolution

All data sources resolve to a single `person_master` record (7.6M rows) through:
- **Deterministic matching** — SSN hash, voter ID, email, phone
- **Probabilistic matching** — Name + address fuzzy match with confidence scoring
- **Source linking** — `person_source_links` table (1.8M rows) tracks which sources contributed to each golden record

## Compliance

- **FEC Limits:** Individual contribution limits tracked per election cycle ($3,300 primary + $3,300 general for 2025-2026)
- **NCBOE Limits:** State-level limits tracked per candidate and committee type
- **Disclosure:** All donations above threshold automatically flagged for public disclosure reporting
- **Data Privacy:** Voter file data governed by NC General Statute, commercial data by licensing agreements

## Data Quality

| Metric | Value |
|--------|-------|
| Total tables | 657 |
| Populated tables | 100 (15.2%) |
| Empty/staged tables | 557 (84.8%) |
| Total rows | 59,098,347 |
| Total columns | 11,498 |
| Identity-resolved persons | 7,656,550 |
| Cross-source link rate | 24.2% (1.85M links / 7.6M persons) |
