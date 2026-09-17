import CyclicBell.D4

/-! Source correspondence for the target-coordinate constants.
The scalar facts used by universal bounds live in ScalarData, which does NOT
import D4, Cycle4, Witness, Attainment, or any target-distribution construction.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.D4

theorem old_weights_phase_bridge (j : Fin 4) :
    swappedWeights j = zeta ^ ((![2,6,14,10] : Fin 4 → ℕ) j) := by
  fin_cases j <;>
    norm_num [swappedWeights, zeta_phaseTable (2 : Fin 16),
      zeta_phaseTable (6 : Fin 16), zeta_phaseTable (14 : Fin 16),
      zeta_phaseTable (10 : Fin 16), phaseTable]

theorem old_q_phase_bridge : q = ![1, zeta ^ 2, -1, zeta ^ 6] := by
  funext j
  fin_cases j <;> simp [q, zeta_sq, zeta_phaseTable (6 : Fin 16), phaseTable]


end CyclicBell.D4
