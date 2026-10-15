# PR 672 independent geometry review

Target 6700060; original head `13d9b2d944ce8ec121381a4bc21e48d2bb19846e`; selected immutable queue status `claimed_solved`. The controlling README is the qualified result being reviewed. This is one geometry and scope approach family, independent of the parent analytic and priority gates.

**Verdict: qualified geometric pass; zero mandatory findings and zero optional findings.** The Euclidean pullback application of the stated Bi Theorem 1.1 is valid under the explicitly required ambient-smooth, face-preserving map and inverse. The planar argument is valid. No geometric repair is needed to that scoped claim.

This review does not prove Bi's analytic theorem from its foundations, make a novelty claim, settle current community acceptance, or determine whether the PR should be merged or closed. It specifically does not promote the submitted statement to arbitrary corner-singular, facewise-smooth, interior-smooth, or merely combinatorially equivalent competitors.

## Independent source inspections

Fresh primary-source PDFs were downloaded to this review's excluded `tmp` directory and matched the prior submitted hashes byte-for-byte:

- Gromov, *101 Questions, Problems and Conjectures around Scalar Curvature*, October 1, 2017: SHA-256 `1478b4025eb55e7237ab3f066e8924938a1de4cd407d74893b49f2b9007d9645`, 1,430,132 bytes. Read complete Section 22, printed pp.60–61, and visually inspected those two full pages. The original Question 64 asks the extremal-to-mean-convex-extremal implication, with corresponding faces, nonnegative face mean curvature, weak angle comparisons everywhere, and strictness somewhere. It introduces no distance-decreasing or fixed-boundary-metric assumption.
- Gromov, *Dirac and Plateau Billiards in Domains with Corners*, author manuscript dated September 20, 2013: SHA-256 `63f6ac985ad59f2cdbee6465b948171bad03fbc322548c92a1fdf1da4ca11761`, 681,225 bytes. Read Section 1 pp.2–3 and related mean-convexity and extremality passages in Sections 1.2, 1.5–1.6; visually inspected the full pp.2–3. Ambient extension and the restricted ambient tangent bundle support the convention used in the controlling README. The 2017 paragraph does not itself resolve all broader readings of 'diffeomorphic'.
- Bi, *Dihedral Rigidity for Convex Polytopes by Smooth Approximation*, arXiv:2608.06320v1: SHA-256 `49cfd90c34f7e87e72daf088721e7e0cc30f44e49d1be06be74d951ad4a33ab1`, 449,303 bytes. Read complete setup and Theorem 1.1 pp.1–2, geometric Lemmas 2.1–2.2 and nearby corner/ridge setup, and final angle-recovery/even-dimension proof pp.17–18. Visually inspected full pp.1–2. The theorem requires a smooth metric on a neighborhood, R>=0 on P, H>=0 on facets, and reversed exterior-angle comparisons on all ridges; its conclusion includes the normal-pairing equality needed here. There is no simple-polytope, acute-angle, extra spin, or upper-dimensional hypothesis in its statement.

Raw sources and renderings are inspection intermediates, not publication-package content. The report's mathematical derivations are independently authored in `DERIVATION.md`. Full theorem-proof validation belongs to the separate analytic review; this review does not reuse the submitted audit's verdict as evidence that the imported theorem is correct.

## Adversarial checks and conclusions

1. **Corner differential and metric extension.** Smoothness of F and its inverse in ambient extensions forces dF invertible at the boundary by the interior chain rule and continuity. Local pullback tensors patch to a smooth positive-definite neighborhood tensor. The partition does not corrupt curvature on P: all jets there are determined by their common interior restriction. R_g=0 extends to closed corners. Curvature outside P is not an assumption of the source theorem.
2. **Normals, curvature and orientations.** Face preservation and the inward side determine the outward normal even if F reverses orientation. Isometry invariance preserves II and H. Explicit affine reflections and a nonlinear flat pullback verify the signs; a nonlinear shear supplies a hostile flat example with one negative face mean curvature, preventing any mistaken inference from scalar flatness to mean convexity.
3. **Dihedral convention.** The actual interior wedge angle is pi minus the outward-normal angle, including nonacute wedges. Thus the interior comparison reverses exactly as required by Bi. An acute unoriented tangent-plane angle would lose necessary information and is not used.
4. **All points and one strict point.** The conclusion is normal equality on closed intersections, not only an almost-everywhere or relative-interior assertion. It rules out the original one-point strictness criterion. Continuity also prevents a strict deficit confined to a smooth ridge endpoint.
5. **Nonsimple corners.** An irredundant convex ridge has exactly two incident facets; triple intersections have codimension at least three. This does not require a simple polytope. However a smooth corner correspondence must linearly identify tangent cones, a real restriction at nonsimple vertices.
6. **Dimension range.** The source statement covers all n>=3. The final product passage preserves scalar curvature, side mean curvature and old normal pairings; end facets are totally geodesic and new angles are pi/2. The submitted n=2 proof follows from the signed turning theorem for an embedded disk. n=1 is vacuous for the strict codimension-two condition.
7. **Planar signs and strictness.** A counterclockwise unit circle has both signed turning curvature and outward sphere-positive mean curvature +1. One strict angle decrease raises total corner turning beyond 2pi, forcing negative integrated smooth curvature. The proof needs no uniform strict deficit or convexity of each full higher-dimensional second fundamental form.

## New exact diagnostics

`independent_controls.py` performs 106 checks under both ordinary and optimized Python, with identical output. It uses exact symbolic and rational arithmetic and explicit failures, not assertions disabled by optimization. Groups cover a nonlinear pullback and its full Riemann tensor, both curvature signs, reflected affine normal identities, nonacute interior/exterior angle comparisons, degeneracy of a weak corner map, the product metric, and one-point planar strictness.

A new finite construction makes the category restriction independently checkable. Two pentagonal pyramids have strictly convex bases

    ((0,0),(2,0),(3,1),(2,3),(0,2))
    ((0,0),(2,0),(3,1),(2,3),(-1,2))

in z=1 and common apex 0. For each of their ten incidence-preserving apex-ray correspondences, the homogeneous linear system for a possible derivative A and five ray scales has rank 14 in 14 unknowns. Thus no nonzero A, and in particular no ambient smooth corner diffeomorphism, exists. These are combinatorially equivalent convex polytopes. The construction does not assert that their dihedral angles satisfy the prohibited inequalities; it demonstrates the logical failure of replacing ambient smoothness with combinatorial equivalence.

The separate weak-map model F(x,y)=(x^3,y) on a square has degenerate pullback diag(9x^4,1) at x=0, although its inverse is smooth on open strata. This rejects direct use of a merely stratum-smooth correspondence. It is not a counterexample to the scoped theorem.

## Strongest verified statement and remaining gaps

Accepting Bi's analytic Theorem 1.1, every compact full-dimensional convex Euclidean polytope in n>=3 has the stated mean-convex extremality against ambient-smooth face-preserving competitors. In n=2 the same statement is proved independently by turning. Thus the requested implication holds in the explicitly qualified category; reference convex extremality is not needed there.

The exact remaining category gap is any allowed competitor for which no corresponding nonsingular ambient smooth map and inverse exists. No replacement reduction for that category has been proved here. The source's analytic validity, the priority disposition, publication suitability, and any interpretation broader than the controlling README remain separate gates. These are recorded scope boundaries, not newly found defects in the scoped submitted proof.

No original packet, shared Git state, PR, tracker, or cloud record was changed by this review. No external individual or other shard agent was contacted.
