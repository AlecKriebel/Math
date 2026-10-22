# Third newly documented investigation: pentagon scarcity and the three-square skeleton

Target: problem 3327 / OPG-172. This is the third newly documented substantive pass. The lifetime attempt count is unknown. The unrestricted existence question remains unresolved.

## Results

For an h=2 target, and also for an ordinary Euler hopper of Euler genus four:

1. Every pentagon contains at most two three-square edges.
2. Vertices incident with four three-square edges form an independent set; their neighbors are incident with exactly two three-square edges.
3. At each such four-edge vertex, exactly two of the three possible complementary-pair edges between its six second neighbors occur. Its four three-square edges consequently have a unique partition into two squares using only three-square edges.
4. Every connected component of the three-square-edge subgraph containing a degree-four vertex has a unique square decomposition. Components having only degree-two vertices are cycles.
5. At least one of those cycle components has length at least six. Moreover the sum of the lengths of all cycle components of length other than four is a positive multiple of four, hence at least eight.

Thus the surviving obstruction to the accepted exact-cover criterion must reside in isolated cycle components of the three-square skeleton, not in its degree-four components. No example, universal nonexistence result, upper order bound, or novelty claim is supplied.

## Inputs and notation

All graphs are finite ordinary simple graphs. Write E for Euler genus. The [first structural report](../3327_surface_obstruction_reductions_20261012/STRUCTURAL_REPORT.md), [second structural report](../3327_square_rotation_frontier_20261012/STRUCTURAL_REPORT.md), and [second independent mathematical audit](../3327_square_rotation_frontier_20261012/INDEPENDENT_AUDIT.md) are the dependencies for the following facts: an h=2 target has E(G)=4, is connected, quartic, triangle-free and K_(2,3)-free; every edge belongs to exactly two or three squares; every edge belongs to at least two pentagons; an edge in exactly two squares belongs to at least four pentagons. The same facts hold for an ordinary Euler hopper of Euler genus four.

Write E_2 and E_3 for the two edge classes and T=(V(G),E_3). The full square link at a vertex is a simple graph on its four incident edge ends. Its degrees are two or three, so it is C4, K4 minus an edge, or K4. Correspondingly its degree in T is zero, two, or four. Call these vertex sets D0, D2 and F. In a D2 link the unique missing pair consists of its two E_2 ends.

For any edge uv, the squares through it correspond to edges between A=N(u) minus {v} and B=N(v) minus {u}. This crossedge graph is a matching: if an A vertex a had two neighbors b_1,b_2 in B, then a and v would have the three common neighbors u,b_1,b_2; the other side is symmetric. An E_3 edge therefore gives a perfect matching between A and B. Equivalently, at an end of an E_3 edge, every pair containing that edge end lies in a unique square.

The accepted square-selection theorem says E(G)=2 if and only if the E_3 edges admit a partition into squares consisting entirely of E_3 edges. The accepted contraction argument says that every Euler-genus-at-most-two embedding of G/uv is strictly alternating on its three A and three B ends. Its faces have one of two profiles: two triangular faces and all remaining faces quadrangular, or three triangular faces, one pentagonal face, and all remaining faces quadrangular. All these facial walks are simple cycles.

No new source retrieval or external classification is needed for the proofs below.

## 1. Pentagon lemma

**Theorem 1.** Let G be simple, quartic, triangle-free and K_(2,3)-free, with every edge in two or three squares. Every pentagon of G contains at most two E_3 edges.

Proof. Fix a pentagon v_0 v_1 v_2 v_3 v_4 v_0, with subscripts modulo five. Let q_i mean that v_(i-1) and v_(i+1) have a second common neighbor x_i other than v_i. This neighbor is unique by K_(2,3)-freeness. It is outside the pentagon because every chord of a pentagon would create a triangle. Any two existing x_i and x_j are distinct: if equal, that common vertex would be adjacent to the union of their prescribed pairs of pentagon vertices; for distinct i,j this union contains an adjacent pair, creating a triangle.

An E_3 edge v_i v_(i+1) forces both q_i and q_(i+1), by the perfect square matching. Suppose also that q_(i-1) and q_(i+2) hold. Quarticity now gives the two cross-neighbor sets for this edge as

A={v_(i-1),x_(i-1),x_(i+1)},
B={v_(i+2),x_i,x_(i+2)}.

The perfect matching already includes v_(i-1)x_i and x_(i+1)v_(i+2). Its third edge must therefore be x_(i-1)x_(i+2). Both endpoints of this edge are adjacent to v_(i+3), again creating a triangle. Consequently, for every E_3 edge v_i v_(i+1), at least one of q_(i-1),q_(i+2) fails.

Now suppose the pentagon has at least three E_3 edges. Each endpoint of such an edge has its corresponding q true. If those edges cover all five vertices, every q is true, a contradiction. Otherwise the only possibility is exactly three consecutive edges covering four consecutive vertices. For the middle of these three edges, all four q values just used are true, again a contradiction. This proves the theorem. QED.

This lemma is purely combinatorial and does not assume any embedding or genus-minor hypothesis.

## 2. Independent full-link vertices

**Corollary 2.** Suppose additionally that every edge of G lies on a pentagon. Every E_3 edge has an endpoint in D2. The set F is independent, every neighbor of F is in D2, and |D2| >= 2|F|.

Proof. Take an E_3 edge uv and a pentagon containing it. If both u and v were in F, the two other pentagon edges incident with u or v would also belong to E_3, contradicting Theorem 1. An endpoint of an E_3 edge is in D2 or F, proving the first two assertions. All four neighbors of an F vertex are therefore in D2. Counting F--D2 edges gives 4|F| <= 2|D2|, since each D2 vertex has only two E_3 edges. QED.

In particular an h=2 target cannot have every edge in three squares. This excludes that entire stratum without a classification of rectagraphs or a calculation on any particular graph.

## 3. The six second neighbors of a full-link vertex

Fix f in F and label its neighbors a,b,c,d. For each unordered pair {i,j} among these four neighbors, write x_ij for the other common neighbor of i and j. It exists because the square link at f is K4. The six x_ij are distinct: an equality for different pairs would give f and the common x at least three common neighbors. They are outside the closed neighborhood of f by triangle-freeness.

Moreover

N(i)={f,x_ij,x_ik,x_il}

for {i,j,k,l}={a,b,c,d}. Every pentagon through f must consequently have form

f-i-x_ij-x_kl-k-f,

where {i,j} and {k,l} are complementary pairs. The pairs must be disjoint because an edge between two x vertices with overlapping labels would close a triangle with their common labeled neighbor.

Let r_f be the number of edges present among the three possible complementary pairs

x_ab x_cd, x_ac x_bd, x_ad x_bc.

Each present complementary edge produces exactly four distinct pentagons through f, obtained by choosing one of its two labels at each end. Each edge fi lies on exactly two of these four pentagons. Thus f lies on exactly 4r_f pentagons and each incident edge lies on exactly 2r_f pentagons. This is an exact count, not merely a lower bound.

## 4. Contraction excludes r_f=1

**Lemma 3.** For an h=2 target or ordinary Euler-genus-four hopper, r_f >= 2.

Proof. Every incident edge lies on a pentagon, so r_f>=1. Suppose r_f=1 and contract fa. The six ends at the contracted vertex w split as

A={b,c,d}, B={x_ab,x_ac,x_ad}.

The three possible triangular faces use the square-matching pairs b--x_ab, c--x_ac, d--x_ad. A quadrangular face through w lifts to a pentagon containing fa. There are exactly two such graph pentagons, and their endpoint pairs share the same B end: for example, if the sole complementary edge is x_ab x_cd, the two pairs are c--x_ab and d--x_ab.

In the two-triangular-face profile, four of the six corners at w must belong to quadrangular faces. Those lift to four distinct pentagons, impossible.

In the three-triangular-face profile, the three triangular corners form the perfect matching just listed in the alternating C6 link at w. The other three corners form another perfect matching. At least two of these three corners belong to quadrangular faces, since the unique pentagonal face can use w at most once. Those two corners must have different B ends. The only two available pentagons have the same B end, again impossible. QED.

The argument uses the contracted rotation and face profile, rather than assuming that a large scalar pentagon count by itself gives a valid embedding.

## 5. Exactly two complementary edges and forced squares

**Theorem 4.** At every f in F in an h=2 target or ordinary Euler-genus-four hopper, r_f=2. There are exactly two squares consisting entirely of E_3 edges through f, and these two squares partition its four incident edges.

Proof. Corollary 2 puts a,b,c,d in D2. Each neighbor i therefore has exactly one E_3 edge other than if, among its three radial edges i x_ij.

A present complementary edge x_ij x_kl gives four pentagons through f. Each already has two E_3 edges incident with f. By Theorem 1, the complementary edge and all four radial edges i x_ij, j x_ij, k x_kl, l x_kl must belong to E_2.

If all three complementary edges were present, this would forbid every radial edge from E_3, contradicting the D2 status of the neighbors. Hence r_f<=2. Lemma 3 gives equality.

Suppose the absent complementary edge is x_ab x_cd. The two present complementary edges force all radial edges except a x_ab, b x_ab, c x_cd, d x_cd into E_2. Each neighbor needs one radial E_3 edge, so these four exceptional radial edges are all E_3. Consequently

f-a-x_ab-b-f and f-c-x_cd-d-f

are squares consisting entirely of E_3 edges and partition the four edges at f. Any all-E_3 square through f must use the sole other E_3 edge at each of its two neighbors, so these are the only two. QED.

A further valid rigidity statement is that every low-genus contraction embedding of an edge fi has all three triangular faces and its single pentagonal face through the contracted vertex. Indeed the absent complementary pair leaves one B end with no lifted-pentagon support. In a two-triangle profile, or a three-triangle profile whose pentagon avoids the contracted vertex, that B end would have to achieve degree two in the link from at most its one triangle corner, which is impossible. No nonexistence conclusion is inferred from this additional face rigidity.

## 6. The remaining square-decomposition obstruction

**Theorem 5.** Every component of T containing an F vertex has a unique partition into all-E_3 squares. Every component of T containing edges but no F vertex is a cycle. For a target or Euler-genus-four hopper, at least one of these latter cycles has length at least six.

Proof. Each edge incident with an F vertex is in exactly one all-E_3 square by Theorem 4. At a D2 vertex, an all-E_3 square must use both E_3 edges. There is at most one such square, because its opposite vertex would otherwise give the two E_3 neighbors three common neighbors. Thus every edge already covered by one of the forced squares cannot be covered by a different all-E_3 square. Moreover, if either edge at a D2 vertex is covered, both are covered. If any edge at an F vertex is reached, Theorem 4 covers all four of its edges. Propagating through a connected component containing F therefore covers every edge exactly once. It also proves uniqueness.

A component containing edges and no F is connected and 2-regular, hence a cycle. It is square-decomposable precisely when its length is four. It cannot be a triangle because G is triangle-free and cannot be a pentagon by Theorem 1. If every such cycle had length four, combining its square with the unique decompositions of the F-containing components would partition all E_3 edges into squares. The accepted exact-cover theorem would give E(G)=2, contradicting E(G)=4. Therefore some all-D2 component is a cycle of length at least six. QED.

**Corollary 6.** Let B be the total number of edges in the all-D2 cycle components whose lengths are not four. For a target or Euler-genus-four hopper, B is a positive multiple of four and B>=8.

Proof. If s is the total number of graph squares and n the order of G, double-counting square-edge incidences gives

4s=2|E_2|+3|E_3|=4n+|E_3|.

Thus |E_3| is divisible by four. Removing the uniquely square-decomposed F components and the length-four cycle components removes multiples of four edges. The remaining edge count B is positive by Theorem 5 and divisible by four. Each remaining cycle has length at least six, so B>=8. QED.

The incidence count also sharpens to |D2| >= 2|F| + B >= 2|F| + 8: the B vertices in those isolated cycle components have no F neighbor, so all 4|F| edges from F end in the other D2 vertices, which can receive at most two each.

This gives a necessary structure, not an upper bound on the lengths or number of the remaining cycles. In particular, a length-six component is not individually ruled out: the sum of all residual component lengths, rather than each separate length, must be divisible by four.

## Verification and boundary

The report provides complete combinatorial proofs of its unbounded claims. The dependency-free checker exhausts all 1,024 E_3/q flag assignments on a pentagon, all six labelled alternating C6 links, and all eight complementary-edge patterns at a full-link vertex. It checks the radial forcing and the contraction face-profile restrictions. Graph controls are the circulant C12(2,3), C5 Cartesian-product C5, and Q4. Their pentagon counts are respectively 48, 10 and zero; every pentagon in the circulant has exactly two E_3 edges, and every pentagon in the Cartesian-product graph has zero. The checker was executed under normal Python, -O and -OO with byte-identical output; no essential check depends on assertions. These checks are corroboration, not an enumeration of all graphs or a replacement for the proofs.

The unresolved first-genus frontier consists of nonbipartite graphs satisfying the accepted restrictions and the new conditions above, including an isolated all-D2 E_3 cycle component of length at least six. Neither those remaining cycle components nor the higher-genus and orientably-simple routes are excluded here.

No new external source retrieval is used.
