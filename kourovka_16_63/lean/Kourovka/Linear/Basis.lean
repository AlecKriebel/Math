/- Uncompiled proof source. Finite-coordinate extensionality, with no enumeration of vectors. -/
import Mathlib.LinearAlgebra.BilinearMap
import Mathlib.Tactic

namespace Kourovka.Linear
open scoped BigOperators

variable {R : Type*} [CommRing R]
variable {I : Type*} [Fintype I] [DecidableEq I]

/-- The standard coordinate vector. The order of the equality is intentional. -/
def unitVec (i : I) : I → R := fun j => if i = j then 1 else 0

@[simp] theorem unitVec_same (i : I) : (unitVec i : I → R) i = 1 := by
  simp [unitVec]

@[simp] theorem unitVec_other (i j : I) (h : i ≠ j) :
    (unitVec i : I → R) j = 0 := by simp [unitVec, h]

theorem decompose (v : I → R) : v = ∑ i, v i • unitVec i := by
  funext j
  simp [unitVec, Finset.sum_apply, Pi.smul_apply, smul_eq_mul]

variable {V : Type*} [AddCommGroup V] [Module R V]

/-- Two linear maps agree once they agree on coordinate vectors. -/
theorem ext_basis (f g : (I → R) →ₗ[R] V)
    (h : ∀ i, f (unitVec i) = g (unitVec i)) : f = g := by
  apply LinearMap.ext
  intro v
  conv_lhs => rw [decompose v]
  conv_rhs => rw [decompose v]
  simp only [map_sum, map_smul, h]

theorem linear_apply (f : (I → R) →ₗ[R] V) (v : I → R) :
    f v = ∑ i, v i • f (unitVec i) := by
  conv_lhs => rw [decompose v]
  simp only [map_sum, map_smul]

theorem ext_bilinear
    (b c : (I → R) →ₗ[R] (I → R) →ₗ[R] V)
    (h : ∀ i j, b (unitVec i) (unitVec j) = c (unitVec i) (unitVec j)) : b = c := by
  apply ext_basis
  intro i
  apply ext_basis
  intro j
  exact h i j

theorem ext_trilinear
    (b c : (I → R) →ₗ[R] (I → R) →ₗ[R] (I → R) →ₗ[R] V)
    (h : ∀ i j k, b (unitVec i) (unitVec j) (unitVec k) =
      c (unitVec i) (unitVec j) (unitVec k)) : b = c := by
  apply ext_basis
  intro i
  apply ext_bilinear
  exact h i

/-- The full Leibniz defect, not merely a numerical test on a list. -/
def jacobiTensor (b : (I → R) →ₗ[R] (I → R) →ₗ[R] (I → R)) :
    (I → R) →ₗ[R] (I → R) →ₗ[R] (I → R) →ₗ[R] (I → R) where
  toFun u :=
    { toFun := fun v =>
        { toFun := fun w => b u (b v w) - b (b u v) w - b v (b u w)
          map_add' := by
            intro w z
            simp only [LinearMap.coe_mk, AddHom.coe_mk, map_add, LinearMap.add_apply]
            abel
          map_smul' := by
            intro a w
            simp only [LinearMap.coe_mk, AddHom.coe_mk, map_smul, LinearMap.smul_apply, smul_sub, RingHom.id_apply] }
      map_add' := by
        intro v z
        apply LinearMap.ext
        intro w
        simp only [LinearMap.coe_mk, AddHom.coe_mk, map_add, LinearMap.add_apply]
        abel
      map_smul' := by
        intro a v
        apply LinearMap.ext
        intro w
        simp only [LinearMap.coe_mk, AddHom.coe_mk, map_smul, LinearMap.smul_apply, smul_sub, RingHom.id_apply] }
  map_add' := by
    intro u z
    apply LinearMap.ext
    intro v
    apply LinearMap.ext
    intro w
    simp only [LinearMap.coe_mk, AddHom.coe_mk, map_add, LinearMap.add_apply]
    abel
  map_smul' := by
    intro a u
    apply LinearMap.ext
    intro v
    apply LinearMap.ext
    intro w
    simp only [LinearMap.coe_mk, AddHom.coe_mk, map_smul, LinearMap.smul_apply, smul_sub, RingHom.id_apply]

/-- A finite basis certificate implies the identity for every vector over R. -/
theorem jacobi_of_basis (b : (I → R) →ₗ[R] (I → R) →ₗ[R] (I → R))
    (h : ∀ i j k,
      b (unitVec i) (b (unitVec j) (unitVec k)) -
      b (b (unitVec i) (unitVec j)) (unitVec k) -
      b (unitVec j) (b (unitVec i) (unitVec k)) = 0) :
    ∀ u v w, b u (b v w) = b (b u v) w + b v (b u w) := by
  have hz : jacobiTensor b = 0 := by
    apply ext_trilinear
    intro i j k
    simpa only [jacobiTensor, LinearMap.coe_mk, AddHom.coe_mk,
      LinearMap.zero_apply] using h i j k
  intro u v w
  have hval : b u (b v w) - b (b u v) w - b v (b u w) = 0 := by
    have hh := congrArg (fun F => F u v w) hz
    simpa [jacobiTensor] using hh
  calc
    b u (b v w) =
        (b u (b v w) - b (b u v) w - b v (b u w)) +
          (b (b u v) w + b v (b u w)) := by abel
    _ = b (b u v) w + b v (b u w) := by rw [hval, zero_add]

end Kourovka.Linear
