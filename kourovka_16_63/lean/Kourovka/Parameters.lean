/-
UNCOMPILED research source. No group law or automorphism count is proved here.
The concrete carrier is additive coordinates only; it is not called G.
-/
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.NormNum.Prime

namespace Kourovka

def prime : Nat := 1009
def depth : Nat := 1689
def dimension : Nat := 31

theorem prime_is_prime : Nat.Prime 1009 := by norm_num

theorem coordinate_exponent : 31 * 1689 = 52359 := by norm_num

theorem automorphism_exponent : 30 * 1689 + 1689 = 52359 := by norm_num

theorem class_in_lazard_range : (846 : Nat) < 1009 := by norm_num

/-- The intended additive carrier, without a declared BCH multiplication. -/
def Coordinates (i : Nat) := Fin 31 → ZMod (1009 ^ i)

end Kourovka
