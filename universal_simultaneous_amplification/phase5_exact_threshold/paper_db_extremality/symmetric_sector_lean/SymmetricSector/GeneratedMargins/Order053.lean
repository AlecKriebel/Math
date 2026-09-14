import SymmetricSector.GeneratedMargins.Order052

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w53 : List ℕ := [0, 10095, 10289, 10491, 10700, 10918, 11145, 11382, 11629, 11886, 12155, 12437, 12731, 13040, 13364, 13704, 14061, 14437, 14834, 15253, 15695, 16163, 16659, 17186, 17747, 18344, 18982, 19664, 20396, 21182, 22029, 22944, 23936, 25013, 26186, 27469, 28877, 30428, 32144, 34051, 36181, 38572, 41272, 44340, 47848, 51890, 56584, 62082, 68583, 76350, 85734, 97212, 111440]

theorem cert53 : MarginCertificate 53 w53 (1 / 100) := by decide +kernel

theorem bound53 : beta 53 + epsilon 53 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert53

end SymmetricSector.GeneratedMargins
