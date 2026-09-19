/- Uncompiled source. All endomorphisms, with the paper's output-row/input-column convention. -/
import Kourovka.Linear.BilinearOps

namespace Kourovka.Linear
open scoped BigOperators
variable {R : Type*} [CommRing R]
variable {I : Type*} [Fintype I] [DecidableEq I]
abbrev EndCoords (I R : Type*) := I × I → R

/-- Matrix unit E_ab takes v to its b-coordinate times the a-th standard vector. -/
def elementary (a b : I) : (I → R) →ₗ[R] (I → R) where
  toFun v := v b • unitVec a
  map_add' := by intro u v; simp [add_smul]
  map_smul' := by intro c u; simp [Pi.smul_apply,smul_eq_mul,smul_smul]

@[simp] theorem elementary_apply (a b : I) (v : I → R) :
    elementary a b v = v b • unitVec a := rfl

def fromEntries : EndCoords I R →ₗ[R] ((I → R) →ₗ[R] (I → R)) where
  toFun d := ∑ c : I × I, d c • elementary c.1 c.2
  map_add' := by intro d e; simp [add_smul,Finset.sum_add_distrib]
  map_smul' := by intro c d; simp [smul_smul,Finset.smul_sum,smul_eq_mul]

def toEntries : ((I → R) →ₗ[R] (I → R)) →ₗ[R] EndCoords I R where
  toFun D := fun c => D (unitVec c.2) c.1
  map_add' := by intro D E; rfl
  map_smul' := by intro c D; rfl

/-- Usual matrix-vector multiplication, derived from the matrix-unit expansion. -/
theorem fromEntries_apply (d : EndCoords I R) (v : I → R) (i : I) :
    fromEntries d v i = ∑ j, d (i,j) * v j := by
  simp [fromEntries,Fintype.sum_prod_type,elementary,unitVec,
    Finset.sum_apply,Pi.smul_apply,smul_eq_mul]

@[simp] theorem entries_fromEntries (d : EndCoords I R) : toEntries (fromEntries d) = d := by
  funext c
  rcases c with ⟨a,b⟩
  simp [toEntries,fromEntries_apply,unitVec]

@[simp] theorem fromEntries_entries (D : (I → R) →ₗ[R] (I → R)) :
    fromEntries (toEntries D) = D := by
  apply ext_basis
  intro j
  funext i
  simp [fromEntries_apply,toEntries,unitVec]

/-- A proved inverse pair: every endomorphism, not just selected matrices. -/
def endomorphismCoordinates : EndCoords I R ≃ₗ[R] ((I → R) →ₗ[R] (I → R)) :=
  { fromEntries with
    invFun := toEntries
    left_inv := entries_fromEntries
    right_inv := fromEntries_entries }

end Kourovka.Linear
