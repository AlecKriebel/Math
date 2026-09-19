/- Uncompiled source. Exact cardinality of all diagonal systems, including free columns. -/
import Kourovka.Certificates.ScalarKernel
import Kourovka.Certificates.KernelTransport
import Mathlib.Data.Fintype.Pi

namespace Kourovka.Certificates
open scoped BigOperators

variable {R : Type*} [CommRing R]
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def diagonalMap (a : ι → R) : (ι → R) →ₗ[R] (ι → R) where
  toFun x := fun j => a j*x j
  map_add' := by intro x y; funext j; simp only [Pi.add_apply,mul_add]
  map_smul' := by intro c x; funext j; simp only [Pi.smul_apply,smul_eq_mul,RingHom.id_apply]; ring

/-- The actual complete solution set separates coordinatewise. -/
def diagonalKernelEquiv (a : ι → R) :
    KernelSet (diagonalMap a) ≃ ((j:ι) → {x:R // a j*x=0}) where
  toFun x j := ⟨x.val j,congrFun x.property j⟩
  invFun x := ⟨fun j => (x j).val,funext fun j => (x j).property⟩
  left_inv := by intro x; rfl
  right_inv := by intro x; rfl

theorem diagonalKernel_card [Fintype R] (a : ι → R) :
    Nat.card (KernelSet (diagonalMap a)) = ∏ j, Nat.card {x:R // a j*x=0} := by
  classical
  rw [Nat.card_congr (diagonalKernelEquiv a)]
  simp only [Nat.card_eq_fintype_card,Fintype.card_pi]

/-- Padding a system by identically zero output rows changes no kernel. -/
def padMap {V W : Type*} [AddCommGroup V] [Module R V] [AddCommGroup W] [Module R W]
    (K : V →ₗ[R] W) (τ : Type*) : V →ₗ[R] (W × (τ→R)) := K.prod 0

def paddedKernelEquiv {V W : Type*} [AddCommGroup V] [Module R V]
    [AddCommGroup W] [Module R W] (K : V →ₗ[R] W) (τ : Type*) :
    KernelSet (padMap K τ) ≃ KernelSet K where
  toFun x := ⟨x.val,congrArg Prod.fst x.property⟩
  invFun x := ⟨x.val,by ext <;> simp [padMap,x.property]⟩
  left_inv := by intro x; rfl
  right_inv := by intro x; rfl

/-- The abstract diagonal vector contains a valuation for each constrained column;
none is a genuinely zero column. The application must certify which case each actual column has. -/
def diagonalCoefficient (p depth : Nat) (valuation : Option Nat) : ZMod (p^depth) :=
  match valuation with
  | none => 0
  | some v => (p^v : Nat)

theorem diagonal_prime_power_card (p depth : Nat) (hp : 0<p)
    (vals : ι → Option Nat) (hv : ∀ j v, vals j=some v → v≤depth) :
    Nat.card (KernelSet (diagonalMap (fun j => diagonalCoefficient p depth (vals j)))) =
      p ^ (∑ j, (vals j).getD depth) := by
  classical
  letI : NeZero (p^depth) := ⟨ne_of_gt (pow_pos hp depth)⟩
  rw [diagonalKernel_card]
  have heach : ∀ j, Nat.card {x : ZMod (p^depth) //
      diagonalCoefficient p depth (vals j)*x=0} = p^((vals j).getD depth) := by
    intro j
    cases hval : vals j with
    | none =>
      simp only [diagonalCoefficient,hval,Option.getD_none]
      rw [Nat.card_congr (ScalarKernel.zeroKernelEquiv (ZMod (p^depth)))]
      simp [Nat.card_eq_fintype_card,ZMod.card]
    | some v =>
      simpa only [diagonalCoefficient,hval,Option.getD_some] using
        ScalarKernel.prime_power_card p depth v hp (hv j v hval)
  simp_rw [heach]
  rw [Finset.prod_pow_eq_pow_sum]

end Kourovka.Certificates
