import Mathlib

/-!
# The physical model (paper §2)

Complex, not merely real, qubits.  There is no ancillary Hilbert space.
Zero effects and zero projectors are allowed.  The two convex hulls are separate
from the raw strategy images.  No equality between the raw images is asserted.

STATUS: proof source; this release has NOT been compiled by Lean.
-/

noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace Bell

abbrev Qubit := Fin 2
abbrev Joint := Qubit × Qubit
abbrev Operator := Matrix Qubit Qubit ℂ
abbrev JointOperator := Matrix Joint Joint ℂ

/-- The tensor product, with its basis order explicit. -/
def tensor (A B : Operator) : JointOperator :=
  fun i j => A i.1 j.1 * B i.2 j.2

structure State where
  density : JointOperator
  positive : density.PosSemidef
  normalized : Matrix.trace density = 1

structure POVM (n : ℕ) where
  effect : Fin n → Operator
  positive : ∀ a, (effect a).PosSemidef
  normalized : ∑ a, effect a = 1

structure PVM (n : ℕ) extends POVM n where
  idempotent : ∀ a, effect a * effect a = effect a
  orthogonal : ∀ a b, a ≠ b → effect a * effect b = 0

structure Architecture where
  aliceInputs : ℕ
  bobInputs : ℕ
  aliceOutputs : Fin aliceInputs → ℕ
  bobOutputs : Fin bobInputs → ℕ

abbrev Behavior (A : Architecture) :=
  (x : Fin A.aliceInputs) → (y : Fin A.bobInputs) →
    Fin (A.aliceOutputs x) → Fin (A.bobOutputs y) → ℝ

/-- The real part is redundant for valid states/effects, but defines the ambient
real behavior map without requiring a proof argument at every evaluation. -/
def born (ρ : JointOperator) (M N : Operator) : ℝ :=
  (Matrix.trace (ρ * tensor M N)).re

structure Strategy (A : Architecture) where
  state : State
  alice : (x : Fin A.aliceInputs) → POVM (A.aliceOutputs x)
  bob : (y : Fin A.bobInputs) → POVM (A.bobOutputs y)

structure ProjectiveStrategy (A : Architecture) where
  state : State
  alice : (x : Fin A.aliceInputs) → PVM (A.aliceOutputs x)
  bob : (y : Fin A.bobInputs) → PVM (A.bobOutputs y)

def Strategy.behavior {A : Architecture} (s : Strategy A) : Behavior A :=
  fun x y a b => born s.state.density ((s.alice x).effect a) ((s.bob y).effect b)

def ProjectiveStrategy.toStrategy {A : Architecture}
    (s : ProjectiveStrategy A) : Strategy A where
  state := s.state
  alice := fun x => (s.alice x).toPOVM
  bob := fun y => (s.bob y).toPOVM

def rawPOVM (A : Architecture) : Set (Behavior A) :=
  Set.range (Strategy.behavior (A := A))

def rawPVM (A : Architecture) : Set (Behavior A) :=
  Set.range (fun s : ProjectiveStrategy A => s.toStrategy.behavior)

def convexPOVM (A : Architecture) : Set (Behavior A) :=
  convexHull ℝ (rawPOVM A)

def convexPVM (A : Architecture) : Set (Behavior A) :=
  convexHull ℝ (rawPVM A)

theorem rawPVM_subset_rawPOVM (A : Architecture) : rawPVM A ⊆ rawPOVM A := by
  rintro p ⟨s, rfl⟩
  exact ⟨s.toStrategy, rfl⟩

theorem convexPVM_subset_convexPOVM (A : Architecture) :
    convexPVM A ⊆ convexPOVM A := by
  exact convexHull_mono (rawPVM_subset_rawPOVM A)

/-- A rectangular Gram matrix is positive semidefinite. -/
theorem gram_positive {n : ℕ} (B : Matrix (Fin n) Qubit ℂ) :
    (B.conjTranspose * B).PosSemidef := by
  simpa using
    (Matrix.PosSemidef.one : (1 : Matrix (Fin n) (Fin n) ℂ).PosSemidef)
      .conjTranspose_mul_mul_same B

/-- The same fact for the four-dimensional joint state. -/
theorem joint_gram_positive {n : ℕ} (B : Matrix (Fin n) Joint ℂ) :
    (B.conjTranspose * B).PosSemidef := by
  simpa using
    (Matrix.PosSemidef.one : (1 : Matrix (Fin n) (Fin n) ℂ).PosSemidef)
      .conjTranspose_mul_mul_same B

end Bell
