# PR210 supporting release-source adversary04

**Disposition: UNRESOLVED. Three mandatory finding mechanisms, no separate optional findings. Do not use this review as clean clearance.** The supporting review is 100% complete; repair and a fresh subsequent independent review remain required. The scientific PDF/ZIP/TeX/metadata/deposit are unchanged and are outside the mathematical scope of this source review.

## Exact sources and independence

All six current publication helpers and the supplemental reconciler were read in full before prior opinions. `INPUTS.json` and `INDEPENDENT_ATTACK_PLAN.md` froze the independent families at 2026-10-16T03:48:00.418685+00:00. The plan's initial prose timestamp was accidentally rounded to 03:51 and is transparently corrected; the actual INPUTS timestamp and review order were never changed. The source copies under `reviewed_sources/` match these exact input pins and preserve them for a fresh reviewer after repair:

| Source basename | Bytes | SHA256 |
|---|---:|---|
| append_verified_tracker.py | 6439 | `9eedf40db79d0949b1bf98a80b78decc71e94201b7030c7cf42af93f915c0ebb` |
| integrate_reviewed_pr.py | 18074 | `b0309af583e85f3e7c443191322420d5b8a11e73d9eb1d01a34b3f1248912528` |
| publish_preprint.py | 5335 | `67287d9f4e45779040502d7226391a36839716e40cc42f9507a13ae10fd569a5` |
| release_binding.py | 10448 | `afc858a311137fa99e9a33207848d2ccc913a12f07862aa663b610b262bdb8ce` |
| verify_and_merge.py | 8638 | `e56e3f6eb7a7b183f8fe4a3e977f267783188c12faf2766cf456f98910d5eabe` |
| verify_published_readonly.py | 4367 | `05b5e494de791a03fa876da2b777e8891cf145ff67fc78aac9fb9221ec774a8b` |
| reconcile_published_release_readonly.py | 10002 | `f37a36699e2ad0a527e4d71f314b126f29dd2176916d0ec7420acd86afa60e00` |

No actual helper file was executed. Action-bearing helpers ran only as byte-identical copies in disposable fixtures below this review directory; the pure binding module likewise loaded from a temporary byte-identical own copy. Every subprocess and URL entry point was explicitly trapped, with socket creation/Popen forbidden. There were no real provider/CLI/network/Git/index/ref/QUEUE/SQL reads or writes, no secrets/environment inspection, installation, caches, communication or target edits. Programs ran under Python-B. Disposable fixtures were removed. Local original evidence/package/source files were read only.

Only after the frozen plan did I inspect original failure evidence, the complete source03 report/current probes/results and sealed payloads, and the historical release03 archive. `HISTORICAL_EVIDENCE_CHECK.json` reads/hashes every retained eight-call native preparation stdout/stderr record and summarizes the public facts without reproducing the large transport bodies. All 14 archive rows validate. `REVIEWED_SOURCE_DELTA.diff` shows the queued-row repair and newly required synthetic source04 family inclusion as the integration delta from source03. Source03 sealed payload hashes all validate. I did not count prior reviewers' tests as independent tests.

## R4-F1 — Actual MAIN still refuses (mandatory)

The frozen original PR head remains 2180d64b648b81ac660a792f7823d0b715f9cf12, draft/open and claimed_solved/1-of-5 in retained original evidence. Fresh MAIN's captured008 row is queued/0-of-5 and has no scientific subtree. Its three empty release fields 10,11,12 each contain **two spaces**. The new integrator line 93 sets each to **one space**, then line 94 compares the full row exactly. Thus actual untouched MAIN still fails before source copy, Git object construction, native ref intent or update.

Root discovered the exact spacing discrepancy while comparing its reconstruction to actual capture. I independently decoded saved 002/008, verified lengths `[2,2,2]` against `[1,1,1]`, and executed the actual captured target row through the copied current helper with all effects trapped. It refused at the intended guard with zero copy/object/ref mutations. This is a confirmed root-reported finding, not a claim that source04 first discovered it.

My initial adapted fixture likewise reconstructed a one-space row from the source. This limitation is explicit in `HARNESS_ADAPTATION.json` and the completed reused regression 42: that synthetic row exercises implementation intent, and is **not** evidence the actual queued row works. The final independent program separately uses the actual retained008 row; it does not relabel source-derived data as actual data. Twelve per-column queued near misses refuse, and the prior claimed_solved MAIN route succeeds. Repair must use trustworthy exact placeholder evidence, retain original eligibility, and test actual captured whitespace and all near misses.

## R4-F2 — Unpinned historical authority redirects SAME release (mandatory)

The reconciler checks `prior_published_clearance_sha256` against archived FINAL_CLEARANCE and checks archive files against ARCHIVE_MANIFEST. The manifest itself is not pinned by fresh clearance. Old clearance pins scientific inputs, not subsequent publication/tracker record identities. Current receipts need only equal the archived receipts.

In independent disposable fixtures, I retained the exact old clearance/science hashes, changed both archived/current verified receipts coherently and recomputed the unpinned manifest. With fresh read-only responses for an existing duplicate record 23398176 containing the same exact pair, the reconciler accepted that record and downstream `publication()`/`tracker()` accepted it. In a separate fixture, changing archived/current `updated_range` to `'Other tab'!A7:D7` was accepted while spreadsheet properties still contained sheet 1254632077 titled Math Puzzles. The code gets whatever range the untrusted receipt says; assigning a fixed sheet_id in the accepted receipt does not establish that the cells belong to it.

These are coherent synthetic counterexamples, not observations of another real public deposit or sheet. They falsify the required SAME actual record 23398175 / DOI 10.5281/zenodo.23398175 / exact `'Math Puzzles'!A113:D113` transition. No external mutation is involved. Fresh clearance must independently bind the exact historical manifest/evidence set and exact provider/destination identities; manifest schema, membership and safe paths must also be constrained.

## R4-F3 — Evidence can drift during verification (mandatory)

After its early historical/current-receipt checks, the reconciler spends time on PR/original-QUEUE/provider inspection, two downloads, tracker properties and four-cell readback. Its last `unchanged()` checks the clearance/science/helper context, and its self-pin checks its own source. Neither refreshes the accepted archive/current original evidence.

A fixture changes archived ZENODO_VERIFIED_PUBLICATION during the first read-only GET, after the initial archive check. The transition succeeds, derives new receipt content from the earlier parsed object, then rereads the now-changed archive hash for `initial_publication_receipt_sha256`. That provenance points to bytes which were never accepted as that original object, while the final result claims `prior_evidence_preserved=True`. Another fixture changes the CURRENT publication receipt at the same boundary; replacement silently discards those changed bytes. A third shows a current PUBLISH_ATTEMPT differing from its archived original is not checked at all. This last observation supports the same evidence-preservation repair rather than creating a separate optional issue.

Preserve accepted same-byte snapshots and derive parse/hash/provenance identities from them. Verify the intended current initial receipts/intents against archived originals, and revalidate the complete immutable archive and current originals immediately before local intent/replacement. Evidence drift must abort with evidence intact, before rebinding. The shared lock controls cooperating stages; these probes explicitly simulate a noncooperating local writer and must not be confused with external provider races.

## Checked behavior and test accounting

`independent_reconciliation_probes.py` completed 49 recorded assertions/observations: 43 passing assertions (including the diagnostic actual-row refusal) and six counterexample observations grouped into the three findings above. The first completed corrected version ran 45 controls and reproduced the initial three reconciler observations; the 49-control result is its completed superset. Its normal reconciliation verifies exactly five read-only subprocess calls and two exact public download URLs, retains all archived bytes and original stage/publish intents, and binds accepted new local receipts. Stale old-clearance/self/helper/archive/current-receipt inputs refuse before provider calls. Wrong record, environment, unpublished state, provider file set, DOI version/resolution, tracker title/fourth cell and public file SHA refuse before local-write intent. Reentry refuses before calls. A normal synthetic one-space queued integration passes after the complete read-only transition; this is explicitly distinct from the actual-row failure.

Injected first and second local receipt replacement failures propagate, preserve immutable archive plus durable sticky intent, block automatic retry before calls, and leave a pair that blocks native integration before provider calls. Failure writing the final summary after both freshly verified receipts are durably replaced leaves a complete usable pair plus sticky intent and missing summary. This is documented incomplete local bookkeeping; it is not evidence of unverified publication or repeated external action. No hardware crash was simulated or durability beyond the helper's fsync semantics claimed.

`regression_workflow_probes.py` completed 42 reused controls with the required explicitly synthetic source04 seal, realistic original 14-column row and implementation-derived queued placeholder. These check source03's prior guard repairs across publication, actual public SHA pair/DOI, one tracker append, full exact native tree/body verification, ready and expected-head merge in a purely mocked workflow. They are regression evidence only. The reused transition suite was interrupted by host ENOSPC in durable directory setup and has **no completed result**. No total of 84 passing reused controls is claimed.

`FAILURE_DISCLOSURES.json` records the first test-dispatch error, the complete 45/42/49 runs, ENOSPC interruptions and timestamp correction. The initial strict read-only trap rejected a subsequent native GET; correcting test dispatch selected the already existing native mock only for that native stage. No helper/guard was weakened. An expanded run and reused transition run hit ENOSPC in disposable fixture writes. The later sequential expanded 49 run completed before the instruction to stop broad failing-version replays arrived. No further broad replay ran after that instruction.

## Local scientific and original-evidence integrity

`LOCAL_INTEGRITY_RESULTS.json` confirms all seven frozen-source pins, all 14 historical archive rows, all source03 sealed payloads, both submitted package pins plus source-manifest/TeX/metadata pins, 181 unique safe ZIP entries, all 42 native-template path/byte equalities with the ZIP, and 60/60 comparisons of the 20 Intake-pinned original files across three copies. PDF remains 90186 bytes / SHA256 `efa4617d9b3ce2091afe472eb35b5144ec30f3117ffac22dc201498f95a0b731`; ZIP remains 604537 bytes / SHA256 `ae127ebe4d8962c1fe8894db16da72a6e215ddb51a6699804b26c6ace0143290`.

At the checker timestamp, actual current FINAL_CLEARANCE and initial publication/tracker/stage/publish receipt bytes exactly equal the archived originals. Old genuine clearance intentionally fails the newly changed integrator pin, and no other helper mismatch appears. Actual verified record 23398175 and exact tracker 113 facts are retained local evidence; this review made no new provider observation and granted no publication/merge authority.

## Disposition and next acceptance boundary

All three findings remain unresolved against the exact sources pinned here. Fresh clearance must not be assembled from source04 as a clean review. Repair the exact-row, independent historical authority and evidence-snapshot mechanisms, then obtain a fresh independent supporting review that checks all required/optional findings and meaningful complete transition/regression controls. The manuscript's three accepted whole-package reviews and scientific pair remain unchanged; this report neither substitutes for them nor reopens their mathematics.

Every retained public payload, including frozen supporting source inputs and incomplete-run disclosures, is listed in AUTHORED_MANIFEST. Temporary fixtures are excluded because removed; the manifest excludes itself. Replaying the current programs after repair requires selecting the frozen input copies to reproduce these failing versions, or explicitly adapting their source locations/expectations for a newly reviewed version. Such an adaptation must be recorded and must not count reused assertions as fresh independent controls.
