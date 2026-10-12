# The complemented rectangle seed: a known FFLV result and a source correction

**Problem:** 30003069 / OWR-14221-005. **Assessment:** the coherent complemented-seed question has a published answer, credited to Fang–Fourier (2018). The imported assertion about the unchanged non-mirror rectangle graph is not the statement printed in the original report. The report itself has a frozen-label typing defect, described below. This is a source audit with one elementary diagnostic approach, not a new FFLV theorem. Separate adversarial review is pending.

## 1. What the original page actually says

The complete contribution is Xin Fang, joint work with Ghislain Fourier, *Polytopes arising from mirror plabic graphs*, Oberwolfach Reports 13 (2016), 626–628, in [OWR 13/2016](https://ems.press/content/serial-article-files/46617). The page images, rather than text extraction alone, are essential: extraction loses overbars.

The report distinguishes three pieces of notation.

1. On p. 626, the distinguished rectangle graph `G₀` for `Gr(n−k,n)` gives a Newton–Okounkov body equivalent to `GT(rω_(n−k))`, by Rietsch–Williams.
2. On p. 627, Theorem 4 concerns the mirror `G₀∨` and gives `FFLV(rω_k)`.
3. The later Conjecture 2 concerns **`Ḡ₀`**, with an overbar. It follows a construction from complemented cluster labels. It does not concern the unchanged graph in item 1. The report records the case `Gr(3,6)` as verified.

To keep the tensor-power parameter distinct from a label cutoff, write the latter as `ℓ`. The printed construction starts with `(n−k)`-subsets `I₁,…,I_m`, declares `Δ_(I_ℓ),…,Δ_(I_m)` mutable, and displays

`C′ = {Δ_(I₁),…,Δ_(I_(ℓ−1)), Δ_(I_ℓ^c),…,Δ_(I_m^c)}`.

It calls this a cluster of `Gr(k,n)` and calls its graph `Ḡ`. Thus only the mutable labels are visibly complemented. Taken literally, the frozen labels still have size `n−k`, whereas Plücker coordinates of `Gr(k,n)` have indices of size `k`. When `n≠2k`, this is not a well-typed list of Plücker coordinates on the asserted Grassmannian. The source does not supply an alternative interpretation of those frozen indices.

The imported record removes the overbar, adds “non-mirror,” and reports a general unresolved question for the original graph. Those edits are not faithful to the rendered page. In particular, an unchanged rectangle seed cannot be substituted for `Ḡ₀`.

## 2. The authors' later published formulation

The full five-page paper [Fang–Fourier, *Symmetries on plabic graphs and associated polytopes*, C. R. Math. 356 (2018), 581–585](https://www.numdam.org/item/CRMATH_2018__356_6_581_0.pdf), DOI [10.1016/j.crma.2018.05.003](https://doi.org/10.1016/j.crma.2018.05.003), revisits the same construction. On p. 582 it complements **every** label:

`C′ = {Δ_(I₁^c),…,Δ_(I_m^c)}`.

It identifies the resulting graph with the dual graph and states the FFLV conclusion as Corollary 1. The graph in this conclusion is the distinguished rectangle graph introduced on p. 581, not an arbitrary plabic graph. Section 4.2 makes that restriction explicit in Theorem 3.

Write `G = G^rec_(k,n)` in that paper's convention, so that the original body belongs to `Gr(n−k,n)`. Its dual is formed by swapping the internal colours, reversing the perfect orientation, and relabelling a boundary index `a` by `a+n−k` modulo `n`. The face label in the dual is exactly the complement of the original face label. Theorem 3 proves

`NO_(G∨)(L_k) ≅_Z FFLV(ω_k)`.

Here `≅_Z` means an affine lattice isomorphism: its linear part is integral with determinant ±1. The full paper was read, including the antichain/minimal-flow argument in §4.2. This audit invokes the published theorem; it does not advertise an independent reconstruction of its general flow matrix.

A subsequent primary paper, [Schlößer, arXiv:2501.11466v1 (2025)](https://arxiv.org/abs/2501.11466), gives the complement operation in Lemma 3.7 and Definition 3.8 and restates the dual-rectangle FFLV theorem as Theorem 8.6. Its own checkboard-graph theorem is a different result and is not being used as a substitute for the rectangle theorem.

### Why the self-dual case agrees even with the old frozen-label display

For the top-cell seed, the frozen labels form the family of all cyclic intervals of the appropriate cardinality. Put

`J_s^(d) = {s,s+1,…,s+d−1} mod n`.

Then, as subsets of `[n]`,

`(J_s^(d))^c = J_(s+d)^(n−d)`.

When `n=2k` and `d=k`, complementation therefore permutes the entire frozen family. Keeping the frozen family while complementing the mutable labels gives the same **set of face labels** as complementing all labels. This is not a claim that each frozen label is fixed individually. It explains why the report's `Gr(3,6)` statement fits the published dual-seed formulation.

For `n≠2k`, the literal mixed-cardinality display remains defective. The later all-complement formula is a documented, coherent replacement, not a convention invented here. We make no claim to solve an unspecified alternative operation that would keep frozen variables fixed as individually labelled functions across the two different Grassmannians.

## 3. Valuation, divisor, and tensor-power conventions

The theorem is about the network or face-parameter valuation, not the ordinary exponent valuation in the Plücker cluster coordinates themselves. In the conventions of Fang–Fourier §3.2:

- use the standard acyclic perfect orientation with source set `[k]` on the dual graph;
- attach a parameter to each face except the distinguished redundant face;
- the weight of a path is the product of face parameters to its left; a flow weight is the product of its path weights, and the normalized Plücker coordinate is the sum over vertex-disjoint flows;
- choose a total order of the face parameters and use lexicographic **lowest-term** exponents to obtain the full-rank valuation;
- regard a section `s` of the `d`th power of the Plücker line bundle as the rational function `s/Δ_[k]^d`.

The body uses all section degrees and their normalized valuations. In particular it is not defined merely as the convex hull of degree-one Plücker valuations. The distinction is real for general plabic graphs. Fang–Fourier's theorem asserts the full body identification for the dual rectangle graph.

For the compatible general framework, see [Rietsch–Williams, arXiv:1712.00447v2 (2019)](https://arxiv.org/abs/1712.00447), Definitions 8.1–8.6 and Remark 8.7. The total parameter order can alter the valuation on individual functions, but their resulting bodies and degree-wise valuation polytopes do not depend on that choice. Section 16.1 establishes the ordinary rectangle/GT identification. Their `k` indexes the complementary Grassmannian in some formulas; the target Grassmannian above is explicitly `Gr(k,n)`.

Changing the normalizing nonzero Plücker section changes every degree-normalized valuation by a fixed integral vector. Thus it changes the body only by an integral translation. This does not justify arbitrarily changing a seed or replacing a lowest-term valuation by a highest-term one.

The positive-integer tensor power in the 2016 report follows from the published degree-one result by the following standard direct argument. For a fixed normalizing section `τ`, let

`B = closure(conv { ν(s/τ^d)/d : d≥1, 0≠s∈H⁰(L^d) })`.

Restricting this union to degrees divisible by a positive integer `r` leaves its convex hull unchanged: one inclusion is immediate, and the other follows by replacing a degree-`d` section by `s^r`, since

`ν(s^r/τ^(dr))/(dr) = ν(s/τ^d)/d`.

The definition using `L^r` divides those same degree-`rm` valuations by `m`, rather than by `rm`. Consequently

`NO_(G∨)(L_k^r) = r NO_(G∨)(L_k)`.

The FFLV polytope for `rω_k` is likewise `r FFLV(ω_k)`: its nonnegative coordinates satisfy the same chain inequalities with right-hand side `r`. If the degree-one lattice equivalence is `x↦Ux+b`, the degree-`r` equivalence is `x↦Ux+rb`, again integral unimodular. This supplies every positive integer `r` asked for in the report.

## 4. A diagnostic against the imported unchanged-graph reading

This elementary check is not a counterexample to the barred-graph conjecture. It shows why the word “non-mirror” and the missing bar cannot be accepted harmlessly.

The ordinary rectangle body for `Gr(3,6)` is equivalent to the order polytope of the `3×3` grid poset. The FFLV polytope for `ω₃` is its chain polytope. These identifications are given in Fang–Fourier §4.1 and Proposition 2; the underlying poset is unchanged by reversing both grid directions.

For an `a×b` grid with coordinatewise order, the order polytope has

`(a−1)b + a(b−1) + 2`

facets: one for every cover relation, one for the unique minimal coordinate being zero, and one for the unique maximal coordinate being one. The chain polytope has

`ab + binomial(a+b−2,a−1)`

facets: `ab` coordinate nonnegativity conditions and one upper bound for every maximal northeast lattice path. These are the irredundant descriptions from [Stanley, *Two poset polytopes* (1986), §§1–2](https://math.mit.edu/~rstan/pubs/pubfiles/66.pdf).

For completeness, irredundancy can also be seen directly. For an order-polytope cover, identify its two endpoints and strictly order the resulting acyclic quotient between 0 and 1. A directed cycle in that quotient would give an intermediate element between the endpoints, contradicting the cover property. The resulting point saturates only the selected cover inequality. For the extremal-coordinate inequalities, take strictly increasing values with only the selected extremal coordinate at 0 or 1. Thus each defines a codimension-one face. For a chain-polytope coordinate inequality, take all other coordinates sufficiently small and positive. For a chosen maximal chain `C` of length `h=a+b−1`, assign `1/h` on `C` and a small positive `ε<1/h` off `C`. Its sum is one; any other maximal chain misses at least one element of `C` and, having the same length `h`, has strictly smaller sum. Again exactly the selected inequality is tight. Both polytopes are full dimensional, so these witnesses establish the stated facet counts.

At `a=b=3`, the counts are respectively **14 and 15**. An affine isomorphism preserves facets, so these two polytopes are not even affinely equivalent. Positive dilation does not change the facet count. In particular the unmodified rectangle body cannot equal the FFLV unimodular type in the very `Gr(3,6)` case quoted in the imported record.

The checker independently enumerates the twenty order filters and twenty antichains of the `3×3` grid and computes exact affine ranks on all 29 proposed facets. This is a finite verification of the diagnostic, not verification of a general plabic-flow theorem.

## 5. Conclusion and limitations

The recommended source-aware classification is **already solved for the authors' corrected complemented-seed formulation**, with credit to Fang–Fourier (2018). The literal 2016 mixed-cardinality frozen-label display needs the qualification above; the imported unchanged non-mirror statement is a different, false reading. Neither supports recording a remaining independent general FFLV conjecture for an unchanged rectangle graph.

One substantive diagnostic approach was used (the order/chain facet obstruction); the rest is source reconciliation and the tensor-power normalization. There is no new general plabic equivalence, all-seed result, priority claim, or independent reproof of Fang–Fourier's theorem. The separate final question on p. 627 about all plabic bodies and birational sequences is not this record and has not been addressed.
