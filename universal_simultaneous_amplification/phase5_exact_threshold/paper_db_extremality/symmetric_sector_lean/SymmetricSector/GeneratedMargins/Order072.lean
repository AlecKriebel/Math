import SymmetricSector.GeneratedMargins.Order071

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w72 : List ℕ := [0, 10069, 10211, 10357, 10507, 10662, 10821, 10984, 11153, 11327, 11507, 11692, 11883, 12080, 12284, 12495, 12714, 12940, 13174, 13417, 13668, 13929, 14200, 14482, 14775, 15080, 15398, 15729, 16074, 16435, 16812, 17206, 17619, 18052, 18506, 18983, 19485, 20013, 20570, 21158, 21780, 22438, 23136, 23878, 24667, 25508, 26406, 27367, 28398, 29506, 30699, 31988, 33384, 34900, 36552, 38357, 40336, 42515, 44922, 47593, 50571, 53906, 57661, 61913, 66756, 72308, 78718, 86173, 94915, 105256, 117603, 132496]

theorem cert72 : MarginCertificate 72 w72 (1 / 100) := by decide +kernel

theorem bound72 : beta 72 + epsilon 72 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert72

end SymmetricSector.GeneratedMargins
