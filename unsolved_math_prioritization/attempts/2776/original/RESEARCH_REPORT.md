# KP-2.28: type-preserving right-angled Artin embeddings

## Result and scope

**Status: partial results; the general problem is unresolved in this report.**

For a finite simplicial graph Γ which is not a nontrivial join, the intended question is whether there are an oriented finite-type surface S and an **injective homomorphism** ρ:A(Γ)→Mod(S) taking every intrinsically loxodromic element to a pseudo-Anosov on all of S. The surface may depend on Γ. The requirement is simultaneous for all such elements. It is not enough to produce an embedding, a quasi-isometric embedding, a purely pseudo-Anosov free subgroup, or a map that works on a finite selection of words.

The primary problem is K3, Problem 2.28, printed/PDF pages 108–109 [K3]. Chapter 2 specifies finite-type oriented surfaces by default and allows boundary fixed pointwise. The finite-generator convention for Artin groups appears immediately before the problem. The literal word “map” is interpreted as a group homomorphism, as the adjacent discussion of embeddings requires. A bare injection of sets would make the question trivial: enumerate the countable group and inject it into the nonzero powers of a fixed pseudo-Anosov. We do not claim that set-theoretic observation as a solution.

There are five substantive mathematical routes below:

1. An explicit all-word Schottky construction solves the edgeless-graph case.
2. A direct support-realization attempt gives a finite connected-dominating-set criterion and excludes a common family of local handle constructions for the five-cycle.
3. An anti-tree-factorization attempt fails for a precise reason: every relevant universal-cover diagonal map for a cycle loses a loxodromic element.
4. A free-quotient detection attempt fails on A(P4): an explicit loxodromic element is killed by every homomorphism to every free group, and more generally every group with abelian nontrivial centralizers.
5. An attempt to repair a bad embedding virtually or by finite surface covers cannot remove an existing reducible loxodromic image.

These are construction/reduction/obstruction results, not five independent proofs of the original assertion. Their novelty has not been established; the affirmative free case is classical, and the remaining arguments are elementary consequences or focused obstructions to proposed methods. Literature retrieval, source normalization, and finite checks are not counted as additional mathematical approaches.

## 1. Source dependencies and convention controls

We use the standard presentation A(Γ)=〈V(Γ) | [v,w]=1 when {v,w}∈E(Γ)〉. Write Λ=Γ^op. A *join subgroup* is A(J) where J is an induced nontrivial join subgraph of Γ. We use the intrinsic classification: a nonidentity element is loxodromic if it is not conjugate into a join subgroup. For a cyclically reduced word, this is equivalent to its support not being contained in a join. In the connected, nonjoin, nondegenerate setting, [KMT, Theorems 2.1–2.2] identifies this with the extension-graph and rank-one classifications. For disconnected graphs, we use the intrinsic definition rather than incorrectly assigning a path metric to a disconnected extension graph. All nonidentity elements of a free group are loxodromic in this intrinsic sense.

A positive word has no inverse letters, is cyclically reduced, and has exactly its displayed vertex support. We also use the usual RAAG normal-form criterion: inverse letters can cancel after commuting intervening letters precisely when all those intervening letters commute with that generator. The corresponding circular criterion detects cyclic reduction.

For the support-construction route only, we invoke [R21, Theorems 2–3]: a suitable irredundant collection of pure mapping classes with connected supports generates the expected RAAG after a common sufficiently large power, and the image of a word has pseudo-Anosov dynamics on the subsurface filled by the supports of a cyclically reduced representative. In particular, filling S is sufficient for a pseudo-Anosov on S. The published 2021 version was inspected; its support theorem is absent from the inspected 2020 arXiv version. The exponent threshold is attached to the chosen collection, not a universal constant for arbitrary collections.

Two statements are deliberately not used beyond their verified scope:

- [KMT, Corollary 1.5] is a statement about **finitely generated** subgroups inside an **admissible** RAAG embedding. We do not promote it to arbitrary injective homomorphisms or arbitrary infinitely generated subgroups.
- A pseudo-Anosov centralizer is virtually cyclic in the usual boundaryless finite-type setting. Boundary twists change centralizers when boundary is fixed pointwise. No converse type-preservation argument relying on cyclic centralizers is used for surfaces with boundary.

The list's connected-total-domination wording also needs attention at singleton supports. If v is isolated in Γ, the support {v} is loxodromic intrinsically, while {v} is not a total dominating set in the loopless graph Λ. The exact criterion below uses **closed domination**, which includes this case. For connected support with at least two vertices, closed and total domination agree. This is a convention repair, not a counterexample to the intended problem.

## 2. Route I: an explicit affirmative construction for free groups

### Proposition 2.1
For every finite n≥1 there is an explicitly specified injective homomorphism F_n→SL(2,Z) for which every nonidentity image has absolute trace greater than two. Consequently the edgeless-graph case of KP-2.28 is affirmative, using a once-punctured torus.

### Proof
Let

A = [[34,21],[21,13]],   T = [[1,1],[0,1]],

and define B_i=T^(10i) A T^(-10i), for 0≤i<n. The determinant of A is one. Act on the real projective line by Möbius transformations. Use the intervals

D_+=(3/2,7/4),   D_-=(-3/4,-1/2).

The pole -13/21 of A lies inside D_-. Direct rational evaluation, on the complementary projective interval, gives

A(RP¹ \ D_-) = [8/5,18/11] ⊂ D_+.

Likewise A^(-1)=[[13,-21],[-21,34]] has its pole 34/21 inside D_+, and

A^(-1)(RP¹ \ D_+) = [-7/11,-3/5] ⊂ D_-.

For B_i, translate both intervals by 10i. All 2n intervals have disjoint closures. Attach to the letter B_i its translated plus interval, and to B_i^(-1) its translated minus interval. Each letter sends the complement of its inverse letter's interval into a compact subset of its own interval.

Let W=s_1⋯s_k be a nonempty cyclically reduced word in these 2n letters, with the rightmost letter acting first. Since s_k≠s_1^(-1), the last letter's forbidden interval is disjoint from the closure of D_(s_1). Applying the letter inclusions successively shows

W(cl D_(s_1)) ⊂ int D_(s_1).

Similarly W^(-1) maps cl D_(s_k^(-1)) strictly into its interior. Each of these maps has a fixed point in the corresponding closed interval by the one-dimensional fixed-point theorem. The intervals are disjoint, so W has two distinct real projective fixed points. The strict inclusion also excludes the identity transformation. A nonidentity determinant-one real Möbius transformation with two distinct real fixed points is hyperbolic, so its representing matrix has |trace|>2.

Every nontrivial reduced free word is conjugate to a nonempty cyclically reduced word. Conjugation preserves hyperbolicity. Thus no nontrivial word represents either I or -I, the homomorphism into SL(2,Z) is injective, and every nontrivial image is hyperbolic. The identification Mod(S_(1,1))≅SL(2,Z) makes precisely these matrices pseudo-Anosov. ∎

### What this route does not do
A group in which every nonidentity element is pseudo-Anosov cannot contain a rank-two free abelian subgroup in this boundaryless setting. Thus merely applying the free-group construction to generators does not accommodate the commuting edges in a general RAAG. This route settles the edgeless case and supplies explicit building blocks, but not a gluing theorem for those blocks.

## 3. Route II: direct support realization and a local-gadget obstruction

### Lemma 3.1: the exact finite support criterion
For every nonempty U⊆V(Γ), the following conditions are equivalent:

(a) U is not contained in any nontrivial join subgraph of Γ.

(b) Λ[U] is connected, and every vertex outside U has a Λ-neighbor in U.

In other words, U is a connected dominating set using closed neighborhoods.

### Proof
If Λ[U] is disconnected, divide its components into two nonempty groups. Every cross-pair is adjacent in Γ, so Γ[U] is a nontrivial join. If an outside vertex z has no Λ-neighbor in U, then it is adjacent in Γ to all of U, and Γ[U∪{z}]=Γ[U]*{z} is a join containing U.

Conversely, suppose U lies in J=J_1*J_2 with both factors nonempty. If U meets both factors, Λ[U] is disconnected because there are no Λ-edges between the factors. If U lies entirely in one factor, any vertex of the other factor is outside U and has no Λ-neighbor in U. Thus (b) fails in either case. ∎

Let M(Λ) be the finite family of inclusion-minimal connected dominating sets. Every connected dominating set contains a member of M(Λ), by finite descent. Therefore a support family fills S for every loxodromic support if and only if it fills S for every member of M(Λ). This reduces the infinite word quantifier to a finite family of support tests, but only after a realization satisfying the mapping-class generation hypotheses has been constructed.

### Proposition 3.2: conditional construction and necessary avoidance test
Suppose mapping classes f_v, with connected supports S_v, satisfy the hypotheses of the high-power generation and support theorem [R21] and have disjointness graph Γ. If {S_v:v∈U} fills S for every U∈M(Λ), then sufficiently large common powers give a type-preserving embedding.

Conversely, for any embedding defined by mapping classes supported on these S_v, if some connected dominating set U has an essential nonperipheral curve α disjoint from all S_v with v∈U, that embedding fails the desired type condition.

### Proof
For sufficiency, take a cyclically reduced representative of a loxodromic element and let U be its support. Lemma 3.1 says U is connected dominating, so U contains some minimal member U_0. The supports indexed by U_0 fill S, and hence those indexed by U do as well. The support theorem gives a pseudo-Anosov image. Conjugation does not change the Nielsen–Thurston type.

For necessity, form the positive word w_U containing each vertex of U once, in any order. Its support is U and it is cyclically reduced, hence loxodromic by Lemma 3.1. Each image generator in that word fixes α, so their product fixes α. Its image is reducible, contrary to the requirement. ∎

The same positive word proves that merely increasing all generator powers cannot fix a nonfilling support family. Every powered image still fixes α.

### Corollary 3.3: a five-cycle obstruction to local handles
Let Λ=C_5 and Γ=Λ^op. For any support realization of a type-preserving embedding as above, every essential nonperipheral curve α must essentially intersect supports with labels that are **not a clique in Λ**.

### Proof
The minimal connected dominating sets of C_5 are its five consecutive triples. Any clique has size at most two. For an edge clique, its complementary three vertices form one of those triples. Any singleton clique is contained in an edge clique and therefore also misses a minimal connected dominating set. If α meets supports only with labels in a clique K, choose a minimal connected dominating set U disjoint from K. Then α misses every support indexed by U, contradicting Proposition 3.2. ∎

### Attempt and gap
One natural way to realize an arbitrary intersection graph is to give each vertex a handle and realize edges by disk or strip overlaps away from the handle's essential core. In the five-cycle case the core curve in a private handle meets supports from only one vertex, violating Corollary 3.3. More generally, any essential curve localized to a pairwise overlap labeled by a clique is forbidden.

This is a genuine obstruction to that local construction, not an obstruction to C_5 embeddings in general. Disk overlaps need not carry essential curves, and global arrangements can make every essential curve encounter several support regions. The missing step is a construction of such globally coordinated supports for an arbitrary Λ. The finite hypergraph test does not itself realize a surface.

## 4. Route III: why the anti-tree factorization does not preserve type

[KK15] proves that every RAAG admits a quasi-isometric embedding in an anti-tree RAAG. In the opposite-graph convention G(Λ)=A(Λ^op), its proof constructs a finite subtree T of the universal cover p:Λ̃→Λ and sends a generator v to the product of all vertices of T above v. These factors commute since no two lie adjacent in T.

It is tempting to compose such a map with a type-preserving embedding of the anti-tree RAAG. The needed type-preservation of the intermediate map is false even for cycle complements.

### Proposition 4.1
Let Λ=C_n with n≥5. For every finite subtree T⊂Λ̃ whose vertices meet every fiber label, the diagonal homomorphism

Φ_T:G(C_n)→G(T),   v↦∏_(t∈T, p(t)=v) t,

sends some loxodromic positive word to a nonidentity elliptic element. This holds whether or not Φ_T is injective.

### Proof
The universal cover of C_n is a line. Number the consecutive vertices of T by 0,…,m-1 and relabel the cycle so that p(j)=j mod n. Meeting every fiber forces m≥n.

Set U=V(C_n)\{1,2}. The induced graph C_n[U] is a path with n-2 vertices. It is connected and dominates the two missing vertices: 1 has neighbor 0 and 2 has neighbor 3. By Lemma 3.1, any positive word w using each vertex in U once is loxodromic in G(C_n).

The word Φ_T(w) is positive and has support

W={j∈{0,…,m-1}: j mod n∉{1,2}}.

It contains both vertices 0 and 3, but omits vertices 1 and 2. Consequently T[W] is disconnected. The complement graph on W is therefore a nontrivial join. Thus Φ_T(w) is a nonidentity cyclically reduced element supported in a join subgroup of G(T), and is elliptic. ∎

### What is excluded, and what remains
This proposition excludes the exact universal-cover diagonal factorization as a type-preserving intermediate map for these inputs, including arbitrarily enlarged finite subtrees from the injectivity theorem. It does not exclude a different embedding into an anti-tree RAAG. Nor does it exclude embedding the original cycle-complement RAAG directly into a mapping class group.

The remaining algebraic route would need a new type-preserving intermediate embedding theorem, with support connectivity and domination explicitly tracked. Quasi-isometric embeddedness by itself does not supply this information.

## 5. Route IV: a loxodromic word invisible to all free-group detectors

A second possible strategy is to map a RAAG to free groups, apply the Schottky construction there, and use enough such representations to detect every loxodromic element. The following word prevents even an infinite collection of those detectors from working on A(P4).

### Proposition 5.1
Let

G=〈a,b,c,d | [a,b]=[b,c]=[c,d]=1〉,

with [x,y]=xyx^(-1)y^(-1). Then

w=[[a,c],[b,d]]

is loxodromic in G, but θ(w)=1 for every homomorphism θ:G→F to any free group F. More generally this holds for every target group in which the centralizer of every nonidentity element is abelian.

### Proof: universal vanishing
Write A=θ(a), B=θ(b), C=θ(c), D=θ(d). If B=1 or C=1, one of the two inner commutators is trivial, so θ(w)=1.

Otherwise B and C are nonidentity commuting elements. Since A and C both lie in the abelian centralizer of B, A commutes with C. Likewise B and D both lie in the abelian centralizer of C, so B commutes with D. Thus both inner commutators vanish. In particular the conclusion applies to free groups, whose nonidentity centralizers are cyclic. This argument requires no finiteness assumption on the collection of detectors. ∎

### Proof: loxodromicity
Put x=[a,c]. Since b commutes with both a and c, b commutes with x. Conjugating w by b^(-1) yields

b^(-1)wb = x d b^(-1)d^(-1) x^(-1) d b d^(-1).

On expanding x, the c^(-1) and c enclosing d b^(-1)d^(-1) cancel because c commutes with both b and d. Thus

b^(-1)wb = a c a^(-1) d b^(-1)d^(-1) a c^(-1)a^(-1) d b d^(-1).

Cyclically move the initial a c to the end. The resulting conjugate is

z = a^(-1) d b^(-1)d^(-1) a c^(-1)a^(-1) d b d^(-1) a c.

It is cyclically reduced. To check this directly, consider consecutive occurrences of each generator around the circle:

- The four a-arcs have blockers d, c, d, c, respectively; neither c nor d commutes with a.
- Both arcs between the two b-occurrences contain d, which does not commute with b.
- Both arcs between the two c-occurrences contain a, which does not commute with c.
- The four d-arcs have blockers b, a, b, a, respectively; neither a nor b commutes with d.

Thus no inverse pair can become adjacent by permitted commutations, including across the cyclic end. The support of z is all four vertices. The complement of P4 is the connected path c-a-d-b, so the full support is not a join by Lemma 3.1. Hence z, and therefore w, is loxodromic. ∎

### Consequence and gap
Every map from G into a product of free groups kills w coordinatewise. Therefore no detector family factoring through free groups can distinguish every loxodromic element, irrespective of how Schottky representations are chosen afterward. The same applies to products of any targets with abelian nontrivial centralizers.

Mapping class groups do not satisfy that centralizer condition. The result therefore does **not** obstruct the target embedding itself. A successful construction must retain essential information carried by the commuting-generator configuration, rather than pushing every test into commutative-transitive groups.

## 6. Route V: finite covers and virtual repairs preserve the bad witness

One may try to start with any known RAAG embedding, then pass to a finite cover of the surface or to finite-index data to turn its reducible images into pseudo-Anosovs.

### Proposition 6.1: covering obstruction
Let p:S̃→S be a finite-sheeted unbranched cover of finite-type hyperbolic surfaces. Let f be a reducible mapping class of S, and let f̃ be any lift of some positive power of f. Then f̃ is reducible.

### Proof
Choose a nonempty invariant multicurve C for f. Every component of p^(-1)(C) is an essential nonperipheral simple closed curve. One way to see essentiality and nonperipherality is to equip S with a complete hyperbolic metric with geodesic boundary where applicable: each essential nonperipheral curve has a closed geodesic representative, and each lifted component is a closed geodesic in the lifted metric. Such a geodesic is neither nullhomotopic nor peripheral.

The finite collection p^(-1)(C) is preserved setwise by every lift of every power of f. After discarding duplicate isotopy classes, it is a nonempty multicurve. Therefore the lift is reducible. ∎

The statement concerns unbranched covers without subsequently filling punctures, capping boundary, or forgetting marked points. Those operations can change essentiality and require separate arguments; no impossibility for them is claimed.

### Proposition 6.2: finite-index obstruction
Suppose ρ:A(Γ)→Mod(S) is injective, g is loxodromic, and ρ(g) is reducible. For every finite-index subgroup H≤A(Γ), there is a positive integer k with g^k∈H. That element remains intrinsically loxodromic and its image remains reducible. Thus restriction to finite-index data does not remove the witness.

### Proof
The cyclic action on the finite coset set supplies k>0 with g^k∈H. Positive powers of a cyclically reduced loxodromic element remain cyclically reduced with the same support; conjugation gives the general case. The invariant multicurve of ρ(g) is still invariant under its powers. ∎

For a support realization with a curve disjoint from the support of a loxodromic positive word, the stronger conclusion is immediate: all full inverse-image support configurations still miss the inverse-image multicurve, and all common generator powers still fix the original curve. Thus this repair route must change the actual geometry of the support arrangement, not merely pass to covers, powers, or finite-index subgroups.

## 7. Reproducible checks and their limits

Run `python3 verify_exact.py` in this directory. It uses only the Python standard library and writes `VERIFICATION_RESULTS.json`.

The checked edition verifies:

- The graph criterion on all 1,099 labeled graphs with one through five vertices, testing all 32,767 nonempty vertex subsets against an independently enumerated join predicate.
- 616 cycle-cover examples, n=5,…,20 and n≤|T|≤4n, with loxodromic source support and disconnected lifted support.
- The P4 word's explicit 12-letter cyclically reduced conjugate, its full support, and every circular inverse-pair obstruction. An exhaustive commutation/cancellation/rotation search visits 2,308 states and finds minimum length 12.
- The exact rational Schottky interval inclusions, determinant-one condition, and hyperbolicity of 3,918 cyclically reduced words of lengths at most five in the three-generator sample. The least sampled absolute trace is 47.
- The five minimal dominating triples of C5 and the absence of a clique transversal.

The general statements are proved above. Finite enumeration alone establishes none of the unbounded universal claims. The finite-cover theorem is not computationally tested. No empirical search over a bounded list of embeddings is presented as an obstruction to all embeddings.

## 8. Remaining problem and acceptable conclusions

The report proves a classical affirmative subclass and focused failures of four concrete extension strategies. It provides no graph for which every possible homomorphism fails. It also provides no surface-support construction for an arbitrary finite nonjoin graph.

A full affirmative result still needs an injective homomorphism with simultaneous type control on every loxodromic support. Within the high-power-support method, this means realizing the prescribed disjointness graph and ensuring the filling condition for every minimal connected dominating set, with singleton supports treated when present. A full negative result must obstruct **all** embeddings for some graph, rather than the selected constructions analyzed here.

The appropriate disposition is **partial / unresolved after five mathematical approaches**, subject to independent mathematical review. It is not solved, refuted, verified-prior-solution, or merely a literature-only pass.

## References

[K3] R. İnanç Baykur, Robion C. Kirby, and Daniel Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, author-hosted preliminary version available with AMS permission, 2026, Problem 2.28, pp.108–109; Chapter 2 conventions p.84. https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf

[KMT] Thomas Koberda, Johanna Mangahas, and Samuel J. Taylor, *The geometry of purely loxodromic subgroups of right-angled Artin groups*, Transactions of the American Mathematical Society 369 (2017), 8179–8208. https://doi.org/10.1090/tran/6933 ; inspected author-hosted version: https://www.nsm.buffalo.edu/~mangahas/files/KMT_transactions.pdf

[R21] Ian Runnels, *Effective generation of right-angled Artin groups in mapping class groups*, Geometriae Dedicata 214 (2021), 277–294, Theorems 2–3. https://doi.org/10.1007/s10711-021-00615-0 ; inspected published article: https://par.nsf.gov/servlets/purl/10232333

[KK15] Sang-hyun Kim and Thomas Koberda, *Anti-trees and right-angled Artin subgroups of braid groups*, Geometry & Topology 19 (2015), 3289–3306. https://doi.org/10.2140/gt.2015.19.3289 ; inspected preprint: https://arxiv.org/abs/1312.6465

Additional screened literature and the unverified full-text thesis lead are recorded in `LITERATURE_AND_SCOPE.md`. No third-party source documents or source extracts are included in this packet.
