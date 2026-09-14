import SymmetricSector.GeneratedMargins.Order046

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w47 : List ℕ := [0, 10107, 10327, 10556, 10796, 11047, 11309, 11584, 11873, 12176, 12495, 12830, 13184, 13558, 13953, 14371, 14814, 15286, 15787, 16322, 16893, 17504, 18160, 18866, 19627, 20449, 21341, 22311, 23369, 24528, 25801, 27206, 28764, 30499, 32441, 34627, 37102, 39924, 43164, 46913, 51289, 56444, 62580, 69967, 78971, 90096, 104048]

theorem cert47 : MarginCertificate 47 w47 (1 / 100) := by decide +kernel

theorem bound47 : beta 47 + epsilon 47 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert47

end SymmetricSector.GeneratedMargins
