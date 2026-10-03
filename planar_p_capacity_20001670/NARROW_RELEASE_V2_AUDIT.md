# Narrow re-review of correction-only release v2

Problem 20001670, rank 457. Reviewed 2026-10-03.

## Verdict: PASS

The two corrections faithfully implement the full audit's requested rigor clarifications. No new theorem-blocking issue or expansion of mathematical scope was found. The original conjecture remains **UNRESOLVED after 5/5 substantive attempts**; this correction-only review does not constitute another proof attempt. Any promotion to a solved-problem claim remains on HOLD.

## Frozen material verified

- Corrected-release manifest SHA-256: `3399f4db86a4dddcbb7ad1c5cf278c164037cf7317b12e4492a58e78900ee328`.
- The corrected public directory has exactly the manifest's 12 files. All byte counts and SHA-256 digests match.
- Original manifest SHA-256 remains `9f91143a5283e666038b1d256f7a209c4ba2e99dece5a30c86d9630b5c3f4215`. All original ten files still match that manifest exactly.
- The complete included `FRESH_ADVERSARIAL_AUDIT.md` is byte-identical to the original audit, SHA-256 `fae43a8e62fb0e6da8c7baaa4c7b166cc7fede134984cc556dabf6081385eac1`.
- Among the ten original filenames, only Attempts 3 and 5, README, and RESEARCH_LOG differ in v2. Their complete diffs were inspected. Attempts 1, 2, and 4, SOURCE_GATE, verify_constants.py, and checks.json remain byte-identical.

## Repair 1: Attempt 3

PASS. The replacement argument correctly states that the equilibrium potential equals one quasi-everywhere on K, capacity-zero exceptional sets have zero Lebesgue measure, and Sobolev gradients vanish almost everywhere on each level set. It follows that grad v=0 almost everywhere on K even when K has positive measure and empty interior. The Bregman-defect identity therefore implies the claimed integral over all of K. The inequality, coefficients, and subsequent triangle applications were not changed.

## Repair 2: Attempt 5

PASS. The expanded argument uses uniformly equivalent transformed gradient norms on a compact positive t-interval, continuity of the minimum, weak closedness of the fixed trace class, and uniqueness of the limiting minimizing gradient. For the fixed invertible transformation L_t, weak convergence plus convergence of L^p norms invokes the Radon–Riesz property and gives strong convergence. The parameter derivative is continuous, has p-growth, and passes to the limit by strong convergence and uniform integrability. These statements apply to the nonsmooth triangle and segment formulations without adding boundary-regularity assumptions. The affine identities and the unproved status of the global squeezing inequality are unchanged.

## Change map and checks

The change map accurately describes every modification and correctly distinguishes the historical full audit from this narrow re-review. README and RESEARCH_LOG preserve the partial-result scope, unresolved status, and five-attempt count. Their pending-review wording describes the frozen pre-review checkpoint; this artifact supplies the resulting verdict.

A fresh execution of the corrected release's verify_constants.py reproduces both its checks.json and checks-rerun.local.json byte-for-byte in this runtime. Its 6,145 rational cases and rational brackets remain finite/exact checks, while the continuum proof remains analytic. The gamma table remains explicitly illustrative. Byte-for-byte floating-point output across every possible Python/libm platform was not certified and is not needed for the mathematical conclusions.

No new searches, remote calls, or remote writes were performed. Neither frozen public directory nor either manifest was modified during this review.
