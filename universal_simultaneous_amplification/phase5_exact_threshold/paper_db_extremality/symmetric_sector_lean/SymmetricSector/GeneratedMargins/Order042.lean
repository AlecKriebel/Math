import SymmetricSector.GeneratedMargins.Order041

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w42 : List ℕ := [0, 10120, 10367, 10626, 10898, 11184, 11486, 11804, 12139, 12494, 12870, 13269, 13693, 14145, 14626, 15141, 15692, 16284, 16921, 17608, 18352, 19159, 20037, 20996, 22048, 23205, 24484, 25904, 27489, 29267, 31273, 33550, 36154, 39155, 42642, 46731, 51574, 57375, 64410, 73057, 83845, 97530]

theorem cert42 : MarginCertificate 42 w42 (1 / 100) := by decide +kernel

theorem bound42 : beta 42 + epsilon 42 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert42

end SymmetricSector.GeneratedMargins
