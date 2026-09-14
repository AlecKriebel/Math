import SymmetricSector.Budget
import SymmetricSector.LeftDebt
import SymmetricSector.BadBarriers

namespace SymmetricSector
open Matrix
open scoped BigOperators

/-- The bad-rank debt sum is the good-rank sum with a zero final coordinate. -/
theorem debtWeight_sum (N : ℕ) :
    (∑ i : Bad N, (4*(i.val+3)/(3*(i.val+2)*((N:ℚ)-2))) *
      goodReward N (goodBelow N i)) =
    ∑ i : Good N, debtWeight N i * goodReward N i := by
  unfold debtWeight
  simp only [ite_mul, zero_mul]
  rw [← Finset.sum_filter]
  apply Finset.sum_bij (fun i _ => goodBelow N i)
  · intro i _
    simp [goodBelow, i.isLt]
  · intro i _ j _ h
    exact Fin.ext (congrArg (fun k : Good N => k.val) h)
  · intro j hj
    have hlt : j.val < N - 2 := (Finset.mem_filter.mp hj).2
    refine ⟨⟨j.val, hlt⟩, Finset.mem_univ _, ?_⟩
    apply Fin.ext
    rfl
  · intro i _
    rfl

/-- The complete debt bound uses the actual inverse and the actual beta maximum. -/
theorem phaseDebt_le_beta_first (N : ℕ) (hN : 40 ≤ N) :
    phaseDebt N ≤ beta N * dotProduct (phaseEll N) (phaseF0 N) := by
  apply debt_le_beta_pairing N hN
  · exact phaseEll_lower N (by omega)
  · exact (phaseF0_bounds N (by omega)).1
  · rw [← debtWeight_sum]
    exact phaseDebt_le_printed N (by omega)

theorem phase_first_pos (N : ℕ) (hN : 40 ≤ N) :
    0 < dotProduct (phaseEll N) (phaseF0 N) := by
  apply first_phase_pairing_pos N hN
  · exact phaseEll_lower N (by omega)
  · exact (phaseF0_bounds N (by omega)).1

theorem phaseEll_nonneg (N : ℕ) (hN : 40 ≤ N) : 0 ≤ phaseEll N := by
  intro i
  exact (lowerEll_pos hN (by omega)).le.trans (phaseEll_lower N (by omega) i)

#print axioms phaseDebt_le_beta_first
#print axioms phase_first_pos
end SymmetricSector
