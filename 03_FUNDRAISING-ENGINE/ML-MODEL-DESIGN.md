Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# ML Model Design (E21)

## Overview

The Machine Learning layer provides predictive intelligence across the platform. All models train on the 59M-row Supabase database and deploy as scoring functions.

See [MODEL-REGISTRY.md](../01_DATA-COMMITTEE/MODEL-REGISTRY.md) for complete JSON specifications of all models.

## Model Inventory

### 1. Donation Propensity Model

## INPUT TABLES
- donor_scores
- donor_faction_scores
- nc_datatrust
- donor_contribution_map
- candidates

## OUTPUT TABLES
- donor_propensity_scores
- donor_score_history

## UPDATE FREQUENCY
- Nightly batch

## DEPENDENCIES
- Authority_Index
- District_Personality

Type: Gradient Boosted Classifier
Target: P(donation in next 90 days)
Training: 226,451 labeled donors from fec_god_contributions (127 cols)
Features: 47 features across voter, consumer, and giving history dimensions

### 2. Donor Clustering

## INPUT TABLES
- donor_scores
- donor_profiles
- donor_contribution_map

## OUTPUT TABLES
- donor_clusters

## UPDATE FREQUENCY
- Weekly batch

## DEPENDENCIES
- Donor_State
- Policy_Domain_Vector

Type: K-Means + Hierarchical
Segments: 12 behavioral archetypes
Purpose: Segment donors for targeted messaging and channel optimization

### 3. Lookalike Audience Builder

## INPUT TABLES
- person_master (7,656,550 rows)
- nc_datatrust
- acxiom_consumer_data

## OUTPUT TABLES
- lookalike_prospects

## UPDATE FREQUENCY
- On-demand per campaign

## DEPENDENCIES
- Person_Master
- Donor_Clustering_Model

Type: K-Nearest Neighbors in embedding space
Purpose: Given seed donors, find non-donors who resemble them
Universe: 7.6M person_master records

### 4. Lapse Prediction

## INPUT TABLES
- donor_profiles
- donor_contribution_map
- donor_contacts

## OUTPUT TABLES
- donor_lapse_scores

## UPDATE FREQUENCY
- Nightly batch

## DEPENDENCIES
- Donor_State

Type: Cox Proportional Hazards / Survival Analysis
Target: P(no gift in next 18 months)
Action: High lapse-risk donors routed to retention trigger sequences via E40

### 5. Escalation Predictor

## INPUT TABLES
- donor_profiles
- donor_contribution_map
- donor_scores

## OUTPUT TABLES
- donor_escalation_scores

## UPDATE FREQUENCY
- Nightly batch

## DEPENDENCIES
- Donor_State
- Donation_Propensity_Model

Type: Ordinal Regression
Target: Next giving tier ($25 → $100 → $500 → $1,000 → $2,800)
Features: Giving trajectory, capacity indicators, ask-amount response history

## Data Pipeline
```
nc_datatrust (7.6M) → feature engineering → person_master join → model training
fec_god_contributions (226K) → labeled outcomes → validation holdout
acxiom_consumer_data (7.6M) → capacity features → model enrichment
```
