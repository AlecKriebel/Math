# Independent geometry audit of PR40 / target2814

Frozen source head: `163e34d566d6cbaee3a2a8fdc6394fbb9e49a539`.
Source-first reconstruction and seal precede exposure to submitted SOURCE_STATUS.
This is an audit of an existing source-status correction, not a new solution or
new proof-attempt response. Original substantive attempts0/5; added0; audit0.

**Disposition: PASS_SOURCE_STATUS_WITH_EXPLICIT_PROOF_QUALIFICATIONS.** The
submitted package's modest claim—existing full-text theorem statements cover
the exact target, and the recent closed-case source is a preprint—survives this
family's geometric challenge. No claim of complete independent referee
certification is supported. This audit found local printed proof slips and
supplies checkable repairs below; it does not silently treat them as correct.
The remaining external imports and publication-status limits are explicit.

## Exact scope and complete case split

The literal question is about every complete finite-volume hyperbolic
3-manifold, with no orientability restriction. “Infinitely many” means
infinitely many distinct embedded closed-geodesic images, parametrized once
around. Different starting points, reversal and multiple traversal of one
image do not give new geodesics. The geodesics need not be mutually disjoint.
Torsion-free manifold hypotheses matter; this audit proves no orbifold or
arbitrary variable-curvature or infinite-volume statement.

| Manifold | Operative source | What was actually read | Scope check |
|---|---|---|---|
| Closed, either orientation | Luo–Marković v1, Theorems1.4/1.5 | All13 PDF pages, definitions, lemmas, proof, references | Throughout: closed hyperbolic n-manifold, n≥3; no orientation hypothesis |
| Cusped, orientable | Published Kuhlmann2006, Theorem1.1 | All12 PDF pages, pp2151–2162 | Complete, finite volume, orientation explicitly assumed |
| Cusped, including nonorientable | Xia v1, Theorems1.2/4.1 | All11 PDF pages, especially direct Klein-bottle cusp cases | Nonelementary with virtually rank2 cusp; covers finite-volume cusps |

These are primary full texts, not abstracts substituted for proofs. K3
Problem3.16 and original AIM §5.6 supplied the statement before the submitted
status was read. Only their operative statement, surrounding conventions and
boundary pages were read; the entire book/problem collection was not read.
No submitted old review/readiness, root interpretation or live sibling
scientific interpretation was consulted.

Finite-volume complete hyperbolic3-manifolds are either compact or have
Euclidean compact cusp sections. In dimension3 these sections are a torus or
Klein bottle. A nonorientable ambient manifold can still have a torus cusp;
that falls under Xia's toral case. If the chosen cusp has reversing holonomy,
Xia's direct glide-reflection analysis is required. No proof of simplicity
is descended from an orientable double cover.

## Closed-case proof checks and local repairs

The metric definition of δ-collared is sufficient by itself: if γ(x)=γ(y),
then distance0<δ forces circle distance0, hence x=y. It excludes iterates
as parametrized closed geodesics. The printed geometric collar is widthδ/2;
this distinction is immaterial to the injectivity conclusion and is retained.
Period-orbit counts are understood modulo starting phase (and, if desired,
reversal), not as an uncountable set of parametrized maps.

Here is the independently checked exponent chain. Put h=n−1. A fixed-radius
Bowen ball has Liouville volume comparable to exp(−hr): its unstable,
stable and flow dimensions are n−1,n−1,1. For a δ-net, there are O(δ^(−n))
basepoints; a radiuscδ Bowen ball about a pointed loop of lengthℓ has volume
O(δ^(2n−1)exp(−hℓ)). The weighted pointed-loop count is O(r), uniformly in
the basepoint. Therefore a near-return set L has volume O(δ^(n−1)r).
Sampling the initial time with spacingδ gives O(r/δ) shifted near-return
sets and hence a tight-vector measure O(δ^(n−2)r²). Each bad closed orbit
in the length window has a disjoint homotopy fiber of volume at least
c exp(−hr). The usual fixed-window periodic-orbit lower count is
c exp(hr)/r. Their quotient is O(δ^(n−2)r³).

With δ=r^(−κ), the exponent is 3−(n−2)κ. It is negative exactly when
κ>3/(n−2), as asserted. Equality gives an O(1) bound and does not give
vanishing; n=2 is outside this argument. In n=3 any κ>3 works. Windows
going to infinity contain collared, hence embedded once-around geodesics.
A finite collection of such images has bounded lengths, so the resulting
images are geometrically distinct.

The following repairs are needed if the displayed proof is treated literally.
They affect fixed constants or choice of a witness, not the exponent chain.

1. **Lemma2.4, printedp6:** exponential tracking compares w to the selected
   shifted vector v_c. Use the tightness witness belonging to this v_c,
   which the lemma's premise grants for every small shift, rather than the
   unshifted v. Its two witness times remain in the required interior and
   retain their separation. Then the basepoint distance is <δ+2C exp(−r/10),
   hence <3δ for sufficiently large r. The free homotopy is formed with the
   unique short endpoint connector at tolerance3ε, not a map whose domain
   requires w to return withinε. Choose3ε well below injectivity radius.
2. **Lemma1.12, printedp7:** the printed interval [r/4,4r/4] does not establish
   the needed interior margin. If ℓ is the orbit length and I its longer
   x-to-y arc, place z at the midpoint of I. The encounter times relative
   to z lie in [ℓ/4,3ℓ/4]. For ℓ∈(r−ε,r+ε) and |c|<ε, they lie in
   [r/10,9r/10] for all sufficiently large r. The shorter x-to-y arc has
   length at least i_M: a segment shorter than the injectivity radius is
   minimizing and cannot witness the non-collared condition.
3. **Lemma4.2:** endpoint errors≤δ imply |ℓ(α)−ℓ(β)|≤2δ, not≤δ.
   Equalizing lengths gives endpoint error≤3δ. Convexity and the long-half
   segment argument still give c(L)δ with a changed constant.
4. **Lemma5.1, printedp12:** α has length t≥i_M; its straightened pointed
   loop β need not have length≥10i_M. Lift both to the universal cover.
   The endpoint connectors total≤3δ. If β were trivial, the geodesic α
   would have length≤3δ<i_M, impossible. In fact ℓ(β)≥t−3δ≥7i_M/10.
   Apply the corrected Lemma4.2 with L=i_M/2 and endpoint error2δ,
   after shrinking δ0 (for example below i_M/20). The constant depends
   on M, in accord with §1.1; calling it universal is unnecessary.
5. **Lemma3.2 and §3.1:** also require cδ≤the small Bowen-radius threshold,
   choose δ0≤δ1/c, and count floor(r/δ)+1 sample times. For r/δ≥1 this is
   ≤2r/δ. Neither change alters any power.
6. **Net estimate:** use δ below the injectivity radius so the ball-volume
   comparison is the hyperbolic one. The claim for every largeδ is not
   needed when δ=r^(−κ) tends to zero. Uniform pointed-loop constants
   follow from the global positive injectivity radius of closed M.

The weighted upper count can be checked without an orientation assumption:
in H^n, distinct translates of a lifted basepoint are uniformly separated
by at least2i_M. Disjoint fixed-radius balls around them lie in an annulus
of radius s+O(1), whose volume is O(exp(hs)). Summing unit shells after
weighting by exp(−hℓ) gives O(r). The upper-bound mechanism is thus local
metric geometry, not an orientation-cover simplicity assertion.

The lower fixed-window count and uniform Bowen local-product estimates are
standard negative-curvature/Anosov inputs retained as external mathematical
imports. This family read all of the operative13-page preprint, not the
complete cited Margulis, Katok–Hasselblatt, Kahn–Marković or Sullivan works.
For the existence of the straightened geodesic one can use compactness
directly: a long lifted arc closed by a short connector determines a
nonidentity deck element, and every nonidentity deck element of a closed
torsion-free hyperbolic manifold is axial, even if orientation reversing.
No new target route is supplied by this elementary repair. No remaining
central unsupported geometric assertion was found in this reading, but the
unrecertified classical imports prevent a claim that every proof dependency
has itself been fully independently reproved.

## Cusp proof checks

For the normalized horoballs, the finite ball tangent at height1 has radius
1/2 and center at height1/2. Xia printedp3 says radius1; its diagram and
inversion normalization use the radius1/2 configuration. This is a local
normalization typo. The direct argument is not made valid by its abstract.

For large cusp displacement B, the boundary action of t g0 has the form
f(x)=B+R x/||x||², with R orthogonal. If K=||B||>3, f maps the unit ball
about B strictly into itself, with derivative norm≤(K−1)^(−2)<1. Its
inverse similarly contracts the unit ball about0. There is one attracting
fixed point near B and one repelling point near0. Thus these elements are
axial for large displacement; this fills the step left implicit when Xia
begins by supposing g_t hyperbolic. Both endpoints differ from their limits
by O(1/K). Their axis intersects height1 near0 and B. Applying g_t^(−1)
to the far intersection brings it near the tangency point as well.

The short arc lies near that tangency in an injective metric ball, so is
embedded for large displacement. Local finiteness of the lifted horoballs,
and tangency of just the two selected balls there, separates its interior
from all cusp interiors. The long arc is in one horoball. Two of its
interior points can be identified only by an element stabilizing that
horoball. These observations also exclude intersections between the two
arc interiors. This is the geometry behind Kuhlmann Lemmas4.1/4.2 and
Xia Lemma2.2. Injectivity is required on a once-around fundamental arc;
it excludes a multiple traversal.

For a torus cusp choose lattice coordinates, with B0's second coordinate
b2∈(0,1), and translate in the first lattice direction. The projected
chord's second-coordinate variation is still in (0,1) for sufficiently
small endpoint errors. A lattice difference between two chord points
therefore has second coordinate0. It must be parallel to the first
direction, whereas the chord is not. No such distinct pair exists.
Kuhlmann's printed Euclidean error bound should be rescaled by the norm
of the second-coordinate linear functional for an oblique lattice basis;
the coordinates still converge and the required margin is positive.
This repair also makes Xia's higher-dimensional toral estimate precise.

For a Klein-bottle cusp use s(x,y)=(x+α,−y), t(x,y)=(x,y+β), α,β>0.
All translations have x displacement2kα and y displacementmβ;
all reversing elements have odd x displacement and reflection axis at
some mβ/2. The three cases in Xia §4 cover all distinct A0,B0:

* If their x coordinates differ within one fundamental rectangle, translate
  far in y. The chord's x span remains strictly less thanα and positive,
  excluding every glide and every nonzero-x translation. A pure y
  translation cannot identify distinct points on a nonvertical chord.
* If their x coordinates agree and y coordinates are opposite, use t^n s.
  The x span tends toα, below2α, excluding nontrivial translations.
  An actual glide collision on the semicircular geodesic must preserve
  height: the colliding projected points are symmetric about the chord
  midpoint. Its y coordinate is near nβ/2−a, whose distance to the
  half-β lattice is min(a,β/2−a)>0. Thus no glide collision occurs.
* If the common-x endpoints are not opposite, use s^(2n). The chord's
  y span is nonzero and<β, excluding translations. The midpoint y lies
  strictly between −β/2 and β/2 and is nonzero; it remains away from
  every reflection axis for small endpoint errors. Height-preserving
  glide collisions are excluded by this midpoint test.

Endpoint representatives on the rectangle boundary can be moved to an
equivalent rectangle with the endpoints strictly inside where needed.
The half-open lower boundary y=−β/2 in the chosen convention causes no
new case: two distinct equal-x points cannot have average−β/2; averages
are otherwise strict. Opposite nonzero pairs have0<a<β/2.
The maximal cusp height of the long arcs tends to infinity, since their
Euclidean semicircle radii do. A finite collection of embedded images
has bounded height. Hence the produced images are infinitely distinct,
not different powers or different markings of the same curve.

## Finite covers, primitive orbits and negative controls

Let π:N→M be a finite regular cover with deck group D and let C⊂N be
an embedded geodesic circle. Its image is embedded exactly when every
dC is equal to C or disjoint from C. Necessity follows because distinct
lifts of an embedded base circle are components of its preimage.
Conversely, if π(x)=π(y) for x,y∈C, then y=d x for a deck element;
the condition implies dC=C. Thus C/D_C injects into M and is a circle.
D_C acts freely on C, hence by finite circle rotations, and π|C has
degree|D_C|. Proper intersections with a translate invalidate descent.
Images of an infinite good family remain infinite, since each base circle
has at most|D| lifted components. Upward lifting of an embedded base
circle is valid; downward projection of an arbitrary embedded circle is not.
This reproduces the duplicate prior's elementary obstruction, not a new
global family or a resolution of the target.

The controls include an exact primitive but nonsimple orbit in an
**infinite-volume** hyperbolic3-manifold. Set
A=[[1,2],[0,1]], B=[[1,0],[2,1]], g=AB=[[5,2],[2,1]]. The axis of g
in a vertical H² has endpoints1±√2, circle center1 and radius√2.
The A-translate has center3 with the same radius. They cross at
(horizontal2,height1), with distinct tangents. A does not stabilize the
axis. G=<A,B> is discrete (integer matrices) and torsion-free in PSL2R:
its matrices are I modulo2, and a putative elliptic integer trace would
be0; odd diagonal entries and determinant1 rule out trace0 modulo4.
Ping-pong on |x|>1 and |x|<1 makes A,B a free basis. The cyclically
reduced word AB is not a proper power. Consequently H³/G is a manifold
and this primitive axis projects nonsimply. Its volume is infinite:
the Fuchsian normal coordinate has volume density cosh²u over its
nonzero-area surface and unbounded u. This falsifies a proposed
primitive⇒embedded shortcut; it is explicitly not a counterexample to
the finite-volume target.

Other exact rational controls test the strict exponent boundary, nonzero
cusp-coordinate margins, the half-lattice midpoint obstruction, an actual
glide collision when that obstruction is removed, and a projected-chord
glide collision with unequal heights which is not an actual arc collision.
These finite calculations check the stated mechanisms and falsify unsafe
shortcuts. They are not numerical evidence promoted into a universal proof.

## Strongest result and remaining limits

The exact target is covered by the cited theorem statements, with both
orientations correctly handled. Full operative proof reading supplies more
support than abstract or metadata matching. The elementary repairs above
are checkable and do not solve a fresh target. The recent closed source is
v1 of an August2026 arXiv preprint, not verified peer-reviewed publication;
Xia's retrieved source is also v1, with no journal reference in its official
record. Kuhlmann's2006 source is the published paper. The submitted historical
closed-conditional 178/200 census detail is not recertified here: its original
2008 data/proof were not acquired and it is unnecessary to the new case split.

The audit therefore supports a literature-status correction qualified by
preprint reliance and the stated proof imports, not a new theorem, a new
novelty claim, or an independently certified complete solution. Family-local
controls and manifest are reproducible; root adversarial reproduction and
any publication/integration decisions remain outside this family's scope.
