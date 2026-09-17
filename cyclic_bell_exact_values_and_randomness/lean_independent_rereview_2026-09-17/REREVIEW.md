# Independent re-review of cyclic Bell Lean companion v0.1.1

Date: 17 September 2026. User-requested target: `cyclic_bell_exact_values_and_randomness/lean_formalization/`.

**Final verdict: the previously identified actionable correspondence gaps are closed. No new mathematical blocker was found. The revision is suitable to share as a formal companion to the paper's principal results, with the fresh replay below now passed.** It remains deliberately short of an exhaustive translation of every analytic construction and cited external theorem.

**Fresh machine replay: PASSED.** All 1,894 named-declaration axiom checks, the clean build, validation controls and final source/dependency integrity checks passed.

## Artifact identity and regression boundary

The live source was copied into an isolated snapshot before review. [source_snapshot.json](source_snapshot.json) records the repository commit and content hashes. The bundled manuscript remains byte-identical to canonical `main.tex`, SHA-256 `82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71`.

The ready-to-share archive `cyclic-bell-lean-review-r2.zip` has SHA-256 `4278c3dd68fc05aad5e0dadf8eede36d6a6e8ff47d49aeccfc1288e7cb780ef5`. Every one of its 226 manifest entries passed, and all archived files other than the archive-only manifest match the reviewed source snapshot byte-for-byte. See [archive_check.json](archive_check.json).

All **104 old mathematical modules** are byte-identical to the previously audited delivery. The existing axiom-query module changes only to include new declarations; four new source files are added. The root import exposes the new completion statements. Neither physical model definitions, Bell coefficients, old theorem hypotheses, toolchain pin nor dependency manifest were weakened or replaced. The reproduction runner itself is unchanged. See [delta_check.json](delta_check.json).

The review combined coordinator inspection with three independent AI-assisted tracks: moments/residuals, convention transport, and adversarial scope/regression. This is not external human peer review. The previous full-paper audit remains relevant to the unchanged mathematical modules; the new work received direct source review rather than acceptance based on package self-reports.

## Resolution of the earlier findings

| Previous finding | Revised evidence | Disposition |
|---|---|---|
| Full second-family complex correlation matrix not assembled | `GeneralSecondMoments.lean` proves every reduced entry `lambda_l chi(-ly)`, every extra-input entry `delta_(l,0)`, all local first moments, and equality of complete arrays derived from actual Born probabilities. | Closed |
| Bob-adjoint/outcome-inversion bridge missing | `GeneralOutcomeRelabeling.lean` proves PVM outcome inversion gives the encoded adjoint, physical probabilities transform by b↦−b, and **both** the Fourier and added terms of the Bell functional are transported. | Closed |
| All-dimensional second-family residual annihilation not stated explicitly | `GeneralSecondResiduals.lean` proves the literal `d lambda_l I - A_l tensor Bhat_l` residual and aligned residual annihilate Phi_d, using compression and unitarity without a maximality premise. | Closed |
| Claim ledger contains obsolete scope descriptions | Updated rows point to the actual commuting closure and source canonical-polar bridges; new rows map the completion modules. | Closed |
| General arbitrary polar-decomposition infrastructure outside Lean scope | The same explicit boundary is retained; no unsupported claim that it has been constructed was added. | Disclosed scope boundary, not a main-bound defect |

### What the new statements actually establish

The first-harmonic matrix endpoints quantify every d≥2, every phase permutation, all d Alice inputs, and all d+1 Bob inputs. The row label l is an Alice input, not a claim about every Fourier order. The statements neither assert invariance of the full probability table nor contradict its nonuniform target behavior. Expanded contracts in `GeneralSecondCompletionStatements.lean` expose the literal double sums over Born probabilities and actual density traces, avoiding a synthetic array defined to equal the desired answer.

The residual theorem uses lambda_l itself, not its complex conjugate; conjugation belongs in the scalar Bell functional. This matches the manuscript's SOS. It is a true vector equation, derived from the actual physical encodings and the unitary maximally-entangled-state identity. No zero-residual, scalar-attainment, or maximality hypothesis has been introduced.

The relabeling theorem changes a PVM's outcome labels, leaving state and Alice measurements intact. Its Fourier identity correctly identifies the adjoint combination with the **opposite Fourier mode's** adjoint. The universal finite-dimensional comparison uses the transported functional on both competitor and witness. Observed-maximum and best-fixed-guess statements are carefully scoped: they do not claim an exact Eve-optimal or value-conditioned worst-case guessing probability. The new alternate-convention module does not advertise a new formal q/qa/qc supremum endpoint; its finite witness/transport statements cover the manuscript sentence that required repair.

Detailed evidence: [moments and residuals](moments_residuals_review.md), [relabeling](relabeling_review.md), [scope and regression](scope_regression_review.md).

## Independent finite sanity check

A separate calculation from the manuscript's matrix formulas checked dimensions 2 through 8, including composite dimensions. It confirmed every complex correlator, the extra column, literal residual annihilation, and transported score to floating-point tolerance. Maximum residual errors were below 2e-14. For d=4, the original score was 5, adjointing Bob while keeping the original functional gave 0, and transporting the functional as well restored 5. The d=2 exception behaved correctly.

This is supplementary numerical evidence and a check on the interpretation of the new transport theorem, not a proof or a replacement for Lean. Reproducible [calculation](numeric_convention_check.py) and [results](numeric_convention_check.json) are retained.

## Fresh machine verification

A fresh isolated run `20260917T145943171483Z` passed in 936.8 seconds. It executed 66 recorded commands and rebuilt all 110 project Lean source files. Lean 4.19.0 and the exact pinned dependency revisions were checked before and after the run.

All 1894 declaration reports were present and used only `Classical.choice`, `Quot.sound` and `propext`. No unproved placeholders, custom axioms or native-trust shortcuts appeared. All five acceptance controls compiled; twenty deliberately invalid proof attempts failed in their designated proof bodies rather than due to syntax, import or resource errors. These negative controls are checking-tool regressions, not independent proofs of negated propositions. The expanded Statements module compiled, and protected-source, manuscript and dependency integrity checks passed.

The 63 runner/tooling tests and 24 packaging tests also passed. The new modules and expanded completion contracts are part of the normal import graph and the fresh axiom inventory, not unbuilt auxiliary files. The live source and r2 archive were confirmed unchanged after this review.

Evidence: [summary](reproduction/summary.json), [complete fresh receipt](reproduction/20260917T145943171483Z/run.json), [fresh build/axiom log](reproduction/20260917T145943171483Z/022.log), [runner tests](tooling_runner.log), [package tests](tooling_package.log), [final live-source integrity](final_integrity.json).

The clean replay uses the pinned Lean compiler and clean pinned upstream dependency sources with copied dependency caches. It rebuilds the entire companion from a cleared project build directory. It does not independently rebuild Lean or every Mathlib dependency from source. The axiom audit checks the encoded statements within that normal trust boundary; the source correspondence review is a distinct part of this verdict.

## Remaining scope and one minor documentation correction

The general polar positive-factor identity still accepts a factor satisfying the actual factorization and initial-isometry equations. Arbitrary canonical-polar existence, uniqueness, von Neumann algebra membership and strong-limit construction are not separately formalized. The main first-family arbitrary-Hilbert bound is proved independently without assuming this construction, and the source attaining matrices have an explicit canonical-polar construction. Thus this boundary does not reopen the earlier principal-result finding.

The package also appropriately does not claim to formalize cited external self-testing theorems, research novelty, or every intermediate derivation. Different valid proofs of coefficient normalization, support rigidity and the MUB obstruction remain acceptable.

One **nonblocking navigation error** remains: the settings row in `COVERAGE.md:88` lists `standard_behavior_formula` under `GeneralPhaseTables.lean`, but it is actually declared in `GeneralPhaseBounds.lean:168`. The theorem is present, imported and verified; this is a documentation link issue only. No reviewed source was edited to fix it, preserving the exact artifact under review.

## Sharing recommendation

After the successful fresh replay recorded here, share the r2 archive as a **Lean formal companion covering the principal results and explicit constructions**, with its coverage guide. Do not label it a proof of every line, all background analytic infrastructure, or the cited literature. The earlier missing second-family statements no longer justify holding the package back.

The follow-up draft should communicate that scoped result, direct Ignacio to the reproduction instructions and coverage map, and invite feedback by email. No external message has been sent.
