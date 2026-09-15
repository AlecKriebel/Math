import CyclicBell.GeneralSourceFourier
noncomputable section
open CyclicBell CyclicBell.General
-- MUST FAIL: the k=1 source coefficient is negative, with its phase retained.
example : sourceCoeff (0 : Ix 3) 1=(1/3 : ℂ)*chi (1 : Ix 3) := by
  rw [(source_qutrit_coefficients 0).2.1]
  norm_num
