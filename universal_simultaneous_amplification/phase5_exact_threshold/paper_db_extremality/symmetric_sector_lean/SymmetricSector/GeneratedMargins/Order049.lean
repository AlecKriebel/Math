import SymmetricSector.GeneratedMargins.Order048

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w49 : List ℕ := [0, 10103, 10313, 10532, 10761, 11000, 11250, 11510, 11784, 12070, 12370, 12686, 13017, 13367, 13735, 14123, 14534, 14969, 15430, 15920, 16442, 16997, 17591, 18226, 18908, 19640, 20430, 21284, 22209, 23215, 24312, 25512, 26831, 28286, 29897, 31690, 33695, 35951, 38503, 41408, 44739, 48588, 53073, 58346, 64608, 72127, 81263, 92511, 106560]

theorem cert49 : MarginCertificate 49 w49 (1 / 100) := by decide +kernel

theorem bound49 : beta 49 + epsilon 49 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert49

end SymmetricSector.GeneratedMargins
