# SURGE DETECTION

## Purpose

Detect sudden spikes in political activity — donation surges, voter registration waves, news events, social media momentum — and automatically escalate platform response.

## Monitored Signals

| Signal | Source | Baseline | Surge Threshold |
|--------|--------|----------|----------------|
| Donation velocity | fec_donations + nc_boe_donations_raw ingest | 7-day rolling average | > 2σ above mean |
| Voter registration rate | nc_voters weekly delta | Monthly average | > 50% above monthly norm |
| News mention frequency | E42 News Intelligence feeds | 30-day rolling average | > 3× average |
| Social media engagement | E19 Social Media metrics | Weekly average | > 2× weekly norm |
| Email response rate | E30 Email open/click tracking | Campaign average | > 1.5× campaign average |
| WinRed real-time feed | winred_donors API | Daily average | > 3× daily average |

## Response Protocol

### Level 1: Elevated (1-2 signals above threshold)
- Alert to campaign manager dashboard
- Increase email send frequency by 25%
- Queue supplemental social media content

### Level 2: Surge (3+ signals above threshold)
- Alert to party leadership
- Deploy reserve budget allocation from LP engine
- Activate all dormant trigger sequences for affected district/candidate
- Fast-track direct mail production

### Level 3: Critical (any signal > 5σ or combined score > 10σ)
- Full war-room alert
- Override LP allocation — concentrate resources on surge target
- Deploy all channels simultaneously
- Real-time reporting to all stakeholders every 2 hours

## Integration

Surge Detection feeds into E40 Trigger Logic as a meta-trigger that can amplify or override normal automation sequences.
