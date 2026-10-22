# A counterexample to full-supercritical bond uniqueness near the square lattice

## The result and the question it answers

There is an infinite, connected, simple graph G of maximum degree four, uniformly quasi-isometric to the nearest-neighbor square lattice Z², such that

\[
p_c(G)\le \frac9{10}<\frac{19}{20},\qquad
\mathbb P^G_{19/20}(N_\infty\ge2)
>\frac{2200741829}{6461571200}>\frac13.
\]

Here every actual graph edge is open independently with the same probability p, and N∞ is the number of infinite open components. Thus this is a supercritical iid bond example, not an inhomogeneous or dependent percolation model on the actual graph.

The source is Itai Benjamini's *Coarse Geometry and Randomness*, author manuscript dated 30 October 2013, Open Problem 9.6 on printed/PDF page 64. Its conventions permit arbitrary bounded-degree graphs and define rough isometry with both multiplicative and additive distortion. The short question does not itself specify p. The chapter introduction and adjacent discussion support the formulation that uniqueness should hold almost surely at every fixed p > p_c. The [source adjudication](source_scope/SOURCE_SCOPE_ADJUDICATION.md) keeps that contextual inference explicit.

The example refutes that universal formulation and, consequently, the stronger all-parameter at-most-one formulation. It does not identify any unexpressed intention of the author or contradict a published uniqueness theorem. Bounded literature checking did not authenticate an equivalent earlier example, but that is not a novelty certificate.

## Why the construction works

A geometric comparison controls distances, not local connection probabilities after a finite gadget is traversed. Replacing an edge by 100 edges changes its effective probability from p to p¹⁰⁰. At p = 0.95 that is about 0.00592. Yet a globally fixed subdivision length preserves uniform quasi-isometry.

Keep two opposite quadrants well connected, and use the subdivided edges everywhere else. Each strong quadrant can sustain an infinite cluster. The distance between the quadrants grows with distance along their boundaries, so the total probability of any connecting weak path is summable. This widening separation is important: parallel half-planes separated by a fixed-width strip would have infinitely many equally short crossing opportunities, and this proof would not apply.

The proof has five separate obligations: admissible geometry, exact iid transfer, survival below the target parameter, control of every possible bridge, and correct independence when combining the events. Each is established below and in the [complete proof](pass1_construction/CONSTRUCTION_PROOF.md).

## 1 The deterministic graph has the required geometry

In Z² let

\[
A=\{(x,y):x\ge1,\ y\ge1\},\qquad
B=\{(x,y):x\le-1,\ y\le-1\}.
\]

A lattice edge is strong if both endpoints lie in A or both lie in B. Keep every strong edge. Replace every other lattice edge by a path of exactly 100 edges, with 99 new vertices used by no other replacement path. There are no additional edges.

The graph is connected and simple. Original vertices retain degree four; inserted vertices have degree two. No subdivision length depends on location.

Map each inserted vertex to its nearer original endpoint, fixing original vertices. Call the map f. It is surjective, and every actual edge projects to either a point or one lattice edge. Every vertex is within distance 50 of its image. Therefore

\[
 d_{\mathbb Z^2}(f(u),f(v))\le d_G(u,v)
 \le100\,d_{\mathbb Z^2}(f(u),f(v))+100.
\]

These inequalities imply the source's quasi-isometry inequalities with one constant C = 100, uniformly over all points. The graph is also planar and one-ended, as explained in the [geometry audit](pass1_geometry/GEOMETRY_AND_ENDPOINT_AUDIT.md), but neither extra property is needed for the conclusion.

## 2 The coarse description preserves the iid model exactly

A weak lattice edge is declared effectively open precisely when all 100 actual edges of its replacement path are open. Its probability is q = p¹⁰⁰. A strong effective edge has probability p. Different effective edges use disjoint actual edge sets, so their states are independent.

Connectivity between original vertices is exactly preserved. An actual simple path cannot leave a replacement chain through an internal vertex, because that vertex has degree two. Thus compressing or expanding paths gives both directions of the equivalence.

Every infinite actual cluster contains infinitely many original vertices: a cluster with only finitely many originals is confined to finitely many finite incident paths. Consequently infinite components of the actual and effective models correspond bijectively. The effective inhomogeneity is a calculation within the common-parameter iid model, not a change of model.

## 3 Each strong quadrant survives already at p = 0.9

Let Q be the quadrant graph on N₀². The corner survival estimate used in the proof is

\[
\mathbb P_{9/10}^{Q}(0\leftrightarrow\infty)\ge143/245.
\]

It is proved without importing the exact square-lattice threshold. For a finite set C containing the corner, take the dual edges crossing its primal edge boundary inside Q. Interior dual degrees are even, because membership in C changes an even number of times around each unit square. Bottom and left boundary dual vertices have degree zero or one.

Along the bottom primal axis, membership starts at one and eventually becomes zero. Hence the number of bottom dual endpoints is odd. Some dual component has an odd number of them; the handshaking lemma forces it to contain a left endpoint as well. A simple path between those endpoints is a dual crosscut. If its endpoints are (i+1/2, −1/2) and (−1/2, j+1/2), its length n satisfies n ≥ i+j+2 ≥ 2.

When C is the finite open corner cluster, all edges crossed by that dual path are closed. There are at most n possible bottom starting positions and at most 4·3ⁿ⁻¹ self-avoiding paths of length n from each start. Only eligible paths receive a probability; counting additional paths only overestimates their number. For z = 3(1−t) < 1,

\[
\mathbb P_t^Q(\text{finite corner cluster})
\le\frac43\sum_{n\ge2}n z^n
=\frac43\frac{z^2(2-z)}{(1-z)^2}.
\]

At t = 9/10 this is 102/245. Both strong quadrants therefore have corner survival probability at least 143/245 at p = 19/20 by ordinary product monotonicity. Survival already at 9/10 establishes the strict gap p_c(G) < 19/20; survival only at the target p would not suffice.

## 4 All possible inter-quadrant connections are controlled

Let W mean that some finite all-weak open path connects A to B in the effective lattice. Every open A-to-B connection, even one with strong-edge excursions, implies W: stop a simple connecting path at its first B-vertex and start at its last earlier A-vertex. Every edge of the remaining segment is weak.

Its starting vertex is (1,k) or (k,1), k ≥ 1. The lattice distance from either to B is k+3. With r = 3q < 1, self-avoiding path counting yields

\[
\mathbb P(W)
\le2\sum_{k\ge1}\sum_{m\ge k+3}4\,3^{m-1}q^m
=\frac83\frac{r^4}{(1-r)^2}.
\]

This sum includes every boundary starting point, arbitrarily long detours, and all possible bypasses. The common corner is harmlessly counted twice.

At p = 19/20, Bernoulli's inequality gives (20/19)²⁰ > 2, so q = (19/20)¹⁰⁰ < 1/32. Therefore

\[
\mathbb P(W)<\frac83\frac{(3/32)^4}{(1-3/32)^2}
=\frac{27}{107648}<\frac1{1000}.
\]

No event requiring infinitely many selected edges to be closed is imposed. Instead a union bound shows that the event of no bridge has positive probability.

## 5 Independence gives two surviving isolated clusters

Let S_A and S_B be corner survival using only strong edges inside the two quadrants. They use disjoint actual edge families. W depends only on weak replacement-path edges. Thus S_A, S_B and Wᶜ are independent, including as events generated by infinitely many edge variables.

On S_A ∩ S_B ∩ Wᶜ the two infinite clusters cannot merge, because a merger would give a finite A-to-B connection and hence W. Consequently

\[
\begin{aligned}
\mathbb P_{19/20}^G(N_\infty\ge2)
&>\left(\frac{143}{245}\right)^2
  \left(1-\frac{27}{107648}\right)\\
&=\frac{2200741829}{6461571200}>\frac13.
\end{aligned}
\]

The difference between the displayed rational bound and 1/3 is exactly 140654287/19384713600. Positive probability of two or more infinite clusters is enough to negate almost-sure uniqueness. No transitive cluster-count law or uniqueness-monotonicity theorem is used.

## The dimension-one endpoint and optional extensions

For any connected bounded-degree H quasi-isometric to Z, p_c(H) = 1. A quasi-isometry to Z gives finite coordinate bands of uniformly bounded size at fixed width and a uniform bound on the coordinate span of each edge. Well-separated coordinate cuts are therefore disjoint finite edge sets of uniformly bounded cardinality. At each fixed p < 1, each cut is entirely closed with a uniformly positive probability; independence gives closed cuts infinitely often in both directions. Every cluster is trapped in a finite band. At p = 1 connectedness gives exactly one infinite cluster. The full proof appears in Section 7 of the construction and Section 6 of the geometry audit.

The geometry audit also gives supplementary higher-dimensional and additive-only realizations, with explicit but larger degree or subdivision constants. Their scope is recorded in the [results index](RESULTS_INDEX.md) and the independent acceptance audit. They are not needed to refute the universal assertion and do not change the canonical degree-four example.

## What computation contributes

The retained [validator](pass1_validation/validate_construction.py) recomputes exact rational constants and finite adversarial examples. It checks all 32,768 subsets containing the corner in a 4 by 4 quadrant window, self-avoiding paths and weak bridges through length ten, 1,001 extraction walks, all 128 configurations of a small series gadget, and a 3,193-vertex finite subdivision graph. All checks remain enabled under normal, -O and -OO Python.

These checks corroborate implementation and arithmetic. They do not prove an infinite-event theorem. The parity lemma, geometric-series argument, independence, and metric estimates supply the proof; the [independent validation](pass1_validation/INDEPENDENT_VALIDATION.md) and [acceptance audit](pass1_audit/INDEPENDENT_ACCEPTANCE.md) assess that mathematics separately. The package replays tests only in temporary copies and verifies exact file identities; see [reproducibility](REPRODUCIBILITY.md).
