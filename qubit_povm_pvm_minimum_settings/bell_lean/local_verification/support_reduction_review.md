# Measurement support and encoding repair checkpoint

2026-09-10. Assigned modules `Bell.MeasurementSpans` and `Bell.SmallOutputEncoding` now build successfully with pinned Lean 4.19.0. Completion estimate for this pair: 100%.

The span-intersection statement now explicitly coerces the intersection submodule to its underlying type (`↥(...)`) before taking `Module.finrank`. This repairs the original ill-typed expression and preserves the intended mathematical statement. All other statements and mathematical hypotheses are unchanged.

The coefficient-map proof partitions each finite sum into the active support and its complement using `Fintype.sum_subtype_add_sum_subtype`. Inactive effects and their coordinate images vanish exactly; no approximate zero test is used. The map from the common span intersection to the real time coordinate is injective because common-span filtering makes every element equal to that coordinate times `timeUnit`. Dimension and support-cardinality estimates therefore use the exact four-dimensional coordinate space.

Dependent two-input coefficient and output-map families are built using the dependent eliminator `Fin.cases`. This avoids the invalid original attempt to eliminate a proposition-valued finite-membership proof into data via `fin_cases`. All original input and output labels are retained.

The active measurement is normalized by the exact enumeration equivalence and the vanishing complement. Encoding casts every active index into `Fin 3`; unused labels have exactly zero effect. `encoding_coarsens` proves recovering the original complete effect family, including zero outcomes. Its fallback label exists because a normalized POVM has nonempty active support. The deterministic-input locality proof explicitly identifies the coarsened Born expressions and applies the proved one-input theorem.

Evidence: `measurement_spans.log`, `small_output_encoding.log`, and `support_reduction_axioms.log`. The last audits the intersection/dimension/support bounds, activePOVM, encoding recovery/effect cases, and deterministic Alice/Bob locality. Every dependency closure contains only `propext`, `Classical.choice`, and `Quot.sound`; there are no custom axioms or admitted proofs.
