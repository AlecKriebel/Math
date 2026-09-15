import CyclicBell.Model
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
Actual manuscript functionals and intended universal propositions.
These are definitions, NOT upper-bound theorems. No validity structure assumes
these propositions. In particular, defining FirstUpperBound does not prove it.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell

/-- Inclusion of the four reduced Bob settings into the five augmented ones. -/
def reducedBob (y : Fin 4) : Fin 5 := ⟨y.val, Nat.lt_trans y.isLt (by decide)⟩

def firstReducedValue {nA nB : ℕ} (s : Strategy 2 nA nB) : ℝ :=
  ∑ y : Fin 4,
    (Matrix.trace (s.state.density *
      tensor (observable (s.alice 0) + Complex.I ^ y.val • observable (s.alice 1))
        (observable (s.bob (reducedBob y))))).re

def firstAugmentedValue {nA nB : ℕ} (s : Strategy 2 nA nB) : ℝ :=
  firstReducedValue s +
    (Matrix.trace (s.state.density *
      tensor (observable (s.alice 0)) (observable (s.bob 4)))).re

def firstTargetValue : ℝ := 2 / Real.sin (Real.pi / 8) + 1

/-- Integer exponents preserve the l=0 source convention (-1)^(-1)=-1. -/
def sourceLambda (l : Fin 4) : ℂ :=
  (-1 : ℂ) ^ ((l.val : ℤ) - 1) *
    (Complex.exp (((Real.pi / 4 : ℝ) : ℂ) * Complex.I)) ^
      ((l.val : ℤ) * ((l.val : ℤ) - 1)) /
    ((4 * Real.sin (Real.pi * ((l.val : ℝ) - 1 / 2) / 4) : ℝ) : ℂ)

def bobFourier {nA nB : ℕ} (s : Strategy 4 nA nB) (l : Fin 4) : Op nB :=
  ∑ y : Fin 4, Complex.I ^ (l.val * y.val) • observable (s.bob (reducedBob y))

def secondReducedValue {nA nB : ℕ} (s : Strategy 4 nA nB) : ℝ :=
  ∑ l : Fin 4,
    (Matrix.trace (s.state.density *
      (star (sourceLambda l) • tensor (observable (s.alice l)) (bobFourier s l)))).re

def secondAugmentedValue {nA nB : ℕ} (s : Strategy 4 nA nB) : ℝ :=
  secondReducedValue s +
    (Matrix.trace (s.state.density *
      tensor (observable (s.alice 0)) (observable (s.bob 4)))).re

/-- Target A as a proposition: the source proof is PhysicalBounds.first_upper_bound. -/
def FirstUpperBound : Prop :=
  ∀ (nA nB : ℕ), 0 < nA → 0 < nB →
    ∀ s : Strategy 2 nA nB, firstAugmentedValue s ≤ firstTargetValue

/-- Target F universal proposition; source proof: PhysicalBounds.second_upper_bound. -/
def SecondUpperBound : Prop :=
  ∀ (nA nB : ℕ), 0 < nA → 0 < nB →
    ∀ s : Strategy 4 nA nB, secondAugmentedValue s ≤ 5

end CyclicBell
