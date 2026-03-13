# POLICY DOMAIN VECTOR

## Definition

The Policy Domain Vector is a multi-dimensional representation of issue salience for a donor, district, or candidate. It answers: "What issues does this entity care about most, and how intensely?"

## Dimensions

| Domain | Code | Source Signal |
|--------|------|---------------|
| Fiscal/Tax Policy | FISCAL | Donation patterns to fiscally-focused PACs |
| Immigration | IMMIG | E42 News Intelligence issue tracking |
| Education/School Choice | EDU | School board race engagement, E59 feeds |
| 2nd Amendment | 2A | NRA-affiliated donation patterns |
| Pro-Life | LIFE | Issue-org donation mapping |
| Energy/Environment | ENERGY | Industry employer coding from FEC records |
| Law Enforcement | LAW | Donation to law enforcement PACs/candidates |
| Healthcare | HEALTH | Issue-based campaign contribution patterns |
| Agriculture | AG | Rural district engagement + employer coding |
| Military/Veterans | MIL | Military employer coding + VA proximity |

## Vector Format

Each entity gets a 10-dimensional vector with values 0.0 to 1.0:
```
[FISCAL, IMMIG, EDU, 2A, LIFE, ENERGY, LAW, HEALTH, AG, MIL]
Example donor:  [0.8, 0.3, 0.9, 0.7, 0.6, 0.2, 0.5, 0.1, 0.0, 0.4]
Example district: [0.5, 0.6, 0.4, 0.8, 0.7, 0.3, 0.6, 0.2, 0.9, 0.3]
```

## Application

- **Donor-Candidate Matching:** Cosine similarity between donor vector and candidate vector identifies natural affinity
- **Message Optimization:** Outreach emphasizes issues where the recipient scores highest
- **Candidate Positioning:** Identifies issue gaps in a candidate's donor base for targeted acquisition
