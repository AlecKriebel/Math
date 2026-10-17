# Independent probability audit: opposite-quadrant construction

14 October 2026. Shared mathematical PASS1, row 1785 / 10000037.

## Result and scope

The probability obligations close for the following explicit construction. Let

\[
A=\{(x,y)\in\mathbb Z^2:x\ge1,\ y\ge1\},\qquad
B=\{(x,y)\in\mathbb Z^2:x\le-1,\ y\le-1\}.
\]

Keep every nearest-neighbor lattice edge with both endpoints in A or both endpoints in B. Replace every other lattice edge by a path of exactly 100 edges, using fresh internal vertices for each path. Put independent Bernoulli bond percolation of the same parameter p on every actual graph edge.

At p=19/20, the probability of at least two infinite open clusters is strictly greater than 1/3. At the strictly smaller parameter p0=9/10, a specified vertex already has positive probability of belonging to an infinite cluster. Consequently pc(G)≤9/10<19/20. This is a supercritical counterexample if the companion geometric audit verifies the graph meets the acceptance contract. The argument does not address novelty or the interpretation of uninspected sources.

The proof only needs at least two infinite clusters with positive probability. It does not assert that the number is almost surely two, that cluster count is deterministic, or that uniqueness is monotone in p on this graph.

## 1. Effective independent lattice process

Call an original lattice edge **strong** when both endpoints lie in A or both lie in B, and **weak** otherwise. For a weak edge, declare its effective state open exactly when all 100 actual edges in its replacement path are open. Strong effective edges have parameter p; weak effective edges have parameter q=p^100. All effective states are independent because distinct replacement paths have disjoint actual edge sets, including at common endpoints.

A finite simple actual-graph path between original lattice vertices traverses any replacement path it uses completely: its internal vertices have degree two and the path cannot turn back. Thus original lattice vertices are connected in the actual open graph if and only if they are connected in the effective open lattice graph. Partial open replacement paths cannot provide additional connections.

## 2. Elementary survival in a quadrant

Let Q be the nearest-neighbor graph on N0². At bond parameter r=9/10, the corner belongs to an infinite open Q-cluster with probability at least

\[
\theta_Q(9/10)\ge\frac{143}{245}>0.
\]

### Deterministic dual-cut lemma

For every finite nearest-neighbor connected vertex set C⊂N0² containing (0,0), its edge boundary inside Q contains the primal edges crossed by a self-avoiding dual-lattice path γ with endpoints

\[
(-1/2,j+1/2),\qquad (i+1/2,-1/2),\qquad i,j\ge0,
\]

and all other vertices in [1/2,∞)². If n is the length of γ, then

\[
n\ge i+j+2\ge2.
\]

Here the dual lattice is Z²+(1/2,1/2), with each dual edge crossing its corresponding primal lattice edge.

A finite-graph parity argument proves this without any boundary-tracing convention. Let D consist of exactly the dual edges crossing primal Q-edges with one endpoint in C and one outside C. The graph D is finite because C is finite. At each interior dual vertex (a+1/2,b+1/2), a,b≥0, the four surrounding primal vertices form a unit square. Traversing its four corners cyclically, the indicator of membership in C changes an even number of times. Thus every interior dual vertex of D has degree 0, 2, or 4.

The only other dual vertices that can be incident to D are on the bottom boundary {(a+1/2,−1/2):a≥0} or left boundary {(−1/2,b+1/2):b≥0}; each has degree zero or one. Along the bottom primal ray (0,0),(1,0),(2,0),… the membership indicator starts at one and is eventually zero. Therefore it changes value an odd number of times, which is exactly the number of bottom-boundary vertices of degree one in D. The same assertion holds on the left primal ray.

Since the total number of bottom degree-one vertices is odd, at least one connected component of D has an odd number of them. The handshaking lemma says that a finite graph has an even number of odd-degree vertices. This component must therefore also have an odd number of left degree-one vertices. In particular, it contains a bottom vertex and a left vertex, and a simple path between them. Such a path cannot have any other boundary vertex as an internal vertex, since every boundary vertex has degree at most one. Its internal vertices are consequently in [1/2,∞)². The lattice distance between its endpoints is i+j+2, proving the length bound. This parity proof actually works for any finite C containing the origin, with no connectivity hypothesis needed.

If C is a finite open cluster, each primal boundary edge just described is closed: an open boundary edge would place its other endpoint in C. Thus a finite corner cluster forces a closed dual path of the stated kind. This is a deterministic implication; there is no independence assumption about the random cluster C itself.

### Counting the possible dual paths

For a path of length n, the inequality j≤n−2 gives at most n possible starting vertices on the left boundary. From a fixed starting vertex, the total number of self-avoiding dual paths of length n is at most 4·3^(n−1): at most four first steps and at most three later steps after immediate backtracking is excluded. This deliberately overcounts, allowing paths that have the wrong endpoint or leave the quadrant.

Each eligible self-avoiding dual path supplied by the cut lemma crosses n distinct actual Q-edges, so the probability that all are closed is (1−r)^n. Arbitrary dual paths are used only to bound the number of eligible paths; no probability (1−r)^n is assigned to an ineligible path leaving Q. A union bound over eligible paths therefore gives, whenever 3(1−r)<1,

\[
\begin{aligned}
\mathbb P_r^Q((0,0)\text{ has a finite cluster})
&\le\sum_{n\ge2}4n3^{n-1}(1-r)^n\\
&=\frac43\frac{t^2(2-t)}{(1-t)^2},\qquad t=3(1-r).
\end{aligned}
\]

At r=9/10, t=3/10, and the right side is exactly 102/245. Subtracting from one proves the claimed survival lower bound 143/245. By the standard same-uniforms coupling on the countable edge set, survival probability is nondecreasing in r; no uniqueness-monotonicity assertion is used.

The induced strong subgraphs on A and B are respectively a translate and a reflected translate of Q. Therefore their corners have independent internal survival events S_A and S_B, each with probability at least 143/245 at every p≥9/10.

## 3. All possible bridges, including excursions and bypasses

Let W be the event that some finite effective open lattice path goes from A to B using only weak edges. This event is measurable with respect to the weak effective edge states alone.

Every open path from A to B in the full effective graph forces W. Indeed, first take a finite simple open A-to-B path. Let its first B-vertex occur at index j, and its last A-vertex before j at index i. All internal vertices of the subpath from i to j are outside A∪B. Every edge of that subpath is weak. This extraction permits arbitrarily many earlier strong excursions and arbitrarily large detours; it does not presuppose a straight crossing or a particular route through the weak region.

Every all-weak path leaving A starts at its vertex boundary

\[
\partial A=\{(1,n):n\ge1\}\cup\{(n,1):n\ge1\}.
\]

There are at most two listed starts for each n≥1; counting (1,1) twice only enlarges the bound. The lattice distance from either listed vertex at index n to B is n+3. Thus any self-avoiding all-weak path from such a vertex to B has length m≥n+3.

There are at most 4·3^(m−1) self-avoiding lattice paths of length m from a given vertex. Each candidate that consists entirely of weak edges is open with probability q^m. Counting all self-avoiding paths rather than just the eligible ones provides an upper bound on their number; ineligible paths are not asserted to have probability q^m.

Writing a=3q<1, two union bounds and a geometric-series summation give

\[
\begin{aligned}
\mathbb P(W)
&\le2\sum_{n\ge1}\sum_{m\ge n+3}4\,3^{m-1}q^m\\
&=\frac83\sum_{n\ge1}\frac{a^{n+3}}{1-a}
=\frac83\frac{a^4}{(1-a)^2}.
\end{aligned}
\]

This sum includes every possible low-region bridge at every height and length. It includes bypasses through either of the other two quadrants, paths wandering arbitrarily far before returning, and crossings close to the origin.

## 4. Exact rational constants

At p=19/20 and L=100, q=(19/20)^100<1/32. Indeed, Bernoulli's inequality gives

\[
(20/19)^{20}=(1+1/19)^{20}\ge1+20/19>2,
\]

and raising to the fifth power proves (20/19)^100>32. Since a↦a^4/(1−a)^2 is increasing on [0,1),

\[
\mathbb P(W)<\frac83\frac{(3/32)^4}{(1-3/32)^2}
=\frac{27}{107648}<\frac1{1000}.
\]

In particular, W does not occur with positive probability. No conditioning on an infinite collection of closed edges is needed.

## 5. Combining independence correctly

The internal-A edges, internal-B edges, and all weak edges are three disjoint sets of actual iid graph edges. The sigma-fields they generate are independent. Consequently S_A, S_B, and W^c are independent, even though all three events concern infinitely many edges.

On S_A∩S_B∩W^c there is an infinite open cluster meeting A and another meeting B. They cannot coincide, since equality of connected components would supply a finite open path between them, and such a path forces W. Therefore

\[
\begin{aligned}
\mathbb P_{19/20}^G(N_\infty\ge2)
&\ge\mathbb P(S_A)\mathbb P(S_B)\mathbb P(W^c)\\
&>\left(\frac{143}{245}\right)^2\frac{107621}{107648}
>\frac13.
\end{aligned}
\]

The final inequality is exact rational arithmetic. A much weaker positive lower bound would suffice for the counterexample.

At p0=9/10, the vertex (1,1) has probability at least 143/245 of an infinite cluster using strong edges alone. Hence pc(G,(1,1))≤9/10<19/20. If one specifically chooses the root (0,0), a fixed two-macroedge path from (0,0) to (1,1) uses 200 weak actual edges and is independent of internal-A survival; the root's survival probability at p0 is therefore at least (9/10)^200·143/245>0. This also verifies the supercritical inequality directly for that root.

## 6. What the argument does and does not need

- No exact value of the square-lattice critical parameter is used.
- No transitive uniqueness theorem, 0/1/infinity cluster-count law, nontransitive uniqueness monotonicity, or rough-isometry invariance assertion is used.
- No independence is assumed between a random cluster and its own boundary. The boundary argument is a union bound over deterministic dual paths.
- The weak-edge bridge estimate does not require every weak cluster to be finite. That additional fact would follow from q<1/3 by a rooted path-counting argument, but is unnecessary here.
- Establishing pc<p at one fixed parameter and positive probability of at least two infinite clusters disproves the context-supported universal supercritical uniqueness statement. It also disproves the stronger all-parameter normalization. There is no need to claim anything about critical percolation on this graph.
- The construction in dimension two alone negates a statement quantified over all positive integer dimensions. It does not itself assert a counterexample in dimension one.

## 7. Independent reflection fallback for the survival input

The canonical constants above use the quarter-plane dual-cut parity lemma. There is also a separate, less economical route using only the familiar full-plane finite-cluster contour argument; it can be used if an auditor wants to avoid a boundary crosscut.

Given Bernoulli(r) states on Q, reflect every state to the full lattice through the map (x,y)↦(|x|,|y|). Each original quadrant edge has at most four full-lattice preimages. If the quadrant corner cluster is finite, the reflected full-lattice root cluster is finite, because the absolute-value image of every reflected open path is an open quadrant walk. A finite full-plane cluster is surrounded by a simple closed dual circuit of closed edges.

A length-n enclosing dual circuit, n≥4, has at least n/4 distinct original quadrant edges under reflection. Its probability of being closed is at most (1−r)^(n/4). The number of length-n enclosing circuits is at most 2n·3^(n−1): such a circuit crosses the positive horizontal ray; its x-range is at most n/2 and it surrounds zero, so at most n positive-ray crossing edges can be used as a marked starting edge. Choosing an orientation and then a nonbacktracking walk gives the stated deliberately loose bound. Counting the same circuit more than once is harmless.

It follows that

\[
\mathbb P_r^Q(\text{finite corner cluster})
\le\frac23\sum_{n\ge4}n\,[3(1-r)^{1/4}]^n.
\]

For r0=1295/1296, the bracket equals 1/2, and this bound is 5/12. Thus survival is at least 7/12. If one replaces the canonical parameters by p=2591/2592 and L=12960=5·2592, Bernoulli's inequality again gives p^L<1/32, so the same bridge bound applies. This supplies a complete alternate parameter choice, with a larger subdivision length and unchanged qualitative conclusion. It is an audit cross-check, not an additional pass.
