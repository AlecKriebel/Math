# Signed degree-choosability dependency audit

12 October 2026 UTC. Scope: Theorem 5.1, the arbitrary-size one-sided matching-complement extension, in the round-two fixed-Clebsch-class candidate for problem 3209 / queue row 1752.

## Verdict and limits

**PASS for the external dependency's statement, conventions, and application in Theorem 5.1.** No substantive gap was found in the signed reduction, its degree saturation, or either excluded obstruction. The external signed degree-choosability theorem remains an explicit mathematical dependency. Reading its primary proof is not a claim to have independently re-proved it.

This is a dependency/application audit, not acceptance of every theorem, program, dataset check, or provenance claim in the candidate packet. It does not establish the full prescribed-cut extension, solve the weak pentagon conjecture, or claim novelty or a complete survey of later literature.

The audited Section 5 was reread after its final wording and bibliographic refinements. Its complete reduction is preserved in [SMALL_COMPLEMENT_PROOFS.md](SMALL_COMPLEMENT_PROOFS.md). This edition does not identify the undistributed original proof bytes. No original candidate file was changed by the audit.

## Primary source and exact dependency

The inspected primary source is Thomas Schweser and Michael Stiebitz, [Degree choosable signed graphs, arXiv:1507.04569v1](https://arxiv.org/abs/1507.04569v1), submitted 16 July 2015, 13:42:15 UTC. The [21-page PDF](https://arxiv.org/pdf/1507.04569v1) and [version-specific HTML](https://arxiv.org/html/1507.04569v1) were read. The PDF has 202,056 bytes and SHA-256:

`727b9d254300f36b91c7ff2e02e1538c259ff0075316da2dfffb454ee2da960e`

The [publisher record](https://www.sciencedirect.com/science/article/pii/S0012365X17300079) identifies *Discrete Mathematics* 340(5), 882–891 (2017), DOI [10.1016/j.disc.2017.01.007](https://doi.org/10.1016/j.disc.2017.01.007). The publisher search result was inspected; direct opens failed. The journal full text and its theorem numbering were not checked. All theorem locators below refer to arXiv v1.

The source's mathematical contract, paraphrased: graphs are finite loopless multigraphs; degree counts edges with multiplicity. Edge signs are ±1, and integer colors satisfy c(u)≠σ(uv)c(v). Lists are arbitrary subsets of the integers. For a connected uncolorable pair with |L(v)|≥d(v), Theorem 2.1(a),(e) forces equality and brick blocks. Bricks are balanced complete graphs, balanced odd cycles, unbalanced even cycles, doubled complete graphs, and doubled odd cycles. Doubling supplies one edge of each sign. Balance means positive cycle products. Switching reverses a cut's signs and negates the switched vertices' colors. The canonical even palette is {±1,…,±h}; its odd counterpart adds zero. Theorem 1.7 characterizes non-degree-choosability by brick blocks.

Locators: conventions pp. 2–4; bricks p. 5; lists and Theorem 1.7 pp. 5–6; uncolorable-pair definition and Theorem 2.1(a) p. 7; part (e) p. 8; proof pp. 8–12; Theorem 1.7's proof and Corollary 2.5 p. 14.

Three v1 typographical slips do not change the needed clauses: the sign-map domain on p. 2 should be E(G); the reduction on p. 7 needs L(u), not L(v); and Theorem 2.1(b) needs “adjacent” before “vertices.” None is imported into the candidate.

## Independent applicability checks

The following reasoning audits the candidate's application rather than presenting a replacement proof of Schweser–Stiebitz.

### 1. The constructed object has the right category

The inherited hypotheses are a finite simple triangle-free graph G of maximum degree at most three, a cut (X,Y), and matching M=E(G)\δ(X), with every M-edge contained in X. Thus Y is independent, and every edge incident with Y belongs to the cut graph B.

Each auxiliary entity is one matching pair in X or one unmatched X-vertex. F is finite. If two distinct neighbors x,z of y represented the same entity, they would be the endpoints of an M-edge and x,y,z would form a triangle. Hence no generated constraint is a loop. This argument also shows that the three neighbors of a degree-three y represent three distinct entities.

The signs are genuinely edge signs. The equation c_P≠(−ε_xε_z)c_Q is equivalent, by multiplication by ε_x, to ε_xc_P≠−ε_zc_Q, exactly the forbidden-antipodes condition. Same-sign parallel constraints are identical predicates, so deduplication preserves the solution set. Opposite-sign parallel constraints must both remain; together they disallow equal absolute color values. Degrees throughout this argument count both such edges.

### 2. The eight-color list assignment is legitimate

C={±1,±2,±3,±4} is an eight-element set of ordinary integers. There is no modular arithmetic, no identification of c with −c, and no zero. The eight even vertices of Q4 form four two-element antipodal orbits; therefore an antipode-compatible bijection θ from C exists.

Every auxiliary vertex receives exactly the fixed list C. Once Δ(F)≤8 is established, each component with these lists satisfies the external theorem's degree-list hypothesis. No conclusion about smaller odd signed-chromatic palettes is used. This matters because an assertion formulated only as χ±≤8 can involve a minimum achieved by a zero-containing odd palette; the present proof directly asks for the required fixed zero-free list.

Switching introduces no hidden restriction: if entity P is reoriented, negating all its ε-values changes precisely its incident edge signs. Negating c_P compensates, and C=−C. More generally, for choices t_P∈{±1}, replacing signs by t_Pσ(PQ)t_Q and colors by t_Pc_P preserves each coloring inequality. Cycle products are unchanged because each t_P occurs twice. Thus a triangle with product −1 cannot be switched into a balanced complete graph. The proof does not require choosing a switching representative or a special orientation of matching pairs.

### 3. Degree bounds and saturation are exact

For an entity P, before same-sign deduplication the number of incident generated constraints is

T(P)=Σ[x∈P] Σ[y∈N_B(x)] (d_B(y)−1).

The no-loop observation ensures that this counts incident constraints as intended. Deduplication gives d_F(P)≤T(P). If P is a singleton, d_B(x)≤3 and d_B(y)−1≤2, so T(P)≤6. If P is a pair, each member has one incident M-edge, hence B-degree at most two, and T(P)≤2·2·2=8.

Suppose now that an uncolorable connected component K exists. Theorem 2.1(a) gives d_K(P)=8 for every entity P. Since K is a component, d_F(P)=d_K(P). Therefore P cannot be a singleton. For a pair,

8=d_F(P)≤T(P)≤2Σ[x∈P]d_B(x)≤8.

Equality forces both members of P to have B-degree two, each adjacent y to have B-degree three, and no same-sign constraint deletion incident with P. In particular there is no unmentioned slack caused by duplicate constraints. The candidate's saturation sentence is valid.

Let S be all original X-vertices represented by K and let R=N_B(S). If y∈R, saturation gives three neighbors of y with distinct entities. A constraint joining its first entity to each other entity survives deduplication. Consequently all three entities are in K, so N_B(y)⊆S. This explicitly verifies the component-closure fact needed by the incidence count.

### 4. Only two degree-eight obstruction types remain

Theorem 2.1(e) gives brick blocks. Every listed brick is regular. If K had a cut vertex, an end block D would have a non-cut vertex whose full degree eight is attained inside D. Regularity would make D eight-regular, so its cut vertex already has degree eight within D and also an edge outside D, contradicting degree eight in K. Thus K is a single brick.

For a complete graph on n vertices the degree is n−1; for a doubled complete graph it is 2(n−1). The cycle bricks have degree two, and the doubled odd-cycle bricks have degree four. Hence the only eight-regular possibilities are balanced K9 and signed 2K5. This conclusion concerns the entire connected component, not merely a block or subgraph.

### 5. The balanced K9 exclusion works under switching

Pick any y adjacent to a represented vertex. Saturation supplies three distinct entities P,Q,R. Their generated signs multiply to

(−ε_xε_z)(−ε_zε_w)(−ε_wε_x)=−1.

In the supposed simple K9 these are its unique edges on the three pairs; the generated constraints cannot disappear entirely during deduplication. Thus K9 contains a cycle with product −1, contradicting balance. This does not confuse a triangle's sign product with the requirement that all its individual edges be negative.

### 6. The doubled K5 exclusion counts original incidences correctly

If K=2K5, its five entities are five disjoint M-pairs, so |S|=10. Every x∈S has B-degree two; therefore |E_B(S,R)|=20. By the closure check above, every y∈R has all three neighbors in S. Thus the same edge set has size 3|R|. The impossible equation 20=3|R| excludes 2K5.

This is an incidence count in the original bipartite graph B. It does not count auxiliary edges, assume an induced component of G, or assume distinct Y-neighborhoods.

### 7. Returning to the cube introduces no new coupling

After coloring each component of F from C, define f(x)=θ(ε_xc_P). Matching endpoints receive antipodal images. Every pair of neighbors of a Y-vertex has non-antipodal images. Each such vertex has at most three neighbors. The candidate's elementary cube lemma then supplies a common neighbor for all their images, including repeated images and empty neighborhoods. That common neighbor has odd parity. The choices are independent because Y has no internal edges under the one-sided assumption.

This last independence fails for matching complements on both cut sides; nothing in this audit extends the theorem to that case. Global maximality of the cut is not needed for the checked argument.

## Corrections and final status

Two presentation refinements identified during inspection are already in the inspected candidate: it refers to the proof in the arXiv manuscript while disclosing that journal full text was not inspected, and it calls the generated cycle a triangle with negative sign product. No further mathematical correction is required by this scoped audit.

The full primary manuscript was read, including the proof of Theorem 2.1. Its result is accepted here as an explicitly cited external theorem, not certified by finite experiments or claimed as independently re-proved. The original reduction and all its use-specific deductions were checked symbolically above. The separate full-packet audit was subsequently accepted; its complete substantive reasoning appears in [SMALL_COMPLEMENT_AUDIT.md](SMALL_COMPLEMENT_AUDIT.md). This dependency report alone should still not be read as full-packet acceptance.

[SOURCES.md](SOURCES.md) records permitted public retrieval, locator, size and digest metadata. The source PDF and extracted text are not distributed.
