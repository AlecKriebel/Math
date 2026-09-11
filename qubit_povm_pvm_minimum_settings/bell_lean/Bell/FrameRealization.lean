import Bell.Purification
import Bell.IncidenceScores

/-!
# Pointwise physical realization of the polynomial incidence chart

A Gram frame gives positive, initially unnormalized Alice effects and steered
Bob effects. A compensating congruence normalizes them, after which the explicit
purification constructs a genuine complex two-qubit strategy. No differentiable
choice of matrix square root or purification is needed.
-/
noncomputable section
open scoped Bell.Entrywise
open scoped BigOperators Matrix ComplexOrder Topology
namespace Bell

/-- Unnormalized positive measurement data with common left and right sums. -/
structure UnnormalizedAssemblage (A : Architecture) where
  left : (x : Fin A.aliceInputs) → Fin (A.aliceOutputs x) → Operator
  right : (y : Fin A.bobInputs) → Fin (A.bobOutputs y) → Operator
  leftSum : Operator
  rightSum : Operator
  leftPositive : ∀ x a, (left x a).PosSemidef
  rightPositive : ∀ y b, (right y b).PosSemidef
  leftTotal : ∀ x, ∑ a, left x a = leftSum
  rightTotal : ∀ y, ∑ b, right y b = rightSum
  leftDefinite : leftSum.PosDef
  rightDefinite : rightSum.PosDef
  normalized : Matrix.trace (leftSum * rightSum) = 1

namespace UnnormalizedAssemblage
variable {A : Architecture} (s : UnnormalizedAssemblage A)

def root : Operator := s.leftDefinite.posSemidef.sqrt

theorem root_hermitian : s.root.conjTranspose = s.root :=
  s.leftDefinite.posSemidef.posSemidef_sqrt.isHermitian.eq

theorem root_square : s.root * s.root = s.leftSum :=
  s.leftDefinite.posSemidef.sqrt_mul_self

theorem root_invertible : IsUnit s.root.det := by
  apply isUnit_iff_ne_zero.mpr
  intro hzero
  have heq := congrArg Matrix.det s.root_square
  rw [Matrix.det_mul, hzero, zero_mul] at heq
  exact s.leftDefinite.det_pos.ne' heq.symm

def normalizedAlice (x : Fin A.aliceInputs) : POVM (A.aliceOutputs x) where
  effect := fun a => s.root⁻¹.conjTranspose * s.left x a * s.root⁻¹
  positive := fun a => (s.leftPositive x a).conjTranspose_mul_mul_same s.root⁻¹
  normalized := by
    rw [← Matrix.sum_mul, ← Matrix.mul_sum, s.leftTotal x, ← s.root_square]
    have hh : s.root⁻¹.conjTranspose = s.root⁻¹ := by
      rw [Matrix.conjTranspose_nonsing_inv, s.root_hermitian]
    rw [hh]
    simp [Matrix.mul_assoc, Matrix.nonsing_inv_mul _ s.root_invertible,
      Matrix.mul_nonsing_inv _ s.root_invertible]

def normalizedAssemblage : Assemblage A where
  alice := s.normalizedAlice
  reduced := s.root * s.rightSum * s.root.conjTranspose
  reducedPositive := s.rightDefinite.posSemidef.mul_mul_conjTranspose_same s.root
  reducedNormalized := by
    rw [Matrix.trace_mul_comm, ← Matrix.mul_assoc, s.root_hermitian,
      s.root_square, s.normalized]
  steered := fun y b => s.root * s.right y b * s.root.conjTranspose
  positive := fun y b => (s.rightPositive y b).mul_mul_conjTranspose_same s.root
  commonSum := by
    intro y
    rw [← Matrix.sum_mul, ← Matrix.mul_sum, s.rightTotal y]

theorem normalizedAssemblage_invertible : IsUnit s.normalizedAssemblage.reduced.det := by
  change IsUnit (s.root * s.rightSum * s.root.conjTranspose).det
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_conjTranspose]
  exact (s.root_invertible.mul (isUnit_iff_ne_zero.mpr s.rightDefinite.det_pos.ne')).mul
    (s.root_invertible.map (starRingEnd ℂ))

/-- Exact probabilities before and after normalizing both factors. -/
theorem normalized_behavior (x : Fin A.aliceInputs) (y : Fin A.bobInputs)
    (a : Fin (A.aliceOutputs x)) (b : Fin (A.bobOutputs y)) :
    s.normalizedAssemblage.behavior x y a b = localTrace (s.left x a) (s.right y b) :=
  inverse_congruence_trace s.root (s.left x a) (s.right y b) s.root_invertible

theorem behavior_mem_rawPOVM :
    (fun x y a b => localTrace (s.left x a) (s.right y b)) ∈ rawPOVM A := by
  have heq : s.normalizedAssemblage.behavior =
      fun x y a b => localTrace (s.left x a) (s.right y b) := by
    funext x y a b
    exact s.normalized_behavior x y a b
  rw [← heq]
  exact s.normalizedAssemblage.mem_rawPOVM s.normalizedAssemblage_invertible

end UnnormalizedAssemblage

namespace Lorentz
open QubitGeometry

/-- Gram matrix in the fixed Pauli/Minkowski convention. -/
def frameGram (E : M) : M := E.transpose * minkowski * E

theorem frameGram_symmetric (E : M) : (frameGram E).transpose = frameGram E := by
  simp [frameGram, Matrix.transpose_mul, Matrix.mul_assoc]

theorem frameGram_pair (E : M) (x y : V) :
    matrixPair (frameGram E) x y = lorentzPair (E *ᵥ x) (E *ᵥ y) := by
  rw [lorentzPair_eq_matrixPair]
  exact (matrixPair_mul_frames minkowski E E x y).symm

/-- Linear steered-frame map. Its factor 1/2 compensates the Pauli trace factor. -/
def steeringFrame (E Y : M) : M := (1/2 : ℝ) • (minkowski * E * Y)

@[simp]
theorem steeringFrame_mulVec (E Y : M) (x : V) :
    steeringFrame E Y *ᵥ x = (1/2 : ℝ) • (minkowski *ᵥ (E *ᵥ (Y *ᵥ x))) := by
  simp only [steeringFrame, Matrix.smul_mulVec_assoc, ← Matrix.mulVec_mulVec]

theorem steeringFrame_time (E Y : M) (x : V) :
    (steeringFrame E Y *ᵥ x) 0 = (1/2 : ℝ) * (E *ᵥ (Y *ᵥ x)) 0 := by
  rw [steeringFrame_mulVec]
  generalize E *ᵥ (Y *ᵥ x) = v
  simp [minkowski, Matrix.mulVec, dotProduct, Fin.sum_univ_succ, Matrix.cons_val]

theorem steeringFrame_square (E Y : M) (x : V) :
    lorentzSquare (steeringFrame E Y *ᵥ x) =
      (1/4 : ℝ) * matrixPair (frameGram E) (Y *ᵥ x) (Y *ᵥ x) := by
  rw [frameGram_pair, lorentzPair_self, steeringFrame_mulVec]
  generalize E *ᵥ (Y *ᵥ x) = v
  simp [minkowski, lorentzSquare, Matrix.mulVec, dotProduct, Fin.sum_univ_succ,
    Matrix.cons_val]
  ring

theorem frame_probability (E Y : M) (x y : V) :
    localTrace (pauli (E *ᵥ x)) (pauli (steeringFrame E Y *ᵥ y)) =
      matrixPair (frameGram E * Y) x y := by
  rw [localTrace_apply, pauli_trace_product, Complex.ofReal_re, steeringFrame_mulVec]
  have hp := frameGram_pair E x (Y *ᵥ y)
  rw [lorentzPair_eq_matrixPair] at hp
  simp only [matrixPair_apply] at hp
  simp only [matrixPair_apply, ← Matrix.mulVec_mulVec, dotProduct_smul, smul_eq_mul]
  rw [hp]
  ring

def FramePositive (E Y : M) : Prop :=
  (∀ j : Fin 5, 0 < (E *ᵥ ray j) 0) ∧
  (∀ j : Fin 5, 0 < (E *ᵥ (Y *ᵥ ray j)) 0) ∧
  0 < matrixPair (frameGram E) (Y *ᵥ unitVector) (Y *ᵥ unitVector)

/-- The extra physical conditions are strict polynomial inequalities, hence open. -/
theorem isOpen_framePositive : IsOpen {p : M × M | FramePositive p.1 p.2} := by
  simp only [FramePositive, Set.setOf_and, Set.setOf_forall]
  apply IsOpen.inter
  · apply isOpen_iInter_of_finite
    intro j
    exact isOpen_lt continuous_const (by unfold Matrix.mulVec dotProduct; fun_prop)
  · apply IsOpen.inter
    · apply isOpen_iInter_of_finite
      intro j
      exact isOpen_lt continuous_const (by unfold Matrix.mulVec dotProduct; fun_prop)
    · apply isOpen_lt continuous_const
      simp only [matrixPair_apply, frameGram, Matrix.mul_apply, Matrix.mulVec,
        dotProduct, Matrix.transpose_apply]
      fun_prop

private theorem positive_time_unit (E : M) (hE : ∀ j : Fin 5, 0 < (E *ᵥ ray j) 0) :
    0 < (E *ᵥ unitVector) 0 := by
  have hu : unitVector = ray 0 + ray 1 := by ext i; fin_cases i <;> simp [Matrix.cons_val, unitVector, ray]
  rw [hu, Matrix.mulVec_add, Pi.add_apply]
  exact add_pos (hE 0) (hE 1)

private theorem effectRay_cases (x : Fin 2) (a : Fin 3) :
    effectRay x a = 0 ∨ ∃ j : Fin 5, effectRay x a = ray j := by
  fin_cases x <;> fin_cases a
  · exact Or.inr ⟨0, rfl⟩
  · exact Or.inr ⟨1, rfl⟩
  · exact Or.inl rfl
  · exact Or.inr ⟨2, rfl⟩
  · exact Or.inr ⟨3, rfl⟩
  · exact Or.inr ⟨4, rfl⟩

/-- The raw two-sided frame before normalization. Every premise is a concrete
polynomial relation or strict inequality on E, p and Y. -/
def frameAssemblage (E : M) (z : IncidenceSpace)
    (hGram : frameGram E = chartMetric z.1) (hz : FeasibleIncidence z)
    (hpos : FramePositive E z.2) : UnnormalizedAssemblage binaryTernaryArchitecture where
  left := fun x a => pauli (E *ᵥ effectRay x a)
  right := fun y b => pauli (steeringFrame E z.2 *ᵥ effectRay y b)
  leftSum := pauli (E *ᵥ unitVector)
  rightSum := pauli (steeringFrame E z.2 *ᵥ unitVector)
  leftPositive := by
    intro x a
    rcases effectRay_cases x a with h0 | ⟨j, hj⟩
    · simp [h0, Matrix.PosSemidef.zero]
    · rw [hj]
      apply FutureNull.posSemidef
      refine ⟨hpos.1 j, ?_⟩
      rw [← lorentzPair_self, ← frameGram_pair, hGram, chartMetric_null]
  rightPositive := by
    intro y b
    rcases effectRay_cases y b with h0 | ⟨j, hj⟩
    · simp [h0, Matrix.PosSemidef.zero]
    · rw [hj]
      apply FutureNull.posSemidef
      refine ⟨?_, ?_⟩
      · rw [steeringFrame_time]
        exact mul_pos (by norm_num) (hpos.2.1 j)
      · rw [steeringFrame_square, hGram]
        have hn := congrFun hz.1 j
        change matrixPair (chartMetric z.1) (z.2 *ᵥ ray j) (z.2 *ᵥ ray j) = 0 at hn
        rw [hn, mul_zero]
  leftTotal := by
    intro x
    change (∑ a, pauli (linearOfMatrix E (effectRay x a))) =
      pauli (linearOfMatrix E unitVector)
    rw [← map_sum, ← map_sum, sum_effectRay]
  rightTotal := by
    intro y
    change (∑ b, pauli (linearOfMatrix (steeringFrame E z.2) (effectRay y b))) =
      pauli (linearOfMatrix (steeringFrame E z.2) unitVector)
    rw [← map_sum, ← map_sum, sum_effectRay]
  leftDefinite := by
    apply FutureTimelike.posDef
    refine ⟨positive_time_unit E hpos.1, ?_⟩
    rw [← lorentzPair_self, ← frameGram_pair, hGram, chartMetric_unit]
    norm_num
  rightDefinite := by
    apply FutureTimelike.posDef
    refine ⟨?_, ?_⟩
    · rw [steeringFrame_time]
      have ht : 0 < ((E * z.2) *ᵥ unitVector) 0 :=
        positive_time_unit (E * z.2) (by simpa [Matrix.mulVec_mulVec] using hpos.2.1)
      simpa [Matrix.mulVec_mulVec] using mul_pos (by norm_num : (0 : ℝ) < 1/2) ht
    · rw [steeringFrame_square]
      exact mul_pos (by norm_num) hpos.2.2
  normalized := by
    have hp := frame_probability E z.2 unitVector unitVector
    rw [hGram] at hp
    change localTrace _ _ = incidenceMass z at hp
    rw [hz.2] at hp
    rw [pauli_trace_product]
    apply Complex.ext
    · simpa only [localTrace_apply, pauli_trace_product, Complex.ofReal_re] using hp
    · simp

/-- Complete pointwise reconstruction into the actual fixed-qubit raw set. -/
theorem frame_table_mem_rawPOVM (E : M) (z : IncidenceSpace)
    (hGram : frameGram E = chartMetric z.1) (hz : FeasibleIncidence z)
    (hpos : FramePositive E z.2) :
    tableOfBlock (probabilityBlock z) ∈ rawPOVM binaryTernaryArchitecture := by
  let s := frameAssemblage E z hGram hz hpos
  have hp := s.behavior_mem_rawPOVM
  have heq : (fun x y a b => localTrace (s.left x a) (s.right y b)) =
      tableOfBlock (probabilityBlock z) := by
    funext x y a b
    change localTrace (pauli (E *ᵥ effectRay x a))
      (pauli (steeringFrame E z.2 *ᵥ effectRay y b)) = _
    rw [frame_probability, hGram]
    rfl
  rwa [heq] at hp

end Lorentz
end Bell
