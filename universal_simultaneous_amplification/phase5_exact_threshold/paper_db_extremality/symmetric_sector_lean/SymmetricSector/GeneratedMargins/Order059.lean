import SymmetricSector.GeneratedMargins.Order058

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w59 : List ℕ := [0, 10085, 10259, 10439, 10625, 10818, 11018, 11226, 11441, 11665, 11898, 12140, 12391, 12654, 12927, 13213, 13511, 13823, 14149, 14491, 14850, 15226, 15622, 16038, 16477, 16940, 17429, 17946, 18494, 19076, 19695, 20354, 21057, 21809, 22615, 23480, 24412, 25417, 26505, 27685, 28970, 30374, 31912, 33604, 35472, 37544, 39853, 42439, 45351, 48649, 52408, 56722, 61709, 67521, 74353, 82461, 92183, 103971, 118439]

theorem cert59 : MarginCertificate 59 w59 (1 / 100) := by decide +kernel

theorem bound59 : beta 59 + epsilon 59 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert59

end SymmetricSector.GeneratedMargins
