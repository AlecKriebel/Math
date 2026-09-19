/-
UNCOMPILED research source. This formalizes the scalar elimination in the
new direct flag argument. Its vector-coordinate premises are explicit:
deriving them from the concrete bracket and discharging them remain separate
obligations. These lemmas are NOT a theorem about the full automorphism group.
-/
import Mathlib.Tactic

namespace Kourovka.FlagScalars

section
variable {k : Type*} [Field k]

/-- Scalar equations extracted from [Qx,Qt]=6Qt force Qx=x.
The nonzero premise is precisely injectivity applied to the flag's third vector.
-/
theorem automorphism_first_stage (six : (6 : k) ≠ 0)
    (a b u v s : k)
    (hu : 6 * u = 0) (hv : 6 * v = 0)
    (hthird : u ≠ 0 ∨ v ≠ 0 ∨ s ≠ 0)
    (ha : 6 * a * s = 6 * s) (hb : 6 * b * s = 0) :
    u = 0 ∧ v = 0 ∧ s ≠ 0 ∧ a = 1 ∧ b = 0 := by
  have hu0 : u = 0 := (mul_eq_zero.mp hu).resolve_left six
  have hv0 : v = 0 := (mul_eq_zero.mp hv).resolve_left six
  have hs : s ≠ 0 := by simpa [hu0, hv0] using hthird
  have h6s : (6 : k) * s ≠ 0 := mul_ne_zero six hs
  have ha0 : (a - 1) * (6 * s) = 0 := by
    calc
      (a - 1) * (6 * s) = 6 * a * s - 6 * s := by ring
      _ = 0 := sub_eq_zero.mpr ha
  have ha1 : a = 1 := sub_eq_zero.mp ((mul_eq_zero.mp ha0).resolve_right h6s)
  have hb0 : b * (6 * s) = 0 := by
    calc
      b * (6 * s) = 6 * b * s := by ring
      _ = 0 := hb
  exact ⟨hu0, hv0, hs, ha1, (mul_eq_zero.mp hb0).resolve_right h6s⟩

/-- Scalar equations extracted using the Leibniz rule force Dx=0. -/
theorem derivation_first_stage (six : (6 : k) ≠ 0)
    (a b u v s : k)
    (hu : 6 * u = 0) (hv : 6 * v = 0)
    (ha : 6 * a + 6 * s = 6 * s) (hb : 6 * b = 0) :
    u = 0 ∧ v = 0 ∧ a = 0 ∧ b = 0 := by
  have ha0 : (6 : k) * a = 0 := by
    have hh : 6 * a + 6 * s = 0 + 6 * s := by simpa using ha
    exact add_right_cancel hh
  exact ⟨(mul_eq_zero.mp hu).resolve_left six,
    (mul_eq_zero.mp hv).resolve_left six,
    (mul_eq_zero.mp ha0).resolve_left six,
    (mul_eq_zero.mp hb).resolve_left six⟩

/-- The two independent T_0 reconstructions exclude the residual sign. -/
theorem exclude_residual_sign (q d : k) (hq : q ≠ 0)
    (h : q * d = q) : d = 1 := by
  have hz : q * (d - 1) = 0 := by
    calc
      q * (d - 1) = q * d - q := by ring
      _ = 0 := sub_eq_zero.mpr h
  exact sub_eq_zero.mp ((mul_eq_zero.mp hz).resolve_left hq)

end
end Kourovka.FlagScalars
