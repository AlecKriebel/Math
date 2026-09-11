import Bell.Expectation

/-!
# Qubit PVM support without a rank/eigenvalue case enumeration

Cayley--Hamilton gives a short, purely algebraic proof that three pairwise
orthogonal, nonzero idempotents cannot normalize to the 2-by-2 identity.
Zero projectors and deterministic inputs are retained throughout.

Verification evidence: see CERTIFICATION.md and reports/kernel_report.json.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace Bell

/-- The 2-by-2 Cayley--Hamilton identity, proved entrywise over `ℂ`. -/
theorem qubit_cayley_hamilton (P : Operator) :
    P * P - Matrix.trace P • P + Matrix.det P • (1 : Operator) = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Matrix.trace_fin_two, Matrix.det_fin_two,
      Fin.sum_univ_two, Matrix.one_apply, smul_eq_mul] <;> ring

/-- A nonzero orthogonal partner forces an idempotent's determinant to vanish. -/
theorem orthogonal_idempotent_det_zero (P Q : Operator)
    (hPP : P * P = P) (hPQ : P * Q = 0) (hQ : Q ≠ 0) :
    Matrix.det P = 0 := by
  have h := congrArg (fun X : Operator => X * Q) (qubit_cayley_hamilton P)
  rw [hPP] at h
  have hz : Matrix.det P • Q = 0 := by
    simpa only [Matrix.add_mul, Matrix.sub_mul, Matrix.smul_mul,
      hPQ, Matrix.one_mul, Matrix.zero_mul, smul_zero, sub_self, zero_add] using h
  exact (smul_eq_zero.mp hz).resolve_right hQ

/-- A nonzero singular idempotent on a complex qubit has trace one. -/
theorem singular_idempotent_trace_one (P : Operator)
    (hPP : P * P = P) (hdet : Matrix.det P = 0) (hP : P ≠ 0) :
    Matrix.trace P = 1 := by
  have h := qubit_cayley_hamilton P
  rw [hPP, hdet, zero_smul, add_zero] at h
  have hs : (1 - Matrix.trace P) • P = 0 := by
    simpa only [sub_smul, one_smul] using h
  have := (smul_eq_zero.mp hs).resolve_right hP
  exact (sub_eq_zero.mp this).symm

/-- Every declared three-outcome qubit PVM has at least one zero effect. -/
theorem ternary_pvm_has_zero (M : PVM 3) :
    M.effect 0 = 0 ∨ M.effect 1 = 0 ∨ M.effect 2 = 0 := by
  by_contra h
  push_neg at h
  rcases h with ⟨h₀,h₁,h₂⟩
  have d₀ := orthogonal_idempotent_det_zero (M.effect 0) (M.effect 1)
    (M.idempotent 0) (M.orthogonal 0 1 (by decide)) h₁
  have d₁ := orthogonal_idempotent_det_zero (M.effect 1) (M.effect 0)
    (M.idempotent 1) (M.orthogonal 1 0 (by decide)) h₀
  have d₂ := orthogonal_idempotent_det_zero (M.effect 2) (M.effect 0)
    (M.idempotent 2) (M.orthogonal 2 0 (by decide)) h₀
  have t₀ := singular_idempotent_trace_one (M.effect 0) (M.idempotent 0) d₀ h₀
  have t₁ := singular_idempotent_trace_one (M.effect 1) (M.idempotent 1) d₁ h₁
  have t₂ := singular_idempotent_trace_one (M.effect 2) (M.idempotent 2) d₂ h₂
  have ht := congrArg Matrix.trace M.normalized
  norm_num [Fin.sum_univ_succ, Matrix.trace_add, t₀,t₁,t₂] at ht

/-- Self-adjointness plus squaring to one, with scalar involutions included. -/
structure QubitInvolution where
  matrix : Operator
  hermitian : matrix.conjTranspose = matrix
  sq_one : matrix * matrix = 1

/-- `2P-I` for any genuine orthogonal projection, including `P=0,I`. -/
def projectionInvolution (P : Operator) (hP : P.conjTranspose = P)
    (hid : P * P = P) : QubitInvolution where
  matrix := (2 : ℝ) • P - 1
  hermitian := by simp [hP]
  sq_one := by
    simp only [two_smul, Matrix.sub_mul, Matrix.mul_sub, Matrix.add_mul, Matrix.mul_add,
      Matrix.one_mul, Matrix.mul_one, hid]
    abel

def QubitInvolution.neg (A : QubitInvolution) : QubitInvolution where
  matrix := -A.matrix
  hermitian := by simp [A.hermitian]
  sq_one := by simpa using A.sq_one

/-- The sign convention assigning `+1` to every label except label one. -/
def pvmSignObservable {n : ℕ} (M : PVM n) (a : Fin n) : QubitInvolution :=
  (projectionInvolution (M.effect a) (M.positive a).isHermitian.eq
    (M.idempotent a)).neg

@[simp]
theorem pvmSignObservable_matrix {n : ℕ} (M : PVM n) (a : Fin n) :
    (pvmSignObservable M a).matrix = 1 - (2 : ℝ) • M.effect a := by
  dsimp [pvmSignObservable, projectionInvolution, QubitInvolution.neg]
  abel

end Bell
