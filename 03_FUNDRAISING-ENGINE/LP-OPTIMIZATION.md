Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# Linear Programming Allocation Engine

## Objective Function

Maximize:

```
Σ_i (
  ELCV_i
  × Conversion_Probability_i
  × District_Modifier_i
  × Authority_Modifier_i
  − Channel_Cost_i
  − Fatigue_Penalty_i
)
```

Where:
- ELCV_i = Expected Lifetime Contribution Value for contact i
- Conversion_Probability_i = P(donation | contact, channel, timing) from Donation_Propensity_Model
- District_Modifier_i = District_Personality volatility-adjusted multiplier
- Authority_Modifier_i = Candidate Authority_Index weight (higher authority → higher expected return)
- Channel_Cost_i = Cost per contact for the assigned channel
- Fatigue_Penalty_i = Monotonically increasing cost of over-contacting donor i

## Fatigue Penalty Function

```
Fatigue_Penalty_i = α × (contacts_trailing_7d / fatigue_threshold)^β
```

Where:
- contacts_trailing_7d = total touches across all channels in last 7 days for person i
- fatigue_threshold = maximum acceptable touches per week (default: 3)
- α = penalty scaling factor (calibrated per channel)
- β = convexity exponent (β > 1 ensures accelerating penalty; default: 2.0)

Effect: Penalty is near-zero below threshold, then rises sharply. Prevents LP from concentrating all budget on the top-propensity donors.

## INPUT TABLES
- donor_propensity_scores
- donor_profiles
- district_personality_scores
- authority_scores
- campaign_finance_summary
- channel_cost_rates

## OUTPUT TABLES
- budget_allocation_plan
- channel_assignment_queue

## UPDATE FREQUENCY
- Weekly optimization cycle
- Real-time surge override (Level 2+)

## DEPENDENCIES
- Donation_Propensity_Model
- Authority_Index
- Volatility_Index
- District_Personality
- Channel_Weighting

## Decision Variables

| Variable | Description |
|----------|-------------|
| x_mail(c,t) | Direct mail spend for candidate c in period t |
| x_email(c,t) | Email campaign spend for candidate c in period t |
| x_sms(c,t) | SMS outreach spend for candidate c in period t |
| x_phone(c,t) | Phone banking spend for candidate c in period t |
| x_digital(c,t) | Digital ad spend for candidate c in period t |
| x_event(c,t) | Event spend for candidate c in period t |

## Constraints

Subject to:
1. **Channel_Budget:** Σ_ch x_ch(c,t) ≤ total_budget
2. **Per-Candidate Bounds:** min_spend(c) ≤ Σ_ch x_ch(c,t) ≤ max_spend(c)
3. **Contact_Fatigue_Threshold:** ≤ 3 touches per donor per channel per week
4. **Staff_Time_Constraint:** Phone banking hours ≤ available agent hours
5. **Compliance_Envelope:** Coordinated expenditure limits per FEC rules
6. **Print_Capacity:** x_mail ≤ vendor production capacity per period

```json
{
  "model_name": "LP_Allocation_Engine",
  "type": "Linear Programming (Simplex/Interior Point)",
  "objective": "Maximize Σ(ELCV × P(conversion) × district_mod × authority_mod − channel_cost − fatigue_penalty)",
  "constraints": ["channel_budget", "per_candidate_bounds", "fatigue_threshold", "staff_time", "compliance_envelope", "print_capacity"],
  "fatigue_penalty": "α × (contacts_7d / threshold)^β, β=2.0, accelerating penalty above 3 touches/week",
  "input_models": ["Donation_Propensity_Model", "Authority_Index", "District_Personality", "Volatility_Index"],
  "output": "budget_allocation_plan",
  "update_frequency": "weekly + surge override"
}
```
