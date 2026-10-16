# A capped-cylinder counterexample to the weighted Yamabe heat-trace comparison in dimension three

## 1. Statement and scope

This note addresses Carlo Morpurgo's Conjecture 1 in section 9, item (16),
pages 421–422 of *Low Eigenvalues of Laplace and Schrödinger Operators*,
Oberwolfach Reports 6 (2009), 355–428,
[DOI 10.4171/OWR/2009/06](https://doi.org/10.4171/OWR/2009/06).
The problem is catalogued as OWR-3389-021 / 30001168.

Write the positive Laplacian as Δ. On the unit round sphere (S^n,g₀),
the operator in that question is

    Y₀ = Δ_g₀ + n(n−2)/4.

For a smooth strictly positive W with
∫ W^(n/2) dv_g₀ = vol(S^n,g₀), its weighted realization is

    Y_W = W^(−1/2) Y₀ W^(−1/2) on L²(dv_g₀).

The proposed inequality compares the largest value over t>0 of
t^(n/2) Tr(exp(−tY_W)) with the analogous largest value for W=1.

**Theorem.** In dimension n=3 there is a smooth strictly positive normalized
weight W such that, at an explicitly defined time t_*,

    t_*^(3/2) Tr(exp(−t_*Y_W)) > 13/20,

whereas for every t>0,

    t^(3/2) Tr(exp(−tY₀)) < 129/200.

Consequently the proposed comparison, quantified over n≥3, is false.
The separation between these two rational thresholds is 1/200.
This result says nothing decisive about its restriction to n≥4, or the
separate n≥4 monotonicity question OWR-3389-022 / 30001169.

The geometric and spectral reasoning is proved below. Only the elementary
finite rational inequalities in Lemma 1 use the accompanying certificate.
No claim of historical priority, journal publication, or independent human
peer review is made.

## 2. A uniform bound for the round three-sphere

**Lemma 1.** Let

    F₀(t) = t^(3/2) Σ_{j=1}^∞ j² exp(−t(j²−1/4)).

Then F₀(t)<129/200 for all t>0.

The eigenvalue j²−1/4 has multiplicity j² on the round S³: it comes
from degree j−1 spherical harmonics, whose Laplace eigenvalue is j²−1.
Thus F₀ is exactly the required round heat trace, including the positive
potential 3/4 and all multiplicities.

For 0<t≤1, Gaussian Poisson summation and differentiation give

    t^(3/2) Σ_{j=1}^∞ j² e^(−tj²)
      = (√π/4) [1 + 2 Σ_{m=1}^∞
          (1−2π²m²/t) exp(−π²m²/t)].

For completeness, differentiate
Σ_{j∈Z}exp(−tj²)=√(π/t) Σ_{m∈Z}exp(−π²m²/t),
then multiply by −t^(3/2)/2. Termwise differentiation is justified
uniformly on compact positive-time intervals by Gaussian decay.
Every term in the correction sum is negative when t≤1. Therefore

    F₀(t) ≤ (√π/4)e^(1/4)
          < (1773/1000)/3 = 1773/3000 < 129/200.

Here √π<1773/1000, and the exponential series is strictly less than
the geometric series Σ_{k≥0}(1/4)^k=4/3.

For 1≤t≤2, partition into the 100 closed intervals

    [a,b]=[k/100,(k+1)/100],  k=100,...,199.

On each interval,

    F₀(t) ≤ b√b [ Σ_{j=1}^3 j² e^(−a(j²−1/4))
                         + 32 e^(−63a/4) ].                    (1)

To check the tail, for j≥4 and a≥1 the ratio of consecutive summands is

    ((j+1)/j)² exp(−a(2j+1))
       ≤ (25/16)e^(−9) < 1/2.

The last strict inequality already follows from e^9>1+9.
The entire tail from j=4 is consequently bounded above by twice its
first term, namely 32e^(−63a/4).

Every one of the 100 bounds (1) is strictly below 129/200.
Here is the full reproducible arithmetic specification, rather than
a floating-point sampling claim:

1. Replace √b by r_b=(floor(10^9√b)+1)/10^9, calculating the floor
   with integer square root. Direct rational squaring verifies r_b²>b.
2. Replace each e^(−x), x>0, by 1/P₆₄(x), where
   P₆₄(x)=Σ_{m=0}^{64}x^m/m!. Since P₆₄(x)<e^x, this is an upper bound.
3. Compare

       b r_b [ Σ_{j=1}^3 j²/P₆₄(a(j²−1/4))
                            +32/P₆₄(63a/4) ]

   with 129/200 by exact rational arithmetic for all integer k=100,...,199.

`certificate.py` implements precisely these comparisons. Their largest
upper bound is less than 0.643380136594, occurring on [189/100,190/100].
This displayed decimal is rounded upward; the acceptance comparisons
themselves use fractions only.

Finally, each function t^(3/2)exp(−λt) is nonincreasing for
t≥3/(2λ). All the round eigenvalues satisfy λ≥3/4, so F₀ is
nonincreasing for t≥2. The last interval already bounds F₀(2).
This proves the lemma, including all small and large times.

## 3. An explicit smooth conformal metric with a long exact cylinder

Let L=10000. Identify the twice-punctured sphere with R×S² so that

    g₀ = sech²(s) (ds²+g_S²).

For example, this follows from stereographic polar radius r=e^s in
g₀=4(dr²+r²g_S²)/(1+r²)².

Define the standard smooth step function

    η(x)=0 for x≤0, and η(x)=exp(−1/x) for x>0;
    χ(x)=η(x)/(η(x)+η(1−x)).

Then χ=0 on (−∞,0], χ=1 on [1,∞), 0≤χ≤1, and χ is smooth
with all required endpoint derivatives vanishing. Put

    q(s)=|s|−L/2,
    u(s)=exp(−χ(q(s)) log cosh(q(s))),
    g_L=u(s)² (ds²+g_S²).

Although |s| alone is nonsmooth at zero, u is identically 1 in a whole
neighborhood of zero, so u is smooth on R. It is also smooth at the
two transition points because χ is flat at zero and one.

On |s|≤L/2, u=1. Thus g_L contains the exact product cylinder of
length L and unit S² radius. For |s|≥L/2+1,

    u(s)=sech(|s|−L/2).

The conformal weight relative to the round sphere before volume
normalization is W_L(s)=u(s)² cosh²(s). At the positive pole, in
the smooth stereographic radius ρ=e^(−s), it is exactly

    W_L = e^L (1+ρ²)²/(1+e^L ρ²)².

This is a smooth strictly positive radial function of the Euclidean
coordinates through ρ=0. The identical calculation at the negative pole
uses ρ=e^s. Hence g_L extends to a smooth metric on the whole standard
S³ and W_L extends to a smooth strictly positive weight there. L is a
fixed finite number, not a singular limiting parameter in the theorem.

Write V_L=vol(S³,g_L). Since the S² area is 4π,

    V_L = 4π ∫_R u(s)³ ds ≤ 4π(L+4).                       (2)

Indeed, each cap has integral at most

    ∫₀¹1 dq + ∫₁^∞ sech³(q)dq
      ≤ 1+∫₁^∞8e^(−3q)dq
      = 1+8/(3e³) < 2.

No curvature bound on the transition region is needed.

## 4. Spectral comparison using compactly supported trial functions

For any three-dimensional metric h, use the geometric Yamabe operator

    Y_h = Δ_h + R_h/8.

Inside the exact cylinder, its scalar curvature is 2, so

    Y_{g_L} = −∂²_s + Δ_S² + 1/4.                           (3)

Take the S²-constant Dirichlet modes on the cylinder, extended by zero
to the rest of the sphere:

    φ_k(s,ω)=sin(πk(s+L/2)/L),  −L/2<s<L/2,  k=1,2,... .

The extensions belong to the quadratic-form domain H¹(S³,g_L).
They vanish at the two interfaces; a jump of their normal derivative
does not prevent H¹ membership and introduces no extra quadratic-form
term. The form and L² inner products on their span are exactly those
on the cylinder. On the span of φ₁,...,φ_k, the largest Rayleigh
quotient is

    μ_k = 1/4 + (πk/L)².

Let λ_k(g_L), k≥1, be the full closed-manifold spectrum with
multiplicity. The min–max principle gives λ_k(g_L)≤μ_k, so

    Tr(exp(−4Y_{g_L}))
      ≥ e^(−1) Σ_{k=1}^∞ exp(−4π²k²/L²).                  (4)

This argument deliberately uses only the S²-constant trial subspace.
It requires no truncation of the actual closed spectrum, no assumption
that the caps decouple, and no convergence of spectra as L tends to infinity.

The operator on the whole sphere is positive. One way to see this is
the conformal covariance in the next section: it is unitarily equivalent
to W_L^(−1/2)Y₀W_L^(−1/2), whose quadratic form is strictly positive.
All heat traces in (4) therefore exist and have positive summands.

For the decreasing Gaussian G(x)=exp(−4π²x²/L²),

    Σ_{k=1}^∞ G(k) ≥ ∫₁^∞G(x)dx ≥ ∫₀^∞G(x)dx−1
                      = L/(4√π)−1.                       (5)

Thus even an elementary integral bound suffices in (4).

## 5. Correct volume, measure, normalization, and heat time

Set

    a=(2π²/V_L)^(2/3),   h=a g_L,
    W=a W_L,             t_*=4a.

Since vol(S³,g₀)=2π² and dv_h=W^(3/2)dv_g₀,

    ∫_{S³}W^(3/2)dv_g₀=vol(S³,h)=a^(3/2)V_L=2π².

This is the exact normalization asked for. In particular the weight
is integrated with the round volume measure, not ds dω.

For h=Wg₀ the conformal covariance identity is

    Y_h = W^(−5/4)Y₀W^(1/4).

Multiplication U:f↦W^(3/4)f is unitary from L²(dv_h) to L²(dv_g₀)
and satisfies UY_hU^(−1)=W^(−1/2)Y₀W^(−1/2)=Y_W.
This also verifies that the weighted operator is the one in the question,
including its Hilbert-space measure and both exterior weight powers.

A constant metric rescaling gives Y_h=a^(−1)Y_{g_L}. The selected time
t_*=4a therefore yields the exact identity

    t_*^(3/2)Tr(exp(−t_*Y_W))
      = 8a^(3/2)Tr(exp(−4Y_{g_L}))
      = (16π²/V_L)Tr(exp(−4Y_{g_L})).

Using (2), (4), and (5),

    t_*^(3/2)Tr(exp(−t_*Y_W))
      ≥ (4π/[e(L+4)]) (L/(4√π)−1)
      = (√π/e) (L−4√π)/(L+4).                             (6)

The elementary bounds √π>1.772, √π<1.773, e<2.719 and L=10000
give the strict rational lower bound

    (√π/e)(L−4√π)/(L+4)
      > (1772/2719)(10000000−7092)/10004000
      = 1106714561/1700054750
      > 13/20.                                             (7)

Each positive factor was bounded separately in the appropriate direction.
The exact rational checker verifies (7), as well as its π and e enclosures.

Combining (7) and Lemma 1 proves the theorem. If the word “max” is
interpreted literally instead of as a supremum, there is no issue:
each smooth positive operator has scaled trace tending to zero at infinity
and to √π/4 at zero; the constructed value exceeds that zero-time limit.
The round trace also exceeds its zero-time limit, for example at t=2,
as is immediate from its first eigenvalue contribution. Hence both
suprema are attained at positive finite times.

## 6. What the argument does and does not establish

- The counterexample is in the standard round conformal class on S³.
  It is not a different topology or a merely piecewise smooth metric.
- The metric need not minimize the Yamabe functional. The original
  conjecture imposes no minimizing or constant-scalar-curvature hypothesis.
- The cylinder potential is +1/4, while the round sphere potential is +3/4.
  Dropping either potential would change the problem.
- The time after normalization is 4a, not 4; both the heat operator and
  the t^(3/2) prefactor have been rescaled.
- Large-L intuition suggested the example, but inequalities (2)–(7)
  prove it for the one finite value L=10000.
- The dimension-three small-time increase already recorded in the report
  would not by itself refute the maximum comparison. The strict bound
  above exceeds the round maximum over all positive times.
- No result on the n≥4 monotonicity question is claimed or counted.

## 7. Verification details

Run `python -I -B verify_bundle.py`; also run
`python -I -B -O verify_bundle.py`.
The bundle verifier checks the strict regular-file inventory and all
manifest hashes before executing the certificate with isolated imports
and bytecode writing disabled. The certificate uses integer and Fraction
arithmetic, never floating-point arithmetic for acceptance.

For the π bounds it uses the alternating arctangent series and the identity
π=16 arctan(1/5)−4 arctan(1/239). The identity follows from the tangent
addition formula: tan(4 arctan(1/5))=120/119 and subtracting arctan(1/239)
gives tangent 1, with the angle in (0,π/2). For e, the Taylor polynomial
through degree 10 plus its geometric upper tail is used.

The finite checker cannot independently prove smooth compactification,
conformal covariance, min–max, or Gaussian Poisson summation. These are
explicit analytic obligations in the proof, suitable for separate review.
