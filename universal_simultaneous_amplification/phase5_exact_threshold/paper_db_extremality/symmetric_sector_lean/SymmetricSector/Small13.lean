import SymmetricSector.Small12
import SymmetricSector.Definitions
import SymmetricSector.Phase
import SymmetricSector.RowBounds

open SymmetricSector.Phase

set_option maxRecDepth 2048
set_option maxHeartbeats 0

namespace SymmetricSector.Cert13

theorem d_1 : gradient 13 1 = (15019 / 8192 : ℚ) := by
  rw [gradient]
  norm_num only [show 1 < 13 by decide, if_true]
  rw [gradient]
  norm_num [c₀]

theorem d_2 : gradient 13 2 = (88751 / 90112 : ℚ) := by
  rw [gradient]
  norm_num only [show 2 < 13 by decide, if_true]
  rw [d_1]
  norm_num [c₀]

theorem d_3 : gradient 13 3 = (897103 / 1351680 : ℚ) := by
  rw [gradient]
  norm_num only [show 3 < 13 by decide, if_true]
  rw [d_2]
  norm_num [c₀]

theorem d_4 : gradient 13 4 = (2023723 / 4055040 : ℚ) := by
  rw [gradient]
  norm_num only [show 4 < 13 by decide, if_true]
  rw [d_3]
  norm_num [c₀]

theorem d_5 : gradient 13 5 = (324073 / 811008 : ℚ) := by
  rw [gradient]
  norm_num only [show 5 < 13 by decide, if_true]
  rw [d_4]
  norm_num [c₀]

theorem d_6 : gradient 13 6 = (1891097 / 5677056 : ℚ) := by
  rw [gradient]
  norm_num only [show 6 < 13 by decide, if_true]
  rw [d_5]
  norm_num [c₀]

theorem d_7 : gradient 13 7 = (1621223 / 5677056 : ℚ) := by
  rw [gradient]
  norm_num only [show 7 < 13 by decide, if_true]
  rw [d_6]
  norm_num [c₀]

theorem d_8 : gradient 13 8 = (1013363 / 4055040 : ℚ) := by
  rw [gradient]
  norm_num only [show 8 < 13 by decide, if_true]
  rw [d_7]
  norm_num [c₀]

theorem d_9 : gradient 13 9 = (900821 / 4055040 : ℚ) := by
  rw [gradient]
  norm_num only [show 9 < 13 by decide, if_true]
  rw [d_8]
  norm_num [c₀]

theorem d_10 : gradient 13 10 = (270257 / 1351680 : ℚ) := by
  rw [gradient]
  norm_num only [show 10 < 13 by decide, if_true]
  rw [d_9]
  norm_num [c₀]

theorem d_11 : gradient 13 11 = (49139 / 270336 : ℚ) := by
  rw [gradient]
  norm_num only [show 11 < 13 by decide, if_true]
  rw [d_10]
  norm_num [c₀]

theorem d_12 : gradient 13 12 = (1365 / 8192 : ℚ) := by
  rw [gradient]
  norm_num only [show 12 < 13 by decide, if_true]
  rw [d_11]
  norm_num [c₀]

theorem terminal_gradient : (12 : ℚ) * gradient 13 12 + 2*13*(1/13 - c₀ 13) = 0 := by
  rw [d_12]
  norm_num [c₀]

def response : Channel 13 → ℚ
  | .inl i => ![(1900663557251774398541771458290301 / 1586940988699289950291864533893120 : ℚ), (223550676825761717767190942287617 / 317388197739857990058372906778624 : ℚ), (35794409513344004510007465288939017 / 71412344491468047763133904025190400 : ℚ), (4651112053888630650336426596697199 / 11902057415244674627188984004198400 : ℚ), (729613195616881698564227865122797 / 2272210961092165156099715128074240 : ℚ), (248108388828287000817802671708425 / 908884384436866062439886051229696 : ℚ), (17144140315883106898768158168887 / 72133681304513179558721115176960 : ℚ), (39066289005537738971952408633241 / 185486609068748176008140010455040 : ℚ), (11697778884294162151393892515993 / 61828869689582725336046670151680 : ℚ), (3540818225793449257033335637159 / 20609623229860908445348890050560 : ℚ), (1946273470635835408522646677369 / 12365773937916545067209334030336 : ℚ), (2535 / 16384 : ℚ)] i
  | .inr i => ![(260163130444605318120928112161683 / 317388197739857990058372906778624 : ℚ), (6510949409079570993468344501628047 / 14282468898293609552626780805038080 : ℚ), (1761466515310309519826728958776991 / 5712987559317443821050712322015232 : ℚ), (2609867807726973413521656990557023 / 11361054805460825780498575640371200 : ℚ), (26142541735802636559794141287057 / 144267362609026359117442230353920 : ℚ), (337270292919558955388406305686979 / 2272210961092165156099715128074240 : ℚ), (324318179237019034868896963061701 / 2596812526962474464113960146370560 : ℚ), (19887774144752578179693859667711 / 185486609068748176008140010455040 : ℚ), (17343886445293498165179944412599 / 185486609068748176008140010455040 : ℚ), (5105771890837781967974349436387 / 61828869689582725336046670151680 : ℚ), (1939643950416225284726482157287 / 24731547875833090134418668060672 : ℚ)] i

theorem equations : (1 - coefficientK 13).mulVec response = source 13 := by
  apply funext
  decide +kernel

theorem value : reducedScalar 13 = (39313283481666805460661717943349 / 10156422327675455681867933016915968 : ℚ) := by
  unfold reducedScalar
  rw [← witness_eq_inverse_mulVec (1 - coefficientK 13)
    (coefficient_system_isUnit 13 (by norm_num))
    (source 13) response equations]
  decide +kernel

theorem positive : 0 < reducedScalar 13 := by rw [value]; norm_num

end SymmetricSector.Cert13
