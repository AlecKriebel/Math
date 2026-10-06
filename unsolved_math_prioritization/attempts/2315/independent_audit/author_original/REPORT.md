# Research report for rainbow quadrilateral colorings

## Outcome

EP-810 is unresolved after five approaches. The strongest useful reduction is Theorem 1 in PROOFS.md: the extra requirement of proper edge coloring changes the extremal edge count by only o(n^2), with no palette increase. This conclusion is proved using the standard triangle removal lemma, whose role is explicitly credited.

The exact statement has a fixed positive density, at most n colors on n vertices, and a graph for every sufficiently large n. It does not assume proper coloring and does not restrict attention to induced cycles. These distinctions are preserved throughout the argument.

## Results and their limits

1. Negligible deletion makes the coloring proper. This gives exact equivalence of the all-size existence questions for general graphs and balanced bipartite B-colored graphs. It leaves the B-coloring density question unresolved.
2. The standard projection from a linear (7,4)-free tripartite triple system gives a B-coloring. An alternating four-edge path shows that the converse fails. The remaining gap is genuine additional combinatorial content, not a missing palette convention.
3. Cyclic affine labels with invertible coefficients, even followed by arbitrary output relabeling, force subquadratic edge count. The proof uses the finite multidimensional Szemeredi theorem. Arbitrary labels are not covered.
4. Any complete uniform t-fold blowup of a fixed h-vertex seed containing an edge requires at least t^2 colors, exceeding its ht vertices for t>h. Altered amplification schemes remain outside the result.
5. A common-neighbor count gives at most (1/(2 sqrt(2))+o(1))n^2 edges with n colors. It does not force density to vanish and is not asserted sharp.

## Source and current-literature review

The definitions in Burr, Erdos, Graham, and Sos (1989), printed p.264, and the C4 density discussion on printed p.273 match the mathematical formulation under investigation. The rendered p.273 was inspected to disambiguate the scanned exponent and weak inequality. A record of retrieved PDF bytes and selected inspection locations is in SOURCE_PROVENANCE.json.

Gyarfas and Sarkozy (2023), definitions and Questions 1.2-1.3 on printed pp.111-112, distinguish proper B-colorings from the extra alternating-path condition. Their Proposition 1.6 concerns the C-coloring variant, so it must not be substituted for a B-only equivalence. This note's seven-vertex example isolates the difference directly.

The introduction of Gyarfas, Martin, Ruszinko, and Sarkozy, Proper edge colorings of planar graphs with rainbow C4-s, arXiv:2408.09059v2, dated 29 August 2025, still presents the B-coloring density question and its connection to (7,4). Its planar results concern a sparse host class and do not answer EP-810. https://arxiv.org/abs/2408.09059v2

The following 2026 manuscripts were checked at the abstract/metadata level for scope, not fully audited:
- Bucic, Chen, and Ma, On a maximal anti-Ramsey conjecture of Burr, Erdos, Graham, and Sos, arXiv:2603.18952v1, concerns odd cycles of length at least nine in its main stated result. https://arxiv.org/abs/2603.18952v1
- Li, Ning, and Xie, Two problems of Burr, Erdos, Graham, and Sos on maximal anti-Ramsey functions for P4, arXiv:2606.30505, concerns path targets. https://arxiv.org/abs/2606.30505
- Yang, On the maximal anti-Ramsey problem of Burr, Erdos, Graham, and Sos for P4, arXiv:2607.05896v1, addresses the complementary near-complete density range for a path target. https://arxiv.org/abs/2607.05896v1

Their inspected abstracts do not establish the C4 result sought here. This is a bounded literature check, not proof that no other solution exists. Direct fetches of https://www.erdosproblems.com/810 and https://unsolvedmath.com/problems/2315 returned HTTP 403; the web-tool alternate tracker route also failed. The imported statement was instead checked against the original paper. No restricted-access source was bypassed.

## Repository and inherited-work gate

Before any mathematical investigation, the complete exact-ID problem record and its complete inherited report were inspected. Their pinned hashes matched. The inherited content was literature triage only; the report was empty. No substantive inherited mathematical work was present in those exact inputs.

Bounded read-only searches of AlecKriebel/Math by exact ID 2315, EP-810, and rainbow-quadrilateral phrases returned no exact-problem code, commit, branch, or pull-request match. A broader search for 810 or quadrilateral returned unrelated work, including PR number 810 for a different problem. This is not exhaustive repository history or novelty clearance. Search scope and counts are recorded without private content in VERIFICATION_METADATA.json.

## Validation and audit scope

There is no included executable verifier, solver, enumeration, or computational certificate. No normal or optimized Python mathematical-validation pass is claimed. The author inspected the mathematical deductions and selected relevant primary-source passages. This package requests a fresh independent mathematical audit, especially of the properness deletion map, exact liminf quantifiers, cyclic-coordinate square argument, and scope of the hypergraph example.

The external manifest pins every authored payload file and the complete ZIP by byte count and SHA-256. These hashes check identity only. They do not validate a theorem, establish source authority, or certify completeness of the literature search.
