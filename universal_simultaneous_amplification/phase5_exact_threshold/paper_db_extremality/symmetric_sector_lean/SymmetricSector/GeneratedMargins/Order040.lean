import SymmetricSector.Margins

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w40 : List ℕ := [0, 10126, 10386, 10659, 10947, 11250, 11570, 11909, 12268, 12649, 13054, 13486, 13946, 14438, 14965, 15530, 16139, 16797, 17508, 18281, 19122, 20041, 21049, 22159, 23386, 24750, 26273, 27982, 29913, 32109, 34623, 37524, 40900, 44868, 49579, 55237, 62120, 70612, 81253, 94819]

theorem cert40 : MarginCertificate 40 w40 (1 / 200) := by decide +kernel

theorem bound40 : beta 40 + epsilon 40 ≤ 1 - (1 / 200 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert40

end SymmetricSector.GeneratedMargins
