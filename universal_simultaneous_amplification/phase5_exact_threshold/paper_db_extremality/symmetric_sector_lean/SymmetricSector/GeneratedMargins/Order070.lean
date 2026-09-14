import SymmetricSector.GeneratedMargins.Order069

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w70 : List ℕ := [0, 10071, 10217, 10368, 10522, 10682, 10846, 11015, 11190, 11370, 11556, 11748, 11947, 12152, 12364, 12584, 12812, 13048, 13293, 13547, 13811, 14085, 14371, 14668, 14977, 15299, 15635, 15986, 16353, 16737, 17139, 17561, 18003, 18468, 18957, 19471, 20014, 20587, 21193, 21834, 22515, 23238, 24007, 24827, 25703, 26641, 27647, 28728, 29893, 31152, 32516, 33997, 35611, 37376, 39313, 41445, 43803, 46421, 49341, 52614, 56302, 60482, 65248, 70719, 77043, 84410, 93062, 103316, 115585, 130419]

theorem cert70 : MarginCertificate 70 w70 (1 / 100) := by decide +kernel

theorem bound70 : beta 70 + epsilon 70 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert70

end SymmetricSector.GeneratedMargins
