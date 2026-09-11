import Bell.Quantum

/-! Algebraic convexification lemmas for paper Lemma 2.2.
These do not include compactness or the separating-hyperplane argument. -/

noncomputable section
open scoped BigOperators
namespace Bell

/-- A finite common randomization cannot exceed a common upper bound. -/
theorem finite_mixture_bound {ι : Type*} [Fintype ι]
    (weight value : ι → ℝ) (U : ℝ)
    (hweight : ∀ i, 0 ≤ weight i) (hnorm : ∑ i, weight i = 1)
    (hvalue : ∀ i, value i ≤ U) :
    ∑ i, weight i * value i ≤ U := by
  calc
    ∑ i, weight i * value i ≤ ∑ i, weight i * U :=
      Finset.sum_le_sum (fun i _ => mul_le_mul_of_nonneg_left (hvalue i) (hweight i))
    _ = (∑ i, weight i) * U := by rw [Finset.sum_mul]
    _ = U := by rw [hnorm, one_mul]

/-- Linear inequalities extend to the actual Mathlib convex hull. -/
theorem linear_bound_on_convexHull {E : Type*} [AddCommGroup E] [Module ℝ E]
    (f : E →ₗ[ℝ] ℝ) (S : Set E) (U : ℝ)
    (hS : ∀ p ∈ S, f p ≤ U) :
    ∀ p ∈ convexHull ℝ S, f p ≤ U := by
  have hc : Convex ℝ {p : E | f p ≤ U} := by
    intro x hx y hy a b ha hb hab
    change f (a • x + b • y) ≤ U
    simp only [map_add, map_smul, smul_eq_mul]
    calc
      a * f x + b * f y ≤ a * U + b * U :=
        add_le_add (mul_le_mul_of_nonneg_left hx ha)
          (mul_le_mul_of_nonneg_left hy hb)
      _ = U := by rw [← add_mul, hab, one_mul]
  have hsub : S ⊆ {p : E | f p ≤ U} := hS
  exact convexHull_min hsub hc

/-- The signed filtering identity used in Lemma 4.4, AFTER the Born-rule
pullback and positivity/normalization of the two branches have been established. -/
theorem filtering_average (p pp pm qp qm ε s : ℝ)
    (hp : qp * pp = (1 + ε * s) * p)
    (hm : qm * pm = (1 - ε * s) * p) :
    qp / 2 * pp + qm / 2 * pm = p := by
  nlinarith [hp, hm]

/-- Scalar part of the binary spectral decomposition in Theorem 4.2. -/
theorem binary_spectral_weights (μ lam : ℝ)
    (hμ : 0 ≤ μ) (hμlam : μ ≤ lam) (hlam : lam ≤ 1) :
    0 ≤ lam - μ ∧ 0 ≤ μ ∧ 0 ≤ 1 - lam ∧
      (lam - μ) + μ + (1 - lam) = 1 := by
  constructor
  · linarith
  constructor
  · exact hμ
  constructor <;> linarith

end Bell
