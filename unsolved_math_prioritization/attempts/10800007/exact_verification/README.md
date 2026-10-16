# Verification package

The theorem is proved by the accompanying MANUSCRIPT.tex. A continuous exact root on any neighborhood of the zero coefficients restricts to a square root on a complex disk; a nonzero lifted polygon squares to a closed loop and forces an impossible sign change. Every admissible open cover would include such a neighborhood. The translated coefficient construction shows that deleting only the zero vector does not repair the family.

Python 3.11 or later suffices; only the standard library is used. From this archive's root:

    python3 verify.py models/baseline.json
    python3 -O verify.py models/baseline.json
    python3 run_controls.py --output reproduced-results.json

verify.py checks universal polynomial identities, the complete Jacobian, exact quadratic extrema on closed path intervals, seams/endpoints and strict disk inclusion. It prints JSON and never writes a verification verdict file. Explicit exceptions remain active under optimization. It certifies only supported polynomial/norm inputs, not arbitrary functions or continuity/topology.

run_controls.py executes every one of fifteen supplied models in ordinary and optimized modes. Two mathematically valid orientations must pass; thirteen invalid or unsupported models must fail for the recorded scientific reason. Higher-degree hidden-zero paths fail on the explicit supported-degree limit. This is not a high-degree positivity solver, and the program does not infer no-section topology from finite sampling.

REPRODUCTION.json records the actual root replay of this exact package code/models. Input/output hashes bind each run; timestamps are actual replay metadata. The recorded replay was performed on Python 3.14.6 for v1; the v2 correction changes documentation only, and its checker, driver, models and manuscript remain byte-identical. Those timestamps are retained as actual historical runs, not relabelled v2 executions. New user replays produce their own receipts. MANIFEST.json records archive file identities, excluding itself. The outside deposited LaTeX source must be byte-identical to MANUSCRIPT.tex.

PRIORITY_AUDIT.md credits the classical tools and records actual body/version gaps. The additional audit notes reproduce only our analysis and source locators, never third-party article bodies. Their historical timestamps/status estimates are retained as such; they are not current publication-readiness or novelty certificates.

The original submitted sampled scripts were preserved separately in the repository audit. They had assertion guards disabled by optimization; guarded copies were reproduced, and their finite-sampling blind spots were documented. This archive uses universal exact polynomial bounds for its supported class, while the written connectedness argument supplies topology.

AI-assisted; unrefereed; no conventional human peer review.
