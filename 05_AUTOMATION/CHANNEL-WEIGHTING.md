Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# CHANNEL WEIGHTING

## Purpose

Determine the optimal mix of outreach channels for each donor/voter contact based on their demonstrated preferences and predicted responsiveness.

## Channels

| Channel | Ecosystem | Capacity | Cost per Contact |
|---------|-----------|----------|-----------------|
| Email | E30 | Unlimited | ~$0.01 |
| SMS | E31 | Unlimited | ~$0.03 |
| Phone Banking | E32 | Agent-limited | ~$1.50 |
| Direct Mail | E33 | Print-limited | ~$0.75 |
| Events | E34/E37 | Venue-limited | ~$25 |
| Ringless Voicemail | E17 | Unlimited | ~$0.04 |
| Interactive Voice | E35 | Unlimited | ~$0.08 |
| Social Media | E19 | Budget-limited | ~$0.15 (CPM) |
| Digital Ads | E16 | Budget-limited | ~$0.50 (CPC) |

## Weight Calculation

Each contact gets a channel weight vector based on:
1. **Historical response** — Which channels has this person responded to before?
2. **Demographic prediction** — Age, income, and digital literacy proxies from acxiom_consumer_data
3. **Cost efficiency** — Expected ROI per dollar by channel for this person's donor tier
4. **Fatigue state** — How recently were they contacted on each channel?
5. **Message type** — Fundraising asks work differently than informational updates

## Output

Channel weight vector per person, consumed by the LP Optimization Engine and Trigger Funnel to route each outreach action to the highest-expected-value channel.
