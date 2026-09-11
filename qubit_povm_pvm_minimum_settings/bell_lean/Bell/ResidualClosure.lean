import Bell.GramLift
import Bell.IncidenceRank

/-!
# Physical closure of the genuine binary–ternary stratum

All three rank cases now start from an actual global maximum over complex-qubit
strategies. The local-incidence maximum, stationarity, positive multipliers,
implicit physical curve, and rank-zero PVM mixture are derived in this file's
proof chain. Its remaining inputs are concrete geometric properties of the
residual frame, not any optimization or local-realizability conclusion.
-/
noncomputable section
open scoped Bell.Entrywise
open scoped BigOperators Matrix Topology
namespace Bell.Lorentz
open QubitGeometry

theorem frame_future_pairing (E : M) (z : IncidenceSpace)
    (hGram : frameGram E = chartMetric z.1)
    (hz : FeasibleIncidence z) (hpos : FramePositive E z.2) :
    ∀ j, 0 < matrixPair (chartMetric z.1) (z.2 *ᵥ ray j) (z.2 *ᵥ unitVector) := by
  intro j
  have hj : FutureNull (E *ᵥ (z.2 *ᵥ ray j)) := by
    refine ⟨hpos.2.1 j, ?_⟩
    rw [← lorentzPair_self, ← frameGram_pair, hGram]
    exact congrFun hz.1 j
  have hu : FutureTimelike (E *ᵥ (z.2 *ᵥ unitVector)) := by
    refine ⟨?_, ?_⟩
    · have hunit : E *ᵥ (z.2 *ᵥ unitVector) =
          E *ᵥ (z.2 *ᵥ ray 0) + E *ᵥ (z.2 *ᵥ ray 1) := by
        rw [← binary_circuit]
        simp only [Matrix.mulVec_add]
      rw [hunit]
      exact add_pos (hpos.2.1 0) (hpos.2.1 1)
    · rw [← lorentzPair_self, ← frameGram_pair]
      exact hpos.2.2
  rw [← hGram, frameGram_pair]
  exact timelike_pair_positive hj hu

/-- Future orientation of the transformed rays in the metric convention used
by the independently implemented rank-zero simulator. -/
theorem frame_timeFunctional_positive (g : StrictParameters) (E Y : M)
    (hGram : frameGram E = metric g.a g.b g.c g.d)
    (hunit : E *ᵥ unitVector = timeUnit)
    (hpos : ∀ j, 0 < (E *ᵥ (Y *ᵥ ray j)) 0) :
    ∀ j, 0 < timeFunctional g (Y *ᵥ ray j) := by
  intro j
  rw [timeFunctional_eq_matrixPair, ← hGram, frameGram_pair, hunit]
  simpa [lorentzPair, timeUnit] using hpos j

/-- A normalized genuine residual frame cannot attain a global POVM maximum
strictly above the complete, shared-randomness PVM support function. -/
theorem no_strict_residual_maximum
    (g : StrictParameters) (E Y : M)
    (hE : IsUnit E.det) (hY : IsUnit Y.det)
    (hGram : frameGram E = metric g.a g.b g.c g.d)
    (hunit : E *ᵥ unitVector = timeUnit)
    (hz : FeasibleIncidence (parameterVector g, Y))
    (hpos : FramePositive E Y)
    (f : Behavior binaryTernaryArchitecture →ₗ[ℝ] ℝ)
    (hmax : ∀ q ∈ rawPOVM binaryTernaryArchitecture,
      f q ≤ f (tableOfBlock (metric g.a g.b g.c g.d * Y)))
    (hstrict : ∀ q ∈ convexPVM binaryTernaryArchitecture,
      f q < f (tableOfBlock (metric g.a g.b g.c g.d * Y))) : False := by
  let z : IncidenceSpace := (parameterVector g, Y)
  let F : M →ₗ[ℝ] ℝ := f.comp tableOfBlock
  have hg : IsUnit (metric g.a g.b g.c g.d).det := by
    rw [← hGram, frameGram, Matrix.det_mul, Matrix.det_mul, Matrix.det_transpose]
    have hJ : IsUnit minkowski.det := by
      have hd := congrArg Matrix.det minkowski_square
      rw [Matrix.det_mul, Matrix.det_one] at hd
      apply isUnit_iff_ne_zero.mpr
      intro hzero
      simp [hzero] at hd
    exact (hE.mul hJ).mul hE
  have hinv : IsUnit (probabilityBlock z).det := by
    change IsUnit (metric g.a g.b g.c g.d * Y).det
    rw [Matrix.det_mul]
    exact hg.mul hY
  have hlocal : IsLocalMaxOn (fun w => F (probabilityBlock w))
      {w | FeasibleIncidence w} z :=
    physical_maximum_is_incidence_maximum E z hE hGram hpos f hmax
  obtain ⟨α, λ, hstationary, hmetric⟩ := exists_incidence_stationarity z F hz hinv hlocal
  have hphysical := frame_table_mem_rawPOVM E z hGram hz hpos
  obtain ⟨s, hs⟩ := hphysical
  have hnull : ∀ j, matrixPair (metric g.a g.b g.c g.d)
      (Y *ᵥ ray j) (Y *ᵥ ray j) = 0 := fun j => congrFun hz.1 j
  have hλ : ∀ j, 0 < λ j :=
    multipliers_positive_from_physical_separator s (metric g.a g.b g.c g.d) Y
      hs λ α hnull (frame_future_pairing E z hGram hz hpos) f hstationary
      (by simpa only [hs] using hstrict)
  have hker : nullRowMap Y λ = 0 := (metric_stationary_iff Y λ).mp hmetric
  have hpoly : ∀ j, nullPolynomial g.a g.b g.c g.d (Y *ᵥ ray j) = 0 := by
    intro j
    have hj := hnull j
    simpa only [matrixPair_apply, metric_quadratic] using hj
  by_cases hzero : incidenceRank Y = 0
  · have hm := rank_zero_block_mem g Y hY hpoly
      (frame_timeFunctional_positive g E Y hGram hunit hpos.2.1) hz.2 hzero
    exact (lt_irrefl _ (hstrict _ hm))
  by_cases hone : incidenceRank Y = 1
  · exact rank_one_stationarity_impossible g Y hY λ hλ hpoly hker hone
  · have hr : 2 ≤ incidenceRank Y := by omega
    exact high_rank_not_local_max z F hz hinv α λ hλ hstationary hmetric hr hlocal

end Bell.Lorentz
