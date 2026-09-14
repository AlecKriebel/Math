import SymmetricSector.DebtBudget
import SymmetricSector.Contraction
import SymmetricSector.PhaseMargins
import SymmetricSector.SmallFinite

/-! All-order positivity of the actual symmetric rank-system scalar. The proof
uses the specified inverse, concrete Schur blocks, explicit barrier inequalities,
and full finite kernel certificates. No sign or bridge is a hypothesis. -/
namespace SymmetricSector
open Matrix
open scoped BigOperators

/-- A.36 for the actual reduced scalar at every order in the phase range. -/
theorem reducedScalar_pos_of_forty (N : ℕ) (hN : 40 ≤ N) :
    0 < reducedScalar N := by
  have h3 : 3 ≤ N := by omega
  have hNq : (3 : ℚ) ≤ N := by exact_mod_cast h3
  have hc0 : 0 ≤ c N := by
    simpa [c, phaseContraction] using phaseContraction_nonneg (N : ℚ) hNq
  have hc1 : c N < 1 := by
    simpa [c, phaseContraction] using phaseContraction_lt_one (N : ℚ) hNq
  have hloss : beta N + (1 / (11 / 25 : ℚ)) * (c N / (1 - c N)) < 1 := by
    convert all_phase_margin N hN using 1 <;> unfold epsilon <;> ring
  rw [reducedScalar_eq_schur_pairing N h3]
  exact Phase.phase_scalar_pos (phaseA N) (phaseA_nonneg N h3)
    (phaseV N) (phaseV_pos N h3) (c N) hc0 hc1 (phaseA_phaseV_le N h3)
    (11/25) (by norm_num) (phaseF0 N) (dualGood N) (phaseEll N)
    (phaseEll_nonneg N hN) (phaseF0_bounds N (by omega)).1
    (phaseF0_bounds N (by omega)).2 (dualGood_schur N h3)
    (phaseDebt N) (beta N) (phaseDebt_le_beta_first N hN)
    (phase_first_pos N hN) hloss

/-- The full symmetric-sector reduced-scalar positivity theorem, including
all exceptional finite orders and all analytic orders. N=n−1. -/
theorem reducedScalar_pos (N : ℕ) (hN : 3 ≤ N) : 0 < reducedScalar N := by
  by_cases h39 : N ≤ 39
  · exact finite_small_scalar_pos N hN h39
  · exact reducedScalar_pos_of_forty N (by omega)

#print axioms reducedScalar_pos_of_forty
#print axioms reducedScalar_pos
end SymmetricSector
