import SymmetricSector.Small08
import SymmetricSector.Definitions
import SymmetricSector.Phase
import SymmetricSector.RowBounds

open SymmetricSector.Phase

set_option maxRecDepth 2048
set_option maxHeartbeats 0

namespace SymmetricSector.Cert9

theorem d_1 : gradient 9 1 = (1793 / 1024 : ℚ) := by
  rw [gradient]
  norm_num only [show 1 < 9 by decide, if_true]
  rw [gradient]
  norm_num [c₀]

theorem d_2 : gradient 9 2 = (6921 / 7168 : ℚ) := by
  rw [gradient]
  norm_num only [show 2 < 9 by decide, if_true]
  rw [d_1]
  norm_num [c₀]

theorem d_3 : gradient 9 3 = (14117 / 21504 : ℚ) := by
  rw [gradient]
  norm_num only [show 3 < 9 by decide, if_true]
  rw [d_2]
  norm_num [c₀]

theorem d_4 : gradient 9 4 = (17757 / 35840 : ℚ) := by
  rw [gradient]
  norm_num only [show 4 < 9 by decide, if_true]
  rw [d_3]
  norm_num [c₀]

theorem d_5 : gradient 9 5 = (14243 / 35840 : ℚ) := by
  rw [gradient]
  norm_num only [show 5 < 9 by decide, if_true]
  rw [d_4]
  norm_num [c₀]

theorem d_6 : gradient 9 6 = (2377 / 7168 : ℚ) := by
  rw [gradient]
  norm_num only [show 6 < 9 by decide, if_true]
  rw [d_5]
  norm_num [c₀]

theorem d_7 : gradient 9 7 = (2039 / 7168 : ℚ) := by
  rw [gradient]
  norm_num only [show 7 < 9 by decide, if_true]
  rw [d_6]
  norm_num [c₀]

theorem d_8 : gradient 9 8 = (255 / 1024 : ℚ) := by
  rw [gradient]
  norm_num only [show 8 < 9 by decide, if_true]
  rw [d_7]
  norm_num [c₀]

theorem terminal_gradient : (8 : ℚ) * gradient 9 8 + 2*9*(1/9 - c₀ 9) = 0 := by
  rw [d_8]
  norm_num [c₀]

def response : Channel 9 → ℚ
  | .inl i => ![(391499356579902357 / 351536258334679040 : ℚ), (12403508414501499 / 18501908333404160 : ℚ), (845955390868413757 / 1757681291673395200 : ℚ), (662491903493590353 / 1757681291673395200 : ℚ), (15597397203307371 / 50219465476382720 : ℚ), (2657477347910787 / 10043893095276544 : ℚ), (2317546806903675 / 10043893095276544 : ℚ), (459 / 2048 : ℚ)] i
  | .inr i => ![(266981650093536909 / 351536258334679040 : ℚ), (748212192277469331 / 1757681291673395200 : ℚ), (100811196689430681 / 351536258334679040 : ℚ), (750874751201727 / 3536582075801600 : ℚ), (8356628603417139 / 50219465476382720 : ℚ), (1360755053929125 / 10043893095276544 : ℚ), (2471688869732235 / 20087786190553088 : ℚ)] i

theorem equations : (1 - coefficientK 9).mulVec response = source 9 := by
  apply funext
  decide +kernel

theorem value : reducedScalar 9 = (1843878454004847 / 281229006667743232 : ℚ) := by
  unfold reducedScalar
  rw [← witness_eq_inverse_mulVec (1 - coefficientK 9)
    (coefficient_system_isUnit 9 (by norm_num))
    (source 9) response equations]
  decide +kernel

theorem positive : 0 < reducedScalar 9 := by rw [value]; norm_num

end SymmetricSector.Cert9
