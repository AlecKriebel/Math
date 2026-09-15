import CyclicBell.GeneralAnchoredTables
open CyclicBell CyclicBell.General
-- INTENTIONALLY FALSE: the strict anchor gap excludes d=2.
example : (1/4 : ℝ)<behavior (anchoredStandardStrategy 2 0) 1 none (0 : ZMod 2) 0 := by
  rw [anchored_qubit_cross_uniform 0 1 (by decide) 0 0]
  norm_num
