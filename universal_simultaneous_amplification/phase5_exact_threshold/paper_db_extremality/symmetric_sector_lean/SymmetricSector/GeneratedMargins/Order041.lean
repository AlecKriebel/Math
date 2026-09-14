import SymmetricSector.GeneratedMargins.Order040

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w41 : List ℕ := [0, 10123, 10376, 10642, 10922, 11216, 11527, 11855, 12202, 12570, 12960, 13374, 13815, 14286, 14789, 15329, 15908, 16531, 17203, 17931, 18720, 19580, 20519, 21549, 22683, 23936, 25328, 26882, 28626, 30594, 32831, 35390, 38341, 41773, 45802, 50580, 56310, 63270, 71840, 82556, 96182]

theorem cert41 : MarginCertificate 41 w41 (1 / 100) := by decide +kernel

theorem bound41 : beta 41 + epsilon 41 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert41

end SymmetricSector.GeneratedMargins
