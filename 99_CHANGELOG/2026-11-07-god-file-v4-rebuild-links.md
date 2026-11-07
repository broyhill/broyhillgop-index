# 2026-11-07 — GOD FILE v4 rebuild: working links + current repo

**Contributor:** Claude (claude.ai session, at Ed's direction)
**Status:** index.html + build script only — no data, schema, or database changes
**Live site:** https://commander-portal.vercel.app (Vercel project `commander-portal`, deploys from `main`)

## Ed's order
"Do all 3, update for new html" — (A) fix the dead Data Committee link, (B) rebuild the index against current sources, (C) make search → click → open the original work from the URL.

## What changed
| Fix | Before | After |
|---|---|---|
| A. Data Committee card | `drive.google.com/drive/folders/unknown` (dead) | `19Senn2EGWDJ_ro0K0GlsvES77FKXtdy9` — real folder, child of GOD-FILE root, found via Drive search |
| B. Coverage | 4,071 entries, Mac Desktop/Downloads only, header frozen at Mar 12 2026 | 51,372 entries: all 4,071 originals kept + 47,301 files from `broyhill/BroyhillGOP` @ `da55f50`; header counts computed at build |
| C. Links | `file:///Users/Broyhill/...` — opened only on Ed's Mac in Safari | every entry has a real URL: **GH** badge → GitHub file; **DRIVE** badge → Google Drive search for the file name. 0 `file://` links remain. COPY still copies the path |

Also fixed: 55 original entries used a different schema (no `cat`/`path`/`src`), which broke grouping and made the source filter throw. They are normalized; the 18 folder rows among them show the folder name.

## Numbers (from the build run)
- Original v4 entries kept: 4,071 — linked to GitHub: 279 — Drive-search fallback: 3,792
- An original links to GitHub only when its parent folder also matches the repo copy, or its file name occurs exactly once in the indexed repo files AND its v4 size equals the repo blob size. A bare name collision (deploy.sh, README.md, schema.sql) never counts — a first pass of 1,380 name-only links was wrong in cases like four unrelated `deploy.sh` files all opening `config/deploy.sh` (Devin + Vercel review, PR #1)
- Repo files: 60,466 total → 47,301 after the quality filter → all 47,301 added (238 of them are also the target of an original entry)
- 217 categories · 20,964 MD · 3,181 SQL
- Page: 9.07 MB raw, ~776 KB gzipped (was 1.25 MB with 4k entries); load + first render under 1 s headless

## Rules applied (from the canonical docs, not invented)
- `docs/canonical/BGOP_SEARCH_ENGINE_MASTER_PLAN.md` Part 8 Fix 3 — GitHub repo as a scan root.
- Same doc, pipeline step 2 — quality filter: `vendor/` (Oktopost clone), `archive/`, `node_modules`, images/fonts/media/zips/css/maps out.
- Same doc, step 12 + `ECO_NATIVE_INTEGRATION_MATRIX_2026-06-01.md` — ecosystem assigned by **path ownership only** (an `E##` / `E##-NAME` directory, or `ecosystem_##_` in a file name). Body mentions are not ownership. No ecosystem was renamed; codes without a name in the page's existing `CATS` map (e.g. E84, E101) show as their code. Files with no ecosystem path go under `GH_<TOP_FOLDER>`.

## How to re-run
Runs on any workstation: reads two local files, writes `index.html`, no network and no database (this repo's CLAUDE.md marks it reference-only for platform code and DB connections).
```bash
git -C <BroyhillGOP clone> ls-tree -r -z --name-only HEAD > repo_files.z
git -C <BroyhillGOP clone> ls-tree -r -l HEAD | awk -F'\t' '{split($1,a," "); print a[4]"\t"$2}' > repo_sizes.tsv
python3 tools/build_v4_index.py --repo-list repo_files.z --repo-sizes repo_sizes.tsv --repo-sha $(git -C <clone> rev-parse HEAD)
```
Re-runs are byte-identical for the same inputs. Original v4 entries are never dropped; GitHub entries are rebuilt from the list.

## Known limits
- DRIVE fallback is a name search in Ed's Drive, not a direct file link: the Drive connector returns ~5 files per call, so a full Drive walk (~1,000 calls) was not done. Those 3,792 originals open only if a copy with that name is in Drive; many also have a same-name repo file (different folder, or under the excluded `archive/`), findable by searching the page.
- GitHub links open only for accounts with access to the private `broyhill/BroyhillGOP` repo; Drive links only for Ed's Google account.
- Repo files carry no size or date (blobless clone); originals keep their v4 size.
- The site is public (no Vercel protection). It now lists ~47k repo file paths; it already listed 4k Mac paths before this change.
