Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# District Personality Model

## INPUT TABLES
- nc_voters (9,049,588 rows × 71 cols)
- nc_datatrust (7,654,883 rows × 251 cols)
- nc_boe_donations_raw (652,532 rows × 61 cols)
- fec_donations (1,132,719 rows × 24 cols)
- Contact response data from E30 (Email), E31 (SMS), E32 (Phone Banking)

## OUTPUT TABLES
- district_personality_scores

## UPDATE FREQUENCY
- Quarterly + Event-Triggered

## DEPENDENCIES
- Volatility_Index
- Policy_Domain_Vector

## District Levels

| Level | Count | Source Field |
|-------|-------|-------------|
| Congressional | 13 | nc_voters.congressional_dist |
| State Senate | 50 | nc_voters.nc_senate_dist |
| State House | 120 | nc_voters.nc_house_dist |
| County | 100 | nc_voters.county_id |
| Municipality | 550+ | nc_voters.municipality |
| Precinct | ~2,700 | nc_voters.precinct |
| School Board | 115 | Legislative feed mapping |

## Dimensions (14)

| Dimension | Type | Source |
|-----------|------|--------|
| urbanicity_score | numeric, 0-100 | Census + nc_voters address density |
| affluence_score | numeric, 0-100 | acxiom_consumer_data income/home value aggregate |
| education_score | numeric, 0-100 | acxiom_consumer_data education level aggregate |
| religious_intensity_score | numeric, 0-100 | Church density + issue affinity signals |
| gun_culture_score | numeric, 0-100 | 2A PAC donations + NRA membership proxy |
| fiscal_conservatism_score | numeric, 0-100 | Tax/spending issue donation patterns |
| activism_density_score | numeric, 0-100 | Volunteer + event attendance per capita |
| donor_density | numeric | Donors per 1,000 registered voters |
| avg_gift_size | numeric | Mean donation amount from district residents |
| turnout_elasticity | numeric | Presidential vs off-year turnout delta |
| digital_responsiveness | numeric, 0-100 | Email open + SMS response + social engagement rates |
| issue_sensitivity_vector | numeric[10] | Policy_Domain_Vector aggregated to district |
| partisan_lean | numeric | R vote share trailing 3 election cycles |
| volatility_score | numeric, 0-100 | From Volatility_Index at district level |

## District_Cluster_ID

Clustering Method:
- Algorithm: K-Means (k=10)
- Inputs: All 14 dimensions above
- Update Frequency: Quarterly + Event-Triggered
- Initialization: K-Means++ with 10 random restarts

Output:
- district_cluster_id (integer, 1-10)
- dominant_issue_vector (numeric[10], cluster centroid of Policy_Domain_Vector)
- channel_weight_vector (numeric[9], optimal channel mix for cluster)

## Cluster Stability Rule

Cluster assignments are frozen during the critical campaign window to prevent optimization destabilization.

| Phase | Window | Cluster Behavior |
|-------|--------|-----------------|
| Normal Operations | > 90 days before election | Full reclustering quarterly + event-triggered |
| Pre-Election Freeze | 90-0 days before election | Cluster IDs frozen. No reassignment. |
| Override Exception | During freeze | Intelligence Brain can trigger emergency recluster ONLY if Volatility_Index > 85 for a district AND Data Committee Steward approves |
| Post-Election Reset | After election day | Full recluster with updated election results incorporated |

Rationale: If a district's cluster_id changes 60 days before election, all downstream systems (LP allocation, channel weighting, trigger sequences, candidate Core Donor Files) would need recalibration. The freeze protects candidates from mid-cycle optimization instability.

```json
{
  "stability_rule": "cluster_freeze",
  "freeze_window_days": 90,
  "override_authority": "Intelligence Brain + Data Committee Steward",
  "override_condition": "Volatility_Index > 85 for affected district",
  "post_election_action": "full recluster with election results"
}
```

```json
{
  "model_name": "District_Personality_Model",
  "type": "K-Means Clustering (k=10)",
  "input_dimensions": 14,
  "output_fields": ["district_cluster_id", "dominant_issue_vector", "channel_weight_vector"],
  "geographic_levels": 7,
  "total_districts": "~3,548",
  "update_frequency": "quarterly + event-triggered",
  "dependencies": ["Volatility_Index", "Policy_Domain_Vector"]
}
```
