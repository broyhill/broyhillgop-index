# ML MODEL DESIGN (E21)

## Overview

The Machine Learning layer (Ecosystem 21) provides predictive intelligence across the platform. All models are trained on the 59M-row Supabase database and deployed as scoring functions.

## Active Model Inventory

### 1. Donor Propensity Model
- **Type:** Gradient boosted classifier
- **Target:** P(donation in next 90 days)
- **Features:** 47 features from nc_datatrust, acxiom_consumer_data, prior giving history
- **Training set:** 226K labeled donors from fec_god_contributions (127 cols)

### 2. Donor Clustering
- **Type:** K-means + hierarchical clustering
- **Purpose:** Segment donors into behavioral archetypes for targeted messaging
- **Input:** RFM features + Policy Domain Vector + channel affinity
- **Clusters:** 12 segments (e.g., "High-value issue donors", "Event-driven social givers", "Digital-first small-dollar recurring")

### 3. Lookalike Audience Builder
- **Type:** Nearest-neighbor in embedding space
- **Purpose:** Given a seed list of donors, find non-donors who look like them
- **Universe:** 7.6M person_master records
- **Output:** Ranked prospect list with similarity scores

### 4. Lapse Prediction
- **Type:** Survival analysis / Cox regression
- **Target:** P(no gift in next 18 months)
- **Features:** Days since last gift, gift frequency trend, engagement decline signals
- **Action:** High lapse-risk donors routed to retention trigger sequences

### 5. Escalation Predictor
- **Type:** Ordinal regression
- **Target:** Next giving tier ($25→$100→$500→$1000→$2800)
- **Features:** Giving trajectory, capacity indicators, ask-amount response history

## Data Pipeline
```
nc_datatrust (7.6M) → feature engineering → person_master join → model training
fec_god_contributions (226K) → labeled outcomes → validation holdout
acxiom_consumer_data (7.6M) → capacity features → model enrichment
```
