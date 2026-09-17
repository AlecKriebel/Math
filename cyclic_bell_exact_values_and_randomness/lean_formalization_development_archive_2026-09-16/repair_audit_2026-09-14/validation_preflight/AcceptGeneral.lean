import CyclicBell.GeneralStatements
import CyclicBell.AdversarialStatements
import CyclicBell.Regression
import CyclicBell.GeneralCoverageSourceWeyl
open scoped BigOperators
open CyclicBell.General
/- Positive controls, executed only by the offline build. -/
example : (∑ a : ZMod 5, ∑ b : ZMod 5, swappedTarget 5 a b)=1 :=
  swappedTarget_normalized
example : ¬ ∀ a b : ZMod 5, swappedTarget 5 a b=1/(5 : ℝ)^2 :=
  swappedTarget_not_uniform (by norm_num)
example : (∑ l : ZMod 5, star (generalLambda l)*generalLambda l)=1 :=
  generalLambda_normalization (by norm_num)
example (nA nB : ℕ)
    (s : StrategyOn 5 (Fin 2) (Option (ZMod 5)) (Fin nA) (Fin nB)) :
    firstValue s≤scalarMaximum 5+1 := first_physical_upper (by norm_num) s
example (nA nB : ℕ)
    (s : StrategyOn 5 (ZMod 5) (Option (ZMod 5)) (Fin nA) (Fin nB)) :
    secondValue s≤6 := by
  convert second_physical_upper (by norm_num) s using 1 <;> norm_num
