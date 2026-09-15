import CyclicBell.GeneralSecondCoefficients
open scoped BigOperators
open CyclicBell.General
-- INTENTIONALLY FALSE: the manuscript coefficients have squared norm one.
example : (∑ l : ZMod 5, star (generalLambda l)*generalLambda l)=2 := by
  rw [generalLambda_normalization (by norm_num : 2≤5)]
  norm_num
