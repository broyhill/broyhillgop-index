# LINEAR PROGRAMMING ALLOCATION ENGINE

## Purpose

The LP engine solves the budget allocation problem: given a fixed fundraising budget, how should dollars be distributed across channels, candidates, and time periods to maximize total return?

## Decision Variables

| Variable | Description |
|----------|-------------|
| x_mail(c,t) | Direct mail spend for candidate c in period t |
| x_email(c,t) | Email campaign spend for candidate c in period t |
| x_sms(c,t) | SMS outreach spend for candidate c in period t |
| x_phone(c,t) | Phone banking spend for candidate c in period t |
| x_digital(c,t) | Digital ad spend for candidate c in period t |
| x_event(c,t) | Event spend for candidate c in period t |

## Objective Function

Maximize total expected revenue:
```
max Σ_c Σ_t Σ_ch [ ROI(c, ch) × x_ch(c, t) × seasonality(t) × volatility_boost(c) ]
```

Where:
- ROI(c, ch) = historical return on investment for candidate c in channel ch
- seasonality(t) = time-period multiplier (donations spike near elections, year-end, filing deadlines)
- volatility_boost(c) = multiplier for high-volatility races where marginal dollars have outsized impact

## Constraints

1. **Budget:** Σ all x ≤ total_budget
2. **Per-candidate min/max:** min_spend(c) ≤ Σ_ch x_ch(c,t) ≤ max_spend(c)
3. **Channel capacity:** x_ch ≤ channel_capacity (e.g., can't send more mail than the print vendor can produce)
4. **Compliance:** Coordinated expenditure limits per FEC rules
5. **Fatigue:** Contact frequency caps per donor per channel per week

## Inputs from Other Engines

- **Donor Scoring** → Expected response rates per segment per channel
- **Authority Index** → Candidate viability weighting
- **Volatility Index** → Opportunity multiplier for marginal races
- **District Personality** → Channel preference by geography
