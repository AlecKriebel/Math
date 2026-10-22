# Focused adversarial review: prior full implication and the triangle-to-apex bridge

Date: 2026-10-17 UTC. Scope: PR1119 / problem 30004127, pinned `inputs/PROOF.md`, SHA256 `1483bcaa29473616799fa9c04937e55fc249bd27e293c45d580af236d38709f3`. This is an authored mathematical audit, not external peer review. No other review shard was read or contacted. No external individual was contacted. No Git state was changed.

## Verdict

**No earlier full answer to the Gishboliner–Shapira complexity question was identified in this focused review.** This is a bounded finding, not an exhaustive priority certificate. In particular, I did not identify a publication already giving this fixed hereditary, extendable property, its uniform polynomial tester, and its heavy-apex weighted-distance bridge, or a different such property with the required separation.

**A much shorter derivation of the lower bound is available from established two-sided triangle-testing hardness.** Alon–Shapira (2004) already supplies the exp(Ω(log²(1/ε))) hardness ingredient. The new derivation below maps arbitrary triangle-testing instances through a tripartite cover and then the candidate's heavy apex. It applies to the unrestricted oracle model with all the proposed gifts: known size, every vertex name, distinguished apex, and exact weight vector. It therefore avoids any reliance on Goldreich's unknown-universe query reduction.

The cover/apex deduction below was derived during this audit. Its simplicity does **not** establish that it was previously published, nor should it be reported as a historical earlier full answer. Conversely, a revised account should not present two-sided hardness, parity matching, secret permutation, or the use of a weight-1/2 vertex as new mechanisms. The possible new contribution is the specific fixed property and its quantitative use of an asymptotically negligible exceptional vertex.

## Exact target and success criterion

Let C3 be 3-colorability, A3 the graphs becoming 3-colorable after deleting at most one vertex, and P = K4-free ∩ A3. All distances count each unordered pair once. Uniform distance on N vertices has denominator N². Weighted distance is the sum of D(u)D(v) over modified unordered pairs; every repair on the same vertex set is allowed, including edge additions.

The target is a fixed hereditary, extendable property with a polynomial classical canonical sample bound on every finite input, and a superpolynomial lower bound on total VDF cost Q = samples + adjacency queries. Merely producing a property not testable at all in VDF, or a sample-only lower bound in a weaker oracle model, does not answer that target.

The original comparison is indeed restricted to extendable hereditary properties: OWR 19/2019, Problem 5, printed p.1139 / physical PDF p.27; arXiv:1905.09903v5, Problem 5.6, §5.3. [OWR original](https://ems.press/content/serial-article-files/46798), [GS v5](https://arxiv.org/abs/1905.09903v5).

## A fully explicit reduction importing older hardness

Write τ(H) for the minimum number of edges deleted to make H triangle-free. Triangle-freeness is monotone under edge deletion, so this equals the minimum number of arbitrary additions/deletions needed: intersect any triangle-free target with the input's edge set, which cannot introduce a triangle and cannot increase edit cost.

### 1. Remove the 3-colorability promise by a tripartite cover

Given any graph H on n ≥ 1 labeled vertices, construct L(H) on [3] × V(H). Put an edge between (i,u) and (j,v) exactly when i ≠ j and uv is an edge of H. The three layers are independent, so L(H) is always 3-colorable. Each original edge has six distinct lifted edges.

A triangle in L(H) projects to three distinct mutually adjacent vertices of H: its layer coordinates are pairwise distinct, and equal original coordinates would force a loop of H. Conversely, every triangle of H has six lifted triangles. Thus H is triangle-free if and only if L(H) is triangle-free.

Let F be any triangle-free target on the 3n cover vertices, and let R = E(L(H)) \ E(F). Dropping the added edges of F leaves a triangle-free deletion repair, with |R| no larger than the total edit count. From H delete each edge uv for which at least one of its six lifted edges belongs to R. Each deleted original edge can be charged to a distinct member of R, so at most |R| original edges are deleted. If an original triangle survived, all its lifted edges would survive, giving a triangle in F. Consequently

    τ(H) ≤ τ(L(H)) ≤ 6 τ(H),

and, in the stated unordered-pair normalization,

    dist_uniform(L(H), triangle-free)
        = τ(L(H))/(3n)²
        ≥ dist_uniform(H, triangle-free)/9.                    (A)

This lower inequality is deliberately conservative. It is sufficient, and its proof allows arbitrary additions in the original repair definition.

### 2. The heavy apex is an exact weighted embedding

For a 3-colorable graph L on N vertices, adjoin an apex a adjacent to every vertex. Give a mass 1/2 and each tail vertex mass 1/(2N). Then

    dist_D(J(L), P) = τ(L)/(4N²).                              (B)

For completeness, the two directions are as follows. Deleting τ(L) tail edges removes all triangles; the tail stays 3-colorable, and its join with a is K4-free and lies in A3. Each tail edge costs 1/(4N²).

For an arbitrary target F ∈ P, let S be the tail vertices whose apex edge was removed, and let t be the number of changed tail pairs. F on the tail outside S is triangle-free, since a is still adjacent to every vertex there and F is K4-free. Use F outside S and delete all original tail edges incident with S. This produces a triangle-free graph on the tail with at most t + N|S| changed pairs. The weighted cost of the original F repair is exactly (t + N|S|)/(4N²), since an apex edge costs 1/(4N). Hence τ(L) ≤ t + N|S|. This proves the reverse inequality even if F added edges, changed tail colorability, or used a different exceptional vertex. The argument does not presume that an optimal repair preserves the apex.

Equation (B) is the candidate's Lemma 3; the argument was independently checked here, rather than inferred from a lower bound. Combining it with (A), for M(H) = J(L(H)) gives

    dist_D(M(H), P) ≥ dist_uniform(H, triangle-free)/36.        (C)

If H is triangle-free, M(H) belongs to P. All weights are positive rational numbers: D(a)=1/2 and D(i,u)=1/(6n).

### 3. Simulate the strongest proposed VDF oracle

Suppose a VDF tester for P is run at proximity η. A tester for ordinary triangle-freeness at proximity δ runs that VDF tester at η = δ/36 on M(H).

* Supply the exact input size 3n+1, names a and (i,u), apex identity, and the whole weight vector. These gifts contain no information about unknown edges of H.
* A D-sample is simulated locally: return a with probability 1/2; otherwise choose a uniform element of [3]×[n]. The source dense model already gives n, so this needs no adjacency query.
* A query involving a is answered deterministically. A tail query in the same layer, or between copies of the same original vertex, is answered zero. Every remaining tail adjacency query is answered with one adjacency query to H.
* All replies, repeated labels, and adaptive decisions are exact. There is no approximation of D and no change of success probability.

Thus if H is δ-far, (C) supplies the requisite η-farness; equality cases are preserved with the same ≥ convention. Membership is also preserved. If the VDF tester uses s samples and e edge queries, at most s+2e source labels are inspected, and at most e source adjacency queries are made. A worst-case total bound Q gives at most 2Q inspected source labels. Consequently the reduction preserves the hardness exponent under either dense-model cost convention. No assumption that VDF queries be confined to sampled labels is used. If queries are restricted to sampled labels and all induced adjacencies are free, the source labels appearing in the simulation number at most s. The same older vertex-inspection lower bound then gives the corresponding superpolynomial sample lower bound as well.

### 4. Exact older hardness input

Alon and Shapira, *Testing subgraphs in directed graphs*, JCSS **69**(3), 354–382 (2004), DOI [10.1016/j.jcss.2004.04.008](https://doi.org/10.1016/j.jcss.2004.04.008), already proves a two-sided lower bound of (1/δ)^{c log(1/δ)} for a fixed non-bipartite forbidden undirected subgraph, including the triangle. In the inspected [author manuscript](https://www.cs.tau.ac.il/~nogaa/PDFS/testdig5.pdf), see Theorem 4(ii), p.4, and the explicit undirected consequence at the start of §7, p.23. Definitions on p.2 give n and allow arbitrary adjacency-pair queries. Their convention on p.4 counts inspected vertices with the induced graph available. The proof, pp.25–26, uses random deletions and a hidden permutation to handle adaptive algorithms. The introductory STOC version appeared in 2003, pp.700–709.

Their lower bound therefore yields, by the exact simulation above,

    2 Q_P,VDF(η) ≥ (1/(36η))^{c log(1/(36η))}

up to an inessential absolute constant in the lower-bound statement, for sufficiently small η. Equivalently Q_P,VDF(η) = exp(Ω(log²(1/η))). In particular this implies the candidate's asserted sequence lower bound; it can also be used without committing to the specific explicit sequence of its self-contained construction.

The factor 36 in (C) is exact in this review's unordered n² convention. If importing a literally bidirected normalization rather than the paper's expressly stated undirected consequence, a fixed factor two in the source parameter should be absorbed as well; it has no effect on the separation. The paper's sample/vertex convention should not be silently identified with adjacency-query count: the displayed 2Q exposure bound is the needed bridge.

## What remains supplied by the candidate rather than by the old theorem

The classical side relies on C3 ⊆ P ⊆ A3, not on an efficient K4-removal lemma. A hereditary property in this sandwich inherits a polynomial canonical test from polynomial colorability testing: for sufficiently large n, two disjoint sampled non-3-colorable witnesses exclude deletion of one exceptional vertex; for small n, a larger sample sees the whole graph with high probability. This is the candidate's all-size argument. Known polynomial colorability testing is an ingredient, but the present review did not identify a published general result that already packages the required sandwich together with the weighted hardness embedding.

The single exceptional vertex is inexpensive under the uniform measure (at most O(1/n) of pair edits) and can retain weight 1/2 in VDF. The restriction K4-free then makes triangles in its neighborhood costly. Removing either part of that combination loses the claimed argument: K4-freeness itself is already hard classically, while A3 alone automatically accepts every apex join of a 3-colorable tail. P's closure under deleting edges and vertices and under adding isolated vertices is elementary and was checked directly.

Finding (A)–(C) now establishes a short mathematical proof route, not historical priority for that route. Any claim of a new lower-bound technique would need to confront the older results below.

## Closest pre-existing results and exact gaps

### Alon–Kaufman–Krivelevich–Ron (2008): parity is already standard

[Author manuscript](https://www.math.tau.ac.il/~krivelev/testtria.pdf), §6, Theorem 3, pp.23–27, converts appropriate triangle-discovery lower bounds to two-sided testing lower bounds. For edge-disjoint triangles it replaces each vertex by two copies, each edge by parallel or crossing pairs, and chooses parity so a triangle becomes either two triangles or a 6-cycle. Local observations agree until the relevant triangle is exposed. The general-graph model also permits degrees and neighbor queries, and distance is relative to edge volume rather than n². Those quantitative/model conditions must be translated before using its theorem wholesale.

The candidate's retained-edge even/odd distributions are a different realization of the same standard local-parity principle; they do not warrant novelty credit as a new two-sided mechanism. The previously published result still lacks the P/apex/sandwich combination. The simpler dense AS04 theorem above is sufficient and avoids conversion of sparse-model parameters.

### Goldreich (2018–2021): heavy vertices and VDF one-sided conversion predate this work

The inspected [R3 manuscript](https://www.wisdom.weizmann.ac.il/~oded/R3/vdf.pdf) is dated 4 October 2021. Proposition 2.2, pp.11–12, eliminates unsampled queries in its unknown-universe setting. Theorem 2.3, pp.12–14, converts s-sample VDF testing to one-sided O(s²)-sample testing. Proposition 2.11, pp.27–28, gives an easy-classical/hard-VDF two-star property, even with n supplied, using a center of mass 1/2. That property is not hereditary: an induced subgraph containing only one connected star violates its requirement of two sufficiently large components. It therefore does not answer GS's restricted comparison. The same paper already tests many hereditary graph-partition properties efficiently in VDF.

Once the proposed P and its one-sided weighted triangle obstruction are supplied, Theorem 2.3 is another route to qualitative two-sided superpolynomial hardness. Its proof changes the sampling distribution and uses Proposition 2.2; it does not by itself prove the candidate's stronger hard-family statement with the exact distribution supplied. The direct cover simulation above does prove that stronger statement.

### Gishboliner–Shapira: quantitative positives are conditional

In [v5](https://arxiv.org/abs/1905.09903v5), Proposition 5.4 requires an ε-dependent upper bound on every vertex mass; Proposition 5.7 transfers a canonical standard tester under blowup-avoidability. The heavy mass 1/2 does not meet the needed small-mass hypothesis. The candidate's wheel example directly shows P is not blowup-avoidable, so that sufficient condition cannot be applied. Failing this hypothesis is not itself a negative theorem. The short negative proof still requires (B) and the classical sandwich argument.

The [journal landing page](https://link.springer.com/article/10.1007/s11856-021-2228-8) was inspected: Israel J. Math. 245, 787–837 (2021), version of record 30 October 2021. Only abstract/metadata/references were accessible. The PDF request returned subscription-preview HTML, not a full PDF. No claim is made here to have inspected the journal body or verified identity of its §5 with arXiv v5.

### Fei (2026): sample-only hardness does not give the queried-product-model result

[arXiv:2603.22702v2](https://arxiv.org/html/2603.22702v2), dated 12 August 2026, gives edge-distribution sample bounds (Theorem 1.5); Remark 1 distinguishes extra adjacency queries, and Problem 8.4 leaves their power open. Section 7.1, Definitions 7.1–7.2 and Lemma 7.4, uses the standard two-fold parity cover and cites AKKR08. Its lower bound is for edge samples; the measure may be arbitrary over pairs rather than a vertex product.

There is a concrete obstacle to importing Lemma 7.4 into the present strongest query model. On its stated fixed known host E, choose a known triangle abc. Queries to ((a,0),(b,0)), ((b,0),(c,0)), and ((c,0),(a,0)) reveal the three parity bits, and their parity distinguishes its yes/no vector classes. Thus its edge-sample lower bound is not also a query lower bound for that promise family. An additional hidden-label construction or another argument is necessary. Moreover, sampling an endpoint of a uniform edge gives a degree-biased vertex, not a uniform tail vertex; the required D oracle is not freely available from its sample interface. These are actual simulation gaps, not a dismissal by model name.

### Quantitative hereditary closure results (2026)

Carenini–Seth–Yoshida, [arXiv:2608.01523v1](https://arxiv.org/abs/2608.01523v1), gives a classical quantitative container characterization and partition closure (Theorem 5.1), with constituent properties required to be hereditary and extendable. Representing A3 as a partition into C3 and a class of size at most one fails that last assumption: the singleton class is not extendable. Replacing it by an independent-set class produces 4-colorability and loses the construction. Theorem 6.1 concerns a fixed fractional-size induced member, not deletion of at most one vertex with its size-dependent fraction. These results do not supply the weighted distance embedding or the hard fixed property. They can inform classical upper bounds, but are not an identified prior full answer.

## Validation, access limits, and completion

The mathematical checks are the general proofs (A)–(C), the exact oracle simulation, the explicit hereditary failure of the two-star example, and the three-query countercheck against a naive use of Fei's sample-only lower bound. The source text of AS04 has damaged PDF character mapping. All 30 pages were OCRed privately; the key statements and lower-bound exponent on pp.4 and 26 were also inspected visually. Author-copy theorem numbering is reported as such, without asserting journal pagination of those statements.

`verify_bridge.py` checks every one of the 75 labeled simple graphs with 1≤n≤4. It computes the cover triangle-deletion optimum, and minimizes apex repair cost over every target graph in P on n+1 vertices, including arbitrary additions. Every check passed. The normalization control is a K3 tail: uniform tail distance 1/9, heavy-apex distance 1/36, and any single deleted apex edge costs 1/12. These finite checks are supplemental and prove no asymptotic or priority assertion.

The report's strongest verified outcome is the exact factor-36 reduction from ordinary triangle-freeness to the supplied P, valid with all oracle gifts. The unresolved historical gap is whether any earlier publication gives this particular fixed-property embedding or another full GS separation; none was found in the focused directly inspected set. No global absence claim is justified.

Completion estimate: **100% of this focused implication audit**, not 100% confidence of literature novelty. Third-party full sources and OCR are confined to ignored `sources/private/` and `tmp/`. Authored files include the query ledger, retrieval/version/hash manifest, pinned-input verification, this report, the check program/results, and the research log. No external outreach is proposed or prepared.
