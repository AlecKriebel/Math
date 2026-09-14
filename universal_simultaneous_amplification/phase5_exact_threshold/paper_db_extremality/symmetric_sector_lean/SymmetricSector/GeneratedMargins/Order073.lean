import SymmetricSector.GeneratedMargins.Order072

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w73 : List ℕ := [0, 10068, 10208, 10352, 10500, 10652, 10809, 10970, 11136, 11307, 11483, 11665, 11853, 12046, 12246, 12453, 12667, 12888, 13117, 13355, 13601, 13856, 14120, 14395, 14681, 14978, 15287, 15608, 15944, 16294, 16659, 17041, 17440, 17859, 18297, 18757, 19240, 19748, 20284, 20848, 21444, 22073, 22740, 23447, 24198, 24997, 25848, 26757, 27730, 28773, 29894, 31102, 32406, 33818, 35351, 37021, 38846, 40846, 43047, 45479, 48177, 51183, 54549, 58337, 62624, 67505, 73097, 79549, 87048, 95834, 106217, 118602, 133523]

theorem cert73 : MarginCertificate 73 w73 (1 / 100) := by decide +kernel

theorem bound73 : beta 73 + epsilon 73 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert73

end SymmetricSector.GeneratedMargins
