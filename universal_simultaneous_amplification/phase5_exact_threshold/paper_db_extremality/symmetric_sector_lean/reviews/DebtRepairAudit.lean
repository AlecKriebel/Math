import SymmetricSector.LeftDebt

/-! Independent adversarial check: the original direct Y reward pairing
exceeds the first printed A.31 right-hand side already at N=4. The replacement
LeftDebt proof must therefore not use that false comparison. -/
namespace SymmetricSector.DebtRepairAudit
open scoped BigOperators

/-- Exact counterexample to the unlicensed direct A.28-to-A.31 pairing step.
This concerns the proposed Y bound, not the actual debt. -/
theorem original_Y_pairing_gap_four :
    dotProduct (printedLeftBarrier 4) (-badReward 4) -
      (∑ i : Bad 4,
        (4 * (i.val + 3) / (3 * (i.val + 2) * ((4 : ℚ) - 2))) *
          goodReward 4 (goodBelow 4 i)) = 1 / 360 := by
  norm_num [dotProduct, Bad, Good, printedLeftBarrier, badReward,
    goodReward, reward, goodBelow, Fin.sum_univ_succ]

#check leftBarrier_supersolution
#check leftOccupation_le_barrier
#check phaseEll_lower
#check leftBarrier_reward
#check goodReward_above_reflect
#check phaseDebt_le_constant_sum
#check phaseDebt_le_printed
#check phaseWbar_supersolution
#check phaseC_Wbar_le
#check phaseW_le_Wbar
#check phaseF0_bounds
#print axioms original_Y_pairing_gap_four
#print axioms leftBarrier_supersolution
#print axioms leftOccupation_le_barrier
#print axioms phaseEll_lower
#print axioms phaseDebt_le_constant_sum
#print axioms phaseDebt_le_printed
#print axioms phaseWbar_supersolution
#print axioms phaseC_Wbar_le
#print axioms phaseW_le_Wbar
#print axioms phaseF0_bounds

end SymmetricSector.DebtRepairAudit
