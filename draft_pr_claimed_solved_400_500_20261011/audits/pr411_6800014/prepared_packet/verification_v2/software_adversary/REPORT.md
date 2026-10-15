# Independent software adversary: PR411 / 6800014, verification v2

Frozen report UTC: 2026-10-13T02:26:24Z.

**Verdict: PASS for the reviewed v2 software component; zero identified software blockers. Final post-incorporation custody replay remains required.** This independent review tested the provisional 68-positive-file / 70-total-file bundle, not a future seal or parent acceptance. The three frozen review outputs will increase that inventory to 71 positive / 73 total files. Any final prose/metadata synchronization must be resealed and checked in both modes with the reviewed code unchanged.

## Scope and native gate

Fresh native read-only [PR411](https://github.com/AlecKriebel/Math/pull/411) and its branch-ref resource confirmed open, draft, unmerged; head/ref `ac8b960bdda61c154cc30d7e3aba70389a9b139e`, branch `research/ricci-pinching-6800014`. Independently parsing the actual [exact-head QUEUE header and row](https://github.com/AlecKriebel/Math/blob/ac8b960bdda61c154cc30d7e3aba70389a9b139e/unsolved_math_prioritization/QUEUE.md) gave rank 444, ID 6800014 / AMR-067-0014, status `claimed_solved`, author turns 2/5. The native QUEUE bytes match Git blob SHA1 `81f397cb34eeb6ce1d3c828992abc0969ab2d74d` and SHA256 `0a7d24f03ae65b0e7ef87cd4be265b9229666323e9c1e66ae404542d30864f02`.

This is software, custody and source/prose metadata consistency review. It neither re-proves the central analytic argument nor independently repeats the underlying literature search. No Git/index/branch/PR/QUEUE/Sheet/Zenodo write or external communication occurred. All runtime files, mutated fixtures and raw evidence were created under this reviewer's private source directory. No public reports existed during execution.

## Exact code relation and evaluation behavior

The complete v1/v2 `run_all.py` source diff contains exactly two substitutions: positive-whitelist schema v1→v2, and `SOURCE_AUDIT.md` added to the allowed source-prose change set. The complete resulting AST also agrees. Existing strict symlink and nonregular-entry rejection remains intact. `guard_relation.py`, `run_checked.py`, and `reproduce_controls.py` are exact released-v1 bytes.

All three current mathematical checkers are exact v1 bytes. Independently reversing every mandatory failure branch to its original assertion reconstructs the complete original module AST, including every predicate, statement and definition; the original assertions have no messages. There are 19/2/18 static predicates. Fresh normal and optimized instrumented executions reach every label with exact per-label counts matching the reference: 24/2/28, total 54 per mode. Every regenerated stdout hash matches the recorded reference and fresh normal executions of the original three scripts:

| Script | Static predicates | Evaluations per mode | Exact stdout SHA256 |
|---|---:|---:|---|
| verify.py | 19 | 24 | aa68709f04bcc99385fc8bed3ecde90ffdd3a02cb75436278088c8e45b40b074 |
| check_hessian.py | 2 | 2 | ce230da403b678baa6622dff3adcfdd93e23ffaf3d3df7939f88ae6cc792f3c5 |
| audit/independent_checks.py | 18 | 28 | 70f1d48ea77c1c63fa9fec00c8c435db6fcf771e1031f2973300ff0f14408d15 |

Eight synthetic native-assert comparison cases cover true/false/throwing `__bool__`, `__len__`, false-and and true-or division traps, and stateful and/or branches. Guarded and instrumented normal/-O runs retain the native event sequences, predicate evaluation count, truth-conversion behavior and exception type. Instrumentation wraps the predicate value and returns it unchanged, leaving the guard's original `not` to perform truth conversion. It does not eagerly coerce values to `bool`.

Python 3.14.6, SymPy 1.14.0; all child executions use bytecode suppression. Historical frozen/original `-O` assertion successes remain **NOT CERTIFIED**.

## Independent controls

The unchanged native 38-control harness was independently executed from a private immutable copy of the authenticated provisional bundle. All 38 expected outcomes and required diagnostics matched. This includes fresh positive-whitelist archive extraction into a relocated path with spaces; foreign working-directory baseline; prose/proof/manifest, frozen/original metadata and candidate-script corruption; extra/missing files; unlisted FIFO; whitelist corruption; directly false predicates in all three scripts under both modes; direct frozen corruption; lazy truth traps; and a changed predicate with candidate/publication/whitelist/seal hashes recomputed. The latter still fails the exact full-AST relation.

Supplementary testing ran 65 child executions: 51 independently listed replay/guard/special-entry/truth checks, eight native-assert baselines, and six additional instrumented failure-event checks. Thirteen direct function probes additionally reject non-string/empty/noncanonical/absolute/traversal/missing paths and duplicate/incomplete manifest entries. Listed FIFO, listed and unlisted Unix sockets, inside/outside file symlinks, directory symlink and dangling symlink all fail promptly in normal/-O with the expected strict-entry diagnostic. No hang or acceptance was observed.

The supplied public `TEST_RESULTS.json={}` and `NATIVE_VERDICT=PREPARATION` were preparation placeholders during this review. They were not treated as evidence of successful v2 replay. Independent successes are native runtime results retained privately, separate from historical-v1 records.

## Complete custody and source/prose consistency

The independently authenticated provisional whitelist SHA256 is `071c85ae582166c83bb2726b30f3d8ef95f0acf6b06ef08b75a438adbf819455`; its actual seal SHA256 is `cb6ab87ef7b04b43057505964d64837e4f6507a1ac9dcabdefa9f904a9af392e`. Complete inventories and every positive entry's size, SHA256 and included Git blob SHA1 agree. After all provisional executions, all 70 files remained unchanged.

The original 19 objects agree with the native-source receipt, preserved source snapshot, and released-v1 originals. The current 19 agree with `global_candidate_v2/author_packet/`; their publication manifest binds every other 18 files. Exactly eight original-relative paths differ, matching V2_DERIVATION. Exactly five current prose/metadata paths differ relative to v1. Both proofs, the historical full mathematical audit, frozen metadata and all six frozen files remain exact. Current SOURCE_AUDIT/README end in their complete prior text; editorial map/research log begin with their complete prior text.

All 55 released-v1 files and its complete positive whitelist remain unchanged; actual v1 seal SHA256 `28ffa75ad2854db27f5793f28421fc3f041bedf3dcd7708e2f5bca0d944552c5`. Selected historical reports/code/native results/seal objects match their original sources exactly; the derived historical binding receipt independently agrees with all 55 objects. The copied case-root parent acceptance is v1 context only. Authentic earlier failures, findings and original native conclusions remain preserved.

Selected priority-context authored copies match the separately preserved erratum artifacts exactly. Its actual separate seal is `69a23fca7351c1d9cc1367e1a8d9d7b69e44b0e9bf47c27b9886372aaf9306ca`. They are explicitly partial authored context, with companion references to the separate original review. Neither full third-party source custody nor parent priority acceptance is inferred from these copies.

The current addenda consistently identify inspected I v1(2018-08-03), I v2(2019-05-09), II v2(2019-11-27), and inaccessible/unattested final journal texts. They credit the exact 2018-07-23 existence announcement before both I revisions, without inferring withdrawal, falsehood or a journal correction. They label the old queued0/5,403, corpus and research-gate statements historical; fresh exact-head state is claimed_solved2/5. Current aggregator wording/status is unverified; the429 is expressly a root-reported access observation.

The bounded first priority review is identified as 40 issued queries, 13 successfully downloaded primary PDFs and PASS_QUALIFIED, with a separately sealed bibliographic-label erratum. Novelty, first assertion, first proof and current community-open status are withheld. The literal fixed-group Question 14 distinction is preserved even though the metric is a Ricci soliton on the alternate presentation. The corrected displayed E_t expression `25t^4/(59t^4+32t^2)`, E1=25/91 and E2=25/67 consistently supersedes the printed/provisional error; the distinct original 9/17 witness is unchanged. Omission wording concerns the author 19 only and permits separately prepared authored preprint artifacts under explicit parent custody. No unavailable-paper filename is introduced.

The old `fresh_main_base`, `queue_change` and `software_guard_update` manifest fields are historical v1 values; their dated source-update and pending-v2 fields currently bound that interpretation. Explicit historical field relabeling is a sensible final metadata clarification, retaining exact old values. This report does not pre-certify the final edits: their synchronized bytes/manifest/whitelist/seal and explicit no-v2-queue-mutation/current-runner-review wording must be checked at the final custody stage.

## Trust limits and remaining completion condition

The runner binds reviewed bytes, not arbitrary prose semantics. A simultaneous attacker replacement of code, whitelist and externally authenticated seal lies outside the unkeyed-integrity threat model. The whitelist deliberately omits only itself and its seal; the seal binds the real whitelist digest, and its real digest is authenticated separately. No self-hash cycle or future own-report seal hash is claimed.

Historical standalone manifest `f5446c816081c5322e4279bcd9a61dca5bfb63cfacf69d105d1587ed9d93b7fb` and pre-layout checker `eccde3c2a903b1fca0f232e7e392d537479ddd3936281a37e87c4f7e7047be97` remain **UNATTESTED**. Checking the included frozen files does not attest those absent objects. No mathematical repair, new author proof-search turn, human peer review, novelty, publication acceptance or whole-preprint acceptance is certified.

These three public files are **FROZEN**. The precise outstanding condition is final incorporation/current-metadata inspection and independently authenticated 71-positive/73-total normal/-O integrity replay, preserving all seven reviewed executable bytes. Later complete preprint-package adversaries remain separate.
