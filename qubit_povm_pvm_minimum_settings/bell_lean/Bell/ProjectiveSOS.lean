import Bell.SOSCertificate
import Bell.ProjectionSupport

/-!
# A stronger rational PVM Bell upper bound by explicit SOS

The universal operator inequalities in this file require only five Hermitian
involutions with Alice--Bob tensor separation. No Schmidt parametrization,
maximization oracle, or numerical SDP assertion is used in their proof bodies.

Numerical optimization was used only to discover a candidate rational Gram
matrix. `SOSCertificate.coefficient_factorization` and the operator identity
below are the independent exact proof obligations.

STATUS: uncompiled proof source.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace Bell.SOS

abbrev AliceObservables := Fin 3 → QubitInvolution
abbrev BobObservables := Fin 2 → QubitInvolution

def chsh (A : AliceObservables) (B : BobObservables) : JointOperator :=
  tensor (A 0).matrix ((B 0).matrix + (B 1).matrix) +
  tensor (A 1).matrix ((B 0).matrix - (B 1).matrix)

/-- The auxiliary pair containing labels 0 and 2. -/
def bell02 (A : AliceObservables) (B : BobObservables) : JointOperator :=
  (7/20 : ℝ) • (1 : JointOperator) + (10 : ℝ) • chsh A B +
  (3/20 : ℝ) • tensor 1 (B 0).matrix +
  (1/5 : ℝ) • tensor 1 (B 1).matrix -
  (1/20 : ℝ) • tensor (A 2).matrix 1 +
  (3/20 : ℝ) • tensor (A 2).matrix (B 0).matrix -
  (1/5 : ℝ) • tensor (A 2).matrix (B 1).matrix

/-- The auxiliary pair containing labels 0 and 1. -/
def bell01 (A : AliceObservables) (B : BobObservables) : JointOperator :=
  (10 : ℝ) • chsh A B +
  (3/10 : ℝ) • ((1 : JointOperator) + tensor (A 2).matrix (B 0).matrix)

/-- All twelve words are products of at most one observable from each party. -/
def words (A : AliceObservables) (B : BobObservables) : Fin 12 → JointOperator :=
  ![tensor 1 1,
    tensor (A 0).matrix 1, tensor (A 1).matrix 1, tensor (A 2).matrix 1,
    tensor 1 (B 0).matrix, tensor 1 (B 1).matrix,
    tensor (A 0).matrix (B 0).matrix, tensor (A 0).matrix (B 1).matrix,
    tensor (A 1).matrix (B 0).matrix, tensor (A 1).matrix (B 1).matrix,
    tensor (A 2).matrix (B 0).matrix, tensor (A 2).matrix (B 1).matrix]

theorem words_hermitian (A : AliceObservables) (B : BobObservables) (i : Fin 12) :
    (words A B i).conjTranspose = words A B i := by
  fin_cases i <;> simp [words, (A 0).hermitian, (A 1).hermitian,
    (A 2).hermitian, (B 0).hermitian, (B 1).hermitian]

set_option maxHeartbeats 0 in
/-- The independently checked noncommutative coefficient identity. -/
theorem bell02_certificate (A : AliceObservables) (B : BobObservables) :
    (289/10 : ℝ) • (1 : JointOperator) - bell02 A B = gram Q (words A B) := by
  simp only [gram, words_hermitian]
  norm_num [Q, numerator, words, Fin.sum_univ_succ, tensor_mul,
    (A 0).sq_one, (A 1).sq_one, (A 2).sq_one,
    (B 0).sq_one, (B 1).sq_one, bell02, chsh]
  ext i j
  norm_num [Matrix.add_apply, Matrix.sub_apply, Matrix.smul_apply,
    Pi.smul_apply, Complex.real_smul]
  ring

/-- Uniform in the state and all five observables, including scalar degeneracies. -/
theorem bell02_upper (s : State) (A : AliceObservables) (B : BobObservables) :
    expectation s.density (bell02 A B) ≤ 289/10 :=
  upper_bound_of_gram s (289/10) (bell02 A B) Q L d
    coefficient_factorization (fun k => le_of_lt (pivot_positive k))
    (words A B) (bell02_certificate A B)

/-- The three short square factors for the remaining pair. -/
def smallSquare0 (A : AliceObservables) (B : BobObservables) : JointOperator :=
  (7/5 : ℝ) • tensor (A 0).matrix 1 - tensor 1 (B 0).matrix - tensor 1 (B 1).matrix

def smallSquare1 (A : AliceObservables) (B : BobObservables) : JointOperator :=
  (7/5 : ℝ) • tensor (A 1).matrix 1 - tensor 1 (B 0).matrix + tensor 1 (B 1).matrix

def smallSquare2 (A : AliceObservables) (B : BobObservables) : JointOperator :=
  (1 : JointOperator) - tensor (A 2).matrix (B 0).matrix

set_option maxHeartbeats 0 in
/-- A rational CHSH square identity plus a positive remainder of exactly 1/70. -/
theorem bell01_certificate (A : AliceObservables) (B : BobObservables) :
    (289/10 : ℝ) • (1 : JointOperator) - bell01 A B =
      (25/7 : ℝ) • ((smallSquare0 A B).conjTranspose * smallSquare0 A B) +
      (25/7 : ℝ) • ((smallSquare1 A B).conjTranspose * smallSquare1 A B) +
      (3/20 : ℝ) • ((smallSquare2 A B).conjTranspose * smallSquare2 A B) +
      (1/70 : ℝ) • (1 : JointOperator) := by
  simp only [smallSquare0, smallSquare1, smallSquare2, bell01, chsh,
    Matrix.conjTranspose_add, Matrix.conjTranspose_sub, Matrix.conjTranspose_smul,
    star_trivial, Matrix.conjTranspose_one, tensor_conjTranspose,
    (A 0).hermitian, (A 1).hermitian, (A 2).hermitian,
    (B 0).hermitian, (B 1).hermitian,
    Matrix.add_mul, Matrix.sub_mul, Matrix.mul_add, Matrix.mul_sub,
    Matrix.smul_mul, Matrix.mul_smul, smul_smul,
    tensor_mul, (A 0).sq_one, (A 1).sq_one, (A 2).sq_one,
    (B 0).sq_one, (B 1).sq_one, Matrix.one_mul, Matrix.mul_one,
    tensor_add_left, tensor_add_right, tensor_sub_left, tensor_sub_right, tensor_one_one]
  ext i j
  norm_num [Matrix.add_apply, Matrix.sub_apply, Matrix.smul_apply,
    Pi.smul_apply, Complex.real_smul]
  ring

theorem bell01_upper (s : State) (A : AliceObservables) (B : BobObservables) :
    expectation s.density (bell01 A B) ≤ 289/10 := by
  have h0 := state_expectation_square_nonneg s (smallSquare0 A B)
  have h1 := state_expectation_square_nonneg s (smallSquare1 A B)
  have h2 := state_expectation_square_nonneg s (smallSquare2 A B)
  have hi := congrArg (expectation s.density) (bell01_certificate A B)
  simp only [map_sub, map_add, map_smul, state_expectation_one, smul_eq_mul, mul_one] at hi
  linarith

/-- Relabeling which handles auxiliary support {1,2} with the same Gram matrix. -/
def switchedAlice (A : AliceObservables) : AliceObservables :=
  ![(A 1).neg, (A 0).neg, A 2]

def switchedBob (B : BobObservables) : BobObservables :=
  ![(B 0).neg, B 1]

theorem chsh_switch (A : AliceObservables) (B : BobObservables) :
    chsh (switchedAlice A) (switchedBob B) = chsh A B := by
  norm_num [chsh, switchedAlice, switchedBob, QubitInvolution.neg]
  abel

end Bell.SOS
