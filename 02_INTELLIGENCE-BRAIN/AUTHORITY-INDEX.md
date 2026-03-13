# AUTHORITY INDEX

## Definition

The Authority Index measures a candidate's institutional credibility, endorsement portfolio, and organizational support strength. It quantifies "who is backing this person and how much weight does that backing carry."

## Components

| Component | Weight | Source |
|-----------|--------|--------|
| Endorsement Quality | 30% | endorsement_tracking table — weighted by endorser's own authority |
| Fundraising Network Depth | 25% | fec_god_contributions — unique donor count and max-out rate |
| Party Support Level | 20% | Committee contributions from fec_party_committee_donations (2.5M rows) |
| Incumbent Advantage | 15% | candidates table (242 cols) — prior election wins, margin of victory |
| Media Authority | 10% | E42 News Intelligence — mention frequency and sentiment |

## Scale

0-100, where:
- 0-20: Unknown challenger, no institutional support
- 21-40: Recognized candidate with some endorsements
- 41-60: Competitive candidate with party support
- 61-80: Strong candidate with deep institutional backing
- 81-100: Dominant incumbent or party-anointed frontrunner

## Usage

The Authority Index feeds directly into:
- **Donor matching** — High-authority candidates attract major donors; low-authority candidates need grassroots strategies
- **Budget allocation** — LP engine weights authority when distributing resources across races
- **Trigger logic** — Authority changes (new endorsement, major donation) fire automated outreach sequences
