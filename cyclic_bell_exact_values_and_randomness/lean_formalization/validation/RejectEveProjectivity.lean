import CyclicBell.GeneralAdversarialRegression
noncomputable section
open CyclicBell CyclicBell.General
-- MUST FAIL: arbitrary guessing POVMs must not be restricted to PVMs.
example : uniformOneDimensionalGuess.effect (0,0)*uniformOneDimensionalGuess.effect (0,0)=
    uniformOneDimensionalGuess.effect (0,0) := by
  norm_num [uniformOneDimensionalGuess,Matrix.mul_apply,Matrix.smul_apply,Matrix.one_apply]
