# Universal small-cardinality proof by collision-relation certificates

**Status:** candidate computer-assisted result, independent adversarial review pending. This is a bounded-cardinality partial result for Kourovka 21.130. It does not resolve arbitrary n. No novelty claim has been made.

## Exact statement supported by the completed certificates

For every abelian group G in which multiplication by 2 is injective, and every subset A of cardinality n with 3 ≤ n ≤ 7, there is a cyclic enumeration of A with pairwise distinct adjacent sums. In particular this holds for every finite odd-order abelian G.

The finite certificate files for n=3,4,5,6,7 have respectively 1,3,16,317,1632 nodes. The same authoring script checks every node and every branch. A separate complete verifier, `verify_certificate_minors.py`, checks every saved certificate using rational ranks and determinantal-divisor indices, without importing HNF or saturation helpers. It independently passed all n=3,...,7 certificates; n=7 took7.64seconds. A supplementary checker tests2700 random lattice-membership cases in dimensions1–6. These computational checks supplement the mathematical argument below.

## Normalize and encode the equalities

Translate A so that its first element is zero; write A={b_0=0,b_1,...,b_(n−1)}. Let F=Z^(n−1), with basis e_1,...,e_(n−1), and put e_0=0. A collision between disjoint edges {i,j} and {k,l} is the relation

`r = e_i + e_j − e_k − e_l`.

There are 3 binomial(n,4) possible relations, up to sign. Two edges sharing a vertex cannot have equal sums because the b_i are distinct. Thus every non-rainbow Hamilton cycle contains one of the enumerated disjoint-edge collision relations.

A node stores an integer relation lattice L≤F. Since 2 is injective on G, all relations in

`L_(2) = {v in F : 2^t v belongs to L for some integer t≥0}`

also vanish under the homomorphism e_i↦b_i. We always replace L by L_(2). If any e_i−e_j belongs to this lattice, the branch is impossible because it forces b_i=b_j.

This direction is enough for the positive result. The encoding is also exact for finite odd groups: F/L_(2) is finitely generated and has no 2-primary torsion. If all marked differences are nonzero, its odd torsion part together with a sufficiently large odd-prime quotient of its free part separates all these finitely many differences. Hence a finite odd-order quotient realizes all marked vertices distinctly while preserving every imposed collision. This is not a relaxation to prime-field vector spaces.

## The exhaustive split and the certificate

At each surviving node choose a Hamilton cycle containing no collision relation already in L. If no such cycle exists, the algorithm has found a realizable counterexample relation system; this never occurs in the completed n≤7 runs.

If the target were false for a configuration satisfying L, the chosen cycle would fail to be rainbow. At least one of its possible disjoint-edge collision relations r would therefore hold. Split into all these possibilities, replacing L by `(L+Zr)_(2)`. Each child either:

1. forces a marked vertex equality, which is an explicitly checked contradiction; or
2. equals another relation lattice recorded as a child node.

The certificate records the chosen cycle at every node and includes every possible collision branch in it. Because the cycle had no relation already in L, every child lattice strictly contains L. Strict inclusion rules out directed cycles in the finite recorded graph. A finite descent through a hypothetical counterexample would therefore reach a contradictory leaf. The root lattice is zero, so no counterexample exists.

The verifier checks that the root is zero; each lattice is saturated at2; each chosen cycle is uncovered; the branches list precisely all its possible disjoint-edge collisions; each child is the claimed extended saturated lattice and is strictly larger; and every contradiction leaf has the advertised vertex difference in its extended lattice. The selection heuristic and memoization order are irrelevant to this finite proof.

## Exact lattice operations

The implementation first obtains a row Hermite normal form by integer Euclidean row operations. At each column it takes the gcd pivot among the remaining rows, makes that pivot positive, clears entries below, and reduces entries above modulo it. Membership is exact integer pivot elimination.

To saturate at2, find a nonempty dependency among the basis rows modulo2. Its integer sum has all entries even; add half that sum to the lattice and compute HNF again. The new vector was not in the previous lattice: in a Z-basis it has half-integral coefficients on a nonempty subset of basis elements. Therefore the lattice index decreases by a factor of2. Iterate until the basis rows are independent modulo2.

The last condition is equivalent to absence of order-two torsion in F/L. Thus the finite process produces precisely L_(2). Every step uses integer arithmetic.

An independent membership criterion checks this implementation: if v lies in the rational row span of L, the finite order of its class in (L+Zv)/L is `Delta_r(L)/Delta_r(L+Zv)`, where Delta_r is the gcd of the r×r minors and r is the common rank. Membership in L_(2) is equivalent to this ratio being a power of2. If v is outside the rational span, it is not in L_(2).

## Reproduction

Run with standard-library Python; no external package is required:

`python3 universal_certificate.py 7 verify`

This checks the saved n=7 certificate without running the search. The same command works with n=3,4,5,6. To regenerate a certificate and verify it, omit `verify`.

`python3 universal_small.py 6` and `python3 universal_small.py 7` reproduce the original searches. `universal_fast.py` preserves the mathematical procedure and caches per-node child computations; the n=7 state counts match exactly. Its n=8 run stopped at the240-second limit with34848states; that run is incomplete and gives no absence conclusion.

`python3 verify_certificate_minors.py 7` independently checks the full n=7 certificate with rational rank, Bareiss determinants, and determinantal divisors. It verifies each branch lattice by mutual2-local membership and explicitly checks DAG acyclicity. The same command works for n=3,4,5,6.

`python3 validate_lattice.py` runs the supplementary random determinantal-divisor comparisons and invariance checks.

## Falsifiable controls and limitations

With saturation at2 disabled, the same symbolic search finds a four-vertex obstruction. Its relations are `b_1−b_2+b_3=0` and `2b_3=0`, realized by the full Klein four-group. This is a positive control showing that the engine does not automatically reject genuine even-order obstructions. The output is preserved in `even_group_positive_control_result.json`.

This certificate proves only the completed finite cardinalities. It does not provide induction in n, establish the suggested monotone-score switching conjecture, or turn the identity-trade bound into a Hamilton-cycle construction. Priority/literature review and independent adversarial review must precede any novelty or publication claim.
