import SymmetricSector.GeneratedMargins.Order063

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w64 : List ℕ := [0, 10078, 10238, 10403, 10574, 10750, 10932, 11120, 11315, 11516, 11725, 11942, 12166, 12399, 12641, 12893, 13155, 13427, 13711, 14007, 14316, 14638, 14975, 15328, 15697, 16084, 16491, 16918, 17367, 17841, 18340, 18868, 19426, 20017, 20644, 21310, 22020, 22777, 23586, 24452, 25382, 26382, 27461, 28627, 29892, 31268, 32769, 34412, 36217, 38207, 40412, 42864, 45606, 48686, 52167, 56123, 60649, 65864, 71917, 79002, 87369, 97345, 109364, 124008]

theorem cert64 : MarginCertificate 64 w64 (1 / 100) := by decide +kernel

theorem bound64 : beta 64 + epsilon 64 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert64

end SymmetricSector.GeneratedMargins
