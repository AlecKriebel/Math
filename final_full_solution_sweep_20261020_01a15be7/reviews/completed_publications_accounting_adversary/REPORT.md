# Completed publications accounting adversarial checkpoint

Review completed: 2026-10-21 UTC. Review goal completion estimate: **100%** for this bounded checkpoint. The whole research sweep remains incomplete.

## Verdict

**The four current publications, public payloads and ledger rows pass the independent checks below. The captured accounting validator has genuine fail-closed identity gaps.** These are summary-accounting validation defects; the tests do not show incorrect canonical data or authorize republishing, changing scientific packages, allocating another DOI, or changing ledger rows.

The input is the individually captured bytes in `inputs/effort/`, bounded by `INPUT_MANIFEST.json`. Coverage implementation SHA256 and all inputs are sealed by `OUTPUT_MANIFEST.json`. The captured state has next PR 430, completed ordered prefix 9–429 (421 entries), refreshed inventory maximum 1444 and 1436 PRs. Canonical files may advance later; this review makes no blanket assertion that current files remain unchanged.

## Verified current records

| PR | Problem / source | Public record | Version | Unique ledger row |
|---|---|---|---|---|
| 292 | 30001608 / OWR-4530-006 | https://zenodo.org/records/23524971 | 1.0 | 174 |
| 397 | 9700002 / AMR-096-0002 | https://zenodo.org/records/23527793 | 1.0 | 176 |
| 399 | 30001179 / OWR-3392-005 | https://zenodo.org/records/23539283 | 1.0 | 177 |
| 280 reopened | 30000156 / OWR-768-006 | https://zenodo.org/records/23539734 | 1.1 | 178 |

The full DOI for each record is `10.5281/zenodo.` followed by its record number. Independent unauthenticated HTTPS GETs returned HTTP 200 for all four records, four DOI resolutions and eight files. Every DOI ended at the exact HTTPS `zenodo.org/records/<expected-record>` path without query or fragment. All four API records report published status, done state and submitted=true. Record ID, DOI, title, version, author/ORCID, intended metadata and file sets match. API representations of deposit upload_type/publication_type as resource_type type/subtype, and license string as license.id, are explicitly normalized; raw representation differences remain in `PUBLIC_VALIDATION.json`.

All eight publicly downloaded PDF/ZIP files match the root receipt byte counts, SHA256 and MD5 values, and the API checksum/size metadata. Their hashes also match the frozen release manifests and later root publication clearances. No stale or substituted public payload was found. Preparation manifests for PR399 and PR280 retain publication_ready=false/published=false as historical preparation state; later clearances and live public records establish their publication. These historical flags do not contradict the later outcomes.

All four ZIPs have unique safe paths, no symlink entries, valid CRCs and complete exact SHA256/size manifests. Counts are 92/91 (members/payloads) for PR292, 138/137 for PR397, 82/81 for PR399, and 69/68 for PR280: **377 verified payloads**. Each contains editable TeX, a README, reproduction code, frozen originals, source snapshots and scoped review support. All **92 original files** (40+24+11+17) match both their source snapshot sizes/hashes and their immutable Git blob bytes. PR397's historical source snapshot calls its local originals `original/`; the public archive puts those same files under documented `candidate/`. That layout mapping was applied explicitly. No mathematical checks were rerun in this publication-accounting audit.

## Live ledger and duplicate checks

The actual GWS CLI values.get read requested the whole `'Math Puzzles'!A:AQ` range with FORMATTED_VALUE and returned 178 rows. Raw response, exact request arguments, timestamps and hashes are in `live/`. Columns A–D of rows 174,176,177,178 match each corresponding root ledger receipt exactly. Across the complete returned sheet, each DOI, problem ID, exact source alias, exact publication title and original PR URL occurs only on its expected row. There are four distinct result identities, DOIs and rows, with no missing or extra corresponding row found.

Broad semantic leads were checked rather than assumed duplicates. PR397 leads at rows107 (a distinct fixed-city ODE problem) and115 (oriented percolation flow) differ in target and theorem. PR399 leads at rows78 (ambient dependence of independence) and88 (GNS descent) concern distinct questions; row177 explicitly explains the shared generation target of 30001178 without allocating a second result. PR280's row21 lead is the unrelated regular-pentagon quintic fifth-torsion result. PR292 has only row174. The lead texts and exact matching rows are retained in `LEDGER_VALIDATION.json`.

This is a live whole-ledger uniqueness check plus exact public-record identity check. It is **not** a new exhaustive authenticated enumeration of every Zenodo account draft/version, all other repositories or the worldwide literature. Root's earlier bounded lifecycle duplicate checks are recorded in the captured receipts; they were not promoted into a new independent universe-wide deduplication certificate.

## Historical and effective accounting

An independent direct journal calculation, separate from execution of coverage_snapshot.py, confirms the exact 421-entry ordered prefix and the single historical PR280 hold. `PR0280_DISPOSITION.json` still has SHA256 `12786fed27bdc64dc25404de4d559f04611947006cfb62f0ee6e8bf1399009b1`, agrees semantically with the preserved ordered journal entry, and records the prior `skip_priority_gate_not_met` decision. The new replacement binds that exact historical hash.

Historical counts correctly retain **3 published** and **3 priority holds**. Applying the separately verified PR280 replacement exactly once yields **4 published** and **2 priority holds**, with all other counts unchanged. The completed-publications list has exactly those four entries, each presently matching its root publication receipt in PR, problem, DOI, record, row and merge commit. The separate existing external-publication reconciliation for PR293 is not counted as a fifth own new publication. `INDEPENDENT_ACCOUNTING.json` and `coverage_baseline.json` retain these checks.

## Actionable accounting-validator findings

**A1 — Cross-artifact identities are incompletely bound.** In isolated copies of the captured code and inputs, changing publication.pr to999, replacement.ledger_row to179, completed.verification to PR0292's receipt, completed.record or problem_id to another result, replacement.problem_ids, or publication.record still yields an accepted snapshot with four published entries. The current implementation checks the replacement PR, selected DOI equalities and the publication row against the completed row, but omits the remaining corresponding identity equalities and the equality between completed.verification and replacement.publication_evidence. This permits mutually inconsistent accounting evidence to be described as fully verified.

**A2 — Ordinary completed entries are not reconciled to their proof of publication or effective dispositions.** A PR292 completed entry can name PR397's verification, claim an unrelated unique DOI, or change its PR to293 and still pass. Appending another PR292 entry with a new unique DOI, or an unbound PR999 publication using an existing receipt path, also passes while the effective publication disposition count remains four. The completed list needs an exact one-to-one relation with effective own publication dispositions, unique PR/problem/record/row identities where applicable, and matching receipt contents.

**A3 — Claimed verification accepts missing material.** Replacing the reopened publication's files array by an empty array still passes. At minimum, the summary validator must validate the expected material receipt schema and nonempty required public PDF/ZIP evidence and bind that evidence to the exact publication. This need not turn the summary script into another network publisher or proof auditor. It should fail closed when its local evidence is incomplete, while retaining its explicit structural scope.

`OVERRIDE_CONTROLS.json` contains **21 cases**: baseline accepted; seven genuine guards correctly reject corrupted historical binding, duplicate override/DOI, published=false, wrong reopened DOI, wrong public row and wrong replacement PR; **13 deliberately inconsistent cases are wrongly accepted**. Each changed input is retained under `fixtures/`. All changes were to review-local fixtures. The original implementation and canonical input bytes are preserved for repair acceptance. No repair was applied by this reviewer.

A repair should preserve the four valid canonical records and the historical/effective count distinction, reject all inconsistent controls, bind canonical receipt paths/identities/material fields, and use independent fresh controls for malformed types, alternate DOI spellings, duplicate rows/records, missing evidence and path escapes as relevant. New review/repair should be separately timestamped; do not overwrite this pre-repair evidence.

## Limits and workflow incident

This checkpoint verifies accounting, public publication identities and reproducible file integrity. It does not independently prove the scientific theorems or audit priority. Each is a scoped unrefereed AI-assisted result with the bounded novelty/source limitations stated in its metadata and ledger text. Successful publication does not certify universal novelty, human peer review, current openness or the entire source question beyond the printed scope.

The web renderer could not open the Zenodo record pages; the fresh direct public HTTPS metadata/landing/file captures succeeded and provide the actual evidence. No account token was used for those captures. Immutable Git objects were read with `GIT_OPTIONAL_LOCKS=0`; no ordinary git status, index, ref, commit, push, provider write or external outreach was performed.

**Local workflow violation:** `gws generate-skills --help` unexpectedly executed skill generation in `/Users/alec/Documents/Math`, emitting `docs/skills.md` and `skills/`, outside this review folder. No pre-command bytes or baseline were captured, so this review cannot say whether preexisting originals were overwritten or only generated files were created. The exact command, emitted path categories, available time bound and lack of baseline are in `INCIDENT.json`. The parent was notified promptly and controls any overlap inspection; this reviewer performed no deletion/revert. Subsequent GWS access was limited to the authorized read-only values.get. This incident does not change the public byte and ledger evidence, but it prevents an unqualified claim that every local write was confined to the review folder.
