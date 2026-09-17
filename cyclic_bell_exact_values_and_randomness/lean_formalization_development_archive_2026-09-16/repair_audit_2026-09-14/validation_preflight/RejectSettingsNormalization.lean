import CyclicBell.GeneralPhaseTables
open CyclicBell CyclicBell.General
open scoped BigOperators
-- INTENTIONALLY FALSE: doubling the actual Born table doubles its total mass.
example : (∑ a : ZMod 5,∑ b : ZMod 5,
    2*phasePairProbability (0 : ℝ) (-1/4) a b)=1 := by
  simp only [← Finset.mul_sum,phasePair_normalized]
  norm_num
