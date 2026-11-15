# Negative answers to the printed totally mixed face questions

Alec Kriebel · 17 October 2026 · Version 1.0.0 · Unrefereed preprint

## Original abstract

For two polytopes, retain the faces of their Minkowski sum whose two canonical summands have positive dimensions and whose dimension is the sum of those dimensions. This is the definition in Payne’s printed Oberwolfach question. Let D be the standard four-simplex and I = [0,1]. For the full-dimensional lattice polytopes D × I and (−D) × I in ℝ⁵, the qualifying-face order complex is a disjoint union of two connected pure graphs, each with 50 vertices and 60 edges. Its rational Betti numbers are (2,22,0,…). Thus both printed assertions, shellability and the homology of a wedge of three-spheres, fail. The shared interval factor deliberately produces a nongeneric example. The argument concerns the printed additive-dimension definition; it does not settle shellability for the different mixed faces used in stable tropical intersections.

## Overview

A Minkowski sum adds every point of one polytope to every point of another. Each exposed face has canonical faces from the two summands. The printed question keeps only faces where both summands have positive dimension and their dimensions add exactly.

For two explicit lattice polytopes in five dimensions, the resulting face-inclusion complex splits into two loop-filled graphs. This gives negative answers to both the shellability and sphere-wedge homology assertions in the printed question.

## Result

Let D = conv(0,e₁,e₂,e₃,e₄) be the standard four-simplex and I = [0,1]. Both P₁ = D × I and P₂ = (−D) × I are full-dimensional lattice 5-polytopes.

Retain F = F₁ + F₂ when its canonical summands, exposed by the same functional, satisfy dim F₁ > 0, dim F₂ > 0 and dim F = dim F₁ + dim F₂. Form the ordinary order complex: its vertices are qualifying faces and its simplices are nonempty strict chains. No artificial minimum or maximum is adjoined.

This complex is K ⊔ K. Each K is a connected pure graph with 50 vertices and 60 edges, homotopy equivalent to a wedge of eleven circles. The ordinary rational homology is H₀ = ℚ², H₁ = ℚ²² and Hⱼ = 0 for j ≥ 2. The complex is not shellable under either pure or standard nonpure shellability, and it does not have the homology of a wedge of three-spheres.

## Why it works

Proper nonempty faces of the simplex difference D−D are indexed by nonempty disjoint subsets A,B of its five vertex labels. Their dimensions add, and inclusion is exactly containment in each label set. The positive-dimension filter keeps the size pairs (2,2), (2,3) and (3,2): 30 minimal faces and 20 maximal faces, with 60 comparabilities and no three-element strict chains. Their graph K is connected.

The common interval factor is decisive. Qualifying faces with a nonzero interval coefficient in their exposing functional form the two endpoint copies of K. With zero coefficient, each summand gains an interval direction but the sum gains only one, so exact dimension additivity fails. The full-base end faces and the whole sum fail the filter too; no qualifying face links the two copies.

Each connected graph has 60−50+1 = 11 independent cycles. In any proposed shelling, the first edge from the second component meets the earlier edges only in the empty face, rather than the required zero-dimensional intersection. This rules out both shellability conventions. Two components and nonzero first homology also rule out the printed sphere-wedge target.

The paper gives the complete analytic face argument. Two exact standard-library checkers accompany it as supplementary verification; the proof does not depend on running them.

## Definitions and limits

The shared interval deliberately makes this example nongeneric. Payne’s printed Problem 3 states no general-position condition. No generic-perturbation theorem, minimum-dimension claim, historical firstness or present worldwide openness is asserted.

The exact-additivity filter is different from Adiprasito’s public 2020 manuscript underlying a 2024 article, which requires dim(Σ_{i∈J} Fᵢ) ≥ |J| for every nonempty index subset J. A vertical face with summand dimensions 2 and 2 and sum dimension 3 passes those lower bounds but fails exact additivity. This note does not contradict that stable-intersection theorem or settle its shellability question.

Adiprasito and coauthors’ colorful-Gale “totally mixed” convention instead requires facets of the summands. Hiatt–Simpson–Wang–Wu v2, Section 8, concerns a different Schön subvariety of (ℂ*)⁸ and its tropical link; no identification with this two-summand face poset is supplied.

## Earlier work

Canonical Minkowski face decomposition and simplex-difference geometry are classical. Fukuda–Weibel provide the general decomposition statement, and Sturmfels–Tevelev’s scaled opposite tetrahedra give the earlier six-point homology control. That zero-dimensional complex is shellable, so it does not by itself prove nonshellability. The common-interval construction supplies the positive-dimensional disconnected example here.

## Paper and supporting files

Read the complete unchanged four-page paper below, open or download its original PDF, or download the complete original source-and-verification ZIP.

## Collaboration

Independent verification, a substantive comparison of the face definitions or work toward a journal submission would be welcome. Collaboration and authorship would reflect actual contributions.

## AI assistance and review status

AI tools were used extensively in developing, checking, researching and writing this note and its supporting materials. This is an unrefereed preprint; adversarial AI checks are not external human peer review, journal acceptance or formal proof-assistant certification.

## License

The note and original authored supporting materials, including verification code, are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). Cited third-party works retain their own rights.

## Related literature

- [Payne: The complex of totally mixed faces](https://doi.org/10.4171/OWR/2019/39). Problem 3, Oberwolfach Report 39/2019, p. 2464: the printed positive/exact-additivity question.
- [Fukuda–Weibel: On f-vectors of Minkowski additions of convex polytopes](https://arxiv.org/abs/math/0510470v4). Lemma 4 of arXiv v4: canonical Minkowski face decomposition.
- [Sturmfels–Tevelev: Elimination theory for tropical varieties](https://arxiv.org/abs/0704.3471v1). Examples 1.3 and 4.10: the classical opposite-tetrahedron and six-ray antecedent.
- [Björner–Wachs: Shellable nonpure complexes and posets. I](https://doi.org/10.1090/S0002-9947-96-01534-6). The standard nonpure shellability and strict-chain order-complex conventions.
- [Adiprasito and coauthors: Colorful simplicial depth, Minkowski sums, and generalized Gale transforms](https://doi.org/10.1093/imrn/rnx184). The distinct facet-based “totally mixed” convention.
- [Adiprasito: A note on the topology of polyhedral hypersurfaces and complete intersections](https://webusers.imj-prg.fr/~karim.adiprasito/cint.pdf). Public manuscript, 27 July 2020, Corollary 1.3: the broader subset lower-bound criterion. The related 2024 publication has a different title. [2024 publication](https://doi.org/10.4310/PAMQ.2024.v20.n1.a2).
- [Hiatt–Simpson–Wang–Wu: Topology and Euler characteristics of tropical varieties](https://arxiv.org/abs/2606.10817v2). Revised v2, 24 July 2026, Section 8: a different Schön variety in (ℂ*)⁸.

## Citation

Alec Kriebel. Negative answers to the printed totally mixed face questions. Version 1.0.0. Zenodo, 17 October 2026. doi:10.5281/zenodo.23440943.
