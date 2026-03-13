Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# VOLATILITY INDEX

## Definition

The Volatility Index measures how likely a district, donor segment, or race outcome is to shift from its current trajectory. High volatility = high opportunity (or high risk).

## Calculation

Volatility is computed at three levels:

### District Volatility
- Margin swing between last 2 election cycles
- Registration party-switch rate (trailing 12 months)
- Unaffiliated voter share trend
- Source: nc_voters party changes + election results

### Donor Volatility
- Gift amount variance (standard deviation of last 5 gifts)
- Cross-party giving (donors who give to both R and D candidates)
- Channel switching frequency
- Source: fec_donations + nc_boe_donations_raw + donor_profiles

### Race Volatility
- Polling movement (where available)
- Fundraising momentum shifts (quarter-over-quarter)
- Authority Index changes
- Opposition candidate emergence

## Scale

0-100:
- 0-25: Stable — predictable behavior, low opportunity for change
- 26-50: Moderate — some movement, worth monitoring
- 51-75: Volatile — active shifts, prioritize for intervention
- 76-100: Extreme — rapid change, deploy resources immediately

## Strategic Application

The Volatility Index is multiplied against the Authority Index to produce an **Opportunity Score**:
```
Opportunity = Volatility × (1 - Authority/100)
```
High volatility + low authority = maximum opportunity for intervention.
