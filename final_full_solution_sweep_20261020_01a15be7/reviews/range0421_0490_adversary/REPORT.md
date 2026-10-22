# Independent adversarial review: PR421–490

Completed 2026-10-21T17:24:59.706761+00:00. **PASS for all 70 recorded classifications, within the eligibility and existing-publication identity scope below. No blocking finding or requested correction remains.** Review completion estimate: **100% of this assigned range review**. This is not an estimate of whole-sweep or mathematical discovery completion.

The range contains **50 `unsolved`, 17 `already_solved`, and 3 `claimed_solved` corresponding changed QUEUE rows**. The first 67 must be skipped under the user's explicit-status rule. The three claimed solutions are already published and correctly represented in whole live ledger rows: PR421 / row66 / DOI10.5281/zenodo.23328912; PR464 / row65 / DOI10.5281/zenodo.23320818; PR468 / row62 / DOI10.5281/zenodo.23310484. No unpublished eligible full-solution claim or missing-status case was found in this range.

## Evidence and independence

I read the classification policy and independently checked actual Git commit objects, rather than treating the root's scope receipts or `pinned_scope_check.py` as a certification. The canonical helpers were not run or edited. For **each PR**, I compared the frozen inventory's exact base...head diff using `git diff --no-ext-diff --no-renames --name-only -z`; its complete NUL-delimited path set matched both cached path inventories and file count. I separately read the entire zero-context QUEUE patch, its actual head QUEUE blob, and actual changed claim/source entrypoints. Every diff adds exactly one corresponding own row. All 70 own rows exactly match the eligibility cache and root's recorded source lines where supplied. No queue truncation, extra unclassified row, unrelated-status substitution, hidden second effort root, or malformed status was observed. All scoped disposition files exactly equal their single corresponding frozen journal entries. The complete path counts include 211 paths for PR464 and 95 for PR468.

`per_pr_assessments.json` records each actual source alias, ID, own-row status, complete path count, effort root, and actual changed-file ID anchors. Every PR has an ID anchor in actual pinned claim/source material. The complete pinned path and QUEUE evidence is in `pinned/`. Pinned actual entrypoint files are retained there as well. The independently checked eligibility boundary is separate from proof correctness.

At 2026-10-21T17:18:22.945377+00:00, a fresh read of all 70 GitHub PRs found **no change** from the individually frozen inventory in title, complete body, state, draft status, updated timestamp, head SHA or base SHA. Merged status was not used as publication evidence. At 2026-10-21T17:16:58.237726+00:00, a fresh GWS `values.get` of `'Math Puzzles'!A:AQ` with `FORMATTED_VALUE` returned **178 whole rows**. The exact entire result and read receipt are retained. GWS skill shared instructions were absent; the task explicitly prohibited `generate-skills`, so no skill generation or unrelated filesystem write was attempted. Only the authorized direct read command was used.

The 170 source snapshots in `INPUT_MANIFEST.json` were read individually and hashed at their own `read_at` timestamps. Inventory and journal snapshots are separately frozen mutable inputs. These are not a claim that the shared tree or all remote state was atomically frozen. Only the scoped 70 inventory records and journal entries were used for this decision. `OUTPUT_MANIFEST.json` binds the generated review evidence; its own hash is separately in `OUTPUT_MANIFEST.sha256`.

## Deliberately challenged eligibility cases

- **Custom roots423/425/426/428/429/437/438/440/446/449/450/465/469/490:** actual pinned README/source or release entrypoints explicitly identify their same numeric problem and source alias. Their actual QUEUE patches say `unsolved`. The restricted results, repaired formulas, counterexamples to auxiliary claims, and complete special cases do not require substantive candidate work under the user's rule.
- **PR441:** `kourovka_21_136/README.md`, including its frozen original, explicitly identifies catalogue **2645 / Kourovka21.136** and the infinite-order conjugacy question. Its actual QUEUE row is 2645 / KOU-21.136, `unsolved`,5/5. The lack of numeric2645 in the directory name does not break correspondence. The finite-derived-length soluble-by-torsion theorem is explicitly restricted and the general question is retained as unresolved.
- **PR431 and435:** the additional nonstandard `problems/2561_involution_product_orders` and `problems/2611_free_spectrum_integer_base` roots identify their same numeric records; no unrelated changed row was substituted.
- **PR469:** the README and release-scope material explicitly acknowledge a complete unbounded quantitative fractional-coefficient advantage, state that the source does not require a superpolynomial gap, and retain the conservative `unsolved`,5/5 campaign status for qualitative naturalness/history reasons. The actual own QUEUE row is explicitly `unsolved`; this review does **not** override that label or start a proof/priority audit.
- **PR436/445/458/462/463/466/480:** current bodies contain stale `claimed_solved` wording. Actual complete pinned changes add the corresponding `already_solved` row for the same problem. For458/462/463/466/480 the row itself contains an explicit dated source-bound priority correction. Under policy2 and the user's status rule, these are correctly excluded even if their bodies retain an original complete theorem. This is an eligibility conclusion; it does not independently certify the row's literature analysis.

## Existing publication identities and available payloads

Fresh Zenodo API responses for all three records report `status=published`, `state=done`, `submitted=true`. Every DOI resolves HTTP200 to its expected canonical record. All **seven actual public downloads** match provider byte counts and MD5 checksums and match the root's recorded SHA256 values. All **four ZIPs** have unique safe member paths, no symlinks, and clean CRCs. The three positive payload manifests independently verify **22+180+67=269** payload sizes and SHA256s. These are integrity/availability checks, not execution of published mathematics or fresh package acceptance.

- **PR421 /20001515 / AIM5.2 / row66 / record23328912:** two independently fetched historical primary AIM captures have identical25734 bytes and SHA256 `9dfa1624c5743d114c671ea69201a9ea46fe577e707239e245cc7f22b30b8121`. The actual archived record asks for geometric CAT(0) cubulation of the mapping torus `a→a,b→ab,c→bcb`; the final `b` is positive. This matches the PR, source README, public metadata, six-page source, verification README and whole row66. Its finite quotient counts(1,7,8,2), link counts(14,32,16), and free proper cocompact action describe the same deposited claim. The nearby workshop formula `b→aba` is explicitly distinguished and is not substituted for the original target. Source ZIP4 members and verification ZIP24 members are available. Earlier qualitative tools are credited; minimality, virtual specialness and firstness are not asserted. The current live AIM page failed web retrieval; archive identity is available. [2024 original AIM capture](https://web.archive.org/web/20240828224508id_/http://aimpl.org/freebycyclic/5/), [2026 capture](https://web.archive.org/web/20260310215532id_/http://www.aimpl.org/freebycyclic/5/).
- **PR464 /30004807 / OWR-8415343-010 / row65 / record23320818:** I read the original report's geometric conjecture on printed2232–2233. The paper and ledger consistently state a negative-mass regular-ZAS counterexample under static-foliation and retained-boundary vector tests, full scalar absolute convergence for every allowed test, normalized radial defect−8π, known DKMV metric/tensor and BKTZ flux attribution. NEC violation and exclusions for arbitrary tilted slices, prescribed matter and collapsed-point tests are visible. The informal source formulation is not silently strengthened: the disclosed interpretation matches across the publication, PR and row. The85393-byte PDF and258059-byte verification ZIP are available; all181 members include editable source, current controls and13 historical files. The public manuscript and canonical metadata exactly match their pinned PR blobs. [Original Oberwolfach report](https://ems.press/content/serial-article-files/46918).
- **PR468 /30000689 / OWR-1455-008 / row62 / record23310484:** the original Conjecture4 at printed238 asks for the missing-middle-face embedding obstruction. Its arbitrary triangulated topological even-sphere source and topological embedding target match the actual public theorem and row62. The actual-vertex convention makes d=0 vacuous; the published scope includes credited d≥3 synthesis and the actual-PL-class dimension-four extension. No first-priority claim is implied. The96399-byte PDF and152980-byte verification ZIP are available; all68 members include editable source, current controls and15 historical files. The public manuscript and canonical metadata exactly match pinned PR blobs. [Original Oberwolfach report](https://ems.press/content/serial-article-files/46090).

The broad semantic matches were actively rejected as duplicates: live **row69 / PR256 / DOI23331331** concerns outer-pedal elliptic-billiard centroid/signed area, not weak Bianchi identities. Live **row169 / PR1155 / DOI23444839** concerns double-Cohen-Macaulay sphere-subcomplex decomposition, not the missing-face embedding obstruction. These are distinct original problems and conclusions. This observation does not process, mathematically audit or dispose either out-of-range PR.

## Exact per-PR outcome

Every path count and status in this table comes from actual pinned Git changes. Each explicit non-claimed status was skipped without substantive mathematics or priority work.

| PR | Original problem / alias | Actual corresponding status | Complete changed paths | Independent assessment |
|---|---|---|---:|---|
| 421 | 20001515 / AIM-GEOMETRIC_GROUP_THEORY-0024 | claimed_solved | 54 | Existing publication matched |
| 422 | 20001546 / AIM-GEOMETRIC_GROUP_THEORY-0055 | unsolved | 19 | Explicit status exclusion confirmed |
| 423 | 20001670 / AIM-GEOMETRY-0008 | unsolved | 16 | Explicit status exclusion confirmed |
| 424 | 20001782 / AIM-GEOMETRY-0120 | unsolved | 14 | Explicit status exclusion confirmed |
| 425 | 20001851 / AIM-GEOMETRY-0189 | unsolved | 18 | Explicit status exclusion confirmed |
| 426 | 20001939 / AIM-GEOMETRY-0277 | unsolved | 15 | Explicit status exclusion confirmed |
| 427 | 20002029 / AIM-GEOMETRY-0367 | unsolved | 33 | Explicit status exclusion confirmed |
| 428 | 20002237 / AIM-LOGIC-0013 | unsolved | 16 | Explicit status exclusion confirmed |
| 429 | 20002290 / AIM-LOGIC-0066 | unsolved | 19 | Explicit status exclusion confirmed |
| 430 | 2566 / KOU-21.57 | unsolved | 17 | Explicit status exclusion confirmed |
| 431 | 2561 / KOU-21.52 | unsolved | 67 | Explicit status exclusion confirmed |
| 432 | 2580 / KOU-21.71 | unsolved | 17 | Explicit status exclusion confirmed |
| 433 | 2609 / KOU-21.100 | already_solved | 22 | Explicit status exclusion confirmed |
| 434 | 2607 / KOU-21.98 | unsolved | 16 | Explicit status exclusion confirmed |
| 435 | 2611 / KOU-21.102 | unsolved | 40 | Explicit status exclusion confirmed |
| 436 | 2569 / KOU-21.60 | already_solved | 27 | Explicit status exclusion confirmed |
| 437 | 2628 / KOU-21.119 | unsolved | 16 | Explicit status exclusion confirmed |
| 438 | 2622 / KOU-21.113 | unsolved | 23 | Explicit status exclusion confirmed |
| 439 | 2643 / KOU-21.134 | already_solved | 12 | Explicit status exclusion confirmed |
| 440 | 2637 / KOU-21.128 | unsolved | 39 | Explicit status exclusion confirmed |
| 441 | 2645 / KOU-21.136 | unsolved | 32 | Explicit status exclusion confirmed |
| 442 | 2801 / KP-3.3 | already_solved | 10 | Explicit status exclusion confirmed |
| 443 | 2650 / KOU-21.141 | unsolved | 44 | Explicit status exclusion confirmed |
| 444 | 30006563 / OWR-14299905-038 | unsolved | 26 | Explicit status exclusion confirmed |
| 445 | 30002737 / OWR-13355-001 | already_solved | 13 | Explicit status exclusion confirmed |
| 446 | 30006560 / OWR-14299905-035 | unsolved | 27 | Explicit status exclusion confirmed |
| 447 | 30004980 / OWR-9790352-030 | unsolved | 47 | Explicit status exclusion confirmed |
| 448 | 30005144 / OWR-10252937-007 | already_solved | 20 | Explicit status exclusion confirmed |
| 449 | 30005041 / OWR-9790362-012 | unsolved | 15 | Explicit status exclusion confirmed |
| 450 | 30005075 / OWR-9790367-005 | unsolved | 23 | Explicit status exclusion confirmed |
| 451 | 30005220 / OWR-11101920-004 | unsolved | 25 | Explicit status exclusion confirmed |
| 452 | 30004557 / OWR-2654830-012 | unsolved | 23 | Explicit status exclusion confirmed |
| 453 | 2305057 / AMR-022-5057 | already_solved | 13 | Explicit status exclusion confirmed |
| 454 | 10400167 / AMR-103-0167 | unsolved | 27 | Explicit status exclusion confirmed |
| 455 | 30005248 / OWR-11695855-001 | unsolved | 17 | Explicit status exclusion confirmed |
| 456 | 6200043 / AMR-061-0043 | unsolved | 52 | Explicit status exclusion confirmed |
| 457 | 30005718 / OWR-14298007-013 | unsolved | 55 | Explicit status exclusion confirmed |
| 458 | 20000693 / AIM-ANALYTIC_NUMBER_THEORY-0057 | already_solved | 28 | Explicit status exclusion confirmed |
| 459 | 30005507 / OWR-13750328-012 | unsolved | 17 | Explicit status exclusion confirmed |
| 460 | 30005508 / OWR-13750328-013 | unsolved | 19 | Explicit status exclusion confirmed |
| 461 | 30005717 / OWR-14298007-012 | unsolved | 18 | Explicit status exclusion confirmed |
| 462 | 30005528 / OWR-13750333-009 | already_solved | 13 | Explicit status exclusion confirmed |
| 463 | 6000016 / AMR-059-0016 | already_solved | 15 | Explicit status exclusion confirmed |
| 464 | 30004807 / OWR-8415343-010 | claimed_solved | 211 | Existing publication matched |
| 465 | 30000330 / OWR-1106-004 | unsolved | 17 | Explicit status exclusion confirmed |
| 466 | 30000999 / OWR-2042-008 | already_solved | 18 | Explicit status exclusion confirmed |
| 467 | 30005772 / OWR-14298158-017 | unsolved | 16 | Explicit status exclusion confirmed |
| 468 | 30000689 / OWR-1455-008 | claimed_solved | 95 | Existing publication matched |
| 469 | 30005832 / OWR-14298166-010 | unsolved | 15 | Explicit status exclusion confirmed |
| 470 | 30005723 / OWR-14298009-001 | unsolved | 19 | Explicit status exclusion confirmed |
| 471 | 30002659 / OWR-13110-001 | unsolved | 21 | Explicit status exclusion confirmed |
| 472 | 11000020 / AMR-109-0020 | already_solved | 22 | Explicit status exclusion confirmed |
| 473 | 30001895 / OWR-11136-027 | unsolved | 85 | Explicit status exclusion confirmed |
| 474 | 30001148 / OWR-3388-006 | already_solved | 18 | Explicit status exclusion confirmed |
| 475 | 30006510 / OWR-14299586-001 | unsolved | 16 | Explicit status exclusion confirmed |
| 476 | 30002320 / OWR-12481-005 | unsolved | 18 | Explicit status exclusion confirmed |
| 477 | 30002086 / OWR-11789-007 | unsolved | 18 | Explicit status exclusion confirmed |
| 478 | 30005961 / OWR-14298581-008 | unsolved | 12 | Explicit status exclusion confirmed |
| 479 | 30003616 / OWR-15951-003 | unsolved | 15 | Explicit status exclusion confirmed |
| 480 | 30003656 / OWR-15958-003 | already_solved | 14 | Explicit status exclusion confirmed |
| 481 | 10400136 / AMR-103-0136 | unsolved | 18 | Explicit status exclusion confirmed |
| 482 | 10900004 / AMR-108-0004 | unsolved | 18 | Explicit status exclusion confirmed |
| 483 | 20001282 / AIM-CONVEX_GEOMETRY-0014 | unsolved | 12 | Explicit status exclusion confirmed |
| 484 | 20001287 / AIM-CONVEX_GEOMETRY-0019 | already_solved | 14 | Explicit status exclusion confirmed |
| 485 | 20001306 / AIM-CONVEX_GEOMETRY-0038 | unsolved | 14 | Explicit status exclusion confirmed |
| 486 | 20001353 / AIM-DYNAMICAL_SYSTEMS-0011 | already_solved | 16 | Explicit status exclusion confirmed |
| 487 | 20001754 / AIM-GEOMETRY-0092 | unsolved | 17 | Explicit status exclusion confirmed |
| 488 | 20001752 / AIM-GEOMETRY-0090 | unsolved | 20 | Explicit status exclusion confirmed |
| 489 | 20003004 / AIM-TOPOLOGY-0092 | already_solved | 21 | Explicit status exclusion confirmed |
| 490 | 20002696 / AIM-PROBABILITY-0138 | unsolved | 15 | Explicit status exclusion confirmed |

## Unresolved findings and limits

**Blocking unresolved findings: none.** The root can accept the range's classifications as supported by this independently observed evidence.

Residual boundaries are explicit: this does not prove scientific correctness, novelty, historical first priority, universal current openness, every possible interpretation of informal original questions, arbitrary cache/manifest schema validity, or unchanged future remote state. The read-only verifier supports the two actually observed manifest shapes and these actual inputs; it is not a general schema-security proof. The canonical helper's previous hardening review was neither rerun nor promoted to stronger authority. The unavailable current AIM page is offset for identity by two actually recovered archival primary captures, without certifying current-page freshness. Later sweep state or new PRs fall outside this fixed assigned range. Recheck material live state before any future irreversible action.

No publication, ledger change, provider mutation, Git/index/ref/PR change, commit, push, external comment, new mathematical computation or contact with another person occurred. All new review files are confined to this dedicated folder. The parent receives this report solely through the authorized audit workflow.

## Reproduction

With the pinned Git objects already present, run `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0 python3 verify_review_evidence.py` from this folder. It checks frozen input hashes, re-reads actual pinned path/QUEUE evidence, checks the retained whole-row publication identities, provider payload hashes and269 positive archive payloads. `verification_replay.json` records a successful read-only replay. Public service reads and source observations have their original receipt timestamps; this replay does not refetch live state or execute publication scripts.
