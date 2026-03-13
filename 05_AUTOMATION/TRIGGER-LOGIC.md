# TRIGGER LOGIC (E40)

## Overview

The Trigger Funnel Orchestration engine (E40) is the automation backbone of BroyhillGOP. It monitors events across all ecosystems and fires multi-channel response sequences based on configurable rules.

## Trigger Categories

### Donation Triggers
| Event | Response |
|-------|----------|
| First donation received | Welcome sequence (email + SMS + thank-you mail) |
| Donation > $500 | Major donor flag + personal outreach from candidate |
| Recurring donation started | Recurring donor welcome + escalation track |
| Donation after 12+ month lapse | Reactivation celebration sequence |
| Approaching FEC max-out | Max-out alert to candidate + compliance flag |

### Voter Behavior Triggers
| Event | Response |
|-------|----------|
| Party registration change (D→R or U→R) | Welcome-to-the-party outreach |
| New voter registration in target district | Voter welcome + candidate intro |
| Voter turnout in primary (first time) | Engagement escalation |

### Intelligence Triggers
| Event | Response |
|-------|----------|
| Volatility Index crosses 50 for a district | Resource surge recommendation |
| Authority Index drops > 10 points for a candidate | Alert to party leadership |
| New opposition candidate files | Competitive race alert |
| Legislative vote on hot-button issue | Issue-based donor activation blast |

### Time-Based Triggers
| Event | Response |
|-------|----------|
| 30/60/90 days before election | Escalating ask frequency |
| Filing deadline approaching | Compliance reminder + last-call fundraising push |
| Year-end (Dec 15-31) | Tax-deduction appeal sequence |

## Execution

Triggers fire into channel-specific queues (E30 Email, E31 SMS, E32 Phone, E33 Mail) with priority scoring and fatigue-limit enforcement.
