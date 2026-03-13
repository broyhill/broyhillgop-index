Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# MASTER SCHEMA

## Database Overview

BroyhillGOP runs on Supabase PostgreSQL with 657 tables containing 59,098,347 rows across 11,498 columns.

## Core Tables — Full Column Detail

### nc_datatrust (7,654,883 rows | 251 columns | 15 indexes)
The DataTrust voter file is the richest single table — 251 columns covering voter registration, demographics, modeled propensity scores, consumer data overlays, and political history. Key column groups:
- Voter ID and registration (rnc_regid, state_voter_id, county_id)
- Demographics (age, gender, race, education, income brackets)
- Modeled scores (partisanship, turnout propensity, donor propensity, issue affinity)
- Contact info (addresses, phones, emails)
- Vote history (general/primary participation flags by year)

### nc_voters (9,049,588 rows | 71 columns | 29 indexes)
Official NCSBE voter registration file. Every registered voter in North Carolina.
- Registration details (voter_reg_num, status, party, registration_date)
- Demographics (age, race, gender, ethnicity)
- Geographic (county, precinct, congressional_dist, nc_senate_dist, nc_house_dist, municipality)
- Contact (residential_address, mailing_address)

### person_master (7,656,550 rows | 37 columns | 9 indexes)
The identity spine — one golden record per resolved person.
- Identifiers (person_id UUID, best_voter_id, best_datatrust_id)
- Merged demographics (name, age, gender, race — best available from all sources)
- Contact (best_address, best_phone, best_email)
- Flags (is_donor, is_volunteer, is_activist, is_voter)
- Scores (composite_score, donor_propensity, volunteer_propensity)

### fec_donations (1,132,719 rows | 24 columns | 6 indexes)
Federal Election Commission individual contribution records.
- Transaction (transaction_id, amount, date, transaction_type)
- Donor (contributor_name, contributor_city, contributor_state, contributor_zip, contributor_employer, contributor_occupation)
- Recipient (committee_id, committee_name, candidate_id)

### fec_god_contributions (226,451 rows | 127 columns | 22 indexes)
The "GOD" enriched FEC record — 127 columns of derived intelligence per donation.
- All base FEC fields plus: donor scoring, giving history, escalation trajectory, lapse risk, committee type classification, district mapping, issue affinity scores

### nc_boe_donations_raw (652,532 rows | 61 columns | 28 indexes)
NC Board of Elections campaign finance records.
- Transaction details (amount, date, type, purpose)
- Donor info (name, address, employer, occupation)
- Committee/candidate recipient details
- Filing metadata (report_name, period, filing_type)

### rnc_voter_core (1,105,946 rows | 62 columns | 19 indexes)
RNC's proprietary voter file for NC.
- Voter registration and demographics
- Modeled partisan and turnout scores
- Phone and address data
- Vote history summary

### candidates (2,303 rows | 242 columns)
Master candidate table — 242 columns covering every aspect of a candidate's profile, campaign history, donor network, and strategic positioning.

### donor_profiles (34 columns)
Aggregated donor intelligence — lifetime giving, frequency, recency, preferred channels, escalation stage, lapse risk.

### winred_donors (194,279 rows | 26 columns | 5 indexes)
WinRed online fundraising platform donor records with transaction history and recurring gift flags.

## Table Distribution by Ecosystem

63 ecosystem groups, with data concentrated in:
- CORE Data/Identity — nc_datatrust, nc_voters, person_master, acxiom_consumer_data
- CORE Fundraising — fec_donations, fec_god_contributions, nc_boe_donations_raw, winred_donors
- RNC Data — rnc_voter_core, rnc_phones, rnc_addresses, rnc_demographics_acs, rnc_scores
