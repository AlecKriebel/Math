import SymmetricSector.GeneratedMargins.Order049

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w50 : List ℕ := [0, 10101, 10307, 10521, 10745, 10978, 11222, 11476, 11742, 12021, 12313, 12619, 12941, 13279, 13635, 14010, 14406, 14825, 15268, 15738, 16237, 16768, 17334, 17939, 18586, 19280, 20027, 20831, 21700, 22642, 23665, 24781, 26003, 27344, 28823, 30461, 32283, 34320, 36610, 39199, 42146, 45522, 49420, 53958, 59289, 65613, 73196, 82396, 93704, 107799]

theorem cert50 : MarginCertificate 50 w50 (1 / 100) := by decide +kernel

theorem bound50 : beta 50 + epsilon 50 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert50

end SymmetricSector.GeneratedMargins
