Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# Feature Lineage Registry

Every computed feature in the platform traces back to raw source columns. This registry declares the provenance chain for each derived feature used in scoring, modeling, and optimization.

## donor_scores Features

```json
{
  "feature": "composite_score",
  "output_table": "donor_scores",
  "output_type": "numeric (0-100)",
  "derived_from": [
    "donor_scores.intensity_score",
    "donor_scores.frequency_score",
    "donor_scores.recency_score",
    "donor_scores.consistency_score",
    "donor_scores.growth_score"
  ],
  "raw_sources": [
    "fec_donations.contribution_receipt_amount",
    "fec_donations.contribution_receipt_date",
    "nc_boe_donations_raw.amount",
    "nc_boe_donations_raw.date_occured",
    "winred_donors.total_donated"
  ],
  "calculation_location": "E01 Data Import → donor scoring pipeline",
  "formula": "weighted combination of intensity, frequency, recency, consistency, growth",
  "update_frequency": "nightly batch"
}
```

```json
{
  "feature": "intensity_score",
  "output_table": "donor_scores",
  "output_type": "integer (0-100)",
  "derived_from": [
    "donor_contribution_map.contribution_receipt_amount",
    "donor_contribution_map.contribution_receipt_date"
  ],
  "raw_sources": [
    "fec_donations.contribution_receipt_amount",
    "nc_boe_donations_raw.amount",
    "winred_donors.total_donated"
  ],
  "calculation_location": "E01 Data Import",
  "formula": "normalized score of total giving volume relative to cohort",
  "update_frequency": "nightly batch"
}
```

```json
{
  "feature": "frequency_score",
  "output_table": "donor_scores",
  "output_type": "numeric (0-100)",
  "derived_from": [
    "donor_contribution_map.contribution_receipt_date (count distinct)"
  ],
  "raw_sources": [
    "fec_donations.contribution_receipt_date",
    "nc_boe_donations_raw.date_occured"
  ],
  "calculation_location": "E01 Data Import",
  "formula": "count of distinct donation events in trailing 24 months, normalized to 0-100",
  "update_frequency": "nightly batch"
}
```

```json
{
  "feature": "recency_score",
  "output_table": "donor_scores",
  "output_type": "numeric (0-100)",
  "derived_from": [
    "donor_profiles.last_donation_date",
    "CURRENT_DATE"
  ],
  "raw_sources": [
    "fec_donations.contribution_receipt_date (MAX)",
    "nc_boe_donations_raw.date_occured (MAX)",
    "winred_donors.last_donation_date"
  ],
  "calculation_location": "E01 Data Import",
  "formula": "100 × exp(-λ × days_since_last_gift), λ calibrated so score=50 at 180 days",
  "update_frequency": "nightly batch"
}
```

```json
{
  "feature": "growth_score",
  "output_table": "donor_scores",
  "output_type": "numeric (0-100)",
  "derived_from": [
    "donor_contribution_map.contribution_receipt_amount (time series)"
  ],
  "raw_sources": [
    "fec_donations.contribution_receipt_amount + contribution_receipt_date",
    "nc_boe_donations_raw.amount + date_occured"
  ],
  "calculation_location": "E01 Data Import",
  "formula": "slope of gift amounts over time, normalized (positive slope = high growth)",
  "update_frequency": "nightly batch"
}
```

```json
{
  "feature": "predicted_churn_risk",
  "output_table": "donor_scores",
  "output_type": "numeric (0-1 probability)",
  "derived_from": [
    "donor_scores.recency_score",
    "donor_scores.frequency_score",
    "donor_scores.consistency_score",
    "donor_profiles.email_engagement_score",
    "donor_profiles.sms_engagement_score"
  ],
  "raw_sources": [
    "fec_donations.contribution_receipt_date",
    "donor_contacts.last_response_date",
    "E30 email open/click events",
    "E31 SMS delivery/response events"
  ],
  "calculation_location": "Lapse_Prediction_Model (E21 ML Layer)",
  "formula": "Cox proportional hazards: P(no gift in 18 months)",
  "update_frequency": "nightly batch",
  "model_dependency": "Lapse_Prediction_Model"
}
```

```json
{
  "feature": "predicted_lifetime_value",
  "output_table": "donor_scores",
  "output_type": "numeric (dollars)",
  "derived_from": [
    "donor_scores.composite_score",
    "donor_scores.growth_score",
    "donor_scores.predicted_churn_risk",
    "donor_profiles.total_donations",
    "donor_profiles.donation_count"
  ],
  "raw_sources": [
    "All donation source tables (fec, ncboe, winred)",
    "acxiom_consumer_data.estimated_income (capacity proxy)"
  ],
  "calculation_location": "E21 ML Layer",
  "formula": "expected_annual_value / (1 - retention_rate) adjusted for escalation trajectory",
  "update_frequency": "nightly batch",
  "model_dependency": "Escalation_Predictor_Model"
}
```

```json
{
  "feature": "optimal_ask_amount",
  "output_table": "donor_scores",
  "output_type": "numeric (dollars)",
  "derived_from": [
    "donor_scores.predicted_next_amount",
    "donor_scores.amount_percentile",
    "donor_profiles.max_donation",
    "donor_profiles.average_donation"
  ],
  "raw_sources": [
    "fec_donations.contribution_receipt_amount (history)",
    "nc_boe_donations_raw.amount (history)",
    "acxiom_consumer_data.home_value (capacity)"
  ],
  "calculation_location": "E21 ML Layer → Escalation_Predictor_Model",
  "formula": "predicted_next_tier × capacity_adjustment × fatigue_discount",
  "update_frequency": "nightly batch",
  "model_dependency": "Escalation_Predictor_Model"
}
```

## donor_faction_scores Features

```json
{
  "feature": "maga_score",
  "output_table": "donor_faction_scores",
  "output_type": "numeric (0-100)",
  "derived_from": [
    "donor_contribution_map.committee_id (filtered to MAGA-aligned PACs)",
    "nc_datatrust.coalitionid_socialconservative",
    "nc_datatrust.coalitionid_gunowner"
  ],
  "raw_sources": [
    "fec_donations.committee_id + contribution_receipt_amount",
    "nc_datatrust modeled coalition scores"
  ],
  "calculation_location": "E01 Data Import → faction classification",
  "formula": "weighted sum of MAGA-aligned committee donations + DataTrust coalition scores",
  "update_frequency": "nightly batch"
}
```

```json
{
  "feature": "fisc_score",
  "output_table": "donor_faction_scores",
  "output_type": "numeric (0-100)",
  "derived_from": [
    "donor_contribution_map.committee_id (filtered to fiscal/tax PACs)",
    "nc_datatrust.coalitionid_fiscalconservative",
    "fec_god_contributions.employer_industry_code"
  ],
  "raw_sources": [
    "fec_donations.committee_id + amount (fiscal-focused committees)",
    "fec_donations.contributor_employer + contributor_occupation",
    "nc_datatrust fiscal modeling scores"
  ],
  "calculation_location": "E01 Data Import → faction classification",
  "formula": "weighted sum of fiscal PAC donations + employer industry alignment + DataTrust fiscal score",
  "update_frequency": "nightly batch"
}
```

```json
{
  "feature": "evan_score",
  "output_table": "donor_faction_scores",
  "output_type": "numeric (0-100)",
  "derived_from": [
    "donor_contribution_map.committee_id (filtered to evangelical/faith PACs)",
    "nc_datatrust.coalitionid_religiousright",
    "nc_datatrust.churchattendance_model"
  ],
  "raw_sources": [
    "fec_donations.committee_id (faith-org committees)",
    "nc_datatrust religious modeling scores"
  ],
  "calculation_location": "E01 Data Import → faction classification",
  "formula": "weighted sum of faith PAC donations + DataTrust religious coalition + church attendance model",
  "update_frequency": "nightly batch"
}
```

## donor_propensity_scores Features

```json
{
  "feature": "donation_propensity",
  "output_table": "donor_propensity_scores",
  "output_type": "numeric (0-1 probability)",
  "derived_from": [
    "donor_scores.composite_score",
    "donor_scores.recency_score",
    "donor_scores.frequency_score",
    "donor_faction_scores.primary_faction",
    "donor_faction_scores.confidence_score",
    "nc_datatrust.partisan_score",
    "nc_datatrust.turnout_score",
    "person_master.congressional_district",
    "acxiom_consumer_data.estimated_income"
  ],
  "raw_sources": [
    "All donation tables (amount, date, committee)",
    "nc_datatrust (251 cols of voter + modeled data)",
    "acxiom_consumer_data (152 cols of consumer data)",
    "person_master (identity spine)"
  ],
  "calculation_location": "Donation_Propensity_Model (E21 ML Layer)",
  "formula": "Gradient Boosted Classifier: P(donation in next 90 days)",
  "training_set": "fec_god_contributions (226,451 rows × 127 cols)",
  "update_frequency": "nightly batch",
  "model_dependency": "Donation_Propensity_Model"
}
```

```json
{
  "feature": "upgrade_propensity",
  "output_table": "donor_propensity_scores",
  "output_type": "numeric (0-1 probability)",
  "derived_from": [
    "donor_scores.growth_score",
    "donor_scores.amount_percentile",
    "donor_profiles.max_donation",
    "donor_profiles.donation_count",
    "donor_profiles.estimated_capacity"
  ],
  "raw_sources": [
    "fec_donations.contribution_receipt_amount (trajectory)",
    "acxiom_consumer_data.home_value + estimated_income"
  ],
  "calculation_location": "Escalation_Predictor_Model (E21 ML Layer)",
  "formula": "Ordinal Regression: P(next gift in higher tier)",
  "update_frequency": "nightly batch",
  "model_dependency": "Escalation_Predictor_Model"
}
```

## person_master Identity Features

```json
{
  "feature": "republican_party_score",
  "output_table": "person_master",
  "output_type": "text (raw score from DataTrust)",
  "derived_from": [
    "nc_datatrust.partisan_score",
    "nc_voters.party_cd"
  ],
  "raw_sources": [
    "nc_datatrust modeled partisan propensity",
    "nc_voters official party registration"
  ],
  "calculation_location": "Identity resolution pipeline",
  "formula": "Best available: DataTrust modeled score preferred, NCSBE registration as fallback",
  "update_frequency": "On identity resolution (weekly)"
}
```

```json
{
  "feature": "is_donor",
  "output_table": "person_master",
  "output_type": "boolean",
  "derived_from": [
    "donor_contribution_map.golden_record_id (EXISTS check)"
  ],
  "raw_sources": [
    "fec_donations (1.1M rows)",
    "nc_boe_donations_raw (652K rows)",
    "winred_donors (194K rows)"
  ],
  "calculation_location": "Identity resolution pipeline",
  "formula": "TRUE if person_id exists in donor_contribution_map",
  "update_frequency": "On identity resolution (weekly)"
}
```

```json
{
  "feature": "source_count",
  "output_table": "person_master",
  "output_type": "integer",
  "derived_from": [
    "person_source_links (1,850,683 rows) COUNT by golden_record_id"
  ],
  "raw_sources": [
    "nc_voters",
    "nc_datatrust",
    "fec_donations",
    "nc_boe_donations_raw",
    "rnc_voter_core",
    "winred_donors",
    "contact_enrichment"
  ],
  "calculation_location": "Identity resolution pipeline",
  "formula": "COUNT DISTINCT source_system FROM person_source_links WHERE golden_record_id = person_id",
  "update_frequency": "On identity resolution (weekly)"
}
```

## RFM Score Lineage

```json
{
  "feature": "rfm_score",
  "output_table": "donor_scores",
  "output_type": "integer (111-555)",
  "derived_from": [
    "donor_scores.rfm_recency (1-5 quintile)",
    "donor_scores.rfm_frequency (1-5 quintile)",
    "donor_scores.rfm_monetary (1-5 quintile)"
  ],
  "raw_sources": [
    "donor_profiles.last_donation_date (recency)",
    "donor_profiles.donation_count (frequency)",
    "donor_profiles.total_donations (monetary)"
  ],
  "calculation_location": "E01 Data Import → RFM scoring",
  "formula": "Concatenation: rfm_recency × 100 + rfm_frequency × 10 + rfm_monetary",
  "update_frequency": "nightly batch"
}
```

```json
{
  "feature": "rfm_segment",
  "output_table": "donor_scores",
  "output_type": "varchar (segment label)",
  "derived_from": [
    "donor_scores.rfm_score"
  ],
  "raw_sources": [
    "Same as rfm_score"
  ],
  "calculation_location": "E01 Data Import → RFM scoring",
  "formula": "Rule-based mapping: 555=Champion, 5X1=At Risk, 1XX=Hibernating, etc.",
  "update_frequency": "nightly batch"
}
```

## Lifecycle Stage Lineage

```json
{
  "feature": "lifecycle_stage",
  "output_table": "donor_scores",
  "output_type": "varchar (enum: Prospect|Engaged|First_Gift|Repeat_Donor|Escalating_Donor|High_Value_Core|Lapsed|Reactivated)",
  "derived_from": [
    "donor_profiles.donation_count",
    "donor_profiles.max_donation",
    "donor_profiles.total_donations",
    "donor_profiles.last_donation_date",
    "CURRENT_DATE"
  ],
  "raw_sources": [
    "All donation source tables",
    "donor_state_transitions (historical log)"
  ],
  "calculation_location": "Donor State Machine (E01 → E40 Trigger Logic)",
  "formula": "State machine rules defined in DONOR-STATE-MODEL.md",
  "update_frequency": "nightly batch + real-time on Donation_Event trigger"
}
```
