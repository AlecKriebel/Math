import SymmetricSector.GeneratedMargins.Order053

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w54 : List ℕ := [0, 10093, 10283, 10481, 10686, 10900, 11122, 11353, 11594, 11845, 12108, 12382, 12668, 12968, 13282, 13612, 13958, 14322, 14705, 15108, 15534, 15984, 16461, 16966, 17502, 18072, 18680, 19329, 20023, 20767, 21567, 22428, 23358, 24366, 25460, 26652, 27955, 29385, 30960, 32702, 34637, 36798, 39223, 41959, 45066, 48617, 52705, 57449, 63001, 69560, 77386, 86829, 98362, 112633]

theorem cert54 : MarginCertificate 54 w54 (1 / 100) := by decide +kernel

theorem bound54 : beta 54 + epsilon 54 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert54

end SymmetricSector.GeneratedMargins
