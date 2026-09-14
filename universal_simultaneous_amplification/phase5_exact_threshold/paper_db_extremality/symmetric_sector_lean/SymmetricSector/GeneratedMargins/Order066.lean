import SymmetricSector.GeneratedMargins.Order065

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w66 : List ℕ := [0, 10076, 10231, 10391, 10556, 10726, 10901, 11083, 11270, 11464, 11665, 11873, 12088, 12311, 12542, 12782, 13032, 13291, 13560, 13841, 14133, 14438, 14756, 15088, 15435, 15798, 16178, 16577, 16995, 17435, 17898, 18385, 18899, 19442, 20016, 20624, 21269, 21954, 22684, 23462, 24293, 25183, 26138, 27166, 28274, 29471, 30769, 32180, 33719, 35403, 37253, 39291, 41548, 44056, 46858, 50004, 53555, 57587, 62195, 67497, 73643, 80825, 89290, 99362, 111467, 126177]

theorem cert66 : MarginCertificate 66 w66 (1 / 100) := by decide +kernel

theorem bound66 : beta 66 + epsilon 66 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert66

end SymmetricSector.GeneratedMargins
