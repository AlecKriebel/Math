import SymmetricSector.GeneratedMargins.Order057

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w58 : List ℕ := [0, 10086, 10263, 10447, 10636, 10833, 11037, 11249, 11469, 11698, 11936, 12184, 12442, 12711, 12992, 13286, 13592, 13913, 14250, 14603, 14973, 15362, 15772, 16204, 16659, 17140, 17650, 18189, 18762, 19371, 20020, 20712, 21453, 22246, 23099, 24016, 25007, 26079, 27242, 28509, 29892, 31409, 33077, 34921, 36966, 39246, 41801, 44678, 47939, 51657, 55927, 60866, 66627, 73406, 81459, 91127, 102866, 117296]

theorem cert58 : MarginCertificate 58 w58 (1 / 100) := by decide +kernel

theorem bound58 : beta 58 + epsilon 58 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert58

end SymmetricSector.GeneratedMargins
