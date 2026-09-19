/- Exact algebraic part of the unit-factor argument.
No assertion about convergence or integrality of the infinite U-series is made here. -/
import Mathlib.Algebra.Algebra.Basic
import Mathlib.Algebra.Module.End
import Mathlib.Tactic

namespace Kourovka.Analytic

variable {A : Type*} [Ring A]

/-- A geometric polynomial, defined recursively without any inverse operation. -/
def geometric (x:A) : Nat → A
  | 0 => 0
  | n+1 => 1+x*geometric x n

theorem one_sub_mul_geometric (x:A) (n:Nat) :
    (1-x)*geometric x n = 1-x^n := by
  induction n with
  | zero => simp [geometric]
  | succ n ih =>
    rw [geometric]
    calc
      (1-x)*(1+x*geometric x n) = (1-x)+x*((1-x)*geometric x n) := by noncomm_ring
      _ = (1-x)+x*(1-x^n) := by rw [ih]
      _ = 1-x^(n+1) := by rw [pow_succ']; noncomm_ring

theorem geometric_mul_one_sub (x:A) (n:Nat) :
    geometric x n*(1-x) = 1-x^n := by
  induction n with
  | zero => simp [geometric]
  | succ n ih =>
    rw [geometric]
    calc
      (1+x*geometric x n)*(1-x) = (1-x)+x*(geometric x n*(1-x)) := by noncomm_ring
      _ = (1-x)+x*(1-x^n) := by rw [ih]
      _ = 1-x^(n+1) := by rw [pow_succ']; noncomm_ring

/-- The inverse is explicit even in a noncommutative ring and even with zero divisors. -/
def oneSubUnit (x:A) (n:Nat) (h:x^n=0) : Aˣ where
  val := 1-x
  inv := geometric x n
  val_inv := by rw [one_sub_mul_geometric,h,sub_zero]
  inv_val := by rw [geometric_mul_one_sub,h,sub_zero]

def oneAddUnit (x:A) (n:Nat) (h:x^n=0) : Aˣ := by
  have hn : (-x)^n=0 := by rw [neg_pow,h,mul_zero]
  exact oneSubUnit (-x) n hn

@[simp] theorem oneAddUnit_val (x:A) (n:Nat) (h:x^n=0) :
    (oneAddUnit x n h : A) = 1+x := by simp [oneAddUnit,oneSubUnit]

variable {R : Type*} [CommRing R] [Algebra R A]

def evalHorner (X:A) : List R → A
  | [] => 0
  | c::cs => algebraMap R A c + X*evalHorner X cs

theorem commute_evalHorner (X:A) (cs:List R) : Commute X (evalHorner X cs) := by
  induction cs with
  | nil => exact Commute.zero_right X
  | cons c cs ih =>
    change Commute X (algebraMap R A c+X*evalHorner X cs)
    have hc : Commute X (algebraMap R A c) := (Algebra.commutes c X).symm
    exact hc.add_right ((Commute.refl X).mul_right ih)

/-- Any polynomial 1+X*V(X) is a unit when X is nilpotent. -/
def polynomialUnit (X:A) (cs:List R) (n:Nat) (hX:X^n=0) : Aˣ :=
  oneAddUnit (X*evalHorner X cs) n (by
    rw [(commute_evalHorner X cs).mul_pow,hX,zero_mul])

@[simp] theorem polynomialUnit_val (X:A) (cs:List R) (n:Nat) (hX:X^n=0) :
    (polynomialUnit X cs n hX:A) = 1+X*evalHorner X cs := by
  simp [polynomialUnit]

section Module
variable {M : Type*} [AddCommGroup M] [Module R M]

/-- Units of the endomorphism ring are actual linear equivalences. -/
def unitToEquiv (U : (Module.End R M)ˣ) : M ≃ₗ[R] M where
  toFun := (U:Module.End R M)
  invFun := (↑(U⁻¹) : Module.End R M)
  left_inv := by
    intro x
    have h := congrArg (fun D:Module.End R M => D x) U.inv_val
    simpa only [Module.End.mul_apply,Module.End.one_apply] using h
  right_inv := by
    intro x
    have h := congrArg (fun D:Module.End R M => D x) U.val_inv
    simpa only [Module.End.mul_apply,Module.End.one_apply] using h
  map_add' := (U:Module.End R M).map_add
  map_smul' := (U:Module.End R M).map_smul

/-- Exact equality of the two zero conditions, not a first-order approximation. -/
theorem factor_zero_iff (X:Module.End R M) (U:(Module.End R M)ˣ) (x:M) :
    ((U:Module.End R M)*X) x=0 ↔ X x=0 := by
  change (unitToEquiv U) (X x)=0 ↔ X x=0
  constructor
  · intro h
    apply (unitToEquiv U).injective
    simpa only [map_zero] using h
  · intro h
    rw [h,map_zero]

/-- At a quotient precision, an integral unit factor preserves exactly the same congruence ideal.
Both preservation assumptions must later be proved for the ACTUAL tensor lattice and U. -/
theorem factor_mem_iff (X:Module.End R M) (U:(Module.End R M)ˣ) (S:Submodule R M)
    (hU:∀ x,x∈S → (U:Module.End R M) x∈S)
    (hInv:∀ x,x∈S → (↑(U⁻¹) : Module.End R M) x∈S) (v:M) :
    ((U:Module.End R M)*X) v∈S ↔ X v∈S := by
  constructor
  · intro h
    have hh := hInv _ h
    have he := congrArg (fun D:Module.End R M => D (X v)) U.inv_val
    change (↑(U⁻¹) : Module.End R M) ((U : Module.End R M) (X v)) = X v at he
    change (↑(U⁻¹) : Module.End R M) ((U : Module.End R M) (X v)) ∈ S at hh
    rw [he] at hh
    exact hh
  · intro h
    exact hU _ h

end Module
end Kourovka.Analytic
