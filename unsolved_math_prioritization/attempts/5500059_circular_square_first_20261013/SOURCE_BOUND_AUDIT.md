# Source and admissibility audit: Most Circular Partition of a Square

## Scope and current disposition

This audit concerns TOPP Problem 59, also catalogued as 5500059 / AMR-054-0059. It distinguishes published assertions, explicitly conjectural statements, independent mathematical repairs, and independently checked coordinate constructions. It does not claim to settle the optimum or establish novelty by an exhaustive literature search.

The problem minimizes the largest circumradius/inradius ratio among convex polygonal cells covering the whole square with pairwise disjoint interiors. The two circles need not be concentric. Inscribed disks of adjacent cells need not touch. A boundary strip alone is not a solution.

For finite partitions, a precise working quantity is the infimum of this maximum over finite families of compact convex polygons with nonempty interiors. This is a normalization for the present finite results, not a proof of equivalence to every possible interpretation allowing arbitrary infinite partitions. TOPP does not explicitly insert “finite”; the paper uses an indexed collection, maximum, and minimum, while discussing infinite limiting behavior. Infinite collections can fail to have an attained maximum; finite boundary-chain arguments cannot silently be applied to accumulation points. Neither the existence of a finite optimum nor equality with an unrestricted infinite-partition formulation is assumed here.

## Primary sources and frozen identities

1. Mirela Damian and Joseph O'Rourke, *Partitioning Regular Polygons into Circular Pieces I: Convex Partitions*, arXiv cs/0304023v1, https://arxiv.org/abs/cs/0304023v1. Recovered PDF: 879230 bytes, SHA-256 3ed91112d1280fde3b09727747819dd8ed59656a68b6493323a244b6b47f03ac.
2. Same authors and title, arXiv cs/0304023v2, https://arxiv.org/abs/cs/0304023v2. Revision submitted 8 February 2026. Recovered PDF: 852003 bytes, SHA-256 5652cd7d9143d33427b4b022010f966903b6fd103df5b28b7020de89b5ac1f76. The PDF title page itself displays 10 February 2026; submission metadata and printed date are recorded distinctly.
3. TOPP Problem 59, https://topp.openproblem.net/p59. Its visible revision history is 16 August 2004. The current page reports the problem open and the interval [1.28868, 1.29950].
4. Claudia Obermaier and Markus Wagner, *Towards an Evolved Lower Bound for the Most Circular Partition of a Square*, IEEE CEC 2009, pp. 1463–1469, DOI https://doi.org/10.1109/CEC.2009.4983115. Author-hosted PDF https://cs.adelaide.edu.au/~markus/pub/2009cec.pdf: 659188 bytes, SHA-256 8976c5e656d3ea7884c1980a79fce5f9d3349844bbd51501b8892825b6626aa3.

The complete recovered v2 text was read, and its normalized text was compared with v1 across the whole paper. The mathematical scrutiny below is focused on square-related statements, not a certification of all results about other regular polygons. Printed v2 pages 14–19 were also rendered and visually inspected to rule out extraction artifacts in the decisive formulas. The 2009 paper was read in full. Source PDFs and extracted text remain private; this report contains authored analysis and bibliographic metadata.

## What the sources actually assert

The general interval [1.28868, 1.29950] remains stated in v2 Table 1 and Section 5.5. The lower endpoint is assigned to Theorem 12 and the upper endpoint to the complete 92-piece Figure 16 construction. The source gives no full coordinate/radius certificate in the inspected text. The isolated number 1.29550 in the introductory roadmap to Section 5 is inconsistent with Section 5.2, Figure 16, Table 1, and Section 5.5; it should not be promoted into a stronger upper bound.

Figures 20–21 and 25 cover boundary regions while leaving the interior unfilled. Their reported qualities, 1.28898 and 1.29650, are consequently not full-square upper bounds. Restrictions to boundary pentagons or hexagons, with numbers 1.31408 and 1.29625, are explicitly presented without proof in Section 5.1–5.2.

The February 2026 revision changes the restricted tangent-indisk assertion 1.28939 from v1 Lemma 19 (printed p. 18) to v2 Conjecture 1 (printed p. 19). This is also disclosed by the arXiv abstract-page comments. The restriction requires neighboring boundary indisks to touch; it is not imposed on the original problem. The finite-attainment conjecture is renumbered Conjecture 2. The normalized whole-paper comparison found these substantive changes in Section 5.4, corresponding renumbering, date changes, and layout changes; the earlier general bound was not withdrawn by this revision.

The 2009 evolutionary study reports no improvement over the earlier complete construction. Its short-run best value is 1.3405, and its discussion describes the failure to improve the earlier best partition. The title and some prose call a constructive target a “lower bound”; under the minimization convention such a successful construction would provide an upper bound. The paper is evidence of a subsequent search attempt, not an improved bound.

A bounded search used the exact problem title, the original paper title, and the distinctive number 1.28868; the 2009 study was followed to its author-hosted PDF and institutional bibliographic record. This is not a complete citation census. Search-result timestamps are not publication dates. The nonconvex companion arXiv cs/0412095 treats a different admissible class and does not resolve this convex problem.

## Presentation errors and missing reductions in Section 5.3

The following observations are about the printed argument as written; they are not an assertion that the intended lower bound is false.

- Lemmas 13–14 print a minimum of two cell ratios, although their balancing argument bounds the maximum. A lower bound for a partition only requires one difficult cell. Replacing this minimum by maximum repairs that logical target, but does not on its own supply the geometric reductions.
- Lemma 13's second angle-order assumption and the opening of Lemma 14 use opposite inequalities for the same next boundary angle. A finite-chain selection argument is needed instead of accepting both simultaneously.
- Identifying a circumradius with half a chord is generally too strong; half the chord is a lower bound. Likewise an arbitrary maximal indisk need not be tangent to every boundary support under discussion. Explicit support inequalities are needed.
- In Lemma 14 the normalization is r_B=1, so the ratio equals R_B, not 1/R_B. The displayed system itself simplifies correctly: with t=tan(theta/2), x_o=(t+t^(-1))/2, one gets R_B=x_o^2+1/4 and y_o=x_o^2-1/4. The printed reciprocal is inconsistent with both this system and the numerical ratio greater than one.
- Lemma 15 uses the optimal-value notation where a statement about each finite partition's attained ratio is intended. Strict inequality for every finite partition does not by itself make the infimum strictly larger. Its next-angle/termination step requires a finite boundary-chain argument.

Independent reconstruction can replace these omitted steps without requiring concentric circles or neighboring disk tangency. A final acceptance of any reconstructed proof is attached separately to the exact reviewed artifact bytes.

## Concrete range defect in Lemma 16

As a formula for every slant angle, the asserted minimum 1/4+csc(theta)^2 is false. At theta=60 degrees, take a unit disk centered at (sqrt(3),1), horizontal support y=0, and the two parallel supports of slant 60 degrees. Their feet on y=0 are b=(0,0) and c=(4/sqrt(3),0). The circle centered at (3sqrt(3)/4,3/4) of radius 3/2 contains the disk: the center distance is 1/2. It contains b with equality and c because the squared distance to c is 19/12 < 9/4. Thus the alleged minimum 19/12 is too large. The true minimum here is 3/2, also forced by b and the unit disk.

The three-active-constraint expression does hold in the relevant near-right-angle branch. For 0<theta<=90 degrees the corrected disk-plus-two-feet envelope is

F(theta)=(1+csc(theta/2))/2 for theta<=2 atan(1/sqrt(phi)),
F(theta)=1/4+csc(theta)^2 thereafter,
where phi=(1+sqrt(5))/2.

At the transition the optimal circle changes from one endpoint plus the disk to both endpoints plus the disk. The balancing angle near 78.87 degrees lies in the second branch. Consequently the range defect does not refute the intended numerical lower endpoint, but citing Lemma 16 without its valid range is insufficient.

## Limits of illustration-based verification

A plotted PDF graph can identify a construction's combinatorics, but rounding, line-coordinate mismatch, and omitted centers prevent treating its visual appearance as an exact certificate. A new optimized coordinate set must independently prove that all cells are convex, their interiors are disjoint, their union is the square, and each has a feasible indisk and enclosing circle meeting the claimed ratio. Those four checks are separate from floating-point optimization and from the published drawing's label.

## Open issues retained

The exact optimum, finite attainment, and unrestricted infinite admissibility remain unresolved by this source audit. No assertion is made about lifetime proof-attempt counts; recovery established source triage, not that no earlier substantive attempt ever occurred. A newly documented pass and a globally first attempt are different claims.
