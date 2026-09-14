import SymmetricSector.Small09
import SymmetricSector.Definitions
import SymmetricSector.Phase
import SymmetricSector.RowBounds

open SymmetricSector.Phase

set_option maxRecDepth 2048
set_option maxHeartbeats 0

namespace SymmetricSector.Cert10

theorem d_1 : gradient 10 1 = (4097 / 2304 : ℚ) := by
  rw [gradient]
  norm_num only [show 1 < 10 by decide, if_true]
  rw [gradient]
  norm_num [c₀]

theorem d_2 : gradient 10 2 = (8965 / 9216 : ℚ) := by
  rw [gradient]
  norm_num only [show 2 < 10 by decide, if_true]
  rw [d_1]
  norm_num [c₀]

theorem d_3 : gradient 10 3 = (21271 / 32256 : ℚ) := by
  rw [gradient]
  norm_num only [show 3 < 10 by decide, if_true]
  rw [d_2]
  norm_num [c₀]

theorem d_4 : gradient 10 4 = (32065 / 64512 : ℚ) := by
  rw [gradient]
  norm_num only [show 4 < 10 by decide, if_true]
  rw [d_3]
  norm_num [c₀]

theorem d_5 : gradient 10 5 = (251 / 630 : ℚ) := by
  rw [gradient]
  norm_num only [show 5 < 10 by decide, if_true]
  rw [d_4]
  norm_num [c₀]

theorem d_6 : gradient 10 6 = (21439 / 64512 : ℚ) := by
  rw [gradient]
  norm_num only [show 6 < 10 by decide, if_true]
  rw [d_5]
  norm_num [c₀]

theorem d_7 : gradient 10 7 = (9193 / 32256 : ℚ) := by
  rw [gradient]
  norm_num only [show 7 < 10 by decide, if_true]
  rw [d_6]
  norm_num [c₀]

theorem d_8 : gradient 10 8 = (2299 / 9216 : ℚ) := by
  rw [gradient]
  norm_num only [show 8 < 10 by decide, if_true]
  rw [d_7]
  norm_num [c₀]

theorem d_9 : gradient 10 9 = (511 / 2304 : ℚ) := by
  rw [gradient]
  norm_num only [show 9 < 10 by decide, if_true]
  rw [d_8]
  norm_num [c₀]

theorem terminal_gradient : (9 : ℚ) * gradient 10 9 + 2*10*(1/10 - c₀ 10) = 0 := by
  rw [d_9]
  norm_num [c₀]

def response : Channel 10 → ℚ
  | .inl i => ![(12557111661000746969 / 11005572941757570048 : ℚ), (315161276355676688197 / 462234063553817942016 : ℚ), (7049574354278047757 / 14444814486056810688 : ℚ), (41995782663018259439 / 110055729417575700480 : ℚ), (72597157175142980077 / 231117031776908971008 : ℚ), (123598385227561383995 / 462234063553817942016 : ℚ), (2992361066053263645 / 12839835098717165056 : ℚ), (13649489020641444475 / 66033437650545420288 : ℚ), (2555 / 12672 : ℚ)] i
  | .inr i => ![(360107896389988808597 / 462234063553817942016 : ℚ), (201325872899914137961 / 462234063553817942016 : ℚ), (226246995622513869679 / 770390105923029903360 : ℚ), (503349948135004370423 / 2311170317769089710080 : ℚ), (79039015621694760851 / 462234063553817942016 : ℚ), (21486751256007947125 / 154078021184605980672 : ℚ), (54020340286837235135 / 462234063553817942016 : ℚ), (6529189839884507135 / 60530651179666635264 : ℚ)] i

theorem equations : (1 - coefficientK 10).mulVec response = source 10 := by
  apply funext
  decide +kernel

theorem value : reducedScalar 10 = (14700724333113143041 / 2582641116999109771264 : ℚ) := by
  unfold reducedScalar
  rw [← witness_eq_inverse_mulVec (1 - coefficientK 10)
    (coefficient_system_isUnit 10 (by norm_num))
    (source 10) response equations]
  decide +kernel

theorem positive : 0 < reducedScalar 10 := by rw [value]; norm_num

end SymmetricSector.Cert10
