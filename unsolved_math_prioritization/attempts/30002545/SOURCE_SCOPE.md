# Exact source and literature scope

Problem 30002545 is Bóna's question on printed page 707 of OWR 12/2014. The entire question, including Stanley's conditional observation, was read and the page visually checked. Trees use vertex set [n], are rooted and plane, and every child label is smaller than its parent's. They are not unlabeled Catalan trees and not binary search trees. Choose a uniform tree, then a uniform vertex. The request explicitly forbids generating functions and induction and does not allow assuming that the limit exists.

The original report prints the total number of leaves as (2n+1)!!/3. This is a source typo, not an adopted premise: it exceeds the total number of vertices already for n=2. Bóna–Pittel, arXiv:2108.04989v2, Example 2.3, gives (2n−1)!!/3 for n≥2. Their introductory definitions, tree-size conventions and Example 2.3 were checked; their general-rank asymptotic proofs are not used here or claimed fully audited. Publisher metadata identifies the 2023 Random Structures & Algorithms article, DOI 10.1002/rsa.21138.

The method-relevant prior sources are more important than the already-known limit:

- Janson, arXiv:0803.1129v1, sections 1–2: the contour bijection maps a plane recursive tree with m+1 vertices to a Stirling permutation of order m, carrying leaves to plateaux. Its equations (1.2), (1.6) already imply the exact mean. The proof of exchangeability there uses a symmetric urn.
- Janson–Kuba–Panholzer, arXiv:0805.4084v1, section 3.1, Theorems 1–2 and Remark 4: Gessel's bijection maps Stirling permutations to ternary increasing trees, carrying plateaux to empty middle slots. Its total empty-slot count and slot symmetry give a finite combinatorial route. Gessel's earlier credit through Park is acknowledged. The paper's introduction says descents correspond to plane-tree leaves; the detailed Janson contour map and direct inspection instead give plateaux. We use the actual maps, not that introductory sentence.
- Janson's 2013 corrigendum credits the first contour correspondence to Koganov (1996). The official primary PDF search excerpt was read, but direct PDF retrieval returned 502, so no complete downloaded corrigendum or hash is claimed.

Current title/alias searches and the 2023/2026 primary-source records were checked. No new or priority claim is justified. The candidate, if accepted, is a self-contained combinatorial reconstruction from established bijections. Its static inverse descriptions avoid relying on an inductive enumeration or recurrence. An independently reviewed proof-style verdict is required before final disposition.

The target page on unsolvedmath.com was unavailable; the complete pinned source record and original OWR page supplied the statement. Full PDF files are local audit inputs, not republished in the public packet.
