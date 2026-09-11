import Bell.EntrywiseTopology
import Bell.UphillDirection

/-!
# Polynomial incidence coordinates and an exact finite score identity

We use `(p,Y)` with `g = metric p` and `P = g Y`. The five equations
`(Y r_j)ᵀ g (Y r_j) = 0` and the scalar normalization are polynomial.
The original coordinates are recovered by `Y = g⁻¹ P` whenever `g` is invertible.

At a stationary point the score difference to another normalized feasible
point is exactly a weighted quadratic form of `Y' - Y`, evaluated at `g'`.
No second derivative, Taylor remainder, or differentiability of matrix inverse
is used in this identity.

All the hypotheses of the algebraic lemmas below are explicit. This file does
not postulate that arbitrary physical data have already been reduced to this
chart. Proof source is awaiting the user's compilation run.
-/
noncomputable section
open scoped Bell.Entrywise
open scoped BigOperators Matrix
namespace Bell.Lorentz

/-- Matrix action as an honest real linear map. -/
def linearOfMatrix (A : M) : Endomorphism where
  toFun := fun x => A *ᵥ x
  map_add' := by intro x y; exact Matrix.mulVec_add A x y
  map_smul' := by intro t x; simp [Matrix.mulVec_smul]

@[simp]
theorem linearOfMatrix_apply (A : M) (x : V) : linearOfMatrix A x = A *ᵥ x := rfl

/-- Coordinates of an endomorphism in the fixed standard basis. -/
def matrixOfLinear (L : Endomorphism) : M := fun i j => L (Pi.single j 1) i

theorem matrixOfLinear_mulVec (L : Endomorphism) (x : V) :
    matrixOfLinear L *ᵥ x = L x := by
  have hx : (∑ j : Fin 4, x j • (Pi.single j 1 : V)) = x := by
    funext i
    simp
  calc
    matrixOfLinear L *ᵥ x = ∑ j : Fin 4, x j • L (Pi.single j 1) := by
      funext i
      simp [matrixOfLinear, Matrix.mulVec, dotProduct, mul_comm]
    _ = L (∑ j : Fin 4, x j • (Pi.single j 1 : V)) := by simp
    _ = L x := congrArg L hx

@[simp]
theorem matrixOfLinear_id : matrixOfLinear (LinearMap.id : Endomorphism) = 1 := by
  ext i j
  simp [matrixOfLinear, Matrix.one_apply, Pi.single_apply, eq_comm]

@[simp]
theorem matrixOfLinear_add (L K : Endomorphism) :
    matrixOfLinear (L + K) = matrixOfLinear L + matrixOfLinear K := by
  ext i j
  rfl

@[simp]
theorem matrixOfLinear_smul (t : ℝ) (L : Endomorphism) :
    matrixOfLinear (t • L) = t • matrixOfLinear L := by
  ext i j
  rfl

@[simp]
theorem linearOfMatrix_matrixOfLinear (L : Endomorphism) :
    linearOfMatrix (matrixOfLinear L) = L := by
  ext x i
  exact congrFun (matrixOfLinear_mulVec L x) i

/-- The real bilinear form associated to a matrix, without a symmetry assumption. -/
def matrixPair (A : M) : Bilinear where
  toFun := fun x =>
    { toFun := fun y => dotProduct x (A *ᵥ y)
      map_add' := by intro y z; simp [Matrix.mulVec_add, dotProduct_add]
      map_smul' := by intro t y; simp [Matrix.mulVec_smul, dotProduct_smul] }
  map_add' := by
    intro x y
    ext z
    simp [add_dotProduct]
  map_smul' := by
    intro t x
    ext z
    simp [smul_dotProduct]

@[simp]
theorem matrixPair_apply (A : M) (x y : V) :
    matrixPair A x y = dotProduct x (A *ᵥ y) := rfl

theorem matrixPair_transpose (A : M) (x y : V) :
    matrixPair A.transpose x y = matrixPair A y x := by
  simp only [matrixPair_apply, Matrix.mulVec, dotProduct, Matrix.transpose_apply,
    Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem matrixPair_symmetric {A : M} (hA : A.transpose = A) (x y : V) :
    matrixPair A x y = matrixPair A y x := by
  rw [← matrixPair_transpose, hA]

@[simp]
theorem matrixPair_add_matrix (A B : M) (x y : V) :
    matrixPair (A + B) x y = matrixPair A x y + matrixPair B x y := by
  simp only [matrixPair_apply, Matrix.add_mulVec, dotProduct_add]

@[simp]
theorem matrixPair_sub_matrix (A B : M) (x y : V) :
    matrixPair (A - B) x y = matrixPair A x y - matrixPair B x y := by
  simp only [matrixPair_apply, Matrix.sub_mulVec, dotProduct_sub]

@[simp]
theorem matrixPair_smul_matrix (t : ℝ) (A : M) (x y : V) :
    matrixPair (t • A) x y = t * matrixPair A x y := by
  simp [Matrix.smul_mulVec, dotProduct_smul]

/-- Pull a bilinear form back by a linear frame. -/
def pullbackForm (A : M) (Y : Endomorphism) : Bilinear where
  toFun := fun x => (matrixPair A (Y x)).comp Y
  map_add' := by intro x y; ext z; simp
  map_smul' := by intro t x; ext z; simp

@[simp]
theorem pullbackForm_apply (A : M) (Y : Endomorphism) (x y : V) :
    pullbackForm A Y x y = matrixPair A (Y x) (Y y) := rfl

/-- The affine four-parameter metric, now with a single parameter vector. -/
def chartMetric (p : V) : M := metric (p 0) (p 1) (p 2) (p 3)

/-- Its derivative is constant and linear in the four metric increments. -/
def metricVariation : V →ₗ[ℝ] M where
  toFun := fun h =>
    !![0, 0, h 0, h 1;
       0, 0, h 2, h 3;
       h 0, h 2, 0, h 0+h 1+h 2+h 3;
       h 1, h 3, h 0+h 1+h 2+h 3, 0]
  map_add' := by
    intro h k
    ext i j
    fin_cases i <;> fin_cases j <;> norm_num [Pi.add_apply] <;> ring
  map_smul' := by
    intro t h
    ext i j
    fin_cases i <;> fin_cases j <;> norm_num [Pi.smul_apply, smul_eq_mul] <;> ring

theorem chartMetric_add (p h : V) : chartMetric (p + h) = chartMetric p + metricVariation h := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [chartMetric, metric, metricVariation, Pi.add_apply] <;> ring

theorem chartMetric_sub (p q : V) : chartMetric q - chartMetric p = metricVariation (q - p) := by
  have h := chartMetric_add p (q - p)
  have hpq : p + (q - p) = q := by abel
  rw [hpq] at h
  rw [h]
  abel

theorem chartMetric_symmetric (p : V) : (chartMetric p).transpose = chartMetric p := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

theorem metricVariation_symmetric (h : V) :
    (metricVariation h).transpose = metricVariation h := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

theorem metricVariation_quadratic (h x : V) :
    matrixPair (metricVariation h) x x = 2 * dotProduct h (phi x) := by
  simp [metricVariation, matrixPair, phi, Matrix.mulVec, dotProduct, Fin.sum_univ_succ]
  ring

theorem chartMetric_null (p : V) (j : Fin 5) : matrixPair (chartMetric p) (ray j) (ray j) = 0 := by
  rw [matrixPair_apply, chartMetric, metric_quadratic]
  exact coefficient_rays_null _ _ _ _ j

theorem chartMetric_unit (p : V) : matrixPair (chartMetric p) unitVector unitVector = 1 := by
  rw [matrixPair_apply, chartMetric, metric_quadratic]
  exact metric_normalization _ _ _ _

/-- Normalization as a linear functional of the probability block. -/
def blockMass : M →ₗ[ℝ] ℝ where
  toFun := fun P => dotProduct unitVector (P *ᵥ unitVector)
  map_add' := by intro P Q; simp [Matrix.add_mulVec, dotProduct_add]
  map_smul' := by intro t P; simp [Matrix.smul_mulVec, dotProduct_smul]

/-- Weighted null constraints, with no positivity assumption on the weights. -/
def weightedGram (λ : Fin 5 → ℝ) (G Y : M) : ℝ :=
  ∑ j, λ j * matrixPair G (Y *ᵥ ray j) (Y *ᵥ ray j)

def weightedCross (λ : Fin 5 → ℝ) (G Y Z : M) : ℝ :=
  ∑ j, λ j * matrixPair G (Y *ᵥ ray j) (Z *ᵥ ray j)

def weightedPairing (λ : Fin 5 → ℝ) (Y P : M) : ℝ :=
  ∑ j, λ j * dotProduct (Y *ᵥ ray j) (P *ᵥ ray j)

@[simp]
theorem weightedPairing_mul (λ : Fin 5 → ℝ) (Y G Z : M) :
    weightedPairing λ Y (G * Z) = weightedCross λ G Y Z := by
  simp [weightedPairing, weightedCross, matrixPair, Matrix.mulVec_mulVec]

@[simp]
theorem weightedCross_self (λ : Fin 5 → ℝ) (G Y : M) :
    weightedCross λ G Y Y = weightedGram λ G Y := rfl

theorem weightedGram_zero_of_null (λ : Fin 5 → ℝ) (G Y : M)
    (hnull : ∀ j, matrixPair G (Y *ᵥ ray j) (Y *ᵥ ray j) = 0) :
    weightedGram λ G Y = 0 := by
  simp [weightedGram, hnull]

theorem weightedGram_add_metric (λ : Fin 5 → ℝ) (G H Y : M) :
    weightedGram λ (G + H) Y = weightedGram λ G Y + weightedGram λ H Y := by
  simp [weightedGram, mul_add, Finset.sum_add_distrib]

theorem weightedGram_sub_metric (λ : Fin 5 → ℝ) (G H Y : M) :
    weightedGram λ (G - H) Y = weightedGram λ G Y - weightedGram λ H Y := by
  simp [weightedGram, mul_sub, Finset.sum_sub_distrib]

theorem weightedCross_add_right (λ : Fin 5 → ℝ) (G Y Z W : M) :
    weightedCross λ G Y (Z + W) = weightedCross λ G Y Z + weightedCross λ G Y W := by
  simp [weightedCross, Matrix.add_mulVec, map_add, mul_add, Finset.sum_add_distrib]

theorem weightedGram_add_frame (λ : Fin 5 → ℝ) (G Y Z : M)
    (hG : G.transpose = G) :
    weightedGram λ G (Y + Z) = weightedGram λ G Y +
      2 * weightedCross λ G Y Z + weightedGram λ G Z := by
  simp only [weightedGram, weightedCross, Matrix.add_mulVec, map_add,
    LinearMap.add_apply]
  simp_rw [matrixPair_symmetric hG (Z *ᵥ _) (Y *ᵥ _)]
  simp only [Finset.mul_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem weightedGram_smul_frame (λ : Fin 5 → ℝ) (G Y : M) (t : ℝ) :
    weightedGram λ G (t • Y) = t^2 * weightedGram λ G Y := by
  simp only [weightedGram, Matrix.smul_mulVec, map_smul,
    LinearMap.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j _
  ring

/-- Coordinate-free finite score identity. No curve or derivative is involved. -/
theorem exact_stationary_score_gap
    (G G' Y Y' : M) (hG' : G'.transpose = G')
    (λ : Fin 5 → ℝ) (F : M →ₗ[ℝ] ℝ) (α : ℝ)
    (stationary : ∀ P, F P = α * blockMass P - 2 * weightedPairing λ Y P)
    (hbase : weightedGram λ G Y = 0)
    (hnew : weightedGram λ G' Y' = 0)
    (hmetric : weightedGram λ (G' - G) Y = 0)
    (hnorm : blockMass (G' * Y') = blockMass (G * Y)) :
    F (G' * Y') - F (G * Y) = weightedGram λ G' (Y' - Y) := by
  have hbase' : weightedGram λ G' Y = 0 := by
    rw [weightedGram_sub_metric, hbase, sub_zero] at hmetric
    exact hmetric
  have hsplit := weightedGram_add_frame λ G' Y (Y' - Y) hG'
  have hYY : Y + (Y' - Y) = Y' := by abel
  rw [hYY, hnew, hbase'] at hsplit
  have hcross := weightedCross_add_right λ G' Y Y (Y' - Y)
  rw [hYY, weightedCross_self, hbase'] at hcross
  rw [stationary, stationary, hnorm, weightedPairing_mul, weightedPairing_mul,
    weightedCross_self, hbase, hcross]
  linarith

/-- Polynomial chart coordinates. The second component is `Y = g⁻¹ P`. -/
abbrev IncidenceSpace := V × M

def probabilityBlock (z : IncidenceSpace) : M := chartMetric z.1 * z.2

def incidenceNulls (z : IncidenceSpace) : Fin 5 → ℝ :=
  fun j => matrixPair (chartMetric z.1) (z.2 *ᵥ ray j) (z.2 *ᵥ ray j)

def incidenceMass (z : IncidenceSpace) : ℝ := blockMass (probabilityBlock z)

def incidenceConstraints (z : IncidenceSpace) : (Fin 5 → ℝ) × ℝ :=
  (incidenceNulls z, incidenceMass z)

def FeasibleIncidence (z : IncidenceSpace) : Prop :=
  incidenceNulls z = 0 ∧ incidenceMass z = 1

/-- No inverse occurs anywhere in the six defining equations. -/
theorem contDiff_incidenceConstraints : ContDiff ℝ ⊤ incidenceConstraints := by
  unfold incidenceConstraints incidenceNulls incidenceMass probabilityBlock blockMass
    chartMetric metric matrixPair
  simp only [Matrix.mul_apply, Matrix.mulVec, dotProduct, Fin.sum_univ_succ]
  fun_prop

/-- Exact finite improvement identity in the polynomial coordinates. -/
theorem polynomial_score_gap
    (z z' : IncidenceSpace) (λ : Fin 5 → ℝ) (F : M →ₗ[ℝ] ℝ) (α : ℝ)
    (hz : FeasibleIncidence z) (hz' : FeasibleIncidence z')
    (stationary : ∀ P, F P = α * blockMass P - 2 * weightedPairing λ z.2 P)
    (metricStationary : ∀ h, weightedGram λ (metricVariation h) z.2 = 0) :
    F (probabilityBlock z') - F (probabilityBlock z) =
      weightedGram λ (chartMetric z'.1) (z'.2 - z.2) := by
  apply exact_stationary_score_gap (chartMetric z.1) (chartMetric z'.1) z.2 z'.2
    (chartMetric_symmetric _) λ F α stationary
  · apply weightedGram_zero_of_null
    intro j
    exact congrFun hz.1 j
  · apply weightedGram_zero_of_null
    intro j
    exact congrFun hz'.1 j
  · rw [chartMetric_sub]
    exact metricStationary _
  · exact hz'.2.trans hz.2.symm

end Bell.Lorentz
