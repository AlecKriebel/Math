import CyclicBell.Attainment

/-! Explicit one-dimensional Eve. These are actual positive scalar-matrix POVM
effects, not an optimization over compatible realizations. The conditional
scalar density for output (a,b) has trace p(a,b).
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell

def behavior {inputs nA nB : ℕ} (σ : Strategy inputs nA nB)
    (x : Fin inputs) (y : Fin 5) (a b : Fin 4) : ℝ :=
  born σ.state.density ((σ.alice x).effect a) ((σ.bob y).effect b)

def targetDistribution {inputs nA nB : ℕ} (σ : Strategy inputs nA nB)
    (x : Fin inputs) : Fin 4 → Fin 4 → ℝ := behavior σ x 4

/-- On a one-dimensional space, always return the pair g. -/
def trivialEveEffect (g : Fin 4 × Fin 4) (a b : Fin 4) : Op 1 :=
  if (a,b) = g then 1 else 0

def trivialConditional (p : Fin 4 → Fin 4 → ℝ) (a b : Fin 4) : Op 1 :=
  (p a b : ℂ) • 1

def trivialEveSuccess (p : Fin 4 → Fin 4 → ℝ) (g : Fin 4 × Fin 4) : ℝ :=
  (∑ a : Fin 4, ∑ b : Fin 4,
    (Matrix.trace (trivialEveEffect g a b * trivialConditional p a b)).re)

theorem trivialEve_positive (g : Fin 4 × Fin 4) (a b : Fin 4) :
    (trivialEveEffect g a b).PosSemidef := by
  unfold trivialEveEffect
  split
  · exact Matrix.PosSemidef.one
  · exact Matrix.PosSemidef.zero

theorem trivialEve_complete (g : Fin 4 × Fin 4) :
    (∑ a : Fin 4, ∑ b : Fin 4, trivialEveEffect g a b) = 1 := by
  rcases g with ⟨a,b⟩
  simp [trivialEveEffect, Prod.mk.injEq, ite_and]

theorem trivialConditional_trace (p : Fin 4 → Fin 4 → ℝ) (a b : Fin 4) :
    Matrix.trace (trivialConditional p a b) = (p a b : ℂ) := by
  simp [trivialConditional, Matrix.trace, Matrix.diag_apply, Fin.sum_univ_succ]

theorem trivialConditional_positive (p : Fin 4 → Fin 4 → ℝ)
    (hp : ∀ a b, 0 ≤ p a b) (a b : Fin 4) :
    (trivialConditional p a b).PosSemidef := by
  have he : trivialConditional p a b = Matrix.diagonal (fun _ : Fin 1 => (p a b : ℂ)) := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [trivialConditional]
  rw [he]
  apply Matrix.posSemidef_diagonal_iff.mpr
  intro i
  exact_mod_cast hp a b

theorem trivialEve_success_eq (p : Fin 4 → Fin 4 → ℝ) (g : Fin 4 × Fin 4) :
    trivialEveSuccess p g = p g.1 g.2 := by
  rcases g with ⟨a,b⟩
  simp [trivialEveSuccess, trivialEveEffect, Prod.mk.injEq, ite_and,
    apply_ite, trivialConditional_trace]

/-- An explicit normalization check for the conditional Eve states. -/
theorem trivialConditional_total (p : Fin 4 → Fin 4 → ℝ)
    (hp : (∑ a : Fin 4, ∑ b : Fin 4, p a b) = 1) :
    (∑ a : Fin 4, ∑ b : Fin 4, trivialConditional p a b) = (1 : Op 1) := by
  unfold trivialConditional
  simp_rw [← Finset.sum_smul]
  have hc : (∑ a : Fin 4, ∑ b : Fin 4, (p a b : ℂ)) = 1 := by exact_mod_cast hp
  rw [hc, one_smul]

/-! Physical bridge for a genuinely adjoined one-dimensional Eve system. -/

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- R tensor I_E with E=C^1; the unique Eve index is kept explicit. -/
def adjoinTrivialEve (R : Matrix ι ι ℂ) : Matrix (ι × Fin 1) (ι × Fin 1) ℂ :=
  fun i j => R i.1 j.1

def partialTraceToTrivialEve (R : Matrix (ι × Fin 1) (ι × Fin 1) ℂ) : Op 1 :=
  fun e f => ∑ i : ι, R (i,e) (i,f)

def actualTrivialConditional (ρ T : Matrix ι ι ℂ) : Op 1 :=
  partialTraceToTrivialEve
    (adjoinTrivialEve T * adjoinTrivialEve ρ * (adjoinTrivialEve T).conjTranspose)

theorem adjoinTrivialEve_projector (ψ : ι → ℂ) :
    adjoinTrivialEve (projector ψ) = projector (fun i : ι × Fin 1 => ψ i.1) := rfl

theorem adjoinTrivialEve_mul (R S : Matrix ι ι ℂ) :
    adjoinTrivialEve (R * S) = adjoinTrivialEve R * adjoinTrivialEve S := by
  ext i j
  simp [adjoinTrivialEve, Matrix.mul_apply, Fintype.sum_prod_type, Fin.sum_univ_succ]

theorem adjoinTrivialEve_adjoint (R : Matrix ι ι ℂ) :
    adjoinTrivialEve R.conjTranspose = (adjoinTrivialEve R).conjTranspose := by
  ext i j
  rfl

theorem adjoinTrivialEve_positive {ρ : Matrix ι ι ℂ} (hρ : ρ.PosSemidef) :
    (adjoinTrivialEve ρ).PosSemidef :=
  hρ.submatrix (fun i : ι × Fin 1 => i.1)

theorem adjoinTrivialEve_trace (ρ : Matrix ι ι ℂ) :
    Matrix.trace (adjoinTrivialEve ρ) = Matrix.trace ρ := by
  simp [Matrix.trace, Matrix.diag_apply, adjoinTrivialEve,
    Fintype.sum_prod_type, Fin.sum_univ_succ]

theorem partialTrace_adjoin (R : Matrix ι ι ℂ) :
    partialTraceToTrivialEve (adjoinTrivialEve R) = Matrix.trace R • (1 : Op 1) := by
  ext e f
  fin_cases e <;> fin_cases f
  simp [partialTraceToTrivialEve, adjoinTrivialEve, Matrix.trace, Matrix.diag_apply]

/-- Sandwiching the actual joint state and tracing AB gives the Born scalar.
The identity is false for an arbitrary nonprojective T; idempotence is used. -/
theorem actualTrivialConditional_eq {ρ T : Matrix ι ι ℂ}
    (hρ : ρ.IsHermitian) (hT : T.IsHermitian) (hidem : T * T = T) :
    actualTrivialConditional ρ T =
      (((Matrix.trace (ρ * T)).re : ℝ) : ℂ) • (1 : Op 1) := by
  have ht : Matrix.trace (T * ρ * T.conjTranspose) = Matrix.trace (ρ * T) := by
    rw [hT.eq, Matrix.trace_mul_comm, ← mul_assoc, hidem, Matrix.trace_mul_comm]
  have hreal : star (Matrix.trace (ρ * T)) = Matrix.trace (ρ * T) := by
    rw [← Matrix.trace_conjTranspose, Matrix.conjTranspose_mul, hρ.eq, hT.eq,
      Matrix.trace_mul_comm]
  have hi : (Matrix.trace (ρ * T)).im = 0 := by
    have hh : -(Matrix.trace (ρ * T)).im = (Matrix.trace (ρ * T)).im := by
      simpa using congrArg Complex.im hreal
    linarith
  have hre : Matrix.trace (ρ * T) = (((Matrix.trace (ρ * T)).re : ℝ) : ℂ) := by
    apply Complex.ext <;> simp [hi]
  unfold actualTrivialConditional
  rw [← adjoinTrivialEve_adjoint, ← adjoinTrivialEve_mul, ← adjoinTrivialEve_mul,
    partialTrace_adjoin, ht, hre]
  simp

/-- All physical projectors, not only the explicit witness, satisfy the bridge. -/
theorem pvm_trivialEve_Born_bridge {nA nB : ℕ} (ρ : State nA nB)
    (M : PVM nA) (N : PVM nB) (a b : Fin 4) :
    actualTrivialConditional ρ.density (tensor (M.effect a) (N.effect b)) =
      (born ρ.density (M.effect a) (N.effect b) : ℂ) • (1 : Op 1) := by
  apply actualTrivialConditional_eq ρ.positive.isHermitian
  · change (tensor (M.effect a) (N.effect b)).conjTranspose = _
    rw [tensor_adjoint, (M.positive a).isHermitian.eq, (N.positive b).isHermitian.eq]
  · rw [tensor_mul, M.idempotent, N.idempotent]

end CyclicBell
