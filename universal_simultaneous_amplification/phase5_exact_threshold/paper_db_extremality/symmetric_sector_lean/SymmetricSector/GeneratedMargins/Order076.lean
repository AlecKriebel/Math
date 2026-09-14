import SymmetricSector.GeneratedMargins.Order075

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w76 : List ℕ := [0, 10066, 10200, 10338, 10479, 10625, 10774, 10928, 11086, 11249, 11417, 11589, 11767, 11951, 12140, 12335, 12536, 12745, 12960, 13182, 13412, 13650, 13897, 14152, 14417, 14692, 14978, 15275, 15584, 15905, 16239, 16588, 16951, 17331, 17728, 18143, 18577, 19032, 19510, 20012, 20539, 21095, 21680, 22298, 22951, 23643, 24376, 25155, 25983, 26865, 27807, 28815, 29895, 31055, 32305, 33654, 35114, 36698, 38423, 40306, 42370, 44639, 47144, 49920, 53010, 56467, 60352, 64743, 69735, 75445, 82020, 89646, 98560, 109067, 121562, 136566]

theorem cert76 : MarginCertificate 76 w76 (1 / 100) := by decide +kernel

theorem bound76 : beta 76 + epsilon 76 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert76

end SymmetricSector.GeneratedMargins
