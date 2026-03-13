# ACTIVATION PIPELINE

## Overview

When a new Republican candidate enters a race in North Carolina, the Activation Pipeline provisions their personalized data and tools from the shared platform in a structured sequence.

## Pipeline Stages

### Stage 1: Candidate Registration
- Create record in `candidates` table (242 columns)
- Assign district, office level, election cycle
- Link to party committee hierarchy

### Stage 2: District Intelligence Package
- Pull District Personality Model for their specific district
- Generate voter universe: all registered voters in the district from nc_voters
- Cross-reference with nc_datatrust for modeled scores
- Produce initial supporter/persuadable/opponent segmentation

### Stage 3: Core Donor File Generation
- Query donor_profiles for donors with geographic or issue affinity to the candidate
- Score all donors using the Donor Scoring model with candidate-specific features
- Rank and segment: Tier 1 (ask immediately), Tier 2 (cultivate), Tier 3 (long-term prospect)
- Match against FEC/NCBOE history to identify prior givers to similar candidates

### Stage 4: Channel Activation
- Load candidate into E30 Email, E31 SMS, E32 Phone Banking, E33 Direct Mail systems
- Generate initial outreach templates from E09 Content Creation AI
- Set up compliance tracking for FEC/NCBOE contribution limits
- Configure trigger sequences in E40 Automation Control

### Stage 5: Dashboard Provisioning
- Create candidate-specific dashboard view in Inspinia Admin
- Real-time donation tracker, donor pipeline visualization, outreach metrics
- Volunteer roster and event calendar
- Budget vs. actual spending tracker

## Data Flow
```
candidates (242 cols) → District Personality → Donor Scoring → Core Donor File
                      → Channel Setup → Trigger Config → Dashboard
```
