import SymmetricSector.GeneratedMargins.Order066

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w67 : List ℕ := [0, 10075, 10227, 10385, 10547, 10714, 10887, 11065, 11249, 11439, 11636, 11840, 12051, 12269, 12495, 12730, 12974, 13227, 13490, 13763, 14048, 14344, 14653, 14976, 15313, 15665, 16033, 16419, 16823, 17248, 17694, 18163, 18657, 19178, 19728, 20310, 20927, 21581, 22276, 23015, 23804, 24646, 25548, 26516, 27557, 28679, 29892, 31207, 32636, 34194, 35898, 37769, 39831, 42113, 44649, 47481, 50659, 54245, 58315, 62963, 68308, 74499, 81728, 90241, 100359, 112506, 127248]

theorem cert67 : MarginCertificate 67 w67 (1 / 100) := by decide +kernel

theorem bound67 : beta 67 + epsilon 67 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert67

end SymmetricSector.GeneratedMargins
