import SymmetricSector.Definitions
import SymmetricSector.Phase
import SymmetricSector.RowBounds

open SymmetricSector.Phase

set_option maxRecDepth 2048
set_option maxHeartbeats 0

namespace SymmetricSector.Cert3

theorem d_1 : gradient 3 1 = (5 / 4 : ℚ) := by
  rw [gradient]
  norm_num only [show 1 < 3 by decide, if_true]
  rw [gradient]
  norm_num [c₀]

theorem d_2 : gradient 3 2 = (3 / 4 : ℚ) := by
  rw [gradient]
  norm_num only [show 2 < 3 by decide, if_true]
  rw [d_1]
  norm_num [c₀]

theorem terminal_gradient : (2 : ℚ) * gradient 3 2 + 2*3*(1/3 - c₀ 3) = 0 := by
  rw [d_2]
  norm_num [c₀]

def response : Channel 3 → ℚ
  | .inl i => ![(69 / 104 : ℚ), (9 / 16 : ℚ)] i
  | .inr i => ![(207 / 416 : ℚ)] i

theorem equations : (1 - coefficientK 3).mulVec response = source 3 := by
  apply funext
  decide +kernel

theorem value : reducedScalar 3 = (3 / 208 : ℚ) := by
  unfold reducedScalar
  rw [← witness_eq_inverse_mulVec (1 - coefficientK 3)
    (coefficient_system_isUnit 3 (by norm_num))
    (source 3) response equations]
  decide +kernel

theorem positive : 0 < reducedScalar 3 := by rw [value]; norm_num

end SymmetricSector.Cert3
