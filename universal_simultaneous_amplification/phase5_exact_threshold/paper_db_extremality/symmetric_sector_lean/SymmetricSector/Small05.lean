import SymmetricSector.Small04
import SymmetricSector.Definitions
import SymmetricSector.Phase
import SymmetricSector.RowBounds

open SymmetricSector.Phase

set_option maxRecDepth 2048
set_option maxHeartbeats 0

namespace SymmetricSector.Cert5

theorem d_1 : gradient 5 1 = (49 / 32 : ℚ) := by
  rw [gradient]
  norm_num only [show 1 < 5 by decide, if_true]
  rw [gradient]
  norm_num [c₀]

theorem d_2 : gradient 5 2 = (85 / 96 : ℚ) := by
  rw [gradient]
  norm_num only [show 2 < 5 by decide, if_true]
  rw [d_1]
  norm_num [c₀]

theorem d_3 : gradient 5 3 = (59 / 96 : ℚ) := by
  rw [gradient]
  norm_num only [show 3 < 5 by decide, if_true]
  rw [d_2]
  norm_num [c₀]

theorem d_4 : gradient 5 4 = (15 / 32 : ℚ) := by
  rw [gradient]
  norm_num only [show 4 < 5 by decide, if_true]
  rw [d_3]
  norm_num [c₀]

theorem terminal_gradient : (4 : ℚ) * gradient 5 4 + 2*5*(1/5 - c₀ 5) = 0 := by
  rw [d_4]
  norm_num [c₀]

def response : Channel 5 → ℚ
  | .inl i => ![(30212495 / 33353856 : ℚ), (19068115 / 33353856 : ℚ), (4669745 / 11117952 : ℚ), (25 / 64 : ℚ)] i
  | .inr i => ![(6776225 / 11117952 : ℚ), (11566925 / 33353856 : ℚ), (5819275 / 22235904 : ℚ)] i

theorem equations : (1 - coefficientK 5).mulVec response = source 5 := by
  apply funext
  decide +kernel

theorem value : reducedScalar 5 = (176345 / 14823936 : ℚ) := by
  unfold reducedScalar
  rw [← witness_eq_inverse_mulVec (1 - coefficientK 5)
    (coefficient_system_isUnit 5 (by norm_num))
    (source 5) response equations]
  decide +kernel

theorem positive : 0 < reducedScalar 5 := by rw [value]; norm_num

end SymmetricSector.Cert5
