# Rigorous partial results for unit-current-pair empire merging

**Review status.** Accepted as rigorous partial results by the accompanying independent AI-assisted mathematical audit. Finite-time hegemony remains OPEN. This manuscript and audit are unrefereed; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed. No novelty or bibliographic priority is claimed.

## 1. Graph formulation

Let G = (V,E) be the initial cell-adjacency graph, with one edge for each unordered pair of initial cells sharing a positive-length boundary. For the square, triangular-cell, hexagonal-cell, and generic Poisson–Voronoi starts this graph is locally finite, with bounded initial cells. A state is a partition pi of V into connected blocks. Distinct blocks A,B are adjacent precisely when

m_pi(A,B) = #{uv in E: u in A, v in B} > 0.

The unit-current-pair generator on a finite graph is

(Lf)(pi) = sum over unordered adjacent blocks {A,B} of [f(pi with A,B merged) − f(pi)].

The total rate is the number of edges of the *simple quotient graph*. Parallel original interfaces do not contribute additional rate. The infinite-plane question is not answered merely by writing this finite generator.

## 2. Marked-Poisson construction and domination

### Proposition 1 (finite graphs)

Attach an independent rate-1 Poisson point process to every e in E, with independent Uniform[0,1] marks. At a point on e = uv at time s, do nothing if u,v are already in the same block. Otherwise, let A,B be their current blocks. Merge A,B if and only if the mark is at most 1/m_pi(A,B).

This produces the unit-current-pair process. Moreover, at every time s, each empire block is contained in a connected component of the graph consisting of edges that have had at least one Poisson point by s.

### Proof

At a fixed state pi, exactly m = m_pi(A,B) original edges offer a merger of A,B. Each has proposal intensity 1 and independent acceptance probability 1/m. Consequently the total accepted intensity for that unordered pair is m(1/m) = 1. Distinct pair transitions use disjoint sets of original edges. Standard marked-Poisson infinitesimal rates therefore give L. The finite-state continuous-time chain is nonexplosive.

Every accepted merger uses an original edge with a proposal point already observed. Inductively all vertices in each resulting block are connected by observed proposal edges. This proves the refinement assertion pathwise. Since independent Poisson processes have at least one point by s independently with probability 1 − exp(−s), the larger partition is ordinary independent bond percolation at that parameter. QED.

### Proposition 2 (local construction through a finite-component horizon)

Let G be a countable locally finite graph. Fix T < infinity and suppose independent bond percolation on G at p = 1 − exp(−T) has only finite connected components almost surely. Then the preceding marked-Poisson construction is well defined on the entire interval [0,T], has the unit-current-pair transition rates, and all its blocks are finite throughout that interval.

### Proof

Expose only which edges have at least one proposal by T. By assumption every component K of this proposal graph is finite. No merger through time T can join different K's, since such a merger requires a proposal edge. Within each K, use chronological order to process the finitely many proposals on the finitely many original G-edges whose endpoints lie in K. (The boundary of K is finite too, by local finiteness, and none of those leaving edges has a proposal by T.) A current block lies in K; every original adjacency joining two current blocks in K is included when computing m, whether or not that particular edge has proposed yet. Thus rates are not changed by omitting the outside.

The componentwise constructions agree. They are consistent as T varies: enlarging a horizon may enlarge the exposed candidate component, but any merger by an earlier time still uses a proposal by that earlier time. Decisions up to that earlier time have the same current blocks and the same original-edge multiplicities. In particular the construction is adapted to past marks despite the finite-component argument's use of a horizon. The same local infinitesimal argument as Proposition 1 gives rate 1 for every current adjacent pair. Each initial vertex has only finitely many relevant events on [0,T], and every block lies in a finite K. QED.

This proposition does not assert a construction by this method for T after the proposal graph percolates. Nor does it assert that no other construction can work there.

### Corollary 3 (square-cell lower-time bound)

For initial cells z + [0,1]^2, z in Z^2, the unit-current-pair process in Proposition 2 is defined through T = log 2 and has no infinite-area empire at any time in [0, log 2], almost surely.

Indeed p(T) = 1/2, and the Harris nonpercolation theorem states that the ordinary square-lattice bond process has no infinite cluster at p = 1/2. This gives the hypothesis of Proposition 2. A finite union of unit squares has finite area. Since the construction holds simultaneously throughout [0,T], this is not only a statement at each separate deterministic time.

Primary reference for the critical nonpercolation fact: B. Bollobás and O. Riordan, A short proof of the Harris–Kesten Theorem, Bull. London Math. Soc. 38 (2006), 470–484, https://arxiv.org/abs/math/0410359 and https://doi.org/10.1112/S002460930601842X. This reference explicitly proves/recounts nonpercolation at p = 1/2; merely knowing the numerical value of p_c without its critical behavior would not be sufficient for the endpoint.

The corollary is a lower bound, not a proof of finite-time hegemony. If a global extension is fixed, no hegemony time of that extension can lie in this interval. A strict inequality for the infimum of percolating times is not asserted, since an infimum need not be attained.

### Elementary variants without exact critical constants

If the initial graph has maximum degree Delta >= 3 and (Delta − 1)(1 − exp(−T)) < 1, there are almost surely only finite proposal components. To see this, the number of self-avoiding length-n paths from a fixed vertex is at most Delta(Delta − 1)^(n−1); their total open probability tends to zero. An infinite locally finite connected component would contain arbitrarily long such paths. Countability handles all vertices.

Thus Proposition 2 applies, with strict endpoint, through any T < log((Delta − 1)/(Delta − 2)). In particular:
- square cells: Delta = 4, giving T < log(3/2), weaker than Corollary 3;
- equilateral triangular cells: dual graph is honeycomb, Delta = 3, giving T < log 2;
- regular hexagonal cells: dual graph is triangular, Delta = 6, giving T < log(5/4).

These formulas name the cells and the adjacency graphs separately to avoid interchanging triangular and hexagonal starts. Poisson–Voronoi cell degrees are unbounded, so this maximum-degree specialization is not applied to them. Proposition 2 remains a conditional graph statement for that start; no numerical Poisson–Voronoi bound is claimed.

## 3. Exact clique projection and dependent boundary survival

### Proposition 4 (initial clique projection)

Suppose k distinct initial cells form a complete subgraph of G. In any finite unit-current-pair process, restrict the current partition to these k marked cells. The restricted partition is the continuous-time Kingman coalescent with merger rate 1 for each pair of its current blocks. The same conclusion holds on any interval of a locally constructed infinite process on which these transition rules hold.

### Proof

Different restricted blocks belong to different full current regions. Each such pair of full regions remains adjacent: choose a marked initial cell in each; their original positive-length interface persists as long as the full regions are distinct. Exactly one full merger combines those two restricted blocks, and its rate is 1. A merger involving at most one full region carrying marked cells leaves the restricted partition unchanged. Thus the total transition rate for every pair of restricted blocks depends only on the restriction and equals 1. This is the finite-state lumpability criterion, or directly the generator on functions of the restriction. Outside mergers cannot cause two marked blocks to coalesce without a direct merger of their current full regions. QED.

### Corollary 5 (three cells at a hexagonal vertex)

In the regular hexagonal tessellation, the three cells meeting at a vertex are pairwise adjacent. Write X_12(t), X_13(t), X_23(t) for the indicators that their original interfaces still separate distinct regions. Then, for every time at which the process is defined as above,

P(X_12 = 1) = exp(−t),
P(X_12 = X_13 = X_23 = 1) = exp(−3t),
P(X_12 = X_13 = 1) = [exp(−t) + exp(−3t)]/2.

### Calculation

With all three marked blocks distinct, the total marked-merger rate is 3. The probability that all remain distinct is exp(−3t). The probability that only a particular pair, say {2,3}, has coalesced by t while the resulting pair-block is still separate from 1 is

integral from 0 to t of exp(−3s) exp(−(t−s)) ds
= [exp(−t) − exp(−3t)]/2.

The event X_12 = X_13 = 1 is the disjoint union of these two states. Adding their probabilities proves the formula. For a single interface, two of the three two-block states retain it; adding gives exp(−t).

The covariance of the two displayed interface indicators is

[exp(−t) + exp(−3t)]/2 − exp(−2t)
= (1/2) exp(−t) [1 − exp(−t)]^2 > 0, for t > 0.

This identity holds irrespective of the surrounding cells, because the clique projection is closed. The same local conclusion applies at a generic Poisson–Voronoi triple vertex conditional on a well-defined unit-current-pair evolution; it is not a construction or hegemony theorem for that random tessellation.

This calculation identifies the dependence rather than removing it. It supplies no Peierls product bound. A process that independently opens original adjacency edges instead has total rate m_pi(A,B) between current blocks; the equality of individual interface lifetimes does not turn the two processes into the same model.
