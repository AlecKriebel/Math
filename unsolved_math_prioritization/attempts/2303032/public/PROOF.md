# Function Theory 3.32: verification of the published integrability theorem

**Historical result, not a new solution.** Aikawa's 1994 Corollary 6(i)
answers the named problem. This note reconstructs its sufficient-range proof.
For barrier orders at most two it also proves optimality, including endpoint
failure. For barrier orders greater than two, the sharper uniform-optimality
claim is reported in the literature, but its counterexample construction has
**not** been independently reconstructed here. No endpoint assertion in that
regime is certified by this note.

## 1. Exact target and the two different parameters

Let D be a bounded Lipschitz domain in R^n, n >= 2, with uniform interior
circular cones of half-angle at least theta, where 0 < theta < pi/2. The
question is which positive exponents p are guaranteed to satisfy

    integral_D u(x)^p dx < infinity

for every positive superharmonic function u on D. Superharmonic excludes the
identically infinite function. There is no boundary boundedness hypothesis.
The guarantee is over domains with the stated geometry, not a determination
of the best exponent of each particular domain.

Define the spherical cap Sigma_theta = {omega in S^(n-1): omega_n > cos theta}.
Let lambda_1 be its first Dirichlet Laplace--Beltrami eigenvalue, and define

    a = a_n(theta) > 0 by a(a+n-2) = lambda_1.

Equivalently, r^a Phi(omega) is the positive cone-harmonic function which
vanishes on the lateral boundary, with Phi the positive first eigenfunction.
Here a >= 1 for theta <= pi/2. In dimension two, a = pi/(2 theta); in
dimension four, a = pi/theta - 1. Thus **a is not theta**. In the original
question the letter alpha denotes the geometric angle; in Aikawa's theorem
it denotes a. Hayman--Lingham's short update reuses alpha without explaining
this change. In particular, one must not substitute an angle in radians into
the exponent formula.

The published guarantee is

    0 < p < p_*(n,a),
    p_*(n,a) = min{ n/(n+a-2), 1/(a-1) }.

At a=1 the second entry is interpreted as infinity. Its equivalent split is

    p_* = n/(n+a-2)    for 1 <= a <= 2;
    p_* = 1/(a-1)      for a >= 2.

Indeed, with positive denominators, the first entry is at most the second
exactly when (n-1)(a-2) <= 0. Both entries equal one at a=2.

A k-Lipschitz chart gives theta=arctan(1/k). More generally, the proof below
uses the Lipschitz regularity for boundary estimates and the stated uniform
interior-cone condition for the Green lower bound. It does not require an
unjustified converse asserting that arbitrary cone placements give charts
of Lipschitz constant exactly cot(theta).

## 2. Standard potential-theoretic inputs and their scope

Write delta(x)=dist(x,partial D). Choose x0 in D with u(x0)<infinity and let
g(x)=G_D(x,x0), with -Delta g=c_n delta_x0 in the chosen normalization.
Such an x0 exists because a nontrivial superharmonic function is locally
integrable. All estimates involving g below are in a sufficiently small
boundary layer, separated from its pole.

We use these classical local facts, which are also the inputs of Aikawa's
1994 proof and his 2019 exposition:

1. A bounded Lipschitz domain is regular for the Dirichlet problem. Positive
   harmonic functions vanishing on a boundary patch satisfy the scale-local
   Carleson estimate and a boundary Holder estimate. See Aikawa 2019,
   Lemma 1.2 and the proof of Lemma 1.4. Interior Harnack and derivative
   estimates hold on balls compactly contained in D.
2. The interior-cone comparison gives g(x) >= c delta(x)^a near the boundary.
   For k-Lipschitz domains this is Aikawa 1994, pp. 3--4; the general uniform
   interior-cone formulation is Aikawa 1998, Lemma 15(ii).
3. If B is a ball whose fixed enlargement lies in D, 1 <= s < n/(n-2)
   (any finite s when n=2), and E is a positive-measure subset of B, then

       ( |B|^(-1) integral_B u^s )^(1/s)
          <= C |E|^(-1) integral_E u.                 (2.1)

   This is the local weak Harnack estimate in its positive-set form:
   Aikawa 1994, Lemmas 2--3, and Aikawa 2019, Lemma 1.5. For completeness,
   one can sweep u to the closed inner ball inside the enlarged ball,
   leaving the values on that inner ball unchanged. The resulting function
   is a Green potential of a positive measure there. For poles in that
   closed ball the enlarged-ball Green function is bounded below by
   c r^(2-n) on the inner ball, while its L^s norm there is at most
   C r^(2-n+n/s). These follow from its fundamental-solution singularity
   (a logarithm for n=2), which has precisely the stated local L^s range.
   Integrating the lower estimate over E and using Minkowski on the
   potential gives (2.1). The same argument follows by decomposing the
   local Riesz representation into nearby poles and a positive harmonic
   remainder, followed by Harnack for the latter.

These inputs are explicitly identified; this is not a formalization of all
classical potential theory from first principles. Neither pointwise gradient
nonvanishing nor an upper bound on the exterior barrier order is assumed.

The cone lower bound in input 2 can be understood directly. Compare g on an
interior cone of fixed radius with its homogeneous cone barrier, using a
positive uniform lower bound on an interior part of the cone cap. This gives
the r^a bound along its axis. Lipschitz-domain Harnack chains compare that
axis point at height comparable to delta(x) with x; the chain length is
uniform at that scale. Compact interior regions are harmless. This also
explains why the lower bound remains available when a domain has wider
interior cones than its particular Lipschitz charts exhibit.

## 3. Boundary layer volume

For 0 < t < t0,

    |{x in D : delta(x)<t}| <= C t.                    (3.1)

To see this, cover the compact boundary by finitely many Lipschitz graph
charts. In one chart, vertical height h over the graph satisfies
h <= sqrt(1+k^2) delta(x), after shrinking the chart to avoid its edge.
Hence delta<t confines x to a vertical strip of thickness C t. Fubini in
that chart and summation over the finite cover prove (3.1). Decomposing the
boundary layer into dyadic strips gives

    integral_D delta(x)^(-q) dx < infinity for q<1.    (3.2)

Nonpositive q are immediate from boundedness; for 0<q<1 the strip sum is
bounded by a constant times sum_j 2^(-j(1-q)). This is only a strict
inequality statement; q=1 is not supplied.

## 4. Coarea gives a weighted gradient estimate

For almost every t>0, the Green level domain D_t={g>t} has smooth boundary,
is relatively compact in D, and contains x0. The Green function of D_t with
pole x0 is g-t. The outward normal derivative is -|grad g|, so harmonic
measure at x0 is c_n^(-1)|grad g| d sigma on its boundary. The
super-mean-value inequality gives

    integral_{g=t} u |grad g| d sigma <= c_n u(x0).

Apply coarea, first to nonnegative bounded truncations and then by monotone
convergence. For every nonnegative integrable weight phi on (0,T),

    integral_{0<g<T} u phi(g) |grad g|^2 dx
        <= c_n u(x0) integral_0^T phi(t) dt.           (4.1)

Sard's theorem removes the exceptional critical levels. Nonnegativity makes
the use of coarea/Tonelli legitimate without any prior integrability claim.
The truncation at T avoids irrelevant behavior at the pole.

## 5. Why critical points of g cause no gap

It would be wrong to assume |grad g| >= c g/delta at every point. Instead
there is a fixed kappa<1 such that, for each boundary-layer x, the ball
B_x=B(x,kappa delta(x)) contains a measurable subset E_x with

    |E_x| >= c |B_x|,
    |grad g| >= c g(x)/delta(x) on E_x.               (5.1)

Here is a derivation of the positive-volume assertion. Put d=delta(x) and
choose a nearest boundary point z0. The Carleson and boundary Holder
estimates imply

    g(y) <= C (|y-z0|/d)^beta g(x)

for y sufficiently close to z0 in the boundary patch, with fixed beta>0.
The point z=z0+eta(x-z0) is inside B(x,d), hence in D. Taking a fixed eta>0
small enough ensures g(z)<=g(x)/2. The segment [z,x] stays in a ball
B(x,kappa_0 d), kappa_0<1. The fundamental theorem of calculus therefore
produces a point w on that segment with |grad g(w)|>=c g(x)/d.

Choose kappa_0<kappa<kappa'<1. On B(x,kappa' d), Harnack and the interior
second-derivative estimate bound |D^2 g| by C g(x)/d^2. Consequently the
lower gradient estimate at w persists on a ball B(w,rho d) contained in
B(x,kappa d), for a fixed sufficiently small rho>0. That ball is an
admissible E_x and has volume comparable to d^n. All constants depend only
on the fixed geometry and the chosen boundary layer, not on x.

Select a bounded-overlap covering of the boundary layer by such B_j, using
a standard Whitney/Besicovitch covering. Its fixed enlargements remain in D.
On each ball, g is comparable to g(x_j), and delta is comparable to d_j.
For phi(t)=t^(s-1), s>0, apply (2.1) with exponent one and E=E_j. Then

    integral_{B_j} u g^(s+1) delta^(-2)
      <= C integral_{E_j} u g^(s-1)|grad g|^2
      <= C integral_{B_j} u g^(s-1)|grad g|^2.

Summing and using (4.1), with a fixed sufficiently large T for the boundary
layer, gives

    integral_near_boundary u g^(s+1) delta^(-2) < infinity.

Since g>=c delta^a, set s=epsilon/a. For every epsilon>0,

    integral_D u delta^(a-2+epsilon) dx < infinity.  (5.2)

The compact complement contributes a finite amount by local integrability
of u and the boundedness above and below of delta there. This is the key
weighted theorem, and matches Aikawa 1994, Corollary 5(i).

## 6. The two exponent regimes

### 6.1. 1 <= a < 2

First suppose 1 <= p < n/(n+a-2). Choose

    epsilon = 2-a-n(1-1/p) > 0.

A Whitney-ball covering of D and (2.1) with E=B give

    ||u||_{L^p(D)}
      <= sum_j ||u||_{L^p(B_j)}
      <= C sum_j r_j^(-n(1-1/p)) integral_{B_j} u
      <= C integral_D u delta^(-n(1-1/p))
      = C integral_D u delta^(a-2+epsilon) < infinity.

The first inequality follows from (sum A_j)^(1/p)<=sum A_j^(1/p) for
nonnegative A_j. Bounded overlap gives the third. The local exponent
condition is satisfied because p<n/(n+a-2)<=n/(n-1)<n/(n-2) for n>2.
In n=2 every finite local exponent is permitted. The argument also includes
p=1. Every 0<p<1 then follows from u^p<=1+u and |D|<infinity.

### 6.2. a >= 2

Suppose 0<p<1/(a-1), so p<1. Choose epsilon>0 satisfying

    (a-1+epsilon)p < 1.

Set b=a-2+epsilon>0. Holder, with exponents 1/p and 1/(1-p), yields

    integral_D u^p
      <= (integral_D u delta^b)^p
         (integral_D delta^(-bp/(1-p)))^(1-p).

The first factor is finite by (5.2). The second is finite by (3.2), because
bp/(1-p)<1 is exactly (a-1+epsilon)p<1. This proves the published strict
range. In particular, at a=2 it proves every p<1, and it does not assert
p=1. No Minkowski inequality for p<1 has been used.

## 7. Exact cone controls and the boundary of the reconstruction

Let Phi be the positive first spherical eigenfunction from Section 1.
The polar-coordinate Laplacian gives

    Delta[r^b Phi] = r^(b-2)[b(b+n-2)-a(a+n-2)] Phi.

Both b=a and b=-(a+n-2) make the bracket vanish. Thus

    H(r,omega)=r^(-(a+n-2)) Phi(omega)

is positive harmonic inside the cone. Restrict it to a bounded domain which
agrees with the cone near the vertex and is capped away from the vertex. One explicit choice is the interior
of the convex hull of the origin and B(t e_n,t sin(theta)), t>0. The tangent
cone at the origin has exactly half-angle theta, and the conical side joins
the spherical cap tangentially. The boundary is C^1 away from the origin
and Lipschitz at the origin. Near the origin, fixed short translates of the
cone along its axis stay inside this domain; on the compact remainder of
the C^1 boundary, uniform interior cones of every fixed half-angle below
pi/2 exist. Thus a common positive radius works for the prescribed theta.
Polar integration near the tip gives

    integral H^p < infinity  iff  p(a+n-2)<n.          (7.1)

The angular integral is finite and strictly positive. At equality the radial
integral is integral_0^r0 dr/r and diverges. For a<=2 this is exactly the
published p_* and proves sharpness, including the endpoint. This example
is an obstruction to a uniform guarantee over the domain class; it does
not assert that every member of the class has this critical exponent.

At a=2 there is a completely explicit harmonic polynomial

    Q(x)=(n-1)x_n^2 - sum_{i<n} x_i^2.

It is positive on the cone with half-angle arccos(1/sqrt(n)). Its Kelvin
transform Q(x)/|x|^(n+2) is positive harmonic there and has degree -n, so
it is not in L^1 near the vertex. This certifies the sharp L^1 transition.
The smooth half-space model a=1 likewise gives the familiar threshold
n/(n-1), including failure at the endpoint. For C^1 domains the subcritical
range follows by choosing arbitrarily small Lipschitz constants and taking
a down to one; no endpoint inclusion follows by taking that limit.

**Critical distinction for a>2.** Formula (7.1) gives only the larger
obstruction n/(n+a-2), whereas the sufficient bound is 1/(a-1). Indeed,

    1/(a-1) < n/(n+a-2) for a>2.

For example n=2,a=3 gives 1/2<2/3. A single cone is therefore not a proof
of optimality for the smaller bound. Aikawa describes the published bound
as sharp in the 1994 paper, the 1998 introduction, the 2000 introduction,
and the 2019 exposition. The accessible 1994 and 2019 texts do not supply
an explicit counterexample construction for this narrower regime. The
1996 Aikawa--Essen monograph has a relevant section (II.9.5, pp.175--180),
but its full text was unavailable through the checked publisher route.

Accordingly, this dossier records the historical resolution at theorem
level and the sufficient range with a reconstructed proof. It does not
claim a complete independent reconstruction of sharpness for a>2, nor
that equality at p=1/(a-1) fails in every individual domain. Domain-by-domain
critical exponents can be better than a bound derived from a nonoptimal
cone certificate. The unresolved point **in this verification** is the
counterexample/endpoint analysis for a>2, not evidence of a newly open
problem or a new result.

## 8. References

- H. Aikawa, *Integrability of superharmonic functions and subharmonic
  functions*, Proc. Amer. Math. Soc. 120 (1994), 109--117, DOI
  [10.2307/2160174](https://doi.org/10.2307/2160174).
  [Author manuscript](https://www.isc.chubu.ac.jp/aikawa/research/AikawaPapers/int.pdf),
  especially pp.3--4, 5--9 and Corollary 6(i).
- H. Aikawa, *Norm estimate of Green operator, perturbation of Green function
  and integrability of superharmonic functions*, Math. Ann. 312 (1998),
  289--318, DOI [10.1007/s002080050223](https://doi.org/10.1007/s002080050223).
  [Author manuscript](https://www.isc.chubu.ac.jp/aikawa/research/AikawaPapers/neg.pdf),
  introduction and Theorem 7/Lemma 15.
- H. Aikawa, *Integrability of superharmonic functions in a John domain*,
  Proc. Amer. Math. Soc. 128 (2000), 195--201, DOI
  [10.1090/S0002-9939-99-04991-6](https://doi.org/10.1090/S0002-9939-99-04991-6).
  [Author manuscript](https://www.isc.chubu.ac.jp/aikawa/research/AikawaPapers/john.pdf),
  introduction, for the author's later historical assessment.
- H. Aikawa, *Potential theoretic notions related to integrability of
  superharmonic functions and supertemperatures*, Anal. Math. Phys. 9 (2019),
  711--728, DOI [10.1007/s13324-019-00323-9](https://doi.org/10.1007/s13324-019-00323-9).
  [Author manuscript](https://www.isc.chubu.ac.jp/aikawa/research/AikawaPapers/iccapta.pdf),
  pp.2--6, Lemmas 1.2--1.6, Theorem 1.7 and Remark 1.8.
- W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory
  (New Edition)*, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2),
  printed p.70, Problem/Update 3.32 and reference [13].
