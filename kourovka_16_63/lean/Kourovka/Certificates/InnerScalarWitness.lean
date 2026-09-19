/- Uncompiled source. Transfer of the small exact rank witness to every
characteristic-zero field, including Q_1009. No assumption of unchanged modular
rank or of a flatness theorem is needed: the LEFT INVERSE itself is transported. -/
import Kourovka.Certificates.InnerWitness

namespace Kourovka.Certificates.InnerRank
open Kourovka.Linear Kourovka.Ambient Kourovka.Lattice
open scoped BigOperators
set_option maxRecDepth 20000
set_option maxHeartbeats 2000000

variable (F : Type*) [Field F] [CharZero F]

/-- The matrix coefficient of an inner derivation is an integer polynomial in the
actual bracket constants, hence is compatible with the rational scalar extension. -/
theorem inner_entry_cast (j:Param) (c:Col) :
    algebraMap Rat F (toEntries (innerColumn (R:=Rat) j) c) =
      toEntries (innerColumn (R:=F) j) c := by
  have h := congrFun (mapVec_LB (algebraMap Rat F)
    (unitVec (Fin.castLE (by decide : 30≤31) j)) (unitVec c.2)) c.1
  simpa only [mapVec_unit,mapVec,innerColumn,toEntries] using h

def extendedInverse (i j:Param) : F := algebraMap Rat F (inverseCoeff i j)

theorem extended_left_inverse (i j:Param) :
    (∑ t:Param,extendedInverse F i t * toEntries (innerColumn (R:=F) j) (selectedRow t)) =
      if i=j then 1 else 0 := by
  have h := congrArg (algebraMap Rat F) (leftInverse_all i j)
  by_cases hij:i=j
  · simpa only [map_sum,map_mul,inner_entry_cast,extendedInverse,if_pos hij,map_one] using h
  · simpa only [map_sum,map_mul,inner_entry_cast,extendedInverse,if_neg hij,map_zero] using h

def extendedExtractor : (V F →ₗ[F] V F) →ₗ[F] (Param → F) where
  toFun D := fun i => ∑ j,extendedInverse F i j * toEntries D (selectedRow j)
  map_add' := by
    intro D E; funext i
    simp [mul_add,Finset.sum_add_distrib]
  map_smul' := by
    intro c D; funext i
    simp only [map_smul,Pi.smul_apply,smul_eq_mul,Finset.mul_sum,RingHom.id_apply]
    apply Finset.sum_congr rfl
    intro j hj
    ring

theorem extendedExtractor_innerMap (a:Param→F) : extendedExtractor F (innerMap a)=a := by
  have hmap : (extendedExtractor F).comp (innerMap (R:=F))=LinearMap.id := by
    apply ext_basis
    intro j
    funext i
    change extendedExtractor F (innerMap (unitVec j)) i = unitVec j i
    rw [innerMap_unit]
    simpa only [extendedExtractor, LinearMap.coe_mk, AddHom.coe_mk, unitVec, eq_comm] using
      extended_left_inverse F i j
  exact congrArg (fun G:(Param→F)→ₗ[F](Param→F) => G a) hmap

theorem extended_inner_injective : Function.Injective (innerMap (R:=F)) := by
  intro a b hab
  have h := congrArg (extendedExtractor F) hab
  simpa only [extendedExtractor_innerMap] using h

end Kourovka.Certificates.InnerRank
