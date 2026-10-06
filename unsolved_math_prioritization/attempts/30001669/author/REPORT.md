# Short cycles in highly dominating digraphs

## Result

Problem 30001669 (OWR-4791-028) already has a **negative answer in published work from 2015**. Credit belongs to Yogesh Anbalagan, Hao Huang, Shachar Lovett, Sergey Norin, Adrian Vetta, and Hehui Wu. This note verifies that their theorem applies to the exact 2011 question. It does not claim a new mathematical discovery.

## Exact scope

For a finite directed graph D, write P_s(D) for the condition

    For every U ⊆ V(D) with |U| ≤ s, there exists v ∈ V(D)
    such that v → u for every u ∈ U.

Thus the elements of U have one common **in-neighbor**; equivalently, the witness has arcs directed to all of U. The question asks whether P_100(D) forces a directed cycle with at most 100 edges. Noga Alon's problem appears on printed page 74 of the 2011 Oberwolfach Combinatorics report [1]. The primary passage and supplied statement agree.

This concerns general finite digraphs, not only tournaments. It is a common-neighbor condition, not a minimum-degree hypothesis or the usual assertion that a small set dominates the whole graph. No substitution of the Caccetta–Häggkvist conjecture is involved.

## Published theorem and direct deduction

The authors of [2] define a (k,l)-digraph on printed page 80: all directed cycles have length at least k, and every vertex subset of cardinality at most l has a common predecessor. Their Theorem 11 on page 83 establishes finite examples for every pair of positive integers k,l. Set k=101 and l=100. The resulting finite D satisfies P_100(D), while every directed cycle has at least 101 edges. It is therefore a counterexample to the exact question. The quantifier is already “at most” in the original definition, so no exact-size padding or vacuity argument is needed.

## Construction boundary checks

The published proof obtains a pair-dominating base digraph with directed girth at least (k−1)(l−1)+1, then joins vertices reachable by positive walks of length at most l−1. At our parameters the base bound is 9901 and the power is 99. A cycle of length at most 100 in the power would yield a nonempty closed base walk of length at most 9900, which contains a directed cycle and contradicts the base bound. The base digraph is finite, constructed on a finite cyclic group. These observations also fix the positive-walk convention: length-zero walks must not be included in the power.

Any loop would itself have length 1, and any pair of opposite arcs would give a 2-cycle. Consequently the counterexamples have neither. A witness cannot belong to the set it dominates, since that would require a loop. Multiple arcs are unnecessary. The empty-set case is satisfied because the constructed vertex set is nonempty. Singletons are explicitly within the source definition; following incoming arcs in a finite nonempty graph then ensures that some directed cycle exists.

There is no contradiction with the tournament case: a finite tournament with every vertex having an in-neighbor cannot be transitive and therefore contains a directed triangle. The general digraph quantifier is essential.

## Status and verification limits

The resolution is a published existence theorem, not an explicitly enumerated 100-dominating adjacency matrix in this package. No finite census or exhaustive 100-subset check is claimed. The mathematical deduction above is complete relative to the cited theorem. The supplied code checks package integrity, metadata consistency, and the parameter inequalities; it does not prove the cited theorem or instantiate its enormous construction.

The exact primary question, the definition on page 80, and Theorem 11 on page 83 were read and visually inspected on 2026-10-06. The live aggregator request returned HTTP 403; no bypass was attempted. Statement recovery therefore used the full supplied corpus and the official primary report. Both the statement hash and the prescribed complete-record review hash match. The older corpus assessment describing the problem as open is superseded by [2]. A bounded fresh search found no correction withdrawing this theorem; this is not an exhaustive literature-clearance claim.

The investigation stopped after the first approach, matching the exact question to a credited published resolution. There is no remaining mathematical gap in that identification. Producing an explicit finite adjacency certificate would be a separate task and is unnecessary for recognizing the published negative answer.

## References

1. Jeff Kahn, Angelika Steger, and Benjamin Sudakov, editors/organizers, Combinatorics, Oberwolfach Reports 8 (2011), no. 1, pp. 5–83. Noga Alon's problem: p. 74. DOI: https://doi.org/10.4171/OWR/2011/01 . Official article: https://ems.press/journals/owr/articles/4791 . Official PDF: https://ems.press/content/serial-article-files/46314?nt=1 .
2. Yogesh Anbalagan, Hao Huang, Shachar Lovett, Sergey Norin, Adrian Vetta, and Hehui Wu, Large Supports are Required for Well-Supported Nash Equilibria, APPROX/RANDOM 2015, LIPIcs 40, pp. 78–84. Definition: p. 80; Theorem 11: p. 83. DOI and publisher record: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX-RANDOM.2015.78 . Preprint submitted 14 April 2015: https://arxiv.org/abs/1504.03602 .

No source PDFs, extracted passages, source datasets, corpus records, or private coordination material are included in this package.
