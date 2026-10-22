# Authored verification of scoped results

This document is a mathematical reproduction and set of controls for already-existing work. The general negative answer is explicitly attributed to DannyExperiments (2026), whose result is stronger than the odd-index statement below. The sector calculation is based on the Taylor-remainder method in E. Deniz, M. Çağlar, R. Szász, arXiv:1906.09498v1 (2019), not a novelty claim. No full-circle β=1 proof is supplied here.

## 1. Finite coefficient extraction and the fifth-degree witness

The binomial expansions of (1+xz)^α and (1−z)^(−β) converge absolutely for |z|<1. Their Cauchy product gives

A_j(α,β,x)=Σ_{k=0}^j binom(α,k)(β)_{j−k}x^k/(j−k)!.

At x=−1, the two analytic powers use the same normalized logarithm, so the generating germ equals (1−z)^(α−β). Consequently

A_j(α,β,−1)=(−1)^j binom(α−β,j).

For α=3/2, β=1/32, j=5, the coefficients of x^0,…,x^5 in A₅ are

1789359/268435456,
208065/16777216,
2145/524288,
−33/32768,
3/4096,
−3/256.

Summing gives 2997183/268435456. Summing with alternating signs gives 3171231/268435456; this also equals −binom(47/32,5). Both are positive and their difference is

(3171231−2997183)/268435456 = 5439/8388608 > 0.

The parameter conditions α>0, β>0, |x|=1 and odd j≥5 all hold. This proves the stated failure without approximation and even if an absolute value is inserted on the right-hand side.

## 2. Reproduction of the published cubic witness

At degree three,

A₃(x)=β(β+1)(β+2)/6 + αβ(β+1)x/2
       + α(α−1)βx²/2 + α(α−1)(α−2)x³/6.

Write s=α+β and d=α−β. Expanding the preceding finite polynomial at ±1 yields

A₃(1)=s(s²−3d+2)/6,
A₃(−1)=−d(d−1)(d−2)/6.

For the published witness α=3/2, β=1/14, one has s=11/7, d=10/7 and hence

A₃(1)=33/686,
A₃(−1)=20/343=40/686,
|A₃(−1)|−A₃(1)=1/98.

This degree-three example alone would not demonstrate failure at degree five. The distinct witness in section 1 addresses that index, and the exact script checks that reusing β=1/14 at degree five does not yield a violation.

## 3. Rational witnesses at every odd degree, by continuity

The following argument verifies an odd-index subcase of the already-published stronger every-index theorem, by a different elementary route.

Fix any odd j=2m+1≥3 and set α=3/2. Let P(β)=A_j(3/2,β,1), a real polynomial in β. Since the number of negative factors in binom(3/2,j) is j−2, which is odd,

P(0)=binom(3/2,j)<0.

At β=1/2, the generating germ simplifies exactly:

(1+z)^(3/2)(1−z)^(−1/2)=(1+z)²(1−z²)^(−1/2).

Thus P(1/2)=2 binom(2m,m)/4^m>0. There is at least one root in (0,1/2). Let r be the largest such root; it exists because P is a nonzero polynomial with finitely many roots. Then P(β)>0 on (r,1/2].

For β∈(0,1/2), d=3/2−β lies in (1,3/2). The binomial coefficient binom(d,j) has exactly j−2 negative factors and is strictly negative. Therefore

Q(β):=A_j(3/2,β,−1)=−binom(3/2−β,j)>0

throughout this interval, including at r. At r one has Q(r)>P(r)=0. Continuity supplies δ>0 such that r+δ<1/2 and Q(β)>P(β) whenever r<β<r+δ. Rational density then supplies a rational β in this interval. It follows that

0<A_j(3/2,β,1)<|A_j(3/2,β,−1)|.

Both parameters are rational and positive. This establishes existence for every odd j≥3. It does not identify one fixed β that works for every j, and it makes no assertion in the unit square because α=3/2.

## 4. Endpoint identities for the original domain

Assume 0<α<1 and β=1. Put S_j(x)=Σ_{k=0}^j binom(α,k)x^k. The alternating-binomial identity gives

S_j(−1)=(−1)^j binom(α−1,j)=Π_{r=1}^j(1−α/r)>0.

This identity can be proved from Pascal's recurrence, or from the generating-germ cancellation in section 1. For odd j, S_j(1)>2^α: Taylor's integral remainder for f(w)=(1+w)^α has negative derivative f^(j+1)(t) on t∈[0,1], hence f(1)−S_j(1)<0. In particular the original right-hand side is positive. Also S_j(−1)<1<2^α<S_j(1), proving the original inequality at x=−1; x=1 is equality.

## 5. An all-odd-degree sector lemma (partial result only)

**Claim.** For 0<α<1, every odd j≥1, and x=e^(iθ) with 2π/3≤|θ|≤π,

|S_j(x)|<S_j(1).

It is enough to consider 2π/3≤θ<π; conjugation handles negative angles and polynomial continuity handles θ=π. Let

B=Π_{r=1}^j(1−α/r),  y=−cos θ∈[1/2,1),
r=|1+x|=sqrt(2−2y),  D(t)=1+t²−2ty.

Taylor's integral remainder along the segment from 0 to x gives

S_j(x)=(1+x)^α + αB x^(j+1) ∫₀¹(1−t)^j(1+tx)^(α−j−1)dt.

The sign is plus because j is odd and the (j+1)-st derivative of (1+w)^α has a negative real scalar factor. The chosen branch is analytic on this segment when x≠−1. Taking absolute values yields

|S_j(x)| ≤ r^α + αB I_j(y),
I_j(y)=∫₀¹ [(1−t)/sqrt(D(t))]^j D(t)^((α−1)/2)dt.

Since D(t)−(1−t)²=2t(1−y)≥0, the bracket lies in [0,1]; hence I_j≤I₁. Furthermore 0<D(t)≤1 for 0≤t≤1 and y≥1/2. Splitting 1−t=(1−y)−(t−y) gives

I₁=(1−y)∫₀¹D(t)^(α/2−1)dt − ∫₀¹(t−y)D(t)^(α/2−1)dt
   ≤ (1−y)∫₀¹D(t)^(−1)dt + (1−r^α)/α
   = C(y)+(1−r^α)/α.

Here

C(y)=sqrt((1−y)/(1+y))·[arctan sqrt((1−y)/(1+y))
                         + arctan(y/sqrt(1−y²))].

Set u=sqrt((1−y)/(1+y))∈(0,1/sqrt(3)]. The angle identity reduces this to

C(y)=u(π/2−arctan u).

Its derivative with respect to u is π/2−arctan u−u/(1+u²)>0 on this interval: the first two terms are at least π/3 and the last is at most sqrt(3)/4. Therefore

0<C(y)≤π/(3sqrt(3))<2/3<log 2.

For a fully elementary constant comparison, π<22/7<2sqrt(3) proves the first strict inequality; log 2>2/3 follows from log((1+t)/(1−t))>2t at t=1/3, by integrating 2/(1−t²)>2.

Using 0<B<1 and 0≤r≤1,

|S_j(x)| ≤ (1−B)r^α+B+αBC(y)
          ≤ 1+αBC(y)
          < 1+α log 2
          ≤ 2^α
          < S_j(1).

The last inequality was established in section 4, and the preceding one is exp(v)≥1+v. This proves the sector claim. The argument leaves the sector 0<|θ|<2π/3 unresolved; it must not be described as a full proof.

## 6. Recurrence control

Logarithmic differentiation of F gives

(1+(x−1)z−xz²)F'(z)=[αx+β+x(β−α)z]F(z).

Equating coefficients proves, for n≥1,

(n+1)A_{n+1}=[αx+β−n(x−1)]A_n+x(n−1+β−α)A_{n−1}.

This is an exact recurrence and a check on coefficient extraction. Taking absolute values in it loses phase information and does not establish the desired sharp maximum at x=1. No inductive proof is claimed from the recurrence alone.
