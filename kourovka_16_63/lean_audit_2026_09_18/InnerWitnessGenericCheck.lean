import Kourovka.Certificates.InnerWitnessData
namespace Kourovka.Certificates.InnerRank
open Kourovka.Linear Kourovka.Ambient Kourovka.Lattice
open scoped BigOperators
/-- The checked finite matrix identities imply an identity on ALL parameter vectors. -/
theorem extractor_innerMap_of_check (hcheck : ∀ i, LeftInverseCheck i) (a : Param → Rat) : extractor (innerMap a) = a := by
  have hmap : extractor.comp (innerMap (R:=Rat)) = LinearMap.id := by
    apply ext_basis
    intro j
    funext i
    change extractor (innerMap (unitVec j)) i = unitVec j i
    rw [innerMap_unit]
    simpa only [extractor, LinearMap.coe_mk, AddHom.coe_mk, unitVec, eq_comm] using
      hcheck i j
  exact congrArg (fun F : (Param → Rat) →ₗ[Rat] (Param → Rat) => F a) hmap

theorem innerMap_injective_of_check (hcheck : ∀ i, LeftInverseCheck i) : Function.Injective (innerMap (R:=Rat)) := by
  intro a b hab
  have h := congrArg extractor hab
  simpa only [extractor_innerMap_of_check hcheck] using h

end Kourovka.Certificates.InnerRank
