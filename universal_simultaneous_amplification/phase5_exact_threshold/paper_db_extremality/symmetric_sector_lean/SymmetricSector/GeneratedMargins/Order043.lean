import SymmetricSector.GeneratedMargins.Order042

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w43 : List ℕ := [0, 10117, 10358, 10611, 10876, 11154, 11447, 11755, 12080, 12423, 12786, 13171, 13579, 14012, 14474, 14966, 15492, 16056, 16661, 17311, 18013, 18773, 19597, 20494, 21473, 22546, 23727, 25032, 26480, 28095, 29906, 31948, 34266, 36915, 39965, 43506, 47654, 52562, 58433, 65541, 74263, 85122, 98863]

theorem cert43 : MarginCertificate 43 w43 (1 / 100) := by decide +kernel

theorem bound43 : beta 43 + epsilon 43 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert43

end SymmetricSector.GeneratedMargins
