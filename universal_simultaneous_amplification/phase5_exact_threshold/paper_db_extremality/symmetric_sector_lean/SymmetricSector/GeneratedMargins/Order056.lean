import SymmetricSector.GeneratedMargins.Order055

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w56 : List ℕ := [0, 10090, 10273, 10463, 10661, 10865, 11078, 11299, 11529, 11769, 12018, 12279, 12550, 12834, 13131, 13441, 13766, 14107, 14466, 14842, 15239, 15656, 16097, 16563, 17056, 17578, 18133, 18723, 19351, 20022, 20739, 21508, 22334, 23223, 24184, 25224, 26353, 27582, 28926, 30399, 32021, 33814, 35805, 38026, 40516, 43323, 46508, 50144, 54324, 59167, 64825, 71495, 79437, 88995, 100633, 114985]

theorem cert56 : MarginCertificate 56 w56 (1 / 100) := by decide +kernel

theorem bound56 : beta 56 + epsilon 56 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert56

end SymmetricSector.GeneratedMargins
