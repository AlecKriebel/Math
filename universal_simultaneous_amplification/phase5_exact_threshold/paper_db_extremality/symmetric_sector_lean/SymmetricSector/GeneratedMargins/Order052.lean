import SymmetricSector.GeneratedMargins.Order051

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w52 : List ℕ := [0, 10097, 10295, 10500, 10715, 10937, 11170, 11412, 11665, 11929, 12205, 12495, 12798, 13116, 13450, 13801, 14170, 14560, 14971, 15405, 15865, 16353, 16870, 17421, 18008, 18635, 19306, 20025, 20798, 21631, 22531, 23505, 24564, 25718, 26981, 28367, 29894, 31584, 33463, 35562, 37920, 40584, 43612, 47077, 51071, 55713, 61156, 67599, 75306, 84630, 96053, 110238]

theorem cert52 : MarginCertificate 52 w52 (1 / 100) := by decide +kernel

theorem bound52 : beta 52 + epsilon 52 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert52

end SymmetricSector.GeneratedMargins
