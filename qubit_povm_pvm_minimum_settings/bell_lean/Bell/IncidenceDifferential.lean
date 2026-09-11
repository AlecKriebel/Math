import Bell.IncidenceAlgebra
import Mathlib.Analysis.Calculus.FDeriv.Mul
import Mathlib.Analysis.Calculus.FDeriv.Prod

/-!
# Polynomial incidence differential and its explicit right inverse

Surjectivity is proved by constructing a preimage of every six-vector. There
is no assumption called smoothness, tangent integrability, or Jacobian rank.
The only regularity input is invertibility of the probability block, together
with the displayed null equations and normalization.
-/
set_option maxRecDepth 100000
set_option maxHeartbeats 200000

noncomputable section
open scoped Bell.Entrywise
open scoped BigOperators Matrix
namespace Bell.Lorentz

abbrev ConstraintSpace := (Fin 5 → ℝ) × ℝ

/-- Linear first variation of P=gY. -/
def blockDerivative (z : IncidenceSpace) : IncidenceSpace →ₗ[ℝ] M where
  toFun := fun d => metricVariation d.1 * z.2 + chartMetric z.1 * d.2
  map_add' := by
    intro d e
    simp only [Prod.fst_add, Prod.snd_add, map_add, Matrix.add_mul, Matrix.mul_add]
    abel
  map_smul' := by
    intro t d
    simp only [Prod.smul_fst, Prod.smul_snd, map_smul,
      Matrix.smul_mul, Matrix.mul_smul, smul_add, RingHom.id_apply]

/-- The full three-term product-rule derivative of the five null constraints. -/
def nullDerivative (z : IncidenceSpace) : IncidenceSpace →ₗ[ℝ] (Fin 5 → ℝ) where
  toFun := fun d j =>
    matrixPair (chartMetric z.1) (d.2 *ᵥ ray j) (z.2 *ᵥ ray j) +
    matrixPair (metricVariation d.1) (z.2 *ᵥ ray j) (z.2 *ᵥ ray j) +
    matrixPair (chartMetric z.1) (z.2 *ᵥ ray j) (d.2 *ᵥ ray j)
  map_add' := by
    intro d e
    funext j
    simp only [Prod.fst_add, Prod.snd_add, map_add, Matrix.add_mulVec,
      LinearMap.add_apply, matrixPair_add_matrix, Pi.add_apply]
    ring
  map_smul' := by
    intro t d
    funext j
    simp only [Prod.smul_fst, Prod.smul_snd, map_smul, Matrix.smul_mulVec_assoc,
      LinearMap.smul_apply, matrixPair_smul_matrix, Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    ring

def massDerivative (z : IncidenceSpace) : IncidenceSpace →ₗ[ℝ] ℝ :=
  blockMass.comp (blockDerivative z)

def constraintDerivative (z : IncidenceSpace) : IncidenceSpace →ₗ[ℝ] ConstraintSpace :=
  (nullDerivative z).prod (massDerivative z)

def constraintDerivativeCLM (z : IncidenceSpace) : IncidenceSpace →L[ℝ] ConstraintSpace :=
  (constraintDerivative z).toContinuousLinearMap

@[simp]
theorem constraintDerivativeCLM_apply (z d : IncidenceSpace) :
    constraintDerivativeCLM z d = constraintDerivative z d := rfl

theorem nullDerivative_symmetric (z d : IncidenceSpace) (j : Fin 5) :
    nullDerivative z d j =
      2 * matrixPair (chartMetric z.1) (z.2 *ᵥ ray j) (d.2 *ᵥ ray j) +
      matrixPair (metricVariation d.1) (z.2 *ᵥ ray j) (z.2 *ᵥ ray j) := by
  dsimp only [nullDerivative, LinearMap.coe_mk, AddHom.coe_mk]
  rw [matrixPair_symmetric (chartMetric_symmetric _) (d.2 *ᵥ _) (z.2 *ᵥ _)]
  ring

private def matrixCoordinate (i k : Fin 4) : M →ₗ[ℝ] ℝ where
  toFun := fun A => A i k
  map_add' := by intros; rfl
  map_smul' := by intros; rfl

private def metricCoordinate (i k : Fin 4) : IncidenceSpace →L[ℝ] ℝ :=
  ((matrixCoordinate i k).comp
    (metricVariation.comp (LinearMap.fst ℝ V M))).toContinuousLinearMap

private def frameCoordinate (r : V) (i : Fin 4) : IncidenceSpace →L[ℝ] ℝ :=
  ({ toFun := fun z : IncidenceSpace => (z.2 *ᵥ r) i
     map_add' := by intro z w; simp [Matrix.add_mulVec]
     map_smul' := by intro t z; simp [Matrix.smul_mulVec_assoc] } :
    IncidenceSpace →ₗ[ℝ] ℝ).toContinuousLinearMap

private theorem metricCoordinate_hasStrictFDerivAt (z : IncidenceSpace) (i k : Fin 4) :
    HasStrictFDerivAt (fun w : IncidenceSpace => chartMetric w.1 i k)
      (metricCoordinate i k) z := by
  have heq : (fun w : IncidenceSpace => chartMetric w.1 i k) =
      fun w => chartMetric 0 i k + metricCoordinate i k w := by
    funext w
    have h := chartMetric_add 0 w.1
    simpa only [zero_add, Matrix.add_apply, metricCoordinate, matrixCoordinate,
      LinearMap.coe_toContinuousLinearMap', LinearMap.comp_apply, LinearMap.fst_apply] using
      congrFun (congrFun h i) k
  rw [heq]
  exact (metricCoordinate i k).hasStrictFDerivAt.const_add _

/-- Direct finite-coordinate product-rule calculation of each null derivative. -/
theorem incidenceNull_hasStrictFDerivAt (z : IncidenceSpace) (j : Fin 5) :
    HasStrictFDerivAt (fun w => incidenceNulls w j)
      (((LinearMap.proj j).comp (nullDerivative z)).toContinuousLinearMap) z := by
  let r := ray j
  have ht (i k : Fin 4) :=
    (((frameCoordinate r i).hasStrictFDerivAt (x := z)).mul
      (metricCoordinate_hasStrictFDerivAt z i k)).mul
      ((frameCoordinate r k).hasStrictFDerivAt (x := z))
  have hs := HasStrictFDerivAt.sum (u := Finset.univ) (fun i _ =>
    HasStrictFDerivAt.sum (u := Finset.univ) (fun k _ => ht i k))
  convert hs using 1
  · funext w
    simp [incidenceNulls, matrixPair, frameCoordinate, r, Matrix.mulVec,
      dotProduct, Finset.mul_sum, mul_assoc]
  · apply ContinuousLinearMap.ext
    intro d
    simp [nullDerivative, matrixPair, frameCoordinate, metricCoordinate, matrixCoordinate,
      r, Matrix.mulVec, dotProduct, Fin.sum_univ_succ]
    ring

/-- Direct finite-coordinate derivative of the probability block. -/
theorem probabilityBlock_hasStrictFDerivAt (z : IncidenceSpace) :
    HasStrictFDerivAt probabilityBlock (blockDerivative z).toContinuousLinearMap z := by
  apply hasStrictFDerivAt_pi'.mpr
  intro i
  apply hasStrictFDerivAt_pi'.mpr
  intro k
  let e : V := Pi.single k 1
  have ht (l : Fin 4) := (metricCoordinate_hasStrictFDerivAt z i l).mul
    ((frameCoordinate e l).hasStrictFDerivAt (x := z))
  have hs := HasStrictFDerivAt.sum (u := Finset.univ) (fun l _ => ht l)
  convert hs using 1
  · funext w
    simp [probabilityBlock, frameCoordinate, e, Matrix.mul_apply]
  · apply ContinuousLinearMap.ext
    intro d
    change (metricVariation d.1 * z.2 + chartMetric z.1 * d.2) i k = _
    simp [blockDerivative, metricCoordinate, matrixCoordinate, frameCoordinate, e,
      Matrix.mul_apply, Fin.sum_univ_succ]
    ring

theorem incidenceMass_hasStrictFDerivAt (z : IncidenceSpace) :
    HasStrictFDerivAt incidenceMass (massDerivative z).toContinuousLinearMap z := by
  have h := blockMass.toContinuousLinearMap.hasStrictFDerivAt.comp z
    (probabilityBlock_hasStrictFDerivAt z)
  exact h

theorem incidenceConstraints_hasStrictFDerivAt (z : IncidenceSpace) :
    HasStrictFDerivAt incidenceConstraints (constraintDerivativeCLM z) z := by
  have hn : HasStrictFDerivAt incidenceNulls (nullDerivative z).toContinuousLinearMap z := by
    apply hasStrictFDerivAt_pi'.mpr
    intro j
    exact incidenceNull_hasStrictFDerivAt z j
  have h := hn.prodMk (incidenceMass_hasStrictFDerivAt z)
  exact h

/-- A symmetric matrix prescribing its quadratic values on the five fixed rays. -/
def nullDerivativeSeed (c : Fin 5 → ℝ) : M :=
  !![c 0 / 2, (c 4-c 0-c 1-c 2-c 3)/4, 0, 0;
     (c 4-c 0-c 1-c 2-c 3)/4, c 1 / 2, 0, 0;
     0, 0, c 2 / 2, 0;
     0, 0, 0, c 3 / 2]

theorem nullDerivativeSeed_values (c : Fin 5 → ℝ) (j : Fin 5) :
    2 * matrixPair (nullDerivativeSeed c) (ray j) (ray j) = c j := by
  fin_cases j <;>
    norm_num [Matrix.cons_val, nullDerivativeSeed, matrixPair, ray, Matrix.mulVec, dotProduct, Fin.sum_univ_succ] <;>
    simp [Matrix.cons_val] <;> ring

/-- Right inverse for the five null derivatives before normalization. -/
theorem nullDerivative_seed_preimage (z : IncidenceSpace)
    (hinv : IsUnit (probabilityBlock z).det) (c : Fin 5 → ℝ) :
    nullDerivative z (0, (probabilityBlock z).transpose⁻¹ * nullDerivativeSeed c) = c := by
  funext j
  rw [nullDerivative_symmetric]
  simp only [map_zero,
    matrixPair_apply, Matrix.zero_mulVec, dotProduct_zero, add_zero]
  change 2 * matrixPair (chartMetric z.1) (z.2 *ᵥ ray j)
    (((probabilityBlock z).transpose⁻¹ * nullDerivativeSeed c) *ᵥ ray j) = c j
  rw [matrixPair_mul_frames]
  have htr : z.2.transpose * chartMetric z.1 = (probabilityBlock z).transpose := by
    simp [probabilityBlock, Matrix.transpose_mul, chartMetric_symmetric]
  rw [htr, Matrix.mul_nonsing_inv_cancel_left _ _ (by simpa using hinv)]
  exact nullDerivativeSeed_values c j

/-- The radial direction preserves every null equation and changes mass by one. -/
theorem constraintDerivative_radial (z : IncidenceSpace) (hz : FeasibleIncidence z) :
    constraintDerivative z (0, z.2) = (0, 1) := by
  apply Prod.ext
  · funext j
    rw [show (constraintDerivative z (0, z.2)).1 = nullDerivative z (0, z.2) from rfl,
      nullDerivative_symmetric]
    have hj := congrFun hz.1 j
    change matrixPair (chartMetric z.1) (z.2 *ᵥ ray j) (z.2 *ᵥ ray j) = 0 at hj
    simp [hj]
  · change blockMass (metricVariation 0 * z.2 + chartMetric z.1 * z.2) = 1
    simpa [incidenceMass, probabilityBlock] using hz.2

/-- Explicit surjectivity of all six constraint differentials. -/
theorem constraintDerivative_surjective (z : IncidenceSpace) (hz : FeasibleIncidence z)
    (hinv : IsUnit (probabilityBlock z).det) : Function.Surjective (constraintDerivative z) := by
  rintro ⟨c, n⟩
  let d₀ : IncidenceSpace := (0, (probabilityBlock z).transpose⁻¹ * nullDerivativeSeed c)
  let s := massDerivative z d₀
  have h₀ : constraintDerivative z d₀ = (c, s) := by
    exact Prod.ext (nullDerivative_seed_preimage z hinv c) rfl
  refine ⟨d₀ + (n-s) • (0, z.2), ?_⟩
  rw [map_add, map_smul, h₀, constraintDerivative_radial z hz]
  apply Prod.ext
  · simp
  · simp

theorem constraintDerivative_range (z : IncidenceSpace) (hz : FeasibleIncidence z)
    (hinv : IsUnit (probabilityBlock z).det) :
    LinearMap.range (constraintDerivativeCLM z) = ⊤ :=
  LinearMap.range_eq_top.mpr (constraintDerivative_surjective z hz hinv)

end Bell.Lorentz
