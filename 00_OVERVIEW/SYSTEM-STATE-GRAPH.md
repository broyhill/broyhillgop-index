Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# System State Graph

End-to-end data flow from raw ingestion through optimization to feedback loop.

## Primary Loop

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  RAW DATA INGESTION                                                 │
│  nc_voters (9M) + nc_datatrust (7.6M) + fec_donations (1.1M)      │
│  + nc_boe_donations_raw (652K) + winred_donors (194K)              │
│  + rnc_voter_core (1.1M) + acxiom_consumer_data (7.6M)            │
│                                                                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│  IDENTITY RESOLUTION                                                │
│  Deterministic + Probabilistic matching → person_master (7.6M)      │
│  person_source_links (1.85M cross-references)                       │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│  BASE SCORING                                                       │
│  RFM Scoring → donor_scores                                         │
│  Faction Classification → donor_faction_scores                      │
│  Donor State Machine → lifecycle_stage                              │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│  INTELLIGENCE LAYER                                                 │
│  Authority_Index + Volatility_Index + District_Personality          │
│  + Policy_Domain_Vector                                             │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│  ML PREDICTION LAYER                                                │
│  Donation_Propensity + Lapse_Prediction + Escalation_Predictor     │
│  + Donor_Clustering + Lookalike_Audience                            │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│  OPTIMIZATION LAYER                                                 │
│  LP_Allocation_Engine (budget × channel × candidate × time)        │
│  Subject to: compliance + fatigue + resource constraints            │
│  Revenue_Forecast (P10/P50/P90 by candidate × channel × tier)     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│  EXECUTION LAYER                                                    │
│  Trigger_Funnel (E40) → Channel routing:                            │
│    E30 Email │ E31 SMS │ E32 Phone │ E33 Mail │ E34 Events         │
│  Model Precedence Order enforced (Compliance → Fatigue → LP → Msg) │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│  FEEDBACK LOOP                                                      │
│  Donation events → donor_state_transitions → Donor_State update     │
│  Channel responses → engagement scores → model retraining inputs    │
│  Surge detection → Volatility_Index update → LP reoptimization     │
│                                                                     │
│  ──→ LOOPS BACK TO BASE SCORING (nightly) ──→                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Feedback Signals

| Signal | Source | Feeds Into | Latency |
|--------|--------|-----------|---------|
| Donation event | fec_donations, nc_boe_donations_raw, winred_donors | Donor_State, donor_scores, donor_profiles | Real-time (WinRed) / Daily (FEC) / Weekly (NCBOE) |
| Email open/click | E30 Email tracking | donor_profiles.email_engagement_score | Near real-time |
| SMS response | E31 SMS delivery reports | donor_profiles.sms_engagement_score | Near real-time |
| Phone contact result | E32 Phone banking logs | donor_contacts | End of shift |
| Event attendance | E34/E37 Event check-in | person_master.is_volunteer, donor_contacts | Next day |
| Voter registration change | nc_voters weekly refresh | person_master.registered_party | Weekly |
| News/social surge | E42 News Intelligence | Volatility_Index, Surge_Detection | Hourly |

## Cycle Time

| Phase | Frequency | Duration |
|-------|-----------|----------|
| Full pipeline (data → scores → models → allocation) | Nightly | ~4 hours (02:00-06:00 UTC) |
| Real-time feedback (donation → state update) | Continuous | < 5 minutes (WinRed webhook) |
| Weekly refresh (voter file + identity resolution) | Weekly | ~2 hours |
| Quarterly recluster (district personality) | Quarterly | ~1 hour |
