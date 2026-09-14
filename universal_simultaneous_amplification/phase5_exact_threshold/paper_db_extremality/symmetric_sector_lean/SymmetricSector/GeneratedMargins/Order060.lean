import SymmetricSector.GeneratedMargins.Order059

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w60 : List ℕ := [0, 10084, 10254, 10431, 10614, 10803, 11000, 11203, 11414, 11633, 11860, 12097, 12343, 12599, 12865, 13143, 13434, 13737, 14054, 14385, 14733, 15097, 15479, 15881, 16304, 16750, 17220, 17717, 18243, 18800, 19391, 20019, 20688, 21402, 22165, 22983, 23861, 24807, 25827, 26931, 28128, 29431, 30854, 32413, 34128, 36021, 38120, 40459, 43077, 46023, 49358, 53157, 57514, 62548, 68409, 75293, 83454, 93228, 105064, 119569]

theorem cert60 : MarginCertificate 60 w60 (1 / 100) := by decide +kernel

theorem bound60 : beta 60 + epsilon 60 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert60

end SymmetricSector.GeneratedMargins
