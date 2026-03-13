Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# Model Compatibility Matrix

Declares which models depend on which, preventing circular references and enabling safe retraining order.

## Dependency Graph

```
Level 0 (Raw Data — no model dependencies):
  nc_voters, nc_datatrust, fec_donations, nc_boe_donations_raw,
  rnc_voter_core, acxiom_consumer_data, winred_donors

Level 1 (Identity + Base Scoring):
  Identity_Resolution → person_master
  RFM_Scoring → donor_scores (rfm_* fields)
  Faction_Classification → donor_faction_scores

Level 2 (Computed Indexes):
  Volatility_Index ← nc_voters, fec_donations, nc_boe_donations_raw
  Authority_Index ← candidates, fec_party_committee_donations, endorsement_tracking

Level 3 (Behavioral Models):
  District_Personality_Model ← nc_voters, nc_datatrust, Volatility_Index
  Donor_Clustering_Model ← donor_scores, donor_profiles, Policy_Domain_Vector

Level 4 (Predictive Models):
  Donation_Propensity_Model ← donor_scores, nc_datatrust, Authority_Index, District_Personality
  Lapse_Prediction_Model ← donor_profiles, donor_contribution_map
  Escalation_Predictor_Model ← donor_profiles, donor_scores, Donation_Propensity_Model

Level 5 (Optimization):
  LP_Allocation_Engine ← Donation_Propensity_Model, Authority_Index, District_Personality, Volatility_Index
  Revenue_Forecast ← Donation_Propensity_Model, Escalation_Predictor_Model, Donor_Clustering_Model

Level 6 (Execution):
  Trigger_Funnel (E40) ← LP_Allocation_Engine, Lapse_Prediction_Model, Surge_Detection
  Channel_Weighting ← District_Personality_Model, donor engagement history
```

## Safe Retraining Order

Models MUST be retrained in level order (0 → 6). A model at level N can only be retrained after all level N-1 dependencies have been refreshed.

| Retrain Step | Models | Prerequisite |
|-------------|--------|-------------|
| 1 | Identity_Resolution, RFM_Scoring, Faction_Classification | Raw data ingestion complete |
| 2 | Volatility_Index, Authority_Index | Step 1 complete |
| 3 | District_Personality_Model, Donor_Clustering_Model | Step 2 complete |
| 4 | Donation_Propensity, Lapse_Prediction, Escalation_Predictor | Step 3 complete |
| 5 | LP_Allocation_Engine, Revenue_Forecast | Step 4 complete |
| 6 | Trigger_Funnel, Channel_Weighting | Step 5 complete |

## Circular Reference Check

No circular dependencies exist. The graph is a strict DAG (Directed Acyclic Graph).

Validation: For any model M, trace all dependencies — no path returns to M.

```json
{
  "graph_type": "DAG (Directed Acyclic Graph)",
  "levels": 7,
  "total_models": 12,
  "circular_references": "NONE",
  "retraining_policy": "strict level-order, no skip",
  "validation": "automated DAG check before any model promotion"
}
```
