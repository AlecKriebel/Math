import SymmetricSector.GeneratedMargins.Order074

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w75 : List ℕ := [0, 10067, 10203, 10342, 10486, 10634, 10785, 10942, 11102, 11268, 11438, 11614, 11795, 11982, 12174, 12373, 12579, 12791, 13010, 13238, 13473, 13716, 13969, 14230, 14502, 14784, 15077, 15382, 15699, 16029, 16373, 16732, 17107, 17499, 17909, 18338, 18787, 19259, 19755, 20276, 20825, 21403, 22014, 22659, 23342, 24067, 24836, 25654, 26526, 27457, 28453, 29521, 30669, 31905, 33239, 34683, 36250, 37956, 39820, 41863, 44110, 46591, 49341, 52403, 55830, 59683, 64040, 68995, 74666, 81201, 88785, 97657, 108123, 120582, 135559]

theorem cert75 : MarginCertificate 75 w75 (1 / 100) := by decide +kernel

theorem bound75 : beta 75 + epsilon 75 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert75

end SymmetricSector.GeneratedMargins
