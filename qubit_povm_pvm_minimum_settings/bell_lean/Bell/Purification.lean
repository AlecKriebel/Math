import Bell.QubitCoordinates

/-!
# Positive qubit assemblages and explicit two-qubit purification

For a full-rank common reduced state, every finite assemblage is realized by
one pure complex two-qubit state and a single complete POVM per input. The
construction retains all declared output labels, including zero effects.
-/
noncomputable section
open scoped Bell.Entrywise
open scoped BigOperators Matrix ComplexOrder
namespace Bell

/-- The local trace functional, bundled over the real scalars. -/
def localTrace (A : Operator) : Operator →ₗ[ℝ] ℝ where
  toFun B := (Matrix.trace (A * B)).re
  map_add' := by intro B C; simp [Matrix.mul_add, Matrix.trace_add]
  map_smul' := by intro t B; simp [Matrix.mul_smul, Matrix.trace_smul]

@[simp]
theorem localTrace_apply (A B : Operator) : localTrace A B = (Matrix.trace (A * B)).re := rfl

theorem localTrace_comm (A B : Operator) : localTrace A B = localTrace B A := by
  exact congrArg Complex.re (Matrix.trace_mul_comm A B)

theorem posSemidef_real_smul {n : Type*} [Fintype n] [DecidableEq n]
    {A : Matrix n n ℂ} (hA : A.PosSemidef) {t : ℝ} (ht : 0 ≤ t) :
    (t • A).PosSemidef := by
  refine ⟨?_, fun x => ?_⟩
  · change (t • A).conjTranspose = t • A
    simp [hA.isHermitian.eq]
  · have hc : (0 : ℂ) ≤ (t : ℂ) := by exact_mod_cast ht
    simpa [Matrix.smul_mulVec_assoc, dotProduct_smul, smul_eq_mul] using
      mul_nonneg hc (hA.2 x)

theorem localTrace_nonnegative {A B : Operator} (hA : A.PosSemidef) (hB : B.PosSemidef) :
    0 ≤ localTrace A B := by
  have hp := positive_trace_nonneg (hA.mul_mul_conjTranspose_same hB.sqrt)
  change 0 ≤ (Matrix.trace (A * B)).re
  rw [← hB.sqrt_mul_self, ← hB.posSemidef_sqrt.isHermitian.eq,
    Matrix.trace_mul_cycle']
  simpa [Matrix.mul_assoc, hB.posSemidef_sqrt.isHermitian.eq] using hp

/-- Coefficient matrix of a pure state, with joint index order explicit. -/
def pureDensity (C : Operator) : JointOperator :=
  fun i j => C i.1 i.2 * star (C j.1 j.2)

theorem pureDensity_positive (C : Operator) : (pureDensity C).PosSemidef := by
  let B : Matrix (Fin 1) Joint ℂ := fun _ i => star (C i.1 i.2)
  have hp := joint_gram_positive B
  convert hp using 1
  ext i j
  simp [pureDensity, B, Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ]

theorem pureDensity_trace (C : Operator) :
    Matrix.trace (pureDensity C) = Matrix.trace (C * C.conjTranspose) := by
  simp [pureDensity, Matrix.trace, Matrix.mul_apply, Matrix.conjTranspose_apply,
    Fintype.sum_prod_type, Fin.sum_univ_succ]

def pureState (C : Operator) (hC : Matrix.trace (C * C.conjTranspose) = 1) : State where
  density := pureDensity C
  positive := pureDensity_positive C
  normalized := (pureDensity_trace C).trans hC

/- Full complex Born identity; transposition on Bob is essential. -/
set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
theorem pureDensity_born (C M N : Operator) :
    born (pureDensity C) M N = localTrace M (C * N.transpose * C.conjTranspose) := by
  change (Matrix.trace (pureDensity C * tensor M N)).re =
    (Matrix.trace (M * (C * N.transpose * C.conjTranspose))).re
  unfold pureDensity tensor
  congr 1
  simp only [Matrix.trace, Matrix.diag, Matrix.mul_apply, Matrix.conjTranspose_apply,
    Matrix.transpose_apply, Fintype.sum_prod_type, Fin.sum_univ_succ]
  ring

/-- Common positive reduced operator and all input-dependent steered outcomes. -/
structure Assemblage (A : Architecture) where
  alice : (x : Fin A.aliceInputs) → POVM (A.aliceOutputs x)
  reduced : Operator
  reducedPositive : reduced.PosSemidef
  reducedNormalized : Matrix.trace reduced = 1
  steered : (y : Fin A.bobInputs) → Fin (A.bobOutputs y) → Operator
  positive : ∀ y b, (steered y b).PosSemidef
  commonSum : ∀ y, ∑ b, steered y b = reduced

def Assemblage.behavior {A : Architecture} (s : Assemblage A) : Behavior A :=
  fun x y a b => localTrace ((s.alice x).effect a) (s.steered y b)

def Assemblage.root {A : Architecture} (s : Assemblage A) : Operator :=
  s.reducedPositive.sqrt

theorem Assemblage.root_hermitian {A : Architecture} (s : Assemblage A) :
    s.root.conjTranspose = s.root := s.reducedPositive.posSemidef_sqrt.isHermitian.eq

theorem Assemblage.root_square {A : Architecture} (s : Assemblage A) :
    s.root * s.root = s.reduced := s.reducedPositive.sqrt_mul_self

theorem Assemblage.root_invertible {A : Architecture} (s : Assemblage A)
    (hρ : IsUnit s.reduced.det) : IsUnit s.root.det := by
  apply isUnit_iff_ne_zero.mpr
  intro hzero
  have hdet := congrArg Matrix.det s.root_square
  rw [Matrix.det_mul, hzero, zero_mul] at hdet
  exact (isUnit_iff_ne_zero.mp hρ) hdet.symm

def Assemblage.purifiedBob {A : Architecture} (s : Assemblage A)
    (hρ : IsUnit s.reduced.det) (y : Fin A.bobInputs) : POVM (A.bobOutputs y) where
  effect := fun b => (s.root⁻¹ * s.steered y b * s.root⁻¹.conjTranspose).transpose
  positive := fun b => ((s.positive y b).mul_mul_conjTranspose_same s.root⁻¹).transpose
  normalized := by
    rw [← Matrix.transpose_sum, ← Matrix.sum_mul, ← Matrix.mul_sum, s.commonSum y]
    have hC := s.root_invertible hρ
    have hback : s.root⁻¹ * s.reduced * s.root⁻¹.conjTranspose = 1 := by
      rw [← s.root_square, Matrix.conjTranspose_nonsing_inv, s.root_hermitian]
      simp only [← Matrix.mul_assoc, Matrix.nonsing_inv_mul s.root hC, one_mul,
        Matrix.mul_nonsing_inv s.root hC]
    rw [hback, Matrix.transpose_one]

def Assemblage.purifiedStrategy {A : Architecture} (s : Assemblage A)
    (hρ : IsUnit s.reduced.det) : Strategy A where
  state := pureState s.root (by rw [s.root_hermitian, s.root_square, s.reducedNormalized])
  alice := s.alice
  bob := s.purifiedBob hρ

/-- Every outcome is reconstructed simultaneously on the same purification. -/
theorem Assemblage.purified_behavior {A : Architecture} (s : Assemblage A)
    (hρ : IsUnit s.reduced.det) : (s.purifiedStrategy hρ).behavior = s.behavior := by
  funext x y a b
  change born (pureDensity s.root) ((s.alice x).effect a)
    ((s.root⁻¹ * s.steered y b * s.root⁻¹.conjTranspose).transpose) = _
  rw [pureDensity_born, Matrix.transpose_transpose]
  have hC := s.root_invertible hρ
  have hback : s.root * (s.root⁻¹ * s.steered y b * s.root⁻¹.conjTranspose) *
      s.root.conjTranspose = s.steered y b := by
    calc
      _ = (s.root * s.root⁻¹) * s.steered y b *
          (s.root⁻¹.conjTranspose * s.root.conjTranspose) := by noncomm_ring
      _ = s.steered y b := by
        rw [← Matrix.conjTranspose_mul, Matrix.mul_nonsing_inv _ hC,
          Matrix.conjTranspose_one, one_mul, mul_one]
  rw [hback]
  rfl

theorem Assemblage.mem_rawPOVM {A : Architecture} (s : Assemblage A)
    (hρ : IsUnit s.reduced.det) : s.behavior ∈ rawPOVM A :=
  ⟨s.purifiedStrategy hρ, s.purified_behavior hρ⟩

/-- An inverse square-root normalization on Alice and the compensating
congruence on the assemblage preserve every trace probability. -/
theorem inverse_congruence_trace (C A S : Operator) (hC : IsUnit C.det) :
    localTrace (C⁻¹.conjTranspose * A * C⁻¹) (C * S * C.conjTranspose) =
      localTrace A S := by
  simp only [localTrace_apply]
  have heq : C⁻¹.conjTranspose * A * C⁻¹ * (C * S * C.conjTranspose) =
      C⁻¹.conjTranspose * (A * S) * C.conjTranspose := by
    calc
      _ = C⁻¹.conjTranspose * A * (C⁻¹ * C) * S * C.conjTranspose := by noncomm_ring
      _ = _ := by rw [Matrix.nonsing_inv_mul _ hC]; noncomm_ring
  rw [heq, Matrix.trace_mul_comm]
  congr 1
  rw [← Matrix.mul_assoc, ← Matrix.conjTranspose_mul,
    Matrix.nonsing_inv_mul _ hC, Matrix.conjTranspose_one, one_mul]

end Bell
