import CyclicBell.GeneralStatements
import CyclicBell.AdversarialStatements
import CyclicBell.Regression
import CyclicBell.GeneralCoverageSourceWeyl
open CyclicBell
/- EXPECTED FAILURE: the actual displayed functional has no extra factor d=4. -/
example : firstAugmentedValue D4.firstStrategy = firstTargetValue / 4 := by
  exact D4.first_attainment
