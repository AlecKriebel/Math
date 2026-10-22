# Mathematical scope and public sources

Prepared 2026-10-20. Identifier: AMR-030-0003 (3100003).

## Exact target

For every fixed non-equilateral, nondegenerate Euclidean triangle T = {a,b,c} in R², does there exist a function c_T: R² → {1,2,3} such that, for every Euclidean isometry g, the three values c_T(g(a)), c_T(g(b)), c_T(g(c)) are not all equal?

The quantifier order is **for every T, there exists c_T, for every congruent copy of T**. The coloring can depend on shape and size. No universal coloring avoiding every triangle is required. All plane points, reflected copies, and boundary points are included. Scale is fixed, and only vertices are colored. There is no measurability, periodicity, or polygonal regularity assumption. Equilateral triangles already admit two-color avoidance; this package retains the non-equilateral target and the ordinary nondegenerate interpretation.

## What is and is not established

1. **Stripes.** The ellipse/open-hexagon criterion is exact, with strict inequalities essential at tangencies. The quantitative lower cutoff proves finite decidability of the all-width stripe problem for algebraically specified triangles. The supplied code implements only the rational fixed-width test. The all-width algorithm has not been implemented or run end to end, including for the displayed flat triangle. Failure at width equal to the minimum altitude is not failure at every width.
2. **Polygonal certification.** The finite offset reduction, strict linear elimination, and quadratic sign procedure provide a proof of decidability for a supplied algebraic periodic polygonal coloring. This general verifier is not implemented here. No positive avoiding candidate for every triangle or complexity bound on necessary candidates is supplied.
3. **Finite menus.** For every fixed finite menu of regular three-colorings, there is an epsilon such that every member contains each isosceles triangle of side lengths (1,1,b) with 0<b<epsilon. The menu is fixed before epsilon is chosen. This does not exclude a new coloring selected separately for each b, or arbitrary irregular colorings.
4. **Grids and rational points.** The fixed-triangle hypergraph on a square lattice, and on Q², is two-colorable. This does not extend those colorings to R². Density does not preserve exact congruence. Finite-grid computations cannot settle the unrestricted plane conjecture.
5. **Overall status.** No all-triangle three-color construction or counterexample to the unrestricted conjecture is established. These are partial results only; neither current-openness certification nor earliest-priority certification is claimed.

## Public source chain

The following links identify the problem and contextualize known partial results. The source inspection supporting these notes was completed on 2026-10-20; this package does not reproduce the source documents.

- Joshua Cooper, *Combinatorial Problems I Like*, Euclidean Ramsey Theory section, third problem. https://people.math.sc.edu/cooper/combprob.html . This is the problem-list source, attributing the question to Graham and specifying monochromatic congruent copies. The page reports its last edit as October 2020.
- Ron Graham and Eric Tressler, *Open Problems in Euclidean Ramsey Theory*, Conjecture 2 on manuscript page 1 and stripe discussion on page 2. https://mathweb.ucsd.edu/~ronspubs/10_14_euclid.pdf . Chapter DOI: https://doi.org/10.1007/978-0-8176-8092-3_7 . This confirms the fixed-triangle three-color target; the distinct two-color conjecture is not this problem.
- Oswin Aichholzer and Daniel Perz, *Triangles in the colored Euclidean plane*, EuroCG 2019, pp. 10:1–10:7. https://www.eurocg2019.uu.nl/papers/10.pdf . Problems 1–2 include reflected copies; Theorems 3.1–3.2 provide existing stripe coverage. The document identifies itself as an extended abstract/preprint, not a formally reviewed paper. Known sufficient stripe families are not counted as new here.
- Alexander Natalchenko and Arsenii Sagdeev, *Monochromatic triangles in the max-norm plane*, arXiv:2302.09972v2, 7 April 2024. https://arxiv.org/html/2302.09972v2 . Journal DOI: https://doi.org/10.1016/j.ejc.2024.103977 . Its introduction reports the Euclidean three-color bound as conjectural and seven as the known general upper bound. The paper's completed classification concerns the maximum norm, not Euclidean congruence.
- Gabriel Currier, Kenneth Moore and Chi Hoi Yip, *Avoiding short progressions in Euclidean Ramsey theory*, arXiv:2404.19233v3, 30 May 2025. https://arxiv.org/html/2404.19233v3 . This later work concerns collinear progressions and does not resolve the present all-triangle question.

The strongest recent directly inspected primary status statement for this exact conjecture in the source review is dated April 2024. Targeted searches through 2026-10-20 located no later full resolution, but absence from search results does not prove current openness. The defensible literature description is: **open in inspected primary literature; no later resolution located**. This package makes no exhaustive-literature or historical-origin claim.
