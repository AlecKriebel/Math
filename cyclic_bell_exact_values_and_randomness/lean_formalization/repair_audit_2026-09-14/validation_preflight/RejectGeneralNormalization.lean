import CyclicBell.GeneralSwap
open scoped BigOperators
open CyclicBell.General
-- INTENTIONALLY FALSE: an actual normalized Born table cannot sum to two.
example : (∑ a : ZMod 5, ∑ b : ZMod 5, swappedTarget 5 a b)=2 := by
  rw [swappedTarget_normalized]
  norm_num
