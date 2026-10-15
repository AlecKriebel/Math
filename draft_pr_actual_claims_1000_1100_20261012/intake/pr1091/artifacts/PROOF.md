# Negative answer to the ratio-free rectangle question

Problem: AIM-COMBINATORICS-0229 / 20001104, original AIM Problem 2.4; Croot–Lev's expanded list, §4.9.

## Status and attribution

The precise ratio-free large-rectangle assertion is false. Classification: VERIFIED PRIOR NEGATIVE. The underlying Boolean-cube/basis obstruction is already in the literature: Green and Kane, *An example concerning set addition in F_2^n* (2017), §4 (v1 pages4–5; v2 page5), records A={0,1}^n and B={e_1,...,e_n} in Z^n, attributes the observation to Hosseini, Impagliazzo and Lovett, and states a stronger small-sumset obstruction. The argument below supplies a fully explicit integer embedding and an elementary quantitative proof of the exact AIM quantifier negation. It is an independently written verification of a known construction, not a novelty claim.

Primary current-version URL: https://arxiv.org/pdf/1703.01036v2
Author-hosted version: https://cseweb.ucsd.edu/~dakane/probabilisticallyclosedCounterExample.pdf
The retrieved versions are arXiv:1703.01036v1 (3 March 2017) and v2 (13 November 2017). The relevant §4 remark is present in both. The arXiv abstract-page observation recorded on 10 October 2026 lists v2 as the latest version and describes it as to appear in a special volume of Proceedings of the Steklov Institute. This is a recorded manuscript-status statement, not a new journal-publication verification.

The source uses positive basis vectors. The affine reflection x↦(1,...,1)−x preserves the Boolean cube and changes their signs; thus its construction is equivalent to the one below. Moreover, the AIM conclusion |A′+B′|≤K|A| with |A′|≥c|A| would imply |A′+B′|≤(K/c)|A′|, so the source's stronger obstruction indeed rules out the exact desired rectangle. The explicit argument below does not rely on that stronger assertion.

Tao–Vu, *Additive Combinatorics*, printed p.91 (PDF page111), Exercise2.6.1 gives a different simplex construction, and Exercise2.6.2 asks to modify it to exclude ε=0 in Theorem2.35. This is related background, exactly as Green–Kane describes it; we do not attribute the full Boolean-cube rectangle statement directly to the exercise.

## Construction in the integers

For each integer d≥2 set

A_d = {sum_{i=0}^{d−1} ε_i 3^i : ε_i∈{0,1}},
B_d = {−3^i : 0≤i<d}.

Let m=|A_d|=2^d and n=|B_d|=d. In particular m>n. For a=a(ε) let (a,−3^i) belong to G_d exactly when ε_i=1. Each coordinate is 1 for exactly half the cube, so

|G_d| = d2^{d−1} = mn/2.

The restricted sumset is exactly A_d without its largest element T_d=sum_i3^i: subtracting 3^i from a digit-1 coordinate turns that digit to 0, and conversely every cube point except T_d has a zero digit which can be changed to 1 before that subtraction. Therefore

|A_d +_{G_d} B_d| = 2^d−1 < m.

Thus the hypotheses hold with the fixed constants δ=1/2 and C=1.

## Injection on nonedges

If ε_i=0, then a(ε)−3^i has signed base-3 digits −1 at coordinate i and ε_j∈{0,1} elsewhere. Finite signed base-3 expansions with all digits in {−1,0,1} are unique. Indeed, if two such expansions differ, let r be their highest differing coordinate. Its contribution has absolute value at least 3^r, whereas the total absolute contribution of all lower coordinates is at most

2 sum_{j<r}3^j = 3^r−1.

Consequently different nonedges give different sums: the unique −1 digit recovers i, and the other digits recover ε. They also cannot coincide with edge sums, whose signed digits have no −1.

## Uniform lower bound on every large rectangle

Let A′⊆A_d and B′⊆B_d. Write α=|A′|/m and let J={i:−3^i∈B′}, t=|J|. For ε uniformly distributed on {0,1}^d define

X(ε)=#{i∈J:ε_i=0}.

The selected bits are independent, so E X=t/2 and Var X=t/4. In particular

sum_{ε∈{0,1}^d}(X(ε)−t/2)^2 = mt/4.

The number N of nonedges in A′×B′ therefore satisfies Cauchy–Schwarz:

N = sum_{a(ε)∈A′}X(ε)
  ≥ |A′|t/2 − sqrt(|A′| sum_{ε}(X(ε)−t/2)^2)
  = m[αt/2 − sqrt(αt)/2].

By the nonedge injection,

|A′+B′| ≥ m[αt/2 − sqrt(αt)/2].                 (1)

If αt≥4, then sqrt(αt)/2≤αt/4, and hence

|A′+B′| ≥ αtm/4.                               (2)

For any fixed 0<c≤1, if |A′|≥cm and |B′|≥cn=cd, then αt≥c²d. Consequently, whenever d≥4/c²,

|A′+B′| ≥ (c²d/4)m.                            (3)

The estimates hold for every choice of A′ and B′, with no union bound and no exceptional coordinate subset.

## Quantifier negation

Given any proposed constants c>0 and K>0 for δ=1/2,C=1, the assertion is already impossible if c>1. For 0<c≤1 choose an integer

d > max{2,4/c²,4K/c²}.

The construction satisfies all AIM hypotheses. But every pair of subsets meeting the required retained-size bounds satisfies, by (3),

|A′+B′| > Km.

This refutes the requested uniform statement. The imbalance m/n=2^d/d is allowed to grow; excluding it would change the original problem.

## Compatibility with other structural statements

Writing S=A+_G B, an inclusion of a retained rectangle sumset in S+S−S can still be true: it gives no O(m) bound here without a bound on that container. The existing asymmetric-BSG results with imbalance losses are also consistent with this example. The present conclusion is not inferred from the failure of an approximate-group theorem; it follows by an explicit count of distinct sums in every eligible rectangle.

The original source asks a broad preliminary question about structure, followed by the precise rectangle question. Only the latter concrete assertion is refuted here; this does not assert that all possible structural conclusions fail.

## Verification scope

The proof is analytic and valid for all d. Finite tests are supplementary and do not replace its quantifier argument. The primary construction appears in Green–Kane's §4 over Z^n; the integer embedding and exact graph are verified directly above. This AI-assisted, unrefereed edition includes the authored proof and audit, with public bibliographic and source-identity metadata. It does not claim external human peer review, journal acceptance or formal proof-assistant certification.
