import CyclicBell.Regression
open CyclicBell
/- EXPECTED FAILURE: the actual displayed functional has no extra factor d=4. -/
example : firstAugmentedValue D4.firstStrategy = firstTargetValue / 4 := by
  simp only [D4.extra_factor_four_is_wrong]
