import SymmetricSector.Small13
import SymmetricSector.Definitions
import SymmetricSector.Phase
import SymmetricSector.RowBounds

open SymmetricSector.Phase

set_option maxRecDepth 2048
set_option maxHeartbeats 0

namespace SymmetricSector.Cert14

theorem d_1 : gradient 14 1 = (98305 / 53248 : ℚ) := by
  rw [gradient]
  norm_num only [show 1 < 14 by decide, if_true]
  rw [gradient]
  norm_num [c₀]

theorem d_2 : gradient 14 2 = (105133 / 106496 : ℚ) := by
  rw [gradient]
  norm_num only [show 2 < 14 by decide, if_true]
  rw [d_1]
  norm_num [c₀]

theorem d_3 : gradient 14 3 = (583703 / 878592 : ℚ) := by
  rw [gradient]
  norm_num only [show 3 < 14 by decide, if_true]
  rw [d_2]
  norm_num [c₀]

theorem d_4 : gradient 14 4 = (2924733 / 5857280 : ℚ) := by
  rw [gradient]
  norm_num only [show 4 < 14 by decide, if_true]
  rw [d_3]
  norm_num [c₀]

theorem d_5 : gradient 14 5 = (2107201 / 5271552 : ℚ) := by
  rw [gradient]
  norm_num only [show 5 < 14 by decide, if_true]
  rw [d_4]
  norm_num [c₀]

theorem d_6 : gradient 14 6 = (3512915 / 10543104 : ℚ) := by
  rw [gradient]
  norm_num only [show 6 < 14 by decide, if_true]
  rw [d_5]
  norm_num [c₀]

theorem d_7 : gradient 14 7 = (3431 / 12012 : ℚ) := by
  rw [gradient]
  norm_num only [show 7 < 14 by decide, if_true]
  rw [d_6]
  norm_num [c₀]

theorem d_8 : gradient 14 8 = (2635181 / 10543104 : ℚ) := by
  rw [gradient]
  norm_num only [show 8 < 14 by decide, if_true]
  rw [d_7]
  norm_num [c₀]

theorem d_9 : gradient 14 9 = (5856187 / 26357760 : ℚ) := by
  rw [gradient]
  norm_num only [show 9 < 14 by decide, if_true]
  rw [d_8]
  norm_num [c₀]

theorem d_10 : gradient 14 10 = (1171267 / 5857280 : ℚ) := by
  rw [gradient]
  norm_num only [show 10 < 14 by decide, if_true]
  rw [d_9]
  norm_num [c₀]

theorem d_11 : gradient 14 11 = (159721 / 878592 : ℚ) := by
  rw [gradient]
  norm_num only [show 11 < 14 by decide, if_true]
  rw [d_10]
  norm_num [c₀]

theorem d_12 : gradient 14 12 = (17747 / 106496 : ℚ) := by
  rw [gradient]
  norm_num only [show 12 < 14 by decide, if_true]
  rw [d_11]
  norm_num [c₀]

theorem d_13 : gradient 14 13 = (8191 / 53248 : ℚ) := by
  rw [gradient]
  norm_num only [show 13 < 14 by decide, if_true]
  rw [d_12]
  norm_num [c₀]

theorem terminal_gradient : (13 : ℚ) * gradient 14 13 + 2*14*(1/14 - c₀ 14) = 0 := by
  rw [d_13]
  norm_num [c₀]

def response : Channel 14 → ℚ
  | .inl i => ![(10976429499812583100411185073081 / 9062742129046993217995340267520 : ℚ), (70726985338123961205051526453153 / 99690163419516925397948742942720 : ℚ), (83781521469380649932646900923371 / 166150272365861542329914571571200 : ℚ), (195845789475861871949690602497107 / 498450817097584626989743714713600 : ℚ), (32173631833804560707053979158319 / 99690163419516925397948742942720 : ℚ), (12760906403068373340128722854037 / 46522076262441231852376080039936 : ℚ), (1586845655763476974135567445735 / 6646010894634461693196582862848 : ℚ), (7029685806862179816231581396657 / 33230054473172308465982914314240 : ℚ), (2104580468059993140973267525811 / 11076684824390769488660971438080 : ℚ), (17197484819508219905905414135801 / 99690163419516925397948742942720 : ℚ), (286412752127474056660235449475 / 1812548425809398643599068053504 : ℚ), (8008526329532151413164790441 / 54925709873012080109062668288 : ℚ), (57337 / 399360 : ℚ)] i
  | .inr i => ![(55119257969022867512880422010193 / 66460108946344616931965828628480 : ℚ), (459280917820754035539013957143053 / 996901634195169253979487429427200 : ℚ), (62193526108174941831370867756369 / 199380326839033850795897485885440 : ℚ), (77338479879247436586623701322909 / 332300544731723084659829143142400 : ℚ), (256577169195831553963333786237361 / 1395662287873236955571282401198080 : ℚ), (14028758532700572484713264865741 / 93044152524882463704752160079872 : ℚ), (937867690164342325935546342383 / 7384456549593846325773980958720 : ℚ), (1450785361859311212782702436313 / 13292021789268923386393165725696 : ℚ), (1461229168395700129565370317863 / 15336948218387219291992114298880 : ℚ), (5596933446603120165045425673323 / 66460108946344616931965828628480 : ℚ), (272641290103061912984866698959 / 3625096851618797287198136107008 : ℚ), (9865657915808000840235224747 / 137314274682530200272656670720 : ℚ)] i

theorem equations : (1 - coefficientK 14).mulVec response = source 14 := by
  apply funext
  decide +kernel

theorem value : reducedScalar 14 = (640673660611955778294807707 / 185902402647117809599904415744 : ℚ) := by
  unfold reducedScalar
  rw [← witness_eq_inverse_mulVec (1 - coefficientK 14)
    (coefficient_system_isUnit 14 (by norm_num))
    (source 14) response equations]
  decide +kernel

theorem positive : 0 < reducedScalar 14 := by rw [value]; norm_num

end SymmetricSector.Cert14
