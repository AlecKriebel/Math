# Independent audit: the rooted-arborescence splitting boundary

## Verdict and exact version

**Accepted as a partial mathematical result, after one local witness correction.** No unresolved proof defect was found in the revised report. The general rooted-arborescence Integer Carathéodory Property (ICP) question remains unresolved by this work.

Target: **30001933 / OWR-11451-006**.

Distributed report: *A sharp vertex-count obstruction to direct splitting integrality for rooted arborescences*, [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md), 13,607 bytes, SHA-256:

`fb4bc3639dba84d3d8ea5cc1080cbc529bbc26ce09598ba50670482f3649f21b`.

This proof-and-audit edition preserves the accepted symbolic arguments and the corrected witness. Supplementary computation reports and private workflow references are omitted. The audit is AI-assisted and unrefereed; acceptance does not mean external human peer review, journal acceptance, or formal proof-assistant certification.

Audit date: 2026-10-10 UTC.

Accepted conclusions, with their exact limits:

1. If deleting the root leaves a cactus in the underlying simple undirected graph, the rooted-arborescence polytope belongs to the Gijswijt–Regts sufficient splitting class C. Arbitrary finite parallel multiplicities and either arc direction are allowed.
2. Every rooted directed multigraph on at most four vertices consequently belongs to C.
3. The specified five-vertex, eight-arc graph has a fractional vertex in `P ∩ (1−P)` and therefore lies outside C. Five is the least possible **vertex count** for failure of C in this class of rooted-arborescence polytopes.
4. That same five-vertex polytope nevertheless has ICP, by the explicit integral-capacity circulation lift and the Gijswijt–Regts coordinate-projection theorem.

This does not establish minimum arc count, classify all graphs in C, prove ICP for all arborescence polytopes, produce an ICP counterexample, establish a greedy decomposition theorem, or certify historical novelty.

## 1. The exact target and foundational dependencies

The report uses a fixed root vertex, not a number of packed trees. Its quantifiers require, for each positive integer k and each integer w in kP, a representation by affinely independent integer points of P, with nonnegative integer coefficients totaling k. This agrees with Gijswijt–Regts's journal definition. Allowing zero coefficients is harmless: discard them. An integer point in the convex hull of 0–1 tree vectors is itself one of those vectors: in any convex representation, each coordinate equal to 0 or 1 forces that coordinate of every positively weighted vector to agree.

The cited class is exactly the source class after substituting k=a+b and r=a. It requires box-integrality for **all** nonnegative integer a,b and all integer translation vectors, including those for which the intersection is empty. Empty intersections impose no obstruction. A bounded polyhedron is integer precisely when its vertices are integral; every nonempty face of an integral polytope contains an integral vertex.

The proof relies on the published Gijswijt–Regts results: Theorem 1 for C implies ICP, Theorem 5 for coordinate projections of C implies ICP, and Theorem 6 for integral-right-side TU systems in C. Those statements were checked against the journal paper, including the affine-independence conclusion in Theorem 5. This audit does not replace those published theorems with an IDP assertion. In particular, projecting an arbitrary affinely independent decomposition need not preserve affine independence; the cited projection theorem supplies a stronger argument, using a suitable face on which the projection is injective.

Theorem 11 about intersections of equal-rank gammoid base polytopes is correctly credited as background. The report's actual proof of ICP for its example uses an explicit circulation lift followed by Theorems 6 and 5; it does not need to assert that an arbitrary graphic matroid is a gammoid, nor does it assume unverified equal ranks in an auxiliary matroid intersection.

The remaining foundational facts are elementary: directed-incidence matrices are TU; adding signed copies of rows and unit rows preserves TU; bounded TU systems with integral right sides have integral vertices; and coordinate projections of integer polyhedra are integer. For the bounded applications, the last fact follows immediately by projecting the convex hull of integral vertices. More generally, a nonempty exposed face of a projected polyhedron is the projection of the corresponding exposed face upstairs, which supplies an integer point.

## 2. Audit of the integer-linear unique-lift lemma

Let Q be exactly the image of P under an integer matrix L, with coordinate projection π satisfying πL=I. The inverse identity makes L injective on the entire ambient space, not merely on P. For positive a,b and integer w, put W=Lw. Both inclusions in

`L(aP ∩ (w−bP)) = aQ ∩ (W−bQ)`

hold:

- If x=ap=w−bq with p,q in P, then Lx=aLp=W−bLq.
- If y=aLp=W−bLq, then injectivity gives ap=w−bq. Thus y=L(ap) with ap in the claimed intersection.

Given any integral coordinate box B downstairs, its inverse image under π is a coordinate box upstairs with unrestricted auxiliary coordinates. Hence the lift of the boxed splitting intersection is precisely the upper splitting intersection with this box. Its integrality follows from Q in C, and projection returns the required boxed intersection downstairs.

### Zero scalings

The relevant polytopes are nonempty. With ordinary set scaling, `0P={0}` and `0Q={0}`. If a=0, the downstairs split is either empty or `{0}`; the equality above holds because `Lw ∈ bQ` is equivalent to `w ∈ bP`. If b=0, it is either empty or `{w}`, and the same equivalence applies. When a=b=0, injectivity ensures W=0 exactly when w=0. Any nonempty boxed singleton in these cases is integral. Thus there is no omitted endpoint case.

### Why fixed flow coordinates cause no affine error

The eventual lift is genuinely linear. A head-to-sink flow equal to 1 on P is represented by the sum of the original incoming coordinates at that head. The return flow equal to |V|−1 is represented by the sum of all original coordinates. These expressions define integer linear functions even for arbitrary ambient w that do not satisfy the arborescence affine equations. No constant coordinate is incorrectly treated as an affine offset. For a split to be nonempty, those linear expressions automatically have the corresponding scaled totals; otherwise both sides of the lift equality are empty.

Therefore the lemma is valid in the full scope required by the cactus proof. Mere existence of an integral or TU lift would not suffice for this conclusion.

## 3. Audit of the universal cactus construction

### 3.1 Loops, root edges, and finite degeneracies

Loops and arcs entering the root are unusable and can be removed. Keeping them as zero coordinates does not change membership in C: for a split in the enlarged space, a nonzero translation in an added coordinate makes the intersection empty; otherwise it is the old split times zero. A coordinate box either excludes that zero and makes the result empty, or leaves the old boxed intersection. The same zero-coordinate embedding preserves ICP.

All other arcs remain individually distinguished. Opposite directions and parallel copies between nonroot vertices enter the same unordered edge group. Parallel arcs from the root have separate original coordinates and separate source-to-head network arcs. The head's fixed total of 1 prevents selecting two such arcs into the same vertex. No simplicity assumption on the directed graph is hidden here.

The construction allows isolated nonroot vertices and disconnected cactus components. Existence of an arborescence is assumed; a graph with none is outside the nonempty argument and has the stated vacuous ICP claim. With only the root present, the polytope is a singleton in zero effective coordinates; the return flow is fixed to zero and the same argument works.

### 3.2 Exact forest constraints

After loops are removed, a selected set of nonroot arcs is an undirected multigraph forest precisely when it selects at most one member of each edge group and fails to select at least one edge of every simple cycle of H.

Necessity follows from absence of parallel two-edge cycles and ordinary cycles. For sufficiency, group capacity first gives a genuine simple subgraph of H. If it contained a cycle, that subgraph would contain a simple cycle C, using every edge of C, contrary to the C inequality. This proves the characterization without assuming any orientation of the selected arcs.

The cactus hypothesis is used at the correct place: different simple cycles have disjoint edge sets. An edge belongs to at most one cycle, so every group node has a unique input arc, either from its cycle node or directly from the source. Cycles may share vertices without sharing an edge, and the proof does not require them to be vertex-disjoint. The phrase cactus is explicitly defined in the report so disconnected cacti are included.

### 3.3 The network is a valid member of C

Each coordinate has finite integral lower and upper bounds: 0 to 1 for ordinary arcs, 0 to |C|−1 for cycle inputs, fixed 1 for head outputs, and fixed |V|−1 for the return. Conservation is a homogeneous directed-incidence system. Writing it as two inequalities and adjoining the bounds gives a TU matrix and integral right side. Thus the circulation polytope is bounded and belongs to C.

This can also be checked directly for positive a,b: the split circulation must satisfy the two conservation systems and integral lower/upper bounds obtained by intersecting the scaled bounds with their translated reflected bounds. If the conservation systems conflict, the split is empty; otherwise it is a network-incidence system with integral bounds. Additional coordinate boxes only add integral bounds. The a=0 or b=0 cases are the integral singletons described above. This checks that fixed positive flows introduce no exception to the TU conclusion.

### 3.4 Projection equality, not just a relaxation

An integral circulation gives values 0 or 1 on every original-arc coordinate and exactly one incoming original arc at every nonroot vertex. At every edge group, conservation and the capacity of the unique input arc give group total at most one. At every cycle node, conservation and its input capacity give total at most |C|−1. The nonroot selected arcs therefore form a forest.

Any directed cycle in the selection would avoid the root, which has no entering arc, and would give an undirected nonroot cycle. Thus no directed cycle exists. Starting from a nonroot vertex and following its unique parent backward must eventually reach the root: otherwise finiteness forces a repeated vertex and a directed cycle. Reversing the parent chain gives a root-to-vertex directed path. The selected set is therefore precisely a spanning rooted out-arborescence.

Conversely, any arborescence's underlying undirected graph is a tree, so its nonroot arcs satisfy all group and cycle capacities. Assigning the selected coordinates and sending their group and cycle sums through the corresponding input arcs respects all capacities and conservation. Head outputs and the return arc have the required fixed values. This provides a feasible integral lift of every arborescence.

Since the bounded network polytope is the convex hull of integral vertices, all its projected points lie in the convex hull of the arborescences. Conversely, the lifts of every arborescence and convexity put their entire convex hull in the projection. Thus the projection is exactly P, with no unstated sufficiency of an arborescence inequality description.

### 3.5 Uniqueness and integer linearity

Conservation determines each group input as the sum of its original arc coordinates, and determines each cycle input as the sum of the inputs of that cycle's groups. Every head output is the sum of original coordinates entering its vertex. Conservation determines the return as the sum of all original coordinates. There are no other network coordinates. The formulas are sums with integer coefficients, copy the original coordinates unchanged, and define a global integer matrix L with πL=I. Hence Q={Lx:x in P} and the lemma applies.

This proves the universal cactus result symbolically.

### 3.6 The minimum vertex-count consequence

Deleting the root from a graph on at most four vertices leaves at most three vertices. Every simple graph on at most three vertices has at most one simple cycle, so it satisfies the report's cactus condition. Parallel arcs and loops were already handled. Thus every nonempty rooted-arborescence polytope at those sizes lies in C. Combined with the five-vertex obstruction below, this establishes the claimed sharp vertex count. It is not an extrapolation from a search over small simple digraphs.

## 4. Audit of the five-vertex obstruction

Keep the report's ordered arcs a,b,c,d,e,f,g,h. The four proposed membership trees are valid, with root paths explicitly visible as follows:

- `adeh`: 0→3→1→2→4.
- `bceh`: 0→2→4→1, with 0→3.
- `acfg`: 0→2→3→1, with 0→4.
- `bdfg`: 0→4→1→2→3.

Their incidence-vector midpoints give exactly the displayed z and 1−z. Consequently membership in P and its reflected translate is established by exact convex combinations, without a floating-point feasibility claim.

The two upper bounds on `a+d+f` and `b+d+h` are valid because an arborescence cannot contain either of the specified directed triangles. Validity extends from tree vertices to P by convexity. Applying the first bound to 1−x yields `a+d+f ≥ 1` on the split intersection. The coordinate bounds and the two indegree equations used in the vertex certificate are also valid.

At z, the four fixed coordinates are e=1, f=0, g=0, h=1. The remaining tight equations reduce to

`a+b=1`, `c+d=1`, `b+d=1`, `a+d=1`.

Subtracting the last two gives a=b; then a+b=1 gives a=b=1/2, and the remaining equations give c=d=1/2. Thus the eight active constraints have a unique solution. No assertion that all eight constraints are facets is needed.

If z were a proper convex combination of two points in the split, each active valid inequality must be tight at both endpoints, as must each affine equality. The uniqueness calculation forces both endpoints to equal z. Therefore z is a vertex. It has four noninteger coordinates, so the split is not integer, hence not box-integer. This is a valid failure of C with a=b=1 and integer w equal to the all-ones vector.

The displayed integer decomposition `1 = chi(aceh)+chi(bdfg)` is also correct. The first summand has root paths 0→3→1 and 0→2→4; the second was checked above. These are two distinct points, so they are affinely independent, and their coefficients total two. The fractional split vertex therefore does not itself give an ICP failure, even at its displayed translation vector.

## 5. Audit of ICP for the entire obstruction polytope

### 5.1 The matching representation really represents forests

The five nonroot edges form K4 with edge {3,4} removed. Put A={a,f}, B={b,h}, and let d be the remaining edge. Allowed slot sets are {1,2} for A, {2,3} for B, and {2} for d.

- Every set of size at most two is matchable. Pairs within A use 1 and 2, pairs within B use 2 and 3, pairs crossing A and B can use 1 and 3, and a pair with d puts d in 2 and its partner in the appropriate exclusive slot. All such sets are forests because the five edges form a simple graph.
- A triple containing d is unmatchable exactly when its other two elements both belong to A or both to B. These are adf and bdh, precisely the two triangles. Otherwise assign A to 1, d to 2, and B to 3.
- A triple without d consists of two elements from one side and one from the other. Assign the doubled side its two allowed slots and the other element the remaining exclusive slot. Such triples are not triangles and are forests.
- Sets of at least four edges cannot be forests on four vertices and cannot fit into three slots.

This proves the equivalence for all subsets. In particular, the four-edge undirected cycle a,f,h,b is not overlooked: it is excluded by the three-slot total capacity.

### 5.2 The full matching-flow polytope projects exactly to P

The three root arcs have distinct private slots. Integral circulation chooses four distinct slot-to-element assignments, one original incoming arc at each head. The element-to-head capacity of 1 prevents an element from being selected twice via different slots. The slot capacities enforce a matching. Thus the selected nonroot set is a forest, and the same parent-chain proof as above makes the selected set an arborescence.

Conversely, every arborescence's nonroot set is a forest and hence admits the established matching, while its root arcs use their dedicated slots. These choices give an integral circulation with the four fixed head outputs and fixed return flow. Boundedness and TU integrality again promote this equivalence of integral objects to equality of the entire projected polytope with P.

The matching-flow system has integral bounds and a TU incidence matrix, so it belongs to C. Gijswijt–Regts Theorem 5 then proves ICP for P for every k and every lattice point in kP. This is stronger than checking the single all-ones vector; no support-count bound or ordinary tree-packing theorem is substituted for affine independence.

### 5.3 The detected defect and its verified correction

The initial report attempted to demonstrate nonuniqueness by the pair {a,b}. Although that pair is matchable into the abstract slots, both arcs enter vertex 1. Hence it cannot occur in a feasible circulation of the full lift and does not witness nonuniqueness over P.

The revised report replaces it with the arborescence `{a,c,e,g}`. Its a coordinate can use slot 1 or slot 2; c,e,g use their dedicated slots. Both assignments give feasible full circulations and the same original arc vector, and differ on the source-to-slot and slot-to-a coordinates. This repairs the demonstration without changing any theorem statement, projection construction, or obstruction certificate.

The revised report was inspected after the repair. The old witness is retained here only to document the audit finding and why the correction is sufficient.

## 6. Source, historical, and novelty boundaries

The source statements were checked using the full journal text, the original report's Question 2 and surrounding definition, and the recent survey's Open Question 8.6. Relevant original-report and survey pages were visually inspected; the journal's definition and TU/projection page were also rendered and visually inspected. The public journal PDF and official EMS PDF were reachable during this audit. The survey's older URL redirected and its direct institutional PDF endpoint was not retrievable through this audit's web tool, so the survey body check used the previously retained, rehashed final-copy bytes; the institution's current publication record independently confirms its bibliographic identity.

Verified retained public-source PDF identities:

- Gijswijt–Regts journal paper: 169,252 bytes; SHA-256 `06d78f4c48fb29ffcade81d77ace52b1da0562c2b5205ce1bcbaf7cc540f5f75`.
- Original OWR report: 692,215 bytes; SHA-256 `8929eb517cf07898a4ac27e65404398187686e7481ae2f8ae84f7be2e80cf977`.
- Lancini–Pisanu final institutional copy: 1,013,796 bytes; SHA-256 `081092931e993dbac180080b9842d8f8a904ae919b874de0ce6915fe7fcd4e79`.

The Gijswijt–Regts sufficient class, TU implication, ICP projection theorem, and gammoid-intersection theorem retain their original credit. The report supplies an explicit application, a preservation argument, and a graph certificate; this audit does not certify that those partial constructions are historically new. The recent survey is evidence that the exact question is still listed there, not proof that every subsequent result has been excluded. Its surrounding discussion is not used in place of the original, complete ICP definition.

### Public references

1. D. Gijswijt and G. Regts, *Polyhedra with the Integer Carathéodory Property*, Journal of Combinatorial Theory, Series B 102 (2012), 62–70. [DOI](https://doi.org/10.1016/j.jctb.2011.04.004), [public journal copy](https://www.math.ucdavis.edu/~deloera/TEACHING/READINGSEMINAR/PAPERS/gijswijt%2Bregts.pdf). Definition and condition (3), Theorems 1, 5, 6, 11, Question 2.
2. D. Gijswijt, joint work with G. Regts, *Polyhedra with the Integer Carathéodory Property*, in *Combinatorial Optimization*, Oberwolfach Report 53/2011, pp. 3025–3027. [Official report page](https://ems.press/journals/owr/articles/11451), [official PDF](https://ems.press/content/serial-article-files/46369?nt=1). Question 2 is separate from the subsequent greedy Question 3.
3. E. Lancini and F. Pisanu, *A horizon tour of box-total dual integrality*, Computer Science Review 61 (2026), 100928. [DOI](https://doi.org/10.1016/j.cosrev.2026.100928), [institutional publication record](https://research.dial.uclouvain.be/entities/publication/442f8ee7-ccce-4f60-9104-b5b6394c8023). Open Question 8.6, printed p. 38 / retained PDF p. 40.

**Final disposition:** accept the revised report as a rigorously supported partial boundary result. Keep the general rooted-arborescence ICP target unresolved. No claim beyond the four accepted conclusions is endorsed.
