Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# Resource Constraint Specification

The LP Optimization Engine and Trigger Funnel assume finite operational capacity. This file declares hard limits that constrain all automation and allocation decisions.

## Channel Capacity Limits

| Channel | Constraint Type | Limit | Unit | Binding On |
|---------|----------------|-------|------|-----------|
| Email (E30) | Daily send limit | 50,000 | emails/day | ESP throttle (SendGrid/Mailgun) |
| Email (E30) | Warmup ceiling | 10,000 | emails/day for new domains | Domain reputation protection |
| SMS (E31) | Throughput cap | 5,000 | messages/hour | 10DLC carrier limits |
| SMS (E31) | Daily ceiling | 25,000 | messages/day | Budget + carrier compliance |
| Phone Banking (E32) | Concurrent agents | 50 | simultaneous calls | Staffing + dialer licenses |
| Phone Banking (E32) | Daily capacity | 2,500 | completed calls/day | Agent hours × calls/hour |
| Direct Mail (E33) | Print capacity | 100,000 | pieces/week | Vendor production line |
| Direct Mail (E33) | Lead time | 5 | business days | Design → print → mail |
| RVM (E17) | Throughput | 10,000 | drops/hour | Vendor API limit |
| Events (E34/E37) | Concurrent events | 3 | events/week | Staff + venue availability |
| Events (E34/E37) | Max attendance | 500 | per event | Venue capacity |
| Social/Digital (E19) | Daily ad spend | variable | $/day | Campaign budget allocation |
| IVR (E35) | Concurrent lines | 200 | simultaneous | Telephony infrastructure |

## Compute Constraints

| Resource | Limit | Impact |
|----------|-------|--------|
| Supabase DB connections | 100 concurrent | Limits parallel model scoring jobs |
| Edge Function timeout | 60 seconds | Constrains real-time scoring complexity |
| ML batch job window | 02:00-06:00 UTC | Nightly scoring must complete in 4-hour window |
| GOD FILE rebuild | 15 minutes | Max time for full index regeneration |
| Identity resolution batch | 2 hours | Weekly person_master refresh window |

## Staff Constraints

| Role | Capacity | Hours/Week | Binding On |
|------|----------|-----------|-----------|
| Phone bank agents | 50 max | 40 hrs/week each | E32 Phone Banking throughput |
| Canvassers | 200 max | 20 hrs/week each | E13 Canvassing coverage |
| Data steward | 1 | 40 hrs/week | Model review, compliance audit, override approvals |
| Campaign managers | 1 per candidate | 50 hrs/week | Budget approval, outreach launch authorization |

## LP Integration

All resource constraints are modeled as hard upper bounds in the LP Optimization Engine:

```
x_email(c,t) ≤ 50,000 / num_active_candidates    (daily email cap per candidate)
x_phone(c,t) ≤ 2,500 / num_active_candidates      (daily call cap per candidate)  
x_mail(c,t)  ≤ 100,000 / num_active_candidates    (weekly mail cap per candidate)
x_sms(c,t)   ≤ 25,000 / num_active_candidates     (daily SMS cap per candidate)
```

When resource constraints bind (i.e., demand exceeds capacity), the LP engine allocates scarce capacity to the highest-ELCV contacts first, subject to fatigue and compliance constraints.

```json
{
  "constraint_type": "resource_capacity",
  "enforcement": "hard upper bound in LP",
  "overflow_policy": "allocate by ELCV rank, excess demand queued to next period",
  "monitoring": "daily capacity utilization reported to dashboard",
  "alert_threshold": "> 85% utilization triggers capacity warning"
}
```
