import SymmetricSector.GeneratedMargins.Order073

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w74 : List ℕ := [0, 10068, 10205, 10347, 10493, 10643, 10797, 10955, 11119, 11287, 11460, 11639, 11823, 12013, 12210, 12413, 12622, 12839, 13063, 13295, 13535, 13785, 14043, 14311, 14589, 14879, 15180, 15493, 15819, 16159, 16513, 16883, 17270, 17675, 18098, 18542, 19008, 19498, 20012, 20554, 21125, 21728, 22366, 23041, 23757, 24517, 25326, 26188, 27108, 28092, 29148, 30282, 31503, 32822, 34250, 35801, 37489, 39333, 41355, 43579, 46035, 48759, 51794, 55190, 59011, 63333, 68251, 73883, 80377, 87919, 96748, 107173, 119595, 134544]

theorem cert74 : MarginCertificate 74 w74 (1 / 100) := by decide +kernel

theorem bound74 : beta 74 + epsilon 74 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert74

end SymmetricSector.GeneratedMargins
