# Independent adversarial review: tripartite-cover reduction

Review date: 2026-10-17 UTC. The review concerns a proposed simplification of the lower-bound route for the fixed property

\[
P=\{G:G\text{ is }K_4\text{-free and deleting at most one vertex leaves a 3-colorable graph}\}.
\]

## Verdict and strongest verified claim

**PASS, with explicit model and empty-input guards.** The proposed elementary reduction is mathematically valid with the stated factor 36. It handles unrestricted adaptive, two-sided testers and arbitrary edge-edit repairs, including additions. No secret permutation or hiding of the cover representation is required.

More precisely, every tester for P at proximity parameter ε, with worst-case total cost at most Q sample calls plus adjacency queries, gives a uniform triangle-freeness tester at parameter 36ε using at most Q adjacency queries. The triangle-freeness tester may know n and generate free uniform samples locally. The assertion holds algorithmically for every n≥1, and the n=0 case is accepted directly without constructing a distribution.

Consequently, for complexities defined as minima of worst-case costs over all finite input sizes, in the indicated models and at the same error probability,

\[
q_{\mathrm{VDF},P}^{\mathrm{sample+query}}(\varepsilon)
\ge q_{\mathrm{uniform},\mathrm{TF}}^{\mathrm{query}}(36\varepsilon).
\]

For a nonvacuous customary parameter range one may state this for 0<ε<1/144. The algorithmic implication itself needs only ε>0; if the triangle-freeness far promise is empty, it remains valid but carries no lower-bound content.

This report verifies the reduction, not any imported numerical asymptotic lower bound for classical triangle-freeness. In particular, an `exp(Ω(log²(1/ε)))` consequence still needs an exact primary-source theorem for the corresponding two-sided adaptive adjacency-query model. No claim about priority or novelty is made here.

## Independence and materials

The only mathematical input read from the audit package was the pinned `../../inputs/PROOF.md`. Its Section 4 was checked directly rather than accepting the accompanying audit. No other review report was read. No external person was contacted, no third-party body was downloaded, and no Git mutation, fetch, index operation, or PR action was performed. All authored material is inside this review folder.

## 1. Distance convention and the deletion guard

All graphs are finite, undirected, loopless, and simple. For a graph X on m≥1 vertices, write

\[
\tau(X)=\min\{|S|:S\subseteq E(X),\ X-S\text{ is triangle-free}\}.
\]

Triangle-freeness is closed under edge deletion. For any triangle-free repair F of X, the graph with edge set E(X)∩E(F) is also triangle-free and costs exactly |E(X)∖E(F)| deletions. This is no more than |E(X)△E(F)|. Conversely, a deletion repair is an allowed unrestricted repair. Therefore the minimum unrestricted triangle-freeness edit cost is exactly τ(X), and

\[
\operatorname{dist}_{\rm unif}(X,\mathrm{TF})=\tau(X)/m^2.
\]

This argument establishes the guard needed before projecting a repair of the cover. It neither assumes nor asserts that arbitrary repairs of P use deletions.

## 2. Cover construction and factor 9

Let H have n≥1 vertices. Define L on {1,2,3}×V(H) by

\[
\{(i,u),(j,v)\}\in E(L)
\iff i\ne j\text{ and }\{u,v\}\in E(H).
\]

The three first-coordinate classes form a proper 3-coloring. Every triangle of L uses three distinct first coordinates. Its original vertices are also distinct, because an edge with u=v would require a loop in H. Projection therefore maps a triangle of L to a triangle of H. Conversely, any triangle uvw of H gives the triangle (1,u),(2,v),(3,w) in L. Hence

\[
H\in\mathrm{TF}\iff L\in\mathrm{TF}.
\]

Each original edge has exactly six distinct lifted edges: one for each ordered pair i≠j, with u assigned the first part and v the second. Distinct original edges have disjoint sets of lifted edges.

Take an optimal deletion repair S⊆E(L), with |S|=τ(L). Delete an original edge whenever at least one of its lifted edges lies in S. The resulting original deletion set R satisfies |R|≤|S|, because the lifted edge sets partition E(L). If H−R contained a triangle uvw, none of the lifted edges of its three original edges would have been deleted. In particular, (1,u),(2,v),(3,w) would be a triangle of L−S, a contradiction. Thus

\[
\tau(H)\le |R|\le\tau(L).
\]

Since L has 3n vertices,

\[
\operatorname{dist}_{\rm unif}(L,\mathrm{TF})
=\frac{\tau(L)}{9n^2}
\ge\frac{\tau(H)}{9n^2}
=\frac19\operatorname{dist}_{\rm unif}(H,\mathrm{TF}).
\]

The proof requires no coloring promise on H, no bound on its triangle overlap, and no assumption that its triangles are edge-disjoint.

## 3. Independent check of the heavy-apex identity

Here state the identity for an arbitrary 3-colorable tail X on m≥1 vertices. Add a universal apex a to obtain J(X), and let

\[
D(a)=\frac12,\qquad D(x)=\frac1{2m}\quad(x\in V(X)).
\]

**Upper bound.** Delete τ(X) tail edges to make the tail triangle-free. The tail remains 3-colorable because edge deletion preserves a proper coloring. The resulting join is K4-free: a K4 through a would require a tail triangle, while a tail K4 cannot occur in a 3-colorable graph. Deleting a leaves a 3-colorable graph, so this is a repair into P. Each deleted tail edge has D-weight 1/(4m²). Hence

\[
\operatorname{dist}_{D}(J(X),P)\le\frac{\tau(X)}{4m^2}.
\]

**Lower bound with arbitrary additions.** Take any repaired graph F∈P on the same labeled vertex set. Let S consist of the tail vertices whose edge to a was deleted. There are no possible apex-edge additions, since J(X) began with every apex–tail pair present. The apex-edge repair cost is |S|/(4m). Write c_t for the total weighted cost of all tail changes, deletions and additions together; their number is 4m²c_t.

Because F is K4-free, F[V(X)∖S] is triangle-free: a triangle there would still have all three adjacencies to a. Form a triangle-free graph Y on V(X) by keeping this induced subgraph and isolating S. The number of changes from X to Y outside S is at most 4m²c_t. The original edges of X incident with S number at most m|S|. These two sets of pairs are disjoint, so

\[
\frac{\tau(X)}{m^2}
\le\frac{|E(X)\triangle E(Y)|}{m^2}
\le4c_t+\frac{|S|}{m}
=4\left(c_t+\frac{|S|}{4m}\right).
\]

The first inequality is permitted because τ(X) is the unrestricted minimum too, by Section 1. Minimizing over F gives

\[
\boxed{\operatorname{dist}_{D}(J(X),P)
=\frac14\operatorname{dist}_{\rm unif}(X,\mathrm{TF}).}
\]

The lower bound uses only the K4-free condition on F. It does not require the apex to remain the exceptional vertex in F, nor does it assume anything about the coloring of the repaired tail. Choosing another exceptional vertex or adding tail edges therefore creates no escape from the argument. The 3-colorability assumption on the original tail is used in the upper bound.

Substitute X=L and m=3n. Then D(a)=1/2 and every tail label has weight 1/(6n), and

\[
\operatorname{dist}_{D}(J(L),P)
\ge\frac1{36}\operatorname{dist}_{\rm unif}(H,\mathrm{TF}).
\]

Thus a 36ε-far H gives an ε-far weighted instance. If H is triangle-free, the construction produces a member of P.

## 4. Oracle reduction and exact quantifiers

Fix ε>0 and an algorithm A that tests P at parameter ε, with error at most 1/3 on every property member and every ε-far instance. Suppose every execution of A uses at most Q sample calls plus adjacency queries, with no restriction on adaptivity or internal computation. Its input model may also provide the size, all vertex names, the full weight vector, and the distinguished apex name.

Construct a tester B for triangle-freeness at parameter 36ε. Its input is H with known n and names V(H); the only charged operation is an adjacency query. For n=0, accept immediately. For n≥1, run A against the virtual weighted graph J(L), without constructing or querying the whole graph:

- Supply size 3n+1 and distinct labels a and (i,u), if A's model provides them. A name assignment such as a=0 and (i,u)=1+(i−1)n+u is available when V(H)={0,…,n−1}.
- A distribution sample is generated locally: choose a with probability 1/2; otherwise choose i uniformly from {1,2,3} and u uniformly from V(H). These independent choices give each tail label probability 1/(6n). Repeated sample names are retained as repeated names, not converted to new vertices.
- Answer a self-query by 0. Answer a query between a and a distinct tail label by 1.
- For two tail labels, answer 0 locally if their first coordinates agree or their original vertices agree. In every other case, query the single original adjacency H(u,v) and return it.

All answers are exactly the corresponding graph adjacencies. In particular, the simulator must not answer the apex self-query by 1 or send a loop query to an oracle that only permits distinct original labels. The above rules avoid both issues.

Conditioned on A's random coins, the simulator produces exactly A's valid oracle interaction on J(L), and its samples are independent draws from exactly D. This remains true for arbitrary adaptive queries to unsampled labels and arbitrarily repeated queries. The adjacency-query cost to H is at most the number of adjacency queries made by A, hence at most Q. The local sample simulation incurs no charged H adjacency query.

If H is triangle-free, J(L) belongs to P, so B accepts with probability at least 2/3. If H is 36ε-far, J(L) is ε-far, so B rejects with probability at least 2/3. These are per-input guarantees; no random instance distribution, conditioning on a far event, or permutation coupling is used.

No secret permutation is needed. A may know the cover representation and the original grouping of the three copies of each vertex, in addition to every stated gift: any algorithm exploiting these facts would itself yield a triangle-freeness algorithm through the same simulation. This last statement applies to a promise algorithm on this constructed family as well, provided it succeeds for every H in the yes and far cases.

Taking the infimum over all valid A establishes the complexity inequality above. If one instead uses costs depending on the vertex count, the direct statement is the size-by-size implication from a bound on 3n+1 weighted vertices to a bound on n original vertices. Expected-query bounds are also preserved as expectations, but a theorem stated only for expected costs should not be silently substituted for a worst-case theorem, or conversely.

## 5. Falsification attempts and boundary cases

| Potential escape | Check and outcome |
|---|---|
| A triangle in the cover projects to a walk with repeated vertices | Impossible: repeated original endpoints would require a loop. |
| Some original edge retains five copies after one lift is deleted | The projection deletes that original edge entirely. Cost does not increase because each projected edge has a distinct deleted lift as witness. |
| Repair of L uses additions | Intersect the repair with L; triangle-freeness survives and edit cost does not increase. |
| Repair of J(L) adds tail edges or changes the exceptional vertex | The independent lower bound uses only its K4-free apex neighborhood, and accounts for every tail addition in c_t. |
| Apex erasure makes the input cheap to repair | Deleting apex edges to S already costs |S|/(4m), enough to pay for isolating S in the normalized tail distance bound. |
| H is not 3-colorable or contains K4 | L is always 3-colorable; H has no required coloring promise. The K4 finite control passes. |
| Self-queries, duplicate samples, copies of the same original vertex | Handle locally as specified above; all names retain their identity. |
| n=1 or n=2 | H and L are triangle-free; their heavy-apex outputs lie in P. No far promise exists for positive ε on these inputs. |
| n=0 | The formula 1/(6n) is undefined. B accepts directly; do not invoke the distribution construction. |
| ε=0 | Excluded: the usual testing promise is formulated for positive proximity, since members would also be zero-far under an “at least” convention. |
| Classical tester knows n; VDF tester does not | A simulation may ignore extra n information, or provide it to a strengthened VDF model. The lower-bound import must match the stated known-n classical model. |
| Finite-size lower bound treated as a uniform all-size theorem | State the algorithmic implication first. Any source lower bound must then be applied with its exact size and parameter quantifiers. |
| Canonical or one-sided lower bound substituted for unrestricted two-sided one | Not justified by this reduction. The source must supply the required unrestricted two-sided bound, or a separately proved conversion. |

The maximum uniform triangle-deletion distance is less than 1/4 for every finite nonempty graph: a random bipartition retains at least half the edges in expectation, so deleting at most |E(H)|/2≤n(n−1)/4 edges makes H bipartite. This explains the convenient nonvacuous range 36ε<1/4; it is not an extra assumption in the simulation.

## 6. Exact finite control

Run:

```text
python3 check_small_covers.py
```

The authored dependency-free script examines all 76 labeled graphs with 0≤n≤4, including all 64 labeled four-vertex graphs. For H and its three-part cover it solves the exact minimum triangle-edge hitting-set problem by an exhaustive, memoized recurrence: choose a surviving triangle, and branch on deleting each of its three edges. Every deletion repair must take one branch, so this is an exact integer computation rather than an LP relaxation. Every returned deletion witness is separately checked by enumerating all surviving triangles. The cover witness is projected back to H and checked separately.

Results in `small_cover_results.json`:

- 76 graphs checked, including 24 with triangles.
- Every yes/no triangle equivalence and every proposed distance inequality passed.
- Every H triangle produced exactly six cover triangles, as expected.
- The smallest observed ratio τ(L)/τ(H) among positive cases was 6. This is only a finite observation; the proof above asserts the sufficient universal lower bound 1.
- For H=K4, τ(H)=2 and τ(L)=12, with 24 cover triangles.
- The largest exact recurrence state count was 28,232.

These checks support and adversarially exercise the cover argument; they do not replace its proof. They do not enumerate arbitrary weighted P repairs, whose exclusion is established analytically in Section 3.

## 7. Remaining gap and promotion boundary

There is no remaining mathematical gap in the stated finite-graph reduction. Its cost inequality and factor 36 are independently verified.

The remaining external dependency for the proposed asymptotic corollary is **the exact classical lower-bound statement**, with two-sided error, unrestricted adaptivity, adjacency-query accounting, uniform-sample convention, known input size, and ε/size quantifiers checked against a primary source. This report intentionally leaves that dependency unpromoted. It does not independently review the manuscript's separate ordinary-model P upper bound, its original explicit hard-instance construction, or its priority claims.
