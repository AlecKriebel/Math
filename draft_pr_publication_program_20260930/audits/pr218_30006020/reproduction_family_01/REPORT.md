# Independent computational and reproducibility audit of PR218

Audit date: 2026-10-18 UTC. This report concerns the authenticated published package and its finite mathematics. It makes no case-completion, novelty, universal-priority, human-review, publication-clearance or provider-state certification.

**Finding:** No substantive arithmetic, finite-model or reproducibility defect was found. The published finite counts reproduce exactly, and distinct new computations support the transcription and finite algebra. These computations do not replace the analytic proof or the cited geometric theorems.

## Input custody and package correspondence

The two assigned source pins matched before scientific execution:

| Input | Bytes | SHA-256 |
|---|---:|---|
| `ROOT_NATIVE_CUSTODY_ACCEPTANCE_01.json` | 7,054 | `4b4deaed33b198a3e9814a46536108eed5c49cc26ff81975afd760b464d9e663` |
| `authenticated_sources_01/SOURCE_MATERIALIZATION_MANIFEST.json` | 276,014 | `16abd824d189596e2bb54101af72c2c1046a1f0d17a70ba130a019495226965d` |
| Exact published PDF | 96,674 | `ad3a7dcbbcdb9a7c53bd1e63085644434132a556c9a09e8a1c16121073949f02` |
| Exact published verification ZIP | 275,698 | `cfe1d84ff7f50cdfcc2682eab618aab495838de549bb4a2e24c26abcbe798810` |

All 391 materialization entries matched their byte counts, SHA-256 hashes and native blob identifiers, computed directly without Git commands: 22 original, 30 current and 339 coherent-Main entries. This is body integrity relative to the already authenticated manifest; it is not a new claim about provenance beyond the recorded custody boundary.

The ZIP was safely extracted into the owned audit folder. It has 138 regular payloads totaling 619,375 uncompressed bytes. There are no duplicate names, absolute/traversing paths or symbolic links. Every one of the 137 payloads listed in root `PACKAGE_FILES.json` matches; the only excluded payload is that manifest itself. Every one of the 16 sealed `verification/PACKAGE_MANIFEST.json` payloads also matches.

The ZIP TeX matches authenticated final native `preprint/cylinder_areas.tex` exactly, SHA-256 `7da26974ef1e8b15922bff398424954874177d20580cf5b0526cd998e34de6b8`. All 22 archived original-submission bodies match the original attempt. Both current-source manifests and every listed current/original/frozen-preprint hash verify. The ZIP `current_source` has 28 files and exactly matches the dated prepared `preprint/pr_update/30006020` snapshot. Against the later 30-file native current attempt, five administrative files differ and two publication/acceptance receipts have been added. The candidate from section 1 onward is byte-identical; sections 3–9 are byte-identical among original, ZIP and native candidates. Those are honestly documented preparation-versus-release status changes, not a mathematical discrepancy. ZIP metadata, native metadata, and `deposit.json`'s metadata object agree.

Evidence: `INPUT_PINS_01.json`, `SAFE_EXTRACTION_AND_MANIFEST_01.json`, `WHOLE_PACKAGE_CORRESPONDENCE_01.json`, `NATIVE_BODY_AND_CURRENT_MANIFEST_VERIFICATION_01.json`.

## Actual replays and their meaning

The final TeX, current proof and checker sources were read before inherited review verdicts. Programs were executed with active assertions and isolated output locations. All mathematical programs ran unmodified; programs writing beside themselves were first copied to owned scratch. Full commands, interpreters, working directories, source hashes, timing, standard output and return codes are recorded in the receipts.

| Program or family | Reproduced result | Evidentiary scope |
|---|---:|---|
| Portable final wrapper | PASS; 7,100 counted rational assertions; 123 separate DVV composition cases | Exact receipt regression and sealed-payload integrity |
| Original author checker / final identical author control | 3,439 assertions each | Ordered compositions to size 10 for height truncations 1 and 2; algebraic factorial/marking/prefactor checks |
| Original independent checker / final identical partition control | 2,032 assertions each | Full zeta weights after cancelling common pi powers; partitions to size 14; selected moments and Beta-window means |
| Final labelled-permutation control | 1,629 assertions, all 46,233 permutations of sizes 1–8 actually traversed | Cycle-type counting and all ordered selectors through order 3, including repeated sizes |
| Final DVV control / archived geometry checker | 123 ordered compositions, genus 2–5, at most three loops | Rational low-genus source-expansion algebra; the same DVV oracle appears on both sides of several coefficient identities |
| Original SciPy model diagnostic | Three means and coefficient diagnostics reproduce within ordinary floating differences below `4.5e-16` | Nonvalidated ideal-model floating diagnostics only |
| Archived assembly audit | 422 selectors, including 261 repeated-size selectors; 1,225 prefactor comparisons | Exact finite algebra, plus separately labelled floating asymptotic diagnostics |
| Archived Gamma diagnostic | PASS; 15 finite-size/scale cases; factorial-identity discrepancy at most `2.220446049250313e-16` | Ordinary floating diagnostics, not error enclosures |
| Archived fixed-type scope control | 115 rational comparisons | Beta identity for a different conditional model; not evidence about the full geometric mixture |
| Native manuscript-review 01 checker | 114 exact assertions | Finite compositions and two-coordinate Dirichlet rectangles |
| Native manuscript-review 02 checker | 4,466 exact assertions | Finite Poisson/composition normalization, selectors and prefactors |

The first three distinct final control totals are exactly `3439+2032+1629=7100`. Replaying identical historical and final copies does not create additional independent evidence. Neither 46,233 traversed permutations nor 123 DVV compositions is silently added to the 7,100 assertion count.

The original diagnostic ran with the already available Python 3.9.6, NumPy 2.0.2 and SciPy 1.13.1. Its historical receipt names NumPy 2.3.5 and SciPy 1.17.0. The reported mean differences are 0, `2.220446049250313e-16` and `5.551115123125783e-17`; the coefficient differences are at most `4.440892098500626e-16`. These are empirical cross-environment comparisons, not certified rounding-error bounds. No packages were installed.

All 12 mathematical program entries in the exact public ZIP were executed. The remaining five Python entries are four historical source-retrieval/report-finalization scripts and one optional historical provenance helper with old absolute subject/private paths. They were not executed as mathematical controls. No source-retrieval script, publication mutator, provider/tracker operation or Git command was run. `CHECKED_PROGRAM_SCOPE_01.json` lists every one of the 17 ZIP Python entries and its classification.

Evidence: `REPLAY_RECEIPTS_01.json`, `EXTENDED_REPLAY_RECEIPTS_01.json`, `MANUSCRIPT_REVIEW_REPLAY_RECEIPTS_01.json`, `SCOPE_CONTROL_REPLAY_RECEIPT_01.json`, `NUMERICAL_DIAGNOSTIC_COMPARISON_01.json`.

## Wrapper falsification controls

The documented standard-library entry point also passes on Python 3.9 and when the invoking process has `PYTHONOPTIMIZE=2`; children still run with assertions active because the wrapper supplies `-I` without `-O`. In separate owned copies, it correctly rejects an altered control, altered expected receipt, manifest path traversal and duplicate manifest entry. These checks test accidental alteration and the documented local integrity boundary. They do not prevent an attacker from rewriting both code and manifest, which the package already explicitly acknowledges.

Evidence: `WRAPPER_ADVERSARIAL_RECEIPT_01.json`.

## Additional independent exact computation

`independent_controls_01.py` implements two distinct finite mechanisms detailed in `INDEPENDENT_DERIVATION.md`:

1. A translated-simplex lower-threshold formula, followed by inclusion-exclusion, computes arbitrary integer-Dirichlet rectangles. It covers rectangles crossing the sum-to-one boundary, selection of every component with zero residual shape, and the one-cylinder atom. It agrees with 144 separate Beta/order-statistics marginal evaluations and explicit singular-face reference cases. It gives complete exact normalized-count distributions for model sizes 1–8 in two windows, with nonnegative probabilities summing exactly to one. Ordered selected-assembly formulas independently agree through order three. The assembly comparison shares this new probability kernel; it is not falsely described as a second probability oracle.
2. A first-KdV plus string recursion, anchored by the genus-zero multinomial formula, computes intersection numbers without the published DVV factors. It matches the pinned DVV evaluator on 244 degree multisets in genus 0–4, and matches one-point closed forms through genus 10. The published evaluator is loaded only as a final comparator, not as an input to the KdV calculation. Top-level published assertions, loops and file writes are excluded.

There are 1,158 successful rational assertions. This includes both a comparison and a separate positivity assertion for each of the same 244 correlators; it is not 1,158 independent mathematical results. All 16 complete model count distributions and the family counts are in `INDEPENDENT_CONTROLS_RECEIPT_01.json`.

## Adversarial verification of the new checker

A separately assigned adversary independently derived the shifted-simplex formula and implemented direct convolution of truncated polynomial densities. That different probability mechanism agrees on 2,032 rectangle comparisons and 889 survival comparisons across 127 integer-shape parameter families, including odd shapes, zero-width windows, atoms and selection of every component. A direct count-generating polynomial, without factorial moments or their inversion, matches every coefficient of all 16 new model count distributions. The adversary also proved the KdV evaluator's well-founded rank and checked 10,395 valid recursive edges; no computational DVV circularity was found. The original receipt replays exactly apart from timestamp.

The adversary correctly notes that count-distribution normalization and moment reconstruction are algebraic consequences of the inversion, not separate probability oracles. Its independent direct-convolution comparisons are the additional corroboration. It also found unsupported-input behavior: the internal lower-threshold helper does not reject negative thresholds, and for example returns `3/4` for total 3, selected shape 2, threshold `-1/2`, whereas the true survival is one. The declared formula requires nonnegative thresholds; every submitted call has endpoints in `[0,1]`. This is an out-of-domain helper-hardening limitation, not an invalid submitted result. No frozen checker was modified.

The adversary report, code, receipt and finite artifact pins are in `independent_control_adversary_01/`. Its `AUDIT_RECEIPT.json` SHA-256 is `25303a7c8cd4f56575eeb18b377d1449e912c242b9a1a022a7ba798f495c02f9`; its artifact manifest SHA-256 is `8d89c28cd30bfeea19f4d44ff153b252ca0101497a5dd306ec416c5439fd1020`. These pins were verified directly before inclusion here. This is internal computational review, not human peer review or an asymptotic theorem certificate.

## Findings and limits

No substantive defect was found. Two details matter when interpreting the evidence:

- Historical comment imprecision: `verification/controls/partition_exact.py:64` says “All ordered triples of labels,” while line 65 enumerates all single labels, all pairs, and diagonal triples only. It does not enumerate arbitrary mixed triples. The final labelled-permutation checker separately enumerates every ordered triple through size 8, and the package's coverage table does not make the inaccurate historical-comment claim. This is a preserved descriptive nit, not a theorem or announced-total error; no frozen file was changed.
- The author checker's 2,046 `simplex_monomial_factor` assertions at `verification/controls/author_exact.py:54`–57 verify factorial cancellation after inserting the simplex formula. They do not independently integrate the simplex. Similarly, many DVV coefficient identities reuse a single intersection oracle. The package accurately calls these finite transcription/algebra controls. The independent shifted-simplex and KdV checks address those finite-oracle limitations, without eliminating the larger analytic obligations.

The written proof was also checked for the relevant separation of bounded-observation total variation from unbounded moment transfer, Gamma versus normalized-Dirichlet marking, arbitrary slow `q -> infinity`, the shared Gamma total, and the order of limits. No contradiction with these finite calculations was found. The theorem still requires the correctly applied positive geometric expansion, uniform large-genus intersection bounds, exceptional-graph bounds, coefficient asymptotics, Gamma tail estimates and uniform-integrability argument. Finite computations cannot prove those uniform statements, establish the full geometric dictionary, determine priority, certify unavailable announced work, or resolve the explicitly reserved `4g-4` versus `6g-6` microscopic discrepancy. Other strata, primitive-cover ensembles, diagonal sampling and endpoint scales remain outside the checked claim.

All retained audit artifacts stayed in this audit family. The unmodified portable wrapper also used automatically deleted isolated temporary directories, as its implementation specifies. The frozen/authenticated/public files, Git state, provider state and tracker were unchanged. This bounded computational review does not mark the overall case complete.
