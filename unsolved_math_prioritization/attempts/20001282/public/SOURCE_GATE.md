# Source, scope, and novelty gate

Problem 20001282 / AIM-CONVEX_GEOMETRY-0014. Checked 2026-10-03.

## Exact original target

The official AIM 2010 Mahler-duality list, printed page 3, numbers Kuperberg's fixed-combinatorial-type question **18**. It asks about all centrally symmetric three-dimensional face types except cube/octahedron, first excluding local minima and then asking for a unique critical affine orbit that is a local maximum.

Primary source: https://aimath.org/WWN/mahlerduality/mahlerduality.pdf

The problem landing page https://www.unsolvedmath.com/problems/20001282 was not accessible through the web reader. The official AIM PDF was accessible through the reader, including the surrounding numbered questions. A direct HTTP attempt to download the AIM PDF returned 403. The primary parsed PDF, rather than the product-prism queue title, controls the mathematical statement.

## Literature that changes the answer

- Meyer–Reisner's classical shadow-system theorem supplies convex reciprocal polar volume and affine rigidity. The full arXiv PDF was inspected at Theorem 1 and Proposition 7. https://arxiv.org/abs/math/0606305
- Chen–Li–Xi–Xu's **2026 preprint** supplies type-preserving symmetric admissible speeds and the primal/dual dimension count. The fixed-type no-minimum result follows from Proposition 3.8 and Lemmas 4.1 and 5.2, with polarity. This is a mathematical inference from their local statements, not a quotation of a theorem explicitly named “Kuperberg's Question 18.” https://arxiv.org/abs/2605.13795v1
- The arXiv submission record shows v1 on 13 May 2026; the downloaded PDF is dated 14 May 2026. Its experimental HTML displays a different document date. This note pins the v1 identifier and PDF, and does not infer a revision history or publication from that display difference. No journal reference was shown in the inspected arXiv metadata.
- The symmetric three-dimensional Mahler bound itself is established by Iriyeh–Shibata. It must not be confused with the stronger fixed-type local statement. https://arxiv.org/abs/1706.01749
- Alexander's 2017 BIRS lecture announces that the double cone over a regular hexagon maximizes volume product among symmetric three-polytopes with at most eight vertices, with value 12. This is prior evidence against novelty of the maximum. https://archive.birs.ca/files/2017/17w5074/files/Alexander_Banff.pdf
- The author-hosted/arXiv paper *Polytopes of maximal volume product* and its publisher abstract were also checked. A specific symmetric eight-vertex theorem was not located there; the conference announcement should not silently be promoted to a verified theorem in that journal paper. https://arxiv.org/abs/1708.07914 ; https://doi.org/10.1007/s00454-019-00072-3

No primary source was found proving or refuting the universal unique-critical-orbit assertion. No all-critical-point theorem for the complete hexagonal-bipyramid chart was located in this bounded search. Neither negative search establishes novelty.

## Prior-attempt and scope check

The live main-branch queue was read and rank 509 was still queued. Repository searches for 20001282 and Kuperberg, and all-state PR searches for 20001282, AIM-CONVEX_GEOMETRY-0014, Kuperberg, Mahler, and “volume product” returned no matches. The nearby convex-geometry attempt 20001284 concerns star-body section perimeters and is mathematically different. These checks support proceeding with this record; search coverage is not an exhaustive history proof.

No remote write, branch creation, commit, pull request, or queue edit was performed in the author stage. The public package contains only authored notes and exact-check code/output. Source PDFs, complete source extracts, and retrieval records are excluded.

## Claim boundaries for review

1. General no-minimum theorem: a deduction from current preprint machinery, with a self-contained geometric/counting exposition and classical analytic input. No first-solution claim.
2. Full hexagonal-bipyramid/prism critical classification: explicit exact verification, including the transverse nonplanar-equator coordinate; no priority claim.
3. Universal critical-point uniqueness and maximality: unresolved here. Overall classification remains partial.
4. Finite computations support the formulas and examples; they do not certify the universal statements or literature completeness.
5. A fresh independent audit must check full chart coverage, equality-case use in the shadow theorem, preservation of the dual type, the dimension count, and the scope of the conclusion before publication.
