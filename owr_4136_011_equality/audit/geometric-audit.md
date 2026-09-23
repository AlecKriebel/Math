# Independent geometric audit

Audit completed: 2026-09-23 04:02 UTC. Completion estimate for this assigned
geometric-proof audit: **100%**. This is a mathematical review of the supplied
argument, not a priority determination or a claim of formal machine verification.

## Exact claim audited

Let \(K\subset\mathbb R^n\) be compact, convex, and have nonempty interior,
where \(n\geq1\). Let \(r>0\), and assume that every extreme point \(v\) of
\(K\) satisfies \(\|v\|_2\geq r\). Write

\[
g_K=|K|^{-1}\int_K x\,dx,\qquad
C_2(K)=|K|^{-1}\int_K\|x\|_2^2\,dx.
\]

The supplied claim is

\[
C_2(K)\geq\frac{r^2+\(n+1\)\|g_K\|_2^2}{n+2},
\]

with equality exactly for the nondegenerate simplices whose vertices have
norm \(r\). The audit focused on the purported new geometric step and on
whether countable decomposition really justifies equality rigidity.

**Verdict: accepted.** No mathematical gap was found in these parts. The
construction has the required countability, positive volumes, and disjointness;
the limiting step does not lose equality information. The details below make
the potentially vulnerable points checkable without relying on a triangulation
theorem for arbitrary convex bodies.

## 1. The extreme-point approximation is legitimate

The extreme-point set need not be closed. That is harmless. A subset of a
Euclidean space is second countable and therefore separable in its relative
topology. Choose a finite or countably infinite dense subset \(D\) of
\(\operatorname{ext}K\), add \(n+1\) affinely independent extreme points, and
enumerate \(D\) without repetition, putting those \(n+1\) points first. Such
independent extreme points exist because finite-dimensional Minkowski's theorem
implies that \(\operatorname{ext}K\) affinely spans \(K\).

For \(P_m=\operatorname{conv}(v_1,\ldots,v_m)\), every subsequently added
point \(v_{m+1}\) is outside \(P_m\). Otherwise it is a convex combination of
distinct points of \(K\), contrary to its extremality. This also proves that
the new hull is genuinely larger at each actual insertion. If \(D\) is finite,
the construction simply stops after its last point.

Density and the finite-dimensional extreme-point theorem give

\[
\overline{\bigcup_m P_m}
=\overline{\operatorname{conv}D}=K.
\]

The union \(C=\bigcup_m P_m\) is convex and contains a full-dimensional
simplex. A full-dimensional convex set has the same interior as its closure,
so \(\operatorname{int}K\subset C\). Thus \(K\setminus C\) is contained
in \(\partial K\), which has zero \(n\)-dimensional Lebesgue measure.

This reasoning does not assume that every boundary point is an extreme point,
or that the boundary is polyhedral, smooth, or strictly convex.

## 2. Strictly visible facets suffice

Write a full-dimensional polytope as

\[
P=\{z:a_F\cdot z\leq b_F\text{ for every facet }F\},
\]

and let \(v\notin P\). A visible facet satisfies \(a_F\cdot v>b_F\).
For \(x\in\operatorname{conv}(P,v)\setminus(P\cup\{v\})\), its ray from
\(v\) intersects \(P\). Let \(y\) be the first intersection. At least one
facet active at \(y\) has \(a_F\cdot v>b_F\). Indeed, if every active
inequality at \(y\) were satisfied at \(v\), then points on \([v,y)\)
sufficiently near \(y\) would satisfy all inequalities: inactive inequalities
remain strict by continuity, and active ones hold along that segment. This
contradicts the definition of the first intersection. Hence

\[
\operatorname{conv}(P,v)
=P\cup\bigcup_{F\text{ visible}}\operatorname{conv}(v,F).
\]

The apex \(v\) belongs to each visible pyramid; at least one such facet exists.
This explicitly deals with the degenerate ray at \(x=v\).

The pyramids have pairwise disjoint full-dimensional interiors. For an interior
point of \(\operatorname{conv}(v,F)\), its ray first meets \(P\) in
\(\operatorname{relint}F\): before reaching the facet hyperplane the facet
inequality is violated. A ray has only one first intersection, and two distinct
facets have disjoint relative interiors. Each pyramid interior is also outside
\(P\), by its violated facet inequality.

Coplanarity with a nonvisible facet therefore causes no gap. It contributes
only lower-dimensional boundary pieces, which are already covered by the finite
union or are irrelevant to the measure statement.

## 3. No new vertices are needed

Every finite polytope can be partitioned into simplices using its vertices.
For completeness, induct on dimension: choose a vertex \(u\), triangulate every
facet not containing \(u\), and cone its simplices to \(u\). Rays from \(u\)
through interior points leave the polytope through those facets, giving a
partition of the interior; closure gives the full polytope. All cones are
nondegenerate, and all vertices are original vertices. The zero-dimensional
base case is a single point.

Apply this fact separately to each visible facet of \(P_m\), then cone to
\(v_{m+1}\). The resulting full-dimensional simplices have vertices among the
enumerated extreme points of \(K\). Compatibility between triangulations on
different facets is unnecessary: only disjoint full-dimensional interiors are
required, and any incompatibility is on lower-dimensional faces. The result
need not be a locally finite simplicial complex, and no such property is used.

Starting with \(P_{n+1}\) and never subdividing previously inserted simplices
produces finitely or countably many nondegenerate simplices. At each stage
there are finitely many new simplices. Their interiors are disjoint within
each shell, from earlier shells, and from the initial simplex. Their union
covers \(C\) (in fact exactly, if each finite triangulation includes its closed
faces), and hence covers \(K\) modulo a null set.

## 4. Countable integration and equality are sound

Let the simplices be \(S_j\), with

\[
w_j=|S_j|/|K|>0,\quad c_j=g_{S_j},\quad
q_j=\frac1{n+1}\sum_{i=0}^n\|x_{j,i}\|_2^2.
\]

Intersections of distinct simplices are null: since their interiors are
disjoint, an intersection is contained in their boundaries. There are only
countably many such boundaries. Consequently countable additivity of the
integrals yields

\[
\sum_j w_j=1,\quad \sum_jw_jc_j=g_K,\quad
\sum_jw_jC_2(S_j)=C_2(K).
\]

All vertices, simplex centroids, and integration points belong to the compact
set \(K\). Therefore all series needed for the second-moment and weighted
variance identities converge absolutely. No unproved interchange of an
unbounded limit and an integral is present.

The supplied simplex moment calculation gives the exact identity

\[
C_2(K)-\frac{r^2+\(n+1\)\|g_K\|_2^2}{n+2}
=\frac1{n+2}\sum_jw_j(q_j-r^2)
 +\frac{n+1}{n+2}\sum_jw_j\|c_j-g_K\|_2^2.
\]

Both summands are sums of nonnegative terms. A zero countable sum of
nonnegative terms forces every term to be zero, irrespective of whether the
weights tend to zero. Since every weight is strictly positive, equality gives
\(q_j=r^2\) and \(c_j=g_K\) for every \(j\). The first condition forces every
simplex vertex to have norm \(r\). The second is stronger: a nondegenerate
simplex has its centroid in its ordinary \(n\)-dimensional interior, so two
distinct simplices with centroid \(g_K\) would have intersecting interiors.
Thus there is only one simplex.

The final equality \(K=S\) follows either from density of the constructed
union, or just from full measure and closedness. For the latter argument,
if an interior point of \(K\) lay outside the closed set \(S\), some ball
inside \(K\setminus S\) would have positive volume. Therefore
\(\operatorname{int}K\subset S\), and taking closures gives \(K\subset S\).
The reverse inclusion is built into the construction.

The converse follows directly from the same simplex moment identity.

## 5. Adversarial boundary checks

- **Dimension one:** \(K=[a,b]\), \(a<b\), has exactly two extreme points.
  The initial simplex is all of \(K\). Equality requires
  \(|a|=|b|=r\), hence \(K=[-r,r]\). Directly,
  \(C_2(K)=(a^2+ab+b^2)/3\), agreeing with the claimed identity and equality
  conditions.
- **Infinitely many very small simplices:** no uniform positive lower bound
  on weights is used. Exact equality forces each individual positive-weight
  variance term to vanish.
- **Nonclosed extreme-point set:** only relative density and closure of the
  convex hull are used; no closedness assumption appears.
- **Flat or nonsimplicial faces:** vertex triangulations and shell construction
  remain valid; matching lower-dimensional face subdivisions is unnecessary.
- **Origin outside \(K\):** neither decomposition nor variance algebra requires
  the origin to belong to \(K\). The theorem with the centroid term still has
  the stated equality class.
- **Degenerate bodies:** excluded by nonempty interior; this assumption must
  be retained because the normalized \(n\)-dimensional integrals otherwise
  need not be defined.
- **Regularity of the equality simplex:** not required. For the strengthened
  theorem with the centroid term, even nonregular triangles inscribed in the
  radius-\(r\) circle attain equality. For the weaker bound
  \(C_2(K)\geq r^2/(n+2)\), equality additionally requires \(g_K=0\).
  The latter extra condition makes equality triangles equilateral; it does
  not force regularity in all higher dimensions.

## Remaining scope

No unfilled geometric or equality-rigidity gap remains in the audited claim.
The precise statement of OWR-4136-011, definitions in the original source,
and priority of the argument require separate source and literature audits.
The proof is elementary but its shortness alone is not evidence of novelty.
