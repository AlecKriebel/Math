# Exact-target audit and publication boundary

## Accepted result

For n>=k>=1, exact equality of all length-k subsequence-pattern counts occurs precisely for k=1; for k=2 with n=0 or 1 modulo 4; and for k=3 with n=0,1,9,20,28,29 modulo 36. There are no examples for k>=4. In particular the positive cases have infinitely many lengths and the negative cases have none. This is the prior result of Gal Beniamini, Nir Lavee and Nati Linial, *How Balanced Can Permutations Be?*, Combinatorica 45, article 9 (2025), DOI https://doi.org/10.1007/s00493-024-00127-x.

## Complete elementary portion

The definition concerns arbitrary increasing index sets, not consecutive substrings. The profile total is binom(n,k), so the common required count is binom(n,k)/k!.

The downward-closure double count includes n=k, where its binomial divisor remains positive. The direct endpoint profile also excludes n=k>=2. The ordered-pair-of-increasing-pairs identity partitions unions of size 2, 3 and 4, with aggregate coefficients 1, 10 and 36. Uniform profiles would force a square identity whose right side exceeds its left by n(n-1)(2n+5)/72>0 for n>=4. This is a complete contradiction throughout n>=k>=4, independent of divisibility and of all order-3 witnesses.

Order 1 is immediate. For order 2, adjacent increasing-pair swaps realize every inversion count, proving sufficiency of 4 dividing n(n-1). The modular arithmetic for order 3 follows from downward closure and divisibility by 9 of the product of three consecutive integers.

## Analytical construction audit

The quarter-turn construction has genuine distinct coordinates. Its six triple patterns split into two symmetry orbits. Counting increasing triples gives the even formula and the centre correction m^2+2P for odd length. The resulting criterion is 3M+3(m+e)P=binom(m,3)+m^3+e binom(m,2), where e is 0 or 1. Omitting the odd correction would be erroneous.

All six affine families are attributed to the source Appendix A. Their parameter ranges are retained, as are the authored analytical count formulas and all atom cuts. The cuts fix coordinate-comparison chambers on the full parameter half-lines. Empty endpoint atoms contribute zero. Summing products of binomial occupancy factors gives polynomials of the asserted degree and yields the stated exact formulas. The argument therefore goes beyond unsupported interpolation from four samples. Direct finite tests are implementation cross-checks; they are not the reason the parameter conclusions are unbounded.

## Finite evidence and exact scope of acceptance

Premise F1 in PROOF.md identifies the 19 exceptional witnesses in the published Table 1, pages 28–29, and arXiv v1 Table 1, page 21. Every witness is separately checked by two independent triple-count methods, and the two source versions agree. The public edition omits witness contents, per-witness outcome tables, raw generated certificates and executable code. Reproduction of F1 requires obtaining the cited source inputs and checking them anew.

The full accepted audit also exhaustively checked the pair-square identity on all 5,913 permutations of lengths 1 through 7 and both rotation formulas on 306 parity-labelled inputs of lengths 1 through 5. All six families had exact symbolic chamber and polynomial checks, plus direct profile checks. The audit's recorded normal, -O and -OO runs produced byte-identical substantive outputs. Edition preparation byte-reauthenticated that evidence; it did not rerun those mathematical computations.

The published Proposition 2.4's strict endpoint wording is supplied by the independent endpoint proof. Compressed Appendix A calculations are expanded by the chamber derivation and odd-centre count. These are explanatory completions; this edition does not allege that the published theorem is false or claim a new theorem.

Acceptance concerns only the historical exact existence and infinitude question. It does not accept all of either full paper, especially unrelated discrepancy, permuton and reconstruction results. No outside communication or publication action is part of this edition preparation.

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit of the exact target, not external human peer review, journal acceptance of this exposition, formal proof-assistant certification, or CI verification. No novelty or exhaustive literature-status claim is made.

The complete low-order classification cannot be independently reproduced from this edition alone. This is not a complete self-contained proof of the finite-witness part. Hashes alone do not prove the omitted premise F1. The nonexistence theorem for n>=k>=4 and the order-1 and order-2 classifications have complete elementary proofs in PROOF.md.
