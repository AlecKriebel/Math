# Proof 19  A fixed counterexample on zero two seven

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Circuit obstructions and positive uncentered blocks](01_circuit_obstructions.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## Theorem

Let z be Haar-uniform on the unit circle. For every real p with 4<p<6,

    integral |8+11z²+10z⁷|^p < integral |8−11z²+10z⁷|^p.

Thus the three-frequency set {0,2,7} fails the real constant-one majorant property throughout the entire open exponent interval (4,6). Translation, nonzero integer dilation, and reflection give the corresponding equivalent frequency sets. The fixed tuple works on the whole open exponent interval; this chapter does not classify other triples.

## 1. Uniform convergent series with the endpoint zeros removed

Put q=p/2, P_+=8+11z²+10z⁷, P_−=8−11z²+10z⁷, S_±=|P_±|², M=29²=841, and U_±=1−S_±/M. The triangle inequality gives 0≤U_±≤1. Write μ_j^±=CT(U_±^j), where CT is the constant Laurent coefficient, equal to normalized Haar integration.

The binomial series for (1−u)^q is absolutely uniformly convergent on 0≤u≤1 for q>0. The two S-distributions have the same moments through degree 6: the primitive affine relation (5,−7,2) has mass 7, so no sign-sensitive pair of k-fold sums occurs for k<7. Alternatively this equality can be checked directly in the Laurent polynomials for k≤6. In particular μ_j^+=μ_j^− for j=0,1,2,3.

For j≥4 and 2<q<3, define

    w_j(q) = [product from r=4 to j−1 of (r−q)] / j!,

with the empty product 1. Then

    (−1)^j binom(q,j) = −q(q−1)(q−2)(3−q) w_j(q).

Consequently the plus-minus norm-power difference is

    D_p = −M^q q(q−1)(q−2)(3−q) F(q),
    F(q) = sum from j=4 to infinity of w_j(q)(μ_j^+−μ_j^−).

Every factor preceding F(q), apart from the displayed minus sign, is positive on 2<q<3. It remains to prove F(q)>0. The normalized series also converges at both closed endpoints q=2,3. All its weights are nonnegative and nonincreasing in q∈[2,3].

The exact tail identity, for N≥4, is

    sum from j>N of w_j(q) = product from r=4 to N of (r−q)/(q N!)
                           = (N+1)w_(N+1)(q)/q.

For 2<q<3 it follows from the finite binomial-sum identity and the vanishing infinite binomial sum, after division by q(q−1)(q−2)(3−q). Direct telescoping, or continuity, gives q=2 and q=3 as well. Since U_±^j≤U_±^(N+1) for j>N,

    |F(q)−sum_(j=4)^N w_j(q)(μ_j^+−μ_j^−)|
    ≤ [(N+1)w_(N+1)(q)/q](μ_(N+1)^++μ_(N+1)^−).

This provides a uniform, exact, convergent tail bound; no numerical quadrature enters.

## 2. Exact moment computation

The two integer Laurent polynomials are

    M U_± = 556 ∓88(z²+z^(−2)) ∓110(z⁵+z^(−5)) −80(z⁷+z^(−7)).

Their integer coefficients are convolved through power N+1. Dividing each constant coefficient by M^j gives μ_j^± exactly. To keep subsequent arithmetic small, each rational moment is enclosed between floor(2^160 μ_j)/2^160 and ceil(2^160 μ_j)/2^160. These bounds are formed by integer division of the exact numerator and denominator.

## 3. Uniform interval verification

The program [certify_uniform_027.py](../certificates/certify_uniform_027.py) uses N=256 and divides the closed q interval [2,3] into 256 adjacent rational bins

    [2+k/256, 2+(k+1)/256],  k=0,...,255.

On each bin, the lower and upper bounds on w_j are propagated using the exact recurrence

    w_4(q)=1/24,
    w_j(q)=w_(j−1)(q)(j−1−q)/j.

The right endpoint gives a lower bound and the left endpoint an upper bound. Every multiplication/division is rounded outward on the 2^(-160) grid using integer floor or ceiling. For each summand, all four products of weight and moment-difference interval endpoints are compared, again with outward rounding. The lower finite-sum bound minus the upper tail bound is positive on every bin.

Saved exact output [certify_uniform_027.json](../certificates/certify_uniform_027.json) records the minimum lower bound

    152688347388779894298590457794782099679820 / 2^160 > 0.

Its decimal display is about 1.0447360679501536×10^(−7); the decimal display is not used in acceptance. The worst bin is k=255. The script raises an exception unless the exact lower numerator is strictly positive. Thus F(q)>0 for all q∈[2,3], proving the theorem on the open p interval.

## Scope

This is one fixed, rational-coefficient witness valid at every exponent in (4,6). It is not a numerical absence-of-counterexamples argument, a local Taylor test, an assertion about {0,2,5}, or a complete classification of three-point supports. The factorization explicitly retains equality at p=4 and p=6. The additional fixed K=9 and K=11 witnesses are proved separately in [Proof 20](20_uniform_029_0211.md).
