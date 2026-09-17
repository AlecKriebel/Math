import CyclicBell.GeneralStatements
import CyclicBell.AdversarialStatements
import CyclicBell.Regression
import CyclicBell.GeneralCoverageSourceWeyl
open CyclicBell
/- EXPECTED FAILURE: dropping the polar factor's complex conjugation is wrong. -/
example : D4.witnessB 0 = D4.weighted (fun j => D4.zeta ^ D4.polarExponents 0 j) := by
  simp only [D4.bob_conjugation_is_essential]
