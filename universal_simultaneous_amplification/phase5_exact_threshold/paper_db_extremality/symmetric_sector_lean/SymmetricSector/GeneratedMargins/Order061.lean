import SymmetricSector.GeneratedMargins.Order060

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w61 : List ℕ := [0, 10082, 10250, 10424, 10604, 10789, 10982, 11181, 11388, 11602, 11825, 12056, 12296, 12546, 12806, 13077, 13359, 13654, 13962, 14284, 14621, 14974, 15344, 15733, 16141, 16570, 17023, 17501, 18005, 18539, 19104, 19704, 20342, 21021, 21746, 22521, 23351, 24242, 25201, 26236, 27356, 28570, 29892, 31334, 32914, 34652, 36570, 38696, 41063, 43712, 46692, 50064, 53903, 58303, 63383, 69293, 76229, 84443, 94269, 106152, 120693]

theorem cert61 : MarginCertificate 61 w61 (1 / 100) := by decide +kernel

theorem bound61 : beta 61 + epsilon 61 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert61

end SymmetricSector.GeneratedMargins
