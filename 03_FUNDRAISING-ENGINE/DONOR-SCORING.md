Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# Donor Scoring

## Objective

Score every person in the system (0-100) on likelihood and capacity to donate to Republican candidates in North Carolina.

## INPUT TABLES
- donor_scores (36 cols)
- donor_faction_scores
- nc_datatrust (7,654,883 rows × 251 cols)
- acxiom_consumer_data (7,655,559 rows × 152 cols)
- donor_contribution_map (2,523,766 rows)
- candidates (2,303 rows × 242 cols)

## OUTPUT TABLES
- donor_propensity_scores
- donor_score_history

## UPDATE FREQUENCY
- Nightly batch

## DEPENDENCIES
- Authority_Index
- District_Personality
- Policy_Domain_Vector

## Formula

```
composite_donor_score =
    (0.40 × propensity_score)
  + (0.30 × capacity_score)
  + (0.20 × affinity_score)
  + (0.10 × accessibility_score)
```

Where:
- propensity_score: P(donation in next 90 days) from Donation_Propensity_Model
- capacity_score: Estimated giving capacity from income, home value, occupation (acxiom_consumer_data)
- affinity_score: Cosine similarity of person's Policy_Domain_Vector to target candidate
- accessibility_score: Reachability (has email × has phone × has address × not suppressed)

### donor_scores

Rows: 0 (populated dynamically)
Cols: 36

Key Columns:
- person_id (uuid)
- composite_score (numeric, 0-100)
- capacity_score (numeric, 0-100)
- activism_index (numeric, 0-100)
- repeat_velocity_score (numeric)
- escalation_rate (numeric)
- churn_risk_score (numeric, 0-1)
- behavioral_intensity_index (numeric, 0-100)
- office_affinity_vector (numeric[])
- authority_alignment_score (numeric, 0-100)

Primary Key: person_id
Indexes: composite_score DESC, churn_risk_score DESC

```json
{
  "model_name": "Composite_Donor_Score",
  "input_features": ["propensity_score", "capacity_score", "affinity_score", "accessibility_score"],
  "output": "composite_donor_score (0-100)",
  "formula": "0.40×propensity + 0.30×capacity + 0.20×affinity + 0.10×accessibility",
  "update_frequency": "nightly",
  "dependencies": ["Donation_Propensity_Model", "Authority_Index", "District_Personality"]
}
```
