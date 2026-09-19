import Kourovka.Finite.Coordinates
import Kourovka.Linear.EndomorphismCoordinates
namespace AuditAbstractConstructor
open Kourovka.Finite Kourovka.Linear Kourovka.Ambient Kourovka.Lattice
variable (i : Nat)
local instance : LieRing (LAt i) := lieRingAt i
local instance : LieAlgebra (RAt i) (LAt i) := lieAlgebraAt i
noncomputable def ofLinear (f : LAt i →ₗ[RAt i] LAt i)
    (hf : Function.Bijective f)
    (hb : ∀ x y, f (LB x y) = LB (f x) (f y)) :
    (LAt i) ≃ₗ⁅RAt i⁆ (LAt i) :=
  LieEquiv.ofBijective
    { toLinearMap := f
      map_lie' := by intro x y; exact hb x y }
    hf
noncomputable def ofEntries (a : (I × I) → RAt i)
    (hf : Function.Bijective (fromEntries a))
    (hb : ∀ x y, fromEntries a (LB x y) = LB (fromEntries a x) (fromEntries a y)) :
    (LAt i) ≃ₗ⁅RAt i⁆ (LAt i) := ofLinear i (fromEntries a) hf hb
end AuditAbstractConstructor
