# Function Theory 7.17: sampled exponential type in a half-plane

Problem ID: 2307017 (AMR-022-7017). Research checkpoint: 2026-10-04.

## Result and scope

The standard, distinct-integer interpretation is already solved in the literature. Hayman–Lingham's 2018 Update 7.17 explicitly credits Korevaar and Zeinstra (1985), and also cites Zeinstra (1992). This note supplies an independent reconstruction using elementary estimates and the classical Blaschke and positive-harmonic representations. It makes no novelty claim. It remains subject to independent audit.

**Theorem.** Let f be bounded and holomorphic on H = {z: Re z > 0}. Let alpha be real with |alpha| < pi/2, and let R be a subset of the positive integers with sum_{n in R} 1/n = infinity. With log 0 = -infinity,

    limsup_{n in R, n -> infinity} log |f(n exp(i alpha))| / n
      = limsup_{r -> infinity} log |f(r exp(i alpha))| / r.

If f is not identically zero, both quantities equal -a cos(alpha), where a >= 0 is the mass at infinity in the positive-harmonic representation of -log|f/B| after normalization and removal of its Blaschke zero factor B. In particular both quantities are finite.

Here exponential type means the signed logarithmic limsup, not a pointwise limit and not log-plus type. A strictly increasing sequence of positive integers is equivalent to the subset formulation. The printed source does not explicitly require distinct or increasing samples. We interpret its classical claim as a theorem about distinct positive integers, equivalently an increasing sequence; this is consistent with the separated-sampling hypothesis in the cited literature. If arbitrary repetitions are permitted, the literal statement is false: Section 6 gives a counterexample even when the repeated sequence tends to infinity.

## 1. Classical representation input

Multiplication of f by a nonzero constant does not change either type, so assume 0 < ||f||_infinity <= 1. List the zeros a_j = u_j + i v_j in H with multiplicity. The half-plane Blaschke theorem gives

    sum_j beta_j < infinity,       beta_j = u_j / (1 + |a_j|^2),

and a Blaschke product B with precisely these zeros. The zero-free quotient F = f/B is holomorphic and has |F| <= 1. Consequently h = -log|F| is nonnegative and harmonic. The positive-harmonic representation in H is

    h(x+iy) = a x + x integral_R [((y-t)^2+x^2)^(-1)] d nu(t),
    a >= 0,       integral_R (1+t^2)^(-1) d nu(t) < infinity.             (1)

The normalization of nu absorbs any conventional factor 1/pi.

These are classical representation theorems, not assumptions specific to this problem. For completeness, the zero condition follows by transporting Jensen's formula from the unit disc through w=(z-1)/(z+1):

    1-|w|^2 = 4 Re z / |z+1|^2,
    1+|z|^2 <= |z+1|^2 <= 2(1+|z|^2).

Thus the disc Blaschke condition is equivalent to the displayed half-plane condition. Dividing a bounded disc function successively by the finite Blaschke factors preserves its unit sup norm by the Schwarz lemma. Local convergence of the Blaschke products then proves |F| <= 1. Formula (1) is the Poisson representation of a positive harmonic disc function, with the atom at the boundary point corresponding to infinity separated from the remaining measure. One obtains that disc representation by weak compactness of the positive measures h(r exp(i theta)) d theta/(2 pi), whose total mass is h(0), and the Poisson formula. This also covers h=0.

Set q=exp(i alpha), c=cos(alpha)>0, s=sin(alpha). From (1),

    h(rq)/r = a c + c integral_R [r^2-2 r s t+t^2]^(-1) d nu(t).

Since

    r^2-2 r s t+t^2 >= (1-|s|)(r^2+t^2),

for r>=1 the integrand times 1+t^2 is bounded by 1/(1-|s|), and tends pointwise to zero. Dominated convergence with respect to the finite measure d nu(t)/(1+t^2) yields

    h(rq)/r -> a c.                                                     (2)

## 2. Blaschke potentials and a small exceptional set

For a=u+iv in H, write R_a=|a| and

    g_a(r) = log |(rq+conjugate(a))/(rq-a)|
           = (1/2) log(1+4 r c u / |rq-a|^2) >= 0.                       (3)

Away from the zeros, -log|B(rq)| = sum_j g_{a_j}(r). At a zero the two sides have the same value +infinity. Unimodular normalizations of the factors do not affect (3).

Let E0 contain all integers n < 1/c, and all remaining positive integers n for which |nq-a_j|<1/4 for at least one zero. The discs of radius 1/4 about distinct nq are disjoint, so one can select a different zero for each of the latter integers. For such a selected zero,

    u >= cn-1/4 >= cn/2,      |a| <= n+1/4,
    beta_a >= cn/[2(1+(n+1/4)^2)] >= c/(6n).

Here n>=1/c and n>=1. Hence

    sum_{n in E0} 1/n < infinity.                                      (4)

For n outside E0 all distances |nq-a_j| are at least 1/4.

Call a zero local to n if

    n/2 <= |a| <= 2n      and      Re a >= cn/2.                         (5)

Write L(n) for the sum of g_a(n) over the local zeros, and D(n) for the sum over all other zeros. These are nonnegative extended sums.

## 3. The nonlocal part is uniformly sublinear

The inequality log(1+x)<=x in (3) gives

    g_a(n)/n <= 2 c u / |nq-a|^2.                                      (6)

Partition the nonlocal zeros into three disjoint regions.

* If |a|<n/2, then g_a(n)/n <= 8 c u/n^2. Relative to beta_a, this has multiplier 8c(1+|a|^2)/n^2 <= 10c for n>=1. For each fixed a it tends to zero. Summability of beta_a and dominated convergence give a total tending to zero.
* If |a|>2n, then g_a(n)/n <= 8c u/|a|^2 <= 10c beta_a. The total tends to zero as a tail of the summable series.
* If n/2<=|a|<=2n and u<cn/2, then |nq-a|>=cn/2. Thus g_a(n)/n <= (8/c)u/n^2 <= (40/c)beta_a. Again this is a tail, because |a|>=n/2.

Therefore

    D(n)/n -> 0.                                                       (7)

The preceding estimates also show that D(n) is finite. They do not require any regular density of the sampling integers or zeros.

## 4. A summable estimate for the local part

Fix a zero a that is local to at least one integer n, and put R=|a|. Then R>=1/2 and all such integers lie in [R/2,2R]. Let p=Re(a conjugate(q)). For n outside E0,

    |nq-a| >= max(1/4, |n-p|),       |nq+conjugate(a)| <= 3R.

It follows that

    g_a(n) <= log^+(3R/max(1/4,|n-p|)).                                (8)

For every T>0, at most 2T+2 integers satisfy |n-p|<T. The layer-cake identity applied to the right side of (8), now summed over all integers, gives

    sum_{n local, n not in E0} g_a(n)
       <= integral_0^{log(12R)} (6R exp(-t)+2) dt
       <= 6R + 2 log(12R) <= 14R.                                    (9)

The last inequality holds for R>=1/2, since log(12R)<=4R. Also n>=R/2, so

    sum_{n local, n not in E0} g_a(n)/n^2 <= 56/R.

If there is any local n, (5) gives u>=cR/4. Since R>=1/2,

    beta_a = u/(1+R^2) >= c/(20R).

Consequently each zero satisfies

    sum_{n local, n not in E0} g_a(n)/n^2 <= (1120/c) beta_a.            (10)

If there are no local n, the left side is zero. Tonelli's theorem and the Blaschke condition now yield

    sum_{n not in E0} L(n)/n^2 < infinity.                              (11)

For every epsilon>0, the set

    E_epsilon = E0 union {n not in E0: L(n)>=epsilon n}

therefore has finite reciprocal sum. In particular L(n) is finite for each n outside E0.

## 5. Completion of the theorem

Let R be the specified set of distinct integers with divergent reciprocal sum. For every epsilon>0, R minus E_epsilon still has divergent reciprocal sum, hence contains arbitrarily large integers. Combining (7) with the definition of E_epsilon proves

    liminf_{n in R, n -> infinity} [-log|B(nq)|]/n = 0.                  (12)

More explicitly, choose n_k in R minus E_{1/k}, increasing, large enough that D(n_k)/n_k<1/k. Then -log|B(n_k q)|/n_k<2/k.

Since log|f|=log|B|-h, equations (2) and (12) give sampled limsup -ac. For every positive r the inequality log|B(rq)|<=0 and (2) give ray limsup at most -ac; the sampled subsequence gives the reverse inequality. This proves equality. If f is identically zero, both types are -infinity by convention, so the excluded case is immediate.

No estimate is uniform as |alpha| tends to pi/2. The two boundary rays are outside the open half-plane hypothesis. No ordinary limit is asserted: sparse sample zeros may persist.

## 6. Why repetitions change the problem

Take alpha=0 and

    B(z) = product_{k>=1} (2^k-z)/(2^k+z).

The product converges locally uniformly on H, is not zero identically, has |B|<=1, and vanishes at every 2^k. These statements follow either from the Blaschke theorem or directly from the uniform summability of 2z/(2^k+z) on compact sets, together with each factor's modulus bound.

Form a sequence by repeating 2^k exactly 2^k times, in order of k. This sequence tends to infinity and its reciprocal sum diverges (each block contributes 1). Its sampled type is -infinity.

Its ray type is 0. To verify the lower bound without using the theorem above, put x_m=3*2^{m-1}. Then

    |B(x_m)| = product_{j>=2-m} |(2^j-3)/(2^j+3)|.

The product over all integer j is a positive constant C: no factor is zero, and the defects from 1 are summable, bounded by geometric tails at both ends. Therefore |B(x_m)|>=C>0, while |B(x)|<=1. Dividing logarithms by x_m proves ray type 0. Thus arbitrary repetition invalidates the claim. It is a wording caveat, not a novel disproof of the classical distinct-sampling theorem.

## References and attribution

1. W. K. Hayman and E. F. Lingham, Research Problems in Function Theory, arXiv:1809.07200v2 (2018), printed p. 165, Problem and Update 7.17; bibliography items [489] and [812]. https://arxiv.org/abs/1809.07200
2. J. Korevaar and R. Zeinstra, Transformées de Laplace pour les courbes à pente bornée et un résultat correspondant du type Müntz–Szász, C. R. Acad. Sci. Paris, Sér. I 301 (1985), 695–698. Cited as the resolution by reference 1; full text not recovered in this attempt.
3. R. Zeinstra, Zeros and regular growth of Laplace transforms along curves, J. reine angew. Math. 424 (1992), printed pp. 1–15, especially Section 6, Theorem 4, pp. 11–12. https://doi.org/10.1515/crll.1992.424.1 . This theorem is stated for finite complex Borel measures on curves. It is corroborating literature; the proof above does not assume that every bounded analytic function is such a transform.
4. M. Bonk, Conformal Invariant Processes in the Plane, Theorem 7.6, positive-harmonic representation. https://www.math.ucla.edu/~mbonk/252a.1.16f/InvPro.pdf

The primary source problem is credited to J. Korevaar; the resolution is credited to Korevaar and Zeinstra. This reconstruction asserts no priority for its proof method or intermediate estimates.
