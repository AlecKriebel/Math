import SymmetricSector.GeneratedMargins.Order045

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w46 : List ℕ := [0, 10109, 10334, 10569, 10814, 11071, 11341, 11624, 11921, 12233, 12562, 12908, 13274, 13661, 14071, 14506, 14968, 15459, 15983, 16543, 17143, 17786, 18478, 19224, 20031, 20906, 21858, 22897, 24034, 25284, 26665, 28195, 29900, 31810, 33960, 36397, 39176, 42369, 46067, 50387, 55482, 61554, 68874, 77810, 88871, 102772]

theorem cert46 : MarginCertificate 46 w46 (1 / 100) := by decide +kernel

theorem bound46 : beta 46 + epsilon 46 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert46

end SymmetricSector.GeneratedMargins
