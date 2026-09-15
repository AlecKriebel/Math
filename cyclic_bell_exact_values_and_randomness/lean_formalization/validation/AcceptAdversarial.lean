import CyclicBell
noncomputable section
open CyclicBell CyclicBell.General
open scoped BigOperators Matrix ComplexOrder Topology
example : (3 : ℝ)/32≤GvalQ (firstAugmentedBell (d := 4)) 1 none := first_four_Gval_three32.1
example : guessingMinEntropy (GvalQc (secondAugmentedBell (d := 4)) 1 none)<4 :=
  second_four_value_entropy_strict.2.2
example (ε : Type) [Fintype ε] [DecidableEq ε] (σ : GuessLabel 4 → Mat ε) :
    ∃ Q : GuessPOVM 4 ε,povmObjective σ Q=finitePOVMValue σ ∧
      ∀ R : GuessPOVM 4 ε,povmObjective σ R≤povmObjective σ Q := finitePOVMValue_attained σ
example : uniformOneDimensionalGuess.effect (0,0)*uniformOneDimensionalGuess.effect (0,0)≠
    uniformOneDimensionalGuess.effect (0,0) := uniformGuess_not_projective _
example (y : Ix 3) : sourceBob y=(1/3 : ℂ) •
      ((2 : ℂ) • sourceClock 3^2+(2*chi (2*y)) • cyclicShift 3-
        chi (y+1) • (cyclicShift 3^2*sourceClock 3)) := source_qutrit_operator y
