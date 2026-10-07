# Crystalline Wulff minimizers: planar partial results

Problem 30005209 · 7 October 2026

## Disposition

**The geometric classification remains unresolved after five substantive approaches.** This is not a solution claim. The notes establish a planar analytic criterion, give complete triangle and parallelogram subclasses, and construct an implicit family of nonsymmetric quadrilaterals. They do not classify all polygons or higher-dimensional polytopes. No claim of priority is made for the partial results.

Fix \(0<\alpha<2\). The energy is
\[
\mathcal E_\gamma(E)=P_\psi(E)+\gamma V_\alpha(E),\qquad
V_\alpha(E)=\int_E\int_E |x-y|^{-\alpha}\,dx\,dy,\qquad |E|=1.
\]
Here \(P=W_\psi\) is a unit-area convex polygon and \(\psi\) is convex, positively one-homogeneous, and strictly positive on the unit circle. **Evenness is not assumed in the source.** The exponent is fixed before choosing the small-γ threshold.

## Results and their limits

1. **Triangles.** Every nondegenerate triangular Wulff shape is the unique minimizer up to translation for sufficiently small γ. The key sliding-stationarity observation is already in Bonacini–Cristoferi–Topaloglu (2022), Remark 4.1. The conclusion follows from their earlier small-γ reduction and is not claimed as new.
2. **Planar criterion.** Equal side-average Riesz potentials are necessary and sufficient for small-γ global minimality. The proof includes the missing sufficiency steps: a \(C^2\) transport estimate, quantitative Wulff coercivity, existence, and crystalline rigidity. This remains an implicit system, not an explicit classification.
3. **Parallelograms.** Exactly the rhombi satisfy that criterion. A non-rhombic parallelogram fails even first-order minimality for every γ>0.
4. **Near-square continuation.** For every four-normal configuration sufficiently close to the square's, there is a locally unique sliding-critical unit-area quadrilateral near the square, modulo translations. It follows that small-γ minimizers include quadrilaterals outside the side-transitive class of the 2021 theorem. This is a local implicit construction, not a classification of all quadrilaterals.
5. **Boundary/vertex truncations.** An exact expansion identifies the sign governing birth of a new side. Both signs occur among triangular limits. Thus a naive “maximize within each normal fan and rule out its boundary” strategy does not close the global classification.

## Files

- `01_triangle_rigidity.md`: geometric and translation-identity proofs.
- `02_stationarity_and_global_minimality.md`: full planar equivalence proof.
- `03_parallelogram_classification.md`: exact integral comparison.
- `04_near_square_continuation.md`: Hessian and implicit-function construction.
- `05_vertex_truncation_obstruction.md`: boundary expansion and exact thin-triangle limit.
- `SOURCES_AND_SCOPE.md`: primary literature, scope corrections, and bounded current-literature check.
- `SELF_AUDIT.md`: dependencies, checks, and unresolved issues.
- `verify_formulas.py` and `verification_results.json`: reproducible numerical sanity checks of analytic formulas; no numerical output is used as proof.

The mathematical notes are original exposition. They contain no copied source documents or source datasets.
