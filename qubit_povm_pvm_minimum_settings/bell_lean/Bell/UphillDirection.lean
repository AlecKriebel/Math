import Bell.Lorentz
import Mathlib.LinearAlgebra.Dimension.Constructions

/-!
# An explicit rank-one uphill direction

This replaces the full ambient-inertia calculation in the algebraic part of
§9.1 by a simpler construction. For a positive vector v of the state bilinear
form, the endomorphisms W(z) = v zᵀ form a four-dimensional positive family.
At most three homogeneous compatibility constraints leave a nonzero z.
Normalization is imposed by adding a multiple of the identity, without changing
second variation. This argument uses actual linear maps and bilinear forms;
it does not assume the desired uphill conclusion.

This module does NOT identify the forms with the physical incidence Hessian,
construct multipliers, or integrate a tangent to a physical curve.
Validated with the pinned Lean 4.19.0 toolchain; see local_verification/uphill_build.log.
-/
noncomputable section
open scoped BigOperators Matrix
namespace Bell.Lorentz

abbrev Endomorphism := V →ₗ[ℝ] V
abbrev Bilinear := V →ₗ[ℝ] V →ₗ[ℝ] ℝ

def weightedSecondForm (B : Bilinear) (lam : Fin 5 → ℝ) (W : Endomorphism) : ℝ :=
  ∑ j, lam j * B (W (ray j)) (W (ray j))

def compatibility (B : Bilinear) (μ : Fin 5 → ℝ) (W : Endomorphism) : ℝ :=
  ∑ j, μ j * B (ray j) (W (ray j))

def rankOneEndomorphism (v z : V) : Endomorphism where
  toFun := fun y => dotProduct z y • v
  map_add' := by
    intro x y
    simp only [dotProduct,Pi.add_apply,mul_add,Finset.sum_add_distrib,add_smul]
  map_smul' := by
    intro r y
    simp only [dotProduct,Pi.smul_apply,smul_eq_mul]
    have h : (∑ i, z i * (r * y i)) = r * ∑ i, z i * y i := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i _
      ring
    rw [h,smul_smul]
    rfl

@[simp]
theorem rankOneEndomorphism_apply (v z y : V) :
    rankOneEndomorphism v z y = dotProduct z y • v := rfl

theorem dot_ray_basis (z : V) (i : Fin 4) :
    dotProduct z (ray i.castSucc) = z i := by
  fin_cases i <;> simp [Matrix.cons_val, dotProduct,ray,Fin.sum_univ_succ]

theorem positive_weighted_ray_squares (lam : Fin 5 → ℝ)
    (hlam : ∀ j, 0 < lam j) (z : V) (hz : z ≠ 0) :
    0 < ∑ j, lam j * (dotProduct z (ray j))^2 := by
  have hex : ∃ i : Fin 4, z i ≠ 0 := by
    by_contra hn
    push_neg at hn
    exact hz (funext hn)
  obtain ⟨i,hi⟩ := hex
  have hpos : 0 < lam i.castSucc * (dotProduct z (ray i.castSucc))^2 := by
    rw [dot_ray_basis]
    exact mul_pos (hlam i.castSucc) (sq_pos_of_ne_zero hi)
  exact lt_of_lt_of_le hpos
    (Finset.single_le_sum (fun j _ => mul_nonneg (le_of_lt (hlam j)) (sq_nonneg (dotProduct z (ray j))))
      (Finset.mem_univ i.castSucc))

theorem secondForm_rankOne (B : Bilinear) (lam : Fin 5 → ℝ) (v z : V) :
    weightedSecondForm B lam (rankOneEndomorphism v z) =
      B v v * ∑ j, lam j * (dotProduct z (ray j))^2 := by
  simp only [weightedSecondForm,rankOneEndomorphism_apply,map_smul,LinearMap.smul_apply,
    smul_eq_mul,Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j _
  ring

/-- Four real unknowns and at most three homogeneous real linear equations. -/
theorem nonzero_kernel_of_three_constraints {k : ℕ} (hk : k ≤ 3)
    (f : V →ₗ[ℝ] (Fin k → ℝ)) : ∃ z : V, z ≠ 0 ∧ f z = 0 := by
  classical
  by_contra hn
  have hker : ∀ z : V, f z = 0 → z = 0 := by
    intro z hz
    by_contra hne
    exact hn ⟨z,hne,hz⟩
  have hinj : Function.Injective f := by
    intro x y hxy
    apply sub_eq_zero.mp
    apply hker
    rw [map_sub,hxy,sub_self]
  have hdim : 4 ≤ k := by
    simpa [V] using LinearMap.finrank_le_finrank_of_injective hinj
  omega

def compatibilityMap {k : ℕ} (B : Bilinear) (μ : Fin k → Fin 5 → ℝ) (v : V) :
    V →ₗ[ℝ] (Fin k → ℝ) where
  toFun := fun z i => ∑ j, μ i j * B (ray j) v * dotProduct z (ray j)
  map_add' := by
    intro z z'
    funext i
    simp only [Pi.add_apply,dotProduct,add_mul,Finset.sum_add_distrib,mul_add]
  map_smul' := by
    intro r z
    funext i
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply, smul_dotProduct,
      Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j _
    ring

@[simp]
theorem compatibilityMap_apply {k : ℕ} (B : Bilinear) (μ : Fin k → Fin 5 → ℝ)
    (v z : V) (i : Fin k) :
    compatibilityMap B μ v z i = ∑ j, μ i j * B (ray j) v * dotProduct z (ray j) := rfl

theorem compatibility_rankOne {k : ℕ} (B : Bilinear) (μ : Fin k → Fin 5 → ℝ)
    (v z : V) (i : Fin k) :
    compatibility B (μ i) (rankOneEndomorphism v z) = compatibilityMap B μ v z i := by
  simp only [compatibility,rankOneEndomorphism_apply,compatibilityMap_apply,
    map_smul,smul_eq_mul]
  apply Finset.sum_congr rfl
  intro j _
  ring

/-- An uphill direction exists without diagonalizing the 16-dimensional form. -/
theorem uphill_of_three_compatibilities {k : ℕ} (hk : k ≤ 3)
    (B : Bilinear) (v : V) (hv : 0 < B v v)
    (lam : Fin 5 → ℝ) (hlam : ∀ j, 0 < lam j) (μ : Fin k → Fin 5 → ℝ) :
    ∃ W : Endomorphism, 0 < weightedSecondForm B lam W ∧
      ∀ i, compatibility B (μ i) W = 0 := by
  obtain ⟨z,hz,hf⟩ := nonzero_kernel_of_three_constraints hk (compatibilityMap B μ v)
  refine ⟨rankOneEndomorphism v z,?_,?_⟩
  · rw [secondForm_rankOne]
    exact mul_pos hv (positive_weighted_ray_squares lam hlam z hz)
  · intro i
    rw [compatibility_rankOne]
    exact congrFun hf i

theorem compatibility_sum {k : ℕ} (B : Bilinear) (μ : Fin k → Fin 5 → ℝ)
    (c : Fin k → ℝ) (W : Endomorphism) :
    compatibility B (∑ i, c i • μ i) W = ∑ i, c i * compatibility B (μ i) W := by
  simp only [compatibility,Finset.sum_apply,Pi.smul_apply,smul_eq_mul,
    Finset.sum_mul,Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem compatibility_add_identity (B : Bilinear) (μ : Fin 5 → ℝ)
    (W : Endomorphism) (t : ℝ)
    (hnull : ∀ j, B (ray j) (ray j) = 0) :
    compatibility B μ (W + t • LinearMap.id) = compatibility B μ W := by
  simp only [compatibility,LinearMap.add_apply,LinearMap.smul_apply,
    LinearMap.id_apply,map_add,map_smul,smul_eq_mul,hnull,mul_zero,add_zero]

theorem secondForm_add_identity (B : Bilinear) (hB : ∀ x y, B x y = B y x)
    (lam : Fin 5 → ℝ) (W : Endomorphism) (t : ℝ)
    (hnull : ∀ j, B (ray j) (ray j) = 0) :
    weightedSecondForm B lam (W + t • LinearMap.id) =
      weightedSecondForm B lam W + 2*t*compatibility B lam W := by
  simp only [weightedSecondForm,compatibility,LinearMap.add_apply,LinearMap.smul_apply,
    LinearMap.id_apply,map_add,map_smul,LinearMap.add_apply,LinearMap.smul_apply,
    smul_eq_mul,hnull,mul_zero,add_zero,Finset.mul_sum,← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro j _
  rw [hB (W (ray j)) (ray j)]
  ring

/-- Normalization does not consume another positive dimension: the radial
identity direction is null and orthogonal to the compatible tangent. -/
theorem normalized_uphill_of_three_compatibilities {k : ℕ} (hk : k ≤ 3)
    (B : Bilinear) (hB : ∀ x y, B x y = B y x)
    (hnull : ∀ j, B (ray j) (ray j) = 0)
    (v : V) (hv : 0 < B v v)
    (lam : Fin 5 → ℝ) (hlam : ∀ j, 0 < lam j)
    (μ : Fin k → Fin 5 → ℝ) (c : Fin k → ℝ)
    (hspan : lam = ∑ i, c i • μ i)
    (N : Endomorphism →ₗ[ℝ] ℝ) (hN : N LinearMap.id = 1) :
    ∃ W : Endomorphism, 0 < weightedSecondForm B lam W ∧
      (∀ i, compatibility B (μ i) W = 0) ∧ N W = 0 := by
  obtain ⟨W,hup,hcomp⟩ := uphill_of_three_compatibilities hk B v hv lam hlam μ
  have hlamcomp : compatibility B lam W = 0 := by
    rw [hspan,compatibility_sum]
    simp [hcomp]
  refine ⟨W + (-N W) • LinearMap.id,?_,?_,?_⟩
  · rw [secondForm_add_identity B hB lam W (-N W) hnull,hlamcomp,mul_zero,add_zero]
    exact hup
  · intro i
    rw [compatibility_add_identity B (μ i) W (-N W) hnull]
    exact hcomp i
  · rw [map_add,map_smul,hN,smul_eq_mul,mul_one]
    ring

end Bell.Lorentz
