import SymmetricSector.GeneratedMargins.Order078

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w79 : List ℕ := [0, 10063, 10192, 10325, 10460, 10600, 10743, 10890, 11041, 11196, 11356, 11520, 11689, 11863, 12043, 12227, 12418, 12614, 12817, 13026, 13242, 13465, 13696, 13935, 14182, 14438, 14704, 14979, 15264, 15561, 15869, 16189, 16522, 16869, 17231, 17608, 18002, 18413, 18844, 19294, 19766, 20261, 20781, 21328, 21904, 22511, 23151, 23828, 24544, 25303, 26109, 26966, 27879, 28854, 29896, 31013, 32212, 33503, 34896, 36403, 38038, 39817, 41758, 43884, 46220, 48796, 51649, 54822, 58367, 62347, 66840, 71940, 77764, 84458, 92207, 101244, 111869, 124469, 139551]

theorem cert79 : MarginCertificate 79 w79 (1 / 100) := by decide +kernel

theorem bound79 : beta 79 + epsilon 79 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert79

end SymmetricSector.GeneratedMargins
