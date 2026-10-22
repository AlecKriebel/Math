# Acceptance of the global approximate-root partial theorem

Decision: ACCEPTED_PARTIAL_BOUND. No mathematical correction is required.

For every ε > 0, the minimum number N(ε) of open sets covering all six original real coefficients, with a continuous selector on each set strictly within ε in Euclidean distance of an actual real common root, satisfies 2 ≤ N(ε) ≤ 3. The number is independent of the positive tolerance. The exact optimum remains either 2 or 3.

## Accepted proof obligations

1. The original real equations are equivalent to u² + β conjugate(u) = w, with an independent translation parameter α. The global parameter homeomorphism and distance-preserving root translation preserve the minimum cover number in both directions.
2. Root bounds, properness, degree 2 and finite fibers hold without excluding singular parameters. Closed critical-disk injectivity, invariance of domain and Jordan separation establish the central Jordan disk and its continuous negative-degree root.
3. The local critical germ gives fold degree 0 and cusp degree +1. At a cusp the mixed derivative in (s,y) = (F,y) is A ≠ 0 and the reduced cubic coefficient is positive. Degree additivity establishes all four fiber counts.
4. Selecting the two positive exterior roots, and the degree-one cusp root when needed, produces a genuine two-sheeted covering of the relative exterior. Fold roots of degree zero are omitted. The continuity proof covers whole neighborhoods and varying β.
5. The caustic's strictly decreasing argument yields one intersection with each ray, a continuous radial function, and the explicit homeomorphism E_j ≅ I_j × ((C × [0,∞)) \ {(0,0)}). Each chart is relatively closed in its ambient open phase chart and contractible and locally path connected.
6. Covering-space triviality gives exact sections on the two exterior charts. Unbounded real-valued Tietze extension and persistence of nonzero local degree give open approximate collars with one globally fixed tolerance, even on unbounded parameter space and at cusps.
7. A cutoff blends the interior section to zero on an open origin neighborhood. Agreement on the overlap gives continuity. Together with the two collars this is an open three-chart cover of the complete space.
8. A circle with root radius L > ε rules out one approximate chart by disconnectedness of two error disks and square-root monodromy. A global dilation transfers any positive tolerance to any other, proving tolerance independence.

The full arguments, standard dependencies and all boundary/quantifier checks are in PROOF.md and AUDIT.md. The nearby actual root used by a collar need not itself vary continuously on a full neighborhood; persistence supplies the existence required by approximate selection.

## Remaining question and exclusions

The only accepted numeric conclusion is 2 ≤ N(ε) ≤ 3. No two-chart construction or obstruction to all two-chart covers is supplied. The cover and selectors may depend on ε; no common cover/selectors for every tolerance are asserted. This is root-distance approximation, not residual-error control, and no compactness or discriminant-complement restriction is introduced.

The literal all-parameter exact-section caution is separate. It makes no intended-problem interpretation, source-correction or full approximate-resolution claim. The original candidate's pending-audit statement is retained as historical text and contextualized by the subsequent partial acceptance. No source-author implementation or inherited exact-selection lower bound is used in the proof.

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance applies only to the stated partial theorem; it is not external human peer review or formal proof-assistant certification. This is a written proof/audit edition, not a computational reproduction package. Source inspection and symbolic checks described below occurred in the preceding investigation and audit on 11 October 2026. Editorial preparation authenticated retained bytes without a new scholarly-source inspection or mathematical-program rerun.
