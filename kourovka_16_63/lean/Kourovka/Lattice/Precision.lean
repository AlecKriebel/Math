/- Uncompiled source. Exact lattice error estimates and the word-induction lifting step.
These are general lemmas; constructing/reducing the concrete quotient representatives remains separate. -/
import Kourovka.Lattice.Expressions

namespace Kourovka.Lattice.Precision
open Kourovka.Linear

variable {R : Type*} [CommRing R]
variable {M : Type*} [AddCommGroup M] [Module R M]

/-- p^n A as an R-submodule of a common ambient module. -/
def scaled (p : R) (n : Nat) (A : Submodule R M) : Submodule R M where
  carrier := {v | ∃ a, a ∈ A ∧ v = p^n • a}
  zero_mem' := ⟨0,A.zero_mem,by simp⟩
  add_mem' := by
    rintro v w ⟨a,ha,rfl⟩ ⟨b,hb,rfl⟩
    exact ⟨a+b,A.add_mem ha hb,(smul_add _ _ _).symm⟩
  smul_mem' := by
    rintro c v ⟨a,ha,rfl⟩
    refine ⟨c • a,A.smul_mem c ha,?_⟩
    simp only [smul_smul]
    rw [mul_comm c]

theorem scaled_le (p : R) (n : Nat) (A : Submodule R M) : scaled p n A ≤ A := by
  rintro v ⟨a,ha,rfl⟩
  exact A.smul_mem _ ha

theorem scaled_mono (p : R) (n : Nat) {A B : Submodule R M} (h : A ≤ B) :
    scaled p n A ≤ scaled p n B := by
  rintro v ⟨a,ha,rfl⟩
  exact ⟨a,h ha,rfl⟩

theorem scaled_antitone (p : R) (A : Submodule R M) {n m : Nat} (h : n ≤ m) :
    scaled p m A ≤ scaled p n A := by
  rintro v ⟨a,ha,rfl⟩
  refine ⟨p^(m-n) • a,A.smul_mem _ ha,?_⟩
  rw [smul_smul,← pow_add,Nat.add_sub_of_le h]

theorem cancel_smul [NoZeroSMulDivisors R M] {c : R} (hc : c ≠ 0)
    {a b : M} (h : c • a = c • b) : a = b := by
  have hh : c • (a-b) = 0 := by rw [smul_sub,h,sub_self]
  exact sub_eq_zero.mp ((smul_eq_zero.mp hh).resolve_left hc)

/-- Division is justified by torsion freeness in the ambient module, NOT by field division in ZMod(p^i). -/
theorem cancel_scaled_membership [IsDomain R] [NoZeroSMulDivisors R M]
    (p : R) (hp : p ≠ 0) (A : Submodule R M)
    (a b : Nat) (hab : a ≤ b) (v : M)
    (h : p^a • v ∈ scaled p b A) : v ∈ scaled p (b-a) A := by
  obtain ⟨w,hw,heq⟩ := h
  refine ⟨w,hw,?_⟩
  apply cancel_smul (pow_ne_zero a hp)
  rw [heq,smul_smul,← pow_add,Nat.add_sub_of_le hab]

/-- An arbitrary bilinear error on A×A loses exactly four further powers on B×B. -/
theorem bilinear_error_enlargement [IsDomain R] [NoZeroSMulDivisors R M]
    (p : R) (hp : p ≠ 0) (i : Nat) (hi : 6 ≤ i)
    (A B : Submodule R M) (hBA : scaled p 2 B ≤ A)
    (E : Bilinear R M)
    (hE : ∀ u, u ∈ A → ∀ v, v ∈ A → E u v ∈ scaled p (i-2) A) :
    ∀ u, u ∈ B → ∀ v, v ∈ B → E u v ∈ scaled p (i-6) A := by
  intro u hu v hv
  have hu' : p^2 • u ∈ A := hBA ⟨u,hu,rfl⟩
  have hv' : p^2 • v ∈ A := hBA ⟨v,hv,rfl⟩
  have hh := hE _ hu' _ hv'
  have hfac : E (p^2 • u) (p^2 • v) = p^4 • E u v := by
    simp only [map_smul,LinearMap.smul_apply,smul_smul,← pow_add]
  rw [hfac] at hh
  have hcan := cancel_scaled_membership p hp A 4 (i-2) (by omega) (E u v) hh
  have he : i-2-4 = i-6 := by omega
  simpa only [he] using hcan

def automorphismError (b : Bilinear R M) (Q : M →ₗ[R] M) : Bilinear R M :=
  post Q b - pre b Q Q

@[simp] theorem automorphismError_apply (b : Bilinear R M) (Q : M →ₗ[R] M) (u v : M) :
    automorphismError b Q u v = Q (b u v) - b (Q u) (Q v) := rfl

theorem error_scaled_bracket (c : R) (b : Bilinear R M) (Q : M →ₗ[R] M) (u v : M) :
    automorphismError (c • b) Q u v = c • automorphismError b Q u v := by
  simp only [automorphismError_apply,LinearMap.smul_apply,map_smul,smul_sub]

theorem derivation_scaled_bracket (c : R) (b : Bilinear R M) (D : M →ₗ[R] M) (u v : M) :
    delta (c • b) D u v = c • delta b D u v := by
  simp only [delta_apply,LinearMap.smul_apply,map_smul,smul_sub]

/-- The manuscript's i-6 estimate, starting with the SCALED bracket congruence on A. -/
theorem arbitrary_automorphism_error_bound [IsDomain R] [NoZeroSMulDivisors R M]
    (p : R) (hp : p ≠ 0) (i : Nat) (hi : 6 ≤ i)
    (A B : Submodule R M) (hBA : scaled p 2 B ≤ A)
    (b : Bilinear R M) (Q : M →ₗ[R] M)
    (h : ∀ u, u ∈ A → ∀ v, v ∈ A →
      automorphismError (p^2 • b) Q u v ∈ scaled p i A) :
    ∀ u, u ∈ B → ∀ v, v ∈ B →
      automorphismError b Q u v ∈ scaled p (i-6) A := by
  apply bilinear_error_enlargement p hp i hi A B hBA (automorphismError b Q)
  intro u hu v hv
  have hh := h u hu v hv
  rw [error_scaled_bracket] at hh
  exact cancel_scaled_membership p hp A 2 i (by omega) _ hh

theorem arbitrary_derivation_error_bound [IsDomain R] [NoZeroSMulDivisors R M]
    (p : R) (hp : p ≠ 0) (i : Nat) (hi : 6 ≤ i)
    (A B : Submodule R M) (hBA : scaled p 2 B ≤ A)
    (b : Bilinear R M) (D : M →ₗ[R] M)
    (h : ∀ u, u ∈ A → ∀ v, v ∈ A → delta (p^2 • b) D u v ∈ scaled p i A) :
    ∀ u, u ∈ B → ∀ v, v ∈ B → delta b D u v ∈ scaled p (i-6) A := by
  apply bilinear_error_enlargement p hp i hi A B hBA (delta b D)
  intro u hu v hv
  have hh := h u hu v hv
  rw [derivation_scaled_bracket] at hh
  exact cancel_scaled_membership p hp A 2 i (by omega) _ hh

def expressionSpan (b : M → M → M) (x y : M) : Submodule R M :=
  Submodule.span R (Set.range (Expr.eval b x y))

/-- Once generation is supplied, the representative is integral on B despite its nonzero bracket error. -/
theorem approximate_lift_preserves (B : Submodule R M) (b : M → M → M)
    (hB : ∀ u, u ∈ B → ∀ v, v ∈ B → b u v ∈ B)
    (x y : M) (hx : x ∈ B) (hy : y ∈ B)
    (hgen : expressionSpan b x y = B)
    (Q : M →ₗ[R] M) (hQx : Q x ∈ B) (hQy : Q y ∈ B)
    (hE : ∀ u, u ∈ B → ∀ v, v ∈ B → Q (b u v)-b (Q u) (Q v) ∈ B) :
    ∀ u, u ∈ B → Q u ∈ B := by
  have hh : B ≤ B.comap Q := by
    nth_rw 1 [← hgen]
    apply Submodule.span_le.mpr
    rintro a ⟨e,rfl⟩
    exact Expr.approximate_map_mem B b hB Q x y hx hy hQx hQy hE e
  exact hh

theorem approximate_derivation_lift_preserves (B : Submodule R M) (b : M → M → M)
    (hB : ∀ u, u ∈ B → ∀ v, v ∈ B → b u v ∈ B)
    (x y : M) (hx : x ∈ B) (hy : y ∈ B)
    (hgen : expressionSpan b x y = B)
    (D : M →ₗ[R] M) (hDx : D x ∈ B) (hDy : D y ∈ B)
    (hE : ∀ u, u ∈ B → ∀ v, v ∈ B →
      D (b u v)-b (D u) v-b u (D v) ∈ B) :
    ∀ u, u ∈ B → D u ∈ B := by
  have hh : B ≤ B.comap D := by
    nth_rw 1 [← hgen]
    apply Submodule.span_le.mpr
    rintro a ⟨e,rfl⟩
    exact Expr.approximate_derivation_mem B b hB D x y hx hy hDx hDy hE e
  exact hh

end Kourovka.Lattice.Precision
