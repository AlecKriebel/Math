import SymmetricSector.GeneratedMargins.Order076

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w77 : List ℕ := [0, 10065, 10197, 10333, 10473, 10616, 10764, 10915, 11071, 11231, 11396, 11566, 11741, 11921, 12106, 12298, 12496, 12700, 12911, 13128, 13353, 13586, 13828, 14077, 14336, 14605, 14883, 15172, 15473, 15785, 16111, 16449, 16802, 17170, 17555, 17956, 18376, 18816, 19277, 19761, 20269, 20803, 21365, 21957, 22583, 23244, 23944, 24686, 25473, 26311, 27204, 28157, 29176, 30268, 31442, 32705, 34069, 35544, 37145, 38888, 40791, 42875, 45167, 47696, 50498, 53616, 57102, 61019, 65445, 70473, 76221, 82836, 90504, 99460, 110007, 122538, 137568]

theorem cert77 : MarginCertificate 77 w77 (1 / 100) := by decide +kernel

theorem bound77 : beta 77 + epsilon 77 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert77

end SymmetricSector.GeneratedMargins
