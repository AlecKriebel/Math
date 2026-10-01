# Result after five author turns: original target unresolved

Problem 30004757 / OWR-8415338-004. **Five substantive author turns completed.** The precise finite-separation tangent cones, their Hessian transitions, and the general polyhedral/Y-shaped classification have not been determined. No full-resolution or novelty claim is made.

The following partial results are saved for independent review:

1. **Axisymmetric two-mass C¹ description (turn1).** The graph tangent cone is C¹ off the inward ray; its subdifferential on that ray is exactly the shared contact disk. This does not prove higher regularity.
2. **Exact local and homogeneous models (turns2–3).** A radial partial Legendre transform produces a degenerate PDE. Separated local solutions and an anisotropically homogeneous two-plane obstacle model yield compatible rim exponents and constants. No convergence or matching theorem identifies them with the global source solution.
3. **Non-axisymmetric structural reduction (turn4).** A correctly localized 2025 theorem restricts extra exposed faces penetrating an affine chamber to interface-bridging segments in dimensions 3 and 4. Interface rims are not controlled. A conditional angular expansion determines the next radial coefficient from an already known cone, not the cone itself.
4. **Global collision-limit theorem (turn5).** A genuine source-type two-mass family, with fixed isotropic normalization and optionally fixed individual atom weights, has individual tangent bodies converging to half-balls while the merged potential has a full-ball tangent body. This prevents uniform C^{2,β} estimates across collision, but gives no counterexample to fixed-separation smoothness.

The outstanding theorem would select and control the actual finite-separation crease profile and resolve the unknown interface-rim and bridging-segment geometry. The saved reductions do not establish it. The attempt is exhausted; independent verification is separate from author search and must not add a sixth search turn.

## Verification controls

- `reduction_verification.json`: 20 exact symbolic identities for turn2
- `rim_model_verification.json`: 12 exact symbolic identities and cross-model checks for turn3
- `angular_verification.json`: 8 exact determinant/calibration checks for turn4

These are algebra controls. They are not numerical PDE solutions or proofs of the missing matching estimates. Turn5 is an analytic comparison/contact-convergence proof and makes no numerical claim.

## Source and attribution

The original real Alexandrov problem, normalization, and nearby record boundaries are in `EXACT_SCOPE.md`. The main construction, barriers, and duality are credited to Mooney, with higher-dimensional and stability work credited to Mooney–Rakshit. The dimension and exposed-point regularity inputs are credited to Jin–Tu–Xiong and Huang–Tang–Wang. The models use classical Pogorelov-type mechanisms. The limited literature search does not certify a new contribution.

The complete author-turn history is `turn_ledger.json`. This was a new, unassigned target according to the recovered inventory; no interrupted history was reset. The campaign-wide state/history files were touched only by the isolated turn1 checkpoint; their generated queue/catalog changes were restored. All later counts are local to this attempt. Publication, if separately authorized after review, must update only this target's queue row and must mark the original target unresolved.
