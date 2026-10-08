# Generalised empty hexagons: five bounded approaches

**Target:** 3091 / OPG-59923. **Research date:** 2026-10-08 (UTC).
**Disposition:** full target unresolved; five substantive approach families exhausted.
This is an authored partial-result and obstruction report, not a proof of the conjecture.
No novelty is asserted for the elementary lemmas or the known results used below.

## 1. Exact target and conventions

For every integer ell >= 3, does there exist a finite integer f(ell) such that
 every finite set P of at least f(ell) distinct points in R^2 contains either
ell points on one line, or a six-element subset S satisfying both:

1. every point of S is a vertex of its convex hull (strict convex position);
2. P intersect conv(S) = S, where conv is the **closed** convex hull?

Thus points on polygon edges block emptiness. Six points merely on the boundary
of their hull need not be a hexagon. The original problem uses “convex position”;
the source paper that states the same extension explicitly uses strict convexity.
We use that stronger, standard hole convention throughout. Infinite dense sets
are outside the finite target; a finite-point theorem does not imply an unrestricted
infinite-set version.

Write F(ell) for the least valid threshold, if it exists, and H=30 for the known
general-position empty-hexagon threshold. Only F(3)=30 is known from the results
used here. No argument below establishes finite F(ell) for every ell >= 4.

## 2. Current sources and inherited work

The Open Problem Garden statement was inspected on 2026-10-08. Its all-ell
extension is also explicitly posed in Abel et al., *Every Large Point Set contains
Many Collinear Points or an Empty Pentagon*, final discussion. Barát et al.,
*Empty Pentagons in Point Sets with Collinearities*, Theorem 1, supplies a
328 ell^2 threshold for **pentagons**, not hexagons. Those authors state the
hexagon extension as open in their introduction.

Heule and Scheucher, *Happy Ending: An Empty Hexagon in Every Set of 30 Points*
(2024), Theorem 1, proves H=30 under general position. Subercaseaux et al.,
*Formal Verification of the Empty Hexagon Number* (ITP 2024), supplies a
Lean-verified geometric-to-SAT reduction and externally checked SAT computations.
This packet does not rerun their full computation or verify the 29-point witness.
The numerical value 30 is a cited prior theorem, not an output of our tests.
The formalization's integration/trust limits are recorded in SOURCE_AUDIT.md.

Gerken's correct DOI is **10.1007/s00454-007-9018-x**, confirmed against the
publisher and Crossref. The inherited bibliographic variant ending **9008-x**
is incorrect. We retain this correction rather than silently copying the typo.

The inherited exact/same-target gate found no substantive earlier attempt in its
bounded inspected corpus and repository coverage. The exact record had no joined
research report; its generic proposed steps were not a proof attempt. General-
position hexagon literature is supporting prior work, not a resolution of this
all-ell target. Our current source search found no primary source settling the
full target; that negative finding is bounded, not a proof of worldwide openness.

## 3. Shared geometric lemma: remove boundary blockers

**Lemma B (boundary cleanup).** Let k >= 3, let P be finite, and suppose S is a
strictly convex k-subset with int(conv(S)) intersect P empty. There is a
closed-empty strictly convex k-subset T of P with conv(T) contained in conv(S).

**Proof.** Put K=conv(S). Among the finitely many strictly convex k-subsets of
P intersect K, choose T minimizing the positive area of conv(T). Such subsets
exist since S is one. For every full-dimensional convex subset K' of K,
int(K') is contained in int(K). Hence conv(T) has no point of P in its interior.
If p in P\T lies on its boundary, p is in the relative interior of an edge uv:
it cannot equal a vertex, since P is a set. List T in counterclockwise order,
with w,u,v successive vertices, and replace u by p=(1-t)u+t v, 0<t<1.

This replacement preserves all k vertices in strict convex position. One way to
check all degeneracies is by support lines. Every unchanged edge not incident
with u has p strictly on its inward side unless it is the edge beginning at v;
for that edge strictness follows from p having a positive coefficient of u.
The new edge wp has u on its outward side and all the other retained vertices
on its inward side; equivalently it cuts off exactly the corner triangle wup.
The edge pv is on uv's support line, with every other retained vertex strictly
inward. More explicitly, the turns at w,p,v are positive: at p the determinant
is (1-t) orient(w,u,v)>0; at v it is (1-t) orient(u,v,x)>0 when k>3,
and at w it is a positive convex combination of the old support determinants.
For k=3 the new triangle is directly nondegenerate, since w is off uv.
Thus conv((T\{u}) union {p}) is conv(T) minus a corner region of positive area,
and is contained in K. This contradicts minimality. Therefore no such p exists,
and T is closed-empty. QED.

An alternative support-line verification useful for checking the proof is this:
with a=w, b=u, c=v, the segment ap lies in the old polygon; all vertices except
b are on the left of oriented ap, strictly except a. Indeed orient(a,p,z)
is a convex combination of orient(a,b,z) and orient(a,c,z); for vertices z
on the remaining c-to-a chain, both are nonnegative and at least one is positive.
This includes z=c. It avoids inferring global convexity solely from positive
local turns, which would be insufficient for an arbitrary self-intersecting list.

The lemma changes the chosen vertices. It does **not** say that the original S
was closed-empty, and it requires strict convexity before the cleanup. It cannot
turn six boundary points with only three corners into six extreme points.

## 4. Attempt 1: perturb to general position, then pass to a limit

**Mechanism.** Apply the H=30 theorem to arbitrarily small general-position
perturbations and attempt to transfer the resulting empty hexagon back.

**Proposition 1.** Any finite P with at least 30 points has a six-element subset
S whose points lie on the boundary of conv(S) and with no point of P in the
ordinary two-dimensional interior of conv(S). The hull may be a segment.

**Proof.** Label P, and take general-position perturbations P_j tending to P.
Their existence follows by avoiding the finitely many zero sets of triple
orientation determinants, and by keeping points in disjoint small balls.
Each P_j has an empty convex hexagon. There are finitely many six-label subsets,
so one subset occurs along an infinite subsequence. Let S be its limit.
A point strictly inside a full-dimensional convex hull stays inside under
sufficiently small movements of the vertices and of the point. To see this
uniformly, if a ball of radius r about q lies in K, then
h_K(a)-a.q >= r for every unit vector a. Moving all relevant points by at most
delta changes this margin by at most 2 delta. Take 2 delta < r.
Consequently no other point of P is in int(conv(S)). A selected point cannot be
in that interior either: removing a strictly interior point does not change the
hull, so the same stability argument would contradict its being an extreme
point in each perturbed six-set. This proves the assertion. QED.

If P has no ell collinear points and 3 <= ell <= 6, S is not collinear.
If h is the number of its actual corners, its h sides contain at most ell-1
points each. Counting corners once gives

    6 <= |P intersect boundary(conv(S))| <= h(ell-2),   3 <= h <= 6.

In particular ell=3 forces h=6, and Lemma B produces a genuine hole. If h=6
happens for a larger ell, Lemma B again suffices. No boundary-free assumption
beyond interior emptiness is needed for that conditional conclusion.

**Explicit obstruction to the transfer.** The six points
(0,0),(2,0),(4,0),(2,2),(0,4),(0,2) have just three hull corners and maximum
collinearity three. Replace the three side midpoints by
(2,-e),(2+e,2+e),(-e,2), with 0<e<1. All six perturbed points form an empty
strictly convex hexagon, while the limiting six points do not. Exact tests check
e=1/2,1/4,...,1/256. This six-point fixture is a local failure of the transfer,
not a counterexample to the large-set conjecture.

**Exact gap.** One must force a perturbation-selected hexagon with six limiting
corners, or find a replacement mechanism that defeats the fewer-corner cases.
The bound on points per line by itself does not do this. For ell>=7 even six
collinear limiting points are allowed. Route blocked; no universal conclusion.

## 5. Attempt 2: delete degeneracies and pack disjoint slabs

**Mechanism.** Extract general-position subsets while explicitly controlling
points deleted from the ambient set, instead of silently treating subset holes
as ambient holes.

Let tau(P) be the least number of points whose deletion removes every collinear
triple. More generally, let D be any such deletion set of size d, and Q=P\D.

**Proposition 2 (sparse-degeneracy bound).** P contains at least

    max(0, floor((|P|-d)/30)-d)

pairwise vertex-disjoint closed-empty hexagons. In particular |P|>=31d+30
suffices for at least one.

**Proof.** Choose a linear functional taking distinct values on all of P.
Sort Q and divide its first 30 floor(|Q|/30) points into consecutive blocks of
30. The closed projection intervals of these blocks are pairwise disjoint.
The H=30 theorem gives a hexagon empty relative to each block. It is also empty
relative to all of Q: every other Q-point projects outside that block's interval.
Every point of D can belong to at most one of these pairwise disjoint slabs,
so at most d chosen hexagons can be blocked by D. The remaining hexagons are
closed-empty in P and use disjoint vertices. QED.

Thus any hexagon-free P satisfies |P| <= 31 tau(P)+29. The constant 30 is
only the cited general-position theorem; replacing it by any valid H yields
|P| >= (H+1)d+H as a sufficient condition by exactly the same proof.

**Why ordinary extraction is insufficient.** A maximal general-position subset
A of size r in a set with no ell collinear points satisfies

    |P| <= r + (ell-3) binom(r,2).

Indeed every point outside A lies on a line through two points of A, or A was
not maximal. Such a line has at most ell-3 further points. Summing gives the
bound even when lines' covered sets overlap. This forces large A, but does not
control the blockers in P\A. A hexagon empty in A may contain one of them.

Nor does bounded collinearity imply tau(P)=o(|P|). For every m, a planar set
of 3m points can have exactly m collinear triples, all pairwise disjoint, and
no other collinear triples. Construct the triples inductively as p-v,p,p+v.
For a new triple, forbid its points from lying on any old pair-line, and forbid
its line from containing an old point. These are finitely many nonzero polynomial
conditions in the four coordinates of p,v; their complement is nonempty (and
contains rational choices). Also forbid coincidences. The only new collinear
triple is the intended one. The resulting set has no four collinear points and
tau=m: at least one deletion per disjoint triple is necessary, and one each is
sufficient. This is an obstruction to the proposed *bound on tau*, not a claim
that the constructed sets lack hexagons.

**Exact gap.** A fixed ell permits linear deletion cost, whereas the slab proof
needs roughly d<|P|/31. A geometric argument locating unusually sparse-degeneracy
islands, or bounding actual blocked slabs much more sharply than d, is missing.
Route blocked at this gap, not promoted to an all-ell bound.

## 6. Attempt 3: arithmetic counterexamples and amplification

**Mechanism.** Seek arbitrarily large hole-free examples at a fixed collinearity
bound, starting with lattice parity obstruction.

**Proposition 3.** For m>=2 the square grid G_m={0,...,m-1}^2 has maximum
collinearity m and has no closed-empty strictly convex k-gon for any k>=5.
Consequently, if F(ell) exists,

    F(ell) >= max(30, (ell-1)^2+1).

**Proof.** A vertical line meets G_m in at most m points; a nonvertical line
has at most one point at each of the m x-coordinates. Rows attain m.
Among five or more lattice vertices, two a,b have the same parity in both
coordinates. Their midpoint c=(a+b)/2 is an integer point of the grid and lies
in their closed convex hull. It is not one of the chosen vertices: a strictly
convex vertex cannot be a nontrivial convex combination of two others.
Thus c blocks closed emptiness, including when ab is a polygon edge.
Set m=ell-1. The additional bound 30 follows from the known 29-point
hexagon-free general-position example, which also avoids ell collinear points
for every ell>=3. QED.

This parity proof is a reconstruction of the familiar grid obstruction noted
in the pentagon literature; it is not a new lower-bound discovery.

**Amplification obstruction.** Enlarging the grid enlarges its lines. Invertible
affine transformations preserve cardinality, collinearity, strict convexity,
and closed-hull membership, so they cannot enlarge this fixed-ell family.
A perturbation may break the parity-midpoint blockers: the six-point fixture in
Attempt 1 is itself a concrete example of a degenerate set acquiring a hole.
Replacing grid sites by clusters would need a new proof that all mixed-cluster
hexagons remain blocked while every line has bounded size. No such construction
was obtained. Finite grid enumeration below does not supply an infinite family
for a single ell. Route blocked; no counterexample to the conjecture.

## 7. Attempt 4: convex-layer descent and boundary-only sets

**Mechanism.** Reduce a potential counterexample to its innermost convex layers
and try to bound their capacity.

**Proposition 4 (boundary-only case).** If all points of P lie on the boundary
of conv(P), P has no ell collinear points, and |P|>5(ell-2), then P contains a
closed-empty hexagon.

**Proof.** The collinear case has at most ell-1 points and cannot meet the size
hypothesis. Otherwise let h be the number of hull corners. Each hull edge has
at most ell-1 points, and counting corners once gives |P|<=h(ell-2). Thus h>=6.
Select any six hull corners. They are in strict convex position. Their hull's
interior lies in int(conv(P)), so contains no point of P. Apply Lemma B. QED.

This is a sufficient bound; no optimality is claimed. In particular, a subset
of a polygon boundary can have *more* corners than the original polygon, so
one must not infer a necessary upper bound on hole size from h alone.

For an arbitrary P, remove **all** boundary points of its convex hull and
repeat; let L be the nonempty final layer. Any previously removed point lies
outside conv(L): after each removal, the remaining hull lies strictly inside
the previous hull. Hence any closed-empty hexagon of L is also one of P.
It follows that every hexagon-free set with no ell collinear points satisfies

    |L| <= 5(ell-2).

**Exact gap.** This only bounds the last layer. Earlier layers can be blocked
by points deeper inside; it is invalid to apply the boundary-only proposition
as though those blockers did not exist. There is no bound here on the number
of layers or on the sizes of earlier layers. Arbitrarily many nested triangles
can be placed in general position by successive generic choices; their last
layer always has three points, even though sufficiently large such sets have
hexagons elsewhere. Thus a small final layer does not by itself control total
size. A new interaction lemma between layers is required. Route blocked.

## 8. Attempt 5: enlarge an empty pentagon through an empty ear

**Mechanism.** Use the known bounded-collinearity pentagon theorem, then force
one additional extreme vertex by a minimal-distance argument.

Let S=(v_0,...,v_4) be an empty pentagon, counterclockwise, and set
D_i(q)=orient(v_i,v_{i+1},q), with indices modulo 5. Define the open extension
region for edge i by

    E_i = {q : D_i(q)<0 and D_j(q)>0 for every j != i}.

**Proposition 5 (nearest-ear extension).** If P meets E_i, then P contains a
closed-empty hexagon whose vertices include all five vertices of S.

**Proof.** Select q in P intersect E_i minimizing -D_i(q)>0. As q is outside
just edge i and strictly inside all the other edge halfplanes, inserting q
between u=v_i and v=v_{i+1} gives a strictly convex hexagon. At u and v its
strict turns are respectively the strict inequalities for the preceding and
following edges, and at q the turn is -D_i(q)>0; geometrically its hull is
conv(S) union triangle(u,v,q), attached along uv.

Any potential blocker p in that closed triangle, other than u,v,q, has a convex
representation p=alpha u+beta v+gamma q. If gamma=0 it lies on uv, which is
already clear by the emptiness of S. Otherwise 0<gamma<1. For every j != i,
D_j(p)>0 because D_j(u),D_j(v)>=0 and D_j(q)>0; and
-D_i(p)=gamma(-D_i(q)) lies strictly between zero and -D_i(q). Therefore p is
in E_i closer to its base line, contradicting minimality. This includes points
on uq or vq. No point lies in conv(S) either. The hexagon is closed-empty. QED.

**Corollary.** In a hexagon-free set every empty pentagon has all five E_i
devoid of points of P. For |P|>=328 ell^2 and no ell collinear points, an empty
pentagon exists by the cited theorem, so any counterexample must obey this
empty-region constraint for every such pentagon.

**Explicit limit of the argument.** For
S={(0,0),(4,0),(5,3),(2,5),(-1,3)} and q=(10,-2), S remains empty and q lies
outside exactly two of its edge halfplanes. The six-point set has only five
hull corners, no collinear triple, and no empty hexagon. None of the five E_i
contains a point of P. Thus nonempty exterior does not imply an available ear.
This small fixture is not a counterexample to the large-set conjecture.

**Exact gap.** The pentagon theorem does not guarantee an empty pentagon with
an occupied one-edge extension region. Forcing one, or exploiting the global
structure of all the empty E_i, remains the hard step. No size bound follows
from Proposition 5 alone. Route blocked.

## 9. Final scope and success criteria

The five approaches use different mechanisms: topological stability under
perturbation; deletion/packing; arithmetic blocking constructions; convex-layer
capacity; and extremal geometric extension. Source checking, implementation,
finite enumeration, and adversarial checking are validation activities, not
additional approaches or hidden proof-search turns.

The strongest established conditional conclusions are Propositions 2, 4, and 5,
with complete proofs above. Proposition 1 identifies the exact degeneracy loss;
Proposition 3 reconstructs the quadratic grid lower bound. None settles the
all-ell statement or the ell=4 case. None is advertised as novel.

A full positive resolution must bound the size of every hexagon-free set with
at most ell-1 points on any line, uniformly for each fixed ell. A full negative
resolution must give arbitrarily large such sets for one fixed ell. Neither
artifact has been produced. The correct campaign disposition is **exhausted,
5/5, unresolved with proved elementary partials**, subject to independent audit.

The finite executable checks validate the supplied examples and implementations.
They are not universal geometric proofs, independent reproduction of H=30, or
formal verification of the prose arguments. See VERIFICATION.md and the exact
receipts. No external source documents or dataset contents are in this packet.
