# Corrections and recommended clarifications

## Required mathematical repairs

None. The candidate counterexample passed this audit, with the main n/c+1 problem still unresolved.

## Recommended source clarification

Add a short warning that the last line of Beheshti--Eisenbud Example 4.7 (arXiv:0806.1928v3, printed page 12) appears to omit the normalization by c in its e=3,c=3 example. The definition and a direct conormal computation give length(Q)=6 and q=2. The audited construction already uses the correct definition and does not rely on that line.

## Recommended reproducibility wording

The frozen check.py computes normal determinants and syzygy ranks, while its regularity/Hilbert and derivation entries are encoded consequences of the proof. Describe those entries as formula consistency checks, or include the independent audit checker, which computes actual monomial interpolation spans and derivation constraints as well as the full conormal relations. No frozen file was changed.

## Recommended literature addition

Record Ziv Ran, "On the size and local equations of fibres of general projections," Advances in Mathematics 397 (2022), 108206, arXiv:2205.06751v1. The audit inspected its theorem statements and scope. It supplies length/local-equation results under stated embedding hypotheses, not either requested sharp comparison. This addition does not establish novelty or exhaustive continuing-openness of the full target.

## Optional exposition strengthening

- State that the normal Hessian block is obtained by differentiating the Schur complement of the independent derivative block.
- State that the actual obstruction module is Q isomorphic to k^g, making the absence of a missing free summand transparent.
- State that finite presentation and flat completion preserve the Hom/cokernel calculation and its finite length.

These points are already justified by the existing argument and do not repair a logical gap.

## Status constraints

Keep the overall target unsolved at 5/5 approaches. The strongest verified result is a negative answer to the stronger Q comparison. Do not label the weaker uniform regularity conjecture solved, contradicted, or subsumed by this audit. Do not claim first discovery or external human peer review.
