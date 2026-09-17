import CyclicBell.D4
-- INTENTIONALLY FALSE. The audit runner must reject this physical claim.
example : CyclicBell.D4.targetBorn 0 1 = (1 : ℝ) / 16 := by
  rw [CyclicBell.D4.target_01]
  norm_num
