Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# Revenue Forecast

## Formula

```
Revenue(c, t) = Σ_segment [
  donor_count(seg)
  × P(donate | seg, c, t)
  × E[amount | seg, c, t]
  × seasonality_multiplier(t)
]
```

Where:
- donor_count(seg): Active donors in segment from donor_clusters
- P(donate): From Donation_Propensity_Model
- E[amount]: Historical average adjusted by Escalation_Predictor output
- seasonality_multiplier: Time-period weight (election proximity, year-end, filing deadlines)

## INPUT TABLES
- donor_profiles (~170K active donors)
- donor_clusters (12 segments)
- donor_propensity_scores
- donor_escalation_scores
- fec_donations (1,132,719 rows)
- nc_boe_donations_raw (652,532 rows)
- candidates (2,303 rows)
- campaign_finance_summary

## OUTPUT TABLES
- revenue_forecast_monthly
- revenue_forecast_by_candidate

## UPDATE FREQUENCY
- Monthly refresh
- Event-triggered recalculation (new candidate, surge event)

## DEPENDENCIES
- Donation_Propensity_Model
- Escalation_Predictor_Model
- Donor_Clustering_Model
- Campaign_Context

## Output Dimensions

Monthly projection segmented by:
- Candidate (or candidate group)
- Channel (mail, digital, email, event, phone)
- Donor tier (small-dollar, mid-level, major, max-out)
- Confidence interval (P10, P50, P90)

## Cross-Check

Top-down validation against historical revenue by cycle (2020, 2022, 2024) adjusted for candidate Authority_Index and Volatility_Index environment.

```json
{
  "model_name": "Revenue_Forecast",
  "type": "Bottom-up segment aggregation with top-down cross-check",
  "formula": "Σ(count × P(donate) × E[amount] × seasonality)",
  "output": "Monthly revenue by candidate × channel × tier with P10/P50/P90",
  "update_frequency": "monthly + event-triggered",
  "dependencies": ["Donation_Propensity_Model", "Escalation_Predictor_Model", "Donor_Clustering_Model"]
}
```
