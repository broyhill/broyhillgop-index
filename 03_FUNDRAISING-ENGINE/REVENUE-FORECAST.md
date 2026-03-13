# REVENUE FORECAST

## Purpose

Project total fundraising revenue by candidate, channel, and time period. The forecast drives budget planning, staffing decisions, and expectation-setting with candidates and party leadership.

## Methodology

### Bottom-Up Forecast
```
Revenue(c, t) = Σ_segment [ donor_count(seg) × P(donate | seg, c, t) × E[amount | seg, c, t] ]
```

For each donor segment:
1. **Count** active donors in the segment from donor_profiles
2. **Probability** of giving in period t from the Donor Propensity Model
3. **Expected amount** from historical average adjusted by Escalation Predictor

### Top-Down Cross-Check
- Historical revenue by cycle (2020, 2022, 2024) adjusted for candidate strength and environment
- Comparable race analysis using Authority Index and Volatility Index

## Data Inputs

| Input | Source | Rows |
|-------|--------|------|
| Donor segments | donor_profiles | ~170K active donors |
| Historical giving | fec_donations + nc_boe_donations_raw | 1.78M transactions |
| Propensity scores | ML model output | 7.6M scored persons |
| Seasonality curves | Historical daily donation patterns | 6 years of data |
| Candidate pipeline | candidates table | 2,303 candidate records |

## Output

Monthly revenue projection by:
- Candidate (or candidate group)
- Channel (mail, digital, email, event, phone)
- Donor tier (small-dollar, mid-level, major, max-out)
- Confidence interval (P10, P50, P90)
