import SymmetricSector.Small06
import SymmetricSector.Definitions
import SymmetricSector.Phase
import SymmetricSector.RowBounds

open SymmetricSector.Phase

set_option maxRecDepth 2048
set_option maxHeartbeats 0

namespace SymmetricSector.Cert7

theorem d_1 : gradient 7 1 = (107 / 64 : ℚ) := by
  rw [gradient]
  norm_num only [show 1 < 7 by decide, if_true]
  rw [gradient]
  norm_num [c₀]

theorem d_2 : gradient 7 2 = (301 / 320 : ℚ) := by
  rw [gradient]
  norm_num only [show 2 < 7 by decide, if_true]
  rw [d_1]
  norm_num [c₀]

theorem d_3 : gradient 7 3 = (619 / 960 : ℚ) := by
  rw [gradient]
  norm_num only [show 3 < 7 by decide, if_true]
  rw [d_2]
  norm_num [c₀]

theorem d_4 : gradient 7 4 = (469 / 960 : ℚ) := by
  rw [gradient]
  norm_num only [show 4 < 7 by decide, if_true]
  rw [d_3]
  norm_num [c₀]

theorem d_5 : gradient 7 5 = (377 / 960 : ℚ) := by
  rw [gradient]
  norm_num only [show 5 < 7 by decide, if_true]
  rw [d_4]
  norm_num [c₀]

theorem d_6 : gradient 7 6 = (21 / 64 : ℚ) := by
  rw [gradient]
  norm_num only [show 6 < 7 by decide, if_true]
  rw [d_5]
  norm_num [c₀]

theorem terminal_gradient : (6 : ℚ) * gradient 7 6 + 2*7*(1/7 - c₀ 7) = 0 := by
  rw [d_6]
  norm_num [c₀]

def response : Channel 7 → ℚ
  | .inl i => ![(2829053018309 / 2729255632000 : ℚ), (1735889598597 / 2729255632000 : ℚ), (3771224628983 / 8187766896000 : ℚ), (989290448293 / 2729255632000 : ℚ), (490711453379 / 1637553379200 : ℚ), (147 / 512 : ℚ)] i
  | .inr i => ![(1921289286609 / 2729255632000 : ℚ), (650420062229 / 1637553379200 : ℚ), (2187985078937 / 8187766896000 : ℚ), (64577161691 / 327510675840 : ℚ), (2221279419401 / 13100427033600 : ℚ)] i

theorem equations : (1 - coefficientK 7).mulVec response = source 7 := by
  apply funext
  decide +kernel

theorem value : reducedScalar 7 = (385860864319 / 43668090112000 : ℚ) := by
  unfold reducedScalar
  rw [← witness_eq_inverse_mulVec (1 - coefficientK 7)
    (coefficient_system_isUnit 7 (by norm_num))
    (source 7) response equations]
  decide +kernel

theorem positive : 0 < reducedScalar 7 := by rw [value]; norm_num

end SymmetricSector.Cert7
