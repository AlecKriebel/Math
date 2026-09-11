import Bell.FiniteConvexCompactness
#print axioms Bell.probabilitySimplex_isCompact
#print axioms Bell.combinations_isCompact
#print axioms Bell.combinations_subset_convexHull
#print axioms Bell.convexHull_eq_finite_combinations
#print axioms Bell.compact_convexHull
#print axioms Bell.extreme_midpoint
#print axioms Bell.extreme_positive_combination
#print axioms Bell.contains_compact_of_contains_extreme
example : Bell.probabilitySimplex (Fin 0) = ∅ := by
  ext w
  simp [Bell.probabilitySimplex]
example : Bell.combinations 0 (Set.univ : Set ℝ) = ∅ := by
  simp [Bell.combinations, Bell.probabilitySimplex]
example : IsCompact (convexHull ℝ (∅ : Set ℝ)) :=
  Bell.compact_convexHull isCompact_empty
