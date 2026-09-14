import SymmetricSector.GeneratedMargins.Order077

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w78 : List ℕ := [0, 10064, 10195, 10329, 10467, 10608, 10753, 10902, 11056, 11213, 11376, 11543, 11715, 11892, 12074, 12262, 12456, 12656, 12863, 13076, 13297, 13525, 13761, 14005, 14258, 14520, 14792, 15074, 15367, 15671, 15987, 16316, 16659, 17016, 17389, 17778, 18185, 18610, 19055, 19522, 20011, 20525, 21066, 21635, 22234, 22867, 23536, 24244, 24995, 25792, 26639, 27542, 28506, 29537, 30641, 31827, 33104, 34483, 35974, 37592, 39353, 41275, 43380, 45694, 48246, 51074, 54220, 57736, 61685, 66144, 71208, 76994, 83649, 91358, 100355, 110941, 123507, 138563]

theorem cert78 : MarginCertificate 78 w78 (1 / 100) := by decide +kernel

theorem bound78 : beta 78 + epsilon 78 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert78

end SymmetricSector.GeneratedMargins
