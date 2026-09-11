import Bell.ResidualClosure

/-!
# From positive qubit frames to the strict residual coordinates

No metric signature or strict-parameter conditions are assumed by the frame
constructor. They follow from invertibility, positive rank-one effects, and
normalization. Both complete measurement partitions and all labels are retained.
-/
noncomputable section
open scoped Bell.Entrywise
open scoped BigOperators Matrix ComplexOrder
namespace Bell.Lorentz
open QubitGeometry

attribute [local simp] Matrix.cons_val_two Matrix.cons_val_three Matrix.cons_val_four

/-- The five fixed coefficient rays are pairwise projectively distinct. -/
theorem coefficient_rays_distinct (i j : Fin 5) (hij : i ≠ j) :
    ¬ SameRay (ray i) (ray j) := by
  intro h
  exact hij (coefficient_rays_projectively_distinct i j h)

theorem frame_rays_distinct (E : M) (hE : IsUnit E.det)
    (i j : Fin 5) (hij : i ≠ j) : ¬ SameRay (E *ᵥ ray i) (E *ᵥ ray j) := by
  rintro ⟨t, ht, h⟩
  apply coefficient_rays_distinct i j hij
  refine ⟨t, ht, ?_⟩
  have he := congrArg (fun x => E⁻¹ *ᵥ x) h
  simpa only [Matrix.mulVec_smul, Matrix.mulVec_mulVec,
    Matrix.nonsing_inv_mul E hE, Matrix.one_mulVec] using he

set_option maxRecDepth 100000 in
set_option maxHeartbeats 1000000 in
/-- All symmetric forms satisfying the coefficient null equations and mass
normalization have exactly the paper's four-parameter affine normal form. -/
theorem metric_normal_form (G : M) (hsym : G.transpose = G)
    (hn : ∀ j, matrixPair G (ray j) (ray j) = 0)
    (hu : matrixPair G unitVector unitVector = 1) :
    G = metric (G 0 2) (G 0 3) (G 1 2) (G 1 3) := by
  have hc2 (h : 2 < 4) : (⟨2,h⟩ : Fin 4) = 2 := rfl
  have hc3 (h : 3 < 4) : (⟨3,h⟩ : Fin 4) = 3 := rfl
  have hs3 : (2 : Fin 3).succ = (3 : Fin 4) := rfl
  have h00 := hn 0
  have h11 := hn 1
  have h22 := hn 2
  have h33 := hn 3
  have hv := hn 4
  have h01 := congrFun (congrFun hsym 0) 1
  have h02 := congrFun (congrFun hsym 0) 2
  have h03 := congrFun (congrFun hsym 0) 3
  have h12 := congrFun (congrFun hsym 1) 2
  have h13 := congrFun (congrFun hsym 1) 3
  have h23 := congrFun (congrFun hsym 2) 3
  norm_num [matrixPair_apply, Matrix.mulVec, dotProduct, Fin.sum_univ_succ,
    ray, unitVector, Matrix.transpose_apply] at h00 h11 h22 h33 hv hu h01 h02 h03 h12 h13 h23
  simp only [hc2, hc3, hs3] at h00 h11 h22 h33 hv hu h01 h02 h03 h12 h13 h23
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [metric] <;>
    (try simp only [hc2, hc3, hs3]) <;>
    linarith only [h00, h11, h22, h33, hv, hu, h01, h02, h03, h12, h13, h23]

/-- Concrete geometric data of two five-effect frames before any optimization.
`steering` contains the coordinates of Bob's steered, not normalized, effects. -/
structure ResidualFrames where
  alice : M
  steering : M
  alice_invertible : IsUnit alice.det
  steering_invertible : IsUnit steering.det
  alice_unit : alice *ᵥ unitVector = timeUnit
  alice_null : ∀ j, FutureNull (alice *ᵥ ray j)
  steering_null : ∀ j, FutureNull (steering *ᵥ ray j)
  reduced_timelike : FutureTimelike (steering *ᵥ unitVector)
  normalized : 2 * dotProduct (alice *ᵥ unitVector) (steering *ᵥ unitVector) = 1

namespace ResidualFrames

def gram (r : ResidualFrames) : M := frameGram r.alice

theorem gram_null (r : ResidualFrames) (j : Fin 5) :
    matrixPair r.gram (ray j) (ray j) = 0 := by
  rw [gram, frameGram_pair, lorentzPair_self]
  exact (r.alice_null j).2

theorem gram_unit (r : ResidualFrames) : matrixPair r.gram unitVector unitVector = 1 := by
  rw [gram, frameGram_pair, r.alice_unit]
  norm_num [lorentzPair, timeUnit]

theorem gram_off_diagonal_positive (r : ResidualFrames) (i j : Fin 5) (hij : i ≠ j) :
    0 < matrixPair r.gram (ray i) (ray j) := by
  rw [gram, frameGram_pair]
  exact null_pair_positive_of_distinct (r.alice_null i) (r.alice_null j)
    (frame_rays_distinct r.alice r.alice_invertible i j hij)

def parameters (r : ResidualFrames) : StrictParameters := by
  have hn := metric_normal_form r.gram (frameGram_symmetric _) r.gram_null r.gram_unit
  have p02 := r.gram_off_diagonal_positive 0 2 (by decide)
  have p03 := r.gram_off_diagonal_positive 0 3 (by decide)
  have p12 := r.gram_off_diagonal_positive 1 2 (by decide)
  have p13 := r.gram_off_diagonal_positive 1 3 (by decide)
  have p23 := r.gram_off_diagonal_positive 2 3 (by decide)
  have p04 := r.gram_off_diagonal_positive 0 4 (by decide)
  have p14 := r.gram_off_diagonal_positive 1 4 (by decide)
  have p24 := r.gram_off_diagonal_positive 2 4 (by decide)
  have p34 := r.gram_off_diagonal_positive 3 4 (by decide)
  rw [hn] at p02 p03 p12 p13 p23 p04 p14 p24 p34
  simp [matrixPair_apply, metric, ray, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] at p02 p03 p12 p13 p23 p04 p14 p24 p34
  exact ⟨r.gram 0 2, r.gram 0 3, r.gram 1 2, r.gram 1 3,
    p02, p03, p12, p13, by linarith, by linarith, by linarith, by linarith, by linarith⟩

theorem parameters_gram (r : ResidualFrames) :
    metric r.parameters.a r.parameters.b r.parameters.c r.parameters.d = r.gram := by
  exact (metric_normal_form r.gram (frameGram_symmetric _) r.gram_null r.gram_unit).symm

/-- The probability matrix follows from the trace pairing of the two frames. -/
def block (r : ResidualFrames) : M := (2 : ℝ) • (r.alice.transpose * r.steering)

def transformed (r : ResidualFrames) : M :=
  (2 : ℝ) • (r.alice⁻¹ * minkowski * r.steering)

theorem alice_transformed (r : ResidualFrames) :
    r.alice * r.transformed = (2 : ℝ) • (minkowski * r.steering) := by
  simp [transformed, Matrix.mul_smul, ← Matrix.mul_assoc,
    Matrix.mul_nonsing_inv _ r.alice_invertible]

theorem gram_transformed (r : ResidualFrames) : r.gram * r.transformed = r.block := by
  dsimp [gram, frameGram, transformed, block]
  rw [Matrix.mul_smul]
  congr 1
  calc
    _ = r.alice.transpose * minkowski * (r.alice * r.alice⁻¹) * minkowski * r.steering := by
      noncomm_ring
    _ = r.alice.transpose * r.steering := by
      rw [Matrix.mul_nonsing_inv _ r.alice_invertible, mul_one]
      rw [Matrix.mul_assoc r.alice.transpose, minkowski_square, mul_one]

theorem transformed_invertible (r : ResidualFrames) : IsUnit r.transformed.det := by
  have hJ : IsUnit minkowski.det := by
    apply isUnit_iff_ne_zero.mpr
    have hd := congrArg Matrix.det minkowski_square
    rw [Matrix.det_mul, Matrix.det_one] at hd
    intro hzero
    simp [hzero] at hd
  have hAi : IsUnit r.alice⁻¹.det := by
    rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv]
    exact r.alice_invertible.inv
  rw [transformed, Matrix.det_smul, Matrix.det_mul, Matrix.det_mul]
  exact (isUnit_iff_ne_zero.mpr (by norm_num : (2 : ℝ)^Fintype.card (Fin 4) ≠ 0)).mul
    ((hAi.mul hJ).mul r.steering_invertible)

theorem transformed_null (r : ResidualFrames) (j : Fin 5) :
    matrixPair r.gram (r.transformed *ᵥ ray j) (r.transformed *ᵥ ray j) = 0 := by
  rw [gram, frameGram_pair, lorentzPair_self, Matrix.mulVec_mulVec, r.alice_transformed]
  have hs := (r.steering_null j).2
  rw [Matrix.smul_mulVec_assoc, ← Matrix.mulVec_mulVec]
  generalize r.steering *ᵥ ray j = v at hs ⊢
  simp [minkowski, lorentzSquare,
    Matrix.mulVec, dotProduct, Fin.sum_univ_succ] at hs ⊢
  nlinarith

theorem block_normalized (r : ResidualFrames) : blockMass r.block = 1 := by
  have hi : matrixPair (r.alice.transpose * r.steering) unitVector unitVector =
      dotProduct (r.alice *ᵥ unitVector) (r.steering *ᵥ unitVector) := by
    have h := matrixPair_mul_frames (1 : M) r.alice r.steering unitVector unitVector
    simpa [matrixPair_apply] using h.symm
  change matrixPair r.block unitVector unitVector = 1
  rw [block, matrixPair_smul_matrix]
  rw [hi]
  exact r.normalized

theorem feasible (r : ResidualFrames) :
    FeasibleIncidence (parameterVector r.parameters, r.transformed) := by
  constructor
  · funext j
    change matrixPair (metric r.parameters.a r.parameters.b r.parameters.c r.parameters.d)
      (r.transformed *ᵥ ray j) (r.transformed *ᵥ ray j) = 0
    rw [r.parameters_gram]
    exact r.transformed_null j
  · change blockMass (metric r.parameters.a r.parameters.b r.parameters.c r.parameters.d *
        r.transformed) = 1
    rw [r.parameters_gram, r.gram_transformed]
    exact r.block_normalized

theorem frame_positive (r : ResidualFrames) : FramePositive r.alice r.transformed := by
  refine ⟨fun j => (r.alice_null j).1, ?_, ?_⟩
  · intro j
    rw [Matrix.mulVec_mulVec, r.alice_transformed]
    rw [Matrix.smul_mulVec_assoc, ← Matrix.mulVec_mulVec]
    have hj := (r.steering_null j).1
    generalize r.steering *ᵥ ray j = v at hj ⊢
    simpa [minkowski, Matrix.mulVec, dotProduct, Fin.sum_univ_succ] using
      mul_pos (by norm_num : (0 : ℝ) < 2) hj
  · rw [frameGram_pair, lorentzPair_self, Matrix.mulVec_mulVec, r.alice_transformed]
    have hq := r.reduced_timelike.2
    rw [Matrix.smul_mulVec_assoc, ← Matrix.mulVec_mulVec]
    generalize r.steering *ᵥ unitVector = v at hq ⊢
    simp [minkowski, lorentzSquare,
      Matrix.mulVec, dotProduct, Fin.sum_univ_succ] at hq ⊢
    nlinarith

/-- The previously proved analytic closure now applies to actual positive
frames, with strict metric parameters and all physical chart conditions derived. -/
theorem not_strict_maximum (r : ResidualFrames)
    (f : Behavior binaryTernaryArchitecture →ₗ[ℝ] ℝ)
    (hmax : ∀ q ∈ rawPOVM binaryTernaryArchitecture, f q ≤ f (tableOfBlock r.block))
    (hstrict : ∀ q ∈ convexPVM binaryTernaryArchitecture, f q < f (tableOfBlock r.block)) : False := by
  have hblock : metric r.parameters.a r.parameters.b r.parameters.c r.parameters.d * r.transformed =
      r.block := by rw [r.parameters_gram, r.gram_transformed]
  apply no_strict_residual_maximum r.parameters r.alice r.transformed r.alice_invertible
    r.transformed_invertible r.parameters_gram.symm r.alice_unit r.feasible r.frame_positive f
  · simpa [hblock] using hmax
  · simpa [hblock] using hstrict

end ResidualFrames
end Bell.Lorentz
