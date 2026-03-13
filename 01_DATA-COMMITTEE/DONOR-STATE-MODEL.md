# DONOR STATE MODEL

## Overview

The Donor State Model tracks every donor's lifecycle position and predicts their trajectory. It is the foundation of the Fundraising Optimization Engine.

## States

```
PROSPECT → FIRST_GIFT → REPEAT_DONOR → COMMITTED → MAJOR_DONOR → MAX_OUT
    ↓           ↓            ↓              ↓            ↓
  LAPSED ←── LAPSED ←──── LAPSED ←────── LAPSED ←──── LAPSED
    ↓
  REACTIVATED → (re-enters at appropriate level)
```

### State Definitions

| State | Criteria | Count (est.) |
|-------|----------|-------------|
| PROSPECT | In voter/consumer file but no donation history | ~7M |
| FIRST_GIFT | Exactly 1 donation on record | ~80K |
| REPEAT_DONOR | 2-4 donations, no single gift > $250 | ~40K |
| COMMITTED | 5+ donations OR recurring donor | ~15K |
| MAJOR_DONOR | Any single gift > $1,000 or cumulative > $5,000 | ~5K |
| MAX_OUT | Hit FEC individual limit ($3,300/election) for at least one candidate | ~2K |
| LAPSED | No donation in 18+ months from any prior giving state | ~30K |
| REACTIVATED | Was LAPSED, made a new donation | ~8K |

## Key Tables

- `donor_profiles` (34 cols) — Current state, lifetime value, last gift date, escalation score
- `donor_state_transitions` — Historical log of every state change with timestamp and trigger
- `donor_contribution_map` (2.5M rows) — Links donors to their individual contributions across all sources
- `donor_contacts` (155K rows) — Contact attempts and responses per donor
- `donor_voter_links` (125K rows) — Maps donors to their voter registration record

## Scoring Dimensions

1. **Recency** — Days since last gift (exponential decay)
2. **Frequency** — Number of gifts in trailing 12 months
3. **Monetary** — Average and max gift amounts
4. **Escalation Velocity** — Rate of increase in giving level
5. **Channel Affinity** — Preferred donation channel (WinRed, mail, event, direct)
6. **Lapse Risk** — Predicted probability of going 18+ months without giving
