import Bell.Expectation

/-!
# General finite rational Gram/SOS evaluation

The coefficient matrix is not assumed positive by an oracle: its explicit LDL
factorization and positive pivots will be supplied by `SOSCertificate`. This
module gives the generic algebraic bridge from those entries to actual positive
Born expectations. It does not assume any Bell upper bound.

STATUS: uncompiled proof source.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace Bell.SOS

/-- A finite Hermitian Gram expression in arbitrary joint operators. -/
def gram {n : ℕ} (Q : Matrix (Fin n) (Fin n) ℝ)
    (W : Fin n → JointOperator) : JointOperator :=
  ∑ i, ∑ j, Q i j • ((W i).conjTranspose * W j)

/-- The order of the factors in the explicit LDL coefficient formula. -/
def ldl {n : ℕ} (L : Matrix (Fin n) (Fin n) ℝ) (d : Fin n → ℝ) :
    Matrix (Fin n) (Fin n) ℝ :=
  fun i j => ∑ k, d k * L i k * L j k

theorem rotate_three_sums {ι κ τ E : Type*}
    [Fintype ι] [Fintype κ] [Fintype τ] [AddCommMonoid E]
    (f : ι → κ → τ → E) :
    (∑ i, ∑ j, ∑ k, f i j k) = ∑ k, ∑ i, ∑ j, f i j k := by
  calc
    (∑ i, ∑ j, ∑ k, f i j k) = ∑ i, ∑ k, ∑ j, f i j k := by
      apply Finset.sum_congr rfl
      intro i _
      exact Finset.sum_comm
    _ = ∑ k, ∑ i, ∑ j, f i j k := Finset.sum_comm

/-- An exact coefficient identity becomes a weighted sum of operator squares. -/
theorem gram_ldl {n : ℕ} (L : Matrix (Fin n) (Fin n) ℝ) (d : Fin n → ℝ)
    (W : Fin n → JointOperator) :
    gram (ldl L d) W =
      ∑ k, d k • ((∑ i, L i k • W i).conjTranspose * (∑ i, L i k • W i)) := by
  simp only [gram, ldl, Matrix.conjTranspose_sum, Matrix.conjTranspose_smul,
    star_trivial, Matrix.sum_mul, Matrix.mul_sum, Matrix.smul_mul, Matrix.mul_smul,
    Finset.sum_smul, Finset.smul_sum, smul_smul, mul_assoc]
  exact rotate_three_sums (fun i j k =>
    (d k * (L i k * L j k)) • ((W i).conjTranspose * W j))

/-- Positivity holds for every positive complex density matrix. -/
theorem expectation_gram_nonnegative {n : ℕ} (s : State)
    (Q L : Matrix (Fin n) (Fin n) ℝ) (d : Fin n → ℝ)
    (hQ : Q = ldl L d) (hd : ∀ k, 0 ≤ d k) (W : Fin n → JointOperator) :
    0 ≤ expectation s.density (gram Q W) := by
  rw [hQ, gram_ldl, map_sum]
  apply Finset.sum_nonneg
  intro k _
  rw [map_smul, smul_eq_mul]
  exact mul_nonneg (hd k)
    (state_expectation_square_nonneg s (∑ i, L i k • W i))

/-- A fixed operator SOS is enough for an upper bound on all states. -/
theorem upper_bound_of_gram {n : ℕ} (s : State) (C : ℝ) (B : JointOperator)
    (Q L : Matrix (Fin n) (Fin n) ℝ) (d : Fin n → ℝ)
    (hQ : Q = ldl L d) (hd : ∀ k, 0 ≤ d k) (W : Fin n → JointOperator)
    (hidentity : C • (1 : JointOperator) - B = gram Q W) :
    expectation s.density B ≤ C := by
  have hp := expectation_gram_nonnegative s Q L d hQ hd W
  rw [← hidentity, map_sub, map_smul, state_expectation_one, smul_eq_mul, mul_one] at hp
  linarith

end Bell.SOS
