Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# Data Committee Firewall Model

This specification defines the tenant isolation, data propagation, and cross-boundary rules for the multi-tenant BroyhillGOP platform.

## Tenant Scope Definition

| Tenant Type | Scope | Example |
|------------|-------|---------|
| Candidate | Single candidate campaign | "John Smith for NC Senate District 42" |
| Committee | Party committee or PAC | "Forsyth County Republican Party" |
| Platform | Shared infrastructure | BroyhillGOP central operations |

## Data Classification

### CANNOT Propagate Across Tenants

| Data Type | Reason | Enforcement |
|-----------|--------|-------------|
| Individual donor contact history | Candidate-specific relationship | RLS policy on donor_contacts |
| Fundraising ask amounts | Competitive intelligence | RLS policy on outreach_log |
| Donor response data (opens, clicks, replies) | Campaign-specific engagement | RLS policy on channel response tables |
| Core Donor File composition | Strategic asset | RLS policy on candidate_donor_files |
| Budget allocation details | Financial privacy | RLS policy on budget_allocation_plan |
| Internal campaign communications | Privileged | RLS policy on campaign_notes |

### CANNOT Be Tenant-Specific (Trained Centrally)

| Asset | Reason | Scope |
|-------|--------|-------|
| Donation_Propensity_Model | Requires full training data for statistical power | Platform-wide |
| Donor_Clustering_Model | Segments must be consistent across candidates | Platform-wide |
| Lapse_Prediction_Model | Churn patterns are universal | Platform-wide |
| District_Personality_Model | Districts serve multiple candidates | Platform-wide |
| Identity Resolution | Golden record must be singular | Platform-wide |
| Volatility_Index | District-level, not candidate-level | Platform-wide |

### Tenant-Scoped Data

| Data Type | Scoped To | Access |
|-----------|----------|--------|
| Core Donor File | Candidate | Only that candidate's campaign manager |
| Outreach history | Candidate | Only that candidate's team |
| Channel performance metrics | Candidate | Only that candidate + Platform Admin |
| Budget allocation | Candidate | Only that candidate's campaign manager |
| Volunteer assignments | Candidate | Only that candidate's team |

### Metadata Allowed to Flow Upward (Anonymized)

| Metadata | Aggregation | Purpose |
|----------|-------------|---------|
| Aggregate donation volume | By district, by week | Platform-level trend monitoring |
| Channel response rates | By segment (not individual) | Model retraining inputs |
| Donor state transition counts | By state pair (not individual) | State machine calibration |
| Capacity utilization | By channel | Resource constraint updates |

No individually identifiable data flows upward. All upward flows are aggregated to cohort or district level with minimum group size of 50.

## RLS Enforcement

All tenant isolation is enforced at the database level via Supabase Row Level Security:

```sql
-- Example: donor_contacts table
CREATE POLICY tenant_isolation ON donor_contacts
  FOR ALL
  USING (candidate_id = current_setting('app.current_candidate_id')::uuid)
  WITH CHECK (candidate_id = current_setting('app.current_candidate_id')::uuid);
```

Platform Admin and Data Steward roles bypass RLS for model training and system administration only.

```json
{
  "isolation_model": "RLS-enforced tenant scoping",
  "cross_tenant_data": "PROHIBITED",
  "centralized_models": "trained on platform-wide data, outputs scoped to tenant",
  "upward_metadata": "aggregated only, minimum group size 50",
  "audit": "all cross-scope access logged to audit_log"
}
```
