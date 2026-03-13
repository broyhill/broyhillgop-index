# DISTRICT PERSONALITY MODEL

## Overview

Every political district in North Carolina has a quantifiable "personality" — a composite behavioral and demographic profile that predicts how it will respond to different candidates, messages, and fundraising strategies.

## District Levels

| Level | Count | Source |
|-------|-------|--------|
| Congressional | 13 | nc_voters district mapping |
| State Senate | 50 | nc_voters nc_senate_dist |
| State House | 120 | nc_voters nc_house_dist |
| County | 100 | nc_voters county_id |
| Municipality | 550+ | nc_voters municipality |
| Precinct | ~2,700 | nc_voters precinct |
| School Board | 115 | Legislative feed architecture |

## Personality Dimensions

1. **Partisan Lean** — Republican vote share trend over last 3 cycles
2. **Turnout Elasticity** — How much turnout changes between presidential and off-year elections
3. **Donor Density** — Donors per 1,000 registered voters
4. **Average Gift Size** — Mean donation amount from district residents
5. **Issue Sensitivity** — Which policy topics drive the most engagement (from E42 News Intelligence sentiment analysis)
6. **Volatility Score** — How much the district's behavior swings between cycles
7. **Digital Responsiveness** — Email open rates, SMS response rates, social engagement from the district

## Data Sources

- `nc_voters` (9M rows) — Registration, party, demographics, geographic assignment
- `nc_datatrust` (7.6M rows) — Modeled scores at individual level, aggregated to district
- `nc_boe_donations_raw` (652K rows) — Donation patterns by donor geography
- `fec_donations` (1.1M rows) — Federal giving patterns by ZIP/district
- Contact response data from E30 (Email), E31 (SMS), E32 (Phone Banking)
