/- Uncompiled source. Full Lie-RING automorphisms, scalar-linear automorphisms and
invertible bracket-preserving matrices. These equivalences do not count the group
and do not assert the missing BCH/group-automorphism correspondence. -/
import Kourovka.Finite.AdditiveLinear
import Mathlib.Algebra.Lie.Basic
import Kourovka.Linear.EndomorphismCoordinates

namespace Kourovka.Finite.FullAutomorphisms
open Kourovka.Linear
abbrev I := Fin 31
abbrev RAt (i : Nat) := ZMod (1009^i)
abbrev LAt (i : Nat) := I → RAt i

variable (i : Nat)
variable [LieRing (LAt i)] [LieAlgebra (RAt i) (LAt i)]
local notation "LB" => fun x y : LAt i => ⁅x,y⁆

/-- The ordinary mathlib equivalence type over Int: full additive bracket bijections. -/
abbrev RingAut := (LAt i) ≃ₗ⁅Int⁆ (LAt i)
abbrev ScalarAut := (LAt i) ≃ₗ⁅RAt i⁆ (LAt i)

def toScalar (Q : RingAut i) : ScalarAut i :=
  { additiveEquivToLinear Q.toLinearEquiv.toAddEquiv with
    map_lie' := by intro x y; exact Q.map_lie x y }

def toInteger (Q : ScalarAut i) : RingAut i where
  toFun := Q
  invFun := Q.invFun
  left_inv := Q.left_inv
  right_inv := Q.right_inv
  map_add' := Q.toLinearEquiv.map_add
  map_smul' := by
    intro z x
    exact Q.toLinearEquiv.toAddMonoidHom.map_zsmul x z
  map_lie' := by intro x y; exact Q.map_lie x y

/-- Automatic residue-ring linearity is surjective on the entire automorphism set. -/
def ringAutEquivScalarAut : RingAut i ≃ ScalarAut i where
  toFun := toScalar i
  invFun := toInteger i
  left_inv := by intro Q; apply LieEquiv.ext; intro x; rfl
  right_inv := by intro Q; apply LieEquiv.ext; intro x; rfl

/-- Entries of EVERY invertible bracket-preserving map; no chosen subgroup or exponential domain. -/
def AdmissibleEntries : Type :=
  {a : (I × I) → RAt i //
    Function.Bijective (fromEntries a) ∧
      ∀ x y, fromEntries a (LB x y)=LB (fromEntries a x) (fromEntries a y)}

def toEntriesAut (Q : ScalarAut i) : AdmissibleEntries i :=
  ⟨toEntries Q.toLinearEquiv.toLinearMap,by
    constructor
    · simpa only [fromEntries_entries] using Q.toLinearEquiv.bijective
    · intro x y
      simp only [fromEntries_entries]
      exact Q.map_lie x y⟩

noncomputable def fromEntriesAut (a : AdmissibleEntries i) : ScalarAut i :=
  { LinearEquiv.ofBijective (fromEntries a.val) a.property.1 with
    map_lie' := by intro x y; exact a.property.2 x y }

noncomputable def scalarAutEquivEntries : ScalarAut i ≃ AdmissibleEntries i where
  toFun := toEntriesAut i
  invFun := fromEntriesAut i
  left_inv := by
    intro Q
    apply LieEquiv.ext
    intro x
    change fromEntries (toEntries Q.toLinearEquiv.toLinearMap) x=Q x
    rw [fromEntries_entries]
    rfl
  right_inv := by
    intro a
    apply Subtype.ext
    change toEntries (fromEntries a.val)=a.val
    exact entries_fromEntries a.val

/-- Complete matrix presentation of the full Lie-ring automorphism SET. -/
noncomputable def ringAutEquivEntries : RingAut i ≃ AdmissibleEntries i :=
  (ringAutEquivScalarAut i).trans (scalarAutEquivEntries i)

theorem full_lie_aut_card_eq_matrix_card :
    Nat.card (RingAut i)=Nat.card (AdmissibleEntries i) :=
  Nat.card_congr (ringAutEquivEntries i)

end Kourovka.Finite.FullAutomorphisms
