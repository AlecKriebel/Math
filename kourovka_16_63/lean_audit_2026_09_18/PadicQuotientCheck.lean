import Mathlib.NumberTheory.Padics.RingHoms
import Mathlib.GroupTheory.QuotientGroup.Basic
import Kourovka.Linear.EndomorphismCoordinates
import Kourovka.Parameters
import Mathlib.SetTheory.Cardinal.Finite
namespace Kourovka.Ambient
abbrev I := Fin 31
abbrev V (R : Type*) := I → R
def mapVec {R S : Type*} [CommRing R] [CommRing S] (f : R →+* S) (x : V R) : V S := fun j => f (x j)
end Kourovka.Ambient
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
    simpa using (ZMod.intCast_zmod_eq_zero_iff_dvd (a j) (1009^i)).mpr
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


end Kourovka.Finite
namespace Kourovka.Finite.Padic
open Kourovka.Ambient
local instance : Fact (Nat.Prime 1009) := ⟨Kourovka.prime_is_prime⟩
abbrev O := PadicInt 1009
abbrev Ell := V O

/-- Coefficientwise canonical p-adic reduction, not a chosen integer approximation. -/
noncomputable def reduction (i:Nat) : Ell →+ LAt i where
  toFun x := fun j => PadicInt.toZModPow i (x j)
  map_zero' := by funext j; exact map_zero _
  map_add' := by intro x y; funext j; exact map_add _ _ _

/-- Integer representatives provide a right inverse as a function, not a ring homomorphism. -/
noncomputable def sectionMap (i:Nat) (x:LAt i) : Ell := fun j => (x j).val

theorem reduction_section (i:Nat) (x:LAt i) : reduction i (sectionMap i x)=x := by
  funext j
  change PadicInt.toZModPow i ((x j).val:O)=x j
  rw [map_natCast,ZMod.natCast_zmod_val]

theorem reduction_surjective (i:Nat) : Function.Surjective (reduction i) :=
  fun x => ⟨sectionMap i x,reduction_section i x⟩

theorem reduction_scalar_zero (i:Nat) (a:O) :
    PadicInt.toZModPow i a=0 ↔ (1009:O)^i ∣ a := by
  change a∈RingHom.ker (PadicInt.toZModPow i) ↔ _
  rw [PadicInt.ker_toZModPow,Ideal.mem_span_singleton]
  norm_cast

/-- The kernel is exactly p^i times the ell-coordinate lattice, in both directions. -/
theorem reduction_zero_iff (i:Nat) (x:Ell) :
    reduction i x=0 ↔ ∃ y:Ell,x=(1009:O)^i • y := by
  constructor
  · intro h
    have hh : ∀ j,(1009:O)^i ∣ x j := by
      intro j
      exact (reduction_scalar_zero i (x j)).mp (congrFun h j)
    choose y hy using hh
    exact ⟨y,funext hy⟩
  · rintro ⟨y,rfl⟩
    funext j
    apply (reduction_scalar_zero i _).mpr
    exact ⟨y j,rfl⟩

/-- First isomorphism theorem for the additive quotient; no BCH group is being asserted. -/
noncomputable def quotientEquiv (i:Nat) :
    Ell ⧸ (reduction i).ker ≃+ LAt i :=
  QuotientAddGroup.quotientKerEquivOfSurjective (reduction i) (reduction_surjective i)

/-- Thus the formal finite coordinates carry precisely the reduced p-adic ell bracket. -/
theorem quotient_coordinate_order (i:Nat) :
    Nat.card (Ell ⧸ (reduction i).ker)=1009^(31*i) := by
  rw [Nat.card_congr (quotientEquiv i).toEquiv]
  exact cardinality i

end Kourovka.Finite.Padic
