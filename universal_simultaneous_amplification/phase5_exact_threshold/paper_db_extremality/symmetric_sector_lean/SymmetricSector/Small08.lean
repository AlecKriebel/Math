import SymmetricSector.Small07
import SymmetricSector.Definitions
import SymmetricSector.Phase
import SymmetricSector.RowBounds

open SymmetricSector.Phase

set_option maxRecDepth 2048
set_option maxHeartbeats 0

namespace SymmetricSector.Cert8

theorem d_1 : gradient 8 1 = (769 / 448 : ℚ) := by
  rw [gradient]
  norm_num only [show 1 < 8 by decide, if_true]
  rw [gradient]
  norm_num [c₀]

theorem d_2 : gradient 8 2 = (107 / 112 : ℚ) := by
  rw [gradient]
  norm_num only [show 2 < 8 by decide, if_true]
  rw [d_1]
  norm_num [c₀]

theorem d_3 : gradient 8 3 = (4381 / 6720 : ℚ) := by
  rw [gradient]
  norm_num only [show 3 < 8 by decide, if_true]
  rw [d_2]
  norm_num [c₀]

theorem d_4 : gradient 8 4 = (69 / 140 : ℚ) := by
  rw [gradient]
  norm_num only [show 4 < 8 by decide, if_true]
  rw [d_3]
  norm_num [c₀]

theorem d_5 : gradient 8 5 = (2659 / 6720 : ℚ) := by
  rw [gradient]
  norm_num only [show 5 < 8 by decide, if_true]
  rw [d_4]
  norm_num [c₀]

theorem d_6 : gradient 8 6 = (37 / 112 : ℚ) := by
  rw [gradient]
  norm_num only [show 6 < 8 by decide, if_true]
  rw [d_5]
  norm_num [c₀]

theorem d_7 : gradient 8 7 = (127 / 448 : ℚ) := by
  rw [gradient]
  norm_num only [show 7 < 8 by decide, if_true]
  rw [d_6]
  norm_num [c₀]

theorem terminal_gradient : (7 : ℚ) * gradient 8 7 + 2*8*(1/8 - c₀ 8) = 0 := by
  rw [d_7]
  norm_num [c₀]

def response : Channel 8 → ℚ
  | .inl i => ![(20064975882319 / 18583514825085 : ℚ), (38988244681747 / 59467247440272 : ℚ), (117071522975839 / 247780197667800 : ℚ), (275625157113359 / 743340593003400 : ℚ), (324906874093 / 1061915132862 : ℚ), (5171908406555 / 19822415813424 : ℚ), (127 / 504 : ℚ)] i
  | .inr i => ![(910660030313 / 1238900988339 : ℚ), (15359399653589 / 37167029650170 : ℚ), (2067931983097 / 7433405930034 : ℚ), (909786657542 / 4424646386925 : ℚ), (2989214356778 / 18583514825085 : ℚ), (58996492699 / 412966996113 : ℚ)] i

theorem equations : (1 - coefficientK 8).mulVec response = source 8 := by
  apply funext
  decide +kernel

theorem value : reducedScalar 8 = (5420382036149 / 713606969283264 : ℚ) := by
  unfold reducedScalar
  rw [← witness_eq_inverse_mulVec (1 - coefficientK 8)
    (coefficient_system_isUnit 8 (by norm_num))
    (source 8) response equations]
  decide +kernel

theorem positive : 0 < reducedScalar 8 := by rw [value]; norm_num

end SymmetricSector.Cert8
