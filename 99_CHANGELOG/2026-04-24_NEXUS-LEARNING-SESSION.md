# Changelog Entry — 2026-04-24 · Nexus Learning Session

**Contributor:** Nexus (Perplexity, E51)
**Status:** Advisory — no data or schema changes in this session
**Scope:** Documentation + planning only; cross-reference to `broyhill/nexus-platform` for full detail

---

## What happened

A learning-posture session (per Ed's direct instruction *"learn some more before you tamper"*) in which Nexus read across the full BroyhillGOP corpus — this index, the main BroyhillGOP repo, the nexus-platform repo, the Supreme Masterplan, and the NCRDC Legal Document Suite in Drive/Dropbox — and corrected eight mis-assumptions from the opening minutes of the session.

## Key facts verified LIVE on Hetzner (post-compromise rotated credentials, sandbox access confirmed)

| Object | Count | Source | As of |
|---|---|---|---|
| `raw.ncboe_donations` | 321,348 rows | Hetzner | 2026-04-24 04:29 UTC |
| `raw.ncboe_donations` distinct clusters | 98,303 | Hetzner | 2026-04-24 04:29 UTC |
| Canary cluster 372171 | 147 txns / $332,631.30 / ed@broyhill.net | Hetzner | 2026-04-24 04:29 UTC |
| Acxiom-resolved donations | 290,561 (90.4%) | Hetzner | 2026-04-24 04:29 UTC |
| Acxiom-resolved clusters | 80,605 of 98,303 (82.0%) | Hetzner | 2026-04-24 04:29 UTC |
| `committee.v_republican_party_individual_donors` | 183,412 rows / 10,032 clusters / 129 party-affiliate orgs | Hetzner | 2026-04-24 04:30 UTC |
| `core.datatrust_voter_nc` | 7,727,637 rows × 252 cols | Hetzner | 2026-04-24 04:29 UTC |
| `core.acxiom_ibe` | 7,655,593 rows × 911 cols | Hetzner | 2026-04-24 04:29 UTC |
| `core.acxiom_market_indices` | 7,655,593 rows × 526 cols | Hetzner | 2026-04-24 04:29 UTC |
| `core.acxiom_ap_models` | 7,655,593 rows × 480 cols | Hetzner | 2026-04-24 04:29 UTC |
| `core.acxiom_consumer_nc` | 7,655,593 rows × 22 cols | Hetzner | 2026-04-24 04:29 UTC |
| DataTrust + Acxiom combined attribute columns | **2,191 total across 7.6M people** | Hetzner | 2026-04-24 04:29 UTC |

This confirms the "2,200 variables" the Blueprint references are **already loaded** on the production server — not pending an ingest.

## Contradictions surfaced for Ed's ruling (not resolved in this session)

1. **NCBOE row count.** `nexus-platform/BroyhillGOP-master-plan/TO-DOS-CURRENT.md` and `nexus-platform/SUPREME-MASTERPLAN/FAMILY-AND-DONOR-ROSTER.md` both say "2,431,198 raw / 321,348 unique — do not 'fix.'" The `database-operations` skill (last edited 2026-04-17 post-tumor-cleanup) says the 2.4M inflated table was dropped; the live spine is 321,348. Live tonight = **321,348**. Both statements cannot coexist.
2. **Cursor FORBIDDEN list.** `nexus-platform/agents/cursor/CURSOR-FIRST-MESSAGE-COMMITTEE-PARTY.md` and `.cursorrules` block `nc_voters`, `person_master`, `nc_datatrust`, `fec_god_contributions`. The rollup work the platform needs — 20 name-variations-per-donor over 10 years accordion-rolled through Acxiom resolution — requires those joins. Scope needs widening or routed via views.
3. **Plaintext credential in public repo.** `broyhill/BroyhillGOP/docs/00_READ_FIRST_MANDATORY_INSTRUCTIONS.md` contains a plaintext Supabase password. The `broyhill/BroyhillGOP` repo is public. Same attack surface as the April-17 compromise. Rotate and purge history.

## What Nexus learned that is now locked into the model

1. **BroyhillGOP is an AI CRM.** 60 ecosystems, Republican-only, serving 3,000 candidates (federal → county sheriff) across all 100 NC counties. 10-year, 160,000-record donor database. AI is the product, not an add-on.
2. **The 6 condensed categories** (this repo's top-level folders — `00_OVERVIEW` through `05_AUTOMATION`) are the unified mental model every candidate sees in the same order; the 60 modules E00-E60 live *inside* those 6 categories.
3. **Candidate silos are data boundaries; categories are mental-model boundaries.** Different candidates, same six boxes, personalized contents.
4. **Acxiom IS DataTrust** — same data, vendor vs. partner naming.
5. **Acxiom is the dedupe engine,** not an enrichment overlay. `rnc_regid` is the match key. 90.4% of the donor spine resolves through it.
6. **Party affiliates are organizations, not candidates.** 129 NCGOP/county GOP/caucus/REC recipients — distinct from the 2,200+ candidate committees. Must never be mixed per RULE_DONOR_SEPARATION.
7. **The real-time loop is: Match → Microsegment → Nurture-to-Close → Attribute → Learn → Repeat — every minute, for 3,000 candidates in parallel,** powered by molecular cost/benefit/variance accounting that becomes ML training data.
8. **The #1 platform gap is the Brain Worker daemon** — 905 triggers loaded, nothing fires them. Until this runs, every other system is batch.

## Artifacts produced in `nexus-platform` this session

| Path | Purpose |
|---|---|
| [`sessions/transcripts/2026-04-24-perplexity-nexus-transcript.md`](https://github.com/broyhill/nexus-platform/blob/main/sessions/transcripts/2026-04-24-perplexity-nexus-transcript.md) | Full learning-session transcript with eight corrections documented |
| [`BroyhillGOP-master-plan/TOMORROW-2026-04-24.md`](https://github.com/broyhill/nexus-platform/blob/main/BroyhillGOP-master-plan/TOMORROW-2026-04-24.md) | Tomorrow-morning plan: party-affiliate accordion under new `affiliate` schema |
| [`BroyhillGOP-master-plan/weekly-plans/2026-04-24_to_2026-04-30.md`](https://github.com/broyhill/nexus-platform/blob/main/BroyhillGOP-master-plan/weekly-plans/2026-04-24_to_2026-04-30.md) | 7-day plan: from static data to firing engine (Brain Worker live by Day 6, DRAFT mode) |
| [`sessions/NEXUS-LOG.md`](https://github.com/broyhill/nexus-platform/blob/main/sessions/NEXUS-LOG.md) | Session 2 appended |
| [`BroyhillGOP-master-plan/updates/2026-04-24-perplexity.md`](https://github.com/broyhill/nexus-platform/blob/main/BroyhillGOP-master-plan/updates/2026-04-24-perplexity.md) | Master-plan update with flagged contradictions |

## Discipline on tomorrow's work

Rules from `broyhill/BroyhillGOP/sessions/2026-04-18/ACCOUNTABILITY_2026-04-18.md` are now mandatory at every session boot:

- **Rule A** — query `information_schema.columns` before any DDL/DML
- **Rule B** — every factual answer names source table + host + sync date
- **Rule C** — resolve connectivity before accepting the first user request
- **Rule D** — honest reversal when wrong, not reframe
- **Rule E** — never skip a step of a protocol we claim to follow

## Next changelog entry will follow

The next entry in this file will be after Day 1 of the 7-day plan — the party-affiliate accordion — and will report the new `affiliate.*` schema objects for indexing.

---

*Committed to the document search engine index so every future agent session can locate this learning from keyword search. — Nexus, 2026-04-24 01:23 EDT.*
