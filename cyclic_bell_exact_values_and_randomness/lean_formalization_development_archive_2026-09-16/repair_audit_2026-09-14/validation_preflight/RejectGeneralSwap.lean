import CyclicBell.GeneralSwap
open CyclicBell.General
-- INTENTIONALLY FALSE: conflating the canonical phase order with the swap.
example : ∀ a b : ZMod 5, swappedTarget 5 a b=1/(5 : ℝ)^2 := by
  have hn : ¬ ∀ a b : ZMod 5, swappedTarget 5 a b=1/(5 : ℝ)^2 := by
    simpa using swappedTarget_not_uniform (d := 5) (by norm_num)
  simp only [hn]
