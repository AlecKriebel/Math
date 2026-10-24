# Fresh two-dimensional filter adversarial audit

Verdict: **PASS as incorporation of a known prior theorem and a sufficient exclusion class**, not a new solution or original theorem for21.126.

## Primary scope

I read actual Corollary1.3 on printed p3 of the cached Huang–Osajda arXiv1710.05157v2 and its dimension definition on printed p5. I independently checked the publisher's open-access version of record, [DOI10.1007/s00208-019-01823-6](https://link.springer.com/article/10.1007/s00208-019-01823-6). It confirms the subgroup theorem, publication on April10,2019, and the same statements. The result applies to finitely presented subgroups of two-dimensional Artin groups, rather than only the ambient group. Dimension means cohomological dimension. The cached PDF's margin date March15,2019 and body date November2,2021 genuinely differ; no explanation for that discrepancy is assumed. Independent publisher confirmation supplies the established2019 priority date.

## Deductions tested

A triangle-free RAAG satisfies the cited triangle condition vacuously. When it has an edge, its Salvetti complex supplies cohomological dimension at most2 and its Z² subgroup forces dimension at least2. This justifies application even if the theorem's phrase two-dimensional is read as exact dimension. The note separately handles edgeless graphs as free groups, so it does not conflate dimensions0,1,2. The deduction gives an upper bound only: it does not falsely require a cyclic or free subgroup's Dehn function to be equivalent to n².

Finite presentation is essential and correctly retained. The expanded claim does not say every finitely generated subgroup of a triangle-free RAAG is finitely presented. That would fail already for some subgroups of a product of free groups. This is distinct from the previously checked, stronger coherence property for forest RAAGs. The historical forest note remains valid but is subsumed as an exclusion method by the new known theorem.

The degree-nine bound in the expanded class follows from the already reviewed complete-multipartite seed theorem and the free-product / central-Z closure lemma. Replacing forest seeds by all triangle-free graphs strengthens the sufficient criterion while leaving that closure proof unchanged. A hypothetical witness cannot have any finite-support embedding into a graph in the class. This is only a necessary restriction on a hypothetical witness; it does not turn any outside graph into a viable candidate or assert that all other known exclusions are exhausted.

## Independent exact census

`independent_dimension_two_census.py` reuses only this reviewer's earlier independent encodings and orbit routine, never either author census module. It generates all labelled grammar constructions forward from triangle-free or at-most-three-part multipartite seeds, then takes explicit disjoint unions and single universal-vertex additions. Its triangle test enumerates vertex triples. Its nonadjacency-equivalence test for multipartite seeds and adjacent-transposition orbit enumeration are independent of the author's connected-component parser and permutation canonicalization.

It reproduces labelled inside counts1,1,2,8,64,754,11723 through six vertices. Isomorphism inside counts through five are1,1,2,4,11,29. It independently reproduces all five outside canonical masks59,185,187,221,254 and every corresponding JSON edge list. All graphs on at most four vertices belong to the expanded class. These computations validate only the grammar census and the stated sufficient exclusion, with no original group witness.

No substantive objection remains to the exact note and code listed in the receipt. The overall Kourovka problem remains unresolved, and known results receive explicit priority credit.

Audit completed 2026-10-24T21:23:35.675855+00:00.
