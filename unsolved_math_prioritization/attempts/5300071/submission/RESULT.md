# Uniform access for relaxed Newton maps: partial results and exact gap

Problem ID 5300071 (AMR-052-0071), source-ranked 650.
Status: **unsolved**. Five approach families were investigated. No complete proof,
counterexample to the intended formulation, or verified prior resolution was obtained.
The elementary results below are supporting lemmas, with no novelty claim.

## 1. Target and quantifiers

Let f be a nonconstant complex polynomial of degree d, all of whose zeros have
modulus at most 1. Let alpha be a zero of multiplicity m. Cancel removable factors
in N_h(z)=z-h f(z)/f'(z), and let U_h(alpha) be the connected component containing
alpha of its basin of convergence to alpha. Parameters are real, 0<h<=m; h is
fixed during each iteration. The target is an absolute c>0 such that, for every
such f, alpha and every R>=3, the set

    C_R intersect (intersection over 0<h<=m of U_h(alpha)), C_R={z: |z|=R},

contains arcs with total Euclidean length at least 2*pi*R/(c*d).
Thus the normalized angular length must be at least 2*pi/(c*d). The arcs may
depend on f, alpha and R, but must work simultaneously for all h. A parameter
mesh, a positive planar area, access along a curve, or a bound for each h
separately is not the claim. Nor does convergence identify the immediate basin
without a connection to alpha through points in the basin.

The primary source is Sutherland's Conjecture 2, printed p.43 of Bielefeld and
Lyubich, *Problems in Holomorphic Dynamics*, IMS 92/7:
https://www.math.stonybrook.edu/preprints/ims92-7.pdf . Its phrase about circles
omits their center. We use circles centered at the normalization origin, as in
the circle estimates motivating it. The unrestricted-center reading is false:
for f(z)=z^2-1/4, the basin of -1/2 at h=1 is the left half-plane, so the circle
of radius 3 centered at 10 misses it. This does not resolve the intended problem.

The multiplicity m is that of the selected root, not necessarily the minimum
multiplicity of f. Other roots need not attract throughout (0,m]. In particular,
results assuming every finite fixed point attracts cannot automatically be used
on the full requested parameter interval.

## 2. Common local trapping disk (proved)

If f has only the root alpha, then f=c(z-alpha)^d and

    N_h(z)-alpha=(1-h/d)(z-alpha).

Every finite point converges for every 0<h<=d, including the constant-map
endpoint h=d. The target holds in this subcase with c=1.

Otherwise write f(z)=(z-alpha)^m g(z), put

    delta=min{|beta-alpha|: beta is a different zero},
    r=m*delta/(4*d-3*m).

Then the open disk D(alpha,r) lies in every U_h(alpha), 0<h<=m.
Indeed, for |z-alpha|<=r let

    q(z)=(z-alpha)g'(z)/g(z), v=q(z)/m, t=h/m.

The logarithmic derivative, with roots counted with multiplicity, gives

    |q(z)| <= (d-m)*r/(delta-r) = m/4.

There are no zeros of g in the disk, and |m+q|>=3m/4, so the reduced map is
holomorphic there. Direct algebra gives

    N_h(z)-alpha=(z-alpha)*(1-t/(1+v)).

Since |v|<=1/4 and 0<t<=1,

    |1+v|^2-|1+v-t|^2=2t*Re(1+v)-t^2 >= t/2,
    |1+v|^2 <= 25/16,
    |N_h(z)-alpha|^2 <= (1-8t/25)*|z-alpha|^2.

For each fixed positive h this is a strict radial contraction. Iteration stays
in the disk and converges geometrically to alpha. The disk is connected and
contains alpha, proving immediate-basin membership. No contraction rate uniform
as h decreases to zero is asserted.

**Gap:** r depends on root separation and is local. It supplies neither a path
to C_R nor a degree-uniform length on C_R. For example delta may tend to zero
at fixed degree. Local stability alone does not prove uniform exterior access.

## 3. Two distinct roots of equal multiplicity (proved)

For f(z)=c(z-a)^k(z-b)^k with a!=b, d=2k, use the affine coordinate

    u=(2z-a-b)/(a-b), t=h/k, 0<t<=1.

The map becomes F_t(u)=(1-t/2)u+t/(2u), with roots 1 and -1. In the right
half-plane both u and 1/u have positive real part, so F_t preserves it. Under
w=(u-1)/(u+1), this map becomes

    G_t(w)=w*(w+q)/(1+q*w), q=1-t in [0,1).

For |w|<1,

    |1+q*w|^2-|w+q|^2=(1-q^2)*(1-|w|^2)>0.

Hence |G_t(w)|<|w| for w!=0. On the closed disk of radius |w_0|<1 the
second factor has maximum modulus M<1, so |w_n|<=M^n|w_0| and w_n tends
to zero. Thus every right-half-plane point converges to 1. The same argument
with u replaced by -u treats the left half-plane. The imaginary axis is
invariant on the sphere, including poles and infinity; its orbits cannot
converge to either real root. Consequently these two half-planes are exactly
the two full basins, and each is an immediate basin, for every allowed h.

In the original coordinate the basins are the open Voronoi half-planes for a
and b. Their separating line passes through (a+b)/2 and therefore has distance
at most 1 from the origin. Each half-plane cuts a circle C_R, R>=3, in an arc
of length at least

    2R*arccos(1/R) >= 2R*arccos(1/3) > pi*R/2.

Since d>=2, this proves the target on this entire subfamily with c=2. The
half-planes are independent of h, so this is genuinely a simultaneous-parameter
result, not an interchange of the intersection and length operations.

**Gap:** with unequal multiplicities, the same normal form has a different
denominator and these invariant half-planes no longer follow. General
polynomials have still more complicated accesses.

## 4. Fixed-parameter channel route

For a fixed h, suppose the selected immediate basin admits a proper
finite-Blaschke-product model B fixing 0 and with multiplier lambda=1-h/m.
If all its other fixed points are repelling points xi_j on the unit circle
with multipliers mu_j>1, reflection gives the multiplier lambda at infinity
as well. The rational fixed-point index formula then gives

    sum_j 1/(mu_j-1) = 2m/h-1 >= 1.

The associated channel moduli are pi/log(mu_j). These formulas explain why
one expects substantial channels for each h separately. This is a conditional
calculation: the existence and global geometry of the model must be justified
for the particular h and basin. The classical h=1 constructions are inspected
in Sutherland's thesis and Hubbard--Schleicher--Sutherland (2001).

Even perfect fixed-h arc bounds cannot be intersected without a new theorem.
For example every open semicircle E_theta on the unit circle has length pi,
but their intersection over a full rotation is empty. This is a logical
counterexample to the inference, not a Newton-map counterexample. A family of
channel charts, a common corridor, or an appropriate nesting result is missing.
Also, when h exceeds twice another root's multiplicity, that other root is
repelling; the all-finite-fixed-points-attract hypothesis is then unavailable.

An actual elementary warning about one direction of nesting is available.
For f(z)=z(z^2-1) and alpha=0,

    N_1(1/2)=-1,
    N_(1/2)(x)=x*(5x^2-1)/(6x^2-2).

On the interval [-1/2,1/2] the latter ratio has modulus at most 1/2, because
for 0<=s<=1/4, |5s-1|<=1-3s. Every point of this connected interval
therefore converges to zero under N_(1/2), so 1/2 belongs to U_(1/2)(0).
It does not belong to the full basin of zero for h=1. Thus
U_(1/2)(0) is not a subset of U_1(0). This example does not establish or refute
the opposite inclusion. Scaling all coordinates by 1/2 puts all roots strictly
inside the unit disk without changing this conclusion.

## 5. Flow/Euler route and parameter compactness

For the differential equation z'=-f(z)/f'(z), away from nonremovable poles,

    d/dt f(z(t)) = -f(z(t)), hence f(z(t))=exp(-t)f(z(0)).

Fix a compact collection of trajectories that avoids the poles up to a finite
time T and enters the strict interior of the trapping disk in Section 2.
On a compact neighborhood of these trajectories the vector field has finite
Lipschitz and derivative bounds. The usual finite-time Euler estimate then
makes the h-step discrete trajectories enter the trapping disk for all
sufficiently small h>0. If a connected compact path to alpha is covered this
way, its points lie in the immediate basin for those small h. The constants
and permitted h depend on the chosen compact neighborhood, pole separation,
entry margin and T. This statement does not provide a degree-only estimate.

For any compact parameter interval [epsilon,m], convergence certified by a
finite orbit segment followed by a strict trapping region persists locally in
(z,h). A compactness argument can join certificates only after a common set
of starting points has been found for every h. It cannot produce that common
set from nonempty but different basins. The omitted endpoint h=0 is the
identity map and cannot be inserted as an attracting-map endpoint.

**Gap:** provide a common exterior corridor and its quantitative width across
all h, especially near moving separatrices and arbitrarily small root
separations. Neither Euler convergence nor compactness supplies it.

## 6. Reproducible adversarial checks

`verify.py` checks the exact algebraic inequalities and the interval example
with rational arithmetic, the two-root conjugacy with exact rational complex
arithmetic, and computes a finite circle/parameter survey for z(z^2-1).
The numerical part labels convergence to roots, not immediate components.
It uses only five parameters and three radii, finite starting-point meshes,
finite iteration limits and floating arithmetic. It establishes no arc
containment, no lower length bound and no continuum-h certificate. Unresolved
orbits remain explicitly unresolved. Its role is falsification/control, not
proof of the conjecture.

## 7. Conclusion

The intended general conjecture remains **unsolved in this attempt**. The
precise missing result is a degree-uniform arc-length lower bound in the
simultaneous intersection of immediate basins, with h spanning (0,m]. The
proved local disk and equal-multiplicity two-root case cannot replace that
claim. The literature inspection found related fixed-parameter geometry,
small-step context, and recent convergence results, but no verified complete
resolution. This is a bounded literature check, not a claim that none exists.
