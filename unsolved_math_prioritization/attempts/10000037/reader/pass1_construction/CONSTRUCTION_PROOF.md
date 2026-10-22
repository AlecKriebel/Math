# A bounded-subdivision counterexample to supercritical bond uniqueness

Authored mathematical construction, 14 October 2026. Submitted for independent proof audit. No novelty claim.

## Target and statement

The target is the universal assertion that every infinite, connected, simple, bounded-degree graph quasi-isometric to a Euclidean lattice has an almost surely unique infinite Bernoulli-bond cluster at every fixed parameter strictly above its critical probability. The following construction is in dimension two, which suffices to refute that universal assertion and therefore also its stronger all-parameter normalization. It makes no assertion about nonuniqueness at the critical probability.

**Theorem.** There is a deterministic, simple, connected graph G of maximum degree four, quasi-isometric to the nearest-neighbor square lattice with a uniform quasi-isometry constant 100, for which

- p_c(G) <= 9/10;
- at p = 19/20, independent bond percolation on G has at least two infinite open components with probability strictly greater than 1/3.

Every actual edge of G has the same retention probability p. The different probabilities used below occur only in an exactly equivalent coarse description of this iid model.

## 1. Deterministic graph

Let L be the nearest-neighbor graph on Z^2. Put

A = {(x,y) in Z^2 : x >= 1 and y >= 1},
B = {(x,y) in Z^2 : x <= -1 and y <= -1}.

Call a lattice edge strong if both its endpoints lie in A, or both lie in B. Call every other lattice edge weak.

Retain every strong edge as an edge of G. Replace each weak edge e={u,v} by a path of exactly 100 edges from u to v, with 99 new internal vertices. Internal vertices belonging to distinct replacement paths are distinct. There are no additional edges. The vertex sets A and B refer to the original lattice vertices throughout.

Every original lattice vertex has degree four and every new vertex has degree two. The graph is infinite, countable, simple, connected and deterministic. The replacement length is fixed globally; it does not grow with location.

## 2. Uniform metric control

For original vertices u,v,

|u-v|_1 <= d_G(u,v) <= 100 |u-v|_1.

The upper bound lifts a shortest lattice path. For the lower bound, any G-path between original vertices compresses to a lattice walk, whose length is no greater than the G-path length.

Define f:G -> Z^2 to fix each original vertex and map each internal vertex to the nearer endpoint of its replacement path, with ties resolved consistently. Each actual G-edge either has identical endpoint images or images joined by one lattice edge. Consequently

|f(x)-f(y)|_1 <= d_G(x,y).

Every x is at distance at most 50 from f(x), and therefore

d_G(x,y) <= 50 + 100 |f(x)-f(y)|_1 + 50.

The map is surjective. In particular, it obeys the source's single-constant quasi-isometry inequalities with C=100:

100^(-1) |f(x)-f(y)|_1 - 100 <= d_G(x,y)
<= 100 |f(x)-f(y)|_1 + 100.

## 3. Exact transfer from the iid edge model

Perform Bernoulli bond percolation at one parameter t on every actual edge of G, independently. A coarse strong edge is open exactly when that actual edge is open. A coarse weak edge is open exactly when all 100 actual edges of its replacement path are open.

Distinct coarse edges use disjoint actual edge sets. Thus coarse edge states are independent, with strong-edge probability t and weak-edge probability t^100. This inhomogeneous coarse process is a consequence of the iid process on G, not a replacement of the requested model.

Two original vertices are connected by actual open edges if and only if they are connected in the coarse process. The forward implication follows by shortening an actual open path and noting that a path cannot leave a replacement chain through an internal vertex, whose degree is two. The reverse implication lifts every open coarse edge.

Every actual infinite component contains infinitely many original vertices: any component containing only finitely many original vertices lies in the union of those vertices and their finitely many incident replacement paths, or contains no original vertex and lies inside a single finite path. Hence actual and coarse infinite components correspond bijectively.

## 4. Survival in the two strong quadrants

Write Q for the nearest-neighbor graph on N_0^2. We prove

P_{9/10}^Q((0,0) belongs to an infinite cluster) >= 143/245.

### A deterministic dual-cut lemma, proved by parity

Let C be any finite subset of N_0^2 containing (0,0). Take every Q-edge with exactly one endpoint in C and place its crossing dual edge in a finite graph D. The dual vertices are the interior face centers (i+1/2,j+1/2), i,j>=0, together with boundary endpoints (i+1/2,-1/2) and (-1/2,j+1/2), i,j>=0.

At an interior dual vertex, the number of incident D-edges is the number of transitions between membership and nonmembership in C around the four corners of a lattice square. This number is even: 0, 2 or 4. A bottom or left boundary dual vertex has degree 0 or 1, since only one dual edge crossing a Q-edge can meet it.

Along the primal bottom axis, the membership indicators 1_C(i,0), i=0,1,2,..., start at 1 and are eventually 0. Their number of changes is therefore odd. Consequently D has an odd number of degree-one vertices on its bottom boundary. At least one connected component of D has an odd number of bottom degree-one vertices. In that component the total number of odd-degree vertices is even by the handshaking lemma. Since its interior degrees are even and its only other possible odd-degree vertices lie on the left boundary, it also has an odd, hence positive, number of left degree-one vertices.

Choose a simple path in that component from a bottom degree-one vertex to a left degree-one vertex. Its endpoints have the form

(i+1/2,-1/2) and (-1/2,j+1/2), with i,j>=0.

All internal vertices lie in the interior dual quadrant: a degree-one boundary vertex cannot be internal to a simple path. Every edge of this path crosses an edge of the Q-boundary of C. If the path has length n, the distance between its endpoints gives

n >= i+j+2 >= 2.

This proof does not require a simple outer boundary, planarity assertions about boundary tours, or even connectedness of C.

### Counting closed dual paths

If the open Q-cluster C of the corner is finite, all Q-edges with exactly one endpoint in C are closed. The preceding lemma therefore gives a self-avoiding closed dual path of length n>=2 between the two boundary axes.

For length n there are at most n possible starting positions on the bottom boundary, since i<=n-2. From a fixed start there are at most 4*3^(n-1) self-avoiding paths of length n. Only candidates with the stated boundary endpoints and interior vertices are eligible. Every eligible path crosses n distinct Q-edges, whose independent probability of all being closed is (1-t)^n. Counting all self-avoiding paths merely increases the number of eligible candidates; it does not assign probabilities to nonexistent Q-edges.

Put z=3(1-t). For z<1 a union bound gives

P_t^Q(the corner cluster is finite)
<= sum_{n>=2} 4n*3^(n-1)*(1-t)^n
= (4/3) [z/(1-z)^2 - z]
= (4/3) z^2(2-z)/(1-z)^2.

At t=9/10, z=3/10, this bound is exactly 102/245. Thus the infinite-cluster probability is at least 143/245.

The restriction of G to each strong quadrant is exactly Q up to translation or reflection. Consequently p_c(G,(1,1)) <= 9/10, and connectedness gives the same critical value at every root.

For completeness, root independence requires no transitivity: if percolation from a vertex v has positive probability, force open a finite path from any other root u to v. Positive association, or conditioning on the finitely many path edges, gives positive probability of percolation from u. The reverse argument exchanges u and v.

At p=19/20 let S_A and S_B be the events that the corner (1,1), respectively (-1,-1), belongs to an infinite open cluster using only strong edges in its own quadrant. These events each have probability at least 143/245 by ordinary product monotonicity from t=9/10. They are independent because they depend on disjoint sets of actual edges.

## 5. A global bound on every possible inter-quadrant bridge

Set p=19/20, q=p^100, and r=3q. Let W be the event that a finite self-avoiding lattice path from A to B consists entirely of open weak coarse edges.

Any coarse open path from A to B implies W. Indeed, shorten the path to a simple path, stop at its first visit to B, and begin at its last earlier visit to A. All internal vertices of the retained subpath lie outside A union B; hence none of its edges is internal to either quadrant, so every edge is weak. This argument includes arbitrary earlier strong-edge excursions and all possible spatial bypasses.

The start a of such a weak path must lie in the inner vertex boundary of A:

partial A = {(1,n): n>=1} union {(n,1): n>=1}.

For a=(1,n) or a=(n,1), its lattice distance to B is n+3. There are at most 4*3^(m-1) self-avoiding lattice paths of length m>=1 from a. A specified all-weak path of length m is coarse-open with probability q^m. Therefore, when r<1,

P(W)
<= sum_{a in partial A} sum_{m>=dist(a,B)} 4*3^(m-1) q^m
<= [8/(3(1-r))] sum_{n>=1} r^(n+3)
= (8/3) r^4/(1-r)^2.

Double-counting the corner in this upper bound is harmless. Paths that fail to be all-weak or fail to reach B merely enlarge the counting upper bound. The series explicitly sums crossings at every distance from the origin.

Bernoulli's inequality gives

(20/19)^20 >= 1+20/19 > 2,

so q=(19/20)^100 < 1/32 and r<3/32. Thus

P(W) < (8/3)(3/32)^4/(1-3/32)^2
= 27/107648 < 1/1000.

In particular, P(W^c)>999/1000.

## 6. Simultaneous survival and isolation

The event W depends only on actual edges in weak replacement paths. The event S_A depends only on actual strong edges internal to A, and S_B only on actual strong edges internal to B. These three edge families are pairwise disjoint. Thus S_A, S_B and W^c are independent, including their infinite-event sigma algebras.

On S_A intersection S_B intersection W^c, the two strong infinite clusters cannot be connected in the full open graph: such a connection would compress to a coarse A-to-B open path and hence imply W. Therefore

P_p^G(N_infinity >= 2)
>= P_p(S_A) P_p(S_B) P_p(W^c)
> (143/245)^2 * (107621/107648)
= 2200741829/6461571200
> 1/3.

For the last exact inequality, subtracting 1/3 gives

140654287/19384713600 > 0.

Since p_c(G)<=9/10<19/20=p, this is supercritical nonuniqueness, not merely a critical example.

## 7. The dimension-one endpoint

The example is in dimension two. For completeness, the one-dimensional case has a different elementary answer: every connected bounded-degree graph H quasi-isometric to Z has p_c(H)=1, no infinite cluster almost surely for p<1, and exactly one infinite cluster at p=1. Thus its strictly supercritical range p_c(H)<p<=1 is empty.

Here is a proof using the source's metric convention. Choose f:V(H)->Z and C>=1 with

C^(-1)|f(x)-f(y)|-C <= d_H(x,y) <= C|f(x)-f(y)|+C.

For adjacent vertices, |f(x)-f(y)|<=D:=ceil(C(C+1)). Every finite coordinate band f^(-1)([a,b]) has diameter at most C(b-a)+C, hence is finite. Bounded degree also gives a uniform finite size bound B for all bands of coordinate width 2D.

For an integer level t, let E_t be the set of edges whose endpoint f-values lie on opposite sides of the partition (-infinity,t] union [t+1,infinity). Its endpoints all lie in f^(-1)([t-D,t+D]), so |E_t|<=M:=Delta*B uniformly in t, where Delta is the degree bound. The edge sets E_{k(D+1)}, k in Z, are pairwise disjoint: an edge has f-span at most D and cannot cross two such levels.

At any p<1, the events that all edges in these successive cuts are closed are independent and have probability at least (1-p)^M>0. Almost surely infinitely many such cuts are closed in each coordinate direction, by the elementary independent-product bound (1-(1-p)^M)^n -> 0. For any vertex, closed cuts on both sides confine its open cluster to a finite coordinate band. On this same probability-one event every cluster is finite. At p=1 connectedness supplies exactly one infinite cluster. No transitivity is involved.

## 8. Scope checks

- No transitivity, quasi-transitivity, stationarity or random environment is used or assumed.
- Every actual edge is independent with one common probability p=19/20.
- The graph has maximum degree four and is simple; no parallel edges appear.
- All path substitutions have one fixed length 100; uniform metric constants hold globally.
- Positive probability of at least two infinite components is the required negation of almost-sure uniqueness. No transitive 0/1/infinity theorem or uniqueness-monotonicity assertion is used.
- A dimension-two counterexample refutes a statement quantified over all positive dimensions. It does not claim dimension-one nonuniqueness.
- This manuscript is an authored construction, not an assertion of historical novelty. The exact interpretation of the source problem is a separate source-audit question.

## 9. Provenance and mathematical dependencies

The question's context is Itai Benjamini, *Coarse Geometry and Randomness*, author manuscript dated 30 October 2013, Open Problem 9.6, printed/PDF page 64, [preserved author-hosted manuscript](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf). This note addresses the general-graph, common-parameter Bernoulli-bond, quasi-isometry interpretation stated above. It does not claim that the source sentence expressly spells out every parameter quantifier.

The construction and proof here are self-contained, using graph-distance estimates, independent bond variables, a finite-graph parity argument, elementary path counting, geometric series, and exact rational arithmetic. No asserted rough-isometry invariance theorem or externally quoted quadrant threshold is a dependency. No third-party source text, dataset contents, private source material, or coordination material is reproduced. Historical priority and novelty remain separate questions.
