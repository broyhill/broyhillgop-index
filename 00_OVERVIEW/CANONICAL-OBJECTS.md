Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# Canonical Objects

## Donor_State
Type: Persistent Entity
Location: donor_scores, donor_profiles, donor_state_transitions
Primary Key: person_id (uuid)
Dimensions:
- capacity_score (numeric, 0-100)
- activism_index (numeric, 0-100)
- repeat_velocity_score (numeric, gifts/year)
- escalation_rate (numeric, $/year growth)
- churn_risk_score (numeric, 0-1 probability)
- behavioral_intensity_index (numeric, 0-100)
- office_affinity_vector (numeric[], 10 dimensions)
- authority_alignment_score (numeric, 0-100)

State Transitions:
Prospect → Engaged → First_Gift → Repeat_Donor → Escalating_Donor → High_Value_Core
Transitions triggered by: Donation_Event | Escalation_Threshold | Inactivity_Period | Volatility_Event

## Campaign_Context
Type: Dynamic (changes with election cycle)
Location: candidates, campaign_finance_summary, intelligence_brain
Primary Key: candidate_id (uuid) + election_cycle (text)
Dimensions:
- authority_index (numeric, 0-100)
- volatility_score (numeric, 0-100)
- budget_gap (numeric, dollars remaining vs target)
- days_remaining (integer, days to election)
- district_personality_vector (numeric[], 14 dimensions)
- office_level (enum: federal|state_senate|state_house|county|municipal|school_board)

## District_Personality
Type: Aggregated Behavioral Model
Location: intelligence_brain, district_personality_scores
Primary Key: district_id (text) + district_level (enum)
Dimensions:
- urbanicity_score (numeric, 0-100)
- affluence_score (numeric, 0-100)
- education_score (numeric, 0-100)
- religious_intensity_score (numeric, 0-100)
- gun_culture_score (numeric, 0-100)
- fiscal_conservatism_score (numeric, 0-100)
- activism_density_score (numeric, 0-100)
- donor_density (numeric, donors per 1,000 registered voters)
- avg_gift_size (numeric, mean donation dollars)
- turnout_elasticity (numeric, presidential vs off-year delta)
- digital_responsiveness (numeric, 0-100)
- issue_sensitivity_vector (numeric[], 10 dimensions)
- partisan_lean (numeric, R vote share trailing 3 cycles)
- volatility_score (numeric, 0-100)

Clustering:
- Method: K-Means (k=10)
- Inputs: All 14 dimensions above
- Update Frequency: Quarterly + Event-Triggered
- Output: district_cluster_id (integer, 1-10), dominant_issue_vector, channel_weight_vector

## Authority_Index
Type: Computed Score
Location: authority_scores, endorsement_tracking
Primary Key: candidate_id (uuid)
Dimensions:
- endorsement_quality (numeric, 0-100, weight: 0.30)
- fundraising_network_depth (numeric, 0-100, weight: 0.25)
- party_support_level (numeric, 0-100, weight: 0.20)
- incumbent_advantage (numeric, 0-100, weight: 0.15)
- media_authority (numeric, 0-100, weight: 0.10)
Formula: authority_index = Σ(dimension × weight)

## Volatility_Index
Type: Computed Score
Location: volatility_scores, swing_analysis
Primary Key: entity_id (uuid) + entity_type (enum: district|donor|race)
Dimensions:
- margin_swing (numeric, absolute change between last 2 cycles)
- party_switch_rate (numeric, trailing 12-month rate)
- unaffiliated_share_trend (numeric, slope)
- gift_amount_variance (numeric, σ of last 5 gifts) [donor only]
- cross_party_giving (boolean) [donor only]
Formula: opportunity_score = volatility × (1 - authority/100)

## Policy_Domain_Vector
Type: Feature Vector
Location: Computed, stored per entity in scoring tables
Primary Key: entity_id (uuid) + entity_type (enum: person|district|candidate)
Dimensions (10):
- FISCAL (numeric, 0-1)
- IMMIG (numeric, 0-1)
- EDU (numeric, 0-1)
- 2A (numeric, 0-1)
- LIFE (numeric, 0-1)
- ENERGY (numeric, 0-1)
- LAW (numeric, 0-1)
- HEALTH (numeric, 0-1)
- AG (numeric, 0-1)
- MIL (numeric, 0-1)
Similarity: Cosine similarity for donor-candidate and donor-district matching

## Person_Master
Type: Golden Record (Identity Spine)
Location: person_master
Rows: 7,656,550
Primary Key: person_id (uuid)
Key Columns:
- best_voter_id (text)
- best_datatrust_id (text)
- best_name (text)
- best_address (text)
- best_phone (text)
- best_email (text)
- is_donor (boolean)
- is_volunteer (boolean)
- is_voter (boolean)
- composite_score (numeric)
Resolution: Deterministic (voter_id, email, phone hash) + Probabilistic (name+address fuzzy)
Source Links: person_source_links (1,850,683 rows)
