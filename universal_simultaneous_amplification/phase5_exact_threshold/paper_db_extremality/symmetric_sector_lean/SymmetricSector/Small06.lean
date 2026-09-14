import SymmetricSector.Small05
import SymmetricSector.Definitions
import SymmetricSector.Phase
import SymmetricSector.RowBounds

open SymmetricSector.Phase

set_option maxRecDepth 2048
set_option maxHeartbeats 0

namespace SymmetricSector.Cert6

theorem d_1 : gradient 6 1 = (129 / 80 : ℚ) := by
  rw [gradient]
  norm_num only [show 1 < 6 by decide, if_true]
  rw [gradient]
  norm_num [c₀]

theorem d_2 : gradient 6 2 = (147 / 160 : ℚ) := by
  rw [gradient]
  norm_num only [show 2 < 6 by decide, if_true]
  rw [d_1]
  norm_num [c₀]

theorem d_3 : gradient 6 3 = (19 / 30 : ℚ) := by
  rw [gradient]
  norm_num only [show 3 < 6 by decide, if_true]
  rw [d_2]
  norm_num [c₀]

theorem d_4 : gradient 6 4 = (77 / 160 : ℚ) := by
  rw [gradient]
  norm_num only [show 4 < 6 by decide, if_true]
  rw [d_3]
  norm_num [c₀]

theorem d_5 : gradient 6 5 = (31 / 80 : ℚ) := by
  rw [gradient]
  norm_num only [show 5 < 6 by decide, if_true]
  rw [d_4]
  norm_num [c₀]

theorem terminal_gradient : (5 : ℚ) * gradient 6 5 + 2*6*(1/6 - c₀ 6) = 0 := by
  rw [d_5]
  norm_num [c₀]

def response : Channel 6 → ℚ
  | .inl i => ![(66584547 / 67910720 : ℚ), (62064467 / 101866080 : ℚ), (90455209 / 203732160 : ℚ), (11909067 / 33955360 : ℚ), (93 / 280 : ℚ)] i
  | .inr i => ![(270334333 / 407464320 : ℚ), (153149819 / 407464320 : ℚ), (34331377 / 135821440 : ℚ), (49180587 / 237687520 : ℚ)] i

theorem equations : (1 - coefficientK 6).mulVec response = source 6 := by
  apply funext
  decide +kernel

theorem value : reducedScalar 6 = (7823511 / 760600064 : ℚ) := by
  unfold reducedScalar
  rw [← witness_eq_inverse_mulVec (1 - coefficientK 6)
    (coefficient_system_isUnit 6 (by norm_num))
    (source 6) response equations]
  decide +kernel

theorem positive : 0 < reducedScalar 6 := by rw [value]; norm_num

end SymmetricSector.Cert6
