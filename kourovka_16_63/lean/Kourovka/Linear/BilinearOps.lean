/- Uncompiled source. Elementary operations on bilinear maps. -/
import Kourovka.Linear.Basis
import Kourovka.Bracket

namespace Kourovka.Linear
variable {R : Type*} [CommRing R]
variable {V : Type*} [AddCommGroup V] [Module R V]

abbrev Bilinear (R V : Type*) [CommRing R] [AddCommGroup V] [Module R V] :=
  V →ₗ[R] V →ₗ[R] V

def post (F : V →ₗ[R] V) (b : Bilinear R V) : Bilinear R V where
  toFun u := F.comp (b u)
  map_add' := by intro u v; apply LinearMap.ext; intro w; simp
  map_smul' := by intro c u; apply LinearMap.ext; intro w; simp

def pre (b : Bilinear R V) (F G : V →ₗ[R] V) : Bilinear R V where
  toFun u := (b (F u)).comp G
  map_add' := by intro u v; apply LinearMap.ext; intro w; simp
  map_smul' := by intro c u; apply LinearMap.ext; intro w; simp

@[simp] theorem post_apply (F : V →ₗ[R] V) (b : Bilinear R V) (u v : V) :
    post F b u v = F (b u v) := rfl
@[simp] theorem pre_apply (b : Bilinear R V) (F G : V →ₗ[R] V) (u v : V) :
    pre b F G u v = b (F u) (G v) := rfl

/-- Explicitly bilinear transport; the change of basis must be invertible. -/
def transport (P : V ≃ₗ[R] V) (b : Bilinear R V) : Bilinear R V :=
  post P.symm.toLinearMap (pre b P.toLinearMap P.toLinearMap)

@[simp] theorem transport_apply (P : V ≃ₗ[R] V) (b : Bilinear R V) (u v : V) :
    transport P b u v = P.symm (b (P u) (P v)) := rfl

theorem hom_of_basis {I : Type*} [Fintype I] [DecidableEq I]
    (F : (I → R) →ₗ[R] (I → R)) (b c : Bilinear R (I → R))
    (h : ∀ i j, F (b (unitVec i) (unitVec j)) =
      c (F (unitVec i)) (F (unitVec j))) :
    ∀ u v, F (b u v) = c (F u) (F v) := by
  have hh : post F b = pre c F F := ext_bilinear _ _ h
  intro u v
  exact congrArg (fun a => a u v) hh

/-- The Leibniz operator as a linear map of the candidate endomorphism. -/
def delta (b : Bilinear R V) :
    (V →ₗ[R] V) →ₗ[R] Bilinear R V where
  toFun D := post D b - pre b D LinearMap.id - pre b LinearMap.id D
  map_add' := by
    intro D E
    apply LinearMap.ext
    intro u
    apply LinearMap.ext
    intro v
    simp only [post_apply, pre_apply, LinearMap.add_apply, LinearMap.sub_apply,
      LinearMap.id_apply, map_add]
    abel
  map_smul' := by
    intro a D
    apply LinearMap.ext
    intro u
    apply LinearMap.ext
    intro v
    simp only [post_apply, pre_apply, LinearMap.smul_apply, LinearMap.sub_apply,
      LinearMap.id_apply, map_smul, smul_sub, RingHom.id_apply]

@[simp] theorem delta_apply (b : Bilinear R V) (D : V →ₗ[R] V) (u v : V) :
    delta b D u v = D (b u v) - b (D u) v - b u (D v) := rfl

end Kourovka.Linear

namespace Kourovka.Sparse
variable {R : Type*} [CommRing R]

def bilinear (ts : List Term) : Vec R →ₗ[R] Vec R →ₗ[R] Vec R where
  toFun u :=
    { toFun := fromTerms ts u
      map_add' := fromTerms_add_right ts u
      map_smul' := by intro a v; exact fromTerms_smul_right ts a u v }
  map_add' := by
    intro u v
    apply LinearMap.ext
    intro w
    funext k
    exact congrFun (fromTerms_add_left ts u v w) k
  map_smul' := by
    intro a u
    apply LinearMap.ext
    intro v
    funext k
    exact congrFun (fromTerms_smul_left ts a u v) k

end Kourovka.Sparse
