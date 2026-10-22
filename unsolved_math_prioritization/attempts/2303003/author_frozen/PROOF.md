# A bounded version of Hayman's counterexample to the half-plane 1/2 bound

## Result and attribution

The exact question in UnsolvedMath 2303003 / AMR-022-3003 has a negative answer, already given by W. K. Hayman in *On a theorem of Tord Hall*, Duke Mathematical Journal **41** (1974), 25–26, [DOI](https://doi.org/10.1215/S0012-7094-74-04103-9). The original function and parameter choices are printed on p.25. Hayman–Lingham's [2018 problem list](https://arxiv.org/abs/1809.07200v2), printed p.60, explicitly records this negative answer in Update 3.3.

We give a self-contained verification of that construction using the explicit choice epsilon = 10^-6, and truncate it to obtain a finite, bounded, continuous subharmonic example. The inequalities below are an authored reconstruction, not a transcription of Hayman's p.26, which was not accessible. We claim no novelty for the counterexample or the negative resolution. No assertion about the optimal constant is made.

**Theorem.** For every K>0 there is a continuous subharmonic function u on the right half-plane P={z: Re z>0} such that

- −K ≤ u(z)<0 for every z in P;
- inf_{−π/2<theta<π/2} u(r exp(i theta))=−K for every r>0;
- −K/2<u(r)<0 for every positive real r.

Thus the proposed universal inequality u(r)≤−K/2 fails, indeed simultaneously at all positive real points for this single function.

## 1. Definition

It suffices to construct K=1 and multiply by K. Fix

    c=90,  a=1/100,  epsilon=1/1,000,000,
    eta=c epsilon=9/100,000,
    zeta=sin(eta)+i cos(eta)=i exp(−i eta).

In particular |zeta|=1 and Re zeta>0. Let

    E=(0,1−epsilon) union (1+epsilon,infinity),
    h(x+iy)=(1/pi) integral_E x/[x²+(y−t)²] dt,
    G(z)=log |(z+conjugate(zeta))/(z−zeta)|,
    V(z)=h(z)+(a/pi)G(z),                    z≠zeta.

Set

    u(z)=max{−V(z),−1} for z≠zeta,  and  u(zeta)=−1.

The endpoints omitted from E make no difference to its Poisson integral. Throughout, log is the real natural logarithm of a positive real number. All arctangents below take values in (−pi/2,pi/2).

This is Hayman's p.25 function, divided by −M, expressed as a positive Poisson term plus a positive Green term, before the final truncation. To check agreement directly, if theta=arg z then the Poisson term is

    pi h(z)=theta+pi/2
              −atan((y−1+epsilon)/x)
              −atan((1+epsilon−y)/x).

This identity follows just by integrating x/[x²+(y−t)²]. Our proof uses this two-term expression or the integral itself, and requires no potentially ambiguous arctangent addition formula off the real axis.

## 2. Harmonicity, sign, and subharmonicity

The integral defining h converges because its integrand is O(t^-2) as t tends to infinity. It is harmonic in P: on each compact subset its derivatives through order two are dominated by integrable bounds, so the harmonic Poisson kernels may be differentiated under the integral. Alternatively, the displayed arctangent expression establishes the same local fact directly. The integrand is positive; E and its complement both have positive measure. As the Poisson integral over the full real line is 1, we have 0<h<1.

Writing z=x+iy, zeta=s+it with x,s>0 gives

    |z+conjugate(zeta)|²−|z−zeta|²=4xs>0.

Consequently G>0 on P\{zeta}. The numerator has no zero in P. Its log modulus is harmonic there, and log|z−zeta| is subharmonic. Thus −G is subharmonic on P, with value −infinity at zeta; away from zeta it is harmonic. It follows that −V is subharmonic. The maximum of two subharmonic functions is subharmonic, so u is subharmonic. To recall the elementary reason for the maximum rule: at any center, choose a function attaining the maximum there, apply its submean inequality, and bound its circle averages by those of the pointwise maximum; upper semicontinuity is preserved.

As z approaches zeta, G(z) tends to +infinity, while h remains bounded. Therefore u=−1 on a neighborhood of zeta and the definition at zeta is continuous. Everywhere else u is the maximum of two continuous functions. Since V>0, we have −1≤u<0 in P. This avoids any convention about allowing −infinity in a subharmonic function.

## 3. Every semicircle has infimum −1

### 3.1 Radii outside the short gap

Suppose r>0 and |r−1|>epsilon. The point r is interior to E. As z in P tends to ir, the Poisson integral h(z) tends to 1. For completeness, subtract the full-line Poisson integral: the complement of E has positive distance from r locally, so its nearby contribution tends to zero, while its tail is bounded by an integrable kernel times x. This proves the boundary limit without a boundary regularity assumption on u.

Also G(z) tends to zero there, because its numerator and denominator have equal modulus on the imaginary axis and neither vanishes there. Along the semicircle |z|=r, z→ir from within P, we therefore have V(z)→1 and u(z)→−1. Since u≥−1, the infimum is exactly −1. Attainment in the open half-plane is not needed.

### 3.2 Radii in the gap, including both endpoints

Now suppose |r−1|≤epsilon and choose the interior point z=r zeta. For r=1 this is zeta and u(zeta)=−1. Assume r≠1.

The elementary bounds used below are

    r≥1−epsilon>9/10,
    0<eta<1/2,
    sin eta≥eta−eta³/6≥(9/10)eta.

The sine estimate follows, for example, by integrating cos t≥1−t²/2 on [0,eta]. The cosine estimate follows by integrating sin t≤t, and the latter follows from cos t≤1. Thus these inequalities do not require a numerical trigonometric oracle.

Put x=Re(r zeta)=r sin eta. We obtain

    x≥(81/100)eta>(4/5)eta.

Since |zeta|=1,

    |r zeta+conjugate(zeta)|²
       =(r−1)²+4r sin² eta.

Here sqrt(r)≥9/10, so

    |r zeta+conjugate(zeta)|
       ≥2 sqrt(r) sin eta
       ≥(162/100)eta>eta.

The denominator is |r zeta−zeta|=|r−1|≤epsilon. Consequently

    G(r zeta)>log(eta/epsilon)=log c.

The Poisson integral of the positive real t-axis (before removing the gap) equals (theta+pi/2)/pi. At r zeta, theta=pi/2−eta. The removed gap contributes at most

    integral_(1−epsilon)^(1+epsilon) x/[x²+(y−t)²] dt
      ≤2epsilon/x <5epsilon/(2eta)=5/(2c).

Therefore

    pi V(r zeta)>pi−eta−5/(2c)+a log c.

We have log 90>4: indeed e=sum 1/n!<3, since for n≥2, n!≥2^(n−1), strictly for n≥3; hence e^4<81<90. It follows that a log c>1/25. Finally the exact rational inequality

    eta+5/(2c)=9/100000+1/36 <1/25

shows that V(r zeta)>1. Thus u(r zeta)=−1. This proves the required infimum for every remaining radius, including r=1±epsilon.

## 4. Strict violation at every positive real point

Let x>0 be real and define

    q=2x/(x²+1),  so 0<q≤1.

The full positive-axis Poisson integral at x is 1/2. Integrating the removed interval and subtracting gives

    pi h(x)=pi/2−atan(2epsilon x/(x²+1−epsilon²)).

The arctangent difference formula here is unambiguous: both endpoint angles atan((1±epsilon)/x) belong to (0,pi/2), their difference belongs to (0,pi/2), and its tangent is the displayed positive quantity.

The Green function on this same axis is

    G(x)=(1/2)log[(x²+1+2x sin eta)/(x²+1−2x sin eta)]
        =artanh(q sin eta).

For 0≤t<1 and s≥0, elementary integral bounds give

    artanh t=integral_0^t 1/(1−v²) dv ≤t/(1−t²),
    atan s=integral_0^s 1/(1+v²) dv ≥s/(1+s²).

Because sin eta≤eta<1 and q≤1,

    a G(x)≤a q eta/(1−eta²).

Also

    2epsilon x/(x²+1−epsilon²)≥q epsilon,

so monotonicity of atan and the second integral inequality imply

    atan(2epsilon x/(x²+1−epsilon²))
       ≥atan(q epsilon)
       ≥q epsilon/(1+epsilon²).

The constants satisfy the exact strict inequality

    ac/(1−eta²) < 1/(1+epsilon²),

equivalently

    (9/10)(1+10^-12) < 1−81·10^-10.

Since eta=c epsilon and q epsilon>0, the Green contribution is strictly smaller than the removed interval contribution. Hence

    0<V(x)<1/2.

The truncation is inactive at x, and u(x)=−V(x)>−1/2 for every x>0. Multiplying by any K>0 proves the theorem.

## 5. Scope and verification boundary

This proves the entire catalogue question false. The stronger bound −K/3 reported in the source is compatible with the construction; we neither use nor reprove Hall's theorem. The later question asking for the best universal constant is separate and is not solved here. The source's historical negative answer is not being relabeled a new discovery.

`verify.py` checks exact rational inequalities used above and independently compares elementary numerical formulas at representative points. Its finite samples are diagnostics, not proof of the all-radii or all-axis quantifiers. Those quantifiers, boundary limits, continuity, and subharmonicity are proved analytically above. No formal proof assistant or interval arithmetic proof of transcendental functions is claimed.
