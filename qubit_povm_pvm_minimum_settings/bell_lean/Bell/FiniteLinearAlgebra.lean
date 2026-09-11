import Bell.IncidenceAlgebra
import Mathlib.LinearAlgebra.Dual.Lemmas

/-!
# Finite linear algebra for the incidence tangent space

This file proves the annihilator criterion used to lift compatible W-directions
into metric variations. In particular, membership in the range of the metric
map is derived, not supplied as an additional hypothesis.
-/
noncomputable section
open scoped Bell.Entrywise
open scoped BigOperators Matrix
namespace Bell

/-- A finite-dimensional vector belongs to a linear image exactly when every
annihilator of that image annihilates the vector. The proof works for arbitrary
real vector spaces; the quotient is free because the scalars form a field. -/
theorem mem_range_iff_annihilators
    {E F : Type*} [AddCommGroup E] [Module ℝ E] [AddCommGroup F] [Module ℝ F]
    (D : E →ₗ[ℝ] F) (v : F) :
    v ∈ LinearMap.range D ↔
      ∀ l : F →ₗ[ℝ] ℝ, (∀ x, l (D x) = 0) → l v = 0 := by
  constructor
  · rintro ⟨x, rfl⟩ l hl
    exact hl x
  · intro h
    by_contra hn
    obtain ⟨l, hlv, hlrange⟩ :=
      Submodule.exists_dual_map_eq_bot_of_nmem hn (inferInstance : Module.Free ℝ
        (F ⧸ LinearMap.range D))
    apply hlv
    apply h l
    intro x
    have hm : l (D x) ∈ (LinearMap.range D).map l :=
      ⟨D x, ⟨x, rfl⟩, rfl⟩
    rw [hlrange] at hm
    exact hm

/-- Every real functional on a finite product is its coordinate dot product. -/
theorem finite_functional_coordinates {n : ℕ} (l : (Fin n → ℝ) →ₗ[ℝ] ℝ)
    (x : Fin n → ℝ) :
    l x = ∑ i, l (Pi.single i 1) * x i := by
  have hx : (∑ i : Fin n, x i • (Pi.single i 1 : Fin n → ℝ)) = x := by
    funext j
    simp [Pi.single_apply]
  calc
    l x = l (∑ i : Fin n, x i • (Pi.single i 1 : Fin n → ℝ)) := congrArg l hx.symm
    _ = ∑ i, l (Pi.single i 1) * x i := by simp [mul_comm]

namespace Lorentz

/-- The transpose metric differential, without irrelevant scalar factor 2. -/
def nullRowMap (Y : M) : (Fin 5 → ℝ) →ₗ[ℝ] V where
  toFun := fun μ => ∑ j, μ j • phi (Y *ᵥ ray j)
  map_add' := by intro μ ν; simp [Pi.add_apply, add_smul, Finset.sum_add_distrib]
  map_smul' := by intro t μ; simp [Pi.smul_apply, mul_smul, Finset.smul_sum]

/-- The metric-variable part of the five null differentials. -/
def metricDifferential (Y : M) : V →ₗ[ℝ] (Fin 5 → ℝ) where
  toFun := fun h j => 2 * dotProduct h (phi (Y *ᵥ ray j))
  map_add' := by intro h k; funext j; simp [add_dotProduct, mul_add]
  map_smul' := by intro t h; funext j; simp [smul_dotProduct, mul_assoc, mul_left_comm]

@[simp]
theorem nullRowMap_single (Y : M) (j : Fin 5) :
    nullRowMap Y (Pi.single j 1) = phi (Y *ᵥ ray j) := by
  simp [nullRowMap, Pi.single_apply]

theorem metricDifferential_apply (Y : M) (h : V) (j : Fin 5) :
    metricDifferential Y h j = matrixPair (metricVariation h) (Y *ᵥ ray j) (Y *ᵥ ray j) :=
  (metricVariation_quadratic h (Y *ᵥ ray j)).symm

theorem metricDifferential_pairing (Y : M) (μ : Fin 5 → ℝ) (h : V) :
    (∑ j, μ j * metricDifferential Y h j) = 2 * dotProduct h (nullRowMap Y μ) := by
  change (∑ j, μ j * (2 * dotProduct h (phi (Y *ᵥ ray j)))) =
    2 * dotProduct h (∑ j, μ j • phi (Y *ᵥ ray j))
  simp only [dotProduct, Finset.sum_apply,
    Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  ring

/-- Pointwise metric stationarity is exactly membership in the row-map kernel. -/
theorem metric_stationary_iff (Y : M) (lam : Fin 5 → ℝ) :
    (∀ h, weightedGram lam (metricVariation h) Y = 0) ↔ nullRowMap Y lam = 0 := by
  have heq (h : V) : weightedGram lam (metricVariation h) Y =
      2 * dotProduct h (nullRowMap Y lam) := by
    simpa only [weightedGram, ← metricDifferential_apply] using
      metricDifferential_pairing Y lam h
  constructor
  · intro hs
    funext i
    have hi := hs (Pi.single i 1)
    rw [heq] at hi
    simp at hi
    change nullRowMap Y lam i = 0
    linarith
  · intro hs h
    rw [heq, hs]
    simp

/-- A metric increment realizing a desired null differential exists as soon as
all transpose-kernel compatibility equations hold. -/
theorem exists_metric_increment (Y : M) (c : Fin 5 → ℝ)
    (hc : ∀ μ : Fin 5 → ℝ, nullRowMap Y μ = 0 → ∑ j, μ j * c j = 0) :
    ∃ h : V, metricDifferential Y h = c := by
  apply (mem_range_iff_annihilators (metricDifferential Y) c).mpr
  intro l hl
  let μ : Fin 5 → ℝ := fun j => l (Pi.single j 1)
  have hμ : nullRowMap Y μ = 0 := by
    funext i
    have hi := hl (Pi.single i 1)
    rw [finite_functional_coordinates] at hi
    change (∑ j, μ j * metricDifferential Y (Pi.single i 1) j) = 0 at hi
    rw [metricDifferential_pairing] at hi
    simp at hi
    change nullRowMap Y μ i = 0
    linarith
  rw [finite_functional_coordinates]
  exact hc μ hμ

/-- This is the precise lift needed in the W parameterization. -/
theorem exists_compatible_metric (G Y : M) (W : Endomorphism)
    (hcompat : ∀ μ, nullRowMap Y μ = 0 →
      compatibility (pullbackForm G (linearOfMatrix Y)) μ W = 0) :
    ∃ h : V, ∀ j,
      2 * matrixPair G (Y *ᵥ ray j) (Y *ᵥ W (ray j)) +
        matrixPair (metricVariation h) (Y *ᵥ ray j) (Y *ᵥ ray j) = 0 := by
  let c : Fin 5 → ℝ := fun j =>
    -2 * matrixPair G (Y *ᵥ ray j) (Y *ᵥ W (ray j))
  obtain ⟨h, hh⟩ := exists_metric_increment Y c (by
    intro μ hμ
    have hc := hcompat μ hμ
    change (∑ j, μ j * matrixPair G (Y *ᵥ ray j) (Y *ᵥ W (ray j))) = 0 at hc
    calc
      (∑ j, μ j * c j) = -2 * ∑ j,
          μ j * matrixPair G (Y *ᵥ ray j) (Y *ᵥ W (ray j)) := by
        simp only [c, Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro j _
        ring
      _ = 0 := by rw [hc]; ring)
  refine ⟨h, fun j => ?_⟩
  have hj := congrFun hh j
  rw [metricDifferential_apply] at hj
  dsimp only [c] at hj
  linarith

end Lorentz
end Bell
