import SymmetricSector.Small11
import SymmetricSector.Definitions
import SymmetricSector.Phase
import SymmetricSector.RowBounds

open SymmetricSector.Phase

set_option maxRecDepth 2048
set_option maxHeartbeats 0

namespace SymmetricSector.Cert12

theorem d_1 : gradient 12 1 = (20481 / 11264 : ℚ) := by
  rw [gradient]
  norm_num only [show 1 < 12 by decide, if_true]
  rw [gradient]
  norm_num [c₀]

theorem d_2 : gradient 12 2 = (27651 / 28160 : ℚ) := by
  rw [gradient]
  norm_num only [show 2 < 12 by decide, if_true]
  rw [d_1]
  norm_num [c₀]

theorem d_3 : gradient 12 3 = (335939 / 506880 : ℚ) := by
  rw [gradient]
  norm_num only [show 3 < 12 by decide, if_true]
  rw [d_2]
  norm_num [c₀]

theorem d_4 : gradient 12 4 = (84253 / 168960 : ℚ) := by
  rw [gradient]
  norm_num only [show 4 < 12 by decide, if_true]
  rw [d_3]
  norm_num [c₀]

theorem d_5 : gradient 12 5 = (94469 / 236544 : ℚ) := by
  rw [gradient]
  norm_num only [show 5 < 12 by decide, if_true]
  rw [d_4]
  norm_num [c₀]

theorem d_6 : gradient 12 6 = (923 / 2772 : ℚ) := by
  rw [gradient]
  norm_num only [show 6 < 12 by decide, if_true]
  rw [d_5]
  norm_num [c₀]

theorem d_7 : gradient 12 7 = (337639 / 1182720 : ℚ) := by
  rw [gradient]
  norm_num only [show 7 < 12 by decide, if_true]
  rw [d_6]
  norm_num [c₀]

theorem d_8 : gradient 12 8 = (42211 / 168960 : ℚ) := by
  rw [gradient]
  norm_num only [show 8 < 12 by decide, if_true]
  rw [d_7]
  norm_num [c₀]

theorem d_9 : gradient 12 9 = (112573 / 506880 : ℚ) := by
  rw [gradient]
  norm_num only [show 9 < 12 by decide, if_true]
  rw [d_8]
  norm_num [c₀]

theorem d_10 : gradient 12 10 = (5629 / 28160 : ℚ) := by
  rw [gradient]
  norm_num only [show 10 < 12 by decide, if_true]
  rw [d_9]
  norm_num [c₀]

theorem d_11 : gradient 12 11 = (2047 / 11264 : ℚ) := by
  rw [gradient]
  norm_num only [show 11 < 12 by decide, if_true]
  rw [d_10]
  norm_num [c₀]

theorem terminal_gradient : (11 : ℚ) * gradient 12 11 + 2*12*(1/12 - c₀ 12) = 0 := by
  rw [d_11]
  norm_num [c₀]

def response : Channel 12 → ℚ
  | .inl i => ![(1565181099343557641739 / 1324231568418827622400 : ℚ), (3328744339941709780009 / 4767233646307779440640 : ℚ), (1186242410616097751657 / 2383616823153889720320 : ℚ), (12340161901940314698857 / 31781557642051862937600 : ℚ), (53258105826193784223403 / 166853177620772280422400 : ℚ), (150972472983533411175853 / 556177258735907601408000 : ℚ), (65739973553889353504897 / 278088629367953800704000 : ℚ), (14270077144389993961403 / 68103337804396849152000 : ℚ), (311631866896097606471 / 1655289460523534528000 : ℚ), (14151796774349806713 / 82764473026176726400 : ℚ), (6141 / 36608 : ℚ)] i
  | .inr i => ![(4817435979808835838013 / 5959042057884724300800 : ℚ), (1073190609562113789119 / 2383616823153889720320 : ℚ), (36620016023974681027 / 120384688038075238400 : ℚ), (2697099047493975914917 / 11918084115769448601600 : ℚ), (2655529525154569604941 / 14897605144711810752000 : ℚ), (5068642594317532335863 / 34761078670994225088000 : ℚ), (1022283892586465281609 / 8342658881038614021120 : ℚ), (6261843694192018083913 / 59590420578847243008000 : ℚ), (181844110853548897483 / 1986347352628241433600 : ℚ), (53067976014815778009 / 614821799623027110400 : ℚ)] i

theorem equations : (1 - coefficientK 12).mulVec response = source 12 := by
  apply funext
  decide +kernel

theorem value : reducedScalar 12 = (926696197875449223087 / 211877050947012419584000 : ℚ) := by
  unfold reducedScalar
  rw [← witness_eq_inverse_mulVec (1 - coefficientK 12)
    (coefficient_system_isUnit 12 (by norm_num))
    (source 12) response equations]
  decide +kernel

theorem positive : 0 < reducedScalar 12 := by rw [value]; norm_num

end SymmetricSector.Cert12
