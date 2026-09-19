/- Uncompiled source. The exact unimodular change of basis and its explicit inverse. -/
import Kourovka.Ambient.Bilinear
import Kourovka.Linear.BilinearOps

namespace Kourovka.Lattice
open Kourovka.Linear Kourovka.Ambient
variable {R : Type*} [CommRing R]

def toOriginalFn (a : V R) (i : I) : R :=
  if i = 2 then a 1 + a 3
  else if i = 3 then a 2
  else if i = 4 ∨ i = 10 ∨ i = 27 then a 1 + a i
  else a i

def fromOriginalFn (a : V R) (i : I) : R :=
  if i = 2 then a 3
  else if i = 3 then a 2 - a 1
  else if i = 4 ∨ i = 10 ∨ i = 27 then a i - a 1
  else a i

/-- Valid over every commutative ring, not just a characteristic-zero field. -/
def P : V R ≃ₗ[R] V R where
  toFun := toOriginalFn
  invFun := fromOriginalFn
  left_inv := by
    intro a
    funext i
    fin_cases i <;> simp [toOriginalFn,fromOriginalFn] <;> ring
  right_inv := by
    intro a
    funext i
    fin_cases i <;> simp [toOriginalFn,fromOriginalFn] <;> ring
  map_add' := by
    intro a b
    funext i
    fin_cases i <;> simp [toOriginalFn] <;> ring
  map_smul' := by
    intro c a
    funext i
    fin_cases i <;> simp [toOriginalFn,smul_eq_mul] <;> ring

def adaptedB : Bilinear R (V R) := transport P Ambient.B

def weight (i : I) : Nat :=
  if i.val < 2 then 0 else if i.val = 2 then 1 else 2

def degree (i : I) : Nat := 2 + weight i

theorem weight_bounds (i : I) : weight i ≤ 2 := by
  unfold weight
  split_ifs <;> omega

theorem degree_bounds (i : I) : 2 ≤ degree i ∧ degree i ≤ 4 := by
  have h := weight_bounds i
  dsimp [degree]
  omega

/-- The map from ell-coordinates to adapted ambient coordinates. -/
def diagonal : V Int →ₗ[Int] V Int where
  toFun a := fun i => (1009 : Int) ^ degree i * a i
  map_add' := by intro a b; funext i; simp [mul_add]
  map_smul' := by intro c a; funext i; simp [smul_eq_mul]; ring

/-- ell_j = p^(2+w_j) b_j, expressed in the original ambient basis. -/
def embed : V Int →ₗ[Int] V Int := P.toLinearMap.comp diagonal

@[simp] theorem embed_apply (a : V Int) : embed a = P (diagonal a) := rfl

theorem diagonal_injective : Function.Injective diagonal := by
  intro a b h
  funext i
  have hh := congrFun h i
  exact mul_left_cancel₀ (pow_ne_zero _ (by norm_num : (1009 : Int) ≠ 0)) hh

theorem embed_injective : Function.Injective embed :=
  P.injective.comp diagonal_injective

/-- Every ell vector has ambient coordinates divisible by p². -/
theorem embed_divisible_two (a : V Int) :
    ∃ b : V Int, embed a = (1009 : Int)^2 • b := by
  let b : V Int := fun i => (1009 : Int) ^ weight i * a i
  refine ⟨P b, ?_⟩
  change P (diagonal a) = _
  rw [← map_smul]
  apply congrArg P
  funext i
  change (1009 : Int)^degree i * a i = (1009 : Int)^2 * ((1009 : Int)^weight i * a i)
  rw [degree, pow_add]
  ring

/-- A bounded-index saturation estimate; no invalid cancellation modulo p^i is used. -/
theorem embed_divisible_reflect (N : Nat) (hN : 4 ≤ N) (a b : V Int)
    (h : embed a = (1009 : Int)^N • b) :
    ∃ c : V Int, a = (1009 : Int)^(N-4) • c := by
  let v : V Int := P.symm b
  let c : V Int := fun i => (1009 : Int)^(4-degree i) * v i
  refine ⟨c, ?_⟩
  have hh := congrArg P.symm h
  simp only [embed_apply, LinearEquiv.symm_apply_apply, map_smul] at hh
  funext i
  have hi := congrFun hh i
  change (1009 : Int)^degree i * a i = (1009 : Int)^N * v i at hi
  apply mul_left_cancel₀ (pow_ne_zero _ (by norm_num : (1009 : Int) ≠ 0))
  change (1009 : Int)^degree i * a i =
    (1009 : Int)^degree i * ((1009 : Int)^(N-4) * ((1009 : Int)^(4-degree i) * v i))
  rw [hi]
  have hd := degree_bounds i
  have hexp : degree i + (N-4) + (4-degree i) = N := by omega
  rw [← mul_assoc, ← mul_assoc, ← pow_add, ← pow_add, hexp]

end Kourovka.Lattice
