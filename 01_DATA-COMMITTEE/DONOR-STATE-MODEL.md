Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# Donor State Model

## States

```
Prospect → Engaged → First_Gift → Repeat_Donor → Escalating_Donor → High_Value_Core
    ↓          ↓          ↓            ↓                ↓                  ↓
  (exit)    LAPSED ←── LAPSED ←───── LAPSED ←──────── LAPSED ←─────── LAPSED
              ↓
          REACTIVATED → (re-enters at prior level)
```

## State Definitions

| State | Criteria | Trigger In | Trigger Out |
|-------|----------|-----------|------------|
| Prospect | In voter/consumer file, no donation | Data import | First engagement (email open, event RSVP) |
| Engaged | Responded to outreach, no donation | Engagement event | First donation |
| First_Gift | Exactly 1 donation on record | Donation_Event | Second donation OR 18-month inactivity |
| Repeat_Donor | 2-4 donations, none > $250 | Donation_Event | 5th donation OR gift > $250 OR 18-month inactivity |
| Escalating_Donor | 5+ donations OR any gift > $250 | Escalation_Threshold | Gift > $1,000 OR cumulative > $5,000 OR 18-month inactivity |
| High_Value_Core | Any gift > $1,000 OR cumulative > $5,000 | Escalation_Threshold | FEC max-out OR 18-month inactivity |
| LAPSED | No donation in 18+ months from any giving state | Inactivity_Period | New donation (→ REACTIVATED) |
| REACTIVATED | Was LAPSED, made new donation | Donation_Event | Reclassified to appropriate active state |

## Transition Triggers

- **Donation_Event:** Any confirmed donation processed through fec_donations, nc_boe_donations_raw, or winred_donors
- **Escalation_Threshold:** Gift amount or cumulative giving crosses tier boundary
- **Inactivity_Period:** 18 months with no donation (checked nightly)
- **Volatility_Event:** External event (election filing, news surge) that reactivates dormant donors

## Key Tables

### donor_profiles
Rows: Dynamic
Cols: 34
Key Columns:
- person_id (uuid, PK)
- current_state (text, enum of states above)
- lifetime_value (numeric)
- last_gift_date (timestamp)
- last_gift_amount (numeric)
- gift_count (integer)
- escalation_score (numeric, 0-100)
- churn_risk_score (numeric, 0-1)
- preferred_channel (text)

### donor_state_transitions
Key Columns:
- person_id (uuid, FK)
- from_state (text)
- to_state (text)
- triggered_by (text, enum: Donation_Event|Escalation_Threshold|Inactivity_Period|Volatility_Event)
- triggered_at (timestamp)

## Scoring Dimensions
- Recency: Days since last gift (exponential decay)
- Frequency: Gifts in trailing 12 months
- Monetary: Average and max gift amounts
- Escalation Velocity: Rate of giving-level increase ($/year)
- Channel Affinity: Preferred donation channel
- Lapse Risk: P(18+ months without giving) from Lapse_Prediction_Model
