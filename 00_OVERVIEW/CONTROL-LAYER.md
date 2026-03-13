Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# System Control Layer

## Authority Boundaries

### AUTONOMOUS (no human approval required)
- Score recalculation (donor scores, authority index, volatility index)
- Data ingestion from scheduled feeds (FEC, NCSBE, DataTrust, WinRed)
- Identity resolution and person_master updates
- District personality model refresh
- GOD FILE index rebuild
- Model retraining on schedule

### HUMAN-APPROVED (requires explicit authorization)
- Budget allocation changes (LP engine output must be reviewed before execution)
- New candidate activation in pipeline
- Campaign-level outreach launch (first send of any new campaign)
- Compliance exception handling (near-limit donations, late filings)
- Data source onboarding (new vendor or file format)
- Any modification to FEC/NCBOE compliance rules

### ADVISORY ONLY (system recommends, human decides)
- Donor tier reassignment (Platinum/Gold/Silver/Bronze)
- Channel weight overrides for specific segments
- Surge response escalation (Level 2 and Level 3)
- Core Donor File composition changes
- Volunteer-to-candidate matching suggestions

### PROHIBITED (system cannot execute under any circumstances)
- Direct financial transactions or payment processing
- Voter registration modifications
- FEC/NCBOE filing submissions
- Candidate-to-candidate data sharing without RLS enforcement
- Deletion of source records (nc_voters, nc_datatrust, fec_donations)
- Override of contribution limit enforcement

## Data Access Control

| Role | Read | Write | Delete | Scope |
|------|------|-------|--------|-------|
| Platform Admin | All tables | All tables | None (soft-delete only) | Global |
| Campaign Manager | Own candidate + shared models | Own candidate tables | None | Candidate-scoped |
| Data Steward | All tables | Scoring/model tables | None | Model-scoped |
| Candidate User | Own donor file + district data | Contact log only | None | Read-heavy |
| AI Agent | All tables (read) | Scoring tables only | None | Compute-scoped |

## Model Precedence Order

When multiple models produce conflicting recommendations for the same contact, the system resolves conflicts using this strict precedence hierarchy:

| Priority | Layer | Authority | Example |
|----------|-------|-----------|---------|
| 1 | Compliance Constraints | ABSOLUTE | FEC contribution limit reached → block all fundraising asks regardless of model output |
| 2 | Control Layer Prohibitions | ABSOLUTE | Prohibited action (see above) → override all model recommendations |
| 3 | Fatigue Rules | HARD | Contact threshold exceeded → suppress outreach even if propensity is high |
| 4 | Churn Prevention | SOFT OVERRIDE | Lapse_Prediction_Model risk > 0.7 → downgrade ask intensity, switch to soft reactivation |
| 5 | Escalation Logic | CONDITIONAL | Escalation_Predictor recommends tier upgrade → apply ONLY if churn risk < 0.5 |
| 6 | LP Budget Allocation | OPTIMIZATION | Allocate channel spend within remaining constraints |
| 7 | Authority Weighting | MODIFIER | Authority_Index adjusts expected ROI within LP allocation |
| 8 | District Personality | MODIFIER | District model adjusts channel weight and message tone |
| 9 | Message Optimization | FINAL | Select creative/copy variant optimized for contact's Policy_Domain_Vector |

### Conflict Resolution Rules

1. Higher-priority layers ALWAYS override lower-priority layers. No exceptions.
2. ABSOLUTE layers cannot be overridden by any model output or human override.
3. SOFT OVERRIDE layers can be overridden by human approval (logged to audit_log).
4. MODIFIER layers adjust parameters within bounds set by higher layers — they never expand bounds.
5. When two layers at the same priority conflict, the more conservative action wins (lower ask, softer channel, fewer touches).

### Example Conflict Resolution

Scenario: Donor #12345
- ML Propensity Model: 92% likely to give → recommends $1,000 ask
- Authority Model: Candidate has Authority_Index 85 → suggests escalation
- District Model: District cluster is "price-sensitive suburban" → downweights large asks
- Churn Model: Churn risk 0.65 → suggests soft reactivation

Resolution (applied top-down):
1. Compliance: No FEC limit issue → PASS
2. Control Layer: No prohibited action → PASS
3. Fatigue: 2 touches this week (< 3 threshold) → PASS
4. Churn Prevention: Risk 0.65 < 0.7 → does NOT override, but flags for monitoring
5. Escalation: Allowed (churn < 0.5 threshold NOT met, so escalation is CONDITIONAL — apply conservative variant)
6. LP Allocation: Budget available in email + mail channels
7. Authority: High authority → keep $500 ask (conservative escalation, not full $1,000)
8. District: Suburban cluster → route to email (not mail), soften copy tone
9. Message: Select issue-aligned creative based on Policy_Domain_Vector

Final action: $500 email ask with soft-tone suburban-optimized creative

## Audit Trail

All write operations logged to:
- Table: audit_log
- Fields: timestamp, actor_type (human|system|ai), actor_id, table_name, operation, old_value, new_value
- Retention: Indefinite
