Version: v4.0
Last Updated: March 13, 2026
Owner: Data Committee Steward

---

# CORE DONOR FILE

## Definition

The Core Donor File is a candidate-specific, pre-scored list of the most promising donors for a given race. It is the single most valuable deliverable from the platform to a candidate.

## Construction

### Universe Assembly
1. Start with all persons in the candidate's district (nc_voters geographic filter)
2. Add all persons who have donated to similar candidates in the past (fec_donations + nc_boe_donations_raw pattern matching)
3. Add all persons in adjacent districts who donate outside their own district
4. Add all persons flagged by the Lookalike Audience Builder as similar to the candidate's existing donors

### Scoring and Ranking
Each person in the universe receives:
- **Composite Donor Score** (0-100) — from the Donor Scoring model
- **Candidate Affinity Score** — cosine similarity between person's Policy Domain Vector and candidate's issue profile
- **Geographic Proximity Score** — distance weighting (in-district > adjacent > statewide)
- **Giving History Match** — prior giving to the same office level/party/issue space

### Final Ranking
```
Core_Donor_Rank = (0.35 × Donor_Score) + (0.25 × Affinity) + (0.20 × Geo) + (0.20 × History)
```

### Tier Assignment
| Tier | Rank Range | Expected Size | Action |
|------|-----------|--------------|--------|
| Platinum | Top 1% | ~500 | Personal outreach, event invites, major ask |
| Gold | Top 5% | ~2,000 | Phone + mail + email multi-touch sequence |
| Silver | Top 15% | ~5,000 | Direct mail + email sequence |
| Bronze | Top 40% | ~15,000 | Email + digital ads |
| Prospect | Bottom 60% | ~30,000 | Digital awareness only |

## Refresh Cycle
Core Donor Files are regenerated weekly as new donation data flows in and scores update.
