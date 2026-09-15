import CyclicBell.GeneralStatements
import CyclicBell.AdversarialStatements
import CyclicBell.Regression
import CyclicBell.GeneralCoverageSourceWeyl
noncomputable section
open CyclicBell CyclicBell.General
open scoped BigOperators Matrix
-- MUST FAIL: sixteen effects each equal I/8 sum to 2I, not I.
example : (∑ g : GuessLabel 4,(1/8 : ℂ) • (1 : Mat (Fin 1)))=1 := by
  ext i j
  fin_cases i
  fin_cases j
  norm_num [Matrix.sum_apply,Matrix.smul_apply,Matrix.one_apply,
    Finset.sum_const,Fintype.card_prod,ZMod.card,GuessLabel]
