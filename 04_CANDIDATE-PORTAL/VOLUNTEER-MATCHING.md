# VOLUNTEER MATCHING

## Purpose

Match volunteers to candidates and tasks based on skills, geography, availability, and political alignment.

## Data Sources

- `person_master` (7.6M rows) — is_volunteer flag, location, contact info
- `nc_voters` — Party registration, precinct, district assignments
- E05 Volunteer Management ecosystem tables
- E38 Volunteer Coordination ecosystem tables
- E13 Canvassing tables — door-knocking assignment and completion data

## Matching Dimensions

1. **Geography** — Volunteers matched to candidates in their own or adjacent districts
2. **Skills** — Phone banking, canvassing, event setup, data entry, social media
3. **Availability** — Weekday/weekend, hours per week, event dates
4. **Political Alignment** — Policy Domain Vector similarity between volunteer and candidate
5. **Reliability Score** — Historical show-rate from past volunteer commitments

## Output

Ranked volunteer list per candidate with recommended task assignments, integrated into E40 Trigger Funnel for automated recruitment outreach.
