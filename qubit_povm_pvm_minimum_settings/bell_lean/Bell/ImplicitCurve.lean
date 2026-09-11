import Bell.IncidenceAlgebra
import Mathlib.Analysis.Calculus.Implicit
import Mathlib.Analysis.Calculus.Deriv.Slope
import Mathlib.Analysis.Calculus.Deriv.Comp
import Mathlib.Analysis.Calculus.Deriv.Mul

/-!
# First-order feasible curves and exact quadratic score improvement

Only the first-order implicit-function theorem is used. The exact finite score
gap from `IncidenceAlgebra` replaces the usual second-derivative argument.
-/
noncomputable section
open scoped Bell.Entrywise
open Filter Set
open scoped Topology BigOperators Matrix
namespace Bell

/-- Every vector in the kernel of a surjective strict derivative is realized
by a once-differentiable curve in the level set, near parameter zero. -/
theorem exists_level_curve
    {E F : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [NormedAddCommGroup F] [NormedSpace ℝ F] [FiniteDimensional ℝ F]
    (f : E → F) (D : E →L[ℝ] F) (a v : E)
    (hf : HasStrictFDerivAt f D a) (hD : LinearMap.range D = ⊤) (hv : D v = 0) :
    ∃ γ : ℝ → E, γ 0 = a ∧ HasDerivAt γ v 0 ∧
      ∀ᶠ t in 𝓝 (0 : ℝ), f (γ t) = f a := by
  let w : LinearMap.ker D := ⟨v, hv⟩
  let Φ := hf.implicitFunction f D hD (f a)
  let γ : ℝ → E := fun t => Φ (t • w)
  have hφ : HasFDerivAt Φ (LinearMap.ker D).subtypeL 0 :=
    (hf.to_implicitFunction hD).hasFDerivAt
  have ht : HasDerivAt (fun t : ℝ => t • w) w 0 := by
    simpa using (hasDerivAt_id (0 : ℝ)).smul_const w
  have hγ : HasDerivAt γ v 0 := by
    simpa only [γ, zero_smul, Submodule.subtypeL_apply, w] using
      hφ.comp_hasDerivAt_of_eq 0 ht (zero_smul ℝ w).symm
  refine ⟨γ, ?_, hγ, ?_⟩
  · simp [γ, Φ, hf.implicitFunction_apply_image hD]
  · have htend : Tendsto (fun t : ℝ => (f a, t • w)) (𝓝 0) (𝓝 (f a, 0)) := by
      simpa using tendsto_const_nhds.prodMk_nhds ht.continuousAt.tendsto
    exact htend.eventually (hf.map_implicitFunction_eq hD)

namespace Lorentz

/-- Weighted Gram evaluation is a polynomial in both of its matrix arguments. -/
theorem continuous_weightedGram (lam : Fin 5 → ℝ) :
    Continuous (fun p : M × M => weightedGram lam p.1 p.2) := by
  simp only [weightedGram, matrixPair_apply, Matrix.mulVec, dotProduct]
  fun_prop

/-- The scaled score difference along a C¹ chart curve has the expected
quadratic limit. No second differentiability premise appears. -/
theorem quadratic_gap_limit
    (γ : ℝ → IncidenceSpace) (z : IncidenceSpace) (v : IncidenceSpace)
    (hzero : γ 0 = z) (hγ : HasDerivAt γ v 0) (lam : Fin 5 → ℝ) :
    Tendsto (fun t : ℝ =>
      weightedGram lam (chartMetric (γ t).1) (t⁻¹ • ((γ t).2 - z.2)))
      (𝓝[≠] (0 : ℝ)) (𝓝 (weightedGram lam (chartMetric z.1) v.2)) := by
  have hy : HasDerivAt (fun t => (γ t).2) v.2 0 := hγ.snd
  have hs : Tendsto (fun t : ℝ => t⁻¹ • ((γ t).2 - z.2))
      (𝓝[≠] 0) (𝓝 v.2) := by
    simpa only [zero_add, hzero] using hy.tendsto_slope_zero
  have hg : Tendsto (fun t => chartMetric (γ t).1)
      (𝓝[≠] (0 : ℝ)) (𝓝 (chartMetric z.1)) := by
    have hc : Continuous chartMetric := by
      have heq : chartMetric = fun p => chartMetric 0 + metricVariation p := by
        funext p
        simpa using chartMetric_add 0 p
      rw [heq]
      exact continuous_const.add metricVariation.toContinuousLinearMap.continuous
    have ht := hc.continuousAt.tendsto.comp hγ.continuousAt.fst.tendsto
    simpa only [hzero] using ht.mono_left nhdsWithin_le_nhds
  have hpair := hg.prodMk_nhds hs
  have hcomp := ((continuous_weightedGram lam).tendsto (chartMetric z.1, v.2)).comp hpair
  exact hcomp

/-- A positive limiting quadratic form gives strict improvement at all
sufficiently small nonzero parameters of a feasible C¹ curve. -/
theorem eventually_score_improvement
    (γ : ℝ → IncidenceSpace) (z v : IncidenceSpace)
    (hzero : γ 0 = z) (hγ : HasDerivAt γ v 0)
    (hz : FeasibleIncidence z)
    (hfeasible : ∀ᶠ t in 𝓝 (0 : ℝ), FeasibleIncidence (γ t))
    (lam : Fin 5 → ℝ) (F : M →ₗ[ℝ] ℝ) (α : ℝ)
    (stationary : ∀ P, F P = α * blockMass P - 2 * weightedPairing lam z.2 P)
    (metricStationary : ∀ h, weightedGram lam (metricVariation h) z.2 = 0)
    (hpositive : 0 < weightedGram lam (chartMetric z.1) v.2) :
    ∀ᶠ t in 𝓝[≠] (0 : ℝ), F (probabilityBlock z) < F (probabilityBlock (γ t)) := by
  have hlim := quadratic_gap_limit γ z v hzero hγ lam
  have hpos : ∀ᶠ t in 𝓝[≠] (0 : ℝ),
      0 < weightedGram lam (chartMetric (γ t).1) (t⁻¹ • ((γ t).2 - z.2)) :=
    hlim.eventually (Ioi_mem_nhds hpositive)
  filter_upwards [hpos, hfeasible.filter_mono nhdsWithin_le_nhds,
    self_mem_nhdsWithin] with t ht hft hne
  have heq := polynomial_score_gap z (γ t) lam F α hz hft stationary metricStationary
  rw [weightedGram_smul_frame] at ht
  have hgram : 0 < weightedGram lam (chartMetric (γ t).1) ((γ t).2 - z.2) := by
    by_contra! hn
    exact (not_lt_of_ge (mul_nonpos_of_nonneg_of_nonpos (sq_nonneg _) hn)) ht
  linarith

/-- A local maximum on the feasible set cannot possess an uphill feasible C¹
curve. The curve only needs to satisfy the equations near zero. -/
theorem not_local_max_of_uphill_curve
    (γ : ℝ → IncidenceSpace) (z v : IncidenceSpace)
    (hzero : γ 0 = z) (hγ : HasDerivAt γ v 0)
    (hz : FeasibleIncidence z)
    (hfeasible : ∀ᶠ t in 𝓝 (0 : ℝ), FeasibleIncidence (γ t))
    (lam : Fin 5 → ℝ) (F : M →ₗ[ℝ] ℝ) (α : ℝ)
    (stationary : ∀ P, F P = α * blockMass P - 2 * weightedPairing lam z.2 P)
    (metricStationary : ∀ h, weightedGram lam (metricVariation h) z.2 = 0)
    (hpositive : 0 < weightedGram lam (chartMetric z.1) v.2) :
    ¬ IsLocalMaxOn (fun w => F (probabilityBlock w))
      {w | FeasibleIncidence w} z := by
  intro hmax
  have hup := eventually_score_improvement γ z v hzero hγ hz hfeasible
    lam F α stationary metricStationary hpositive
  have htend : Tendsto γ (𝓝 (0 : ℝ)) (𝓝 z) := by
    simpa [hzero] using hγ.continuousAt.tendsto
  have htendOn : Tendsto γ (𝓝 (0 : ℝ)) (𝓝[{w | FeasibleIncidence w}] z) :=
    tendsto_nhdsWithin_iff.mpr ⟨htend, hfeasible⟩
  have hdown : ∀ᶠ t in 𝓝 (0 : ℝ),
      F (probabilityBlock (γ t)) ≤ F (probabilityBlock z) := htendOn.eventually hmax
  have hfalse : ∀ᶠ t in 𝓝[≠] (0 : ℝ), False := by
    filter_upwards [hup, hdown.filter_mono nhdsWithin_le_nhds] with t hu hd
    exact (not_lt_of_ge hd) hu
  exact Filter.Eventually.exists hfalse |>.elim fun _ h => h

end Lorentz
end Bell
