# Rainbow quadrilateral colorings and their remaining density gap

Author research note for problem 2315, EP-810. Status: scoped partial results; the original problem remains unresolved by this attempt. The note is AI-authored and unrefereed. It makes no historical novelty or priority claim.

## 1 Problem and conventions

All graphs are finite, simple, and undirected. A coloring is a function on the edges; a palette of q colors means at most q colors. Every copy of C4 means every four-edge cycle as a subgraph, whether or not it has chords. Call a coloring R if all these cycles have four different colors. Call it B if it is both R and proper.

The target asks for a constant epsilon > 0 and an integer n0 such that for every n >= n0 there is an R-colored n-vertex graph with at least epsilon n^2 edges and at most n colors. Properness is not an assumption of the original question. Burr, Erdos, Graham, and Sos discuss the corresponding extremal function on printed page 273 of [1].

The following five approaches give reductions, restricted obstructions, and a weak upper bound. None gives the required positive-density family or proves its nonexistence.

## 2 Approach one: properness after a negligible deletion

**Theorem 1.** For every eta > 0 there exists n0 such that every R-colored graph G on n >= n0 vertices has a spanning subgraph G' whose inherited coloring is proper and for which |E(G) minus E(G')| <= eta n^2. No new colors are introduced. The threshold is uniform over G and over its palette size.

**Proof.** A monochromatic adjacent pair uv, vw has distinct endpoints u,w. Their common-neighbor set in G is exactly {v}: any second common neighbor z would give the non-rainbow cycle u-v-w-z-u.

Make three disjoint copies A,B,C of V(G). Put an edge a_u b_v whenever uv is an edge of G, and an edge b_v c_w whenever vw is an edge of G. For each ordered pair (u,w) with u != w that occurs as the endpoints of a monochromatic adjacent pair, put a_u c_w in the auxiliary graph T. This third edge has exactly one common neighbor in B, namely b_v, by the preceding observation. Consequently T has at most n(n-1) triangles. These are all its triangles because T is tripartite.

Use the triangle removal lemma [3] with deletion parameter eta/9 on the 3n-vertex graph T. Its triangle density is at most n(n-1)/(3n)^3, which tends to zero uniformly. For sufficiently large n there is a set D of at most eta n^2 auxiliary edges whose removal kills every triangle.

Map each member of D to an edge of G as follows. For a_u b_v use uv; for b_v c_w use vw. For a_u c_w use uv, where v is the unique common neighbor of u,w in the original G. Delete the union F of all these mapped edges from G. Then |F| <= |D|.

If a monochromatic adjacent pair uv,vw survived in G-F, its associated triangle a_u b_v c_w existed in T. One of that triangle's edges belongs to D. In all three cases the selected mapped edge is one of uv,vw, contradicting survival. Thus G-F is proper. Deleting edges cannot create a new cycle, so it is still R and hence B. This proves the theorem. Notice that all common-neighbor statements refer to the original G; newly reduced codegrees do not invalidate the argument. QED.

The removal lemma is a credited external theorem. The construction and deletion argument above are given in full; they are not an effective small-n algorithm or a proof that dense B-colored graphs cannot exist.

**Corollary 2.** Let E_R(n) be the maximum number of edges in an R-colored n-vertex graph with at most n colors, and E_B(n) the analogous proper maximum. Then

0 <= E_R(n) - E_B(n) = o(n^2).

Indeed B implies R, and Theorem 1 applies to an extremizer for E_R(n). Thus the target question is equivalent to liminf E_B(n)/n^2 > 0, and to liminf E_R(n)/n^2 > 0. The stronger assertion E_R(n)=o(n^2) would answer the question negatively, but its necessity is not asserted: the exact negation of the target is liminf E_R(n)/n^2=0, not automatically limsup=0.

**Corollary 3.** The target has an affirmative answer if and only if there is beta > 0 such that, for every sufficiently large integer s, there is a bipartite B-colored graph with two vertex classes of size s, at least beta s^2 edges, and at most s colors.

For the forward direction, start with the graph on s vertices and epsilon s^2 edges. Apply Theorem 1 with eta=epsilon/2. A random bipartition retains at least half the remaining edges for some choice, hence at least epsilon s^2/4 edges. Add isolated vertices so each class has size s. The inherited palette still has at most s colors. For the reverse direction, given a sufficiently large N use s=floor(N/2), and pad the 2s-vertex graph to N vertices. For N>=3, s>=N/3, so there are at least beta N^2/9 edges and at most s<=N colors. Both directions preserve the requirement of every sufficiently large size.

This reaches the B-coloring density question considered in [2], without assuming properness at the outset. It does not answer that question.

## 3 Approach two: the exact hypergraph obstruction

A linear 3-uniform hypergraph is one in which distinct hyperedges share at most one vertex. Suppose H is linear and tripartite with parts X,Y,Z. Project each hyperedge {x,y,z} to the edge xy colored z. This is a simple properly colored bipartite graph: duplicate xy edges, or equal colors on adjacent edges, would contradict linearity.

If H has no four edges on at most seven vertices, this projected coloring is B. Otherwise a non-rainbow four-cycle would yield four distinct hyperedges using four vertices of X union Y and at most three of Z, contradicting the hypothesis. This is the standard direction behind the (7,4) connection in [1,2].

**The converse for B-colorings is false.** Take the five-vertex path with edges, in order,

x1-y1, y1-x2, x2-y2, y2-x3,

colored a,b,a,b. Its coloring is proper and it has no C4, so it is B. Yet its associated four triples

{x1,y1,a}, {x2,y1,b}, {x2,y2,a}, {x3,y2,b}

form a linear tripartite hypergraph on precisely seven vertices. Padding the smaller graph part and the palette with unused elements does not change this obstruction. Thus the general (7,4) assertion cannot be applied merely because a graph is B-colored. In [2] the additional alternating-four-edge-path exclusion enters the C-coloring variant; we do not silently add that requirement here.

The remaining gap is a theorem controlling dense B-colorings despite these allowed alternating paths. No such theorem is proved in this note.

## 4 Approach three: affine cyclic labels cannot give positive density

**Theorem 4.** For each integer m>=2 let G_m be a bipartite graph whose classes are two copies of Z/mZ. Suppose its edge colors have the form

c(x,y) = f_m(a_m x + b_m y + z_m),

where a_m,b_m are units modulo m, z_m is any residue, and f_m is any function to any palette. If all C4s in G_m are rainbow, then |E(G_m)|=o(m^2) as m tends to infinity. The conclusion is uniform in all the displayed choices.

**Proof.** Since a_m and b_m are units, changing coordinates to u=a_m x and v=b_m y is a pair of bijections. The edge set becomes S_m contained in (Z/mZ)^2, with colors f_m(u+v+z_m). Represent both cyclic coordinates by the integers 0,...,m-1.

The finite multidimensional Szemeredi theorem, due to Furstenberg and Katznelson [4] and also given in the finite form of Theorem 10.3 of [5], says that for every delta>0, every sufficiently large m, and every subset S of this square of size at least delta m^2, S contains a translated positive integral dilation of {(0,0),(1,0),(0,1),(1,1)}. In particular it contains

(u,v), (u+d,v), (u,v+d), (u+d,v+d)

with 1<=d<m, and with all coordinates in 0,...,m-1. The all-sufficiently-large-m form follows from the finite theorem at density delta/2: tile a larger square by fixed-size squares, discard its O(m) boundary, and find a tile of density at least delta/2. These points are the four edges of a nondegenerate C4 in the bipartite graph. The edges (u+d,v) and (u,v+d) have equal input u+v+d+z_m to f_m modulo m, and hence equal colors. This contradicts R. Therefore every fixed positive edge density is impossible for all sufficiently large m, which is the claimed little-o estimate. QED.

This rules out a natural linear-palette ansatz, even with arbitrary output coarsening or relabeling. It does not rule out arbitrary colorings, arbitrary Latin-square labels, nonunit coefficients, or vector-space labels over growing-dimensional finite fields. No quantitative rate beyond the cited theorem is claimed.

## 5 Approach four: complete blowups do not amplify a fixed seed

**Lemma 5.** In K_{s,t}, where s,t>=2, every pair of distinct edges lies in a common C4. Therefore an R-coloring of K_{s,t} requires exactly st colors.

For disjoint edges use their four endpoints. For edges sharing one endpoint, select another vertex in that endpoint's part to complete the cycle. Thus any two colors must differ; assigning a distinct color to each edge attains st.

Now fix an h-vertex graph with at least one edge and replace each vertex with t independent twins and each old edge with a complete bipartite graph between its twin classes. The resulting graph has ht vertices and contains a K_{t,t}. For t>=2 it needs at least t^2 colors in any R-coloring. For t>h this exceeds ht. Accordingly a complete uniform blowup of any fixed seed cannot supply the required family, even when all edges may be recolored after blowup. This does not exclude sparse, nonuniform, or otherwise modified amplification.

Padding by isolated vertices does preserve validity, but loses density: an m-edge graph on n vertices has density m/N^2 after padding to N. A family available only at arbitrarily separated sizes does not thereby establish a uniform positive density for every large N.

## 6 Approach five: a codegree count stops short of vanishing density

Let G have n>=1 vertices, m edges, and an R-coloring with at most q colors. Put D=max(1,floor(q/2)). Any two vertices with d>=2 common neighbors induce the edges of a K_{2,d} subgraph. Lemma 5 implies 2d<=q. If d<=1 then d<=D anyway. Hence every codegree is at most D.

Double-counting length-two paths gives

sum_v binom(deg(v),2) = sum_{unordered {u,w}} |N(u) intersect N(w)| <= binom(n,2) D.

Cauchy-Schwarz and sum_v deg(v)=2m yield

2m^2/n - m <= n(n-1)D/2.

Solving the resulting quadratic inequality gives

m <= (n/4) (1 + sqrt(1 + 4(n-1)D)).

For q=n this is m <= (1/(2 sqrt(2)) + o(1))n^2. This is a valid elementary obstruction above a fixed density threshold, but it leaves every sufficiently small fixed positive density possible. It therefore does not resolve the original question. No sharpness is claimed.

## 7 Exact remaining task

Either construct, for every sufficiently large n, an n-vertex R-colored graph with at least epsilon n^2 edges and at most n colors for some fixed epsilon>0; or prove the negation, equivalently liminf E_R(n)/n^2=0. Proving E_R(n)=o(n^2) would suffice and is the stronger sparsity direction suggested by the literature.

Theorem 1 removes improper adjacent repetitions at negligible cost, but it leaves the proper density problem. Theorem 4 and Lemma 5 remove only particular construction strategies. The hypergraph converse counterexample prevents an invalid reduction, and the codegree estimate has a nonzero quadratic leading term. These are the explicit gaps at the end of five approaches.

## References

[1] S. A. Burr, P. Erdos, R. L. Graham, and V. T. Sos, Maximal Antiramsey Graphs and the Strong Chromatic Number, Journal of Graph Theory 13 (1989), 263-282. Definition on printed p.264; dense C4 discussion on printed p.273. https://doi.org/10.1002/jgt.3190130302 ; author-archive PDF: https://users.renyi.hu/~p_erdos/1989-10.pdf

[2] A. Gyarfas and G. N. Sarkozy, Less Strong Chromatic Indices and the (7,4)-Conjecture, Studia Scientiarum Mathematicarum Hungarica 60 (2023), 109-122. Definitions and Questions 1.2-1.3, Propositions 1.4 and 1.6, printed pp.111-113. https://doi.org/10.1556/012.2023.01539 ; author PDF: https://www.renyi.hu/~gyarfas/Cikkek/204_studia.pdf

[3] J. Fox, A new proof of the graph removal lemma, Annals of Mathematics 174 (2011), 561-579; arXiv:1006.1300v2, introduction p.2 and Theorem 1 p.3. The triangle removal lemma itself is credited there to Ruzsa and Szemeredi. https://arxiv.org/abs/1006.1300 ; https://annals.math.princeton.edu/2011/174-1/p17

[4] H. Furstenberg and Y. Katznelson, An ergodic Szemeredi theorem for commuting transformations, Journal d'Analyse Mathematique 34 (1978), 275-291, Theorem B, printed p.275. https://doi.org/10.1007/BF02790016 ; public institutional copy: https://www.cs.umd.edu/~gasarch/TOPICS/vdw/ergodicsz.pdf

[5] W. T. Gowers, Hypergraph regularity and the multidimensional Szemeredi theorem, Annals of Mathematics 166 (2007), 897-946; arXiv:0710.3032, Theorem 10.3. https://arxiv.org/abs/0710.3032
