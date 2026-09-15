import CyclicBell.GeneralPhaseBounds
open CyclicBell CyclicBell.General
-- INTENTIONALLY FALSE: the standard table is not uniform.
example : ∀ a b : ZMod 4,behavior (standardPhaseStrategy 4) 0 0 a b=1/(4 : ℝ)^2 := by
  intro a b
  have h := (standard_tables_nonuniform (d := 4) (by norm_num) 0 0).2.2.2
  exact h
