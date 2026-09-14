import SymmetricSector.Small10
import SymmetricSector.Definitions
import SymmetricSector.Phase
import SymmetricSector.RowBounds

open SymmetricSector.Phase

set_option maxRecDepth 2048
set_option maxHeartbeats 0

namespace SymmetricSector.Cert11

theorem d_1 : gradient 11 1 = (9217 / 5120 : ℚ) := by
  rw [gradient]
  norm_num only [show 1 < 11 by decide, if_true]
  rw [gradient]
  norm_num [c₀]

theorem d_2 : gradient 11 2 = (45067 / 46080 : ℚ) := by
  rw [gradient]
  norm_num only [show 2 < 11 by decide, if_true]
  rw [d_1]
  norm_num [c₀]

theorem d_3 : gradient 11 3 = (15239 / 23040 : ℚ) := by
  rw [gradient]
  norm_num only [show 3 < 11 by decide, if_true]
  rw [d_2]
  norm_num [c₀]

theorem d_4 : gradient 11 4 = (13387 / 26880 : ℚ) := by
  rw [gradient]
  norm_num only [show 4 < 11 by decide, if_true]
  rw [d_3]
  norm_num [c₀]

theorem d_5 : gradient 11 5 = (25741 / 64512 : ℚ) := by
  rw [gradient]
  norm_num only [show 5 < 11 by decide, if_true]
  rw [d_4]
  norm_num [c₀]

theorem d_6 : gradient 11 6 = (107327 / 322560 : ℚ) := by
  rw [gradient]
  norm_num only [show 6 < 11 by decide, if_true]
  rw [d_5]
  norm_num [c₀]

theorem d_7 : gradient 11 7 = (7669 / 26880 : ℚ) := by
  rw [gradient]
  norm_num only [show 7 < 11 by decide, if_true]
  rw [d_6]
  norm_num [c₀]

theorem d_8 : gradient 11 8 = (5753 / 23040 : ℚ) := by
  rw [gradient]
  norm_num only [show 8 < 11 by decide, if_true]
  rw [d_7]
  norm_num [c₀]

theorem d_9 : gradient 11 9 = (10229 / 46080 : ℚ) := by
  rw [gradient]
  norm_num only [show 9 < 11 by decide, if_true]
  rw [d_8]
  norm_num [c₀]

theorem d_10 : gradient 11 10 = (1023 / 5120 : ℚ) := by
  rw [gradient]
  norm_num only [show 10 < 11 by decide, if_true]
  rw [d_9]
  norm_num [c₀]

theorem terminal_gradient : (10 : ℚ) * gradient 11 10 + 2*11*(1/11 - c₀ 11) = 0 := by
  rw [d_10]
  norm_num [c₀]

def response : Channel 11 → ℚ
  | .inl i => ![(83555964959988260790095221 / 71824541099610274136340480 : ℚ), (14178038952683514263580049 / 20521297457031506896097280 : ℚ), (165363457847185584237965417 / 335181191798181279302922240 : ℚ), (10761506654781730599056833 / 27931765983181773275243520 : ℚ), (2950610963197201562767729 / 9310588661060591091747840 : ℚ), (10041333466406607808410649 / 37242354644242364366991360 : ℚ), (11247252854911665201849877 / 47883027399740182757560320 : ℚ), (712287646723042578626053 / 3420216242838584482682880 : ℚ), (71126563966816606149011 / 380024026982064942520320 : ℚ), (3751 / 20480 : ℚ)] i
  | .inr i => ![(10877446396150413767490781 / 13680864971354337930731520 : ℚ), (111508128517961288447742287 / 251385893848635959477191680 : ℚ), (200693151569085869984741473 / 670362383596362558605844480 : ℚ), (7042391564109991207129 / 31668668915172078543360 : ℚ), (1860905390064949503933779 / 10640672755497818390568960 : ℚ), (5985168429310320649138993 / 41897648974772659912865280 : ℚ), (182242192790264088142969 / 1520096107928259770081280 : ℚ), (175603838724910053799033 / 1710108121419292241341440 : ℚ), (145814860895617539868759 / 1520096107928259770081280 : ℚ)] i

theorem equations : (1 - coefficientK 11).mulVec response = source 11 := by
  apply funext
  decide +kernel

theorem value : reducedScalar 11 = (571539495163858763086501 / 114919265759376438618144768 : ℚ) := by
  unfold reducedScalar
  rw [← witness_eq_inverse_mulVec (1 - coefficientK 11)
    (coefficient_system_isUnit 11 (by norm_num))
    (source 11) response equations]
  decide +kernel

theorem positive : 0 < reducedScalar 11 := by rw [value]; norm_num

end SymmetricSector.Cert11
