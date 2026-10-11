# Balanced permutations: complete obstruction and attributed low-order classification

## Verdict and exact scope

**ACCEPT the prior published resolution of the exact existence and infinitude question.**
For integers `n >= k >= 1`, an `n`-permutation has exactly
`n! / ((k!)^2 (n-k)!) = binom(n,k)/k!` occurrences of each `k`-permutation if and only if:

- `k=1`: every `n >= 1` is allowed;
- `k=2`: `n >= 2` and `n = 0 or 1 (mod 4)`;
- `k=3`: `n >= 3` and `n = 0,1,9,20,28,29 (mod 36)`;
- `k >= 4`: no `n >= k` is allowed.

In particular, for each fixed `k <= 3` infinitely many lengths exist, and for each fixed `k >= 4` none exist. The first allowed length for `k=3` is 9.

The attribution is Gal Beniamini, Nir Lavee, and Nati Linial, *How Balanced Can Permutations Be?*, Combinatorica 45, article 9 (2025), DOI https://doi.org/10.1007/s00493-024-00127-x. The published Theorems 1 and 2 summarize the resolution; the relevant proofs are Proposition 2.4 and its corollaries, Section 3, Section 4.2, and Appendices A and B. The arXiv v1 is https://arxiv.org/abs/2306.16954v1 (29 June 2023). The published article was first published online on 2 January 2025.

This is an authored mathematical exposition and internal AI audit of an existing result, not a new solution or a claim of novelty. It does not audit the paper's unrelated quantitative discrepancy, permuton, or reconstruction results. The nonexistence theorem and the order-1 and order-2 classifications are proved completely below. The order-3 sufficiency statement uses separately checked finite witnesses identified in Section 8 but omitted from this edition. Consequently the complete low-order classification cannot be independently reproduced from this edition alone; this is not a complete self-contained proof of the finite-witness part. Hashes alone do not prove that omitted finite premise.

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit of the exact target, with no external human peer review, journal acceptance of this exposition, formal proof-assistant certification, or CI claim.

## 1. Target identification and interpretation

The historical Cooper question is about arbitrary increasing index sets, not contiguous substrings. For a permutation `pi` of `[n]` and a permutation `tau` of `[k]`, write `N_tau(pi)` for the number of index sets `i_1 < ... < i_k` for which the relative order of `(pi(i_1),...,pi(i_k))` is `tau`. The paper uses precisely this definition in Definitions 2.1–2.3 (published pages 4–5). Its term **k-balanced** is therefore exactly the historical **perfectly k-symmetric** condition.

There are `binom(n,k)` index sets, so equality of all `k!` counts means that every count is `binom(n,k)/k!`. The historical formula agrees identically. No limiting process, random choice of a permutation, averaged equality, or approximate uniformity is substituted for that finite exact condition.

The historical source https://people.math.sc.edu/cooper/combprob.html continues to state the old question for `k>3`. Its wording does not override the later proof. The target match and the mathematical verification are distinct: matching definitions alone would not establish the result.

## 2. Downward closure, including the endpoint

Let `n >= k >= r >= 1` and fix `tau` in `S_r`. Count pairs `(B,A)` with `B subset A subset [n]`, `|B|=r`, `|A|=k`, and `pi|B` of type `tau`. Counting first `B`, and then first `A`, gives

`binom(n-r,k-r) N_tau(pi) = sum_{sigma in S_k} N_tau(sigma) N_sigma(pi).`  (2.1)

The coefficient sum on the right is

`sum_{sigma in S_k} N_tau(sigma) = binom(k,r) k!/r!`.

Indeed, choose the `r` positions, choose the `r` values, place the latter in the prescribed relative order, and permute the remaining values; this gives `binom(k,r)^2 (k-r)!`, which equals the displayed expression.

If `pi` is `k`-balanced, substitution and the elementary subset identity

`binom(n,k) binom(k,r) = binom(n,r) binom(n-r,k-r)`

give `N_tau(pi)=binom(n,r)/r!`. The factor being divided out is positive even when `n=k`. Thus downward closure holds for the full domain `n >= k >= r`, not just the paper's stated `n>k>r` in Proposition 2.4.

There is also a direct endpoint check: for `n=k>=2`, the `k`-profile has one entry 1 and every other entry 0, so it cannot be balanced. For `n=k=1`, the unique profile entry is 1. Consequently no conclusion relies on extending a strictly stated hypothesis without proof.

Integrality now gives the **necessary conditions** `r! | binom(n,r)` for every `r <= k`. These conditions alone are not claimed sufficient when `k>=4`.

## 3. Complete nonexistence proof for k >= 4

Let `A=N_12(pi)`. Regard `A^2` as the number of ordered pairs of increasing pairs of indices. Partition the count by the size of the union of the two pairs. A union has size 2, 3, or 4.

- Size 2 contributes `N_12(pi)`.
- For a given triple, type 123 has six ordered pairs of distinct increasing pairs whose union is the triple. Types 132 and 213 each have two. The remaining triple types have none. This contributes `6 N_123 + 2 N_132 + 2 N_213`.
- For a given quadruple `sigma`, let `c_sigma` count ordered choices of two disjoint increasing pairs that use its four positions. Its contribution is `c_sigma N_sigma(pi)`.

For the contradiction only the coefficient sum is needed. There are six ordered partitions of four positions into two pairs. For each partition, exactly `4!/4=6` relative value orders make both pairs increasing: each of the two disjoint comparisons is satisfied in half the orders. Thus `sum_{sigma in S_4} c_sigma=36`. This derivation covers every four-point pattern without requiring an individual coefficient table.

We have proved the exact identity

`A^2 = sum_{sigma in S_4} c_sigma N_sigma + 6N_123 + 2N_132 + 2N_213 + N_12`.  (3.1)

Assume now `n>=4` and `pi` is 4-balanced. Downward closure makes its 3- and 2-profiles uniform. Equation (3.1) becomes

`(binom(n,2)/2)^2 = (36/24)binom(n,4) + (10/6)binom(n,3) + (1/2)binom(n,2)`.

Subtracting the left side from the right side and expanding gives exactly

`n(n-1)(2n+5)/72`.

It is strictly positive for every integer `n>=4`, a contradiction. No divisibility exception or lower-order endpoint survives this argument. If `k>4` and `n>=k`, downward closure gives 4-balance and the same contradiction. This proves the entire negative part.

This argument is a finite double count. It invokes no graph limit, quasirandomness theorem, computational search, or external nonexistence theorem. Appendix B of the paper provides a compatible finer enumeration. The separate audit independently generated all coefficients rather than reading them from the paper.

### Divisibility is not sufficient in general

`n=64` satisfies `r! | binom(64,r)` for `r=1,2,3,4`: the quotients at orders 2, 3, and 4 are 1008, 6944, and 26474. Nevertheless, the positive discrepancy above excludes a 4-balanced permutation. It would be incorrect to extend the low-order admissibility characterization to all `k`.

## 4. Low orders 1 and 2

For `k=1`, every permutation has the only pattern exactly `n` times; the divisibility condition is vacuous.

For `k=2`, necessity is `2 | binom(n,2)`, or `4 | n(n-1)`, which is equivalent to `n=0 or 1 (mod 4)`. For sufficiency, start with the increasing permutation and move to the decreasing permutation by adjacent swaps, always swapping an adjacent increasing pair. At each step the inversion count increases by exactly one and all other pair comparisons are unaffected. The inversion count consequently takes every integer between 0 and `binom(n,2)`. If the latter is even, stop at half the total. The numbers of increasing and decreasing pairs then agree. This proves sufficiency without an assumed realization theorem.

The domain `n>=2` excludes the merely formal residue representative `n=1` in the `k=2` statement.

## 5. Arithmetic for k=3

The order-2 condition again requires `n=0 or 1 (mod 4)`. The order-3 condition is `36 | n(n-1)(n-2)`. Under the order-2 condition the factor 4 is already present, so the remaining condition is `9 | n(n-1)(n-2)`. Exactly one of three consecutive integers is divisible by 3; its contribution must be divisible by 9. Equivalently, `n=0,1,2 (mod 9)`.

Combining the conditions by the Chinese remainder theorem gives exactly

`n=0,1,9,20,28,29 (mod 36)`.

There are no admissible values between 3 and 8. This proves necessity and identifies the precise sufficiency target. Sections 6–7 give the analytical families. Section 8 identifies the additional checked finite premise required for sufficiency at every remaining admissible length.

## 6. Rotation construction and the central-point correction

Given any permutation `sigma` of `[m]`, start with points `(m+i,sigma(i))` for `1<=i<=m`, and add their three images under the map

`R(x,y)=(y,4m+1-x)`.

For each starting point the four x-coordinates are `m+i`, `sigma(i)`, `3m+1-i`, and `4m+1-sigma(i)`. Over all `i`, these partition `[4m]` into four disjoint intervals. The y-coordinates also form `[4m]`. Thus the result is a genuine permutation, invariant under a quarter-turn. Call it `pi_0`. For `pi_1`, add `(2m+1/2,2m+1/2)` and replace each coordinate by its rank. Its length is `4m+1` and it too is quarter-turn invariant.

The quarter-turn acts on the six triple patterns in two orbits: `{123,321}` and `{132,231,213,312}`. Applying the rotation maps occurrences bijectively, so each orbit has a common count. Therefore either construction is 3-balanced exactly when `N_123 = binom(4m+e,3)/6`, where `e` is 0 or 1.

Write

`P=N_12(sigma), D=N_21(sigma)=binom(m,2)-P, M=N_123(sigma)+N_321(sigma)`.

A direct classification of ascending triples in the four blocks gives

`N_123(pi_0)=2M+4mP+2mD`.  (6.1)

Here all-three-in-one-block choices contribute `2M`. There is no ascending triple using three different blocks because the block order is 3142, which has no 123 pattern. A two-in-one-block choice contributes `4mP+2mD`: the increasing block pairs are (first,third), (second,third), and (second,fourth), and counting the two possible blocks holding the pair gives four `mP` terms and two `mD` terms. Rotating an ascending pair by a quarter-turn reverses its pair type; this accounts for the `D` terms.

In `pi_1`, triples through the new centre add exactly `m^2+2P` to the 123 count. The centre can be the middle point, with one point southwest and one northeast (`m^2` choices), or an endpoint with an ascending pair in the opposite southwest/northeast block (`P` choices each). Thus

`N_123(pi_e)=2M+4mP+2mD+e(m^2+2P)`.  (6.2)

Substituting `D=binom(m,2)-P` and simplifying the target count proves the single exact criterion

`3M + 3(m+e)P = binom(m,3)+m^3+e binom(m,2)`.  (6.3)

The extra `3P` and `binom(m,2)` terms when `e=1` are essential. Applying the even-length equation unchanged to an odd-length construction would be incorrect. The published Appendix A gives the odd constructions without spelling out this corrected equation; equation (6.3) supplies the omitted calculation.

## 7. Six infinite construction families, exactly checked

The starting point set consists of three descending blocks of length `ell=3t+1` in increasing block order:

`B_q = {(q ell+i, (q+1)ell+1-i): 1<=i<=ell}`, for `q=0,1,2`.

Let `eps=1/4`. The following affine coordinate formulas specify the mathematical constructions credited to Appendix A of Beniamini–Lavee–Linial, with this definite choice of epsilon. The formulas are retained as analytical construction definitions, not as numerical permutation witnesses. Convert the enlarged point set to its order-isomorphic permutation `sigma`, and apply Section 6.

### Even-length families (t>=2)

Use the first `s=2`, `4`, or `6` points of this list:

1. `(4t+4+eps, 7t+3+eps)`
2. `(7t+3+eps, 4t+2-eps)`
3. `(eps, 3t+1+eps)`
4. `(1+eps, 3t+1-eps)`
5. `(3t+3+eps, eps)`
6. `(3t+2+eps, 5+eps)`

Then `m=9t+3+s` and `n=4m` is respectively `36t+20`, `36t+28`, or `36t+36`.

### Odd-length families (t>=4)

Use the first `s=4`, `6`, or `8` points of this list:

1. `(-5+eps, 1+eps)`
2. `(-3+eps, t-2+eps)`
3. `(-2+eps, 7t+4+eps)`
4. `(eps, 7t+3+eps)`
5. `(-4+eps, 3t-1+eps)`
6. `(2t-2+eps, 5t+1+eps)`
7. `(-1+eps, 3t-2+eps)`
8. `(4t+1+eps, t-1+eps)`

Then `m=9t+3+s` and `n=4m+1` is respectively `36t+29`, `36t+37`, or `36t+45`.

All inserted coordinates are nonintegral, so none equals a base coordinate. Comparisons within each inserted list show no two x-coordinates or two y-coordinates coincide at the stated integer parameter range. Consequently rank normalization is always defined.

### The needed exact polynomial counts

The following counts hold throughout the indicated ranges, including their first parameter values:

- Even, s=2: `P=27t^2+30t+8`, `2M=81t^3+108t^2+53t+10`.
- Even, s=4: `P=27t^2+42t+16`, `2M=81t^3+162t^2+113t+28`.
- Even, s=6: `P=27t^2+54t+26`, `2M=81t^3+216t^2+209t+74`.
- Odd, s=4: `P=27t^2+39t+14`, `2M=81t^3+189t^2+152t+42`.
- Odd, s=6: `P=27t^2+51t+24`, `2M=81t^3+243t^2+248t+86`.
- Odd, s=8: `P=27t^2+63t+36`, `2M=81t^3+297t^2+380t+170`.

Substitute each pair of formulas, `m=9t+3+s`, and its parity into (6.3). The two sides agree coefficient by coefficient. This proves 3-balance for all six infinite families, not just the sampled values.

### A finite summation derivation of the polynomial formulas

The paper observes that the counts are low-degree polynomials and proposes four evaluations. Affine coordinates by themselves only imply piecewise polynomial behavior; one must also check that no order chamber changes inside the claimed range. We make that step explicit.

For each base block `q`, parameterize its points by the integer `i` in `[1,ell]`. For every inserted point `(x,y)`, place cuts at

`floor(x-q ell)` and `floor((q+1)ell+1-y)`,

as well as 0 and `ell`, discarding cuts outside `[0,ell]` and removing duplicates. In each interval `L<i<=U`, all comparisons to all inserted points are fixed. It defines an atom of `U-L` descending points. Different base blocks already have a uniform relative order. The inserted points themselves are singleton atoms. Therefore every tuple of chosen atoms has a fixed permutation type, and every repeated selection from the same base atom is descending.

For a pattern `tau` of order `r<=3`, its count is consequently the finite sum

`sum_{(v_a): sum v_a=r, induced type=tau} product_a binom(length(a),v_a)`.  (7.1)

All atom lengths are affine functions of `t`. The cut order and the atom order are fixed for every integer `t` in the stated range; the explicit cut lists are given in the appendix below. An atom of length zero at the first parameter is simply absent there. Contributions containing it vanish because `binom(0,j)=0` for `j>0`; no extension through a nonexistent point is assumed.

Formula (7.1) proves that the count is a polynomial of degree at most `r`, and gives a direct rational-arithmetic expansion of it. Applying it to 12, 123, and 321 gives the analytical formulas in Section 7. Thus the audit does not rest on an unverified interpolation inference. The analytical cut sequences are given in the appendix below. Raw generated profiles, numerical certificates and executable checking code are omitted; the general finite summation argument is retained.

## 8. Separately checked finite premise and reproduction boundary

The six family start lengths are 92, 100, 108, 173, 181 and 189, respectively. For each family, take its arithmetic progression of common difference 36 from that start. Let `E` be the set of integers `n>=3` satisfying `n=0,1,9,20,28,29 (mod 36)` but not belonging to those six progressions. Counting the smaller admissible representatives in each residue class gives `|E|=19`. This defines the exceptional domain without distributing numerical permutation lists or outcome tables.

**F1 (finite witness premise).** For every `n in E`, Table 1 of Beniamini–Lavee–Linial supplies a list that is a permutation of `[n]` and has each of its six order-3 pattern counts equal to `binom(n,3)/6`.

The exact source is *How Balanced Can Permutations Be?*, Combinatorica 45, article 9 (2025), DOI https://doi.org/10.1007/s00493-024-00127-x, Appendix A, Table 1, published pages 28–29. The corresponding unchanged data are in arXiv:2306.16954v1, Appendix A, Table 1, page 21: https://arxiv.org/pdf/2306.16954v1. Source PDF identities and historical inspection metadata are recorded in SOURCES.json.

F1 was checked in the accepted audit. Every list was verified to contain exactly `[n]`, and every increasing index triple was counted in two independently written ways: rank normalization and a six-way comparison test. Both methods gave the required uniform profile for all 19 lists. The two authenticated source versions contain identical witness data. This is verification of explicit finite inputs, not numerical extrapolation.

Those numerical permutation witnesses, individual outcome tables, raw certificates and checking code are not distributed here. The source citation locates the missing evidence; it is not a substitute for displaying or rechecking that evidence. To reproduce F1, a reader must obtain the identified Table 1, validate each list's length and entries, and independently count every triple as just specified. The complete low-order classification cannot be independently reproduced from this edition alone, and this is not a complete self-contained proof of the finite-witness part. Hashes alone do not prove F1.

Subject to the separately verified F1, all admissible lengths are covered by exactly the analytical families or the exceptional domain, while Section 5 excludes every other length. Thus the audit accepts the existing complete order-3 classification with an explicit boundary between the retained analytical proof and the omitted finite evidence.

## 9. Dependencies, qualifications, and acceptance limits

The proof depends only on:

1. The finite definition of order-isomorphic subsequence occurrence.
2. The double-counting identity (2.1), proved here.
3. The ordered-pair-of-pairs count (3.1), fully derived here.
4. Adjacent swaps for order 2.
5. Quarter-turn symmetry and the block/centre counts in (6.1)–(6.3).
6. Explicit affine point constructions, integer order checks, and the finite sum (7.1).
7. Premise F1: the 19 finite explicit witnesses in the two authenticated versions of Table 1, separately checked but omitted here.

No theorem about permutons, approximate balance, discrepancy, random permutations, or flag algebras is a dependency. The paper's other open questions remain separate and are not inherited into this target.

Two local presentation issues are worth recording without overstating them:

- The published downward-closure proposition is phrased with `n>k`; Section 2 above proves the endpoint directly.
- Appendix A's polynomial-shortcut description is compressed. Section 7 supplies chamber checks and exact coefficient calculations, and Section 6 supplies the odd-centre adjustment. These are completed derivations, not unresolved holes.

The result is accepted as a prior resolution of the historical exact target. This is not a certification that every claim in either full paper is correct, nor a claim that every later paper or correction has been searched. The decisive nonexistence proof and the analytical low-order derivations are supplied independently; acceptance of full order-3 sufficiency additionally uses F1. None of these conclusions relies on such a global literature claim.

## Appendix: exact finite counting derivation


This supplements Section 7 of the audit. Coordinates and notation are defined there. It gives all cuts needed to turn the six geometric constructions into a finite polynomial calculation; no numerical interpolation or asymptotic claim is needed.

For a base block indexed by `q=0,1,2`, write the listed cut sequence as `c_0,...,c_h`. The j-th atom contains all integers `c_(j-1)<i<=c_j` and has length `c_j-c_(j-1)`. Its point coordinates are `q(3t+1)+i` and `(q+1)(3t+1)+1-i`. Every inserted point is an additional length-one atom.

The cuts in each line are nondecreasing for every permitted integer parameter. Equal consecutive cuts only create an empty atom, which contributes zero to all selections. Each atom is internally decreasing. Order atoms by x-coordinate; order their values by y-coordinate. Base atoms in different blocks have matching block order, and the displayed cuts isolate every inserted x- or y-threshold. Hence the relative atom orders are fixed.

Given nonnegative occupancies `v_a` totaling r, first write the atoms in x-order, with `v_a` decreasing values inside each atom. Its relative y-order specifies a unique r-pattern. The multiplicity is `product_a binom(length(a),v_a)`. Sum that multiplicity for every occupancy of total 2 or 3 and the required pattern. This is an explicit finite formula involving at most 21 atoms and occupancy totals at most 3.

For ease of reproducing the calculation without general polynomial software, use `binom(L,0)=1`, `binom(L,1)=L`, `binom(L,2)=L(L-1)/2`, and `binom(L,3)=L(L-1)(L-2)/6`. All displayed L are affine polynomials in t. The degree bound is thus immediate and the coefficients in the analytical formulas in Section 7 follow by expanding finite products.

## All atom cut sequences

### even, s=2; t>=2

- q=0: `0, 3t+1`
- q=1: `0, t+3, 2t+1, 3t+1`
- q=2: `0, t+1, 2t, 3t+1`

Including inserted singleton atoms, there are 9 atoms.

### even, s=4; t>=2

- q=0: `0, 1, 3t+1`
- q=1: `0, t+3, 2t+1, 3t+1`
- q=2: `0, t+1, 2t, 3t+1`

Including inserted singleton atoms, there are 12 atoms.

### even, s=6; t>=2

- q=0: `0, 1, 3t-4, 3t+1`
- q=1: `0, 1, 2, t+3, 2t+1, 3t+1`
- q=2: `0, t+1, 2t, 3t+1`

Including inserted singleton atoms, there are 17 atoms.

### odd, s=4; t>=4

- q=0: `0, 2t+3, 3t, 3t+1`
- q=1: `0, 3t+1`
- q=2: `0, 2t-1, 2t, 3t+1`

Including inserted singleton atoms, there are 11 atoms.

### odd, s=6; t>=4

- q=0: `0, 2, 2t-2, 2t+3, 3t, 3t+1`
- q=1: `0, t+1, 3t+1`
- q=2: `0, 2t-1, 2t, 3t+1`

Including inserted singleton atoms, there are 16 atoms.

### odd, s=8; t>=4

- q=0: `0, 2, 3, 2t-2, 2t+2, 2t+3, 3t, 3t+1`
- q=1: `0, t, t+1, 3t+1`
- q=2: `0, 2t-1, 2t, 3t+1`

Including inserted singleton atoms, there are 21 atoms.

## Endpoint and independent validation

At t=2 in the even constructions, the adjacent cuts t+3 and 2t+1 coincide, producing one empty atom. The formula handles it exactly: all terms selecting a point from that atom vanish. When it becomes nonempty, its order agrees with the open interval it represents. Every other length is nonnegative as specified by the cut lists.

The checker validates clipping, cut order, and coordinate comparison signs as affine inequalities on the entire half-line. Each such inequality is checked by its slope and its value at the initial parameter. For comparisons involving an initially empty atom it starts at the first integer parameter when that atom is nonempty. This is a proof by affine inequalities, not a bounded-parameter test. It then expands the finite occupancy sums with exact rational arithmetic.

Additional direct enumeration checks the inner profiles at the first four parameters, at seven above the first parameter, and at t=50. It checks all six entries of each full outer triple profile at the first four parameters. These finite checks test implementation independently; the unbounded conclusion follows from the symbolic counting derivation.
