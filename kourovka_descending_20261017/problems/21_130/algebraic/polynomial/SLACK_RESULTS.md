# Reduced cyclic polynomial: all odd characteristics at small n

Status: a verified finite-size partial result; no assertion for all n. The general odd-order abelian-group claim remains unresolved. Best-guess completion estimate: **15%** after the formal-group transfer and independent size-eleven audit.

Later independently checked certificates extend the odd-prime range through **n=11** and cover **n=11 for every prime p, including p=2**. The n=10 witness pair has gcd2; the n=11 witness pair has gcd1. See `FINAL_AUDIT.md` and `FIXED_ZERO_N11_AUDIT.md`. The detailed n=3 through9 proposition and table below are preserved as the first checkpoint.

## Proposition

Every subset A of a finite abelian p-group for an odd prime p, with 3≤|A|≤9, has a cyclic enumeration with pairwise distinct adjacent sums.

The elementary-abelian case is supported by the self-contained polynomial/grid proof below and explicit independently checked integer coefficients. The general p-group case additionally uses the sourced formal-group transfer independently audited in FORMAL_GROUP_AUDIT.md; that transfer uses the original Lubin–Tate theorem cached and cited in the parent algebraic folder. No claim of novelty is made.

## Polynomial and coefficient criterion

Let s_i=x_i+x_(i+1 mod n), and let D be the pairs of nonadjacent edges of the fixed cyclic template (indices 0≤i<j<n with j−i neither 1 nor n−1). Define

    Q_n(x)=V(x) ∏_((i,j)∈D)(s_j−s_i).

There are n(n−3)/2 factors in the second product, so deg Q_n=n(n−2). If Q_n(x) is nonzero at a point of A^n, the Vandermonde makes its coordinates pairwise distinct; consequently they enumerate A. Distinct sums for disjoint template edges follow from the second product. For adjacent template edges, the difference is x_(i+2)−x_i, which is already nonzero. This last argument requires n>2, as in the original problem. Thus every nonzero evaluation gives exactly one desired cycle.

Suppose t=(t_0,...,t_(n−1)) has 0≤t_i≤n−1 and ∑t_i=n(n−2), and the coefficient c_t=[x^t]Q_n is nonzero in a field F. For each i choose an arbitrary subset A_i⊂A of size t_i+1. Applying the multivariate coefficient lemma to the unequal-size grid ∏A_i shows Q_n has a nonzero evaluation there. The proof of the lemma is identical to the one in RESULTS.md: each univariate functional kills powers below t_i, and the total degree bound ensures every monomial other than x^t has some exponent below t_i. The Vandermonde then guarantees all n coordinates are distinct even though the auxiliary grid subsets can differ.

Therefore, for a fixed n, a list of eligible integer coefficients with gcd a power of 2 certifies every odd characteristic: no odd prime divides every coefficient in the list. A different coefficient and different auxiliary grid can be used for different characteristics. This is enough to cover every n-element subset of (Z/pZ)^d, by its additive identification with F_(p^d).

## Explicit coefficient certificates

Every exponent tuple in this table satisfies the coordinate bounds and required total degree. The listed coefficients are computed by direct truncated multiplication in `slack_probe.py` and independently by finite differences in `slack_coefficient_audit.py`.

| n | Exponent tuple t | Integer coefficient |
|---:|---|---:|
|3|(0,1,2)|1|
|4|(0,2,3,3)|4|
|5|(1,3,3,4,4)|14|
|5|(0,4,3,4,4)|−24|
|6|(2,3,5,5,4,5)|182|
|6|(2,4,5,5,3,5)|−476|
|6|(0,4,5,5,5,5)|−520|
|7|(1,5,6,5,6,6,6)|−1454|
|7|(4,4,5,5,5,6,6)|1570|
|8|(4,6,5,7,7,6,6,7)|−108696|
|8|(3,4,6,7,7,7,7,7)|−2270792|
|9|(0,7,8,8,8,8,8,8,8)|−137176976|
|9|(1,7,8,7,8,8,8,8,8)|−1261141910|

For n=3,...,9 the gcds of these witness lists are respectively 1,4,2,2,2,8,2. All are powers of 2, proving the proposition. The full truncated-polynomial contents have the same respective values, with support sizes 6,16,100,354,1582,5904,23694. Exact full support at n=8,9 is saved in `slack_n8.json` and `slack_n9.json`.

The independent finite-difference certificate uses no polynomial expansion. For an eligible t, integer interpolation on ∏{0,...,t_i} gives

    c_t = 1/(∏t_i!) · ∑_(0≤a_i≤t_i) (-1)^(∑(t_i−a_i)) (∏binom(t_i,a_i)) Q_n(a).

Since t_i≤n−1, every nonzero Vandermonde evaluation in this grid must use all n distinct numbers 0,...,n−1. Therefore the script needs only the n! permutations, discards those exceeding an individual t_i, and evaluates the displayed integer sum. The final division is performed over Z and checked to have remainder zero. No integer factorial is inverted modulo p.

## Formal-group extension, independently audited

The field embedding alone treats only elementary groups. The parent effort supplies an integral one-dimensional formal group F(X,Y)=X+Y+higher terms whose p^k-torsion contains every finite abelian p-group of bounded exponent and rank, using a Lubin–Tate formal group over an unramified extension of Q_p of adequate degree. All torsion coordinates lie in the maximal ideal of a common finite extension's ring of integers O.

For distinct coordinates b of A, form g(X)=∏_(b∈A)(X−b), so g≡X^n modulo the maximal ideal. The quotient R=O[x_0,...,x_(n−1)]/(g(x_i)) is finite free. Its multiplication operators satisfy x_i^n∈mR, making formal substitution convergent. Replace each adjacent sum in Q_n by F(x_i,x_(i+1)). In R/mR, reduction is the homogeneous truncation x_i^n=0. Although F modulo m need not be globally additive, the degree-n(n−2) homogeneous component is exactly Q_n. Any coefficient unit among our witnesses therefore makes the resulting remainder nonzero.

Over the fraction field, the roots b are distinct and ordinary CRT/interpolation identifies this quotient with functions on A^n. A nonzero remainder has a nonzero grid evaluation, which gives a single desired cycle by injectivity of the torsion-group embedding and the same adjacent-edge cancellation. Full convergence, torsion embedding, and interpolation details are in `FORMAL_GROUP_AUDIT.md`; the imported theorem and parent exposition are separate from the elementary polynomial calculation.

## Exact remaining gap

The small-n computations do not prove the retained coefficient gcd is a power of 2 for general n. That nonvanishing statement is a concrete algebraic conjecture for this route; it must be proved or falsified before this route can claim all finite abelian odd-p groups. Sparse numerical evidence is not treated as such a proof. The formal-group transfer does not embed mixed-prime finite abelian groups into one maximal ideal, so those groups also remain outside this particular mechanism.
