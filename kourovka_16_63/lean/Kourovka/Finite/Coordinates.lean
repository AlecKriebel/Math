/- Uncompiled source. Explicit finite Lie carrier, reduction and its cardinality.
No coordinatewise additive group is substituted for the missing BCH group. -/
import Kourovka.Lattice.Integral
import Kourovka.Parameters
import Kourovka.Finite.AdditiveLinear
import Mathlib.SetTheory.Cardinal.Finite

namespace Kourovka.Finite
open Kourovka.Linear Kourovka.Ambient

instance primePower_neZero (i : Nat) : NeZero (1009^i) :=
  ⟨pow_ne_zero _ (by decide)⟩

abbrev RAt (i : Nat) := ZMod (1009^i)
abbrev LAt (i : Nat) := V (RAt i)

/-- The reduction of the explicit integer lattice coefficients. -/
def reduce (i : Nat) (a : V Int) : LAt i := mapVec (Int.castRingHom (RAt i)) a

def lift (i : Nat) (a : LAt i) : V Int := fun j => ZMod.cast (a j)

@[simp] theorem reduce_lift (i : Nat) (a : LAt i) : reduce i (lift i a) = a := by
  funext j
  exact ZMod.intCast_zmod_cast (a j)

theorem reduce_surjective (i : Nat) : Function.Surjective (reduce i) :=
  fun a => ⟨lift i a,reduce_lift i a⟩

theorem reduce_bracket (i : Nat) (a b : V Int) :
    reduce i (Lattice.LB a b) = Lattice.LB (reduce i a) (reduce i b) :=
  Lattice.mapVec_LB (Int.castRingHom (RAt i)) a b

/-- Coordinatewise quotient kernel, proved using integer divisibility. -/
theorem reduce_eq_zero_iff (i : Nat) (a : V Int) :
    reduce i a = 0 ↔ ∀ j, ((1009 : Int)^i) ∣ a j := by
  constructor
  · intro h j
    have hh := congrFun h j
    simpa using (ZMod.intCast_zmod_eq_zero_iff_dvd (a j) (1009^i)).mp
      (by simpa [reduce,mapVec] using hh)
  · intro h
    funext j
    exact (ZMod.intCast_zmod_eq_zero_iff_dvd (a j) (1009^i)).mpr
      (by simpa using h j)

/-- Every finite vector has an integer lift, and its additive normal form is unique. -/
theorem cardinality (i : Nat) : Nat.card (LAt i) = 1009^(31*i) := by
  rw [Nat.card_eq_fintype_card]
  change Fintype.card (Fin 31 → ZMod (1009^i)) = _
  rw [Fintype.card_fun,ZMod.card,Fintype.card_fin,← pow_mul]
  congr 1
  omega

theorem cardinality_at_depth : Nat.card (LAt 1689) = 1009^52359 := by
  simpa only [Kourovka.coordinate_exponent] using cardinality 1689

/-- The finite Lie-ring structure is obtained from the exact scaled bracket. -/
def lieRingAt (i : Nat) : LieRing (LAt i) := Lattice.lieRing (RAt i)
def lieAlgebraAt (i : Nat) :
    letI := lieRingAt i
    LieAlgebra (RAt i) (LAt i) := Lattice.lieAlgebra (RAt i)

end Kourovka.Finite
