# DONOR SCORING

## Overview

Every person in the system receives a composite donor score (0-100) predicting their likelihood and capacity to donate to Republican candidates in North Carolina.

## Scoring Model

### Input Features (from 5 data sources)

| Feature Group | Source Table | Key Fields |
|--------------|-------------|------------|
| Prior giving | fec_donations, nc_boe_donations_raw | Amount, frequency, recency, candidate type |
| Voter behavior | nc_voters, nc_datatrust | Party reg, turnout history, partisan score |
| Demographics | acxiom_consumer_data (152 cols) | Income, home value, education, occupation |
| Digital engagement | Contact response tables | Email opens, SMS replies, web visits |
| Network effects | donor_contribution_map (2.5M rows) | Shared giving patterns with known donors |

### Score Components

| Component | Weight | Range |
|-----------|--------|-------|
| Propensity (will they give?) | 40% | 0-100 |
| Capacity (how much can they give?) | 30% | 0-100 |
| Affinity (R vs D lean) | 20% | 0-100 |
| Accessibility (can we reach them?) | 10% | 0-100 |

### Composite Score
```
donor_score = (0.4 × propensity) + (0.3 × capacity) + (0.2 × affinity) + (0.1 × accessibility)
```

## Output Tables
- `donor_profiles` — Stores current composite score and sub-scores
- `donor_score_history` — Tracks score changes over time for trend analysis
- Feeds into: LP Optimization Engine, Trigger Funnel, Candidate Portal Core Donor File
