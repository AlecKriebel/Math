import SymmetricSector.GeneratedMargins.Order054

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w55 : List ℕ := [0, 10091, 10278, 10472, 10673, 10882, 11100, 11326, 11561, 11806, 12062, 12329, 12608, 12899, 13205, 13524, 13860, 14212, 14582, 14972, 15382, 15816, 16274, 16758, 17272, 17817, 18397, 19015, 19675, 20381, 21138, 21951, 22826, 23771, 24795, 25907, 27118, 28441, 29893, 31492, 33259, 35222, 37413, 39870, 42642, 45788, 49382, 53517, 58311, 63916, 70531, 78416, 87917, 99503, 113815]

theorem cert55 : MarginCertificate 55 w55 (1 / 100) := by decide +kernel

theorem bound55 : beta 55 + epsilon 55 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert55

end SymmetricSector.GeneratedMargins
