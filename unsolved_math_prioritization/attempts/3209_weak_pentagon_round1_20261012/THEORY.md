# Weak pentagon problem: exact normalization and boundary-extension lemmas

Date: 12 October 2026 UTC. Target: ordered queue row 1752, problem 3209, OPG434. This is the first confirmed substantive continuation round after an earlier bounded screen; the lifetime number of earlier attempts is unknown. It is **not a proof or disproof of the full weak pentagon conjecture**, and no novelty claim is made. The proofs below are complete for their expressly stated restricted conclusions. The main new work within this continuation is a normalization refinement, a fully proved arbitrary-boundary extension toolkit, and exact obstructions to tempting stronger local arguments. The sparse corollary is already subsumed by a stronger published result and is not advertised as a frontier improvement.

## 1. Target, conventions, and source boundary

All graphs here are finite, undirected, and simple. A cubic graph is 3-regular; subcubic means maximum degree at most 3. Components are allowed. A homomorphism need only preserve edges, not nonedges or distinctness. Five edge colors may be used improperly and some may be unused.

The [Open Problem Garden statement](https://www.openproblemgarden.org/op/weak_pentagon_problem) asks whether every triangle-free cubic graph has a partition E(G)=E1∪…∪E5 such that each graph (V(G), E(G)\Ei) is bipartite. Equivalently, it asks for G→H, where H is the Clebsch graph, also denoted PQ4 or PC(4).

[DeVos–Šámal, arXiv:math/0602580v2](https://arxiv.org/abs/math/0602580v2), revised 23 October 2009, states exactly the finite/simple conventions, the cubic conjecture as Conjecture 1.4, and the maximum-degree-three, girth-at-least-17 theorem as Theorem 1.3. Its Proposition 1.1/3.2 already establishes the equivalence with four disjoint cut complements and with five cut complements partitioning all edges. Those equivalences are credited, not claimed as new. Its computer-assisted girth theorem is an external result; the author program was not run in this packet. The [2011 journal DOI](https://doi.org/10.1002/jgt.20580) is a bibliographic identity, not a claim that the publisher PDF was independently audited.

A fresh bounded primary-source search found no full resolution. That is a search result, not a proof of current openness. In particular, the [2026 signed-projective-cube paper](https://doi.org/10.1002/jgt.70046) studies other signed and planar homomorphism results; none of its inspected statements is substituted for the unsigned triangle-free cubic conjecture.

We write δ(U) for the entire set of edges with exactly one endpoint in U. A bipartite edge set is merely contained in a cut; it need not equal that cut. This distinction is essential below.

## 2. A concrete Clebsch model

Let F=F2^4, with standard basis e1,…,e4, J=e1+…+e4, and generator set S={e1,e2,e3,e4,J}. Define H to have vertex set F and an edge xy exactly when x+y belongs to S. This is the quotient of the 5-cube by antipodes and hence is PQ4. We index J by color 5.

The only subsets of S summing to zero are the empty set and S itself. Indeed, in a relation ∑(i≤4) ai ei+a5J=0, coordinate i gives ai=a5. Consequently the only relation has all coefficients equal. Any permutation of the five generators extends to an invertible linear map: select any four generators as a basis and use their sum for the fifth. Translations and these linear maps are automorphisms.

### Lemma 2.1: cut/cycle parity characterization

An edge coloring c:E(G)→{1,…,5} is the generator coloring of a homomorphism G→H if and only if on every cycle of G the five color multiplicities have equal parity. On an even cycle each multiplicity is even; on an odd cycle each is odd.

**Proof.** For a homomorphism f, summing edge differences around a cycle gives zero. The unique-relation calculation gives equal parities. Conversely, assign one root value in F per connected component and define f(v) by summing the edge generators along any root-to-v path. The cycle condition makes this independent of path: every closed walk decomposes modulo 2 into cycles, so its sum is zero. Each edge then has its prescribed generator difference. Finally the sum of five equal parities equals that common parity, which is the parity of the cycle length. ∎

It suffices to check any cycle-space basis. For example, prescribe arbitrary colors on a spanning forest, obtain f by path sums, and test every remaining edge uv for f(u)+f(v)∈S. Its color is then forced. This is an exact finite recognition algorithm, not a polynomial-time solution of the conjecture: the naive forest-color enumeration has 5^(|V|−number of components) branches.

For each i, a generator coloring has E(G)\Ei equal to an entire cut. To see this directly, choose the linear functional ℓi on F taking value 0 on generator i and 1 on the other four. For i=5 this is coordinate parity; for i≤4 it is the sum of the three coordinates other than i. Then E(G)\Ei=δ({v:ℓi(f(v))=1}).

## 3. Normalizing an arbitrary weak-pentagon witness

### Theorem 3.1: one-direction recoloring and pentagon rigidity

Suppose E1,…,E5 is any coloring with bipartite complements. There is a generator coloring E1′,…,E5′ with Ei′⊆Ei for i≤4 and E5⊆E5′. Thus normalization only moves edges from one of the first four colors into color 5. Every edge belonging to a 5-cycle retains its original color. More generally, an edge of color i≤4 retains its color whenever it belongs to an odd cycle on which color i occurs exactly once.

**Proof.** For i≤4, choose a binary bipartition bi of G−Ei, independently on each component. Set b(v)=(b1(v),…,b4(v)). If uv has original color j≤4, every coordinate except possibly j flips, so b(u)+b(v) is either J or J+ej. If it has color 5, the difference is J. The linear involution T(x)=x+(∑xi)J maps J to J and J+ei to ei. Therefore f=T∘b is a homomorphism into H, and its generator coloring has the claimed containments.

On every odd cycle every one of the five original colors occurs: otherwise that cycle survives inside a bipartite complement. In particular a 5-cycle is rainbow. In the normalized coloring it is again rainbow by Lemma 2.1. Moving any of its first four colors to color 5 would make that color absent, so no such edge moves. For the more general assertion, if an odd cycle contains exactly one edge uv of color i, the rest of that cycle is an even-length path in G−Ei. Hence bi(u)=bi(v), so the i-th coordinate does not flip and the difference is J+ei before applying T. ∎

### Corollary 3.2: graphs covered by pentagons

If every edge of G belongs to a 5-cycle, then **every** valid original weak-pentagon coloring already has E(G)\Ei equal to an entire cut for each i. Its color counts on all cycles already satisfy Lemma 2.1.

This follows because Theorem 3.1 leaves the entire coloring unchanged. There is also a direct argument: for each i, bipartition G−Ei. Every edge e∈Ei belongs to a rainbow 5-cycle, whose other four edges form an even path between the endpoints of e. Thus e is not in the associated cut; every edge outside Ei is in it.

This is a statement about the original assignment in a restricted graph class, unlike the unrestricted existence equivalence. It permits parity constraints to be applied directly on pentagon-covered graphs. It does not produce the coloring.

## 4. Exact properties needed for extensions

### Lemma 4.1: small neighborhoods and independent sets

H has 16 vertices, degree 5, no triangles, and exactly two common neighbors for any two distinct nonadjacent vertices. Its independence number is 5. Every three distinct pairwise nonadjacent vertices have exactly one common neighbor.

**Proof.** A triangle would give a nonempty relation among three generators, which is impossible. The ten sums of two distinct generators are all distinct and account for every nonzero nongenerator. A nonadjacent pair x,y has difference si+sj for exactly one unordered pair {i,j}; its two common neighbors are x+si and x+sj. Adjacent pairs have none.

For the independent-set assertions, use the equivalent model whose vertices are even subsets of {1,…,5}, adjacent when their symmetric difference has size 4. The five generators are the 4-subsets. They have exactly the same unique relation as S, so the models are linearly isomorphic. Translate an independent set to contain the empty set. Its remaining members must be 2-subsets, and any two must intersect. A pairwise intersecting family of 2-subsets has size at most 4: either all contain one common point (at most four choices), or, after two are {1,2},{1,3}, a member missing 1 must be {2,3}; then no fourth different member can intersect all three. Thus the independent set has size at most 5; a neighborhood attains 5.

For an independent triple translate the first member to the empty set. Relabel the other two as {1,2},{1,3}. A common neighbor must be a 4-subset missing a point of each of these two pairs, so it must miss their common point 1. This gives exactly one common neighbor. ∎

Repeated terminal images cause no problem: one or two distinct pairwise nonadjacent images also have a common neighbor. Thus a partial homomorphism extends over a single vertex of degree at most 3 exactly when its neighbor images are pairwise nonadjacent, allowing equality. Triangle-freeness of the source does not itself force their images to be nonadjacent.

### Lemma 4.2: any two six-sets have a cross edge

For any A,B⊆V(H) with |A|,|B|≥6 there are a∈A,b∈B with ab∈E(H), even when A and B overlap.

**Proof.** Restrict to six-element subsets. Let Q be H's adjacency matrix and 1 the all-ones vector. Lemma 4.1 gives Q²=3I−2Q+2·11ᵀ. Since Q1=5·1, its eigenvalues on 1⊥ are 1 or −3. Set x=1_A−(3/8)1 and y=1_B−(3/8)1. Both have squared norm 15/4. If A,B have no cross edge, then

0=1_AᵀQ1_B=45/4+xᵀQy.

But xᵀQy≥−3||x||||y||=−45/4. Equality forces y into the −3 eigenspace and x=y: equality in the operator-norm bound eliminates the eigenvalue-1 component, and equality in Cauchy–Schwarz gives the same direction. Hence A=B and A is an independent set of size 6, contradicting Lemma 4.1. ∎

The finite verification also obtains the stronger numerical fact that the union of the open neighborhoods of any six vertices has size at least 13. The proof above requires only the weaker consequence that its complement has size at most 5; it does not depend on that exhaustive numerical result.

### Lemma 4.3: walks of prescribed length

A path of length ℓ can be mapped to H with prescribed endpoint images x,y precisely as follows:

- ℓ=1: x,y are adjacent
- ℓ=2: x,y are equal or nonadjacent
- ℓ=3: x≠y
- ℓ≥4: every pair x,y is possible

**Proof.** Endpoint difference is a sum of ℓ generators, with repetition allowed. At length 2 the possible differences are 0 and the ten sums of two distinct generators. At length 3, repetitions give the five generators; three distinct generators sum to the complementary two-generator sum, giving all other nonzero differences and never zero. At length 4, repetitions give 0 and all two-generator sums, and four distinct generators give the fifth generator. Thus every difference occurs. Adding a generator to the full group leaves the full group, so all larger lengths also allow every difference. ∎

In particular, any odd cycle of length at least 5 and every even cycle maps to H. A triangle does not.

## 5. Arbitrary-boundary extension theorems

The terminal vertices in these statements are already colored by a homomorphism on an outside graph. Terminals may coincide. The displayed internal vertices are distinct, have no extra incident edges to be checked, and are uncolored. These hypotheses prevent a tree calculation from being silently applied across unidentified interior vertices.

### Theorem 5.1: a three-arm subdivided claw

Suppose a center v is joined to three terminals t1,t2,t3 by internally disjoint paths of length 2, with internal vertices u1,u2,u3. Every choice of terminal images extends to the center and internal vertices.

**Proof.** If the terminal images are z1,z2,z3, choose h outside N(z1)∪N(z2)∪N(z3). There are at most 15 forbidden vertices among 16. By Lemma 4.3 each h-to-zi pair admits a length-2 walk. Choose these independently as the three arm images. ∎

### Theorem 5.2: two adjacent centers with four subdivided arms

Suppose centers u,v are adjacent, and each has two additional length-2 arms to four terminals. Every assignment of terminal images extends.

**Proof.** If u's terminal images are a1,a2, its allowed center images form A=V(H)\(N(a1)∪N(a2)), a set of size at least 6. Similarly v has an allowed set B of size at least 6. By Lemma 4.2 choose adjacent center images in A,B, and complete all arms by Lemma 4.3. ∎

This remains true if a matching of cross pairs of the four arm-internal vertices is joined instead of going to outside terminals: a cross pair forms a path of length 3 between u and v. In that case each center has fewer outside terminal restrictions, and hence still has at least six possible images. Once the central edge is mapped, the length-3 paths extend because their endpoint images are distinct. Pairs of arm vertices at the same center would form a triangle and are not permitted.

Theorems 5.1–5.2 provide complete local extension rules; unlike a general coloring assertion, they hold for every outside homomorphism. The exact finite checker tests all 256 normalized terminal triples and all 4,096 normalized terminal quadruples. Translation of H makes fixing the first terminal to zero exhaustive.

## 6. A limited critical-graph consequence

A graph is H-critical if it does not map to H but every proper subgraph does. If a triangle-free subcubic counterexample exists, deleting vertices and edges yields such a graph.

### Theorem 6.1: elementary density bound

Every triangle-free subcubic H-critical graph has average degree at least 19/8. Consequently every triangle-free subcubic G with maximum average degree less than 19/8 maps to H.

**Proof.** An H-critical graph is connected, has minimum degree at least 2, and has no cut vertex. Isolated vertices and leaves extend because H has a vertex and no isolated vertices. For a cut vertex, color the smaller pieces separately and use a translation of H on each piece to make the shared vertex's images agree. A degree-2-only component is a cycle and maps by Lemma 4.3, so a critical graph has degree-3 vertices.

A maximal path with internal degree-2 vertices has degree-3 endpoints. It cannot have three or more internal vertices: delete those internal vertices, color the proper remainder, and extend the path, whose length is at least 4. A path returning to the same degree-3 endpoint would create a cut vertex (unless it were the whole degree-2 cycle, already excluded). Thus these paths are ordinary threads with distinct degree-3 endpoints, each having at most two internal vertices.

No degree-3 vertex has three degree-2 neighbors, by Theorem 5.1. Here triangle-freeness ensures its three neighbors are pairwise nonadjacent, so their other endpoints are outside the deleted center and neighbors. Two adjacent degree-3 vertices cannot each have two degree-2 neighbors, by Theorem 5.2 and its cross-pair variant. The four degree-2 neighbors are distinct because a shared one would form a triangle. Edges among them form a matching across the two centers, exactly as covered by that variant.

Let a,b,c count degree-3 vertices with respectively two, one, and zero degree-2 neighbors, and put n3=a+b+c. Let n2 be the number of degree-2 vertices. The total number of incidences from degree-3 vertices to nonempty threads is 2a+b. Each thread uses two such incidences and contains at most two degree-2 vertices, so n2≤2a+b.

Every vertex counted by a has exactly one direct degree-3 neighbor, and that neighbor is not counted by a. Vertices counted by b have only two direct degree-3 incidences, and those counted by c have three. Therefore a≤2b+3c. It follows that

3n2≤6a+3b≤5a+5b+5c=5n3,

where the second inequality uses a≤2b+5c, a consequence of the displayed stronger bound. Hence

(2n2+3n3)/(n2+n3)≥19/8.

Any noncolorable G contains an H-critical subgraph, contradicting mad(G)<19/8. ∎

**Literature limitation.** This is an elementary consequence of the extension lemmas, not a new sparsity frontier. Borodin–Hartke–Ivanova–Kostochka–West, *Circular (5,2)-coloring of sparse graphs* (2008), proves the stronger result that every triangle-free graph with mad<12/5 maps to C5, and hence to H. This is Theorem 5 on printed page 418 of *Siberian Electronic Mathematical Reports* 5 (2008), 417–426; see [the primary journal record](https://www.mathnet.ru/semr116) and [publisher PDF](https://www.mathnet.ru/php/getFT.phtml?jrnid=semr&paperid=116&what=fullt). That result needs no subcubic restriction. Its statement and local preliminaries were inspected; the full proof was not independently audited here. Since 19/8<12/5, our corollary is strictly weaker. In particular none of these density bounds handles the cubic target, whose average degree is 3.

## 7. Two precise obstructions to overstrong reductions

### 7.1 A naive square reconnection does not preserve arbitrary boundary colorings

Delete a square v0v1v2v3, with external terminals t0,t1,t2,t3, and reconnect t0t1 and t2t3. The fact that a homomorphism exists after this reconnection does not imply that this particular homomorphism extends back over the square.

Choose any adjacent x,y in H and assign terminal images (x,y,y,x). Both new edges have valid images. In the original square, v1 and v2 would both have to map into N(y), which is independent, while v1v2 is an edge. This is impossible.

This is a fully explicit obstruction to a boundary-extension claim, **not a counterexample to the weak pentagon conjecture**. The exterior can be just two disjoint edges on four distinct terminal vertices; the restored graph is triangle-free and subcubic. It still has some Clebsch homomorphism. Exhaustive checking finds 961 nonextendible quadruples among the 4,096 quadruples normalized by t0=0, including this obstruction.

### 7.2 Requiring all canonical color classes to be matchings is too strong

K3,3 maps to H by sending its two sides to an edge. But it has no locally injective homomorphism to H. In a locally injective map the three vertices of each part would have three distinct images, and the two image triples would be joined completely. Any two distinct images in one triple would therefore have at least three common neighbors, contrary to Lemma 4.1.

In the generator coloring, distinct incident colors are exactly local injectivity. Therefore K3,3 has no canonical generator coloring in which every color class is a matching. This does **not** say that K3,3 lacks a proper five-color weak-pentagon witness: it is bipartite and every proper edge coloring satisfies the original bipartite-complement condition. Normalization can destroy properness. The distinction between the original and normalized coloring is indispensable.

## 8. Fixed-cut formulation and the exact remaining gap

If M is a specified cut complement, asking that M be exactly color 5 in a canonical witness is equivalent to finding f:V(G)→F2^4 with

- f(u)+f(v)=J on M
- f(u)+f(v)∈{e1,e2,e3,e4} on E(G)\M.

Thus G−M must map to the ordinary cube Q4 with every M-pair mapped to antipodes. This is stronger than the unpinned homomorphism problem and does not follow merely from G−M being bipartite.

The complement M of a maximum cut in a subcubic graph is a matching: if two noncrossing edges were incident to a vertex, flipping that vertex's side would increase the cut. More generally this holds for any cut locally optimal under individual-vertex flips. Any cut complement has odd intersection with every odd cycle, by cut parity. A matching cut complement therefore meets every 5-cycle exactly once.

The unresolved strengthened question is whether **a global maximum-cut complement** always extends as a fixed canonical color class in every triangle-free subcubic graph. Nothing in this packet proves or disproves it. The independent computational investigation of that stronger route is included in [Fixed cut results](FIXED_CUT_RESULTS.md); its finite successes cannot establish the universal statement.

The exact gap to the original conjecture remains: construct a valid canonical generator coloring (equivalently, four disjoint cut complements) for every triangle-free cubic graph, or exhibit one failing graph with a complete certificate. Our extension rules exclude configurations involving degree-2 vertices in a minimal subcubic obstruction, but do not exclude a cubic obstruction. Arbitrary outside assignments can fail even for a square, so the missing global control cannot be replaced by unproved local extendibility.

## 9. Verification, provenance, and next directions

All proofs in Sections 2–8 are written out here; their restricted conclusions do not depend on a downloaded author's program. The original standard-library Python suite constructs the 16-vertex Cayley graph and checks the generator dependency, common-neighbor counts, independence number, independent triples, prescribed-length walk sets, all normalized claw/double-claw terminal cases, and square failures. Its normal-mode results were independently audited. Its assertions are disabled under Python -O and -OO, so optimized executions of that original suite are output reproduction only, not verification. An independent fail-closed audit and a hardened replacement retained all checks in every mode; see [Theory audit](THEORY_AUDIT.md). Programs and machine-generated result files are not distributed in this prose edition. Enumeration corroborates the proofs; it does not extend their scope.

The earlier screen supplied the five-color/Clebsch witness conversion and a Petersen witness. Section 3 reconstructs that conversion and adds the pentagon-rigidity consequence; it does not imply an independent audit of the earlier whole packet. Sections 4–7 were derived and verified in this continuation. They are presented without a claim that they are absent from prior literature. Source inspection levels and the exact downloaded v2 PDF hash are recorded in [Source history](SOURCE_HISTORY.md), [Source scope](SOURCE_SCOPE.md), and SOURCES.json. Source documents, extracted text, and rendered captures are not distributed.

The independent audit is complete, including the equality case in Lemma 4.2 and the overlap handling in Theorem 6.1; its full mathematical review appears in [Theory audit](THEORY_AUDIT.md). Remaining directions are to determine whether the fixed-global-maximum-cut strengthening fails or formulate a useful cut-selection invariant, to use pentagon rigidity to study simultaneous cycle-basis constraints on graphs covered by pentagons, and to seek a replacement for the failed square reduction that explicitly controls the outside coloring rather than requiring arbitrary-boundary extension. These are directions, not additional completed rounds or results.
