import CyclicBell
noncomputable section
open CyclicBell CyclicBell.General
-- MUST FAIL: the formal lower bound is 3/32, strictly exceeding 1/16.
example : GvalQ (firstAugmentedBell (d := 4)) 1 none≤(1 : ℝ)/16 := by
  have h := first_four_Gval_three32.1
  linarith
