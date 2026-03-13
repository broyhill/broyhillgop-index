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

## Audit Trail

All write operations logged to:
- Table: audit_log
- Fields: timestamp, actor_type (human|system|ai), actor_id, table_name, operation, old_value, new_value
- Retention: Indefinite
