import SymmetricSector.GeneratedMargins.Order047

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w48 : List ℕ := [0, 10105, 10320, 10544, 10778, 11023, 11279, 11546, 11827, 12122, 12431, 12756, 13099, 13460, 13841, 14244, 14670, 15123, 15603, 16114, 16660, 17242, 17865, 18534, 19253, 20029, 20867, 21775, 22763, 23841, 25021, 26317, 27747, 29331, 31095, 33069, 35290, 37804, 40668, 43954, 47753, 52184, 57398, 63598, 71052, 80123, 91310, 105311]

theorem cert48 : MarginCertificate 48 w48 (1 / 100) := by decide +kernel

theorem bound48 : beta 48 + epsilon 48 ≤ 1 - (1 / 100 : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert48

end SymmetricSector.GeneratedMargins
