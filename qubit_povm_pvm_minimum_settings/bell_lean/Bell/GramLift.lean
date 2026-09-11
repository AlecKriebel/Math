import Bell.FrameRealization
import Mathlib.Analysis.Calculus.Implicit

/-!
# Local physical reconstruction without a smooth spinor or square-root choice

The real Gram map E ↦ Eᵀ J E is a submersion at every invertible E. Its derivative
has the explicit right inverse H ↦ (1/2) J E⁻ᵀ H. The first-order implicit-function
theorem supplies a continuous local Gram lift. Strict positivity then persists,
and pointwise FrameRealization gives actual complex-qubit strategies.

Thus the local-realizability assertion is proved rather than stored in a chart
structure as an unexplained field.
-/
noncomputable section
open scoped Bell.Entrywise
open Filter Set
open scoped BigOperators Matrix Topology
namespace Bell.Lorentz
open QubitGeometry

abbrev SymmetricCoordinates := Fin 10 → ℝ

def symmetricCoordinates : M →ₗ[ℝ] SymmetricCoordinates where
  toFun := fun A => ![A 0 0, A 0 1, A 0 2, A 0 3, A 1 1,
    A 1 2, A 1 3, A 2 2, A 2 3, A 3 3]
  map_add' := by intro A B; ext i; fin_cases i <;> rfl
  map_smul' := by intro t A; ext i; fin_cases i <;> rfl

def symmetricMatrix : SymmetricCoordinates →ₗ[ℝ] M where
  toFun := fun c => !![c 0,c 1,c 2,c 3; c 1,c 4,c 5,c 6;
    c 2,c 5,c 7,c 8; c 3,c 6,c 8,c 9]
  map_add' := by intro c d; ext i j; fin_cases i <;> fin_cases j <;> rfl
  map_smul' := by intro t c; ext i j; fin_cases i <;> fin_cases j <;> rfl

theorem symmetricMatrix_symmetric (c : SymmetricCoordinates) :
    (symmetricMatrix c).transpose = symmetricMatrix c := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

@[simp]
theorem symmetricCoordinates_matrix (c : SymmetricCoordinates) :
    symmetricCoordinates (symmetricMatrix c) = c := by
  ext i
  fin_cases i <;> rfl

theorem symmetricMatrix_coordinates (A : M) (hA : A.transpose = A) :
    symmetricMatrix (symmetricCoordinates A) = A := by
  ext i j
  have hij := congrFun (congrFun hA i) j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.cons_val, symmetricMatrix, symmetricCoordinates, Matrix.transpose_apply] at hij ⊢ <;>
    exact hij

def gramMatrixDerivative (E : M) : M →ₗ[ℝ] M where
  toFun := fun D => D.transpose * minkowski * E + E.transpose * minkowski * D
  map_add' := by
    intro D H
    simp only [Matrix.transpose_add, Matrix.add_mul, Matrix.mul_add]
    abel
  map_smul' := by
    intro t D
    simp only [Matrix.transpose_smul, Matrix.smul_mul, Matrix.mul_smul, smul_add, RingHom.id_apply]

def gramCoordinates (E : M) : SymmetricCoordinates := symmetricCoordinates (frameGram E)

def gramDerivative (E : M) : M →L[ℝ] SymmetricCoordinates :=
  (symmetricCoordinates.comp (gramMatrixDerivative E)).toContinuousLinearMap

private def gramEntry (i k : Fin 4) : M →L[ℝ] ℝ :=
  ({ toFun := fun A : M => A i k
     map_add' := by intros; rfl
     map_smul' := by intros; rfl } : M →ₗ[ℝ] ℝ).toContinuousLinearMap

/- Finite-coordinate product rule for the Gram map. -/
set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
theorem frameGram_hasStrictFDerivAt (E : M) :
    HasStrictFDerivAt frameGram (gramMatrixDerivative E).toContinuousLinearMap E := by
  apply hasStrictFDerivAt_pi'.mpr
  intro i
  apply hasStrictFDerivAt_pi'.mpr
  intro j
  have ht (k l : Fin 4) :=
    (((gramEntry k i).hasStrictFDerivAt (x := E)).mul_const (minkowski k l)).mul
      ((gramEntry l j).hasStrictFDerivAt (x := E))
  have hs := HasStrictFDerivAt.sum (u := Finset.univ) (fun k _ =>
    HasStrictFDerivAt.sum (u := Finset.univ) (fun l _ => ht k l))
  convert hs using 1
  · funext A
    simp [frameGram, gramEntry, Matrix.mul_apply, Matrix.transpose_apply,
      Fin.sum_univ_succ]
    ring
  · apply ContinuousLinearMap.ext
    intro D
    change (D.transpose * minkowski * E + E.transpose * minkowski * D) i j = _
    simp [gramMatrixDerivative, gramEntry, Matrix.mul_apply,
      Matrix.transpose_apply, Fin.sum_univ_succ]
    ring

theorem gramCoordinates_hasStrictFDerivAt (E : M) :
    HasStrictFDerivAt gramCoordinates (gramDerivative E) E :=
  symmetricCoordinates.toContinuousLinearMap.hasStrictFDerivAt.comp E
    (frameGram_hasStrictFDerivAt E)

/-- Explicit preimage of every symmetric target derivative. -/
theorem gramMatrixDerivative_right_inverse (E H : M) (hE : IsUnit E.det)
    (hH : H.transpose = H) :
    gramMatrixDerivative E ((1/2 : ℝ) • (minkowski * E.transpose⁻¹ * H)) = H := by
  let D := (1/2 : ℝ) • (minkowski * E.transpose⁻¹ * H)
  have he : IsUnit E.transpose.det := by simpa using hE
  have hr : E.transpose * minkowski * D = (1/2 : ℝ) • H := by
    dsimp [D]
    rw [Matrix.mul_smul]
    congr 1
    calc
      E.transpose * minkowski * (minkowski * E.transpose⁻¹ * H) =
          E.transpose * (minkowski * minkowski) * E.transpose⁻¹ * H := by noncomm_ring
      _ = H := by rw [minkowski_square, mul_one, Matrix.mul_nonsing_inv _ he, one_mul]
  have hl : D.transpose * minkowski * E = (1/2 : ℝ) • H := by
    have ht := congrArg Matrix.transpose hr
    simpa [Matrix.transpose_mul, Matrix.transpose_smul, Matrix.mul_assoc, hH] using ht
  change D.transpose * minkowski * E + E.transpose * minkowski * D = H
  rw [hr, hl, ← add_smul]
  norm_num

theorem gramDerivative_surjective (E : M) (hE : IsUnit E.det) :
    Function.Surjective (gramDerivative E) := by
  intro c
  refine ⟨(1/2 : ℝ) • (minkowski * E.transpose⁻¹ * symmetricMatrix c), ?_⟩
  change symmetricCoordinates (gramMatrixDerivative E _) = c
  rw [gramMatrixDerivative_right_inverse E _ hE (symmetricMatrix_symmetric c),
    symmetricCoordinates_matrix]

/-- A continuous local lift of symmetric forms, based at the given actual frame.
It is intentionally only local; no globally chosen Lorentz frame is asserted. -/
theorem exists_local_gram_lift (E : M) (hE : IsUnit E.det) :
    ∃ L : M → M, L (frameGram E) = E ∧
      Tendsto L (𝓝 (frameGram E)) (𝓝 E) ∧
      ∀ᶠ G in 𝓝 (frameGram E), G.transpose = G → frameGram (L G) = G := by
  let D := gramDerivative E
  have hf := gramCoordinates_hasStrictFDerivAt E
  have hD : LinearMap.range D = ⊤ := LinearMap.range_eq_top.mpr (gramDerivative_surjective E hE)
  let L : M → M := fun G => hf.implicitFunction gramCoordinates D hD (symmetricCoordinates G) 0
  have hct : Tendsto symmetricCoordinates (𝓝 (frameGram E)) (𝓝 (gramCoordinates E)) :=
    symmetricCoordinates.toContinuousLinearMap.continuous.continuousAt.tendsto
  refine ⟨L, ?_, ?_, ?_⟩
  · exact hf.implicitFunction_apply_image hD
  · exact hf.tendsto_implicitFunction hD hct tendsto_const_nhds
  · have ht : Tendsto (fun G : M => (symmetricCoordinates G, (0 : LinearMap.ker D)))
        (𝓝 (frameGram E)) (𝓝 (gramCoordinates E, 0)) := hct.prodMk_nhds tendsto_const_nhds
    have he := ht.eventually (hf.map_implicitFunction_eq hD)
    filter_upwards [he] with G hG hsym
    have hcoord : symmetricCoordinates (frameGram (L G)) = symmetricCoordinates G := hG
    have hmat := congrArg symmetricMatrix hcoord
    simpa [symmetricMatrix_coordinates _ (frameGram_symmetric _),
      symmetricMatrix_coordinates _ hsym] using hmat

/-- Every sufficiently nearby feasible polynomial table is physically
realizable. This is the local completeness bridge used by the maximum proof. -/
theorem eventually_feasible_mem_rawPOVM (E : M) (z : IncidenceSpace)
    (hE : IsUnit E.det) (hGram : frameGram E = chartMetric z.1)
    (hpos : FramePositive E z.2) :
    ∀ᶠ w in 𝓝 z, FeasibleIncidence w →
      tableOfBlock (probabilityBlock w) ∈ rawPOVM binaryTernaryArchitecture := by
  obtain ⟨L, hL0, hLt, hLe⟩ := exists_local_gram_lift E hE
  have hc : Continuous (fun w : IncidenceSpace => chartMetric w.1) := by
    apply continuous_pi
    intro i
    apply continuous_pi
    intro j
    fin_cases i <;> fin_cases j <;>
      simp [chartMetric, metric, Matrix.cons_val] <;> fun_prop
  have hct : Tendsto (fun w : IncidenceSpace => chartMetric w.1) (𝓝 z) (𝓝 (frameGram E)) := by
    rw [hGram]
    exact hc.continuousAt.tendsto
  have hframe : Tendsto (fun w : IncidenceSpace => L (chartMetric w.1)) (𝓝 z) (𝓝 E) :=
    hLt.comp hct
  have hpairs : Tendsto (fun w : IncidenceSpace => (L (chartMetric w.1), w.2))
      (𝓝 z) (𝓝 (E, z.2)) := hframe.prodMk_nhds continuous_snd.continuousAt.tendsto
  have hp := hpairs.eventually (isOpen_framePositive.mem_nhds hpos)
  have hg := hct.eventually hLe
  filter_upwards [hp, hg] with w hw hgw hfeasible
  exact frame_table_mem_rawPOVM (L (chartMetric w.1)) w
    (hgw (chartMetric_symmetric w.1)) hfeasible hw

/-- A global Bell maximum over actual qubit strategies is a constrained local
maximum in the polynomial chart. The required realizability is proved above. -/
theorem physical_maximum_is_incidence_maximum
    (E : M) (z : IncidenceSpace) (hE : IsUnit E.det)
    (hGram : frameGram E = chartMetric z.1) (hpos : FramePositive E z.2)
    (f : Behavior binaryTernaryArchitecture →ₗ[ℝ] ℝ)
    (hmax : ∀ q ∈ rawPOVM binaryTernaryArchitecture,
      f q ≤ f (tableOfBlock (probabilityBlock z))) :
    IsLocalMaxOn (fun w => f (tableOfBlock (probabilityBlock w)))
      {w | FeasibleIncidence w} z := by
  have he := eventually_feasible_mem_rawPOVM E z hE hGram hpos
  filter_upwards [he.filter_mono nhdsWithin_le_nhds, self_mem_nhdsWithin] with w hw hf
  exact hmax _ (hw hf)

end Bell.Lorentz
