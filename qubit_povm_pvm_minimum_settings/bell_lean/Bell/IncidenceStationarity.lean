import Bell.IncidenceDifferential
import Bell.FiniteLinearAlgebra
import Mathlib.Analysis.Calculus.LagrangeMultipliers

/-!
# Incidence stationarity derived from a genuine constrained local maximum

The normalization multiplier is proved nonzero using the explicit surjectivity
of the constraint derivative. The two incidence stationarity identities are
then derived from metric-only and frame-only variations. Neither identity is
assumed in the main theorem of this file.
-/
noncomputable section
open scoped Bell.Entrywise
open scoped BigOperators Matrix Topology
namespace Bell

/-- The ordinary Lagrange functional, with its objective coefficient normalized
to one. Surjectivity excludes the abnormal multiplier case. -/
theorem exists_normalized_lagrange
    {E F : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
    (f : E → F) (φ : E → ℝ) (D : E →L[ℝ] F) (dφ : E →L[ℝ] ℝ) (a : E)
    (hf : HasStrictFDerivAt f D a) (hφ : HasStrictFDerivAt φ dφ a)
    (hsurj : Function.Surjective D)
    (hmax : IsLocalMaxOn φ {x | f x = f a} a) :
    ∃ l : F →ₗ[ℝ] ℝ, ∀ v, dφ v = l (D v) := by
  have hext : IsLocalExtrOn φ {x | f x = f a} a := Or.inr hmax
  obtain ⟨L, c, hnonzero, hL⟩ :=
    hext.exists_linear_map_of_hasStrictFDerivAt hf hφ
  have hc : c ≠ 0 := by
    intro hc
    have hLzero : L = 0 := by
      ext y
      obtain ⟨v, rfl⟩ := hsurj y
      have hv := hL v
      simpa [hc] using hv
    exact hnonzero (by simp [hc, hLzero])
  refine ⟨(-c⁻¹) • L, fun v => ?_⟩
  have hv := hL v
  simp only [smul_eq_mul] at hv
  change dφ v = (-c⁻¹) * L (D v)
  field_simp [hc]
  nlinarith

namespace Lorentz

/-- Coordinates of a functional on the five null values and one mass value. -/
theorem constraint_functional_coordinates (l : ConstraintSpace →ₗ[ℝ] ℝ)
    (v : Fin 5 → ℝ) (n : ℝ) :
    l (v, n) = (∑ j, l (Pi.single j 1, 0) * v j) + l (0, 1) * n := by
  have hvec : (∑ j : Fin 5, v j • ((Pi.single j 1, 0) : ConstraintSpace)) +
      n • ((0, 1) : ConstraintSpace) = (v, n) := by
    apply Prod.ext
    · funext i
      fin_cases i <;> simp [Fin.sum_univ_succ, Pi.single_apply]
    · simp [Fin.sum_univ_succ]
  calc
    l (v, n) = l ((∑ j : Fin 5, v j • ((Pi.single j 1, 0) : ConstraintSpace)) +
        n • ((0, 1) : ConstraintSpace)) := congrArg l hvec.symm
    _ = _ := by
      simp only [map_add, map_sum, map_smul, smul_eq_mul]
      simp [mul_comm]

theorem feasible_iff_constraints_eq (z w : IncidenceSpace) (hz : FeasibleIncidence z) :
    FeasibleIncidence w ↔ incidenceConstraints w = incidenceConstraints z := by
  simp only [FeasibleIncidence, incidenceConstraints, Prod.mk.injEq, hz.1, hz.2]

/-- All six multipliers of the polynomial constraints, with their paper sign. -/
def IncidenceLagrangeEquation (z : IncidenceSpace) (F : M →ₗ[ℝ] ℝ)
    (α : ℝ) (lam : Fin 5 → ℝ) : Prop :=
  ∀ d, F (blockDerivative z d) = α * massDerivative z d -
    ∑ j, lam j * nullDerivative z d j

/-- Existence is deduced from the local-maximum hypothesis and the actual
polynomial derivative. No stationarity oracle is an argument. -/
theorem exists_incidence_lagrange (z : IncidenceSpace) (F : M →ₗ[ℝ] ℝ)
    (hz : FeasibleIncidence z) (hinv : IsUnit (probabilityBlock z).det)
    (hmax : IsLocalMaxOn (fun w => F (probabilityBlock w))
      {w | FeasibleIncidence w} z) :
    ∃ α lam, IncidenceLagrangeEquation z F α lam := by
  let dF : IncidenceSpace →L[ℝ] ℝ :=
    F.toContinuousLinearMap.comp (blockDerivative z).toContinuousLinearMap
  have hF : HasStrictFDerivAt (fun w => F (probabilityBlock w)) dF z :=
    F.toContinuousLinearMap.hasStrictFDerivAt.comp z (probabilityBlock_hasStrictFDerivAt z)
  have hmax' : IsLocalMaxOn (fun w => F (probabilityBlock w))
      {w | incidenceConstraints w = incidenceConstraints z} z := by
    convert hmax using 1
    ext w
    exact (feasible_iff_constraints_eq z w hz).symm
  obtain ⟨l, hl⟩ := exists_normalized_lagrange incidenceConstraints
    (fun w => F (probabilityBlock w)) (constraintDerivativeCLM z) dF z
    (incidenceConstraints_hasStrictFDerivAt z) hF
    (constraintDerivative_surjective z hz hinv) hmax'
  refine ⟨l (0, 1), fun j => -l (Pi.single j 1, 0), ?_⟩
  intro d
  have hd := hl d
  change F (blockDerivative z d) = l (nullDerivative z d, massDerivative z d) at hd
  rw [hd, constraint_functional_coordinates]
  simp only [neg_mul, Finset.sum_neg_distrib]
  ring

theorem lagrange_frame_variations (z : IncidenceSpace) (F : M →ₗ[ℝ] ℝ)
    (α : ℝ) (lam : Fin 5 → ℝ) (hL : IncidenceLagrangeEquation z F α lam) (Z : M) :
    F (chartMetric z.1 * Z) = α * blockMass (chartMetric z.1 * Z) -
      2 * weightedCross lam (chartMetric z.1) z.2 Z := by
  have h := hL (0, Z)
  simp only [blockDerivative, massDerivative, LinearMap.comp_apply, map_zero, zero_mul, zero_add] at h
  simp_rw [nullDerivative_symmetric] at h
  simpa [weightedCross, Finset.mul_sum, mul_assoc, mul_left_comm] using h

theorem lagrange_metric_variations (z : IncidenceSpace) (F : M →ₗ[ℝ] ℝ)
    (α : ℝ) (lam : Fin 5 → ℝ) (hL : IncidenceLagrangeEquation z F α lam) (h : V) :
    F (metricVariation h * z.2) = α * blockMass (metricVariation h * z.2) -
      weightedGram lam (metricVariation h) z.2 := by
  have hh := hL (h, 0)
  simp_rw [nullDerivative_symmetric] at hh
  simpa [blockDerivative, massDerivative, weightedGram] using hh

theorem metric_invertible_of_block (z : IncidenceSpace)
    (hinv : IsUnit (probabilityBlock z).det) : IsUnit (chartMetric z.1).det := by
  apply isUnit_iff_ne_zero.mpr
  intro hzero
  have hb : (probabilityBlock z).det = 0 := by
    simp [probabilityBlock, Matrix.det_mul, hzero]
  exact (isUnit_iff_ne_zero.mp hinv) hb

theorem frame_invertible_of_block (z : IncidenceSpace)
    (hinv : IsUnit (probabilityBlock z).det) : IsUnit z.2.det := by
  apply isUnit_iff_ne_zero.mpr
  intro hzero
  have hb : (probabilityBlock z).det = 0 := by
    simp [probabilityBlock, Matrix.det_mul, hzero]
  exact (isUnit_iff_ne_zero.mp hinv) hb

/-- Recover the stationarity formula on arbitrary probability-block increments. -/
theorem lagrange_block_stationarity (z : IncidenceSpace) (F : M →ₗ[ℝ] ℝ)
    (α : ℝ) (lam : Fin 5 → ℝ) (hL : IncidenceLagrangeEquation z F α lam)
    (hg : IsUnit (chartMetric z.1).det) :
    ∀ P, F P = α * blockMass P - 2 * weightedPairing lam z.2 P := by
  intro P
  have h := lagrange_frame_variations z F α lam hL ((chartMetric z.1)⁻¹ * P)
  rw [← weightedPairing_mul,
    Matrix.mul_nonsing_inv_cancel_left (chartMetric z.1) P hg] at h
  exact h

/-- Metric stationarity follows by comparing metric-only and compensating
frame-only variations. It is not a separate optimization premise. -/
theorem lagrange_metric_stationarity (z : IncidenceSpace) (F : M →ₗ[ℝ] ℝ)
    (α : ℝ) (lam : Fin 5 → ℝ) (hL : IncidenceLagrangeEquation z F α lam)
    (hg : IsUnit (chartMetric z.1).det) :
    ∀ h, weightedGram lam (metricVariation h) z.2 = 0 := by
  intro h
  have hm := lagrange_metric_variations z F α lam hL h
  have hb := lagrange_block_stationarity z F α lam hL hg (metricVariation h * z.2)
  rw [weightedPairing_mul, weightedCross_self] at hb
  linarith

/-- Both stationarity identities, entirely derived at a regular feasible local
maximum of the concrete polynomial incidence problem. -/
theorem exists_incidence_stationarity (z : IncidenceSpace) (F : M →ₗ[ℝ] ℝ)
    (hz : FeasibleIncidence z) (hinv : IsUnit (probabilityBlock z).det)
    (hmax : IsLocalMaxOn (fun w => F (probabilityBlock w))
      {w | FeasibleIncidence w} z) :
    ∃ (α : ℝ) (lam : Fin 5 → ℝ),
      (∀ P, F P = α * blockMass P - 2 * weightedPairing lam z.2 P) ∧
      (∀ h, weightedGram lam (metricVariation h) z.2 = 0) := by
  obtain ⟨α, lam, hL⟩ := exists_incidence_lagrange z F hz hinv hmax
  have hg := metric_invertible_of_block z hinv
  exact ⟨α, lam, lagrange_block_stationarity z F α lam hL hg,
    lagrange_metric_stationarity z F α lam hL hg⟩

end Lorentz
end Bell
