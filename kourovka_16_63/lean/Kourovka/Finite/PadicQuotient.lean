/- Uncompiled source. The genuine p-adic reduction map and its exact kernel. -/
import Kourovka.Finite.Coordinates
import Mathlib.NumberTheory.Padics.RingHoms
import Mathlib.GroupTheory.QuotientGroup.Basic

namespace Kourovka.Finite.Padic
open Kourovka.Ambient Kourovka.Lattice
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

theorem reduction_bracket (i:Nat) (x y:Ell) :
    reduction i (LB x y)=LB (reduction i x) (reduction i y) := by
  exact mapVec_LB (PadicInt.toZModPow i) x y

/-- Thus the formal finite coordinates carry precisely the reduced p-adic ell bracket. -/
theorem quotient_coordinate_order (i:Nat) :
    Nat.card (Ell ⧸ (reduction i).ker)=1009^(31*i) := by
  rw [Nat.card_congr (quotientEquiv i).toEquiv]
  exact cardinality i

end Kourovka.Finite.Padic
