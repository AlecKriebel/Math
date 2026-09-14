import SymmetricSector.GeneratedMargins.Order062

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w63 : List ℕ := [0, 10080, 10242, 10410, 10583, 10763, 10948, 11140, 11338, 11544, 11757, 11978, 12208, 12446, 12694, 12952, 13220, 13500, 13791, 14095, 14413, 14745, 15092, 15456, 15838, 16238, 16659, 17102, 17568, 18060, 18580, 19130, 19713, 20331, 20988, 21687, 22433, 23231, 24085, 25002, 25989, 27053, 28204, 29452, 30810, 32291, 33913, 35696, 37662, 39841, 42265, 44976, 48024, 51469, 55386, 59871, 65041, 71047, 78083, 86400, 96327, 108301, 122911]

theorem cert63 : MarginCertificate 63 w63 (1 / 100) := by decide +kernel

theorem bound63 : beta 63 + epsilon 63 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert63

end SymmetricSector.GeneratedMargins
