import SymmetricSector.GeneratedMargins.Order070

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w71 : List ℕ := [0, 10070, 10214, 10362, 10515, 10671, 10833, 10999, 11171, 11348, 11531, 11719, 11914, 12116, 12324, 12539, 12762, 12993, 13232, 13481, 13738, 14006, 14284, 14573, 14874, 15187, 15514, 15855, 16211, 16583, 16972, 17379, 17806, 18254, 18725, 19221, 19742, 20292, 20873, 21487, 22137, 22826, 23558, 24337, 25168, 26055, 27004, 28022, 29117, 30296, 31570, 32950, 34449, 36082, 37867, 39825, 41981, 44363, 47008, 49957, 53261, 56983, 61199, 66004, 71516, 77883, 85294, 93992, 104290, 116598, 131461]

theorem cert71 : MarginCertificate 71 w71 (1 / 100) := by decide +kernel

theorem bound71 : beta 71 + epsilon 71 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert71

end SymmetricSector.GeneratedMargins
