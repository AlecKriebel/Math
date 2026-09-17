import CyclicBell.GeneralStatements
import CyclicBell.AdversarialStatements
import CyclicBell.Regression
import CyclicBell.GeneralCoverageSourceWeyl
open CyclicBell
/- EXPECTED FAILURE: the canonical target PVM does not have the swapped table. -/
example : D4.canonicalTargetBorn 0 1 = (3 : ℝ) / 32 := by
  rw [D4.canonical_target_uniform]
  norm_num
