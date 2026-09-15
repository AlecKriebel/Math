import CyclicBell.GeneralStatements
import CyclicBell.AdversarialStatements
import CyclicBell.Regression
import CyclicBell.GeneralCoverageSourceWeyl
open CyclicBell
open scoped BigOperators
example : D4.targetBorn 0 1 = (3 : ℝ) / 32 := D4.target_01
example : ip D4.phi D4.phi = 1 := D4.phi_normalized
example (nA nB : ℕ) (σ : Strategy 2 nA nB) : firstAugmentedValue σ ≤ firstTargetValue :=
  first_universal_upper σ
example : firstAugmentedValue D4.firstStrategy = firstTargetValue := D4.first_attainment
example : IsFirstMaximizer D4.firstStrategy := D4.first_is_maximizer
example : secondAugmentedValue D4.secondStrategy = 5 := D4.second_attainment
example : IsSecondMaximizer D4.secondStrategy := D4.second_is_maximizer
example : firstAugmentedValue D4.firstStrategy ≠ firstTargetValue / 4 := D4.extra_factor_four_is_wrong
example : D4.canonicalTargetBorn 0 1 ≠ D4.targetBorn 0 1 := D4.altered_witness_changes_target
