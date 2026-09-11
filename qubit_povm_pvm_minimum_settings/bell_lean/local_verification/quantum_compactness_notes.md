# Quantum strategy compactness audit

Checkpoint: 2026-09-11T01:56:38.925338+00:00; module verification completion estimate: 100%.

The actual production build of `Bell.QuantumCompactness` succeeds under pinned Lean 4.19.0. All original statements and definitions are retained. Repairs expose `Matrix.diag_apply` in the Frobenius trace identity, remove a tactic after a completed goal, supply the real summand explicitly to `Finset.single_le_sum`, and replace an absent closed-forall API with a private theorem proved from closed intersections. Explicit quantifier nesting in projectivity closedness avoids over-applying a generic forall tactic.

Axiom checks for thirteen major results, including raw image equalities, compactness of raw and convex strategies, and `counterexample_has_extreme_maximum`, report only `propext`, `Classical.choice`, and `Quot.sound`.

The Gram parameterization represents every PSD density/effect by a square factor; it does not impose rank-one or purity assumptions. Trace normalization bounds factor entries, with the state trace one and qubit measurement sum trace two. Empty-output architectures produce empty normalized parameter spaces and remain covered without an invented nonemptiness premise. The finite-dimensional hull compactness theorem is used only after proving compactness of raw images.

The extreme-maximum theorem applies separation to the closed convex PVM hull, maximizes the continuous separator on the compact POVM hull, and extracts an extreme point of the exposed maximizing face. Extreme points of the ordinary convex hull belong to the original raw set, yielding the stated unrandomized strategy. It does not assert that an arbitrary optimizer is extreme.
