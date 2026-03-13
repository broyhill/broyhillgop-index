Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# Failure Mode Registry

Declares expected failure scenarios, their impact, detection method, and automated/manual recovery procedures.

## Data Ingestion Failures

| Failure | Impact | Detection | Severity | Recovery |
|---------|--------|-----------|----------|----------|
| DataTrust monthly file not received | nc_datatrust stale (7.6M rows not updated) | File watcher timeout > 48 hours past expected date | HIGH | Alert Data Steward. Models continue on stale data. Flag all scores as "stale_input" in audit_log. Manually request redelivery. |
| WinRed API feed delayed > 4 hours | Real-time donation events not captured | API health check returns non-200 or no new records in 4 hours | MEDIUM | Queue missed donations for batch catch-up. donor_scores recency may drift. Alert dashboard. |
| NCSBE voter file format changed | nc_voters import fails, 9M rows not refreshed | Import job error log, row count < 90% of prior import | HIGH | Halt import. Alert Data Steward. Run format diff. No downstream impact until weekly refresh window. |
| FEC bulk download corrupted | fec_donations batch partially loaded | Row count check, checksum validation | MEDIUM | Rollback to last good import. Re-download from FEC bulk data API. |
| Acxiom license expired | acxiom_consumer_data cannot be refreshed | Annual renewal check | LOW (annual) | Capacity scores stale but functional. Alert for renewal. |

## Model Failures

| Failure | Impact | Detection | Severity | Recovery |
|---------|--------|-----------|----------|----------|
| Donation_Propensity_Model training fails | Nightly scores not updated | ML job exit code != 0, no new rows in donor_propensity_scores | HIGH | Auto-rollback to last good model version. Alert Data Steward. Serve prior day's scores. |
| Model drift exceeds threshold | Scores degrading silently | Drift monitoring (AUC < 0.72 for 2 weeks) | MEDIUM | Auto-queue retraining. If immediate threshold hit (AUC < 0.68), auto-rollback. |
| MODEL-REGISTRY corruption | Model metadata lost | JSON parse failure on registry load | CRITICAL | Restore from git (version-controlled). All models fall back to last deployed version. |
| Circular dependency introduced | Retraining infinite loop | DAG validation check before model promotion | CRITICAL | Block promotion. Alert. Require manual dependency graph review. |

## Infrastructure Failures

| Failure | Impact | Detection | Severity | Recovery |
|---------|--------|-----------|----------|----------|
| Supabase connection pool exhausted | All read/write operations blocked | Connection timeout errors > 10/minute | CRITICAL | Kill long-running queries. Scale connection pool. Pause non-essential batch jobs. |
| Edge Function timeout spike | API responses degraded | P95 latency > 30 seconds | HIGH | Identify slow function. Route traffic to cached responses. Scale compute. |
| Nightly batch overruns 4-hour window | Scores not ready for business day | Job still running at 06:00 UTC | MEDIUM | Serve prior day's scores. Investigate bottleneck. Extend window or optimize pipeline. |
| GOD FILE rebuild fails | Document index stale | Build script exit code != 0 | LOW | Serve prior version. Rebuild manually. |

## Optimization Failures

| Failure | Impact | Detection | Severity | Recovery |
|---------|--------|-----------|----------|----------|
| LP solver infeasible | No budget allocation produced | Solver returns INFEASIBLE status | HIGH | Relax lowest-priority constraints (print capacity, then staff time). Alert. Serve prior allocation with 24-hour expiry. |
| LP solver unbounded | Invalid allocation (infinite spend) | Solver returns UNBOUNDED or allocation > 10× budget | CRITICAL | Halt. Serve prior allocation. Audit constraint matrix. Require human review before re-solve. |
| Revenue forecast job crashes | No updated forecast | Job exit code != 0 | MEDIUM | Serve prior forecast with staleness flag. Investigate and re-run. |
| Authority Index not updated before LP run | LP uses stale authority weights | Dependency check: authority_scores.updated_at < LP run start | MEDIUM | LP proceeds with stale weights + flag. Alert Data Steward. |

## Cascade Failure Scenarios

### Scenario: DataTrust + WinRed both fail simultaneously
Impact: Identity resolution degraded + real-time donations lost
Detection: Both alerts fire within same monitoring window
Response: CRITICAL escalation. Freeze all trigger sequences. Serve last-known-good scores. Manual intervention required.

### Scenario: Model drift + infrastructure degradation
Impact: Bad scores served slowly
Detection: Drift alert + latency alert in same window
Response: Auto-rollback model. Pause batch jobs. Investigate infrastructure first (root cause likely there).

```json
{
  "failure_registry_version": "1.0",
  "total_failure_modes": 17,
  "severity_levels": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
  "auto_recovery_enabled": true,
  "escalation_path": "automated alert → Data Steward → Platform Admin",
  "fallback_policy": "always serve last-known-good, never serve nothing"
}
```
