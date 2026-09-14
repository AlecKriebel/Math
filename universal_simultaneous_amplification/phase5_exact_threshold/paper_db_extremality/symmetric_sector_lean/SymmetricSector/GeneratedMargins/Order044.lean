import SymmetricSector.GeneratedMargins.Order043

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w44 : List ℕ := [0, 10114, 10350, 10596, 10854, 11125, 11410, 11709, 12024, 12356, 12707, 13078, 13471, 13888, 14331, 14803, 15306, 15843, 16419, 17036, 17701, 18418, 19193, 20034, 20949, 21948, 23043, 24247, 25577, 27053, 28698, 30542, 32621, 34979, 37672, 40770, 44364, 48570, 53541, 59480, 66660, 75455, 86383, 100179]

theorem cert44 : MarginCertificate 44 w44 (1 / 100) := by decide +kernel

theorem bound44 : beta 44 + epsilon 44 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert44

end SymmetricSector.GeneratedMargins
