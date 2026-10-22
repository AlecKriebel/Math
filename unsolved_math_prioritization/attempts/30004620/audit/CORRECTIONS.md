# Corrections and qualifications

## Required provenance addendum

The frozen author provenance records the statement hash but omits the catalog review hash. Without changing the freeze, this audit supplies:

- review SHA-256: `b3f0019b864f0700a2943a882d9f11eef9e98dcee2299462ab55eabab2486fe9`
- statement SHA-256: `66d79ee91479b1e8c8ca329adeaca6e27a8a54ea1cafd98a6a35f905b578cff9`
- identity: problem 30004620, OWR-4990375-013, rank 782
- review serialization: SHA-256 of Python `json.dumps([complete_problem_record, exact_key_prior_research_or_empty_dict], sort_keys=True).encode()`

The exact-key research record is absent, so its second component is the empty object. The recomputation matches the full descriptor. The public queue implementation independently confirms this serialization; its verified Git blob SHA is `e646cfc1a3b9653879777e4e1215e9a1043f3a3d`. Verification code and machine-readable results are included. Any later repository update must recheck current identity rather than treating this audit-time match as permanent.

## No mathematical edits required to the author freeze

The exact cone, corrected polar, mixed-nef-product theorem, closure countermodel, and conditional localization repair all pass. Their hypotheses and limits are already stated in the frozen RESULT.md.

## Preserve these qualifications in any downstream summary

1. The polar mismatch is established only for the inspected arXiv v2, not the uninspected publisher full text. It is not a counterexample to the geometric conjecture.
2. The localization repair depends on the credited primary geometric input. Neither F1 nor F2 has been proved nef by this investigation.
3. The interior assertion excludes the numerical zero product. A numerically zero divisor factor gives zero; any four numerically nonzero nef factors give an interior class.
4. The effective face and effective extremality results are not claims about all limits in the ambient pseudoeffective cone.
5. The abstract convex models and numerical candidates are unrealized. Their intersection inequalities are not an effectivity construction.
6. Original surfaces are codimension four; their testing classes are codimension two. The catalog desk note's proposed codimension-four dual route has the degrees reversed. This is a curation issue, not an error in the author RESULT.md.
7. GH v2 Remark 9.2 contains an isolated `3M-8D` transcription where the identity requires `3M-8L`. The source's concluding inequality and the author's repaired argument use the correct latter expression. The audit does not assert anything about the final publisher version.

Disposition remains **UNSOLVED 5/5**. The audit is not a sixth substantive author attempt, a novelty certification, or human peer review.
