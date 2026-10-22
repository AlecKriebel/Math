# Cohomology-vanishing exponents: independently audited partial checkpoint

**Problem 30005041 / OWR-9790362-012 remains unsolved, five of five substantive attempts used.** The full audit passes the scoped partial propositions; it does not certify a complete solution, historical novelty, or human peer review.

- [Frozen research packet](frozen/README.md), with [five mathematical attempts](frozen/ATTEMPTS.md)
- [Full independent adversarial audit](audit/independent_audit.md)
- [Independent primary-source review](audit/source-review/PRIMARY_SOURCE_REVIEW.md)
- [Audit manifest](audit/AUDIT_MANIFEST.json)

The original six-file research packet is preserved byte-for-byte under `frozen/`. Its historical `audit_status: requested_pending` is superseded by the separate final PASS audit without rewriting the frozen evidence. The audit files are likewise preserved after checking that they contain no private context, scholarly PDFs, or absolute workspace paths.

The strongest scoped results are the all-positive-exponent classification of signed atomic Z-actions, a sharp density criterion for positive multiplication intertwiners, and the uniform-primitive criterion for direct sums. None supplies the missing genuinely nonformal cocycle analysis for general diffuse nonsingular actions.

## Reproduce

From this folder run:

    python3 frozen/checks/exact_controls.py
    python3 audit/independent_controls.py --author frozen

The author checker passes 6,480 exact assertion cases. The independent checker passes 52,164 cases including byte/inventory controls; the mathematical controls alone number 52,156. They include 50,363 finite signed permutation models. The written proofs establish the scoped infinite-family statements; finite tests do not solve the original interval problem.

## Checkpoint log

- 2026-10-03: Original target independently recovered at OWR2022/11,p.568,Question1. Five distinct proof routes completed and frozen. No full resolution obtained.
- 2026-10-03: Fresh independent adversarial mathematics/source audit passed without mandatory repair. Both checker outputs reproduced byte-for-byte for publication.
- Research completion estimate: 15% toward a full resolution, a subjective planning estimate only. Source identification and scoped controls are complete; the central diffuse nonsingular obstruction remains.

No release, paper, DOI, or merge is proposed by this checkpoint.
