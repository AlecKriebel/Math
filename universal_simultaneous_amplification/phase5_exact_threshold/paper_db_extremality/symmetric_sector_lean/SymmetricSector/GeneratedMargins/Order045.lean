import SymmetricSector.GeneratedMargins.Order044

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w45 : List ℕ := [0, 10112, 10342, 10582, 10834, 11098, 11374, 11665, 11971, 12293, 12632, 12991, 13370, 13771, 14197, 14650, 15131, 15645, 16193, 16781, 17411, 18090, 18821, 19612, 20470, 21404, 22423, 23539, 24766, 26122, 27625, 29300, 31177, 33292, 35689, 38425, 41571, 45218, 49482, 54516, 60522, 67773, 76639, 87634, 101483]

theorem cert45 : MarginCertificate 45 w45 (1 / 100) := by decide +kernel

theorem bound45 : beta 45 + epsilon 45 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert45

end SymmetricSector.GeneratedMargins
