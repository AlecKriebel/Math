import SymmetricSector.GeneratedMargins.Order056

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w57 : List ℕ := [0, 10088, 10268, 10455, 10648, 10849, 11057, 11274, 11499, 11733, 11976, 12230, 12495, 12771, 13060, 13362, 13677, 14008, 14355, 14719, 15102, 15505, 15930, 16378, 16852, 17353, 17884, 18448, 19047, 19686, 20367, 21096, 21877, 22716, 23620, 24595, 25651, 26797, 28045, 29409, 30904, 32550, 34368, 36386, 38637, 41159, 44002, 47225, 50902, 55127, 60019, 65729, 72454, 80452, 90065, 101754, 116146]

theorem cert57 : MarginCertificate 57 w57 (1 / 100) := by decide +kernel

theorem bound57 : beta 57 + epsilon 57 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert57

end SymmetricSector.GeneratedMargins
