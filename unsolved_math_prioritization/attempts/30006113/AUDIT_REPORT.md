# Source-credit audit: the strong-density FVS extreme-point question

## Decision and exact scope

**Accepted, with the explicit minor corrections below.** Theorem 1 of Karthekeyan Chandrasekaran, Chandra Chekuri, and Shubhang Kulkarni, *An iterative rounding 2-approximation for Feedback Vertex Set via AI-assisted proof of an extreme point property*, arXiv:2609.04414v1 (3 September 2026), supplies an affirmative resolution of the precise strong-density extreme-point question. Its proof in Section 2 is complete after replacing one incorrect termination measure and correcting two incidental displayed/prose slips. None of these changes requires a new mathematical idea or a conjectural imported theorem. The upper bounds in its definition do not prevent transfer to the original formulation.

This is an independent mathematical source audit, not human peer review, formal proof certification, or a claim that the preprint has been refereed. The authors disclose AI assistance. The public arXiv landing pages checked on 10 October 2026 list v1 and the three authors; no later version or journal acceptance was established. Source credit belongs to those authors, with the question attributed to Fiorini. This audit does not claim a new solution.

The accepted statement is as follows. Let G=(V,E) be a finite undirected simple loopless graph containing a cycle. Define

P = {x in R^V : x>=0 and sum over u in S of (d_S(u)-1)x_u >= |E[S]|-|S|+1 for every S subset V with E[S] nonempty}.

Then every extreme point x of P has **at least one** coordinate x_u>=1/2. No cost vector or optimum qualification restricts this statement. Disconnected graphs and isolated vertices are allowed. No assertion about multigraphs, loops, every coordinate being half-integral, or the ordinary cycle-cover LP is accepted.

The IDs 30004905, 30006113, and 30006114 represent one underlying Fiorini question; the last is commentary rather than a separate problem.

## 1. Source identity and formulation comparison

The original Fiorini report, OWR 53/2021, printed page 2944 (PDF page 52), visibly gives nonnegativity and the induced-subgraph inequalities, without upper bounds. The later published paper by Chandrasekaran, Chekuri, Fiorini, Kulkarni, and Weltge, *Polyhedral aspects of feedback vertex set and pseudoforest deletion set*, Eq. (1), PDF page 4, has the same nonnegative formulation. Its Conjecture 1 adds the cycle qualification. The 2024 workshop report, published subsequently, reiterates the still-unresolved question at that time.

The September 2026 preprint's Definition 1, PDF page 2 (printed page 1), instead has x in [0,1]^V. Its Theorem 1, PDF page 3, concerns every extreme point of that bounded polytope. The default graph conventions in Section 1.1 are finite, undirected, simple, and loopless. The only inequality change is the explicit upper bound: the subset quantifier, induced degree coefficients, nonempty-edge qualification, and right side all match.

The four inspected source PDFs were rehashed and matched their recorded SHA-256 and byte-count identities. Public source metadata, historical inspection scope and a summary of supplementary exact-arithmetic controls are recorded in SOURCE_METADATA.json. The complete mathematical audit and corrections are preserved in this edition. ACCEPTANCE.json distinguishes the original accepted document identities from the distributed bytes, and MANIFEST.json hashes the other seven public files. Third-party PDFs, extracted source text, rendered source pages, datasets, programs, generated certificates, raw outputs and private coordination material are excluded.

## 2. Bounded-to-original transfer

Write B=P intersect [0,1]^V, exactly the preprint's Definition 1. Suppose an extreme point x of P violated the desired conclusion. Then 0<=x_u<1/2 for every u, so x belongs to B.

If x=lambda y+(1-lambda)z for y,z in B and 0<lambda<1, then y,z also belong to P. Extremality in P forces y=z=x. Therefore x is an extreme point of B. The preprint's Theorem 1 contradicts x_u<1/2 for every u.

This argument uses only subset inclusion and candidate membership. It does not assume that every vertex of B is a vertex of P, that truncating arbitrary feasible points preserves feasibility, that P is coordinatewise monotone, or that the two polyhedra are equal. If an extreme point of P already has a coordinate above 1, the requested conclusion holds immediately. The transfer therefore covers **all** extreme points of the original formulation.

## 3. Complete dependency audit of Theorem 1

The audited proof is Section 2, printed pages 6-16, including Proposition 1, Lemmas 1-8, Theorem 3, both corollaries, and the final counting contradiction. All nontrivial combinatorial ingredients are proved there. The cited older conditional-supermodularity observation is reproved rather than imported without proof. Jain's method and the iterative-rounding literature are motivation, not additional assumptions needed for this theorem.

### 3.1 Active constraints and cycles

Assume for contradiction that x is extreme in B and all its coordinates are below 1/2. Let Z be the zero coordinates and p=|V|-|Z|. Upper-bound constraints are inactive. The active induced-subgraph rows together with the unit rows indexed by Z span R^V. This standard rank criterion can be seen directly: a nonzero vector perpendicular to all active rows permits both sufficiently small positive and negative perturbations, because there are finitely many inequalities and all inactive ones have positive slack. This would contradict extremality. Conversely, a full-rank active set forces any feasible decomposition to agree in every coordinate. The independent unit rows for Z can be extended to a full basis using active density rows.

Every cycle has a chordless subcycle. On its vertex set the density inequality is sum x_u>=1, so a graph with a cycle has at least three positive coordinates under the strict half bound. This also applies to every cyclic induced subgraph. Nonnegativity is essential when passing from a chordless subcycle to its containing cycle.

For a vertex subset S write r(S)_u=d_S(u)-1 on S and zero off S, b(S)=|E[S]|-|S|+1, and

f(S)=b(S)-r(S)x = sum over uv in E[S] of (1-x_u-x_v) - sum over u in S of (1-x_u) + 1.

An edge-bearing set is tight exactly when f(S)=0. No inequality for an edgeless set is silently inserted.

### 3.2 Conditional supermodularity and exact row uncrossing

Set w_uv=1-x_u-x_v>0. The function S -> sum over E[S] of w_uv is supermodular; the remaining terms in f are modular. The supermodular defect for A,B is the total w-weight of edges between A\B and B\A.

If two tight sets meet in at least two vertices but their intersection I is edgeless, then f(I)=1-|I|+x(I)<1-|I|/2<=0. Their union contains an edge and has f<=0. Supermodularity would give 0<=f(I)+f(A union B)<0, impossible. Thus the intersection has an edge. Feasibility then applies to both intersection and union and forces both to be tight. Equality in supermodularity, together with strictly positive w, forces **no crossing edges** between the two differences.

Consequently r(A)+r(B)=r(A intersection B)+r(A union B), coordinatewise. At a vertex of the intersection, the correct degree expansion counts neighbors in the intersection twice. At a vertex of either difference, the absence of crossing edges gives the desired equality. This verifies all uncrossing hypotheses, including strictness and the nonempty-edge domain.

### 3.3 Spanning by an almost-laminar family

Choose an almost-laminar family L of tight sets with independent rows and maximum cardinality. Here incomparable members meet in at most one vertex. Let W be its row span and Q the span of all tight density rows.

If W were a proper subspace of Q, choose a largest tight A whose row is outside W. A must cross a member of L in at least two vertices; choose an inclusion-minimal such member B. Uncrossing gives tight I=A intersection B and U=A union B with the row identity. Since U is larger than A, its row is in W; hence the row of I is outside W.

To check that I can be adjoined to L: a member T containing B contains I; a member meeting B in at most one vertex meets I in at most one vertex; and a proper member T of B cannot cross I in at least two vertices, since then T would be a smaller choice than B for crossing A. This exhausts the cases. Adding I contradicts maximum cardinality, so W=Q.

Choose a maximal subfamily whose rows remain independent together with all zero-coordinate unit rows. The combined span is R^V by the active-rank criterion. Therefore |L|=p. Removing members preserves almost-laminarity. No unsupported general laminar-basis theorem is being invoked.

### 3.4 Connected and cyclic members; refinement

A tight edge-bearing set cannot have an isolated vertex v: deleting it leaves an edge and changes the slack by -(1-x_v), producing a violated inequality. A disconnected edge-bearing set with k>=2 components cannot be tight, because component feasibility gives r(S)x>=b(S)+(k-1). This is the precise k-component version of the source's abbreviated two-component wording.

A tree member has b=0. Since its row is nonnegative, tightness forces all its positive-coefficient coordinates to be zero coordinates of x. Its row is then in the span of the zero-unit rows, contradicting basis independence. Every basis member is therefore connected and cyclic.

For an inclusion-minimal member S that is not 2-connected, split at a cut vertex v into S1,S2 with intersection {v}, both containing edges. Direct counting gives r(S)=r(S1)+r(S2)+e_v and b(S)=b(S1)+b(S2). Tightness and nonnegative slacks force x_v=0 and tightness of both pieces. At least one piece's row lies outside the span of the other basis rows and the zero-unit rows; replace S by it. This preserves rank and the number of rows.

Almost-laminarity is preserved. Members incomparable with S meet the replacement in at most one vertex; supersets contain it. A proper member inside S is already 2-connected by minimality, so it cannot cross both sides of the cut vertex. It is contained in one side and meets the other in at most {v}.

**Correction:** the source's proposed total-cut-vertex measure need not strictly decrease. The valid integer measure is sum over members T of |T|. Every replacement is a proper subset of S, so this sum strictly decreases. The process terminates, and the resulting basis consists of 2-connected cyclic members, each with at least three support vertices.

### 3.5 Strict support growth along containment

For A properly contained in B in the refined family, suppose all coordinates on D=B\A vanish. Let ell be the number of edges between A and D. Since G[B] is 2-connected, ell>0 and every vertex in B has degree at least two. Subtracting the two tight equalities gives

ell + |E[D]| - |D| = sum over crossing edges uv, u in A, of x_u < ell/2.

But summing degrees over D gives 2|E[D]|+ell>=2|D|. These inequalities contradict one another. Thus B\A contains a new positive coordinate. The source uses the stronger ell>=2, which is valid but unnecessary.

### 3.6 Forest structure and the sharing bound

Every member has at least three vertices. If it had two incomparable minimal supersets, those supersets would meet in at least three vertices, contradicting almost-laminarity. Thus the containment diagram is a rooted forest. Let there be t roots R_i, with k_i members in the respective trees. Every positive coordinate occurs in a root: otherwise every basis row would vanish in that coordinate. Therefore, if m_v counts roots containing a positive coordinate v and sigma_pos=sum(m_v-1), then

sum_i |support(x) intersection R_i| = p + sigma_pos, and sum_i k_i=p.

For pairwise almost-disjoint tight sets A_1,...,A_r, define U as their union, m_v as multiplicity, and sigma=sum(m_v-1)=sum_j|A_j|-|U|. Their induced edge sets are disjoint. Let F be the remaining edges of E[U]. Exact degree and cardinality counting gives

r(U)x-b(U) = sum_v(m_v-1)x_v - (sigma-r+1) - sum_{uv in F}(1-x_u-x_v).

The left side is nonnegative and the final sum is nonnegative. If sigma>0, strict x_v<1/2 gives sigma/2>sum_v(m_v-1)x_v>=sigma-r+1. Hence sigma<2r-2 and, by integrality, sigma<=2r-3 when r>=2. If sigma=0 the same final bound is immediate. This covers crossing edges, zero coordinates, and repeated sharing of a single vertex; no pairwise-only approximation is used.

### 3.7 Inductive surplus and contradiction

For a subtree with k_S members rooted at S, induction gives at least k_S+2 positive coordinates in S. A leaf has at least three. With one child, strict support growth adds one. With r>=2 children, their support sets have total size at least sum_j(k_j+2), and their support-sharing loss is at most the all-vertex loss 2r-3. Their union thus has at least sum_j k_j+3=k_S+2 positive coordinates.

Summing over roots yields p+sigma_pos>=p+2t, so sigma_pos>=2t. There is at least one root because the graph contains a cycle and p>=3. One root has zero sharing, a contradiction. For at least two roots, the sharing bound gives sigma_pos<=sigma_all<=2t-3, again a contradiction. This proves the bounded theorem and Section 2 above transfers it to the original P.

## 4. Edge-strong-density cross-check and transfer limitations

Theorem 2 is a different statement about all nonempty edge subsets F and degrees in (V(F),F), in the same box. Its complete structural proof in Section 3 was also checked: Proposition 3, Lemmas 9-15, Theorem 4, the sharing identity, and the final contradiction. The same rank and counting reasoning applies with edge-laminar families.

The edge supermodular defect is sum of (1-x_u) over vertices belonging to V(A) intersection V(B) but not V(A intersection B). Its equality condition is valid because x_u<1. Uncrossing is used only when A intersection B is a nonempty **edge** set. Degree additivity and the equality of incident-vertex indicators give the row identity. Cut-vertex refinement preserves edge-laminarity and strictly decreases total edge cardinality, as the source correctly states. For nested edge sets A properly contained in B, counting incidences of B\A at old vertices gives a positive number p', while new vertices have degree at least two. Tightness would give |B\A|-|V(B)\V(A)|<p'/2, contradicting incidence counting. The sharing identity has no extra crossing-edge term because the union itself is an edge union. Thus the same surplus contradiction is valid.

There is **no global equality** between the two boxed polytopes. Edge feasibility implies induced-set feasibility, but for a set S containing isolated vertices in G[S] this requires the small check x(I)<=|I|. Taking F=E[S] only directly gives the inequality on V(F); subtracting x(I) and |I| transfers it to S.

Conversely, in the strictly-below-half region, induced-set feasibility does imply every edge inequality. For nonempty F, put S=V(F). Then

f_SD(S)=f_edge(F)+sum_{uv in E[S]\F}(1-x_u-x_v)>=f_edge(F).

Thus f_SD(S)<=0 implies f_edge(F)<=0. An all-small extreme point of the boxed strong-density polytope therefore belongs to the smaller edge polytope and remains extreme there. This yields a valid alternative transfer from Theorem 2, with the strict-region premise made explicit. Mere containment of arbitrary polytopes, without candidate membership, would not suffice.

The orientation extension and the polynomial-time algorithms in Section 4 and Appendix A are **not needed** for the accepted target and are not certified wholesale here. In particular, an extreme point in an extended formulation need not project to an extreme point, and an integrality-gap bound or existence of one large-coordinate optimum does not prove the universal claim. The proof above has no dependency on Farkas' lemma, total unimodularity, submodular minimization algorithms, or ellipsoid implementation details.

## 5. Corrections and adverse controls

The independent exact-rational script tests all 74 labelled simple graphs on 2, 3, and 4 vertices and 5,418 points from {0,1/3,2/5}^V. It checks strict-region agreement of the two formulations, 4,785 eligible uncrossing pairs, and 10,371 almost-disjoint tight pairs. These finite checks are sanity controls; the general proof is the argument above.

Explicit adverse examples establish why scope restrictions cannot be dropped:

- A three-vertex path has the zero extreme point. The graph must contain a cycle.
- For K4, the ordinary cycle-cover LP has extreme point (1/3,1/3,1/3,1/3), determined by its four triangle rows. It violates the full strong-density inequality, whose left side is 8/3 and right side is 3.
- For K_{2,3} with one additional edge between two vertices on its three-vertex side, x=(0,0,2/3,2/3,1/3) is a full-rank extreme point of the strong-density polyhedron. It is not half-integral. Removing the added edge yields an edge inequality with left side 5/3 and right side 2. This independently checks the preprint's Figure 1 and proves strict distinction between formulations.
- At the half boundary, K4 with x=(1/2,0,1/2,1/2) is density-feasible. Two tight triangles can have a zero-weight crossing edge, so the strict uncrossing row identity fails if '<1/2' is casually weakened.
- In K_{2,4}, put 1/2 on its two-vertex side and zero on the other side. Two edge-disjoint tight 4-cycles share two vertices, giving sigma=2>2r-3=1. This catches weakening the strict sharing hypothesis.
- Three 4-cycles joined at one common vertex have one cut vertex. Retaining two cycles still has one cut vertex, although the vertex count decreases from 10 to 7. Giving the common vertex zero and the others 1/3 makes both involved sets tight and feasible. This disproves the proposed structural cut-count measure; it is not claimed to be an impossible all-small extreme point.

Two additional incidental source slips are repaired explicitly: in Lemma 3 the final comparison 1-|I|/2 is <=0, not strictly <0 when |I|=2; the preceding strict inequality already proves f(I)<0. In the intersection-coordinate explanation, the expansion is 2d_I(u)+d_{A\B}(u)+d_{B\A}(u). The correctly stated degree identity and resulting row identity are unchanged. The overview's blanket reference to nonnegative constraint coefficients should be restricted: arbitrary induced-set rows have coefficient -1 at isolated vertices, which the proof correctly removes before using nonnegative tree rows.

## 6. Acceptance boundary and citations

No unresolved mathematical gap remains in the accepted original extreme-point statement after the explicit elementary corrections. The conclusion is source-credited to the September 2026 preprint; it is not promoted to an independently refereed publication or attributed to this audit. Theorem 2 is a checked cross-check with its exact formulation retained. Broader algorithmic and orientation claims are outside this acceptance.

Primary sources:

1. Chandrasekaran, Chekuri, Kulkarni, arXiv:2609.04414v1, 3 September 2026. https://arxiv.org/abs/2609.04414v1
2. Fiorini, *Open Problem: Iterative rounding for feedback vertex set*, OWR 53/2021, p. 2944. https://doi.org/10.4171/owr/2021/53
3. Chekuri, *Open Problem: Rounding Algorithms for Feedback Vertex Set and Subset Feedback Vertex Set*, OWR 50/2024, pp. 2993-2995. https://doi.org/10.4171/owr/2024/50
4. Chandrasekaran, Chekuri, Fiorini, Kulkarni, Weltge, *Polyhedral aspects of feedback vertex set and pseudoforest deletion set*, Mathematical Programming. https://doi.org/10.1007/s10107-024-02179-9; author-hosted full text: https://chekuri.cs.illinois.edu/papers/fvs-polyhedral-mpa.pdf
