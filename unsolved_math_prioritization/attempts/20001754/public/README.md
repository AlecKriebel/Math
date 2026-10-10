# AIM lattice three-point bound: partial results

Problem: 20001754 / AIM-GEOMETRY-0092, AIM Problem 1.32 (de Laat).

**The original problem remains unresolved in general. Five substantive approaches were completed.**

The main additional conclusions are:

- Triangle rebasing symmetry and independent rotations cannot coexist in a nonzero Schwartz function: their generated transformations include an unbounded shear.
- Every feasible objective value has a competitor that is not independently rotationally invariant. Therefore angular dependence alone does not demonstrate an improvement.
- In every dimension an explicit triangle-symmetric feasible Gaussian function makes all three normalized edge restrictions give worse bounds than its square-root objective.
- In dimension at least 2, tensoring rotationally invariant one-point dual measures necessarily violates the exact triangle support condition.

The established invariant-subclass identity `P_ind = L_n^2` is retained as prior context, not claimed as a new solution. The later bound that also constrains `|x+y|` is carefully separated.

Files:
- `PROOF.md`: definitions, proofs, precise limitations
- `RESEARCH_LOG.md`: five approaches and outcome of each
- `SOURCE_GATE.md`: source and duplicate checks
- `check_exact.py`, `exact_results.json`: exact algebra controls
- `FROZEN_AUTHOR_MANIFEST.json`: frozen artifact hashes for independent review

Run the controls with `python check_exact.py`. They check finite algebra and formulas; the all-dimensional arguments are in `PROOF.md`.
