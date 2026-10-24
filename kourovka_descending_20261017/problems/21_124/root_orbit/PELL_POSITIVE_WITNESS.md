# The four-edge Pell candidate is virtually special

UTC checkpoint: 2026-10-24T22:49:00Z. Proposed complete result for this one candidate, **not a complete solution of21.124**, awaiting fresh independent adversarial review. No priority claim or publication recommendation. Full-problem discovery estimate remains6%.

## Exact claim and dependencies

For the group G in tubular/PELL_CANDIDATE.md with pairs(p,q)=(3,2),(20,14),(119,84), there is a homomorphism into an integral permutation-by-translation group that is injective on both Z² vertex groups. Hence G has(VRC) by Merladet Urigüen–Minasyan, arXiv2505.18054v3, Theorem1.6, and is virtually special by Proposition1.10 (Appendix jointly with Wu–Ye). These primary statements were freshly read at https://arxiv.org/html/2505.18054v3 on24October2026. This settles the eligibility of this proposed counterexample affirmatively and defeats it as a negative route. It does not answer the original universal free-by-cyclic problem.

The presentation, prior CAT(0)/F5-by-Z eligibility proofs, and earlier abelian/dihedral exclusions remain unchanged. The finite action constructed here is allowed to have high-dimensional irreducible constituents; it need not commute or be dihedral.

## A compressed exact finite object

The file exact_multiset_certificate.json lists517 triples v=(a,b,t) of integers and517 strictly positive integer multiplicities m(v). For each triple take m(v) copies of v and m(v) copies of -v. Let Omega be this indexed finite list, of size

    N=95419250146190292634685757020254542.

Its coordinate vectors A,B,T in Z^Omega are the first, second and third entries respectively. A is nonzero; B is nonzero. Direct exact integer aggregation verifies, for each displayed pair(p,q), equality of the two multisets

    {p A_j+T_j:j in Omega} = {q B_j+T_j:j in Omega}.

Indeed the certificate is checked first by absolute projected values, since the list is centrally symmetric, and then independently by signed projected values in build_permutations.py. Multiplicities are binary-encoded integers, not floating-point weights. No enormous list is expanded.

For each pair choose the canonical matching of equal projected values: sort the source and destination indices of each value increasingly and match their kth indices. This is a permutation P_i of Omega. With the standard action P_i e_j=e_(P_i j), it gives

    P_i(p_i A+T)=q_i B+T.

The file compressed_permutations.json supplies every coordinate block and a piecewise-translation formula for each P_i. Every segment [s,s+l) maps to[d,d+l), j maps to j+d-s. The source segments and destination segments each partition[0,N), and their marked projected values agree. Thus the formulas specify literal finite permutations with checkable bijectivity and vector identities. Let Q=<P_1,P_2,P_3>, a finite subgroup of S_Omega. No assertion about its exact order is needed.

## Homomorphism and vertex injectivity

Let Q act on Z^Omega by these permutations and trivially on one additional Z coordinate. In(Z^Omega directsum Z) semidirect Q define

    a -> (A,0), b -> (B,0), t -> (T,1), s_i -> P_i.

The first three images are pure translations, so the vertex commutators vanish. Each stable-letter relation s_i(a^p_i t)s_i^-1=b^q_i t is exactly the matched-vector identity above, together with unchanged last coordinate1. Therefore these images define a homomorphism from G.

The vectors(A,0),(T,1) are real linearly independent, as A is nonzero. The same holds for(B,0),(T,1). Thus both rank-two vertex lattices map injectively and discretely. The full image is contained in the discrete integral semidirect product, so it supplies precisely Theorem1.6(ii), with no closure, density, or limiting inference. Proposition1.10 applies because G is the finite tubular graph group already presented. This establishes the claim for G.

## Discovery and certificate boundaries

search_multisets.py used HiGHS through SciPy1.18.1 (NumPy2.5.4) to search finite boxes, finding a numerical feasible support in |A|<=6, |B|<=9, |T|<=40. Numerical infeasibility of smaller boxes has no proved nonexistence status. Naive rational approximation failed exact balance and was not promoted.

exactify_support.py reconstructs the517 weights from529 exact integer linear equations via rational row reduction using python-flint0.9.0. The augmented matrix has rank517, with no free columns; every resulting weight is positive. It clears denominators, removes their common gcd, and checks all three balances integrally. This creates the certificate. Correctness of the final finite object does **not** depend on the LP, its numerical tolerance, the exact solver, or uniqueness of the solution: a separate standard-library verifier can read the positive integers and check all identities directly.

These files are reproducibility material for a partial research outcome. A fresh nonauthor must audit all multiplicities, matching orientation, vertex injectivity, applicability of the prior(VRC)/specialness theorems, and preservation of all three relations before root accepts the affirmative candidate conclusion. No Zenodo upload or tracker row is warranted by this result alone.
