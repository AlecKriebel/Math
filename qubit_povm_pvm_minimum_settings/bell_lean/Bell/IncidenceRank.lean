import Bell.FiniteLinearAlgebra
import Bell.IncidenceDifferential
import Bell.IncidenceStationarity
import Bell.ImplicitCurve
import Bell.IncidenceScores
import Bell.RankOne

/-!
# Exhaustive rank analysis of the regular incidence problem

The high-rank branch derives a compatible metric increment and then corrects
the FULL normalization differential, including its metric term. It does not
mistake the W-only normalization for the physical normalization.

The once-differentiable feasible curve is produced by the implicit-function
theorem with the explicitly surjective derivative from IncidenceDifferential.
-/
noncomputable section
open scoped Bell.Entrywise
open scoped BigOperators Matrix Topology
namespace Bell.Lorentz

/-- An invertible coefficient frame as a linear equivalence. -/
def frameEquiv (Y : M) (hY : IsUnit Y.det) : V ≃ₗ[ℝ] V where
  toLinearMap := linearOfMatrix Y
  invFun := fun x => Y⁻¹ *ᵥ x
  left_inv := by
    intro x
    simp only [linearOfMatrix_apply, Matrix.mulVec_mulVec,
      Matrix.nonsing_inv_mul Y hY, Matrix.one_mulVec]
  right_inv := by
    intro x
    simp only [linearOfMatrix_apply, Matrix.mulVec_mulVec,
      Matrix.mul_nonsing_inv Y hY, Matrix.one_mulVec]

@[simp]
theorem frameEquiv_apply (Y : M) (hY : IsUnit Y.det) (x : V) :
    frameEquiv Y hY x = Y *ᵥ x := rfl

/-- The actual rank of the four-column metric differential. -/
def incidenceRank (Y : M) : ℕ := Module.finrank ℝ (LinearMap.range (nullRowMap Y))

theorem kernel_dimension_le_three (Y : M) (hr : 2 ≤ incidenceRank Y) :
    Module.finrank ℝ (LinearMap.ker (nullRowMap Y)) ≤ 3 := by
  have hd := (nullRowMap Y).finrank_range_add_finrank_ker
  change incidenceRank Y + Module.finrank ℝ (LinearMap.ker (nullRowMap Y)) =
    Module.finrank ℝ (Fin 5 → ℝ) at hd
  norm_num at hd
  omega

/-- A basis of the actual multiplier kernel supplies the at-most-three
compatibility constraints; annihilation on the basis implies annihilation on
all of the kernel. -/
theorem uphill_annihilating_kernel (G Y : M)
    (v : V) (hv : 0 < pullbackForm G (linearOfMatrix Y) v v)
    (λ : Fin 5 → ℝ) (hλ : ∀ j, 0 < λ j)
    (hr : 2 ≤ incidenceRank Y) :
    ∃ W : Endomorphism,
      0 < weightedSecondForm (pullbackForm G (linearOfMatrix Y)) λ W ∧
      ∀ μ, nullRowMap Y μ = 0 →
        compatibility (pullbackForm G (linearOfMatrix Y)) μ W = 0 := by
  let K := LinearMap.ker (nullRowMap Y)
  let b := FiniteDimensional.finBasis ℝ K
  let μ := fun i => (b i).val
  obtain ⟨W, hW, hcomp⟩ := uphill_of_three_compatibilities
    (kernel_dimension_le_three Y hr) (pullbackForm G (linearOfMatrix Y)) v hv λ hλ μ
  refine ⟨W, hW, ?_⟩
  intro ν hν
  let k : K := ⟨ν, hν⟩
  have hrepr : ν = ∑ i, b.repr k i • μ i := by
    have hb := congrArg (fun x : K => x.val) (b.sum_repr k)
    simpa only [Submodule.coe_sum, Submodule.coe_smul, μ, k] using hb.symm
  rw [hrepr, compatibility_sum]
  simp [hcomp]

theorem weightedGram_frame_action (λ : Fin 5 → ℝ) (G Y : M) (W : Endomorphism) :
    weightedGram λ G (Y * matrixOfLinear W) =
      weightedSecondForm (pullbackForm G (linearOfMatrix Y)) λ W := by
  simp [weightedGram, weightedSecondForm, pullbackForm,
    Matrix.mulVec_mulVec, matrixOfLinear_mulVec]

/-- The complete normalized tangent, with the metric contribution included. -/
theorem exists_positive_normalized_tangent (z : IncidenceSpace)
    (hz : FeasibleIncidence z) (hinv : IsUnit (probabilityBlock z).det)
    (λ : Fin 5 → ℝ) (hλ : ∀ j, 0 < λ j)
    (hstationary : nullRowMap z.2 λ = 0) (hr : 2 ≤ incidenceRank z.2) :
    ∃ d : IncidenceSpace, constraintDerivativeCLM z d = 0 ∧
      0 < weightedGram λ (chartMetric z.1) d.2 := by
  let G := chartMetric z.1
  let Y := z.2
  let B := pullbackForm G (linearOfMatrix Y)
  have hY := frame_invertible_of_block z hinv
  let v : V := Y⁻¹ *ᵥ unitVector
  have hYv : Y *ᵥ v = unitVector := by
    simp [v, Matrix.mulVec_mulVec, Matrix.mul_nonsing_inv Y hY]
  have hv : 0 < B v v := by
    change 0 < matrixPair G (Y *ᵥ v) (Y *ᵥ v)
    rw [hYv, chartMetric_unit]
    norm_num
  obtain ⟨W, hW, hcomp⟩ := uphill_annihilating_kernel G Y v hv λ hλ hr
  obtain ⟨h, hh⟩ := exists_compatible_metric G Y W hcomp
  let d₀ : IncidenceSpace := (h, Y * matrixOfLinear W)
  have hn₀ : nullDerivative z d₀ = 0 := by
    funext j
    rw [nullDerivative_symmetric]
    simpa only [d₀, Prod.fst_mk, Prod.snd_mk, Matrix.mulVec_mulVec,
      matrixOfLinear_mulVec] using hh j
  let t := -massDerivative z d₀
  let d := d₀ + t • (0, Y)
  refine ⟨d, ?_, ?_⟩
  · change constraintDerivative z (d₀ + t • (0, Y)) = 0
    rw [map_add, map_smul, constraintDerivative_radial z hz]
    apply Prod.ext
    · simpa [constraintDerivative] using hn₀
    · simp [constraintDerivative, t]
  · have hnull : ∀ j, B (ray j) (ray j) = 0 := by
      intro j
      exact congrFun hz.1 j
    have hB : ∀ x y, B x y = B y x := by
      intro x y
      exact matrixPair_symmetric (chartMetric_symmetric z.1) _ _
    have hλcomp : compatibility B λ W = 0 := hcomp λ hstationary
    have hd₂ : d.2 = Y * matrixOfLinear (W + t • LinearMap.id) := by
      simp only [d, d₀, Prod.snd_add, Prod.snd_smul, Prod.snd_mk,
        matrixOfLinear_add, matrixOfLinear_smul, matrixOfLinear_id,
        Matrix.mul_add, Matrix.mul_smul, mul_one]
    rw [hd₂, weightedGram_frame_action,
      secondForm_add_identity B hB λ W t hnull, hλcomp, mul_zero, add_zero]
    exact hW

/-- The high-rank local-maximum exclusion is now a theorem about the actual
polynomial constraints, not an abstract positive quadratic direction. -/
theorem high_rank_not_local_max (z : IncidenceSpace) (F : M →ₗ[ℝ] ℝ)
    (hz : FeasibleIncidence z) (hinv : IsUnit (probabilityBlock z).det)
    (α : ℝ) (λ : Fin 5 → ℝ) (hλ : ∀ j, 0 < λ j)
    (stationary : ∀ P, F P = α * blockMass P - 2 * weightedPairing λ z.2 P)
    (metricStationary : ∀ h, weightedGram λ (metricVariation h) z.2 = 0)
    (hr : 2 ≤ incidenceRank z.2) :
    ¬ IsLocalMaxOn (fun w => F (probabilityBlock w)) {w | FeasibleIncidence w} z := by
  have hλker := (metric_stationary_iff z.2 λ).mp metricStationary
  obtain ⟨d, hd, hpositive⟩ := exists_positive_normalized_tangent z hz hinv λ hλ hλker hr
  obtain ⟨γ, hzero, hγ, hlevel⟩ := exists_level_curve incidenceConstraints
    (constraintDerivativeCLM z) z d (incidenceConstraints_hasStrictFDerivAt z)
    (constraintDerivative_range z hz hinv) hd
  have hfeasible : ∀ᶠ t in 𝓝 (0 : ℝ), FeasibleIncidence (γ t) :=
    hlevel.mono fun t ht => (feasible_iff_constraints_eq z (γ t) hz).mpr ht
  exact not_local_max_of_uphill_curve γ z d hzero hγ hz hfeasible
    λ F α stationary metricStationary hpositive

/-- A zero-dimensional row image means that every row vanishes. -/
theorem rank_zero_rows (Y : M) (hr : incidenceRank Y = 0) :
    ∀ j, phi (Y *ᵥ ray j) = 0 := by
  have hbot : LinearMap.range (nullRowMap Y) = ⊥ := Submodule.finrank_eq_zero.mp hr
  intro j
  have hm : phi (Y *ᵥ ray j) ∈ LinearMap.range (nullRowMap Y) :=
    ⟨Pi.single j 1, nullRowMap_single Y j⟩
  rw [hbot] at hm
  exact hm

/-- In rank one every row has explicit coordinates on one nonzero generator.
The nonzero row condition follows from rank one rather than being assumed. -/
theorem rank_one_row_coordinates (Y : M) (hr : incidenceRank Y = 1) :
    ∃ (ξ : V) (c : Fin 5 → ℝ), ξ ≠ 0 ∧ (∃ j, c j ≠ 0) ∧
      ∀ j, phi (Y *ᵥ ray j) = c j • ξ := by
  let R := LinearMap.range (nullRowMap Y)
  let b : Basis PUnit ℝ R := Module.basisUnique PUnit hr
  let ξ : V := (b PUnit.unit).val
  have hξ : ξ ≠ 0 := by
    intro h
    exact b.ne_zero PUnit.unit (Subtype.ext h)
  let row : Fin 5 → R := fun j => ⟨phi (Y *ᵥ ray j), ⟨Pi.single j 1, nullRowMap_single Y j⟩⟩
  let c : Fin 5 → ℝ := fun j => b.repr (row j) PUnit.unit
  have hrows : ∀ j, phi (Y *ᵥ ray j) = c j • ξ := by
    intro j
    have hj := congrArg (fun v : R => v.val) (b.sum_repr (row j))
    simpa [row, c, ξ] using hj.symm
  refine ⟨ξ, c, hξ, ?_, hrows⟩
  by_contra! hall
  have hmap : nullRowMap Y = 0 := by
    ext μ i
    simp [nullRowMap, hrows, hall]
  have hr0 : incidenceRank Y = 0 := by simp [incidenceRank, hmap]
  omega

/-- Rank one is excluded by the proved projective-fiber theorem. -/
theorem rank_one_stationarity_impossible (g : StrictParameters) (Y : M)
    (hY : IsUnit Y.det) (λ : Fin 5 → ℝ) (hλ : ∀ j, 0 < λ j)
    (hnull : ∀ j, nullPolynomial g.a g.b g.c g.d (Y *ᵥ ray j) = 0)
    (hstationary : nullRowMap Y λ = 0) (hr : incidenceRank Y = 1) : False := by
  obtain ⟨ξ, c, hξ, hlive, hrows⟩ := rank_one_row_coordinates Y hr
  exact transformed_rank_one_obstruction g (frameEquiv Y hY) λ c ξ
    hnull hλ hξ hlive hrows hstationary

/-- The strict metric parameters as a four-vector. -/
def parameterVector (g : StrictParameters) : V := ![g.a, g.b, g.c, g.d]

@[simp]
theorem chartMetric_parameterVector (g : StrictParameters) :
    chartMetric (parameterVector g) = metric g.a g.b g.c g.d := rfl

theorem timeFunctional_eq_matrixPair (g : StrictParameters) (x : V) :
    timeFunctional g x = matrixPair (metric g.a g.b g.c g.d) unitVector x := by
  simp [timeFunctional, matrixPair, metric, unitVector, dotProduct,
    Matrix.mulVec, Fin.sum_univ_succ]
  ring

/-- Rank-zero simulation in the same matrix convention used by the calculus. -/
theorem rank_zero_block_mem (g : StrictParameters) (Y : M) (hY : IsUnit Y.det)
    (hnull : ∀ j, nullPolynomial g.a g.b g.c g.d (Y *ᵥ ray j) = 0)
    (hfuture : ∀ j, 0 < timeFunctional g (Y *ᵥ ray j))
    (hnormal : blockMass (metric g.a g.b g.c g.d * Y) = 1)
    (hr : incidenceRank Y = 0) :
    tableOfBlock (metric g.a g.b g.c g.d * Y) ∈ convexPVM binaryTernaryArchitecture := by
  let T := frameEquiv Y hY
  have hrep : matrixOfLinear T.toLinearMap = Y := by
    ext i j
    simp [matrixOfLinear, T]
  have hmass : timeFunctional g (T unitVector) = 1 := by
    rw [timeFunctional_eq_matrixPair]
    simpa [blockMass, matrixPair, T, Matrix.mulVec_mulVec] using hnormal
  have hm := rank_zero_transformed_table_mem g T hnull (rank_zero_rows Y hr) hfuture hmass
  rw [← tableOfBlock_eq_transformedMetricTable, hrep] at hm
  exact hm

end Bell.Lorentz
