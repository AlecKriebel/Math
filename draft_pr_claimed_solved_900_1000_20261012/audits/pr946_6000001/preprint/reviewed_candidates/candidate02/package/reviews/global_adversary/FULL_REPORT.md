# PR946 / ID6000001 — independent global obstruction adversary

Audit date: 2026-10-15 UTC. Frozen candidate head:
`7d3adb0e500b0414a49a449e7981d34ade329427`.

## Verdict and exact scope

**PASS for this global/topological adversarial family; no required mathematical
repair identified.** This is a verification verdict on the frozen proof's exact
smooth, positive definite, boundaryless scope. It is not a historical priority,
publication, source-definition, or whole-package acceptance verdict.

The claim tested is: every smooth Hausdorff second-countable n-manifold without
boundary, n>=1, carrying a positive metric and a specified ordered pair of smooth
mutually dual torsion-free connections admits a proper embedding into an open
subset of finite-dimensional Euclidean space equipped with a positive ordinary
Hessian metric, inducing that ordered pair from its two flat torsion-free dual
connections. The target may depend on all source data and need not be convex,
complete, or have globally injective dual coordinates. The candidate bound is
N=binomial(2n+4,3). The zero-dimensional case is separate.

The success criterion for this family was either a concrete counterexample or
unsupported universal step, or a reasoned rejection of the proposed global
obstruction mechanisms, with explicit nontrivial controls. The original proof
was read in full. No other independent family's or historical audit's verdict
was read or used.

## Custody and reproduction

`AUTHENTICATION.json` independently compares all 33 frozen original files against
actual Git objects at the stated head, the frozen disk bytes, and the snapshot
hashes. All match. The actual-Git proof SHA-256 is
`a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2`.
The actual-Git queue row is exactly `claimed_solved`, original observed `4/5`.
Only the proof and author public finite-check program contents were examined
mathematically; authentication of historical audit bytes did not import their
conclusions. No original author or historical audit program was run.

Run this family's controls with Python 3, standard library only:

```text
python3 global_controls.py
```

The exact-rational output is `GLOBAL_CONTROLS.json`. Finite checks certify the
displayed finite algebra, while the following arguments supply the global
meaning. This script is independent of the original symbolic examples. An early
scratch calculation attempted to import SymPy from the default Python, found it
unavailable, and was replaced by the self-contained rational polynomial program;
the failed import supplied no mathematical evidence.

## 1. Compact circle with nonzero periods and connection holonomy

Write z1=x+iy and z2=u+iv in R^4=C^2. Consider the embedded circle

    f(theta)=(exp(i theta), exp(2i theta)), theta modulo 2pi,

and the globally defined polynomial

    Psi = (|z1|^2-1)/2 - Im(z2 conjugate(z1)^2)
          +100[(|z1|^2-1)^2 + |z2-z1^2|^2].

Its value on the circle is zero. If E1,T1 are the radial and positive unit
angular vectors in the first complex coordinate and E2,T2 those in the second,
its gradient on the circle is

    phi = E1 + 2 T1 - T2.

Thus phi(f')=0 although phi is nowhere zero. In particular, the compact maximum
and minimum of the restriction Psi|S do not give ambient critical points.
At theta=0 its Hessian is

    [1601,   2, -400,  -2]
    [   2, 801,    2,-400]
    [-400,   2,  200,   0]
    [  -2,-400,    0, 200].

Its leading principal minors are respectively
1601, 1282397, 128309796, 31238416, all strictly positive. This is an exact
Sylvester-criterion check, not a numerical eigenvalue observation.

For every alpha, the orthogonal action

    rho_alpha(z1,z2)=(exp(i alpha) z1, exp(2i alpha) z2)

preserves Psi: the first radial term and the imaginary cubic term are invariant,
and z2-z1^2 acquires the common unit factor exp(2i alpha). This action is
transitive on S, so all Hessians along S are orthogonally conjugate to the
displayed positive matrix. Consequently the Hessian-positive locus U is one
open neighborhood containing the entire circle. Restrict Psi to U. The circle
embedding is proper because its domain is compact.

Along S,

    f' = T1+2T2,       f''=-E1-4E2,
    phi'=-2E1+T1+2E2.

Differentiating the ambient gradient gives H f'=phi'. Therefore

    g(f',f')=f' dot phi'=1,
    g(nabla_{d/dtheta}d/dtheta,d/dtheta)=f'' dot phi'=-6.

The D-induced connection coefficient is -6. Its metric dual has coefficient
+6. In the global invariant frame d/dtheta the two parallel transport factors
around the positive circle are exp(12pi) and exp(-12pi). Thus even nontrivial
reciprocal linear holonomy of the induced ordered pair is compatible with a
single global Hessian potential and flat ambient connections.

The intrinsic invariant one-form dtheta has nonzero period 2pi. The candidate
does not try to integrate that form: its compatibility form phi df is identically
zero, as it is in this explicit circle model. Fundamental-group or de Rham-period
arguments applied to an unrelated intrinsic form do not obstruct the construction.

For a sharp convexity control take p=f(0)=(1,0,1,0) and
q=f(pi/2)=(0,1,-1,0). Both potential values are zero, but

    gradient(Psi)(p) dot (q-p) = (1,2,0,-1) dot (-1,1,-2,0) = 1.

A differentiable convex potential on a convex set containing this chord would
require Psi(q)>=Psi(p)+1. In fact, at the chord midpoint the directional Hessian
in direction q-p is exactly -798. Thus the positive locus excludes the midpoint.
This fixed model really requires a nonconvex neighborhood; positivity there is
nevertheless sufficient for dual flatness. This is not a claim that every
realization of this abstract circle must use a nonconvex target.

## 2. Proper noncompact model with an incomplete, degenerating metric

In R^2 with coordinates (x,y), put

    q=x^2-y,    F(q)=q/2+q^2,    Psi(x,y)=exp(-x) F(q),
    f(x)=(x,x^2).

The parabola is a proper embedding of all of R, and Psi is zero on its image.
The Hessian's y,y entry is 2 exp(-x). Direct differentiation gives

    det(Hess Psi) / exp(-2x)
      = 2F+4F'-(F')^2 = -2q^2+7q+7/4.

Hence the single open parabolic band

    U = { (7-sqrt(63))/4 < x^2-y < (7+sqrt(63))/4 }

has positive Hessian everywhere and contains the entire image. No uniform lower
metric bound is asserted. The Hessian along f is

    exp(-x) [1-2x+8x^2, 1/2-4x; 1/2-4x, 2],

with determinant (7/4)exp(-2x). On the curve the ambient gradient and its derivative
are

    phi=exp(-x)(x,-1/2),     phi'=exp(-x)(1-x,1/2).

It follows that the induced metric is exp(-x)dx^2, and f'' dot phi'=exp(-x).
The specified ordered connection coefficients are therefore +1 and -2. Its
cubic C=nabla g is -3 exp(-x)dx^3, with normalized value
-3exp(x/2) in the positive unit tangent frame. This is unbounded at +infinity.
The length of the positive end from zero is exactly

    integral_0^infinity exp(-x/2) dx = 2.

This proper Hessian realization is global despite metric incompleteness,
degenerating metric scale, and unbounded normalized cubic geometry. The band is
connected, and the image runs to Euclidean infinity. This explicitly rejects
the proposed implication that properness by itself forces metric completeness
or compactness.

There is a genuine obstruction if one adds **ambient Riemannian completeness**:
a proper isometric embedding into a complete Riemannian manifold induces a
complete metric. An intrinsic Cauchy sequence is ambient Cauchy; ambient
completeness supplies a limit; properness places it on the image, and local
metric comparison gives intrinsic convergence. Therefore this particular
incomplete source cannot have a proper isometric realization in a complete
ambient Riemannian manifold. The candidate expressly allows incomplete targets.

Both explicit examples can be padded to the theorem's n=1 bound N=20 by adjoining
zero embedding coordinates and adding positive quadratic terms in those
coordinates to the potential.

## 3. Countably many components and absence of uniform control

A direct disconnected control has M the disjoint union of countably many copies
of R. On component k>=1 use g_k=exp(-kx)dx^2 and ordered connection coefficients
0,-k. In R^2 use the disjoint open strips

    U_k=R x (k-1/4,k+1/4),
    Psi|U_k=exp(-kx)/k^2+(y-k)^2/2,
    f(k,x)=(x,k).

The Hessian is diag(exp(-kx),1), the ordered pair is induced directly, and f is
proper: an ambient compact set meets only finitely many integer-height lines
and bounds x on each. No common bound on normalized geometry, connection
coefficients, or metric scale is required. A smooth function on the disconnected
open union is exactly a smooth function on each component. This is within the
charter's allowance of an open U, with no connected-target requirement.

Variable tubular radius is also substantive. The proper smooth graph

    e(x)=(x,exp(-x) sin(exp(2x)))

has unbounded curvature. At t_k=pi/2+2pi k and x_k=(log t_k)/2 its slope is
-t_k^(-1/2), its second derivative is t_k^(-1/2)-4t_k^(3/2), and its curvature
magnitude tends to infinity. A fixed positive normal radius fails because the
normal map becomes singular at reciprocal curvature. This does not attack the
candidate: it explicitly uses a variable-radius tube and the open positive
Hessian locus. The candidate's argument never converts pointwise estimates to
uniform estimates.

## 4. Independent review of the universal steps

The finite examples alone would not justify a universal verdict. The following
global proof steps were separately checked against the frozen argument.

1. **Embedding and closedness.** Given the standard proper smooth Whitney
   embedding in R^(2n+1), retaining its linear coordinate features makes f an
   embedding and proper. A proper embedding has closed image. Countably many
   components do not change these arguments. The monomial count includes the
   constant and is exactly binomial(2n+4,3)>n.
2. **Finite jets at all points.** At each point, n restricted linear functions
   of the Whitney coordinates form local coordinates. Every scalar 3-jet is
   represented by a polynomial of degree <=3 in those functions. The same
   finite ambient polynomial space works at every point; no finite chart cover
   is being assumed. The argument is not an equivalent realization hypothesis.
3. **Global right inverse.** Surjectivity of a smooth vector-bundle map gives
   invertibility of E E^dagger pointwise after choosing smooth bundle metrics.
   Matrix inversion is smooth on its open domain of invertible matrices.
   Unbounded inverses at infinity do not prevent a smooth global section.
4. **Jet compatibility.** The normal-coordinate definition prescribes a smooth
   section of the scalar jet bundle using only germs of the exponential map.
   It does not need metric completeness. Its Hessian is g and its third
   ordinary derivatives transform as a scalar jet with zero first derivative;
   the three Levi-Civita correction terms give the displayed Q. The section
   need not be holonomic. In particular, a(p) is held fixed while evaluating
   the jet in the x variable. The identically zero function a(p)f(p) includes
   derivatives of a when differentiated along p. Confusing those two
   differentiations would produce a false integrability contradiction.
5. **Period compatibility and smooth potential.** Differentiating a df=0 and
   a d^2f=g yields df dphi=g and d^2f dphi=Gamma in the stated order. Conormality
   phi df=0 gives an actual globally exact compatibility form, with potential
   value zero. On a normal tube, Psi0(z)=phi_r(z-r) is a single smooth scalar
   function, even for a nontrivial normal bundle. It has the correct value and
   gradient on S. Its tangent Hessian is g and its normal-normal Hessian is zero.
6. **Positive completion without a frame.** The Euclidean tangent/normal split
   is global as a bundle split, not as a choice of frame. A is a smooth positive
   endomorphism of TS; tr(A^-1), the Hilbert-Schmidt norm of B, lambda and |nu|^2
   are invariant smooth scalars. The normal correction has zero 1-jet on S and
   normal Hessian 2lambda I. Since
   B^t A^-1 B <= tr(A^-1)||B||_HS^2 I, the stated Schur complement is strictly
   positive pointwise. No normal trivialization, uniform spectral estimate,
   uniform tube, or finite cover enters.
7. **One open ambient manifold.** Positivity is open in the space of symmetric
   matrices, so the Hessian-positive locus is one open set containing every
   point of S. It is permissible for its geometry to narrow or degenerate at
   infinity. A compact subset of U is compact in Euclidean space, so the
   original properness survives restriction of the target to U.
8. **Both ordered connections.** From H df=dphi, projection of D gives exactly
   f_ij dot phi_k=Gamma_ijk, rather than its dual. Projection of the ambient
   duality identity forces the second induced connection to be the uniquely
   specified g-dual. Positive Hessian symmetry gives torsion-freeness of D*;
   the local gradient coordinates give flatness. Neither computation uses
   convexity or global injectivity of those coordinates. Flatness is a local
   tensorial condition. Projection of each torsion-free ambient connection
   proves necessity of the corresponding source torsion condition.

These checks leave no unsupported equivalent-hard realization step. The genuine
external inputs are standard proper Whitney embedding, smooth bundle metrics,
and the smooth normal tubular neighborhood theorem. Their use is explicit, not
hidden inside a purported calculation. This family did not conduct a historical
priority audit or replace the separate source-definition review.

## 5. Boundary cases, required findings, and optional findings

**n=0:** a second-countable zero-dimensional manifold is countable and discrete.
Enumerate it by a finite subset of positive integers or by all positive integers.
This is a proper embedding in R; Psi(t)=t^2/2 gives the vacuous induced metric
and connection data. The empty case is vacuous as well. The formula for n>=1
is not misapplied to this case.

**Nonorientable source / nontrivial normal bundle:** every operation in the
completion is a bundle operation invariant under orthogonal changes of frame;
no global normal frame or orientation is presumed. The constructed conormal
field is global by the jet right inverse. Its existence is proved rather than
postulated as a topological assumption.

**Manifolds with boundary, indefinite metrics, and absent second countability:**
these are excluded. This family gives no conclusion about them. No boundary
claim may be inferred from the argument. The original-source interpretation of
"statistical manifold" and "dually flat" must remain as a separate required
whole-package check; this report assumes the exact charter interpretation.

**Required mathematical findings:** none. No counterexample, circular universal
step, wrong ordering, or unaddressed global obstruction was found.

**Optional exposition findings:** retain the current explicit exclusions of
convexity, completeness and global dual-coordinate injectivity; they are
mathematically meaningful. The compact-circle and incomplete-parabola controls
could be useful illustrations, but are not repairs or prerequisites for the
proof. A statement about convex targets, complete ambient geometry, finite
probability models, boundary cases, or optimal dimension would require its own
argument and is not established here.

**Blocked routes:** (a) derive a period obstruction from a closed intrinsic form
without identifying it with phi df; (b) infer source completeness from properness
without ambient completeness; (c) treat induced connection holonomy as ambient
flat holonomy; (d) invoke global convexity from a positive Hessian on a nonconvex
domain; (e) require one uniform noncompact tube or spectral bound. Each route
uses an unsupported stronger premise or is contradicted by an explicit control.
No new repair/search mechanism or extra proof-budget turn was used.

**Strongest verified result:** within this family's scope, the frozen universal
construction survives the requested global/topological adversarial checks.
The report and controls support conditional mathematical acceptance of its
global realization assertion, subject to independent source/dependency and
whole-package adjudication. Novelty and overall research promotion remain
unassessed here.
