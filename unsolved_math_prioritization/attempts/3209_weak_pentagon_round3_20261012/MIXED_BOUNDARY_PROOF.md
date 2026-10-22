> Editorial scope: This is the complete authored text of the accepted third-round source document, with operational identities and reproduction directions editorially removed or relabeled. Mathematical arguments and finite-scope counts are preserved. References to candidate status, packet contents, or narrower review scope record the original stage; the final combined decision is in [ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md). This public edition contains prose and public verification metadata only. It contains no programs, raw certificates, dataset contents, source documents, or runnable bundle. Original and distributed identities are different; [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) identifies only the files actually distributed.

# Mixed prescribed Clebsch classes: a boundary theorem and a one-versus-many obstruction

12 October 2026 UTC. Weak pentagon problem, queue row 1752 / problem 3209. **Authored third-continuation candidate for independent audit.** No novelty claim is made. This is not a solution or counterexample to the unrestricted Weak pentagon conjecture.

## 1. Results

Let G be a finite simple triangle-free subcubic graph with a specified cut (X,Y). Write B=δ(X), and suppose M=E(G)\B is a matching. A prescribed extension is a map f:V(G)→F₂⁴ whose differences are unit vectors on B and J=1111 on M. Throughout the mixed case there is exactly one edge rs of M in Y; arbitrarily many edges of M may lie in X.

This packet proves:

1. An exact signed-list reduction with lists of size eight except at at most four boundary entities, whose lists have size four. Only paired boundary entities meeting {r,s} once can have degree larger than their list size; their degrees are at most six.
2. A positive mixed theorem: the specified cut extends whenever every boundary entity has degree at most four in the reduction. In particular it extends if every X-demand that meets N_B(r)∪N_B(s) meets it at both endpoints. There is no bound on the number of X-demands.
3. The general one-versus-many extension is **false**, even for triangle-free cubic graphs: an explicit 18-vertex subcubic obstruction has five X-demands and one Y-demand; an explicit 28-vertex cubic completion has seven X-demands and one Y-demand.
4. Both obstructed cuts are nonglobal. A sealed three-vertex switch already improves either cut. Independent direct checks give maximum cuts 22 and 35, respectively, against prescribed cut sizes 20 and 34. Explicit unrestricted Clebsch homomorphisms are supplied for both graphs.

The negative proof is an elementary antipodal-pair pigeonhole argument. It is independent of the external signed-choosability theorem used for result 2. The subcubic obstruction has exactly four deficient boundary entities, each of degree five with a four-element list. Thus permitting degree five at four boundary entities already invalidates the unrestricted positive extension of the criterion.

The original target concerns unrestricted homomorphisms to the Clebsch graph. Prescribing M as one canonical difference class is stronger; failure of that prescription does not refute the original target. Background: DeVos–Šámal, [High-girth cubic graphs are homomorphic to the Clebsch graph, arXiv:math/0602580v2](https://arxiv.org/abs/math/0602580v2).

## 2. Cube facts and exact reduction

The four-dimensional cube Q₄ has vertices F₂⁴ and unit-vector differences. Its two parity classes each split into four antipodal pairs {a,a+J}. At most three vertices of one parity have a common cube neighbor exactly when no two are antipodal. For the nontrivial direction, translate one to zero; the other distinct vertices have two-element supports, which intersect unless they are antipodal. A coordinate in the intersection gives a common neighbor. Repetitions and smaller sets cause no difficulty.

For any odd vertex h, N(h) contains exactly one vertex from each even antipodal pair, and N(h+J)=N(h)+J. Fix a bijection θ from C={±1,±2,±3,±4} to the even vertices such that θ(−a)=θ(a)+J and θ({1,2,3,4})=N(h). Write D={1,2,3,4}.

### Entities, signs, and lists

Contract each X-edge of M to one entity; each unmatched X-vertex is a singleton entity. Denote the entity of x by P(x). Choose signs ε_x=±1 opposite at endpoints of each contracted pair, and +1 at singleton vertices. An entity color c_P∈C represents the cube image θ(ε_x c_P) at x.

For every y∈Y\{r,s} and each pair of distinct neighbors x,z∈N_B(y), put a signed edge between P(x),P(z), with sign

σ(P(x)P(z))=−ε_x ε_z.

Delete repeated copies of the same signed edge; retain a pair of opposite-sign edges. Call the resulting signed multigraph F. There are no loops: two members of one X-demand cannot share a Y-neighbor without creating a triangle. Its signed-coloring convention is c_P≠σ(PQ)c_Q. Thus its constraints say exactly that two X-neighbors of an ordinary Y-vertex do not have antipodal images.

Let R=N_B(r), T=N_B(s). These sets are disjoint, since a common member would form a triangle with rs. Neither set contains both members of an X-demand. A boundary entity is one containing a member of R∪T. For x in this union prescribe

c_{P(x)}∈(t_x ε_x)D, where t_x=+1 on R and −1 on T.

These prescriptions agree if two boundary vertices represent the same entity: one then belongs to R and the other to T, and their ε-signs are opposite. Define L(P) to be this four-element list at a boundary entity, and C otherwise. There are at most |R|+|T|≤4 boundary entities.

### Proposition 2.1: exact list equivalence

The prescribed cut has an extension if and only if F has an L-coloring.

**Proof.** Given an L-coloring, map x∈X to θ(ε_x c_{P(x)}). Matching partners are antipodal. Every ordinary Y-neighborhood has at most three images and no antipodal pair, so choose its image by the cube fact. Put f(r)=h and f(s)=h+J. The boundary lists ensure adjacency to these values.

Conversely, in each connected component of G, parity of f(v) differs from the specified cut parity by a constant: B-edges change both parities, and M-edges change neither. Translate component images to make every X-image even. In the component containing rs, a further even translation takes f(r) to h and hence f(s) to h+J. Apply θ⁻¹ to the X-images, incorporating ε_x, to obtain entity colors. Cube adjacency forbids antipodal pairs at ordinary Y-neighborhoods; adjacency to h and h+J gives precisely the boundary lists. Components not containing rs impose no boundary conditions. ∎

A singleton has degree at most six in F. A pair has degree at most eight. More precisely, if k is the number of incidences of an entity's members with {r,s}, then

- a singleton has degree at most 2(3−k);
- a pair has degree at most 2(4−k).

Here k is zero or one for a singleton and zero, one, or two for a pair. Each remaining incidence contributes at most two constraints; same-sign deduplication can only lower degree. Therefore unconstrained vertices satisfy |L|≥degree, constrained singletons do too, and a constrained pair with k=2 does too. Only a constrained pair with k=1 can have degree five or six against a list of size four.

### Proposition 2.2: equivalent full-palette reduction

An alternative exact reduction adds to F the constraints generated by all pairs of the transformed boundary roles a_x c_{P(x)}, where a_x=t_x ε_x. The sign for two roles is −a_x a_z. Same-entity constraints are vacuous: the roles have equal a-signs, so they only forbid c_P=−c_P, impossible in C. Deduplicate as above; call the result F⁺. Then the cut extends exactly when F⁺ is C-colorable.

Indeed, the added constraints say that the transformed boundary colors contain no opposite pair. Any such set can be taken into D by independently flipping the names +i and −i for each absolute color i. Such a relabeling preserves every signed-coloring constraint: equality c_P=σc_Q depends only on colors of the same absolute value. It gives an L-coloring of F, and the reverse implication is immediate. This is also an exact way to separate the residual from a merely sufficient coloring condition.

In particular a boundary singleton has degree at most seven in F⁺, and a paired entity with one boundary incidence has degree at most nine. Thus ordinary eight-color degree choosability cannot simply be invoked on F⁺ without further work.

## 3. A positive mixed boundary theorem

### Explicit external dependency

We use Schweser–Stiebitz, [Degree choosable signed graphs, arXiv:1507.04569v1](https://arxiv.org/abs/1507.04569v1), Theorem 2.1(a),(c),(e) and Lemma 2.4, with the source's loopless signed-multigraph conventions. A connected uncolorable degree-list pair has lists of exactly the degrees and brick blocks. Each block inherits an uncolorable list pair, with the original lists at its non-cut vertices. Bricks are balanced complete graphs, balanced odd cycles, unbalanced even cycles, doubled complete graphs, and doubled odd cycles. Each brick is regular. Theorem 2.1(c) gives edgewise block-list compatibility: opposite-sign parallel edges force symmetric lists at their endpoints.

The theorem and these additional list-structure clauses were read in the primary v1 manuscript, pp. 7–8 and 13. Their complete proof remains an explicit external dependency, not an independent proof by this packet. The prior scoped audit covered Theorem 2.1(a),(e) for the one-sided argument; the additional clauses used here received the complete scoped application review reproduced in SIGNED_DEPENDENCY_AUDIT.md. The journal identity is *Discrete Mathematics* 340(5), 882–891 (2017), [DOI 10.1016/j.disc.2017.01.007](https://doi.org/10.1016/j.disc.2017.01.007); this packet uses v1's numbering, not an uninspected journal theorem locator.

### Theorem 3.1

If every boundary entity has degree at most four in F, then the specified mixed cut extends.

**Proof.** Every list has size at least its entity's degree. Suppose a connected component K is uncolorable. The external theorem forces exact degrees and brick blocks. Thus every vertex has degree four or eight. A degree-four vertex is a boundary entity, with nonsymmetric list D or −D. A degree-eight vertex is an unconstrained pair; an unconstrained singleton has degree at most six and could not have exact degree eight.

Choose an end block Q, or K itself if K has only one block. Every non-cut vertex of Q has its full degree inside Q. Regularity of bricks implies that Q has degree four or eight.

If Q has degree eight and has a cut vertex, that vertex already has eight edges in Q and an edge outside it, contradicting Δ(F)≤8. Thus K=Q is an eight-regular brick. Its possible types are balanced K₉ and 2K₅. Every vertex is an unconstrained pair. Equality in the degree bound forces all four ordinary Y-incidences of every pair to be present, each at a degree-three Y-vertex, with no repeated same-sign constraints deleted. The three entities at such a Y-vertex generate a triangle whose sign product is −1. This excludes balanced K₉. If K=2K₅, its five pairs represent ten X-vertices of ordinary B-degree two. Every adjacent ordinary Y-vertex has three neighbors among those ten vertices, because its generated constraints keep their entities in K. The impossible incidence equation 20=3|N_B(X_K)| excludes 2K₅.

Now suppose Q has degree four. At every non-cut vertex of Q its inherited block list equals the nonsymmetric original list D or −D. Hence Q cannot be a doubled brick: its positive and negative parallel edges at such a vertex P force both L_Q(P)=L_Q(P′) and L_Q(P)=−L_Q(P′), so L_Q(P) would be symmetric. The only remaining degree-four brick is a balanced K₅.

Let P be a non-cut vertex of this K₅. It is a boundary entity. If it is a pair, at least one of its at most four X-to-Y incidences was removed with r,s, so at most three ordinary incidences remain. If it is a singleton, at most two remain. If all these Y-vertices had degree at most two, P would have degree at most three in F. Since its degree is four, at least one incident ordinary Y-vertex has degree three. Its three distinct entities generate a triangle of sign product −1. Both edges of this triangle at P belong to Q; the whole triangle, being a cycle, lies in the same block. This contradicts balance of K₅.

Every possible end block has been excluded. Thus no uncolorable K exists. Proposition 2.1 supplies the prescribed extension. ∎

### Corollary 3.2: paired-complete boundary

The cut extends if every X-demand meeting R∪T has both endpoints in R∪T. Necessarily one endpoint then lies in R and the other in T. Constrained pairs have k=2 and degree at most four; constrained singletons have degree at most four. The theorem applies.

This includes the case in which all neighbors of r and s are unmatched in X. It is a genuinely mixed theorem with arbitrarily many X-demands, not a small-|M| statement. For example, arbitrarily many pentagons with their sole demands on X can be joined by cut bridges to a pentagon whose sole demand is rs on Y, using distinct degree-two vertices for the bridges and avoiding the neighbors of r,s. The resulting connected triangle-free subcubic graphs have arbitrarily many X-demands and satisfy the boundary hypothesis. The theorem also applies to graphs without this particular block structure.

## 4. An explicit one-versus-many obstruction

### Graph H on 18 vertices

Let X={0,…,9}, Y={10,…,17}. The matching is

M={(0,1),(2,3),(4,5),(6,7),(8,9),(10,11)}.

The complete list of cut neighborhoods is:

- N_B(10)={0,2}, N_B(11)={5,7};
- N_B(12)={8,1,2}, N_B(13)={8,3,4};
- N_B(14)={9,4,7}, N_B(15)={9,6,1};
- N_B(16)={0,5}, N_B(17)={3,6}.

Thus H has 26 edges, 20 of them cut edges. All vertices have degree three except 16 and 17, which have degree two. It is connected and simple. The cut part is bipartite. No Y-neighborhood contains both endpoints of an X-demand, and 10,11 have disjoint cut neighborhoods, so no triangle can contain a matching edge. Hence H is triangle-free.

### Proposition 4.1: the specified cut has no extension

**Proof.** Suppose an extension exists. All X-images have the same parity; translate to make it even. Set

A=f(0), B=f(2), C=f(4), D=f(6), E=f(8).

Their matching partners have images A+J, B+J, C+J, D+J, E+J. Write h=f(10), so f(11)=h+J. Adjacency at 10 shows A,B∈N(h). Adjacency at 11 gives C+J,D+J∈N(h+J), hence C,D∈N(h). Therefore A,B,C,D contain no antipodal pair.

The ordinary Y-neighborhoods make these four images pairwise distinct:

- 12 forbids A=B; 13 forbids B=C;
- 14 forbids C=D; 15 forbids D=A;
- 16 forbids A=C; 17 forbids B=D.

For example, A=B would put the antipodal images A+J and B at the two neighbors 1,2 of 12, which is impossible. The other five cases are the same direct two-step cube-distance obstruction.

Consequently A,B,C,D occupy all four even antipodal pairs. But the neighborhoods at 12–15 exclude both members of each of these pairs as the value of E:

- 12 excludes E=A and E=B+J;
- 13 excludes E=B and E=C+J;
- 14 excludes E=C and E=D+J;
- 15 excludes E=D and E=A+J.

These are all eight even vertices. No value of E remains, a contradiction. ∎

Equivalently, using entities A,…,E with positive representatives 0,2,4,6,8, the ordinary signed graph F has degree sequence (5,5,5,5,8) and lists D,D,D,D,C. The boundary lists supply all negative constraints among A,B,C,D. The ordinary Y-neighborhoods supply all positive constraints among these four and both signs from each of them to E. Thus the full-palette reduction F⁺ is exactly signed 2K₅. This is an independently checkable certificate, not a solver's bare UNSAT output.

The cube proof does not assume that any four pairwise non-antipodal even labels always have a common neighbor. Their common neighbor here is the already prescribed image h.

## 5. A cubic completion with seven X-demands and one Y-demand

Retain all of H, including its cut and matching statuses. Add X-vertices 18,…,23 and Y-vertices 24,…,27. Add X-demands (18,19),(20,21), cut edges (16,22),(17,23), and cut neighborhoods

- N_B(24)={18,20,22}, N_B(25)={18,21,23};
- N_B(26)={19,20,23}, N_B(27)={19,21,22}.

Call the resulting graph K. It has 28 vertices, 42 edges, and exactly seven X-demands and one Y-demand. Every vertex has degree three. The newly added Y-neighborhoods never contain both members of a demand, and the old neighborhoods are unchanged except for the two new bridges at 16,17. Thus K is connected, simple and triangle-free. Its specified cut has size 34.

Any prescribed extension of K would restrict to an extension of H. Proposition 4.1 therefore rules it out. No assumption about finite catalog completeness or a search heuristic is needed.

The two new matching pairs together with four degree-three Y-neighborhoods form an explicit completion gadget. This is a direct authored construction; it does not rely on a claim that every subcubic graph can be completed with a chosen side distribution.

## 6. Scope certificates: nonglobal cuts and unrestricted witnesses

### A sealed improving switch

In both graphs U={0,2,10} has matching boundary {(0,1),(2,3),(10,11)}, of size three, and cut boundary {(0,16),(2,12)}, of size two. Switching U gains one cut edge. All three vertices already have degree three in H, so the same certificate persists in K. In particular neither obstructed cut is globally maximum. The obstruction does not survive as a claim about an arbitrary maximum-cut complement.

### Exact maximum-cut counts

The verifier enumerates the 2¹⁷ cuts of H normalized by vertex 0 having color zero. Separating according to equality of the port colors at 16 and 17 gives:

- equal ports: maximum 21, attained by 30 normalized cuts;
- unequal ports: maximum 22, attained by 7 normalized cuts.

Thus maxcut(H)=22. In the completion gadget, including its two attachment edges, enumerate all 2¹⁰ choices for the new vertices with port 16 fixed to zero. The results are:

- equal ports: maximum 14, attained by 1 assignment;
- unequal ports: maximum 13, attained by 6 assignments.

Complementing all colors shows that these values depend only on port equality, not their individual colors. The old and new edge sets partition E(K), with only the port colors shared. Therefore

maxcut(K)=max(21+14,22+13)=35,

and its number of normalized maximum cuts is 30·1+7·6=72. This establishes exact global optimality by a small separated enumeration, rather than relying on a heuristic or on all 2²⁷ cuts being searched. Direct cut certificates of sizes 22 and 35 are retained and checked. The counts are properties of these two authored graphs only.

### Unrestricted Clebsch homomorphisms

The Clebsch graph permits differences 1,2,4,8,15. The following label lists, in vertex order, are explicit unrestricted witnesses:

H:
(0,1,6,2,1,5,4,11,8,7,2,10,9,0,3,5,1,0).

K:
(0,1,6,2,1,5,4,11,8,7,2,10,9,0,3,5,1,0,6,7,10,11,0,1,2,9,5,15).

Independent computational testing produced these witness values; this packet checks every edge directly against the permitted difference set. The values are authored computational witnesses, not external dataset contents. They certify explicitly that these particular graphs are not counterexamples to the unrestricted target.

## 7. Verification contract and unresolved frontier

The mathematical proofs above are universal deductions where stated. Finite computation checks only the two explicit graphs, their signed reductions, their unrestricted witnesses, exact maximum cuts, and small cube facts used in the proofs. No sampled or catalog graph is needed as a premise.

The original graph verifier validates byte-count/SHA-256-pinned graph inputs, graph structure and exact demands, the complete signed 2K₅ certificate on H, the four degree-five boundary deficiencies, the sealed switch, the two unrestricted witnesses, and the factorized maximum-cut enumerations. All checks use explicit exceptions, not Python assert, and run under normal Python, -O, and -OO. Deliberate digest, graph, witness, and false-target mutations must be rejected. The original program and graph inputs were frozen outside this public edition. Source PDF/text remain outside this packet; only public titles, URLs, exact dependency locators, hashes and inspection metadata are included.

What remains open in this work is the full Weak pentagon target and the proposed strengthening for every global maximum-cut complement. The present result definitively closes the unrestricted one-versus-many prescribed-cut strategy: even a unique demand on one side does not suffice. A universal theorem for the smaller distribution 4+1 was outside this source report; the accepted complementary elementary theorem is supplied in ONE_VERSUS_FOUR_PROOF.md and ONE_VERSUS_FOUR_AUDIT.md in this edition. The exact four-boundary signed-list formulation remains available for more constrained cases, particularly when global cut optimality forbids the local patterns present in the obstruction.
