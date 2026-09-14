import SymmetricSector.GeneratedMargins.Order068

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w69 : List ℕ := [0, 10072, 10221, 10373, 10530, 10692, 10859, 11031, 11209, 11392, 11582, 11778, 11980, 12190, 12407, 12631, 12864, 13105, 13356, 13616, 13887, 14168, 14461, 14766, 15084, 15416, 15762, 16124, 16503, 16899, 17315, 17751, 18210, 18692, 19200, 19735, 20301, 20899, 21532, 22204, 22917, 23677, 24487, 25352, 26278, 27271, 28339, 29490, 30733, 32080, 33544, 35140, 36885, 38800, 40909, 43242, 45833, 48724, 51965, 55619, 59763, 64490, 69919, 76199, 83520, 92127, 102336, 114565, 129369]

theorem cert69 : MarginCertificate 69 w69 (1 / 100) := by decide +kernel

theorem bound69 : beta 69 + epsilon 69 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert69

end SymmetricSector.GeneratedMargins
