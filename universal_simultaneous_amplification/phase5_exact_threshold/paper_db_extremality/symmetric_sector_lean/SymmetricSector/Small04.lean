import SymmetricSector.Small03
import SymmetricSector.Definitions
import SymmetricSector.Phase
import SymmetricSector.RowBounds

open SymmetricSector.Phase

set_option maxRecDepth 2048
set_option maxHeartbeats 0

namespace SymmetricSector.Cert4

theorem d_1 : gradient 4 1 = (17 / 12 : ℚ) := by
  rw [gradient]
  norm_num only [show 1 < 4 by decide, if_true]
  rw [gradient]
  norm_num [c₀]

theorem d_2 : gradient 4 2 = (5 / 6 : ℚ) := by
  rw [gradient]
  norm_num only [show 2 < 4 by decide, if_true]
  rw [d_1]
  norm_num [c₀]

theorem d_3 : gradient 4 3 = (7 / 12 : ℚ) := by
  rw [gradient]
  norm_num only [show 3 < 4 by decide, if_true]
  rw [d_2]
  norm_num [c₀]

theorem terminal_gradient : (3 : ℚ) * gradient 4 3 + 2*4*(1/4 - c₀ 4) = 0 := by
  rw [d_3]
  norm_num [c₀]

def response : Channel 4 → ℚ
  | .inl i => ![(1072 / 1333 : ℚ), (4139 / 7998 : ℚ), (7 / 15 : ℚ)] i
  | .inr i => ![(2144 / 3999 : ℚ), (2316 / 6665 : ℚ)] i

theorem equations : (1 - coefficientK 4).mulVec response = source 4 := by
  apply funext
  decide +kernel

theorem value : reducedScalar 4 = (359 / 26660 : ℚ) := by
  unfold reducedScalar
  rw [← witness_eq_inverse_mulVec (1 - coefficientK 4)
    (coefficient_system_isUnit 4 (by norm_num))
    (source 4) response equations]
  decide +kernel

theorem positive : 0 < reducedScalar 4 := by rw [value]; norm_num

end SymmetricSector.Cert4
