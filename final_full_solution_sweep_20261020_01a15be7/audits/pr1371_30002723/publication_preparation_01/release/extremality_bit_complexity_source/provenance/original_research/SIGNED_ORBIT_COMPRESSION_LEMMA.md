# Signed interval-orbit compression lemma

20 October 2026. Independent derivation/audit of an ingredient for the full discontinuous candidate algorithm. This lemma is purely finite-dimensional; it makes no assertion about which constraints suffice for extremality.

## Input and aim

There are N real variables v_0,...,v_{N-1}. Polynomially many interval pairings g identify variables by v_{g(k)}=sigma_g v_k, sigma_g in {+1,-1}. The map g is a translation or reflection between integer intervals. A union Z of polynomially many intervals forces v_k=0 for k in Z. All endpoints are binary integers. We need:

1. the exact dimension D of this solution space;
2. if D is at most a specified polynomial threshold K, a basis described by representative variables;
3. the coefficients in that basis of polynomially many point evaluations v_t and prefix sums sum_{k<t} v_k.

All three tasks are polynomial-bit-time using ordinary and weighted Agol–Hass–Thurston interval-pairing algorithms.

## Double cover and dimension

Concatenate two copies of [0,N-1] into [0,2N-1], labeling them + and -. Lift every signed pairing g by (k,e) -> (g(k),sigma_g e). Each input pairing becomes two valid interval pairings, retaining its geometric orientation. For each interval in Z, add the pairing (k,+) -> (k,-). This is an orientation-preserving pairing between the two copies.

Let c be the number of components in the underlying unsigned N-variable graph, and let c_lift be the number of components in the doubled graph with forced-zero flips. Then

D = c_lift - c.

Proof: each underlying component with consistent signs and no forced-zero vertex gives two lift components and one scalar degree of freedom. A sign-inconsistent or forced-zero component gives one lift component and no scalar degree of freedom. AHT counts both c and c_lift in polynomial time. This also covers isolated variables and singleton pairings.

## Output-sensitive representative extraction

Suppose D<=K. Keep the original forced-zero set Z_0, and maintain Z initially equal to Z_0. When D(Z)>0, find the least t such that

D(Z union [0,t]) < D(Z).

Binary search is valid because adding zero constraints is monotone. This least t is the first vertex in the ordinary order that belongs to a currently free component. The drop at t is exactly one: a single vertex cannot belong to two components. Record t as a representative and replace Z by Z union {t}. Repeat until D=0.

Exactly D representatives are produced, in O(D log N) orbit-count queries. Each query adds one prefix-flip pairing and at most D singleton-flip pairings, so the input sizes remain polynomial. The stored representatives belong to distinct free components of the ORIGINAL graph. Enumeration flips are a bookkeeping device and must not be kept in the later basis-counting call.

## Weighted recovery of prefix sums and point values

Return to the original lifted graph with only the original forced-zero flips Z_0. For each representative r_j put a distinct marker coordinate at (r_j,+), and optionally another at (r_j,-). Each orbit with a + marker has exactly that one + marker and corresponds to one free component with basis convention v_{r_j}=1.

For each queried t, put separate nonnegative weight coordinates on:

- all (k,+) with k<t;
- all (k,-) with k<t;
- the singleton (t,+), when a point evaluation is needed;
- the singleton (t,-), when a point evaluation is needed.

The weight function has polynomially many constant pieces in the concatenated integer interval, because each coordinate changes only at a bounded number of known endpoints. Weighted AHT reports the orbit sums in grouped form. The marker identifies the needed orbit; subtracting its minus-sheet prefix count from its plus-sheet prefix count gives the coefficient of the j-th basis variable in sum_{k<t}v_k. The analogous difference of singleton counts gives its coefficient in v_t. Coefficients have magnitude at most N for prefix sums and at most one for evaluations.

Distinct free components have distinct marker signatures. Thus tagged orbits occur individually, even if untagged zero-component orbits are represented by very large multiplicity intervals. No expansion of untagged output is needed. Nonnegative weights are sufficient throughout; there is no reliance on allowing signed weights inside the imported theorem.

## Bit complexity

Counts and sums have O(log N) or O(log N + log K) bits. Pairing count, vector dimension and the number of weight pieces are polynomial in the original input and K. The AHT and weighted AHT bounds therefore imply the claimed polynomial bit complexity. A dimension D larger than K is returned as a binary integer without enumerating components.

## Primary algorithm interface

Agol, Hass and Thurston, *The Computational Complexity of Knot Genus and Spanning Area*, arXiv:math/0205057v2, Theorems 12 and 16, and the grouped output description at the beginning of Section 6: https://arxiv.org/html/math/0205057v2 . The present signed lifting, prefix dimension search, and basis coefficient recovery are the authored reduction, not a claim that they appear in that paper.
