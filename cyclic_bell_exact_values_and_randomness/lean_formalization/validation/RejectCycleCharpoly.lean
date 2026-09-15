import CyclicBell
noncomputable section
open CyclicBell CyclicBell.General
open scoped BigOperators Polynomial
/- Deliberately false: the nonunit one-cell cycle has X-2, not X+2.
This must fail for a proof error, not an import/name/typeclass failure. -/
example : (weightedCycle (fun _ : ZMod 1 => (2 : ℂ))).charpoly =
    Polynomial.X + Polynomial.C (2 : ℂ) := by
  rw [weighted_cycle_charpoly (fun _ : ZMod 1 => (2 : ℂ)) (by intro j; norm_num)]
  norm_num
