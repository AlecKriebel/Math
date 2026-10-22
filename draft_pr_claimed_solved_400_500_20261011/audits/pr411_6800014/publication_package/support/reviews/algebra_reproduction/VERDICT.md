# Algebra reproduction verdict: PR 411 / 6800014

**PASS for the mathematical claim and original Attempt 2 proof.** At pinned head `ac8b960bdda61c154cc30d7e3aba70389a9b139e`, every fixed `0<u<1/2` has the claimed non-strict all-left-invariant-metrics local maximum `F=1/3`, fails the fixed Lie algebra solvsoliton equation, and admits a larger-value same-group metric. No mathematical repair is required. Native author status remains `claimed_solved`, and author proof-search turns remain exactly `2/5`; this audit adds zero author proof-search turns.

The independent criteria, generic Koszul derivation, exact Hessian, complete orbit chart/Taylor proof, non-solvsoliton obstruction, and distinct comparison witness were sealed at 2026-10-13 01:13:56 UTC before any author proof/checker/historical-audit read or peer verdict. The decisive transverse gap eigenvalues are `16(1±2u)` (each twice) and `128(2−u²)` (twice). A complete twelve-dimensional conjugacy chart and exact constant-value parameter family handle the flat directions. The independent comparison has `F=625/1587>1/3`; the original author's distinct comparison `9/17` also checks exactly.

All nineteen receipt files match byte size, SHA256, and Git blob SHA1. All eighteen publication-manifest entries and six frozen-author hashes match. Current and frozen main proof, verify.py, and check_hessian.py are byte-identical. Each file's semantic inspection is recorded in INVENTORY_REVIEW.json. Historical corpus hashes, original search coverage, original pre-layout script bytes, and historical execution environment were not re-created; those provenance claims are not premises of the mathematical proof.

The original proof's generalized-zero-eigenspace orthogonal normal form covers all nearby conjugates. Its entire lower-left coupling block is retained. Its exact quadratic and remainder identities are correct; the uniform compact-interval estimate supplies the required neighborhood inequality. The reduction from all inner products on the fixed algebra to scaled conjugates is valid even with cross terms in the metric. At u=0, F is undefined; at u=1/2, the supplied proof does not decide local maximality. No excluded endpoint was silently included.

The accessible original [Morgan–Pansu Question 14, §11](https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf) asks about local maxima on left-invariant metrics and the equation Ric=cI+D. [Lauret–Will I, §6.4, printed p.20](https://arxiv.org/pdf/1808.01380v2) already displays the exact D_t family and its value 1/3; its preceding discussion leaves the small-parameter local maximum issue open. This audit does not certify novelty or the current inaccessible aggregator wording.

## Executable verification and trust boundary

Forty-two authentic isolated executions used private copies and private Python 3.14.6 / SymPy 1.14.0. The five executable paths (current verify.py, current check_hessian.py, audit/independent_checks.py, and both frozen author scripts) all returned zero under normal and optimized Python from both their copied publication directory and a foreign directory: twenty baseline executions. Outputs match across mode/cwd for each distinct script. The source snapshot was rehashed after all tests and remains unchanged.

| Controlled fixture | Normal execution | Optimized `-O` execution | What it establishes |
|---|---|---|---|
| False exact algebra assertion, each of five checker paths | All five fail | All five exit zero and print success/verification | All validation relies on removable `assert` statements |
| Frozen proof bytes tampered, audit checker | Fails | Exits zero and prints hash PASS | Frozen hash validation is also removed by `-O` |
| Current theorem falsely extended to `0<u<2`, all five checkers | All five exit zero | Baseline optimized validation already absent | Scripts do not bind current theorem prose to the checked identities |
| False publication-manifest claim and hash, all five checkers | All five exit zero | Baseline optimized validation already absent | Scripts never validate the current publication manifest |

The false extended interval is demonstrably false: the independent Hessian has increasing-F directions for u>1/2. The controls do not refute the actual theorem; they delimit what a printed checker PASS certifies. Normal execution substantively verifies the exact algebra. No one should promote `-O` output into evidence of validation. The author's verify.py explicitly leaves analytic coverage as a textual obligation, and this audit independently discharged it. The historical checker gaps require no repair to the theorem, but are reproducibility hardening opportunities: preserve normal execution instructions, use explicit exceptions for mandatory validation, and validate current public-file hashes if executable packet integrity is intended.

The private raw outputs, copied nineteen-file source trees, mutated fixtures, environment, caches, and third-party materials are excluded from the positive publication whitelist. The public files contain original audit text, original check code, integrity metadata, and summarized results only. No external communication, repository/index/branch mutation, live PR write, push, merge, release, or outreach occurred in this family.

Exact remaining mathematical gap: **none for the stated open-interval counterexample.** Remaining non-mathematical limits: no novelty certification, no live aggregator content certification, and bounded provenance reconstruction as stated above.
