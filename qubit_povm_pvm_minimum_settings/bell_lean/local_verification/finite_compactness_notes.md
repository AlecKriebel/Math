# Finite convex compactness compiler audit

Checkpoint: 2026-09-11T01:51:53.812450+00:00; module verification completion estimate: 100%.

The exact original statements in `Bell/FiniteConvexCompactness.lean` compile under pinned Lean 4.19.0. Compatibility repairs are limited to closed-intersection API, finite-set equivalence cardinality, and explicit subtype-sum coercions. No hypotheses, definitions, or theorem conclusions were weakened.

All eight theorem dependencies are restricted to Lean's standard axioms `propext`, `Classical.choice`, and `Quot.sound`. No `sorryAx` occurs. The separately compiled audit checks that the probability simplex on `Fin 0` and zero-slot combinations are empty, and that the empty convex hull is compact.

The finite union ranges over zero through ambient dimension plus one, so it includes every Carathéodory cardinality bound. The nonempty minimal support needed by the affine dimension identity is deduced from the weight sum equal to one. Ordinary convex hull compactness does not assume compactness of the hull; it follows from finite continuous compact images. Only the final containment theorem invokes the closure from the standard Krein–Milman theorem.

This establishes the module's stated compactness and extremality results. It does not independently establish that later Bell theorems apply these results with adequate hypotheses.
