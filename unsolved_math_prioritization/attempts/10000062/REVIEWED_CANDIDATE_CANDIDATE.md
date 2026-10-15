# Congruent diameter-radius balls without cocompact Euclidean symmetry

**Source record:**10000062 / AMR-099-0062.

**Current scoped result:** verified Euclidean noncocompact member of the prior Frettlöh–Garber family. Three independent complete mathematical/source families and root universal audit PASS; new complete current acceptance gate pending. Full source remains unsolved: horizontal translations remain, source periodicity is undefined, and no hyperbolic full-ball result or novelty is certified. Original1/5 preserved; extensive AI/unrefereed review. Original scientific sections1 onward are unchanged.

## 1. Source, definitions, and attribution

The [original source](https://www.wisdom.weizmann.ac.il/~itai/erd100.pdf),
Question5.7, p.7, asks about triangulations of the Euclidean **or** hyperbolic
plane whose triangles have diameter at most r and whose vertex-centered
radius-r metric balls are related by ambient isometries respecting the
triangulation. The exact page was recovered through the
[dated archive copy](https://arquivo.pt/noFrame/replay/20201231041538id_/http://www.wisdom.weizmann.ac.il/~itai/erd100.pdf)
and visually checked. It does not define “periodic.”

Two possible conclusions must be kept distinct:

- **Cocompact/crystallographic:** the full symmetry group has a compact
  fundamental domain; in the Euclidean plane this is rank-two periodicity
- **A nonzero translational period:** at least one nonidentity translation
  preserves the triangulation

The example below disproves the first conclusion in the Euclidean plane and
satisfies the second. It does not produce a hyperbolic example.

The underlying alternating-layer family is already in
[Dirk Frettlöh and Alexey Garber, *Symmetries of Monocoronal Tilings*](https://arxiv.org/abs/1402.4658),
Section2.3, Figure8, and AppendixA.1.2/Figure17. In particular their
non-crystallographic layered triangulations are prior work. What is checked
here is a concrete rational-coordinate specialization and the stronger
**whole metric-ball** condition at the diameter threshold. No novelty or
priority claim is made for the family or this specialization.

A triangulation here is an ordinary locally finite, face-to-face partition
into nondegenerate straight Euclidean triangles. To preserve its restriction
to a closed disk means to map the restricted vertices, edge pieces, and face
pieces, including pieces on the boundary circle. The proof explicitly treats
the outer caps and boundary-only intersections; it does not replace the disk
by the incident vertex star.

## 2. The explicit family

Choose any bi-infinite sequence \(\epsilon_j\in\{-1,1\}\), and put

\[
\delta_j=1+\epsilon_j/2\in\{1/2,3/2\}.
\]

Let \(a_0=0\) and determine \(a_j\), for all integer j, by

\[
a_{j+1}=a_j+\delta_j+1.
\]

There are two rows per layer:

\[
L_{j,k}=(a_j+2k,4j),\qquad
U_{j,k}=(a_j+\delta_j+2k,4j+1),\quad j,k\in\mathbb Z.
\]

Triangulate the short band between \(L_j\) and \(U_j\) using

\[
[L_{j,k},L_{j,k+1},U_{j,k}],\qquad
[U_{j,k-1},U_{j,k},L_{j,k}].\tag{2.1}
\]

Triangulate the tall band between \(U_j\) and \(L_{j+1}\) by the same rule,
with lower row \(U_j\), upper row \(L_{j+1}\), shift1, and height3:

\[
[U_{j,k},U_{j,k+1},L_{j+1,k}],\qquad
[L_{j+1,k-1},L_{j+1,k},U_{j,k}].\tag{2.2}
\]

The two types of triangles partition their strips without overlap. Adjacent
strips share the same row edges, so this is a face-to-face triangulation of
all of \(\mathbb R^2\). It is locally finite: the row heights are separated by
at least1 and the spacing along each row is2.

There are only two unordered triples of squared side lengths:

\[
\{5/4,13/4,4\}\quad\text{and}\quad\{4,10,10\}.\tag{2.3}
\]

The areas are1 and3 respectively. Set

\[
r=\sqrt{10}.
\]

For a Euclidean triangle the diameter equals its longest side, so every
triangle has diameter at most r. Some tall triangles attain the bound.

## 3. Exact metric-ball locality

### Lemma3.1: a lower-row ball depends only on its own short band's chirality

Translate \(L_{j,k}\) to the origin and relabel j=0,k=0. The relevant rows
are then

\[
\begin{array}{c|c}
y&\text{horizontal coordinates modulo2}\\\hline
-4&-1-\delta_{-1}\\
-3&-1\\
0&0\\
1&\delta_0\\
4&\delta_0+1.
\end{array}\tag{3.1}
\]

The disk D of radius \(\sqrt{10}\) about the origin lies strictly between
y=−4 and y=4. In the three bands from y=−3 through y=4, the triangulation is
determined entirely by \(\delta_0\). Only the small cap below y=−3 might see
\(\delta_{-1}\). We check that cap exactly.

The line y=−3 meets D in the segment from \((-1,-3)\) to \((1,-3)\), and
both endpoints are on the circle. Every nonhorizontal edge extending below
that line has vertical displacement −1 and horizontal displacement of
absolute value at most3/2.

At a nearest endpoint \(p=(\pm1,-3)\), write its downward edge as
\(p+t v\), \(0\le t\le1\), where \(v=(h,-1)\) and \(|h|\le3/2\). Then

\[
p\cdot v=3\pm h\ge3/2,
\]

and hence, for every \(t>0\),

\[
|p+tv|^2=10+2t(p\cdot v)+t^2|v|^2>10.\tag{3.2}
\]

Thus these edges meet the closed disk only at their initial endpoint.
Every other upper endpoint of such an edge has \(|x|\ge3\). Along its whole
edge, \(|x|\ge3/2\) and \(|y|\ge3\), giving

\[
x^2+y^2\ge(3/2)^2+9=45/4>10.\tag{3.3}
\]

The lower horizontal row y=−4 is outside D. Therefore the cap
\(D\cap\{y\le-3\}\) contains no further edge pieces: it is the portion of
a single triangle having the fixed base \([(-1,-3),(1,-3)]\). Its shape inside
D is independent of the remote apex and of \(\delta_{-1}\).

This accounts for boundary-only traces too. At each of the two endpoints,
exactly three additional closed edge traces are that single point, and
exactly two additional closed triangle traces are that single point. Their
cyclic incidence pattern is unchanged by the remote choice. All other traces
are fixed. There is no dependence on \(\delta_1\), since its band begins at
y=4>r. This proves the lemma for closed disks, and consequently for open
disks as well. ∎

### Lemma3.2: all vertices and both chiralities have congruent balls

The reflection \((x,y)\mapsto(-x,y)\) exchanges short-band shifts1/2 and3/2
modulo the horizontal period2, and preserves the tall-band geometry. Thus
Lemma3.1's two possible lower-row patches are congruent.

For an upper-row center \(U_{0,0}=(\delta_0,1)\), use the half-turn

\[
(x,y)\longmapsto(\delta_0-x,1-y).\tag{3.4}
\]

This sends that center to a lower-row center at the origin. It takes the
central short strip to itself, reverses the order of the surrounding strips,
and interchanges the two adjacent tall strips. The transformed entire tiling
is another member of the same family, with the same central \(\delta_0\)
and possibly different neighboring choices. Lemma3.1 makes those neighboring
choices irrelevant inside the radius-r disk.

Finally, translations by row offsets and by multiples of2 reduce arbitrary
\(L_{j,k}\) and \(U_{j,k}\) to these cases. Composing the resulting ambient
isometries maps the radius-r ball at any vertex to that at any other vertex,
respecting all restricted cells. ∎

### Why the face statement follows, not just a graph statement

Inside the open disk, edges and vertices divide it into the relative interiors
of the clipped triangular faces. Each nonempty such face is convex and
connected. The described isometries map their boundary edge pieces and the
appropriate side of each boundary line, so they map the face pieces too.
Taking closures preserves their circle intersections. The only external-band
cap was separately identified above as one fixed circular cap; point-only
edge and face traces at its endpoints were counted and matched explicitly.

## 4. A concrete non-cocompact member

Take a single exceptional short band:

\[
\delta_0=1/2,\qquad \delta_j=3/2\quad(j\ne0).\tag{4.1}
\]

For these choices the offsets can be written without recursion:

\[
a_j=\begin{cases}
5j/2,&j\le0,\\
5j/2-1,&j\ge1.
\end{cases}
\]

### Proposition4.1: its translation group is precisely \(2\mathbb Z\times\{0\}\)

By (2.3), edges of length2 are exactly the horizontal row edges. Their
supporting lines, in increasing height, have the alternating spacings1 and3.
A translation symmetry must map a row having a height1 band above it to
another row with that same property. These are exactly the rows y=4j.
Its vertical component is therefore4m for some integer m.

A short band has a metrically detectable chirality: read the sign of the
horizontal displacement of its shortest cross-edge when going from its
lower row to its upper row. It is positive for shift1/2 and negative for
shift3/2. A translation cannot reverse that sign. Hence a translation by
vertical component4m must satisfy \(\delta_{j+m}=\delta_j\) for every j.
The unique exceptional band in (4.1) forces m=0. Preserving the vertices of
any row then forces the horizontal component to lie in \(2\mathbb Z\).
Conversely every such horizontal translation plainly preserves (2.1)–(2.2). ∎

### Proposition4.2: the full symmetry group is not cocompact

Any isometry preserving the triangulation preserves the uniquely characterized
horizontal edges of length2. Its linear part must therefore preserve the
horizontal direction, and is one of the four diagonal orthogonal matrices.
The translation subgroup has index at most4 in the full symmetry group G.
If G had a compact fundamental set, finitely many coset representatives would
produce a compact fundamental set for its translation subgroup. But
\(2\mathbb Z\times\{0\}\) cannot move a point's height; no compact set and
its horizontal translates cover the plane. This is a contradiction. ∎

Together with Lemma3.2 this proves the scoped Euclidean counterexample.
It has a nonzero horizontal period and is not strongly aperiodic.

## 5. Exact checks, boundaries, and source disposition

`python3 verify.py` uses `fractions.Fraction`. It checks all eight assignments
to the neighboring short bands at both row types, sixteen rooted cases.
After the explicitly prescribed isometries, every case has the same:

- 8 vertices in the closed disk
- 28 edges with a positive-length intersection
- 23 positive-area face pieces, using their oriented supporting inequalities
- Two boundary-only locations, each with3 edge traces and2 face traces

The check compares whole endpoints for edges with a positive-length trace,
which is stronger than equality of their clipped pieces in this family.
It separately compares oriented face inequalities and point-only trace
multiplicities. The analytic locality reduction establishes why no omitted
farther layer or edge can affect these finite comparisons.

All coordinates are rational, and the circle has rational squared radius10.
The checker also confirms the two triangle side-length triples and areas.
A negative control at squared radius1001/100 detects the previously hidden
neighboring-layer choice in the canonical patch. This illustrates why one
cannot freely increase the radius used in the proof.

### What is not established

- The source does not define its intended periodicity convention. Under the
  weaker conclusion “has a nonzero translation,” this example is no refutation
- No hyperbolic triangulation satisfying the full ball hypothesis is supplied
- No novelty claim is made for the layered family, which is explicitly prior
  work, nor is global priority established for this metric specialization
- The source's two ambient geometries are not merged into a claim that both
  clauses have been resolved
- This note does not impose or prove the condition with triangle diameters
  strictly smaller than the radius

For ordinary straight Euclidean triangulations, the ball hypothesis implies
congruent incident vertex coronae because the diameter bound puts every
incident triangle in the closed ball. Frettlöh–Garber's Theorem2.2 therefore
already gives at least one translational period for that weaker Euclidean
interpretation. Their hyperbolic examples and the later rhombus constructions
have weaker corona hypotheses and do not by themselves check this metric-ball
condition.

The appropriate current status is **candidate for the explicitly scoped
Euclidean cocompact counterexample; source-level classification unresolved**,
not an unconditional claim that all of AMR-099-0062 is solved.
