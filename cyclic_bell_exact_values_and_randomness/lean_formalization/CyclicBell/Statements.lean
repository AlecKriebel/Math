import CyclicBell.Regression
import CyclicBell.GeneralStatements

/-! Expanded statement correspondence checks, separate from the proofs.
The examples expose the finite physical model through its density and projectors
and are included in the standard library build. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.StatementAudit

/-- Coordinate tensor convention and its index order. -/
example (nA nB : ℕ) (M : Op nA) (N : Op nB)
    (i k : Fin nA) (j l : Fin nB) :
    tensor M N (i,j) (k,l) = M i k * N j l := rfl

/-- Full arbitrary-local-dimension upper bound: NOT restricted to 4x4. -/
example (nA nB : ℕ) (ρ : State nA nB) (A : Fin 2 → PVM nA) (B : Fin 5 → PVM nB) :
    (∑ y : Fin 4,
      (Matrix.trace (ρ.density * tensor
        ((∑ a : Fin 4, Complex.I ^ a.val • (A 0).effect a) +
          Complex.I ^ y.val • (∑ a : Fin 4, Complex.I ^ a.val • (A 1).effect a))
        (∑ b : Fin 4, Complex.I ^ b.val • (B (reducedBob y)).effect b))).re) +
      (Matrix.trace (ρ.density * tensor
        (∑ a : Fin 4, Complex.I ^ a.val • (A 0).effect a)
        (∑ b : Fin 4, Complex.I ^ b.val • (B 4).effect b))).re ≤
      2 / Real.sin (Real.pi / 8) + 1 :=
  first_universal_upper {state := ρ, alice := A, bob := B}

/-- The second bound uses sourceLambda itself and the positive Fourier sign. -/
example (nA nB : ℕ) (ρ : State nA nB) (A : Fin 4 → PVM nA) (B : Fin 5 → PVM nB) :
    (∑ l : Fin 4,
      (Matrix.trace (ρ.density * (star (sourceLambda l) •
        tensor (observable (A l))
          (∑ y : Fin 4, Complex.I ^ (l.val * y.val) • observable (B (reducedBob y)))))).re) +
      (Matrix.trace (ρ.density * tensor (observable (A 0)) (observable (B 4)))).re ≤ 5 :=
  second_universal_upper {state := ρ, alice := A, bob := B}

/-- Validity was not defined through a target score or a target table. -/
example (n : ℕ) (M : PVM n) (a b : Fin 4) (hab : a ≠ b) :
    (M.effect a).PosSemidef ∧ M.effect a * M.effect a = M.effect a ∧
    M.effect a * M.effect b = 0 ∧ (∑ c : Fin 4, M.effect c) = 1 :=
  ⟨M.positive a, M.idempotent a, M.orthogonal a b hab, M.complete⟩

example (n : ℕ) (M : PVM n) :
    (observable M).conjTranspose * observable M = 1 ∧
    observable M * (observable M).conjTranspose = 1 ∧ observable M ^ 4 = 1 :=
  ⟨(observable_unitary M).1, (observable_unitary M).2, observable_fourth_power M⟩

/-- Actual inverse encoding, including the sign of the Fourier exponent. -/
example (n : ℕ) (M : PVM n) (a : Fin 4) :
    (1 / 4 : ℂ) • (∑ j : Fin 4,
      Complex.I ^ (-((a.val * j.val : ℕ) : ℤ)) • observable M ^ j.val) = M.effect a :=
  pvm_source_fourier_reconstruction M a

/-- The declared physical model yields nonnegative, normalized probabilities. -/
example (nA nB : ℕ) (ρ : State nA nB) (M : PVM nA) (N : PVM nB) :
    (∀ a b, 0 ≤ born ρ.density (M.effect a) (N.effect b)) ∧
    (∑ a : Fin 4, ∑ b : Fin 4, born ρ.density (M.effect a) (N.effect b)) = 1 :=
  ⟨born_nonnegative ρ M N, born_normalized ρ M N⟩

/-- Actual positive trace-one states, with no saturation premise. -/
example : D4.firstStrategy.state.density.PosSemidef ∧
    Matrix.trace D4.firstStrategy.state.density = 1 ∧
    D4.secondStrategy.state.density.PosSemidef ∧ Matrix.trace D4.secondStrategy.state.density = 1 :=
  ⟨D4.firstStrategy.state.positive, D4.firstStrategy.state.normalized,
    D4.secondStrategy.state.positive, D4.secondStrategy.state.normalized⟩

/-- All first-family projectors, not only the designated pair. -/
example (x : Fin 2) (y : Fin 5) (a b : Fin 4) :
    ((D4.firstStrategy.alice x).effect a).PosSemidef ∧
    ((D4.firstStrategy.bob y).effect b).PosSemidef ∧
    (∑ c : Fin 4, (D4.firstStrategy.alice x).effect c) = 1 ∧
    (∑ c : Fin 4, (D4.firstStrategy.bob y).effect c) = 1 :=
  ⟨(D4.firstStrategy.alice x).positive a, (D4.firstStrategy.bob y).positive b,
    (D4.firstStrategy.alice x).complete, (D4.firstStrategy.bob y).complete⟩

/-- All second-family measurements, including Alice 2 and 3. -/
example (l : Fin 4) (a : Fin 4) :
    ((D4.secondStrategy.alice l).effect a).PosSemidef ∧
    (∑ c : Fin 4, (D4.secondStrategy.alice l).effect c) = 1 ∧
    ((D4.secondStrategy.alice l).effect a) * ((D4.secondStrategy.alice l).effect a) =
      (D4.secondStrategy.alice l).effect a :=
  ⟨(D4.secondStrategy.alice l).positive a, (D4.secondStrategy.alice l).complete,
    (D4.secondStrategy.alice l).idempotent a⟩

/-- The literal permutation and actual exponential phase are both exposed. -/
example (j : Fin 4) : D4.kappa j = (![0,1,3,2] : Fin 4 → Fin 4) j := D4.kappa_values j
example : D4.zeta = Complex.exp (((Real.pi / 8 : ℝ) : ℂ) * Complex.I) := rfl
example (j : Fin 4) :
    D4.swappedWeights j =
      Complex.exp (((Real.pi / 8 : ℝ) : ℂ) * Complex.I) ^
        ((![2,6,14,10] : Fin 4 → ℕ) j) := D4.old_weights_phase_bridge j

/-- Transpose, adjoint, and entrywise conjugation are not silently exchanged. -/
example (A B : Op 4) :
    expectation D4.phi (tensor A B) = Matrix.trace (A * B.transpose) / 4 := D4.phi_trace A B
example (y : Fin 4) :
    D4.witnessB y = D4.entryConj
      (D4.shift * Matrix.diagonal (fun j => D4.zeta ^ D4.polarExponents y j)) :=
  D4.bob_manuscript_bridge y
example (l : Fin 4) : D4.witnessA l = D4.entryConj (D4.sourceD l) :=
  D4.secondAlice_manuscript_bridge l

/-- Actual trigonometric coefficients, not unspecified normalized coefficients. -/
example (l : Fin 4) : sourceLambda l =
    (![((D4.c + D4.s) / 2 : ℝ), ((D4.c + D4.s) / 2 : ℝ),
      (((D4.s - D4.c) / 2 : ℝ) : ℂ) * Complex.I,
      (((D4.s - D4.c) / 2 : ℝ) : ℂ) * Complex.I] : Fin 4 → ℂ) l :=
  D4.sourceLambda_eq l

example (l : Fin 4) : fourier4 D4.witnessB l = (4 * sourceLambda l) • D4.sourceD l :=
  D4.witness_source_D_compression l

/-- First universal normalization and attainment are separate proof dependencies. -/
example : firstAugmentedValue D4.firstStrategy = 2 / Real.sin (Real.pi / 8) + 1 :=
  D4.first_attainment
example : secondAugmentedValue D4.secondStrategy = 5 := D4.second_attainment
example (nA nB : ℕ) (σ : Strategy 2 nA nB) :
    firstAugmentedValue σ ≤ firstAugmentedValue D4.firstStrategy :=
  D4.first_is_maximizer nA nB σ
example (nA nB : ℕ) (σ : Strategy 4 nA nB) :
    secondAugmentedValue σ ≤ secondAugmentedValue D4.secondStrategy :=
  D4.second_is_maximizer nA nB σ

/-- The displayed table is a trace of the actual state and actual projectors. -/
example (a b : Fin 4) :
    (Matrix.trace (D4.firstStrategy.state.density * tensor
      ((D4.firstStrategy.alice 1).effect a) ((D4.firstStrategy.bob 4).effect b))).re =
      if (a.val + b.val) % 2 = 0 then (1 : ℝ) / 32 else 3 / 32 :=
  D4.first_behavior_table a b
example (a b : Fin 4) :
    (Matrix.trace (D4.secondStrategy.state.density * tensor
      ((D4.secondStrategy.alice 1).effect a) ((D4.secondStrategy.bob 4).effect b))).re =
      if (a.val + b.val) % 2 = 0 then (1 : ℝ) / 32 else 3 / 32 :=
  D4.second_behavior_table a b

/-- The Eve state is derived by an actual sandwich and partial trace. -/
example (a b : Fin 4) :
    actualTrivialConditional D4.firstStrategy.state.density
      (tensor ((D4.firstStrategy.alice 1).effect a) ((D4.firstStrategy.bob 4).effect b)) =
    ((behavior D4.firstStrategy 1 4 a b : ℝ) : ℂ) • (1 : Op 1) :=
  D4.first_physical_Eve_bridge a b

example : trivialEveSuccess (targetDistribution D4.firstStrategy 1) (0,1) = 3 / 32 ∧
    (1 : ℝ) / 16 < trivialEveSuccess (targetDistribution D4.firstStrategy 1) (0,1) :=
  D4.first_trivialEve_gap

/-- This implication, rather than a complete-behavior protocol, is negated. -/
example : ¬ (∀ (nA nB : ℕ) (σ : Strategy 2 nA nB),
    firstAugmentedValue σ = 2 / Real.sin (Real.pi / 8) + 1 →
      ∀ a b, behavior σ 1 4 a b = 1 / 16) := D4.first_scalar_value_does_not_force_uniform

end CyclicBell.StatementAudit
