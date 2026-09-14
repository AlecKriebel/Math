import SymmetricSector.GeneratedMargins.Order061

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w62 : List ℕ := [0, 10081, 10246, 10417, 10593, 10776, 10965, 11160, 11363, 11573, 11790, 12016, 12251, 12495, 12749, 13013, 13288, 13575, 13875, 14188, 14515, 14857, 15215, 15591, 15985, 16400, 16836, 17296, 17781, 18293, 18835, 19409, 20018, 20665, 21354, 22090, 22876, 23718, 24622, 25595, 26645, 27780, 29011, 30351, 31813, 33414, 35174, 37116, 39269, 41665, 44345, 47359, 50768, 54646, 59089, 64214, 70173, 77159, 85425, 95302, 107231, 121807]

theorem cert62 : MarginCertificate 62 w62 (1 / 100) := by decide +kernel

theorem bound62 : beta 62 + epsilon 62 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert62

end SymmetricSector.GeneratedMargins
