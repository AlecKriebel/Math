import SymmetricSector.GeneratedMargins.Order067

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w68 : List ℕ := [0, 10074, 10224, 10379, 10538, 10703, 10873, 11048, 11229, 11416, 11609, 11808, 12015, 12229, 12450, 12680, 12918, 13165, 13422, 13688, 13966, 14254, 14555, 14869, 15196, 15537, 15894, 16268, 16659, 17069, 17500, 17952, 18428, 18929, 19457, 20015, 20605, 21230, 21892, 22596, 23346, 24145, 24999, 25913, 26894, 27948, 29085, 30313, 31644, 33090, 34667, 36392, 38285, 40371, 42678, 45242, 48103, 51313, 54933, 59040, 63728, 69115, 75351, 82626, 91186, 101350, 113539, 128312]

theorem cert68 : MarginCertificate 68 w68 (1 / 100) := by decide +kernel

theorem bound68 : beta 68 + epsilon 68 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert68

end SymmetricSector.GeneratedMargins
