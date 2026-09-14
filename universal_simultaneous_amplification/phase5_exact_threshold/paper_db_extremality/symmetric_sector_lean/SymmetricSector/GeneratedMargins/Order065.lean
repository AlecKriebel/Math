import SymmetricSector.GeneratedMargins.Order064

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w65 : List ℕ := [0, 10077, 10234, 10397, 10565, 10738, 10916, 11101, 11292, 11490, 11695, 11907, 12126, 12354, 12591, 12837, 13092, 13358, 13634, 13922, 14222, 14536, 14863, 15205, 15563, 15938, 16331, 16743, 17177, 17633, 18113, 18620, 19155, 19721, 20320, 20956, 21632, 22352, 23119, 23939, 24818, 25760, 26774, 27867, 29049, 30331, 31724, 33244, 34908, 36735, 38750, 40981, 43461, 46233, 49346, 52862, 56856, 61423, 66682, 72782, 79916, 88332, 98356, 110418, 125095]

theorem cert65 : MarginCertificate 65 w65 (1 / 100) := by decide +kernel

theorem bound65 : beta 65 + epsilon 65 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert65

end SymmetricSector.GeneratedMargins
