# KP-5.4 / 3011: homeomorphism-group ANR analysis

**Status: partial, compact-manifold problem unresolved.** No new solution or novelty claim.

- `REPORT.md`: exact formulation, current-source assessment, five distinct mathematical routes, proofs of the elementary results, and exact remaining gaps.
- `PARAMETRIC_EXTENSION.md`: full Alexander-interpolation argument, finite-dimensional parameter extension, and explicit linear arity-amplification obstruction.
- `check_formulas.py`: finite exact checks with positive and negative controls. These support formula consistency; they do not certify ANR or non-ANR.
- `SOURCE_MANIFEST.json`: public source titles, URLs, hashes, byte counts, inspection scope, and access limits. No source-document bodies are bundled.
- `VERIFICATION.md`: execution scope, actual read-only test results, and limitations.
- `SOURCE_AUDIT.md`: claim-by-claim source dependencies and scope checks.
- `CORRECTIONS.md` and `CORRECTIONS.patch`: explicit correction accounting and pinned report hashes.

Run the checks without writing into this packet:

    PYTHONDONTWRITEBYTECODE=1 python check_formulas.py
    PYTHONDONTWRITEBYTECODE=1 python -O check_formulas.py
    PYTHONDONTWRITEBYTECODE=1 python -OO check_formulas.py

The default destination is stdout. Optional `--output /some/external/path.json` is accepted only outside this packet. `--require-readonly` verifies non-root execution and that the packet tree is not writable.

The main compact problem remains open in this analysis. The known Edwards–Kirby noncompact example is kept separate; it is not called a solution of the intended problem. A failure of canonical Alexander interpolation is also not a non-ANR theorem: the same failure occurs in spatial dimension two, where the ANR question is already answered affirmatively.
