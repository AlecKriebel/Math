# Bounded literature check: Grassmann affine-SOS obstruction

Date: 9 October 2026. Target: the proposed no-finite-semidefinite-lift theorem for the oriented Grassmann orbitope C(4,12), and its consequence for affine-linear sums of squares on the unit real Grassmannian.

## Result

No inspected primary source states the complete proposed result or contradicts it. This is a bounded no-match, not a novelty certification. Important parts of the construction already appear in established literature, and a particularly close product-to-Slater reduction appeared in July 2026. A presentation of the candidate should acknowledge those antecedents and describe the result as a reduction to Fawzi, without claiming that the wedge embedding or the Slater convex body is new.

The check concerns literature status and exact theorem scope. It does not replace an independent proof audit. It does not produce an explicit bad calibration, determine the least dimension, or settle lower-dimensional cases.

## Exact external input

Fawzi’s published Theorem 1 expressly excludes a finite semidefinite representation of Sep(3,3). The definition on printed p.1320 permits arbitrary linear projections of finite-dimensional spectrahedra defined by Hermitian LMIs. Theorem 1 and the explicit reduction to Sep(3,3) and Sep(4,2) are on p.1321. This is the precise strength required by the candidate, stronger than failure of a particular hierarchy or of an unprojected LMI. The published paper was rechecked, including its comments distinguishing these weaker obstructions. No Grassmann, calibration, or Slater application was found in its text. [Fawzi, published PDF](https://www.repository.cam.ac.uk/bitstreams/e6e52df9-b317-4616-9462-c79a3cb4844b/download), [DOI](https://doi.org/10.1007/s00220-021-04163-2).

## Closest prior bridge

Paul, Zhao, and Dai, *Learning the closest Slater determinant*, arXiv:2607.20623v1, 22 July 2026, use the same isometry

J: C^d tensor C^d → exterior-square(C^d direct-sum C^d),
J(x tensor y) = x-up wedge y-down.

Appendix A.2, pp.16–17, Figure 7 and equations (A17)–(A32), maps product vectors to unit Slater determinants and identifies the maximum Slater fidelity of J M J*/Tr(M) with the separable support function of a positive observable M divided by Tr(M). Their Theorem 4 is a computational-hardness theorem, conditional on standard complexity assumptions for its algorithmic consequence. The primary arXiv record lists one version and no journal reference at inspection. [Primary record](https://arxiv.org/abs/2607.20623v1), [PDF](https://arxiv.org/pdf/2607.20623v1).

This is a close and relevant component-level antecedent. The inspected argument is expressed through fidelity/support functions; it does not state the candidate’s exposed Slater-state section as a convex-hull equality, the Kähler face of C(4,12), or the consequent Grassmann/calibration no-lift theorem. The candidate’s combination of those steps therefore was not matched, while novelty of the component embedding is unavailable.

## Earlier established components

Schliemann, Cirac, Kuś, Lewenstein, and Loss already define the compact convex set Sl1 of two-fermion states that are mixtures of elementary Slater determinants. This is the candidate’s intermediate body K on exterior-square C^6, in density-matrix notation. See Definition 1 and the following discussion, printed 022303-3 to 022303-4. Their special exact criterion applies to four one-particle states and is not an arbitrary-dimensional finite-LMI theorem. [PRA 64, 022303 (2001)](https://doi.org/10.1103/PhysRevA.64.022303), [published PDF](https://epub.uni-regensburg.de/28249/1/PhysRevA.64.022303.pdf).

The real-(p,p)-form/Hermitian-form correspondence and the decomposable generators of the strongly-positive cone are also standard background. An inspected modern formulation is Burgos Gil–Gubler–Jell–Künnemann, Definitions 2.1.1–2.1.2 and Proposition 2.1.3, preprint pp.6–8. This provides context for the candidate’s explicit matrix-to-(2,2)-vector map, rather than a no-lift result. [Primary preprint](https://arxiv.org/abs/2003.08644v3), [published article](https://doi.org/10.1007/s00209-021-02697-8).

## Grassmann and calibration status in the inspected sources

- Sanyal–Sottile–Sturmfels, *Orbitopes*, Theorem 7.6, preprint p.34, proves that G(3,6) and its polar are not spectrahedra. The final paragraph of §7, p.35, explicitly leaves their representation as linear projections of spectrahedra unresolved. It cannot be substituted for a no-finite-lift theorem. [arXiv v4](https://arxiv.org/abs/0911.5436v4), [journal DOI](https://doi.org/10.1112/S002557931100132X).
- Rostalski’s BIRS slides dated 15 February 2010 use affine SOS forms for supporting linear functions, prove TH1 exactness for k=2, and give numerical evidence for higher k. Slides 17 and 21 explicitly distinguish tests from a general theorem. [Primary slides](https://www.birs.ca/workshops/2010/10w5007/files/rostalski.pdf).
- Sanyal’s 2015 Oberwolfach report, printed pp.708–709, conjectures degree-at-most-one SOS certificates relative to the unit-sphere/Plücker ideal and reports n≤7 experimental evidence. It identifies the relation to Harvey–Lawson Question 6.5. [Report](https://ems.press/content/serial-article-files/46561).
- Harvey–Lawson’s Question 6.5, printed p.68, asks for a local differential-form completion of the comass inequality to a norm identity on simple vectors. Its affirmative statement concerns the geometries treated in that article. It is not a universal affirmative theorem. [Original article](https://doi.org/10.1007/BF02392726).

## Nearby obstructions that must not be conflated

Bettiol–Kummer–Mendes prove that the cone of nonnegative quadratic forms on the real points of Gr(k,n) is not a spectrahedral shadow when n≥5 and 2≤k≤n−2: Corollary 4.2, preprint p.17. Remark 4.3 identifies the associated orbit representation as Sym²(exterior-power R^n). The candidate instead concerns the convex hull of oriented unit decomposable vectors in the exterior power itself. The representations and function degrees differ; the cited theorem does not literally state the candidate. [Final revised preprint](https://arxiv.org/abs/1908.03713v2), [published article](https://doi.org/10.1137/20M1350777).

Scheiderer’s Theorem 4.23 gives polynomial images with convex hulls lacking lifts; Corollary 4.25 treats nonnegative-form cones. Neither specifies the candidate’s fixed Plücker embedding. [Primary preprint](https://arxiv.org/abs/1612.07048v3).

Kobert–Scheiderer’s positive Theorem 4.2 requires a polar representation. Their §4.1 distinguishes Grassmann nonspectrahedral examples from nonprojected-representable examples in other representations. It supplies no blanket positive theorem for all Grassmann orbitopes. [Primary preprint](https://arxiv.org/abs/2010.02045v1), [published article](https://doi.org/10.1007/s00229-021-01337-z).

## Bounded conclusion

The safe literature statement is: the proposed theorem is an elementary reduction to Fawzi’s established obstruction, using classical Kähler/positive-form and Slater-state constructions, with a close recent product-to-Slater antecedent. This search found no primary source stating the complete Grassmann no-lift/calibration consequence. Whether that combination has appeared elsewhere remains unestablished.
