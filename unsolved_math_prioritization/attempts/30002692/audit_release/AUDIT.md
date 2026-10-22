# Independent adversarial audit: one hyperbolic conformal boundary

## Verdict and exact scope

The frozen author construction is mathematically sound. It gives a connected,
orientable, complete hyperbolic three-manifold with a smooth compact conformal
compactification and exactly one boundary component. That component is an
orientable genus-two surface with a representative metric of sectional curvature
-1. The Einstein normalization is Ric(g) = -2g.

This answers the dimension-unrestricted existential question printed on page
2550 of Eric Woolgar's 2014 contribution. The same end-swapping construction is
explicit in Xi Yin's 2008 version and in Skenderis and van Rees's 2010 version.
No novel theorem or construction is established by this packet. Recommend
`already_solved`, with one of five substantive approaches charged, only with the
explicit qualification that the accepted statement is the inspected primary
statement. An unqualified assertion about the exact current aggregator statement
is not approved: its page remained inaccessible, and raw AI-problem corpora were
not available for comparison.

No mathematical correction to the frozen author proof is required. This is an
AI-assisted independent verification, not human peer review or a formal proof.

## Source and scope challenge

The audit re-downloaded all three primary PDFs from their institutional/arXiv
URLs. Each independently retrieved PDF has exactly the author-reported size and
SHA-256. Fresh extractions also agree byte-for-byte with the corresponding local
extracts. The relevant pages were read, with visual inspection of Woolgar pages
2549-2550, Yin page 20, and Skenderis-van Rees pages 20-21. Public version histories
confirm the earlier dates. SOURCE_AUDIT.json records the public source metadata
and retrieval results without distributing source content.

Woolgar's complete contribution uses the bulk dimension as its dimension
parameter. Its stated ambient restriction is unobstructed asymptotically
Poincare-Einstein metrics. It discusses several particular dimensions and black
hole topologies as examples, but does not impose those choices on the concluding
existence question. The printed question and its surrounding contribution impose
no fixed dimension, dimension parity, orientability, spin, simple connectivity,
handlebody topology, prescribed boundary metric, prescribed filling topology,
volume constraint, or exclusion of this Fuchsian-derived quotient. In particular,
the examples concerning four-dimensional black holes do not silently change the
quantifier in the concluding question. Unstated author intentions cannot be
certified; the decision is expressly about the printed assertion.

The unobstructed restriction is met by an exact smooth even geodesic expansion
below. This does not assert that the conformal anomaly vanishes: absence of a
metric logarithm and absence of a renormalized-volume anomaly are different
properties. The author proof correctly avoids conflating them.

The live aggregator URL independently returned HTTP 403. The supplied catalog
descriptor identifies ID 30002692, code OWR-13347-011, rank 720 and the matching
report DOI. That is an identity aid, not a checked transcript of the inaccessible
statement. Neither an upstream open label nor a queued local entry is evidence
against the prior construction. The audit does not certify exhaustive historical
repository searches or worldwide current open status.

## Independent complete geometric verification

### 1. A hyperbolic surface and the required free symmetry exist

Take a regular hyperbolic hexagon whose angles are pi/3. Existence follows, for
example, by assembling twelve congruent hyperbolic right triangles with angles
pi/6, pi/6, pi/2. The angle sum is strictly below pi, and rotation about the common
center produces the six equal sides and six stated angles. Identify successive
side pairs according to the polygon word a a b b c c, in the direction of boundary
traversal. Each pair consists of equal geodesic edges.

These pairings identify all vertices. The corner link is a single cycle passing
through all six corners, and its total angle is 2pi. Away from the corners two
geodesic half-disks glue to a hyperbolic disk. Around the vertex the six sectors
form a full disk with angle 2pi, so neither an orbifold cone nor a metric seam
occurs. The quotient is therefore a closed smooth hyperbolic surface N. It has
one face, three edges, one vertex and Euler characteristic -1. The equal-direction
pairings are orientation reversing as surface gluings, so N is nonorientable; this
is the closed nonorientable surface of genus three.

Let S be its orientation double cover. The cover is connected because N is
connected and nonorientable. The pulled-back metric h has curvature -1. The deck
involution tau is an isometry with no fixed points: a nonidentity deck map of a
connected cover that fixes a point fixes all lifted paths and is the identity.
By the definition of the orientation cover it reverses the canonical orientation
on S. Multiplication of Euler characteristic by the covering degree gives
chi(S) = -2; hence S is the closed orientable genus-two surface. This supplies a
specific surface, rather than assuming such a symmetry for every metric on every
prescribed boundary.

The independent diagnostics also construct the two-sheeted lifted polygon cell
structure. Its dual graph is connected, its two vertex links are circles, and its
cell counts are V=2, E=6, F=2. These finite checks support the explicit construction;
the preceding local geometric argument supplies its smooth hyperbolic metric.

### 2. The product metric really has sectional curvature -1

On X = R x S put g = dt^2 + cosh(t)^2 h. One independent local derivation uses
the hyperboloid model. Write a local lift of S as y in the unit hyperboloid H^2 in
Minkowski three-space, so <y,y> = -1 and <y,dy> = 0. In Minkowski four-space the
map F(t,y) = (cosh(t)y, sinh(t)) lies in H^3, since

    <F,F> = -cosh(t)^2 + sinh(t)^2 = -1.

Its differential has squared norm dt^2 + cosh(t)^2 h: the radial vector has
norm -sinh(t)^2 + cosh(t)^2 = 1, cross terms vanish, and tangential norms are
scaled by cosh(t)^2. This is a local isometry onto hyperbolic three-space, and
therefore establishes the full constant-curvature tensor, including arbitrary
mixed two-planes. Thus Ric(g) = -2g and scalar curvature is -6.

As an independent algebraic check, independent_checks.py starts directly with
coordinates q=exp(t), v, y>0 and the upper-half-plane metric

    g = dq^2/q^2 + ((q^2+1)/(2q))^2 (dv^2+dy^2)/y^2.

It differentiates the coordinate metric to construct the Christoffel symbols and
all 81 Riemann components, compares them to curvature -1, and contracts all nine
Ricci components. It does not call or import the author's warped-product checks.

### 3. The quotient is free, smooth, and orientable

The map J(t,p) = (-t,tau(p)) has order two and preserves g. Any fixed point
would satisfy t=0 and tau(p)=p, which is impossible. A finite free smooth action
is proper; its quotient M is a smooth manifold and X -> M is a Riemannian
covering. Near t=0 choose a small neighborhood U in S disjoint from tau(U).
The product neighborhoods about (0,p) and (0,tau(p)) are exchanged and map to a
single ordinary three-dimensional chart. There is no reflecting boundary or
orbifold stratum at the middle. The middle surface is N, smoothly embedded with
a nontrivial normal line bundle. A nonorientable one-sided surface inside an
orientable three-manifold is permissible.

Reflection in t reverses the R orientation and tau reverses the S orientation.
Their product preserves orientation, which descends to M. Connectedness descends
from the connected X. Local isometry preserves the curvature and Einstein tensor.

### 4. Completeness survives the construction

For every tangent vector g is at least dt^2+h. The latter product metric is
complete, since the compact S is complete. A g-Cauchy sequence is therefore
Cauchy for the complete product metric and has a limit. Smooth positive definite
metrics are uniformly comparable on a small relatively compact neighborhood of
that limit, so the sequence also converges for g. This proves metric completeness
and hence geodesic completeness by Hopf-Rinow. Geodesics in M lift through the
Riemannian covering to complete geodesics in X; their projections extend for all
time. Thus quotienting has not introduced any incomplete end or interior edge.

### 5. A global defining function and compact closure

A second compactifying coordinate, independent of the author's trigonometric
coordinate, is z = tanh(t/2). Then -1<z<1 and

    rho(z) = (1-z^2)/(1+z^2),
    rho^2 g = 4 dz^2/(1+z^2)^2 + h.

On the compact cylinder [-1,1] x S, the rescaled metric is smooth and positive
definite. The smooth rho is positive inside, vanishes exactly at z=-1 and z=1,
and has derivatives +1 and -1 at those endpoints. It is a global defining
function. The involution extends as (z,p) -> (-z,tau(p)); both rho and the
rescaled metric are invariant. The action remains free on the whole cylinder
and exchanges its two boundary components. Its compact quotient is a smooth
manifold with boundary and interior M. There are no corners: each boundary
orbit has two distinct representatives with ordinary half-space neighborhoods.

The map p -> [(1,p)] from S to the quotient boundary is a diffeomorphism. Every
orbit on the two original boundaries has exactly one representative on z=1.
Hence the boundary is S, not N = S/tau, and its induced metric is precisely h.
It is compact, connected, orientable, and has sectional curvature -1.
Compactness of the cylinder quotient and identification of its entire interior
exclude extra ends. More explicitly, the complement of a large compact central
region is the quotient of two collars interchanged by J and is one connected
collar of S.

### 6. The stated unobstructed regularity holds

On the quotient boundary collar choose its t>0 representative and set x=2e^-t.
The negative-end formula 2e^t is the same function after J identifies the ends.
One obtains the exact identity

    g = x^-2 [dx^2 + (1+x^2/4)^2 h]
      = x^-2 [dx^2 + h + (x^2/2)h + (x^4/16)h].

This is a smooth geodesic compactification with only even powers and no logarithmic
terms, not merely a formal truncated expansion. The metric is exactly Einstein.
It meets the unobstructed APE requirement in the primary context. The collar
function is not used globally as 2e^-|t|, which would not be smooth at t=0; rho
above is the global function. No anomaly, spin, volume, or prescribed-dimension
conclusion is needed.

## Prior construction and limits of the literature match

Yin, arXiv:0710.2129v2, section 6, equation (6.1), printed page 20, describes the
cosh-warped hyperbolic product and its quotient by radial reflection combined
with a fixed-point-free orientation-reversing involution. The result has one
conformal boundary. This is the exact mechanism audited here.

Skenderis and van Rees, arXiv:0912.2090v2, section 4.2, equations (44)-(46),
printed pages 20-21, independently repeat the product, the free combined quotient,
and the boundary expansion. Their language for the central quotient is not used
to infer its orientability: for our orientation-reversing involution the core is
the nonorientable surface N, whereas the conformal boundary is the orientable S.
Neither paper is being relied on as a substitute for the global proof above.
The existence of these printed pre-2014 constructions is sufficient to reject a
novelty claim for the audited construction. It is not an exhaustive priority
investigation, and no claim about the first discovery is made.

## Adversarial controls and acceptance boundary

The original archive and manifest were independently hash-bound, their exact
inventory and member bytes compared with the frozen directory, and the author's
32 diagnostics and seven negative integrity controls replayed in isolation. The
new symbolic/geometric diagnostics give 31 positive controls, including all 81
tensor components, plus ten explicit mathematical mutations rejected. Additional
archive and scope-integrity mutations are recorded in REPLAY_RESULTS.json.

The rejected mathematical alternatives include a wrong warp scale, the sinh or
exponential warp with a negative-curvature fiber, a flat fiber, a wrong Ricci
normalization, pure reflection with fixed points, failure to swap ends, the wrong
orientation sign, a nonsmooth global exponential, and an erroneous polygon angle.
These controls are diagnostic. They cannot replace the mathematical proof of
hyperbolic polygon existence, covering theory, completeness, or smooth quotient
compactification.

The original author release and original archive remain unchanged. This audit
contains no primary PDFs, source extracts, page images, raw imported records,
credentials, or private coordination material. No remote write was performed.
Acceptance must retain the primary-statement limitation, prior-construction
attribution, one-approach count, and AI-assisted/unrefereed status.

## Public source links

- Woolgar contribution in the 2014 report: https://doi.org/10.4171/OWR/2014/45
- Institutional record: https://publications.mfo.de/handle/mfo/3435
- Xi Yin, *Partition Functions of Three-Dimensional Pure Gravity*: https://arxiv.org/abs/0710.2129v2
- Kostas Skenderis and Balt C. van Rees, *Holography and wormholes in 2+1 dimensions*: https://arxiv.org/abs/0912.2090v2
