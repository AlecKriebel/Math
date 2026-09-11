import Bell.Quantum

/-!
# Positive expectations and tensor algebra

All operators below act on the actual complex-qubit spaces from `Bell.Quantum`.
The positivity of a state's functional is proved from its positive-semidefinite
matrix, rather than being added as a hypothesis to the final Bell theorem.

STATUS: proof source, not yet checked by a Lean compiler in this environment.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace Bell

@[simp]
theorem tensor_add_left (A C B : Operator) :
    tensor (A + C) B = tensor A B + tensor C B := by
  ext i j
  simp [tensor, add_mul]

@[simp]
theorem tensor_add_right (A B D : Operator) :
    tensor A (B + D) = tensor A B + tensor A D := by
  ext i j
  simp [tensor, mul_add]

@[simp]
theorem tensor_sub_left (A C B : Operator) :
    tensor (A - C) B = tensor A B - tensor C B := by
  ext i j
  simp [tensor, sub_mul]

@[simp]
theorem tensor_sub_right (A B D : Operator) :
    tensor A (B - D) = tensor A B - tensor A D := by
  ext i j
  simp [tensor, mul_sub]

@[simp]
theorem tensor_smul_left (r : ℝ) (A B : Operator) :
    tensor (r • A) B = r • tensor A B := by
  ext i j
  simp [tensor, smul_mul_assoc, mul_assoc]

@[simp]
theorem tensor_smul_right (r : ℝ) (A B : Operator) :
    tensor A (r • B) = r • tensor A B := by
  ext i j
  simp [tensor, mul_smul_comm, mul_left_comm]

@[simp]
theorem tensor_zero_left (B : Operator) : tensor 0 B = 0 := by
  ext i j
  simp [tensor]

@[simp]
theorem tensor_zero_right (A : Operator) : tensor A 0 = 0 := by
  ext i j
  simp [tensor]

@[simp]
theorem tensor_neg_left (A B : Operator) : tensor (-A) B = -tensor A B := by
  ext i j
  simp [tensor]

@[simp]
theorem tensor_neg_right (A B : Operator) : tensor A (-B) = -tensor A B := by
  ext i j
  simp [tensor]

@[simp]
theorem tensor_one_one : tensor (1 : Operator) 1 = 1 := by
  ext i j
  simp only [tensor, Matrix.one_apply, Prod.ext_iff]
  split_ifs <;> simp_all

/-- Multiplication preserves the tensor-factor order on each party. -/
theorem tensor_mul (A B C D : Operator) :
    tensor A B * tensor C D = tensor (A * C) (B * D) := by
  ext i j
  simp only [tensor, Matrix.mul_apply, Fintype.sum_prod_type, Fin.sum_univ_two]
  ring

@[simp]
theorem tensor_conjTranspose (A B : Operator) :
    (tensor A B).conjTranspose = tensor A.conjTranspose B.conjTranspose := by
  ext i j
  simp [tensor, Matrix.conjTranspose_apply, mul_comm]

/-- Tensor bilinearity over arbitrary finite outcome alphabets. -/
theorem tensor_sum_left {ι : Type*} (s : Finset ι) (A : ι → Operator) (B : Operator) :
    tensor (∑ i ∈ s, A i) B = ∑ i ∈ s, tensor (A i) B := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert i s hi ih => simp [hi, ih]

theorem tensor_sum_right {ι : Type*} (s : Finset ι) (A : Operator) (B : ι → Operator) :
    tensor A (∑ i ∈ s, B i) = ∑ i ∈ s, tensor A (B i) := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert i s hi ih => simp [hi, ih]

/-- The real part, packaged explicitly for finite-sum proofs. -/
def realPart : ℂ →ₗ[ℝ] ℝ where
  toFun := Complex.re
  map_add' := by intros; simp
  map_smul' := by intros; simp

/-- A positive-semidefinite complex matrix has nonnegative real trace. -/
theorem positive_trace_nonneg {n : Type*} [Fintype n] [DecidableEq n]
    {A : Matrix n n ℂ} (hA : A.PosSemidef) : 0 ≤ (Matrix.trace A).re := by
  have hdiag (i : n) : 0 ≤ (A i i).re := by
    simpa only [Matrix.mulVec_single_one, ← Pi.single_star, star_one, single_dotProduct, one_mul, Matrix.transpose_apply] using hA.re_dotProduct_nonneg (Pi.single i (1 : ℂ))
  change 0 ≤ realPart (∑ i, A i i)
  rw [map_sum]
  exact Finset.sum_nonneg (fun i _ => hdiag i)

/-- Born expectation as an actual real-linear functional. -/
def expectation (ρ : JointOperator) : JointOperator →ₗ[ℝ] ℝ where
  toFun X := (Matrix.trace (ρ * X)).re
  map_add' := by
    intro X Y
    simp [Matrix.mul_add, Matrix.trace_add]
  map_smul' := by
    intro r X
    simp [Matrix.mul_smul, Matrix.trace_smul]

@[simp]
theorem expectation_apply (ρ X : JointOperator) :
    expectation ρ X = (Matrix.trace (ρ * X)).re := rfl

@[simp]
theorem state_expectation_one (s : State) : expectation s.density 1 = 1 := by
  simp [expectation, s.normalized]

/-- This is the positivity premise needed by every SOS evaluation. -/
theorem state_expectation_square_nonneg (s : State) (X : JointOperator) :
    0 ≤ expectation s.density (X.conjTranspose * X) := by
  have hp := positive_trace_nonneg (s.positive.mul_mul_conjTranspose_same X)
  change 0 ≤ (Matrix.trace (s.density * (X.conjTranspose * X))).re
  rw [Matrix.trace_mul_cycle']
  simpa only [Matrix.mul_assoc] using hp

theorem state_expectation_positive (s : State) {X : JointOperator}
    (hX : X.PosSemidef) : 0 ≤ expectation s.density X := by
  have h := state_expectation_square_nonneg s hX.sqrt
  rw [hX.posSemidef_sqrt.isHermitian.eq, hX.sqrt_mul_self] at h
  exact h

/-- Tensor positivity follows from actual complex Gram factorizations. -/
theorem tensor_positive {A B : Operator} (hA : A.PosSemidef) (hB : B.PosSemidef) :
    (tensor A B).PosSemidef := by
  let X := tensor hA.sqrt hB.sqrt
  have hX : (X.conjTranspose * X).PosSemidef := by
    exact Matrix.posSemidef_conjTranspose_mul_self X
  have heq : X.conjTranspose * X = tensor A B := by
    dsimp [X]
    rw [tensor_conjTranspose, hA.posSemidef_sqrt.isHermitian.eq,
      hB.posSemidef_sqrt.isHermitian.eq, tensor_mul,
      hA.sqrt_mul_self, hB.sqrt_mul_self]
  rwa [heq] at hX

/-- Nonnegativity of every physical joint probability. -/
theorem born_nonnegative (s : State) {A B : Operator}
    (hA : A.PosSemidef) (hB : B.PosSemidef) : 0 ≤ born s.density A B := by
  exact state_expectation_positive s (tensor_positive hA hB)

@[simp]
theorem born_eq_expectation (ρ : JointOperator) (A B : Operator) :
    born ρ A B = expectation ρ (tensor A B) := rfl

theorem born_sum_alice (s : State) {n : ℕ} (M : POVM n) (B : Operator) :
    (∑ a, born s.density (M.effect a) B) = expectation s.density (tensor 1 B) := by
  simp only [born_eq_expectation, ← map_sum, ← tensor_sum_left, M.normalized]

theorem born_sum_bob (s : State) (A : Operator) {n : ℕ} (N : POVM n) :
    (∑ b, born s.density A (N.effect b)) = expectation s.density (tensor A 1) := by
  simp only [born_eq_expectation, ← map_sum, ← tensor_sum_right, N.normalized]

theorem born_normalization (s : State) {m n : ℕ} (M : POVM m) (N : POVM n) :
    (∑ a, ∑ b, born s.density (M.effect a) (N.effect b)) = 1 := by
  simp only [born_sum_bob, ← map_sum, ← tensor_sum_left, M.normalized,
    tensor_one_one, state_expectation_one]

/-- The fully physical behavior is a normalized nonsignaling table. -/
theorem strategy_behavior_nonnegative {A : Architecture} (s : Strategy A)
    (x y a b) : 0 ≤ s.behavior x y a b :=
  born_nonnegative s.state ((s.alice x).positive a) ((s.bob y).positive b)

theorem strategy_behavior_normalization {A : Architecture} (s : Strategy A) (x y) :
    (∑ a, ∑ b, s.behavior x y a b) = 1 :=
  born_normalization s.state (s.alice x) (s.bob y)

theorem strategy_no_signaling_to_alice {A : Architecture} (s : Strategy A)
    (x y y' a) :
    (∑ b, s.behavior x y a b) = ∑ b, s.behavior x y' a b := by
  simp only [Strategy.behavior, born_sum_bob]

theorem strategy_no_signaling_to_bob {A : Architecture} (s : Strategy A)
    (x x' y b) :
    (∑ a, s.behavior x y a b) = ∑ a, s.behavior x' y a b := by
  simp only [Strategy.behavior, born_sum_alice]

end Bell
