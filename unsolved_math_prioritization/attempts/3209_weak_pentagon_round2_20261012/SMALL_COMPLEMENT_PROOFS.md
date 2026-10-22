# Prescribed Clebsch classes: small complements, a one-sided theorem, and a sharp degree-free boundary

12 October 2026 UTC. Weak pentagon problem, queue row 1752 / problem 3209 (OPG434). **Accepted restricted second-round results; not a solution of the full conjecture.** No novelty claim is made.

## 1. Results and exact scope

Write Q4 for the ordinary four-dimensional cube on F2^4, with unit-vector edge differences, and J=1111 for its antipodal difference. The Clebsch graph is obtained by adding all antipodal edges to Q4. Let G be finite, simple and triangle-free. Fix a cut with sides X,Y, put B=δ(X), and let M=E(G)\B. A fixed-M extension is a map f such that B-edges have unit differences and M-edges have difference J. Thus M is exactly one specified canonical Clebsch color class.

This packet proves these restricted assertions:

1. If |M|≤2, a fixed-M extension exists, with **no degree or matching assumption**.
2. If G is subcubic, M is a matching and |M|≤3, an elementary construction gives a fixed-M extension.
3. If G is subcubic, M is a matching and **all its edges lie on one cut side**, a fixed-M extension exists for arbitrary |M|. This proof uses the published signed degree-choosability theorem, explicitly identified below.
4. The degree-free bound in assertion 1 is sharp: an authored 15-vertex triangle-free graph has a **global maximum-cut complement of three matching edges** with no fixed-M extension. Its maximum degree is 8, so it is outside the weak-pentagon target.

None of assertions 1–3 needs the specified cut to be globally maximum. A maximum cut of a subcubic graph has matching complement, so they apply to the corresponding restricted maximum-cut cases. They do **not** establish the general fixed-global-maximum-cut strengthening or the weak pentagon conjecture. The first-round finite catalog evidence and its independent audit are not premises of any proof here.

The original cubic-to-Clebsch target and its standard cut-complement equivalences are in DeVos–Šámal, [High-girth cubic graphs are homomorphic to the Clebsch graph](https://arxiv.org/abs/math/0602580v2), Proposition 1.1/3.2 and Conjecture 1.4. This packet studies a sufficient, stronger strategy with one prescribed class; failure of that strategy alone need not disprove the original target.

## 2. Two elementary cube facts

### Lemma 2.1: three same-parity vertices

A set of at most three vertices of Q4, all in the same parity class, has a common neighbor if and only if it contains no antipodal pair. Repetitions in a list of vertices make no difference.

**Proof.** Antipodes have cube distance 4 and cannot have a common neighbor. For the converse, translate one of the vertices to 0. Translation preserves distances and changes every parity equally. Every remaining distinct vertex has weight 2, since it is even and is neither 0 nor J. If two remain, their two-element supports are not disjoint, since disjoint supports would make them antipodal. A unit vector in their intersection is adjacent to all three vertices. The cases with fewer distinct vertices are immediate; an empty set imposes no restriction. ∎

The size-three bound matters. The four even vertices 0,3,5,6, written as four-bit integers, contain no antipodal pair but have no common cube neighbor. Thus a degree-four vertex cannot be handled by merely excluding antipodes among its neighbor images.

### Lemma 2.2: antipodal pairs and one neighborhood

Each parity class of Q4 splits into four antipodal pairs. If h is in the other parity class, its four neighbors contain exactly one vertex from each of those pairs, and the four neighbors of h+J are their antipodes.

**Proof.** h+ei is never antipodal to h+ej: their difference has weight 0 or 2, not 4. There are four such neighbors and four pairs. Adding J exchanges the neighborhoods. ∎

## 3. A fully explicit rectangular-grid extension lemma

Let R(k,l) be the Cartesian product of paths on {0,…,k} and {0,…,l}, where k,l≥1. Its graph distance is Manhattan distance.

### Lemma 3.1: extending distance-compatible grid terminals

Let H be any bipartite graph. Suppose some terminal vertices t are assigned points (a_t,b_t) in R(k,l), and that within each connected component:

- |a_t−a_s|+|b_t−b_s|≤d_H(t,s);
- the parity of a_t+b_t agrees with one fixed choice of the bipartition of H.

Then the assignment extends to a graph homomorphism H→R(k,l).

**Proof.** Work in a component containing terminals. Put p_t=a_t+b_t and q_t=a_t−b_t. Define

p(v)=min_t(p_t+d_H(v,t)),     q(v)=min_t(q_t+d_H(v,t)).

The identity |a−a′|+|b−b′|=max(|(a+b)−(a′+b′)|, |(a−b)−(a′−b′)|) shows that both prescribed scalar functions are 1-Lipschitz on the terminals. The two displayed minima therefore recover p_t,q_t at every terminal and are 1-Lipschitz on all vertices. Every summand in either minimum has the parity assigned to v by the bipartition. Consequently p and q have equal parity at v, and each changes by exactly +1 or −1 across an H-edge.

Set a(v)=(p(v)+q(v))/2 and b(v)=(p(v)−q(v))/2. These are integers. Across an edge, exactly one of a,b changes by 1 in absolute value and the other stays fixed. Thus they define a homomorphism into the infinite square grid.

For m≥1 define r_m(z)=m−|((z mod 2m)−m)|, with the residue in {0,…,2m−1}. This maps the integer path onto {0,…,m}, fixes that interval, and takes adjacent integers to adjacent integers. Applying r_k and r_l to the respective coordinates gives the required map to R(k,l), preserving all assigned terminal points. A component with no terminals maps to any one edge of R(k,l). ∎

This is a constructive proof; it does not invoke an absolute-retract classification.

### Theorem 3.2: two omitted edges without a degree bound

If G is triangle-free and |M|≤2, then M extends, whether or not its edges are disjoint.

**Proof.** If M is empty, map X and Y to the two ends of a cube edge. For one edge uv, the endpoints have the same cut parity. In their common B-component their distance is even and at least 4, since a length-two B-path would make a triangle with uv. Map distance d from u onto the path 0,1,3,7,15 for d≤4, and onto 15 for larger even d and 7 for larger odd d. Adjacent vertices in a bipartite graph have distance levels differing by exactly 1. Thus u,v map to antipodes. If they are in different B-components, choose cube-edge maps of those components giving u value 0 and v value 15. Other components are unrestricted.

If the two M-edges share an endpoint, say uv and uw, use the same distance map rooted at u on its B-component. Each of v,w that lies there has even distance at least 4 and receives 15. In other components map the common cut class containing v,w to 15. The other cut class maps to a fixed neighbor of 15. Both demands are met.

It remains to treat disjoint edges uv and xy. Assign grid corners

u↦(0,0), v↦(k,l), x↦(k,0), y↦(0,l), with k+l=4.

If all four endpoints lie on the same cut side, choose k=l=2. Distinct same-side terminals have B-distance at least 2, and each demanded pair has B-distance at least 4. Hence the terminal assignment is distance-compatible.

Otherwise uv lies on one cut side and xy on the other. The cross distances have odd parity. A B-edge ux or vy requires k=1; a B-edge uy or vx requires l=1. These two requirements cannot both occur: any edge of the first type and any edge of the second type share a terminal and, together with uv or xy, would form a triangle. Choose (k,l)=(1,3) if an edge of the first type exists, (3,1) if an edge of the second type exists, and (1,3) if neither exists. Every other finite cross distance is at least 3. The resulting terminal assignment is again distance-compatible and has the correct parity. Infinite distances between components impose no condition.

Lemma 3.1 extends the assignment to R(k,l). Embed this grid into Q4 by representing its first coordinate as a prefix of k one-bits and its second as a prefix of l one-bits in a disjoint block. A grid edge flips one bit, and opposite corners differ by all four bits. This is the desired extension. ∎

## 4. Three matching edges in subcubic graphs: an elementary construction

### Theorem 4.1

Suppose G is triangle-free and subcubic, M is a matching cut complement and |M|≤3. Then M extends.

**Proof.** If every M-edge lies in X, assign a different antipodal pair of even cube vertices to the two endpoints of each M-edge. At most three of the four pairs are used. Assign all remaining vertices in X one vertex of an unused pair. The only antipodal pairs among assigned X-images are the endpoints of M-edges. No such endpoints share a B-neighbor, since that would form a triangle in G. Each vertex in Y therefore sees at most three even cube images, with no antipodal pair. Lemma 2.1 lets us choose its odd image independently. There are no M-edges in Y. The case with all M-edges in Y is obtained by swapping sides.

In the remaining case, swap sides if necessary so that M has one edge rs in Y and at most two edges in X. Choose an odd cube vertex h. Write the four even antipodal pairs as (a_i,b_i), i=1,…,4, with a_i∈N_Q4(h) and b_i=a_i+J∈N_Q4(h+J), using Lemma 2.2.

Let R=N_B(r)⊆X and T=N_B(s)⊆X. Triangle-freeness gives R∩T=∅. It also says that neither R nor T contains both endpoints of an M-edge.

Assign one of the pairs (a_1,b_1),(a_2,b_2) to each M-edge in X, using a distinct pair for each edge. Orient it so that an endpoint in R receives a_i and an endpoint in T receives b_i. The preceding disjointness and triangle restrictions make these requirements consistent. When neither endpoint imposes a requirement, choose either orientation.

Every still-unassigned vertex in R receives a_3, every still-unassigned vertex in T receives b_4, and all other unassigned X-vertices receive a_3. The only antipodal image pairs among X-vertices are again the endpoints of the prescribed M-edges: the two base colors use different unused pairs. Thus every Y-neighborhood has a common cube neighbor by Lemma 2.1. For r choose h, since all its neighbor images lie in N_Q4(h); for s choose h+J. Choose the other Y-images independently. All B-edges and all M-edges satisfy the required differences. ∎

This proof is independent of the signed-coloring result used next. The theorem also covers disconnected graphs because the chosen cut sides and image assignments can be used simultaneously across components.

## 5. Arbitrarily many one-sided prescribed edges

### External theorem used in this section

A signed graph here is loopless and may have parallel edges, with signs σ(e)∈{−1,+1}; a coloring c satisfies c(v)≠σ(vw)c(w). Schweser–Stiebitz, [Degree choosable signed graphs, arXiv:1507.04569v1](https://arxiv.org/html/1507.04569v1), Theorem 2.1(a),(e), implies: if a connected signed graph cannot be colored from lists of size at least each vertex's degree, every list has exactly that degree and every block is a brick. Their brick types are balanced complete graphs, balanced odd cycles, unbalanced even cycles, doubled complete graphs 2K_n, and doubled odd cycles 2C_n. In a doubled graph each original edge is replaced by a positive and a negative edge. “Balanced” means every cycle has positive sign product.

The definitions and these theorem statements were directly inspected in the cited primary manuscript. Its full proof in that manuscript is an external dependency, not an independently re-proved result of this packet. The journal bibliographic identity is *Discrete Mathematics* 340(5), 882–891 (2017), [DOI 10.1016/j.disc.2017.01.007](https://doi.org/10.1016/j.disc.2017.01.007); the journal full text was not inspected for this packet.

### Theorem 5.1: one-sided matching complement

Let G be triangle-free and subcubic. If M is a matching cut complement and every M-edge has its endpoints in X, then M extends, with no bound on |M|.

**Proof.** Fix a bijection θ from the eight signed colors C={±1,±2,±3,±4} to the even cube vertices such that θ(−c)=θ(c)+J. We will assign signed colors to X so that M-pairs receive opposite colors and vertices sharing a neighbor in Y do not receive opposite colors. Lemma 2.1 then supplies every Y-image.

Collapse each M-pair in X to one entity; each unmatched X-vertex is a singleton entity. For each x∈X, write P(x) for its entity and choose ε_x∈{±1}, taking opposite signs on an M-pair and +1 on a singleton. An entity color c_P will give x the signed color ε_x c_P.

For each y∈Y and every unordered pair of distinct neighbors x,z of y, impose an edge between P(x),P(z) with sign −ε_x ε_z. Its signed coloring constraint is precisely

ε_x c_{P(x)} ≠ −ε_z c_{P(z)}.

There are no loops: if x,z were one M-pair, xyz would be a triangle in G. Delete repeated copies of an edge having the same sign, while preserving opposite-sign parallel edges. Call the resulting signed graph F. This deletion does not change its colorings.

A singleton entity has degree at most 3·2=6. A paired entity represents two X-vertices each of B-degree at most 2, and each incident Y-vertex contributes at most two constraints; its degree is at most 2·2·2=8. Thus Δ(F)≤8.

Suppose a connected component K of F cannot be colored from the fixed lists C. Apply the external theorem to these lists of size 8. Every vertex of K has degree exactly 8, and every block is a brick. If K had a cut vertex, take an end block. A non-cut vertex of that block has total degree 8. Each brick is regular, so the block itself is 8-regular; its cut vertex would then already have degree 8 inside the block and also have an edge outside it, a contradiction. Therefore K is a single 8-regular brick. The only types with degree 8 are a balanced K9 and 2K5.

Degree 8 forces equality in all bounds used above. In particular every entity of K is an M-pair, both represented X-vertices have B-degree 2, every Y-vertex adjacent to them has B-degree 3, and its other neighbor entities belong to K. The three entities at any such y are distinct, by triangle-freeness. Their three constraint signs have product

(−ε_x ε_z)(−ε_z ε_w)(−ε_w ε_x)=−1.

Thus they form a triangle with negative sign product. If K were the balanced K9, the three edges are its unique edges on those vertex pairs and contradict balance.

If K were 2K5, it would represent exactly ten X-vertices. Each has B-degree 2, giving twenty incidences to adjacent Y-vertices. Every such Y-vertex has degree 3 and has all its neighbors among those ten X-vertices, because its constraints keep all three entities in K. Hence twenty would be divisible by three, a contradiction.

No component K is uncolorable. Choose a C-coloring of F and set f(x)=θ(ε_x c_{P(x)}). M-pairs are antipodal. In every Y-neighborhood no image pair is antipodal, exactly by the constraints defining F. By Lemma 2.1 its at most three images have a common odd cube neighbor; choose that for f(y). This completes the extension. ∎

The argument handles same-sign duplicate constraints and opposite-sign parallel constraints explicitly; applying a simple-graph Brooks theorem alone would not suffice. It also uses list size 8 directly, rather than inferring availability of a zero-free eight-color palette from an ambiguous smaller odd-sized signed chromatic palette.

## 6. Sharpness without the degree-three hypothesis

### Construction

Let A={t,a_1,b_1,a_2,b_2,a_3,b_3}. Let Y contain a vertex y_ε for each ε∈{0,1}^3. Join y_ε to t and to a_i if ε_i=0, or b_i if ε_i=1, for each i=1,2,3. Denote this bipartite graph by B. Add the three edges a_i b_i, forming M, to obtain G.

There are 15 vertices, 32 B-edges and 3 M-edges. The degrees are 8 at t, 5 at each a_i,b_i, and 4 at each y_ε. The graph is simple, connected and triangle-free. Indeed, the bipartite part has no triangle; a triangle containing an M-edge would require a y_ε adjacent to both endpoints of that pair, which never occurs.

### Proposition 6.1: the displayed cut is globally maximum

Every nontrivial B-cut has at least four edges. To see this, take a nonempty proper side U not containing t and let k=|U∩Y|. If k≥4, the k edges from these vertices to t already cross the cut. If k≤3 and U contains a terminal a_i or b_i, that terminal has four Y-neighbors, at least 4−k of which lie outside U; together with the k t-edges these give at least four crossing edges. If U contains no terminal, it consists only of Y-vertices, each of degree 4, and again the cut has at least four edges.

Switching a vertex set U in the displayed G-cut changes its size by |δ_M(U)|−|δ_B(U)|. For nontrivial U, this is at most 3−4<0. Thus the B-cut of size 32 is the unique maximum cut up to exchanging its sides. In particular M is a global maximum-cut complement, not merely a locally optimal one. ∎

### Proposition 6.2: M has no fixed extension

**Proof.** In any fixed extension, the connected bipartite graph B maps to Q4 with a fixed parity on A; translate if needed so that this is even. Each (a_i,b_i) occupies an antipodal pair. Any endpoints from different pairs share some y_ε, so their images cannot be antipodal. Hence the three demands occupy three distinct antipodal pairs of even cube vertices. Vertex t shares a neighbor with every endpoint, so its image cannot be antipodal to any endpoint; since both members of the three pairs appear, f(t) belongs to the fourth pair.

By Lemma 2.2, every odd cube neighbor h of f(t) has exactly one even neighbor in each of the three occupied terminal pairs. Therefore h supports exactly one of the eight transversals (one chosen endpoint of each pair). There are only four choices of h∈N_Q4(f(t)), but the eight distinct y_ε require all eight different transversals. At least four have no possible image. Contradiction. ∎

This explicit obstruction is a counterexample only to the degree-free extension claim with three demands. It is not subcubic and makes no claim of being a counterexample to an unrestricted Clebsch homomorphism.

## 7. Global optimality and the exact unresolved part

For any fixed cut, switching U increases its size by |δ_M(U)|−|δ_B(U)|. Thus it is globally maximum exactly when

|δ_B(U)|≥|δ_M(U)| for every U⊆V(G).

For subcubic graphs, stability under single-vertex switches makes M a matching: a vertex with two uncut incident edges would improve the cut upon switching. This implication does not reverse global optimality.

The theorems above eliminate all matching complements of size at most three and all one-sided matching complements. They do not address every mixed-side complement with four or more edges. For a cubic graph specifically, degree summation gives

3(|X|−|Y|)=2(|M∩E(X)|−|M∩E(Y)|).

Consequently |M|=4 can only have the mixed distribution 2+2, and |M|=5 can only have distribution 4+1, up to exchanging sides. A global-maximality proof must address these mixed interactions; none is supplied here.

The signed reduction explains one exact obstruction to extending its proof: if M also contains Y-edges, choosing each Y-image independently no longer suffices. Opposite endpoints of a Y-demand must receive antipodal common neighbors simultaneously. Two lists of common neighbors that are individually nonempty need not have antipodal representatives. Degree-eight coloring of F alone does not encode that coupling. The high-degree example also shows that replacing the cubic hypothesis by the global switching inequalities cannot rescue the unrestricted statement.

## 8. Verification and provenance

The independent acceptance audit checks every proof above and the separately stated high-degree addendum. Authored computational checks corroborated the cube lemmas, elementary constructions, signed reduction, the 15-vertex graph, every normalized cut of that graph, and its terminal assignments. Exact counts and control outcomes are retained in [the small-complement audit](SMALL_COMPLEMENT_AUDIT.md) and [the reproduction scope](REPRODUCTION_SCOPE.md). The universal conclusions rest on the written proofs and the stated external theorem, not on those finite tests.

The original symbolic checker used assertions. Its normal replay was accepted as corroboration; its optimized runs are not semantic verification. The optional missing-catalog path was not accepted as completion of catalog checks. A separate explicit-exception implementation supplied fail-closed verification and negative controls in normal, -O, and -OO modes.

The graph and proofs are authored material. This edition distributes mathematical prose, small explicit authored examples, audit reasoning, and permitted public source metadata. It does not distribute executable checkers, raw sample collections, runtime records, copied source documents, or identities of excluded operational artifacts. Consequently the full retained computational runs cannot be reproduced from this prose edition alone. The mathematical constructions and finite checks are described for independent reimplementation, with the boundary made explicit in [REPRODUCTION_SCOPE.md](REPRODUCTION_SCOPE.md).

The signed theorem is credited to its authors. Its exact source and application were inspected; that inspection is not a novelty claim or an exhaustive review of later literature.
