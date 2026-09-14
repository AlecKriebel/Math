import SymmetricSector.GeneratedMargins.Order050

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w51 : List ℕ := [0, 10099, 10300, 10511, 10729, 10957, 11195, 11443, 11703, 11974, 12258, 12555, 12867, 13195, 13540, 13902, 14285, 14688, 15115, 15567, 16046, 16554, 17095, 17672, 18287, 18946, 19653, 20413, 21231, 22116, 23074, 24115, 25250, 26492, 27856, 29359, 31023, 32874, 34942, 37266, 39893, 42880, 46301, 50248, 54839, 60226, 66610, 74255, 83518, 94884, 109025]

theorem cert51 : MarginCertificate 51 w51 (1 / 100) := by decide +kernel

theorem bound51 : beta 51 + epsilon 51 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert51

end SymmetricSector.GeneratedMargins
