# A uniform vertical-gap bound does not imply movability

13 October 2026. Complementary result within shared substantive pass 2 for row 1767 / 30003527. This is a counterexample to a proposed enlargement lemma, **not a counterexample to the full invariant-enlargement question**.

## Result

There is a compact nonmovable set A in R³ for which every vertical fiber is one of

- the empty set;
- a singleton at height 0 or 1;
- the two-point set {0,1};
- the interval [0,1].

Consequently every vertical fiber has at most two connected components, every bounded complementary fiber gap has length exactly 1, and filling all gaps of length at most ε leaves A unchanged whenever 0<ε<1. In particular, short-gap filling need not produce a movable compactum, even with a uniform component bound of two and with the remaining gaps uniformly separated.

The set A is the stationary set of the bounded globally Lipschitz vector field

F_A(x,y,z) = min(1, dist((x,y,z), A)) e₃.

Thus this is a genuine example within the proposed vertical-slowing flow class. No assertion is made that A has no larger compact invariant movable sets in an arbitrary prescribed neighborhood.

## 1. The general short-gap construction is otherwise valid

Let C be any nonempty compact subset of R³. For p∈R² put C_p={z:(p,z)∈C}. Define

G_ε(C) = C ∪ { (p,z): there exist a,b∈C_p with a≤z≤b and b−a≤ε }.

This exactly adjoins the closed bounded complementary intervals of each C_p whose length is at most ε. An interval between nonconsecutive endpoints causes no difficulty: each complementary gap inside it also has length at most ε.

The parameter set

{ (p,a,b,t): (p,a),(p,b)∈C, 0≤b−a≤ε, 0≤t≤1 }

is compact, and its continuous image (p,(1−t)a+tb) is G_ε(C). Thus G_ε(C) is compact. Its distance from C is at most ε/2, because every point of an adjoined segment is within ε/2 of one of its endpoints. For any open U⊃C, sufficiently small ε therefore ensures G_ε(C)⊂U.

Every remaining bounded gap has length greater than ε. If C lies between heights m and M, its filled fibers have at most floor((M−m)/ε)+1 components. This loose bound suffices, including degenerate fibers. The conclusion follows by selecting one separating gap between each successive pair of components; their disjoint lengths must fit inside [m,M].

For F_C=min(1,dist(·,C))e₃, the horizontal coordinate p is constant along an orbit. On a complementary interval of C_p the scalar velocity is positive, and the orbit through any point is the whole open interval. A finite endpoint belongs to C_p and cannot be reached at finite time by uniqueness for the Lipschitz ODE. Every unbounded complementary interval gives an orbit unbounded in at least one time direction. Consequently the compact invariant sets containing C are precisely C together with selections of whole bounded fiber gaps for which the resulting union is closed. In particular G_ε(C) is invariant.

The field is globally Lipschitz and bounded by 1, so its ODE defines a continuous full flow on all of R³. These facts validate compactness, invariance, containment in U, and the component estimate. They do not imply movability.

## 2. A nonmovable compactum in a three-page book

Let I=[0,1] and let

T = { (x,y,0): x∈I, −1≤y≤1 }
    ∪ { (x,0,z): x∈I, 0≤z≤1 }.

This is I times a triod, equivalently a three-page book with common edge

E = { (x,0,0): x∈I }.

Choose a subset K⊂T homeomorphic to the dyadic solenoid. Its existence is a classical theorem with a directly inspected primary source: R. H. Bing, *Embedding Circle-Like Continua in the Plane*, Canadian Journal of Mathematics 14 (1962), 113–128, **Theorem 8 on printed pp.121–122**, proves that every circle-like continuum embeds in the product of a triod and an arc. The dyadic solenoid is circle-like. The statement and the fin-based iterative construction in its proof were directly inspected.

The dyadic solenoid is nonmovable. One standard verification uses its nested solid-torus expansion, whose first homology inverse system is

Z ←(×2) Z ←(×2) Z ← ···.

In any fixed stage the images of later groups are 2^j Z and never stabilize. Movability implies the Mittag–Leffler condition for this inverse system: if the movability index for stage i is j, the factorization up to homotopy through every later stage forces the image at j to equal every sufficiently late image. This contradiction proves nonmovability. Movability is independent of the embedding in a metric ANR, so the chosen copy K in T is nonmovable as well.

Public primary source:

- https://doi.org/10.4153/CJM-1962-009-3
- https://www.cambridge.org/core/services/aop-cambridge-core/content/view/4BF9863EDD2DC1E32E1BD90E11790F4E/S0008414X00017569a.pdf/embedding_circlelike_continua_in_the_plane.pdf

A second directly inspected primary source confirms and generalizes this embedding: J. Olędzki and S. Spież, *On embedding curves in two-dimensional polyhedra*, Fundamenta Mathematicae 122 (1984), 47–55, Theorem 2.2 and Corollaries 3.4–3.5. Its introduction also explicitly identifies Bing's solenoid example. This second paper is not needed once Bing's Theorem 8 is used.

- https://doi.org/10.4064/fm-122-1-47-55
- https://bibliotekanauki.pl/articles/1363524.pdf

## 3. Stretch the common edge into vertical intervals

Define the compact polyhedron

T* = { (x,y,0): x∈I, −1≤y≤1 }
     ∪ { (x,0,z): x∈I, 0≤z≤1 }
     ∪ { (x,y,1): x∈I, 0≤y≤1 }.

Its cross-section is a triod whose third arm first goes upward and then turns right. Define q:T*→T by the following three formulas:

q(x,y,0) = (x,y,0),
q(x,0,z) = (x,0,0),
q(x,y,1) = (x,0,y).

The formulas agree on the overlaps. Therefore q is a continuous surjection. Every inverse image of a point off E is a singleton, and

q⁻¹(x,0,0) = { (x,0,z): 0≤z≤1 }.

Set A=q⁻¹(K). It is compact. The map q|A:A→K has only point and interval fibers; the usual finite-dimensional cell-like-map theorem immediately gives shape equivalence. Section 4 supplies a direct movability-transfer proof for this particular q, so the counterexample does not depend on an unexamined cell-like transfer assertion.

The vertical fibers of A are explicit. If y<0, the only possible height is 0. If y>0, the only possible heights are 0 and 1. At y=0, the fiber is either empty or [0,1], according as (x,0,0) is outside or inside K. Outside x∈I all fibers are empty. This proves the advertised list of fiber types.

## 4. Direct proof that A is nonmovable

We prove that movability of A would imply movability of K. Neighborhoods in the following argument are relative to the indicated compact polyhedron. This gives the ordinary shape-theoretic notion: a finite polyhedron is an ANR, and movability is independent of the chosen metric ANR embedding. Equivalently, ambient homotopies can be restricted and projected by neighborhood retractions.

For 0<t<1, define a homeomorphism h_t:T*→T. It is the identity on the bottom rectangle. On the upward segment set

h_t(x,0,z) = (x,0,tz),

and on the top rectangle set

h_t(x,y,1) = (x,0,t+(1−t)y).

These formulas agree where the pieces meet and are strictly monotone along the bent third arm. The homeomorphisms satisfy sup|h_t−q|≤t.

Write r for the third-arm coordinate in T. The composition q h_t⁻¹ acts on that arm by

r ↦ 0                         if 0≤r≤t,
r ↦ (r−t)/(1−t)               if t≤r≤1,

and is the identity on the other arms. Thus q h_t⁻¹ is joined to the identity by linear interpolation along each arm, fixing x and the common edge. Every point moves by at most t during this homotopy.

Assume A is movable, and fix a relative open neighborhood O of K in T. Apply movability to q⁻¹(O) to obtain a relative open V* with

A⊂V*⊂q⁻¹(O),

such that V* can be homotoped inside q⁻¹(O) into every neighborhood of A.

Since A=q⁻¹(K) and T* is compact, q(T*\V*) is compact and disjoint from K. Choose η>0 smaller than its distance from K, and choose ρ>0 such that the relative ρ-neighborhood of K is contained in O. If one of the complements is empty, omit the corresponding distance restriction. Choose

0<t<min(1/2,η/3,ρ/3).

Because h_t is uniformly t-close to q, there is a relative open neighborhood V of K in T, lying within distance min(η/3,ρ/3) of K, such that

h_t⁻¹(V)⊂V*.

For example, if a point a lies outside V*, then q(a) is at least η from K, so h_t(a) stays more than 2η/3 from K. This verifies the asserted inclusion for the indicated choice of V.

Now let W be any relative open neighborhood of K. Movability of A supplies a homotopy

H:V*×[0,1]→q⁻¹(O)

with H(a,0)=a and H(V*,1)⊂q⁻¹(W). Hence

(y,s) ↦ q(H(h_t⁻¹(y),s))

is a homotopy in O from q h_t⁻¹|V to a map into W. Prepend the explicit armwise homotopy from the identity on V to q h_t⁻¹|V. It stays in O because its points remain within t of V, hence within 2ρ/3 of K. Concatenation is a homotopy of V in O starting with inclusion and ending in W.

The neighborhood V was chosen independently of W. This is precisely movability of K, a contradiction. Therefore A is nonmovable.

## 5. Failure of short-gap filling, including the slab proposal

Every bounded gap of a fiber of A is (0,1). Consequently

G_ε(A)=A for every 0<ε<1.

The vertical-slowing flow fixes A pointwise, so these failed candidate enlargements are nevertheless compact and invariant. A uniform bound of two fiber components does not control their global shape.

If A is cut by any finite cover by closed horizontal slabs of thickness less than 1, the projection of each nonempty slab piece to R² has nonempty fibers that are points or intervals. Each piece consequently has the shape of a planar compactum and is movable, by the standard finite-dimensional cell-like-map theorem and planar movability. The same holds for nonempty intersections of such slab pieces. Nevertheless their union A is not movable. Thus even adding movability of the slab intersections does not repair the unqualified finite-gluing argument. This observation is supplementary: Section 4 already proves the obstruction without using those transfer theorems.

## 6. What the example does not prove

It does not supply a neighborhood U for which every compact invariant B with A⊂B⊂U is nonmovable. In particular, the length of a gap does not bound its distance from A. A unit vertical gap may run arbitrarily close to the vertical intervals lying over E∩K, and an open neighborhood of those intervals permits filling such nearby long gaps. Those invariant additions are omitted by the length-based construction.

A more appropriate local candidate is the maximal invariant part of a metric neighborhood. For δ>0 set N_δ(A)={x:dist(x,A)≤δ} and

M_δ(A)=Inv(N_δ(A)).

For this flow it consists of A and exactly those whole bounded vertical gaps whose closed segments lie in N_δ(A). It is compact and invariant, and lies in U when δ is sufficiently small. The example above proves no failure of movability for M_δ(A). Establishing its movability, or excluding all invariant movable enlargements, remains a separate problem. Merely replacing gap length by maximum distance to A is not a proof of either assertion.

## Inspection and scope

Bing's Theorem 8 and its proof on printed pp.121–122 were directly read. The Olędzki–Spież paper was downloaded and its scanned pages rendered and OCR-read; the first page and Theorem 2.2 spread were visually inspected. These are imported established embedding results, not claimed new theorems. The stretching construction and the direct neighborhood-homotopy argument above are authored here. No novelty claim beyond the verified local argument is made.

This result is part of shared pass 2, not an additional substantive pass. It defeats one proposed positive lemma and sharpens the remaining gap; the full row-1767 target remains unresolved.
