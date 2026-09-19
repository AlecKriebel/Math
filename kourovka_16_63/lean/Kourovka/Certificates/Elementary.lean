/- Uncompiled source. A checked elementary-operation circuit with a soundness proof.
This is not yet a translation/replay of the supplied 931-pivot compressed plan. -/
import Kourovka.Certificates.KernelTransport
import Kourovka.Linear.Basis
import Mathlib.Tactic

namespace Kourovka.Certificates.Elementary
open Kourovka.Linear

variable {R : Type*} [CommRing R]
variable {n : Nat}
abbrev Coord (R : Type*) (n : Nat) := Fin n → R

/-- A coordinate permutation, over an arbitrary commutative ring. -/
def permute (p : Equiv.Perm (Fin n)) : Coord R n ≃ₗ[R] Coord R n where
  toFun x := fun i => x (p i)
  invFun x := fun i => x (p.symm i)
  left_inv := by intro x; funext i; simp
  right_inv := by intro x; funext i; simp
  map_add' := by intro x y; rfl
  map_smul' := by intro c x; rfl

def shearFun (i j : Fin n) (c:R) (x:Coord R n) : Coord R n :=
  fun k => if k=i then x i+c*x j else x k

/-- Adding a multiple of a DIFFERENT coordinate is always invertible, including at nonunits. -/
def shear (i j : Fin n) (hij : i≠j) (c:R) : Coord R n ≃ₗ[R] Coord R n where
  toFun := shearFun i j c
  invFun := shearFun i j (-c)
  left_inv := by
    intro x; funext k
    by_cases hk : k=i
    · subst k; simp [shearFun,hij,Ne.symm hij]
    · simp [shearFun,hk]
  right_inv := by
    intro x; funext k
    by_cases hk : k=i
    · subst k; simp [shearFun,hij,Ne.symm hij]
    · simp [shearFun,hk]
  map_add' := by
    intro x y; funext k
    by_cases hk : k=i <;> simp [shearFun,hk] <;> ring
  map_smul' := by
    intro a x; funext k
    by_cases hk : k=i <;> simp [shearFun,hk,smul_eq_mul] <;> ring

/-- A supplied inverse is used only after its exact multiplication identity is checked. -/
def scale (i : Fin n) (a b:R) (hab : a*b=1) : Coord R n ≃ₗ[R] Coord R n where
  toFun x := fun k => if k=i then a*x k else x k
  invFun x := fun k => if k=i then b*x k else x k
  left_inv := by
    intro x; funext k
    by_cases hk : k=i <;> simp [hk,← mul_assoc,mul_comm b a,hab]
  right_inv := by
    intro x; funext k
    by_cases hk : k=i <;> simp [hk,← mul_assoc,hab]
  map_add' := by intro x y; funext k; by_cases hk:k=i <;> simp [hk,mul_add]
  map_smul' := by intro c x; funext k; by_cases hk:k=i <;> simp [hk,smul_eq_mul] <;> ring

/-- Raw data contain no mathematical proof fields. In particular a proposed inverse is untrusted. -/
inductive Op (R:Type*) (n:Nat) where
  | swap (i j:Fin n)
  | add (i j:Fin n) (c:R)
  | mul (i:Fin n) (a inverse:R)

def decode [DecidableEq R] : Op R n → Option (Coord R n ≃ₗ[R] Coord R n)
  | .swap i j => some (permute (Equiv.swap i j))
  | .add i j c => if h:i≠j then some (shear i j h c) else none
  | .mul i a b => if h:a*b=1 then some (scale i a b h) else none

/-- The first list entry is applied first. A failed inversion/divisibility check cannot be skipped. -/
def decodeList [DecidableEq R] : List (Op R n) → Option (Coord R n ≃ₗ[R] Coord R n)
  | [] => some (LinearEquiv.refl R _)
  | op::ops => do
    let head ← decode op
    let tail ← decodeList ops
    pure (head.trans tail)

structure Circuit (R:Type*) (m n:Nat) where
  rows : List (Op R m)
  cols : List (Op R n)

/-- The result is either rejected or accompanied by actual invertible coordinate changes. -/
def decodeCircuit [DecidableEq R] {m:Nat} (C:Circuit R m n) :
    Option ((Coord R m ≃ₗ[R] Coord R m) × (Coord R n ≃ₗ[R] Coord R n)) := do
  let A ← decodeList C.rows
  let B ← decodeList C.cols
  pure (A,B)

variable {m:Nat}

/-- Ordinary finite basis equality, with a theorem reducing it to equality of ALL vectors. -/
def basisCheck [DecidableEq R] (K D:Coord R n →ₗ[R] Coord R m)
    (A:Coord R m ≃ₗ[R] Coord R m) (B:Coord R n ≃ₗ[R] Coord R n) : Bool :=
  decide (∀ j:Fin n, ∀ i:Fin m, A (K (B (unitVec j))) i = D (unitVec j) i)

theorem basisCheck_sound [DecidableEq R] (K D:Coord R n →ₗ[R] Coord R m)
    (A:Coord R m ≃ₗ[R] Coord R m) (B:Coord R n ≃ₗ[R] Coord R n)
    (h:basisCheck K D A B = true) :
    (A.toLinearMap.comp K).comp B.toLinearMap = D := by
  have hb : ∀ j:Fin n, ∀ i:Fin m, A (K (B (unitVec j))) i = D (unitVec j) i :=
    of_decide_eq_true h
  apply ext_basis
  intro j
  funext i
  exact hb j i

def check [DecidableEq R] (K D:Coord R n →ₗ[R] Coord R m) (C:Circuit R m n) : Bool :=
  match decodeCircuit C with
  | none => false
  | some (A,B) => basisCheck K D A B

/-- Certificate acceptance entails a complete kernel equivalence, not merely equal rank over a field. -/
theorem check_sound [DecidableEq R] (K D:Coord R n →ₗ[R] Coord R m) (C:Circuit R m n)
    (h:check K D C = true) : Nonempty (KernelSet D ≃ KernelSet K) := by
  cases hd : decodeCircuit C with
  | none => simp [check,hd] at h
  | some pair =>
    rcases pair with ⟨A,B⟩
    have hb : basisCheck K D A B = true := by simpa only [check,hd] using h
    exact ⟨kernelTransformEquiv K D A B (basisCheck_sound K D A B hb)⟩

theorem check_card [DecidableEq R] (K D:Coord R n →ₗ[R] Coord R m) (C:Circuit R m n)
    (h:check K D C = true) : Nat.card (KernelSet K) = Nat.card (KernelSet D) := by
  obtain ⟨e⟩ := check_sound K D C h
  exact (Nat.card_congr e).symm

/-- Negative test: 3 is not a unit modulo 9, regardless of the proposed inverse. -/
theorem rejects_nonunit : decode (R:=ZMod 9) (.mul (0:Fin 2) 3 3) = none := by
  have h : (3 : ZMod 9) * 3 ≠ 1 := by decide
  simp [decode, h]

/-- Negative test: adding a coordinate to itself is not silently treated as an invertible shear. -/
theorem rejects_same_coordinate : decode (R:=ZMod 9) (.add (0:Fin 2) 0 1) = none := by
  simp [decode]

/-- Positive test over a composite ring, without any Field instance. -/
theorem accepts_unit : (decode (R:=ZMod 9) (.mul (0:Fin 2) 2 5)).isSome = true := by decide

end Kourovka.Certificates.Elementary
