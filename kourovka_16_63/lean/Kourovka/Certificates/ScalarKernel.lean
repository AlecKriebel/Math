/- Uncompiled source. Exact scalar kernels over composite residue rings.
No cancellation or field inverse is used inside ZMod(c*q). -/
import Mathlib.Data.ZMod.Basic
import Mathlib.SetTheory.Cardinal.Finite
import Mathlib.Tactic

namespace Kourovka.Certificates.ScalarKernel

private theorem cancel_nat_dvd (c q a : Nat) (hc : 0 < c) :
    c*q ∣ c*a ↔ q ∣ a := by
  constructor
  · rintro ⟨t, ht⟩
    refine ⟨t, ?_⟩
    exact mul_left_cancel₀ (ne_of_gt hc) (by simpa only [mul_assoc] using ht)
  · rintro ⟨t, rfl⟩
    exact ⟨t, by simp only [mul_assoc]⟩

/-- The full scalar kernel, not a hand-selected set of annihilated elements. -/
def Carrier (c q : Nat) := {x : ZMod (c*q) // (c : ZMod (c*q))*x = 0}

section
variable (c q : Nat) (hc : 0 < c) (hq : 0 < q)
include hc hq

private theorem kernel_divisible (x : Carrier c q) : q ∣ x.val.val := by
  letI : NeZero (c*q) := ⟨ne_of_gt (Nat.mul_pos hc hq)⟩
  apply (cancel_nat_dvd c q x.val.val hc).mp
  apply (CharP.cast_eq_zero_iff (ZMod (c*q)) (c*q) (c*x.val.val)).mp
  simpa only [Nat.cast_mul,ZMod.natCast_zmod_val] using x.property

private theorem multiple_bound (t : Fin c) : q*t.val < c*q := by
  have h := Nat.mul_lt_mul_of_pos_left t.isLt hq
  simpa only [Nat.mul_comm q c] using h

/-- Explicit representatives are q*t, with 0 <= t < c. -/
def equivFin : Carrier c q ≃ Fin c := by
  letI : NeZero (c*q) := ⟨ne_of_gt (Nat.mul_pos hc hq)⟩
  exact {
    toFun x := ⟨x.val.val/q, by
      apply (Nat.div_lt_iff_lt_mul hq).mpr
      exact ZMod.val_lt x.val⟩
    invFun t := ⟨(q*t.val : Nat), by
      have hzero : ((c*q : Nat) : ZMod (c*q)) = 0 := ZMod.natCast_self _
      calc
        (c : ZMod (c*q)) * (q*t.val : Nat) =
          ((c*q : Nat) : ZMod (c*q)) * t.val := by push_cast; ring
        _ = 0 := by rw [hzero,zero_mul]⟩
    left_inv := by
      intro x
      apply Subtype.ext
      change ((q*(x.val.val/q) : Nat) : ZMod (c*q)) = x.val
      rw [Nat.mul_div_cancel' (kernel_divisible c q hc hq x)]
      exact ZMod.natCast_zmod_val x.val
    right_inv := by
      intro t
      apply Fin.ext
      change (((q*t.val : Nat) : ZMod (c*q)).val/q) = t.val
      rw [ZMod.val_natCast_of_lt (multiple_bound c q hc hq t)]
      exact Nat.mul_div_right t.val hq }

/-- This cardinality includes the c=1 and q=1 boundary cases. -/
theorem card : Nat.card (Carrier c q) = c := by
  rw [Nat.card_congr (equivFin c q hc hq)]
  simp

end

/-- The scalar prime-power count, including valuation zero and valuation equal to the modulus depth. -/
theorem prime_power_card (p i v : Nat) (hp : 0 < p) (hv : v ≤ i) :
    Nat.card {x : ZMod (p^i) // (p^v : Nat) * x = 0} = p^v := by
  have he : p^v * p^(i-v) = p^i := by rw [← pow_add,Nat.add_sub_of_le hv]
  have h := card (p^v) (p^(i-v)) (pow_pos hp _) (pow_pos hp _)
  unfold Carrier at h
  rw [he] at h
  exact h

/-- A zero diagonal position contributes the entire coefficient ring. -/
def zeroKernelEquiv (R : Type*) [Semiring R] : {x : R // (0:R)*x=0} ≃ R where
  toFun x := x.val
  invFun x := ⟨x,zero_mul x⟩
  left_inv := by intro x; rfl
  right_inv := by intro x; rfl

end Kourovka.Certificates.ScalarKernel
