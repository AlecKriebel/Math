# Final manuscript and verifier audit

**Checkpoint:** 2026-09-23 03:39:00 UTC. **Completion estimate:** 100% of this bounded final adversarial review.

**Verdict:** PASS. No blocking mathematical, source-alignment, computational, or PDF presentation defect was found in the reviewed versions. The manuscript supports an explicit negative answer to the printed Question 3(e); it does not claim a guaranteed historical first resolution.

## Reviewed versions

SHA-256 hashes at this checkpoint:

| Artifact | SHA-256 |
| --- | --- |
| `manuscript/paper.tex` | `15af70080eda544f688a86a4b08f39b55bc934a1b5d56a0740c9c83d969e8bce` |
| `output/pdf/paper.pdf` | `cc4bfb582249cfeacb01400d50132bb1c76010876ae40f3f23efd91d2bfb23ee` |
| `verification/verify_exact.py` | `0e3faf4cd457e47dff4084d7d5de39b82507059fa5b61a426c6d59901699094f` |

The PDF contains four pages. I read the complete TeX, compared the extracted PDF text with it, and visually inspected all four rendered pages. The displayed equations, theorem statements, cross-references, attribution, references, and disclosures agree. No clipped equations, missing symbols, overlaps, or broken references were observed.

## Adversarial mathematical checks

1. **Correct question and notion of flatness.** The manuscript matches the printed item 3(e) and the alpha-equals-one formula verified in the first source audit. It keeps the excluded center, admits Levi-Civita structures, and distinguishes statistical 1-conformal flatness from ordinary Riemannian conformal flatness.
2. **Every center and convex neighborhood.** The first variation applies to the smoothly varying connecting geodesic on each convex neighborhood. Its nonzero terminal velocity makes the endpoint energy a submersion off the center. The proof needs no global smooth distance function, unique geodesics on the whole product, or foliation through a cut locus.
3. **Curvature and locality.** Recomputing the difference tensor gives exactly the sign pattern in equation (3). At each point, the sphere plane forces the same vector `A(e1)` to be `e1` that the mixed plane forces to be zero. The contradiction allows arbitrary `A`, so it rules out all local conformal factors without assuming their derivatives can be selected independently.
4. **Dimension claim.** The proof extends to every `n >= 3` because the same three vectors exist and added Euclidean directions do not affect their curvature. The script checks dimensions 3, 4 and 5; the manuscript correctly assigns the general dimension claim to the analytic proof. The optional Ricci/Weyl comparison is the three-dimensional calculation for the main example. No dimension-two conclusion is asserted.
5. **Reparametrization sign.** Writing `gamma(u(s))` in the changed geodesic equation gives `u'' + 2 (dt/du) (u')^2 = 0`, equivalently `ds/du = C exp(2t(gamma(u)))`. Thus the manuscript has the correct sign. On each compact segment this derivative is finite and strictly positive and can be normalized to the prescribed endpoint interval.
6. **Convex neighborhoods in the extension.** This positive reparametrization operates in both directions without changing any path image. Existence and uniqueness of connecting paths inside the same neighborhood are consequently preserved. The metrics differ by a positive scalar, and endpoint velocities differ by a nonzero scalar, so their radial hyperplanes coincide there. The word “corresponding” does not require an unstated map of points or a change of the neighborhood's underlying set.
7. **Non-self-dual tensors.** Equation (5), its value `-3 exp(t)` on the line direction, the stated dual connection, and the composition with factor `t+psi` all agree with direct differentiation and duality. The proof neither assumes completeness of the deformation nor needs it.

## Verifier alignment and execution

I executed the standard-library checker successfully. It reported coefficient/augmented ranks `(9,10)`, `(16,17)`, and `(25,26)` in dimensions 3, 4, and 5; accepted the three constant-curvature controls and the dimension-two sphere boundary control; and confirmed the three-dimensional Ricci and projective Weyl components.

I also inspected the implementation. Every tensor component of equation (3) is included, with `A[ell,i]` represented by column `ell*n+i`; the coefficient signs and product-curvature input are correct. Gaussian elimination uses exact fractions and explicit failure exceptions, rather than floating-point tolerances or removable Python assertions. The tested rank inequality genuinely excludes every endomorphism. The constant-curvature control residuals also exercise the indexing independently of the elimination result.

This checker takes the product-curvature formula as input. The manuscript correctly describes it as a pointwise check, not a verification of the all-centers first-variation argument. The separately implemented symbolic verifier starts from the coordinate metric and its Christoffel/curvature routines agree with the manuscript's conventions. This final pass did not rerun the symbolic suite; its execution is covered by the separate computational review.

## Attribution and exact residual scope

I independently opened [Ueno's versioned preprint](https://arxiv.org/html/2503.10024v2). Proposition 3.5, equation (3.6), and section 3.2 support the known conformal/projective mechanism attributed in the manuscript. Substituting `g=h1` and `sigma=-t` gives the construction used here. The manuscript appropriately disclaims novelty of that construction and of the classical ingredients.

The literature-audit language is bounded and consistent with its recorded limitations. It reports no located earlier explicit resolution, does not certify priority, and discloses the inaccessible live database annotations. This audit likewise does not establish historical priority or current community consensus about the problem's status.

**Strongest verified result:** the reviewed paper contains a complete, short mathematical counterexample to the literal printed implication, and its standard-library verifier correctly checks the pointwise obstruction it claims to check. **Exact remaining proof gap:** none found. **Publication limitation:** an unrefereed result with a bounded priority search, not external human peer review or a priority guarantee.
