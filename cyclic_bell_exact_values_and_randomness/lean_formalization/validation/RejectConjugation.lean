import CyclicBell
open CyclicBell
/- EXPECTED FAILURE: dropping the polar factor's complex conjugation is wrong. -/
example : D4.witnessB 0 = D4.weighted (fun j => D4.zeta ^ D4.polarExponents 0 j) := by
  exact D4.bob_manuscript_bridge 0
