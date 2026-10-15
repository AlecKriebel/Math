# Minimum edge deletion that destroys generic planar rigidity

Problem 3000029 / AMR-029-0029. Authored mathematical partial-result report, 10 October 2026.

**Status:** partial results accepted by the accompanying independent mathematical audit. The general complexity question remains unresolved by this work. This AI-assisted manuscript is unrefereed; acceptance denotes the accompanying audit, not external human peer review, journal acceptance, or formal proof-assistant certification. No novelty or priority claim is made.

## Outcome and exact scope

The arbitrary-input polynomial-time question is **not resolved** here. No valid NP-hardness reduction is obtained. The contributions of this attempt are a precise finite-cover optimization formulation, explicit obstructions to two tempting shortcuts, and exact bounded-parameter consequences. These are not asserted to be new to the literature.

Throughout, G=(V,E) is a finite simple graph, all vertices remain present, n=|V|>=2, and G is generically rigid in the Euclidean plane. Write r for the rank in the two-dimensional generic rigidity matroid, and define

    rho(G) = min{|F| : F subset E, r(E minus F) < 2n-3}.

Thus r(E)=2n-3. The objective is the number of deleted edges. This is neither global rigidity nor vertex deletion, anchoring, matrix-entry editing, or weighted interdiction. In particular, “in the plane” does not require that the abstract graph be planar.

For n=2 the input is K2 and rho=1. A single vertex, if supplied outside the stated domain, has no feasible rigidity-destroying edge deletion; its value is not zero.

## 1. Sources and credit

The original EGRES problem explicitly asks for minimum edge deletion and identifies the minimum-cocircuit formulation:

- [Destroying rigidity](https://oldlemon.cs.elte.hu/egres/open/Destroying_rigidity)
- [Discussion](https://oldlemon.cs.elte.hu/egres/open/Talk:Destroying_rigidity)

Bérczi, Bernáth, Király and Pap, [Blocking optimal structures](https://egres.elte.hu/tr/egres-17-07.pdf), 2017, printed page 3 / PDF page 4, separately describe this rigidity-matroid complexity question as open. Their polynomial unweighted results for unions of graphic/hypergraphic matroids do not establish a result for all count matroids. The discussion's transversal minimum-circuit hardness does not become rigidity minimum-cocircuit hardness by changing terminology.

The rigid-component description behind Section 2 is classical. Servatius, [Planar Rigidity](https://users.wpi.edu/~bservat/phddissertation.pdf), 1987 dissertation, Chapter 4, Theorem 2, printed pages 32–33 / actual PDF pages 52–53 in the 2005 typeset conversion, gives a cocircuit characterization by rigid vertex sets. We give a direct Laman-matroid proof of the simpler budgeted-cover formulation needed here, without claiming the characterization as new. A printed-condition caveat: Theorem 2(2)(b) uses a strict “>” together with “+2” for even subfamilies; for two triangles sharing one vertex, the two rigid blocks have union size five and the displayed right-hand side is also five. The proof below does not use that printed condition. No inference about the source author's intent or replacement theorem is asserted.

The bound rho(G)<=delta(G)-1 is already Lemma 3 of Yu and Anderson, [Agent and Link Redundancy for Autonomous Formations](https://skoge.folk.ntnu.no/prost/proceedings/ifac2008/data/papers/0554.pdf), IFAC 2008, printed page 6586 / PDF page 3. Their convention excludes the two-vertex case; we handle it separately. The algorithmic rank oracle is the standard deterministic (2,3)-pebble game of Lee and Streinu, [Pebble Game Algorithms and Sparse Graphs](https://arxiv.org/abs/math/0702129), published in Discrete Mathematics 308 (2008), 1425–1437, [DOI](https://doi.org/10.1016/j.disc.2007.07.104).

Jordán's [Minimum size highly redundantly rigid graphs in the plane](https://egres.elte.hu/tr/egres-20-21.pdf), published in 2021, concerns extremal sizes and particular graph families. Its edge-redundancy terminology matches the parameter here; its extremal theorems are not an arbitrary-input optimization algorithm. Cruickshank, Jackson, Jordán and Tanigawa's [2025 rigidity survey](https://arxiv.org/abs/2508.11636) likewise did not supply a checked resolution in the inspected material. These bounded searches do not certify worldwide current openness or novelty.

## 2. An exact cover optimization, and its missing algorithm

For a family X={X_1,...,X_h} of vertex subsets with |X_i|>=2, set

    c(X) = sum_i (2|X_i|-3),
    U(X) = union_i E(K_{X_i}),
    d_G(X) = |E minus U(X)|.

The empty family is allowed. Call the family one-thin if |X_i intersect X_j|<=1 whenever i!=j.

**Proposition 1.** For every rigid G with n>=2,

    rho(G) = min {d_G(X) : c(X)<=2n-4}.                         (1)

There is an optimal family that is one-thin, has c(X)=2n-4, and covers all retained edges. For n>=3 its sets cover V. Every minimum deletion F leaves rank exactly 2n-4 and is a cocircuit.

**Proof.** For any displayed family, the graph with retained edges E intersect U(X) has rank at most sum_i r(K_{X_i})=c(X)<=2n-4, by subadditivity. Consequently every feasible family gives a rigidity-destroying deletion. This proves rho(G) is at most the right-hand side.

Conversely, choose a minimum F and put H=G-F. Each deleted edge must restore full rank when added back, since otherwise the smaller deletion F minus {e} would suffice. As adding one edge increases rank by at most one, r(H)=2n-4. The same observation says that every edge of E outside H is outside its matroid closure, so E(H) is a hyperplane of the restricted matroid.

Choose a Laman-independent basis B of H. A vertex set X with |X|>=2 is tight in B when its induced edge count is 2|X|-3. Distinct inclusion-maximal tight sets intersect in at most one vertex: if two tight sets intersect in at least two vertices, the Laman inequalities and the edge-count identity imply their union is tight. Every edge of B belongs to a maximal tight set, starting from its two endpoints. Hence these maximal tight sets partition the edges of B and their costs sum to |B|=2n-4.

They also cover every edge e of H. For e outside B, the circuit in B+e has exactly 2|W|-2 edges on its vertex set W; deleting e leaves a tight set of B containing both endpoints of e. Enlarge W to a maximal tight set. Thus the induced-clique union covers H. If it covered an edge of F, that edge would be in the closure of the tight basis set and hence of H, a contradiction. Its retained G-edges are exactly H. This proves equality in (1) and the thin optimality assertion.

When n>=3, H cannot have an isolated vertex: otherwise its rank is at most the rank on n-1 vertices, namely 2n-5, including the n=3 case where the remaining pair has rank at most one. This contradicts r(H)=2n-4. Thus the sets cover V. For n=2 the empty family supplies the required optimum. QED.

These maximal tight sets are exactly the maximal rigid components of H. To see the nontrivial direction, let H[Y] be rigid and choose a Laman basis D on Y. Every edge of D is covered by some maximal tight set X_i. Let I be the sets used by these edges and U their union. The edge set B[U] spans each K_{X_i}, and therefore spans D. Starting with the rigid graph D, attach each K_{X_i} along its covered edge of D; rigidity gluing shows that U is rigid in the closure of B[U]. Since B[U] is Laman-independent, it has exactly 2|U|-3 edges. Thus U is tight in B, and maximality forces all its X_i to be the same set. Hence Y is contained in one maximal tight set, as claimed.

**Where the algorithmic problem remains.** Formula (1) has exponentially many possible vertex subsets and families. A polynomial rigidity-rank oracle evaluates a proposed edge deletion; it does not optimize this constrained coverage objective. Neither (1) nor an instruction to enumerate all hyperplanes is a polynomial algorithm. Sections 4 and 5 show why a fixed basis or a bounded number of components cannot simply replace the full search.

## 3. Exact bounded-regime consequences

Let delta(G) be the ordinary minimum vertex degree, m=|E|, and q_0=m-(2n-3) the matroid nullity.

**Proposition 2.** For n>=3,

    1 <= rho(G) <= min{delta(G)-1, q_0+1}.                     (2)

The first upper bound is the known degree bound cited above: leave exactly one incident edge at a minimum-degree vertex. Its remaining motion relative to the other vertices prevents rigidity. For the second, retain a basis with one edge removed and delete everything else. The retained rank is 2n-4 and the deletion size is q_0+1.

Therefore enumerate edge subsets in increasing cardinality up to b=min{delta(G)-1,q_0+1}, and use the deterministic pebble-game rank oracle to return the first failing subset. This takes

    O((sum_{j=1}^b binomial(m,j)) P(n,m))

for a polynomial rank-oracle bound P. It is exact and polynomial on every class with a fixed upper bound on minimum degree, or a fixed upper bound on nullity. The parameterized bound is of XP type; it is not an FPT result or a uniform polynomial-time algorithm for arbitrary input.

One immediate special case is topologically planar simple rigid graphs: Euler's edge bound gives delta<=5, so testing deletions of at most four edges is polynomial. This does not answer the original question, whose graphs need not admit planar embeddings. The same bounded-minimum-degree observation applies to graph classes of bounded average degree.

**Lemma 3.** For s>=3, rho(K_s)=s-2.

The degree bound gives the upper bound. For the lower bound we show K_s-D is rigid whenever |D|<=s-3. Induct on s, with K3 as base. If D is empty there is nothing to prove. Otherwise choose a vertex v incident to d>=1 deleted edges. The other s-1 vertices have at most s-3-d<=s-4 missing edges, so their graph is rigid by induction. The remaining degree of v is s-1-d>=2. Adding v with two incident edges preserves planar rigidity. This proves the lower bound. The case K2 has rho=1 separately.

## 4. A fixed-basis cocircuit shortcut fails

**Proposition 4.** Let G=K6 and choose the spanning Laman basis B=K_{3,3}. Every fundamental cocircuit relative to B has size seven, but rho(G)=4.

For any nonbasis edge e, the graph B+e has ten edges on six vertices and is a Laman circuit: every proper vertex set satisfies the Laman bound, while the full set exceeds its rank nine by one. (The only potentially maximal proper case has a 3+2 bipartition and at most seven edges, exactly its Laman bound.) Thus its fundamental circuit contains every edge of B.

For any b in B, the fundamental cocircuit is consequently b together with all six edges of E(K6) minus B. Its size is seven. Lemma 3 gives rho(K6)=4. Hence finding the smallest fundamental cocircuit of one arbitrarily selected basis is incorrect. This is an obstruction to that specific shortcut, not to algorithms that adaptively choose or optimize over bases.

## 5. Unique minimum cuts with arbitrarily many rigid components

The next family strengthens the warning that a rigidity cut need not be an ordinary graph cut. It also prevents assuming that an optimum can be represented by only a bounded number of rigid pieces, even when rho is fixed.

Fix integers t>=1, s>=t+3, q>=2. Begin with the skeleton S=K_{2,q}, whose two hubs are a,b and whose other vertices are z_1,...,z_q. For each skeleton edge e=uv introduce s-2 new vertices used by no other edge, and replace e by the complete graph on

    C_e = {u,v} union its s-2 private vertices.

Keep uv itself. Let H be the union of these 2q cliques. Choose any t distinct pairs of vertices not lying in a common C_e, and add them as a set T of brace edges. There are enough such pairs; for a concrete choice join one private vertex of C_{az_1} to t different private vertices of C_{bz_1}. Call the resulting graph G=H+T.

Its numbers of vertices and edges are

    n = (2s-3)q+2,
    |E(H)| = 2q binomial(s,2),
    |E(G)| = 2q binomial(s,2)+t.

**Theorem 5.** In this construction:

1. H has rank 2n-4, and its maximal rigid components are exactly the 2q cliques C_e.
2. Every missing edge of H raises its rank to 2n-3.
3. G is rigid, rho(G)=t, and T is its unique minimum rigidity-destroying deletion.
4. H is 2-vertex-connected. For the concrete brace choice above, delta(G)=lambda(G)=s-1, where lambda is ordinary edge connectivity.

**Proof of (1).** The skeleton is Laman-independent. To see this directly, a vertex subset with at most one hub induces a star or an empty graph, while a subset with both hubs and k other vertices induces at most 2k edges on k+2 vertices. Both satisfy the Laman inequalities.

For every edge e=uv choose inside C_e the basis consisting of uv and the two edges uw,vw for each private vertex w. The union of these bases is obtained from the independent skeleton by degree-two vertex additions, so it remains independent. Its size is

    2q(2s-3)=2n-4.

Every clique C_e has rank 2s-3, and rank subadditivity gives the matching upper bound on r(H). Equality of the total rank with the sum of the clique ranks means their edge sets are direct summands of the restricted matroid. Consequently, for any vertex set X,

    r(H[X]) = sum_e f(|X intersect C_e|),

where f(0)=f(1)=0 and f(j)=2j-3 for j>=2.

We show that any rigid vertex set of size at least two is contained in one clique. Let A be the set of skeleton edges e for which |X intersect C_e|>=2, and put W=union_{e in A}(X intersect C_e). If |A|=0, H[X] has rank zero; if |A|=1, the rank is sufficient for rigidity only when X is contained in that clique.

Suppose h=|A|>=2. Counting repeated skeleton vertices gives

    sum_{e in A}|X intersect C_e|
      = |W| + sum_{v in X intersect V(S)} max{d_A(v)-1,0}
      <= |W| + 2h - |V(A)|.

Every set A of at least two skeleton edges satisfies

    h <= 2|V(A)|-4.                                         (3)

Indeed, with one incident hub it is a star and h<=2(h+1)-4 for h>=2; with two incident hubs it has at most twice as many edges as incident z-vertices. Therefore

    r(H[X]) <= 2|W| + h - 2|V(A)|
             <= 2|W|-4 <= 2|X|-4.

Such X is not rigid. This proves that the full cliques, and only they, are maximal rigid components.

**Proof of (2).** If a missing edge xy did not raise rank, a circuit in a basis of H plus xy would contain xy. Removing xy from that circuit gives a Laman basis on a vertex set containing x and y. H would therefore have a rigid vertex set containing both. Part (1) says they would belong to one clique, contrary to xy being missing.

**Proof of (3).** Part (2) says that any one brace makes H rigid. Deleting T leaves H, so rho(G)<=t. Suppose D is any other set of at most t deleted edges. At least one brace remains. Since t<=s-3, Lemma 3 says that every graph K_{C_e}-D is still rigid on C_e. Its closure contains all edges of the original clique. Hence the closure of G-D contains H and a remaining brace. By (2), it has full rank. Thus G-D is rigid. This proves both equality and uniqueness of T.

**Proof of (4).** The skeleton K_{2,q} is 2-vertex-connected for q>=2. If a private vertex is removed, each affected clique remains connected and all skeleton edges survive. If a skeleton vertex is removed, the remaining skeleton is connected, and each remaining piece of an affected clique still attaches to its other endpoint. Thus H remains connected after every single vertex deletion.

For every nontrivial vertex partition of H, some clique must meet both sides, since H is connected. Splitting a K_s cuts at least s-1 edges, so lambda(H)>=s-1 and lambda(G)>=s-1. There are private vertices untouched by the concrete braces, for example in cliques belonging to z_2. Such a vertex has degree s-1 in G. Consequently delta(G)=lambda(G)=s-1. QED.

**Consequences.** Keep t fixed and let s grow: both the degree bound and ordinary edge connectivity can exceed the true rigidity-cut value by an arbitrarily large factor. Independently, let q grow: the unique optimum exposes 2q rigid components, while the residual remains 2-vertex-connected. Therefore there is no universal bound, or bound depending only on rho, on the number of maximal rigid components exposed by an optimum.

This also rules out replacing (1) by families of at most f(rho) sets for any fixed function f. A budget-feasible family attaining this unique optimum must cover every edge of H. If one of its sets contained a missing pair of H, its clique union would contain H and that pair, giving rank 2n-3 despite the budget 2n-4. Thus every set is contained in a single C_e, requiring at least 2q sets to cover all its clique edges.

These graphs are easy instances once their construction is revealed. They are counterexamples to structural shortcuts, not a hardness reduction.

## 6. Recorded verification and exact unresolved boundary

The initial proof-review record reports a supporting finite verification using two independently written integer algorithms: greedy Laman-sparsity testing over vertex subsets, and the (2,3)-pebble game. It exhausts all 33,866 labeled simple graphs on 2–6 vertices, including 8,128 rigid graphs. For every rigid graph it computes an optimum deletion by full subset dynamic programming, checks that its complement has rank 2n-4, checks both bounds in (2), and verifies the thin component-cover certificate. The two rank implementations also agree on 500 seeded graphs of orders 7–11.

The K6/K3,3 fundamental cocircuits are checked individually. Six instances of Theorem 5, up to 262 vertices and 1,122 edges, are checked for rank, single-brace restoration, selected/all missing-pair restoration, minimum degree, ordinary min-cut, and 2-vertex-connectivity of the residual. All deletion sets of size at most t are checked in the (q,s,t)=(2,4,1) and (2,5,2) instances. Larger cases use seeded sampled deletion sets and the distinguished cut. The infinite-family proof, not these samples, establishes generality. Computation is not a proof of the arbitrary-input complexity question. Programs, raw generated certificates and detailed outputs are not distributed with this proof-only edition. All analytic arguments are complete without them. Aggregate independent-audit results appear in [ACCEPTANCE.json](ACCEPTANCE.json); edition preparation did not rerun mathematical tests or perform new scholarly-source retrieval, source-file rehash, source inspection, or literature search.

The precise remaining task is to optimize the budgeted clique coverage in (1), or equivalently to find a maximum-cardinality hyperplane of the restricted planar rigidity matroid, in uniform deterministic polynomial time; alternatively, give a correct decision reduction proving an appropriate hardness statement under its standard complexity assumption. Neither has been supplied. Rank testing, fixed-budget enumeration, one-basis fundamental cuts, ordinary min-cuts, and bounded-component enumeration do not close this gap.
