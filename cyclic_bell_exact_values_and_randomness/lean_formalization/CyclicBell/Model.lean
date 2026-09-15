import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Matrix.Notation
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic

/-!
Coordinate physical model. SOURCE CANDIDATE: not yet compiled in the cloud.
The model is not qubit-specific and assumes no score, saturation, or table.
The finite tensor product is given by its computational-basis matrix entries.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell

abbrev Vec (n : ℕ) := Fin n → ℂ
abbrev Op (n : ℕ) := Matrix (Fin n) (Fin n) ℂ
abbrev Joint (nA nB : ℕ) := Fin nA × Fin nB
abbrev JointOp (nA nB : ℕ) := Matrix (Joint nA nB) (Joint nA nB) ℂ

/-- Conjugate-linear in the first argument. -/
def ip {ι : Type*} [Fintype ι] (u v : ι → ℂ) : ℂ :=
  ∑ j, star (u j) * v j

def applyOp {ι : Type*} [Fintype ι] (T : Matrix ι ι ℂ) (v : ι → ℂ) : ι → ℂ :=
  fun i => ∑ j, T i j * v j

def expectation {ι : Type*} [Fintype ι] (ψ : ι → ℂ) (T : Matrix ι ι ℂ) : ℂ :=
  ip ψ (applyOp T ψ)

/-- The outer product v v^dagger, not an assumed spectral projection. -/
def projector {ι : Type*} (v : ι → ℂ) : Matrix ι ι ℂ :=
  fun i j => v i * star (v j)

def tensor {nA nB : ℕ} (A : Op nA) (B : Op nB) : JointOp nA nB :=
  fun i j => A i.1 j.1 * B i.2 j.2

def tensorVec {nA nB : ℕ} (u : Vec nA) (v : Vec nB) : Joint nA nB → ℂ :=
  fun i => u i.1 * v i.2

structure State (nA nB : ℕ) where
  density : JointOp nA nB
  positive : density.PosSemidef
  normalized : Matrix.trace density = 1

/-- Zero effects are allowed. PosSemidef entails Hermiticity. -/
structure PVM (n : ℕ) where
  effect : Fin 4 → Op n
  positive : ∀ a, (effect a).PosSemidef
  complete : ∑ a, effect a = 1
  idempotent : ∀ a, effect a * effect a = effect a
  orthogonal : ∀ a b, a ≠ b → effect a * effect b = 0

/-- Four-outcome measurement encoding, with the manuscript's positive sign. -/
def observable {n : ℕ} (M : PVM n) : Op n :=
  ∑ a, (Complex.I ^ a.val) • M.effect a

structure Strategy (aliceInputs nA nB : ℕ) where
  state : State nA nB
  alice : Fin aliceInputs → PVM nA
  bob : Fin 5 → PVM nB

/-- Standard trace-form mixed-state Born probability. -/
def born {nA nB : ℕ} (ρ : JointOp nA nB) (M : Op nA) (N : Op nB) : ℝ :=
  (Matrix.trace (ρ * tensor M N)).re

/-- Pure-state Born probability, defined before and independently of the witness. -/
def pureBorn {nA nB : ℕ} (ψ : Joint nA nB → ℂ) (M : Op nA) (N : Op nB) : ℝ :=
  (expectation ψ (tensor M N)).re

/-- Always guess one fixed output pair; this is a trivial-Eve success probability. -/
def fixedGuessSuccess (p : Fin 4 → Fin 4 → ℝ) (a b : Fin 4) : ℝ := p a b

theorem ip_star {ι : Type*} [Fintype ι] (u v : ι → ℂ) :
    star (ip u v) = ip v u := by
  simp [ip, mul_comm]

theorem ip_mul_right {ι : Type*} [Fintype ι] (u v : ι → ℂ) (z : ℂ) :
    ip u (fun i => v i * z) = ip u v * z := by
  simp only [ip, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem projector_apply {ι : Type*} [Fintype ι] (u v : ι → ℂ) :
    applyOp (projector u) v = fun i => u i * ip u v := by
  funext i
  simp only [applyOp, projector, ip, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem expectation_projector {ι : Type*} [Fintype ι] (ψ u : ι → ℂ) :
    expectation ψ (projector u) = star (ip u ψ) * ip u ψ := by
  unfold expectation
  rw [projector_apply, ip_mul_right, ← ip_star u ψ]

theorem tensor_projectors {nA nB : ℕ} (u : Vec nA) (v : Vec nB) :
    tensor (projector u) (projector v) = projector (tensorVec u v) := by
  ext i j
  simp only [tensor, projector, tensorVec, star_mul]
  ring

/-- The physical Born expression, not a stipulated Fourier table, reduces to
    a rank-one joint amplitude. -/
theorem pureBorn_projectors {nA nB : ℕ} (ψ : Joint nA nB → ℂ)
    (u : Vec nA) (v : Vec nB) :
    pureBorn ψ (projector u) (projector v) =
      Complex.normSq (ip (tensorVec u v) ψ) := by
  unfold pureBorn
  rw [tensor_projectors, expectation_projector]
  simpa only [Complex.ofReal_re] using
    (congrArg Complex.re
      (Complex.normSq_eq_conj_mul_self (z := ip (tensorVec u v) ψ))).symm

/-- Trace-form and vector-form Born rules agree for the pure-state density. -/
theorem expectation_eq_trace {ι : Type*} [Fintype ι] (ψ : ι → ℂ)
    (T : Matrix ι ι ℂ) :
    expectation ψ T = Matrix.trace (projector ψ * T) := by
  classical
  simp only [expectation, ip, applyOp, Matrix.trace, Matrix.diag_apply, Matrix.mul_apply,
    projector, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem pureBorn_eq_born {nA nB : ℕ} (ψ : Joint nA nB → ℂ)
    (M : Op nA) (N : Op nB) :
    pureBorn ψ M N = born (projector ψ) M N := by
  unfold pureBorn born
  rw [expectation_eq_trace]

theorem projector_positive {ι : Type*} [Fintype ι] (v : ι → ℂ) :
    (projector v).PosSemidef := by
  let R : Matrix (Fin 1) ι ℂ := fun _ j => star (v j)
  have hR : R.conjTranspose * R = projector v := by
    ext i j
    simp [R, Matrix.mul_apply, Matrix.conjTranspose_apply, projector]
  rw [← hR]
  exact Matrix.posSemidef_conjTranspose_mul_self R

theorem projector_mul {ι : Type*} [Fintype ι] (u v : ι → ℂ) :
    projector u * projector v = fun i j => u i * ip u v * star (v j) := by
  ext i j
  simp only [Matrix.mul_apply, projector, ip, Finset.mul_sum, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro k _
  ring

/-- A PVM constructed from a complete orthonormal basis. This constructor
    carries no Bell-value or target-probability hypotheses. -/
def pvmOfBasis {n : ℕ} (w : Fin 4 → Vec n)
    (hor : ∀ a b, ip (w a) (w b) = if a = b then 1 else 0)
    (hc : ∑ a, projector (w a) = 1) : PVM n where
  effect := fun a => projector (w a)
  positive := fun a => projector_positive (w a)
  complete := hc
  idempotent := by
    intro a
    rw [projector_mul]
    ext i j
    simp [hor, projector]
  orthogonal := by
    intro a b hab
    rw [projector_mul]
    ext i j
    simp [hor, hab]

/-- Any normalized pure vector supplies an honest positive trace-one density. -/
def stateOfPure {nA nB : ℕ} (ψ : Joint nA nB → ℂ) (hψ : ip ψ ψ = 1) :
    State nA nB where
  density := projector ψ
  positive := projector_positive ψ
  normalized := by
    simpa [Matrix.trace, projector, ip, mul_comm] using hψ

end CyclicBell
