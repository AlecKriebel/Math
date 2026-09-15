import CyclicBell.GeneralSwap
open CyclicBell.General
-- INTENTIONALLY FALSE: conflating the canonical phase order with the swap.
example : ∀ a b : ZMod 5, swappedTarget 5 a b=1/(5 : ℝ)^2 := by
  apply Classical.byContradiction
  intro h
  have hn := swappedTarget_not_uniform (d := 5) (by norm_num)
  -- Two proofs of the same negation are not a contradiction. This must fail.
  contradiction
