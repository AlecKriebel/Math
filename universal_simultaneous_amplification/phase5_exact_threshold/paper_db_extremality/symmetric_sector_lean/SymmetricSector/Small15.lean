import SymmetricSector.Small14
import SymmetricSector.Definitions
import SymmetricSector.Phase
import SymmetricSector.RowBounds

open SymmetricSector.Phase

set_option maxRecDepth 2048
set_option maxHeartbeats 0

namespace SymmetricSector.Cert15

theorem d_1 : gradient 15 1 = (212993 / 114688 : ℚ) := by
  rw [gradient]
  norm_num only [show 1 < 15 by decide, if_true]
  rw [gradient]
  norm_num [c₀]

theorem d_2 : gradient 15 2 = (1474575 / 1490944 : ℚ) := by
  rw [gradient]
  norm_num only [show 2 < 15 by decide, if_true]
  rw [d_1]
  norm_num [c₀]

theorem d_3 : gradient 15 3 = (2973749 / 4472832 : ℚ) := by
  rw [gradient]
  norm_num only [show 3 < 15 by decide, if_true]
  rw [d_2]
  norm_num [c₀]

theorem d_4 : gradient 15 4 = (8192235 / 16400384 : ℚ) := by
  rw [gradient]
  norm_num only [show 4 < 15 by decide, if_true]
  rw [d_3]
  norm_num [c₀]

theorem d_5 : gradient 15 5 = (6557171 / 16400384 : ℚ) := by
  rw [gradient]
  norm_num only [show 5 < 15 by decide, if_true]
  rw [d_4]
  norm_num [c₀]

theorem d_6 : gradient 15 6 = (49188241 / 147603456 : ℚ) := by
  rw [gradient]
  norm_num only [show 6 < 15 by decide, if_true]
  rw [d_5]
  norm_num [c₀]

theorem d_7 : gradient 15 7 = (14054995 / 49201152 : ℚ) := by
  rw [gradient]
  norm_num only [show 7 < 15 by decide, if_true]
  rw [d_6]
  norm_num [c₀]

theorem d_8 : gradient 15 8 = (12298669 / 49201152 : ℚ) := by
  rw [gradient]
  norm_num only [show 8 < 15 by decide, if_true]
  rw [d_7]
  norm_num [c₀]

theorem d_9 : gradient 15 9 = (32797295 / 147603456 : ℚ) := by
  rw [gradient]
  norm_num only [show 9 < 15 by decide, if_true]
  rw [d_8]
  norm_num [c₀]

theorem d_10 : gradient 15 10 = (16398913 / 82001920 : ℚ) := by
  rw [gradient]
  norm_num only [show 10 < 15 by decide, if_true]
  rw [d_9]
  norm_num [c₀]

theorem d_11 : gradient 15 11 = (2981653 / 16400384 : ℚ) := by
  rw [gradient]
  norm_num only [show 11 < 15 by decide, if_true]
  rw [d_10]
  norm_num [c₀]

theorem d_12 : gradient 15 12 = (248473 / 1490944 : ℚ) := by
  rw [gradient]
  norm_num only [show 12 < 15 by decide, if_true]
  rw [d_11]
  norm_num [c₀]

theorem d_13 : gradient 15 13 = (229361 / 1490944 : ℚ) := by
  rw [gradient]
  norm_num only [show 13 < 15 by decide, if_true]
  rw [d_12]
  norm_num [c₀]

theorem d_14 : gradient 15 14 = (16383 / 114688 : ℚ) := by
  rw [gradient]
  norm_num only [show 14 < 15 by decide, if_true]
  rw [d_13]
  norm_num [c₀]

theorem terminal_gradient : (14 : ℚ) * gradient 15 14 + 2*15*(1/15 - c₀ 15) = 0 := by
  rw [d_14]
  norm_num [c₀]

def response : Channel 15 → ℚ
  | .inl i => ![(6008277979449055023619725697497133 / 4913464153606726986166361227821056 : ℚ), (10522301994157709075273190131364643 / 14740392460820180958499083683463168 : ℚ), (74642349695224822647331487987229 / 147270042751155304762479491842048 : ℚ), (9697873396580786627105493111808913 / 24567320768033634930831806139105280 : ℚ), (666440307752779042990470682017461 / 2055929633165959305285163827363840 : ℚ), (10306606406539288819121090423902079 / 37417919323620459356189981658021888 : ℚ), (996662520340277487035884667950207 / 4157546591513384372909997962002432 : ℚ), (2648707391198145033904242828901513 / 12472639774540153118729993886007296 : ℚ), (914854097656720228117179478781417 / 4797169144053905045665382263848960 : ℚ), (3598956537693142419150582952007763 / 20787732957566921864549989810012160 : ℚ), (1977735599188802524880515382756765 / 12472639774540153118729993886007296 : ℚ), (2154334396395568533746991403055 / 14725666794026154803695388295168 : ℚ), (51333649447023271887030044373225 / 377958781046671306628181632909312 : ℚ), (245745 / 1835008 : ℚ)] i
  | .inr i => ![(12348444076869127899927714246344129 / 14740392460820180958499083683463168 : ℚ), (75383925077128105135088342510264627 / 162144317069021990543489920518094848 : ℚ), (85158295979766808378756751052701159 / 270240528448369984239149867530158080 : ℚ), (6292297419799462543211772663811249 / 26727085231157470968707129755729920 : ℚ), (6967280167735328989597517292347893 / 37417919323620459356189981658021888 : ℚ), (635647203700937931619564311573321 / 4157546591513384372909997962002432 : ℚ), (1607994696576389525357362681243229 / 12472639774540153118729993886007296 : ℚ), (532000798305301733968615884618221 / 4797169144053905045665382263848960 : ℚ), (6042249291280645811651972942287427 / 62363198872700765593649969430036480 : ℚ), (1069013570901767895981379930512535 / 12472639774540153118729993886007296 : ℚ), (136485486899958239702371047116675 / 1781805682077164731247141983715328 : ℚ), (26097291040111516584055108093425 / 377958781046671306628181632909312 : ℚ), (57257009037429538201260185650725 / 863905785249534415150129446649856 : ℚ)] i

theorem equations : (1 - coefficientK 15).mulVec response = source 15 := by
  apply funext
  decide +kernel

theorem value : reducedScalar 15 = (485163358857836373921253419435157 / 157230852915415263557323559290273792 : ℚ) := by
  unfold reducedScalar
  rw [← witness_eq_inverse_mulVec (1 - coefficientK 15)
    (coefficient_system_isUnit 15 (by norm_num))
    (source 15) response equations]
  decide +kernel

theorem positive : 0 < reducedScalar 15 := by rw [value]; norm_num

end SymmetricSector.Cert15
