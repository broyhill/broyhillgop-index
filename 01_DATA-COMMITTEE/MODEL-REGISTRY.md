Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# Model Registry

## Donation_Propensity_Model

```json
{
  "model_name": "Donation_Propensity_Model",
  "type": "Gradient Boosted Classifier",
  "target": "P(donation in next 90 days)",
  "input_tables": ["donor_scores", "nc_datatrust", "acxiom_consumer_data", "donor_contribution_map"],
  "input_features": [
    "capacity_score",
    "activism_index",
    "behavioral_intensity_index",
    "authority_alignment_score",
    "district_personality_vector",
    "repeat_velocity_score",
    "days_since_last_gift",
    "gift_count_trailing_12m",
    "partisan_score",
    "turnout_propensity"
  ],
  "output_table": "donor_propensity_scores",
  "output_field": "probability_of_donation",
  "training_set": "fec_god_contributions (226,451 rows × 127 cols)",
  "update_frequency": "nightly batch",
  "dependencies": ["Authority_Index", "District_Personality"]
}
```

## Donor_Clustering_Model

```json
{
  "model_name": "Donor_Clustering_Model",
  "type": "K-Means + Hierarchical",
  "target": "Segment assignment (12 archetypes)",
  "input_tables": ["donor_scores", "donor_profiles", "donor_contribution_map"],
  "input_features": [
    "recency",
    "frequency",
    "monetary",
    "channel_affinity_vector",
    "policy_domain_vector",
    "escalation_rate",
    "churn_risk_score"
  ],
  "output_table": "donor_clusters",
  "output_field": "cluster_id (integer, 1-12)",
  "training_set": "All donors with 2+ transactions (~120K)",
  "update_frequency": "weekly batch",
  "dependencies": ["Donor_State", "Policy_Domain_Vector"]
}
```

## Lookalike_Audience_Model

```json
{
  "model_name": "Lookalike_Audience_Model",
  "type": "K-Nearest Neighbors in embedding space",
  "target": "Similarity score to seed donor list",
  "input_tables": ["person_master", "nc_datatrust", "acxiom_consumer_data"],
  "input_features": [
    "demographics_vector",
    "geographic_features",
    "consumer_data_overlay",
    "partisan_score",
    "turnout_propensity"
  ],
  "output_table": "lookalike_prospects",
  "output_field": "similarity_score (numeric, 0-1)",
  "universe": "person_master (7,656,550 rows)",
  "update_frequency": "on-demand per campaign",
  "dependencies": ["Person_Master", "Donor_Clustering_Model"]
}
```

## Lapse_Prediction_Model

```json
{
  "model_name": "Lapse_Prediction_Model",
  "type": "Cox Proportional Hazards / Survival Analysis",
  "target": "P(no gift in next 18 months)",
  "input_tables": ["donor_profiles", "donor_contribution_map", "donor_contacts"],
  "input_features": [
    "days_since_last_gift",
    "gift_frequency_trend",
    "engagement_decline_slope",
    "email_open_rate_trailing_30d",
    "sms_response_rate",
    "event_attendance_count"
  ],
  "output_table": "donor_lapse_scores",
  "output_field": "lapse_probability (numeric, 0-1)",
  "training_set": "Historical lapsed donors (18+ month gap) vs active",
  "update_frequency": "nightly batch",
  "dependencies": ["Donor_State"]
}
```

## Escalation_Predictor_Model

```json
{
  "model_name": "Escalation_Predictor_Model",
  "type": "Ordinal Regression",
  "target": "Next giving tier ($25 → $100 → $500 → $1,000 → $2,800)",
  "input_tables": ["donor_profiles", "donor_contribution_map", "donor_scores"],
  "input_features": [
    "current_max_gift",
    "gift_trajectory_slope",
    "capacity_score",
    "ask_amount_response_history",
    "escalation_rate",
    "channel_of_last_gift"
  ],
  "output_table": "donor_escalation_scores",
  "output_field": "predicted_next_tier (ordinal)",
  "training_set": "Donors with 3+ gifts showing tier movement",
  "update_frequency": "nightly batch",
  "dependencies": ["Donor_State", "Donation_Propensity_Model"]
}
```

## District_Personality_Model

```json
{
  "model_name": "District_Personality_Model",
  "type": "K-Means Clustering (k=10) on aggregated behavioral signals",
  "target": "District behavioral archetype assignment",
  "input_tables": ["nc_voters", "nc_datatrust", "nc_boe_donations_raw", "fec_donations"],
  "input_features": [
    "urbanicity_score",
    "affluence_score",
    "education_score",
    "religious_intensity_score",
    "gun_culture_score",
    "fiscal_conservatism_score",
    "activism_density_score",
    "donor_density",
    "avg_gift_size",
    "turnout_elasticity",
    "digital_responsiveness",
    "issue_sensitivity_vector",
    "partisan_lean",
    "volatility_score"
  ],
  "output_table": "district_personality_scores",
  "output_fields": ["district_cluster_id", "dominant_issue_vector", "channel_weight_vector"],
  "update_frequency": "quarterly + event-triggered",
  "dependencies": ["Volatility_Index"]
}
```

## Model Drift Monitoring

All production models are subject to automated drift detection. When performance degrades beyond threshold, the system triggers alerts and can auto-rollback to the last known-good version.

### Monitoring Protocol

| Model | Metric | Baseline | Drift Threshold | Rollback Trigger |
|-------|--------|----------|----------------|-----------------|
| Donation_Propensity_Model | AUC-ROC | 0.78 | < 0.72 (2 consecutive weeks) | < 0.68 (immediate) |
| Donor_Clustering_Model | Silhouette Score | 0.45 | < 0.35 (1 month) | < 0.25 (immediate) |
| Lookalike_Audience_Model | Precision@1000 | 0.15 | < 0.10 (2 weeks) | < 0.07 (immediate) |
| Lapse_Prediction_Model | Calibration Error | 0.05 | > 0.10 (2 weeks) | > 0.15 (immediate) |
| Escalation_Predictor_Model | Ordinal Accuracy | 0.62 | < 0.52 (2 weeks) | < 0.45 (immediate) |
| District_Personality_Model | Intra-cluster Variance | baseline | > 1.5× baseline (quarterly) | > 2× baseline (immediate) |

### Drift Detection Method

```json
{
  "monitoring_frequency": "daily",
  "evaluation_window": "trailing 14 days of predictions vs outcomes",
  "comparison": "current_metric vs baseline_metric",
  "alert_channels": ["dashboard_notification", "email_to_data_steward"],
  "auto_rollback": {
    "enabled": true,
    "rollback_to": "last model version where metric >= baseline",
    "requires_human_approval": false,
    "logged_to": "audit_log"
  },
  "retraining_trigger": {
    "condition": "drift_threshold breached for 2 consecutive evaluation windows",
    "action": "queue automatic retrain with latest data",
    "validation": "holdout set performance must exceed baseline before promotion"
  }
}
```

### Version Control

Every model version is stored with:
- model_id (uuid)
- model_name (text)
- version (semver, e.g., "1.3.2")
- trained_at (timestamp)
- training_data_cutoff (date)
- baseline_metric (numeric)
- current_metric (numeric)
- status (enum: active | staged | rolled_back | retired)
- artifact_path (text, path to serialized model)
