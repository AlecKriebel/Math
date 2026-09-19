/- Uncompiled source. How unequal lattice weights force flag preservation after reduction.
All scalar cancellation occurs in a domain before applying the residue homomorphism. -/
import Kourovka.Linear.EndomorphismCoordinates
import Kourovka.Lattice.AdaptedBasis

namespace Kourovka.Lattice.Weighted
open Kourovka.Linear
open scoped BigOperators

variable {R k : Type*} [CommRing R] [IsDomain R] [CommRing k]
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def member (p:R) (w:ι→Nat) (a:ι→R) : Prop := ∀ j,p^(w j) ∣ a j

theorem scaled_unit_mem (p:R) (w:ι→Nat) (j:ι) : member p w (p^(w j) • unitVec j) := by
  intro i
  by_cases h:i=j
  · subst i
    simp [unitVec]
  · simp [unitVec,h,Ne.symm h]

/-- The coefficient constraints implied by preserving the weighted lattice. -/
theorem entries_divisible (p:R) (w:ι→Nat) (Q:(ι→R)→ₗ[R](ι→R))
    (hQ:∀ a,member p w a → member p w (Q a)) (i j:ι) :
    p^(w i) ∣ p^(w j)*Q (unitVec j) i := by
  have h := hQ _ (scaled_unit_mem p w j) i
  simpa only [map_smul,Pi.smul_apply,smul_eq_mul] using h

private theorem cancel_lower_power (p:R) (hp:p≠0) (a b:Nat) (hab:a<b) (x:R)
    (h:p^b ∣ p^a*x) : p ∣ x := by
  obtain ⟨z,hz⟩ := h
  have he : b=a+(b-a-1)+1 := by omega
  have hpow : p^b=p^a*(p*p^(b-a-1)) := by
    nth_rw 1 [he]
    rw [pow_add,pow_add,pow_one]
    ring
  refine ⟨p^(b-a-1)*z,?_⟩
  apply mul_left_cancel₀ (pow_ne_zero _ hp)
  rw [hz,hpow]
  ring

/-- Strict weight drops vanish after residue reduction; no Field structure on R is used. -/
theorem reduced_entry_zero (p:R) (hp:p≠0) (w:ι→Nat) (f:R→+*k) (hf:f p=0)
    (Q:(ι→R)→ₗ[R](ι→R)) (hQ:∀ a,member p w a → member p w (Q a))
    (i j:ι) (hij:w j<w i) : f (Q (unitVec j) i)=0 := by
  obtain ⟨z,hz⟩ := cancel_lower_power p hp (w j) (w i) hij (Q (unitVec j) i)
    (entries_divisible p w Q hQ i j)
  rw [hz,map_mul,hf,zero_mul]

/-- The full reduction of an endomorphism through its entry matrix. -/
def reduction (f:R→+*k) (Q:(ι→R)→ₗ[R](ι→R)) : (ι→k)→ₗ[k](ι→k) :=
  fromEntries (fun ij => f (Q (unitVec ij.2) ij.1))

/-- Low-weight coordinate submodules, with no implicit basis changes. -/
def level (w:ι→Nat) (b:Nat) : Submodule k (ι→k) where
  carrier := {v | ∀ i,b≤w i → v i=0}
  zero_mem' := by intro i hi; rfl
  add_mem' := by intro u v hu hv i hi; simp [hu i hi,hv i hi]
  smul_mem' := by intro c v hv i hi; simp [hv i hi]

/-- Preservation of each coordinate flag follows for every map preserving the lattice. -/
theorem reduction_preserves_level (p:R) (hp:p≠0) (w:ι→Nat) (f:R→+*k) (hf:f p=0)
    (Q:(ι→R)→ₗ[R](ι→R)) (hQ:∀ a,member p w a → member p w (Q a))
    (b:Nat) (v:ι→k) (hv:v∈level w b) : reduction f Q v∈level w b := by
  intro i hi
  rw [reduction,fromEntries_apply]
  apply Finset.sum_eq_zero
  intro j hj
  by_cases hw:b≤w j
  · rw [hv j hw,mul_zero]
  · have hw' : w j<w i := lt_of_lt_of_le (lt_of_not_ge hw) hi
    rw [reduced_entry_zero p hp w f hf Q hQ i j hw',zero_mul]

/-- These are exactly the dimensions selected by the paper's weights; the P basis change is explicit elsewhere. -/
theorem weight_below_one (j:Kourovka.Ambient.I) : weight j<1 ↔ j.val<2 := by
  fin_cases j <;> decide

theorem weight_below_two (j:Kourovka.Ambient.I) : weight j<2 ↔ j.val<3 := by
  fin_cases j <;> decide

end Kourovka.Lattice.Weighted
