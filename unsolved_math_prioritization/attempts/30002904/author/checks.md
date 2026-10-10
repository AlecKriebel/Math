# Author checks and limitations

These are author checks, not an independent acceptance report.

## Exact source and model checks

- The OWR printed page 1709 was visually inspected. It specifies the operator norm, a two-element product counting measure, and separately defines the inverse-bounded model.
- The journal rendering and author-hosted PDF agree on the numerical bound and threshold in Fuchs--Rivin Theorem 3.4. The PDF page containing that theorem was visually inspected. The malformed separate limits were explicitly distinguished from the intended limit of a quotient.
- Bulinski--Ostafe--Shparlinski PDF pages 5 and 8 were visually inspected. Their disk definition uses closures, and the bad-pair inequality includes equality. Lemma 3.6, Q=1, supplies the exact counting input used here. No claim rests on their freeness theorem alone.
- Source PDFs and HTML are excluded from the frozen package. Their hashes identify exactly the versions inspected, without asserting that different publisher and repository copies have identical bytes.

## Mathematical checks

- The SL2 upper count treats columns with a zero coordinate and the O(X) lower-left-zero matrices.
- The SL2 lower count uses distinct primitive positive first columns, bounded Bezout completions, and H(A) <= ||A||op <= 2H(A).
- The finite-index contradiction uses a power of the translation matrix, not the false implication that every free subgroup of SL2(Z) has infinite index.
- The SL3 Cartan substitution has unit Jacobian. Its chamber constraint is 3u+2d <= 3L. Its dominating integrable density is (1/4)exp(-6u-3d)sinh(d), whose integral is 1/192.
- For every fixed s >= 0, the tail normalization gives 2exp(-2s)-exp(-4s), equal to 1 at s=0 and strictly between 0 and 1 for s>0.
- The inverse-ball condition becomes 2u+d >= L; dominated convergence yields only a Haar-volume conclusion.
- Exact integer matrix multiplication verified both cyclic conjugations, the elementary commutator, and its square in the free-word counterexample. Exact rational arithmetic checked the mass coefficient and eta=5 limiting value. Six checks passed.

## Numerical diagnostic

A private standard-library calculation, run in isolated Python with site loading disabled, independently integrated the finite-L Cartan expression using composite Simpson quadrature with 32768 panels. This was a diagnostic, not a rigorous error-bounded numerical proof. The analytic dominated-convergence proof does not depend on these numbers.

The limiting scaled radial mass is 1/192 = 0.005208333333333333. For the threshold eta=5, the limiting tail probability is 0.00319744.

- L=4: scaled radial mass 0.0052080773527987895; tail 0.0031491084387379855; inverse-ball Haar ratio 0.0019152413356517772
- L=8: scaled radial mass 0.005208333331760244; tail 0.00319743969895504; inverse-ball Haar ratio 0.000000674607102979128
- L=12: scaled radial mass 0.005208333333332734; tail 0.0031974399999985257; inverse-ball Haar ratio 0.00000000022650436143064824

The printed eta=5 upper bound 0.0016 is contradicted by the exact analytic limit, not by reliance on quadrature.

## Package and review boundary

The package has no executable code, so normal versus optimized execution, import-shadow, cache, and execution-root stress tests of a shipped checker are not applicable. File hashes and exact inventory are checked when freezing. Source text, source PDFs, raw problem collections, and coordination records are excluded. The archive is an immutable author snapshot, not an independent certification. Fresh review of the rank-two deduction and especially the rank-three correction is required before publication. Higher-rank discrete generic infinite index remains unresolved by this work.
