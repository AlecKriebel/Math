# Corner-weighted quadrant loops: partial results and a refined positivity counterexample

Problem ID 30002547, catalog identifier OWR-12872-018. Target: Albert–Bousquet-Mélou Conjecture 11. Prepared 2026-10-20 UTC.

**Full-target status: UNSOLVED after five attempts.** The arguments here do not settle the two open parameter intervals (-1,-1/2) and (-1/2,0). This is the scope of this package, not a certification of the current literature's status.

## Exact model

Q_n(a) sums a^c over all 2n-step square-lattice walks from the origin back to the origin that stay in the nonnegative quadrant. The statistic c counts only consecutive NW and ES pairs in the linear word, with no last-to-first seam. The variable u in Q(a,u) marks half-length n. Parameters a are fixed real numbers at least -1; negative weights are signed sums.

## Accepted results

- For every a>=0, the radius is exactly (2+sqrt(2+2a))^(-2), and the ordinary coefficient root limit exists.
- For -1<=a<0, the radius is at least the conjectured piecewise value, with an explicit absolute-coefficient upper bound. The one-sided Abel value at the proposed spectral threshold is finite.
- At a=-1/2, the radius is exactly 1/9, the critical Abel value is 3/2, and the first derivative tends to positive infinity.
- The stronger fixed-vertical assertion (P2) in ABM Section 6.3.1 is false. At vertical projection N^13 S^13 and horizontal half-length 2, the exact polynomial is 13769+27300a+13741a^2 = 210-182(a+1)+13741(a+1)^2. This does not disprove Conjecture 10 or Conjecture 11.
- Displacement-preserving fixed-length nonnegative local blocking cannot exactly represent this signed model for any a<0. An exact Hilbert-space projection formula identifies the critical Abel value on the lower conjectured branch.

The a=-1 radius was already known from ABM Proposition 17. No novelty or priority claim is made for the partial results here. The bounded source search did not verify a full-range resolution; it was not exhaustive.

## Reading order

1. [SOURCE_GATE.md](SOURCE_GATE.md): exact historical target, conventions, known cases, inspected primary sources, and search limitations.
2. [RESULTS.md](RESULTS.md): five-attempt mathematical summary.
3. [ATTEMPT_1.md](ATTEMPT_1.md) through [ATTEMPT_5.md](ATTEMPT_5.md): complete authored arguments, including explicit failed-route boundaries.
4. [ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md): claim-by-claim audit scope and unresolved gaps. Five accompanying audit reports check the mathematical arguments.
5. [REPRODUCIBILITY.md](REPRODUCIBILITY.md): exact finite controls and independent isolated replay. [REPLAY_VERIFICATION.json](REPLAY_VERIFICATION.json) contains all checker stdout and script hashes.
6. [MANIFEST.json](MANIFEST.json): package inventory, byte counts and SHA-256 hashes. [SOURCE_VERIFICATION.json](SOURCE_VERIFICATION.json) records source-PDF metadata only, not source files.

## Reproduce

Use Python 3.10 or later; only the standard library is required.

    python3 -I verify_manifest.py
    python3 -I run_checks.py

The replay copies explicitly allowlisted checkers into a fresh temporary directory and uses Python isolated mode. It needs no source documents, datasets, network, credentials, or third-party packages. All computational checks use integers or exact rational numbers. They are finite normalization/algebra controls, not numerical proofs of the infinite analytical claims.

## Publication scope

This package contains authored mathematical arguments, audits, acceptance and reproducibility reports, exact verification scripts/results, and public bibliographic/verification metadata. It contains no copied source documents, source extractions, dataset contents, private sources, or private coordination files. No external publication is performed by any included script.
