# Root mathematical reconstruction before candidate computation

The primary baseline is sealed. The root has now read the complete candidate
TURN_1.md, PRIOR_RESOLUTION.md and SOURCE_GATE.md (the three mathematical
documents), and the additional primary capacity identity in Jauregui2020,
PDF22 equation(41), including the exact point where nonnegative ADM mass first
enters the later volume estimate. No candidate code, check output, status,
final summary, historical review or full sibling artifact has been read.
The baseline discloses earlier brief sibling findings; this reconstruction
does not claim independence from those briefs. It checks the universal proof
directly, before any numerical or symbolic check output.

## 1. Hypothesis-preserving credited prior resolution

Let M be a smooth connected complete one-ended AF three-manifold in Jauregui's
two-derivative class, decay tau>1/2, scalar curvature integrable, compact boundary
possibly empty. Add scalar curvature nonnegative everywhere and, if present,
minimal boundary. These are the physical conjecture's hypotheses in the full
2020 paper; the OWR sentence is abbreviated and does not repeat them.

Jauregui Theorem5 gives ADM<=mCV, since nonnegative scalar curvature everywhere
implies its outside-a-compact-set assumption. BFM2023 Theorem5.6 at p=2 gives
m2<=miso, with no H2 hypothesis. Its global conventions match completeness,
smooth connected one-endness. At p=2 the capacity normalization is exactly
(4*pi)^(-1) times Dirichlet energy (substitute v=1-phi). Its quasilocal mass is
(V-(4*pi/3)c^3)/(4*pi*c^2). Jauregui Lemma10 identifies its global exhaustion
supremum with mCV; this is not a setwise identity outside efficient sequences.
The existing Huisken-mass theorem identifies miso=ADM in the original smooth
AF class with nonnegative scalar curvature and empty/minimal boundary, as
stated explicitly in Jauregui2020 Theorem2 and Jauregui–Lee Theorem3. The
stronger C1 statement is BFM Penrose paper Theorem1.4. Hence

    ADM <= mCV = m2 <= miso = ADM.

Theorem1.3 of BFM2023 has an extra H2(M,partial M;Z)=0 hypothesis and cannot
alone establish the above topology-free claim. The use of its separate upper
comparison rather than its full equality theorem is essential and correct.
The older BFM2023 comparison proof contains a sign-sensitive multiplication
of an upper integral bound by m+epsilon. On the physical class, miso=ADM>=0
by the positive mass theorem, so choose m>miso and that factor is positive.
Thus the cited route does not rely on the problematic negative-sign step.
Benatti2025 explicitly repairs the broader comparison by splitting signs and
using inclusion of a fixed core; it is corroboration rather than a new proof
claim here. Its full all-p equivalence has extra minimal-surface and
isoperimetric assumptions and is not used to erase them.

Smooth-domain versus arbitrary-compact competitors need checking: capacity is
outer regular for compact sets in this smooth uniformly elliptic setting. For
each compact K choose a bounded smooth enclosing domain L with
cap(L)<=cap(K)+epsilon. Volume does not decrease, so its linear deficit is at
least that of K minus epsilon. For an exhaustion in the usual sense of
eventual containment of each compact subset, choose successively late members
containing the preceding smooth enclosure and take epsilon tending to zero.
This produces a nested smooth exhaustion without reducing the supremum.
Conversely smooth closed domains are admissible compacts. Capacities diverge
because each exhaustion eventually contains every fixed coordinate ball,
whose AF capacities grow without bound. This justifies aligning the two
definitions, rather than replacing the supremum by coordinate balls.

Finite ADM mass is enough for the current original class (integrable scalar
curvature with sufficient decay). Where the sharper C1 prior theorem admits
infinite mass, the extended-value chain remains valid, but no extension is
needed for this accepted claim. Empty boundary is permitted throughout.
The assertion is credited to existing literature, not a novel result.

## 2. Smooth complete sign-free counterexample

Choose any smooth chi:[0,infinity)->[0,1] with chi=0 for r<=2 and chi=1 for
r>=3. Put u=1-chi(r)/r, interpreted as 1 near the origin, and g=u^4 delta on
R3. Smoothness at the origin follows from constancy near it, rather than from
a false claim that r is smooth there. For r>=2, u>=1-1/2=1/2; elsewhere u=1,
and everywhere u<=1. Thus (1/16)delta<=g<=delta, giving positivity and metric
completeness. It is a smooth boundaryless connected one-ended manifold.
On r>=3, u=1-1/r. Every derivative has the required AF decay, and
R_g=-8*u^(-5)*Delta_delta u is smooth and supported in the compact transition
annulus. Scalar curvature is integrable; its global nonnegativity is neither
assumed nor possible for this complete negative-mass example.

For a conformally flat metric, the ADM integrand is
(partial_j g_ij-partial_i g_jj)nu_i=-2*partial_r(u^4).
After area integration and division by 16*pi the mass is
-2*r^2*u^3*u_r. Since u_r=1/r^2 in the end, its limit is -2. This verifies
the sign and coefficient directly. The fill-in is smooth; no singular
negative Schwarzschild origin remains.

For R>=6, set a_R=(R/2)e1 and K_R=closed B(a_R,R). These have smooth compact
boundaries, contain B(0,R/2), and lie in B(0,3R/2). For S>=R,
|a_S-a_R|+R=(S-R)/2+R<=S; hence nestedness holds. The union is all of R3.
The core B(0,3) lies inside each set, and its exterior lies in the harmonic
region r>=R/2>=3. These are genuine exhausting competitors. The limit below
therefore gives a lower bound on the global supremum, unlike nonexhausting
small far-out balls.

## 3. Exact capacity, minimizer and two independent flux checks

In dimension three, dV_g=u^6 dx and the energy density is
|grad phi|_g^2*dV_g=u^2*|grad phi|_delta^2 dx. Let
f=1-R/rho, rho=|x-a_R|, on rho>=R. Both f and u are Euclidean harmonic
outside K_R. The identity

    div(u^2 grad(f/u)) = u*Delta f - f*Delta u = 0

shows that psi=f/u is g-harmonic. It vanishes on the inner boundary and
approaches 1 at infinity. It has finite Dirichlet energy since its gradient
is O(r^-2), and is bounded between zero and one by the maximum principle.
To make the minimizing step explicit, for a compactly supported perturbation
h vanishing on the inner boundary, integration by parts gives
integral u^2 grad(psi).grad(h)=0. Thus E(psi+h)=E(psi)+E(h)>=E(psi).
Approximation and exhaustion extend this to the admissible finite-energy
class. Alternatively the difference of two bounded solutions with zero
boundary and zero infinity limit vanishes by the maximum principle on large
annuli. Hence this is the capacitary minimizer, not just a harmonic trial.

For fixed R as r tends to infinity, rho=r+O(1), so
f=1-R/r+O(r^-2), u=1-1/r, and
psi=1-(R-1)/r+O(r^-2), with differentiated decay. The g-normal flux density
nu_g(psi)dA_g=u^2*partial_r(psi)r^2 dOmega has limit 4*pi*(R-1).
Integration by parts for the energy gives this same flux (inner boundary
term vanishes since psi=0). Normalized capacity is exactly R-1.

An independent inner-boundary flux calculation avoids relying on the infinity
expansion: at rho=R, f=0 and the outward-from-K normal derivative is 1/R,
so u^2*partial_n psi=u/R. Newton's spherical mean gives
average_{rho=R}(1/r)=1/R because |a_R|<R. Thus
(4*pi)^(-1)integral_{partial K_R}u/R dA_delta=R-1. This is positive for
all allowed R. The credited Jauregui equation(41), cap_g(K)=cap_delta(K)+m/2,
proves precisely the same enclosing-set identity before imposing m>=0 on
the subsequent volume estimate; applying it with m=-2 is legitimate.

The candidate's separate trial f also checks the conformal energy. On each
rho-shell with rho>=R>|a_R| the spherical mean of 1/r is 1/rho. Its first
two energy terms give R and -1. Because r>=rho-|a_R|>=rho/2,
the remaining positive term is at most
4*R^2*integral_R^infinity rho^-4 d rho=4/(3R). Therefore its trial energy
lies between R-1 and R-1+4/(3R), consistent with the exact minimizing
capacity. No Euclidean energy was substituted for the metric energy.

## 4. Volume with controlled compact-fill remainder

On r>=3, u^6=(1-1/r)^6=1-6/r+O(r^-2) with a uniform constant independent
of R. On the fixed core the difference between the true u^6 and 1-6/r has
finite integral since 1/r is locally integrable in three dimensions; it
contributes O(1). Moreover integral_{K_R}r^-2 dx <=
integral_{B(0,3R/2)}r^-2 dx=6*pi*R. Hence

    V_g(K_R)=(4*pi/3)R^3-6*I_R+O(R),
    I_R=integral_{B(a_R,R)}1/r dx.

For d=|a_R|<R, the spherical mean on a rho-shell centered at a_R is
1/max(d,rho). Therefore

    I_R=4*pi*(integral_0^d rho^2/d d rho+integral_d^R rho d rho)
       =2*pi*(R^2-d^2/3).

At d=R/2, this is (11*pi/6)R^2 and
V_g=(4*pi/3)R^3-11*pi*R^2+O(R). Thus
3V_g/(4*pi)=R^3-(33/4)R^2+O(R). Taylor's expansion
(1+z)^(1/3)=1+z/3+O(z^2), with z=-(33/4)/R+O(R^-2), gives

    (3V_g/(4*pi))^(1/3)=R-11/4+O(R^-1).

The omitted compact fill and all higher conformal powers vanish in the
constant-order deficit. Subtracting exact capacity R-1 gives limit -7/4.
Consequently mCV>=-7/4>-2=ADM, with a gap at least 1/4. The supremum can
be larger; this does not evaluate the exact mCV or imply its nonnegativity.
The physical-class equality is not contradicted because its scalar curvature
condition fails in the compact interior.

## 5. Boundary, scale and claim checks

For a general negative m, choose a sufficiently large fixed smooth fill-in
with u=1+m/(2r)>0 in the end. The same enclosing shifted balls with
a_R=lambda*R*e1, 0<lambda<1, have cap=R+m/2,
volume radius R+(3m/2)(1-lambda^2/3)+o(1), and deficit
m*(1-lambda^2/2)>m. The original explicit construction already suffices.
lambda=0 recovers deficit m, so shiftedness is substantive. At m=0 the
Euclidean deficit is zero. For m>0 the shifted-ball deficit is below m,
consistent with the positive-mass harmonic-flat upper theorem. Letting
lambda approach one while R remains fixed is not an admissible use of a
uniform core-containment estimate; all formulas here fix lambda<1 before
the limit. Homothetic scaling g->s^2 g scales lengths, capacities and both
masses by s, and volume by s^3; no units mismatch is present.

The construction uses a classical Newton potential and a credited capacity
identity. Its historical novelty is unverified. The accepted strongest
mathematical conclusion can be the credited physical-class resolution plus
this scoped sign-free counterexample, with no new physical theorem, no exact
global mass, and no fresh-priority claim. This is a partial archive, not a
preprint proposal. No mandatory mathematical repair found in the three
complete candidate mathematical documents. Program/output/status/history,
source and manifest reproduction, fresh whole reviews, literal live scope,
queue refresh and actual merge remain pending.

Mathematical-reconstruction workflow estimate: 45%.
