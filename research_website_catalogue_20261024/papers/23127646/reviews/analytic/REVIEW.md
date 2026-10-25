# Independent analytic review — Zenodo 23127646

**Verdict: PASS at the manuscript's stated scope.** I independently verify the rational-boundary formula and its quantitative non-symmetry consequence. No substantive proof gap or counterexample was found. This is an AI mathematical review, not external human peer review, formal proof-assistant verification or a priority certificate. No manuscript repair or publication action was performed.

The reviewed paper is *Non-symmetry of biconstrained two-step reachability*, four pages, dated October 3, 2026, Zenodo version 1.0. The PDF SHA-256 is `35ddcd2a64bf0906fadcf762b913dfd9369941784ca0da87d97a3e9080ea80e4`; the supplied ZIP SHA-256 is `5415f48f702ab2e234376b73c4853043b1b7601316392ff4750123eb66339d81`. The final verdict binds the fresh receipt, both assets, manuscript source, primary sources and authored evidence.

## Independence and reading scope

I read all four PDF pages, including definitions, both theorem proofs, explicit graph descriptions, limitations, disclosure and references, and the complete corresponding TeX. Before opening supplied mathematical helpers I reconstructed the proof and wrote and executed `independent_checks.py` solely from the manuscript. Those results were fixed before helper inspection and are preserved as the initial check script/output. A final refinement made two rejection controls isolate positivity and regularity while preserving the other constraints; the positive graph and proof checks were unchanged. I then inspected the seven executable files reached by the portable replay (the launcher and six mathematical checkers) and reproduced its checks.

The package contains dedicated historical audit reports, priority reports, status files and research diaries. None was opened or used as a mathematical opinion. The portable integrity verifier hashes those files as opaque bytes and reads manifests to check provenance; this is not adoption of their contents. Mathematical helper comments and output make assertions about prior analytic checking, and the manuscript says previous AI audits exist. Those incidental assertions were encountered but were not evidence for my conclusion. I have not read sibling reviews.

## Exact claim and success criterion

The domain consists of finite simple graphs with a partition into nonempty stable sets A, B, C, no A–C edges, and four minimum-degree inequalities: A→B and B→A at fraction x, B→C and C→B at fraction y. Reachability counts distinct A vertices with a length-two path from c through B. It does not count paths with multiplicity.

For each admissible graph, take the largest fraction of A reached by a C vertex, then infimize over all graphs and partitions. This is equivalent to the largest universally guaranteed fraction in the primary problem. It does not assume the graph infimum is attained.

For every rational 0 < θ < 1, the paper defines d(θ) using finite binary incidence matrices with distinct columns, strictly positive rational probability vectors b and q, and Mq = θ1 and Mᵀb = θ1. It minimizes the **unweighted** maximum row count Δ(M) of distinct column types. Theorem 2 asserts

ψ(1−θ, θ) = 1−θ/d(θ),

with a finite ordinary graph attaining that value. Theorem 1 follows by bounding d(13/27), d(14/27) ≤ 4 and proves an absolute gap at least 1/108. It does not identify either invariant, either exact ψ value, or their ordering.

Success required a universal lower bound, a finite attaining upper construction with all four constraints, exact positive-rational blowup, verification of the prior seven-type seed, and a gap argument covering every allowed integer pair. Finite enumeration alone would not satisfy this criterion.

## Universal proof reconstruction

### 1. The integer minimum exists without compactness or an extremizer assumption

For θ = p/r in lowest terms, 0 < p < r. The r cyclic length-p intervals give r distinct nonempty proper column supports, uniform b and q, and every row count p. Thus the template set is nonempty. Every row has positive q-weight θ, so it contains an entry one and Δ ≥ 1. The set of realized degrees is a nonempty subset of positive integers and has a least element, realized by a member of that set. Neither a limit of weights nor a minimum over an unbounded-dimensional compact set is invoked.

This argument avoids conflating the minimum of integer degrees with attainment of the unrelated graph infimum. Attainment of ψ is established only after the explicit construction below.

### 2. Every non-full finite graph yields a regular template

Let F be the maximum reached fraction in an arbitrary (1−θ,θ)-biconstrained graph. If F = 1, the desired lower bound is immediate. If F < 1, **every** c misses at least one a. Their middle-neighborhood sets are disjoint and have sizes at least θ|B| and (1−θ)|B|. Since their union lies in B, both bounds are equalities and the neighborhoods are complementary.

Consequently every C vertex has degree exactly θ|B|. Counting B–C edges and using the reverse degree lower bound forces every B vertex to have degree exactly θ|C|. There is no unstated regularization or rational approximation here; the equality follows from saturation of a finite edge count. If θ|B| is not an integer, this case cannot occur and the graph must have F = 1.

Group C vertices by identical B-neighborhoods Tᵢ. All class weights qᵢ are positive rational numbers, the uniform middle weights bᵥ = 1/|B| are positive rational numbers, and the two exact degree identities give both regularity equations. Grouping is essential: counting the individual C twins would produce the wrong unweighted row degree.

A vertex a missed by class i must have neighborhood B∖Tᵢ, since its minimum degree and disjointness leave no slack. Conversely that exact neighborhood misses class i. Therefore the classes Aᵢ are nonempty and disjoint; a vertex cannot belong to two of them because the Tᵢ are distinct. With pᵢ = |Aᵢ|/|A| and t = min pᵢ, F = 1−t exactly.

For any middle vertex v, the disjoint union of Aᵢ over Tᵢ containing v is a subset of its A nonneighbors. Hence ΣᵢMᵥᵢpᵢ ≤ θ. Other A vertices can add nonneighbors but cannot reverse this inequality. Taking a row of maximum degree gives Δt ≤ θ. Since the extracted template has Δ ≥ d(θ), t ≤ θ/d(θ), proving the claimed lower bound for **every** finite graph.

### 3. A minimizing template gives a finite attaining graph

Choose a template with Δ = d, and let n be its number of distinct column supports. Each support has b-weight θ. Strict positivity of every bᵥ implies that two distinct supports of equal weight cannot contain one another: both directed set differences are nonempty. This fact will preserve all cross-type paths.

Set t = θ/d. Since nθ = Σᵥbᵥ degree(v) ≤ d, the residual δ = 1−nt is nonnegative. Give each Aᵢ weight t, and, if δ > 0, add a universal-to-B A type of weight δ. If δ = 0, omit that type; no zero-weight type is retained. Give B and C their b and q weights. All three part totals equal one.

Join Aᵢ to the complement of Tᵢ and Cᵢ to Tᵢ. Every Aᵢ has B-neighbor weight 1−θ. Every middle vertex has A-neighbor weight 1−t degree(v) ≥ 1−θ. Both B–C directions have neighbor weight exactly θ by the two regularity equations. Thus all four constraints hold simultaneously, using one common middle weight vector.

Cᵢ misses Aᵢ. For j ≠ i, the nonempty difference Tᵢ∖Tⱼ supplies a positive-weight middle witness, so Cᵢ reaches every Aⱼ. It reaches the residual A type when present because θ > 0 ensures Tᵢ is nonempty. The reached A-weight is exactly 1−t for every C type.

All retained weights are positive rational. Taking a denominator separately in each part makes every type a positive integer number of twins. Complete adjacency between adjacent type classes preserves all degree fractions. Positivity of the middle multiplicities preserves the existential path witnesses, so reachability fractions are preserved too. The result is a finite simple graph with nonempty parts and the claimed maximum. This proves both the upper bound and attainment. No general LP theorem, source weighted-graph attainment result, irrational rounding or disappearing zero-weight middle type is needed.

An independent packing interpretation checks the optimization step: for a fixed regular template, maximize t under pᵢ ≥ t ≥ 0, Mp ≤ θ1, and Σpᵢ ≤ 1. The uniform primal pᵢ = θ/Δ is feasible by nθ ≤ Δ. A maximum-degree row and its Δ lower bounds pᵢ ≥ t give the matching dual inequality t ≤ θ/Δ. This is an explicit finite inequality certificate; it does not evaluate the minimum degree across all templates.

### 4. The asymmetric pair and quantitative gap

Direct exact multiplication verifies the printed 7×7 matrix, its positive rational weights, distinct columns and maximum row degree four at θ = 13/27. Complementing entries preserves column distinctness and regularity with the same weights at θ = 14/27; its maximum row degree is also four. Thus the true d,e are positive integers at most four, without any claim that four is minimal.

The boundary formula gives the two values as 1−13/(27d) and 1−14/(27e). Equality would require 13e = 14d, impossible in the allowed range. For d = e the gap is 1/(27d) ≥ 1/108. If e > d, its numerator is at least 10 and de ≤ 12; if d > e, the numerator is at least 15 and again de ≤ 12. Both unequal cases give a strictly larger lower bound. All sixteen rational cases independently agree, with minimum 1/108 at d = e = 4 among the possibilities.

The two displayed ordinary constructions do have parts (108,27,27), reached counts 95 and 94, and all four degree minima. They only give upper bounds for the actual ψ values. Unequal upper bounds do not prove separation; the universal boundary formula is the indispensable step. The manuscript states this correctly.

## Fresh computational evidence and edge cases

`independent-checks.json` was produced before reading supplied helpers. It records:

- 34 exact template cases: the seed and complement, all reduced cyclic fractions with denominators 2–10, and an independent positive rational split of one middle row. Every case checks regularity, distinct supports, incomparability, the residual, literal unweighted degrees/reachability, and a matching primal–dual packing certificate.
- All 16 candidate integer pairs, with exact minimum gap 1/108.
- Exhaustive labeled adjacent-pair graphs on parts (3,3,3), covering all 262144 edge-pair choices at each of θ = 1/3 and 2/3. Each grid has 9010 admissible graphs, including 36 non-full cases; each non-full case obeys saturation, complementary missed classes and the extracted row inequality.
- Rejection controls for duplicate columns, zero weights with normalization/regularity preserved, and incorrect regularity with positivity/normalization preserved. These are tests of domain enforcement, not substitutes for the positivity argument.
- A common hypothetical value 4/5 satisfying both displayed upper bounds, showing why that pair of bounds alone cannot certify asymmetry.

The seven-type cases have positive residual A mass; the cyclic cases exercise zero residual. The row-split case exercises repeated rows and different denominator choices in the three parts. The analytic argument separately covers arbitrary leftover A vertices, repeated C columns before grouping, arbitrarily many finite types, nonuniform rational weights, incompatible integer cardinalities and the full-reach branch. The endpoints θ = 0,1 and irrational θ are outside the stated boundary theorem.

All arithmetic is exact integers or `Fraction`; no numerical stability or tolerance assumption enters. The finite cases corroborate local identities, and the universal proof above supplies the quantifiers they cannot test.

## Supplied reproduction

After the independent work, I inspected and ran the portable verifier with ordinary nonoptimized Python and bytecode disabled. It reproduced all six mathematical-program outputs byte for byte: 29175, 12749, 1831, 2552, 122568 and 357 checks, totaling **169232**. It also checked the package file set and hashes, 41 original proof-record files, 135 nested manifest entries, and unchanged final bytes. `published-replay.stdout.json` preserves program names and output hashes. No project code wrote files; outputs were captured only in this review folder.

Several old controls address exploratory routes and generic invalid inferences rather than the final theorem. Their successful execution is not evidence that their earlier routes prove global asymmetry. Their actual finite checks were inspected and are reported at that limited scope. Historical narrative documents remained opaque throughout.

## Primary interfaces and credit

Original publisher/author PDFs and receipts are saved under `primary-sources`. OWR printed pp. 46–47 state the matching symmetry question. CHSSS published pp. 4–6 define the matching finite model; Figure 1's upper bipartite graph and weights match the printed matrix by independent visual tracing. Published p. 10 concerns φ symmetry, and p. 72 treats only the special equality ψ(x,y)=x. Neither supplies general ψ symmetry or the present boundary formula. The new argument needs their explicit seed, not their LP proof or any presumed extremizer. No exhaustive novelty review was attempted.

## Final scope and remaining limitations

The strongest verified conclusion is the exact rational-boundary formula, finite attainment there, and the stated absolute gap at the two rational parameter orders. There is no unresolved mathematical node in those claims identified by this review. Exact invariant minima, exact ψ values, ordering, a computable global algorithm for d(θ), extensions off the rational boundary, and historical firstness are not established or required. AI review is not external human peer review.
