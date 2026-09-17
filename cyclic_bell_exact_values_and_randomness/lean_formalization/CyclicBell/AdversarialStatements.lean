import CyclicBell.GeneralAdversarialRegression

/-! Expanded statement contracts for the adversarial models and bounds.
The examples expose the quantified physical definitions and endpoint statements. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder Topology
namespace CyclicBell.General

example {d : ℕ} [NeZero d] {α β ι κ ε : Type}
    [Fintype ι] [Fintype κ] [Fintype ε] [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]
    (s : TripartiteOn d α β ι κ ε) (x : α) (y : β) (a b : Ix d) (g : GuessLabel d) :
    tripartiteBehavior s x y a b g=(Matrix.trace (s.eve.effect g*
      mixedConditionalE s.state.density (kron ((s.alice x).effect a) ((s.bob y).effect b)))).re :=
  tripartiteBehavior_instrument s x y a b g

example {d : ℕ} [NeZero d] {α β ι κ ε : Type}
    [Fintype ι] [Fintype κ] [Fintype ε] [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]
    (s : TripartiteOn d α β ι κ ε) :
    commutingExtendedBehavior (tripartiteToCommuting s)=tripartiteBehavior s :=
  tripartiteToCommuting_behavior s

example {d : ℕ} [NeZero d] {α β : Type} :
    GuessQa d α β=closure (GuessQ d α β) := rfl

example {d : ℕ} [NeZero d] {α β : Type} (f : BellBehavior d α β → ℝ) (x : α) (y : β) :
    GvalQa f x y=sSup ((fun r => guessingSuccess r x y) ''
      {r | r∈closure (GuessQ d α β) ∧ f (forgetE r)=betaQa f}) := rfl

example {d : ℕ} [NeZero d] {α β H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (s : CommutingEveOn d α β H) (x : α) (y : β) :
    0≤guessingSuccess (commutingExtendedBehavior s) x y ∧
      guessingSuccess (commutingExtendedBehavior s) x y≤1 :=
  ⟨guessingSuccess_nonnegative _ (commutingExtended_normalized s) x y,
    guessingSuccess_le_one _ (commutingExtended_normalized s) x y⟩

example {d : ℕ} [NeZero d] (hd : 4≤d) :
    (paperGuessFloor d≤GvalQ (firstAugmentedBell (d := d)) 1 none ∧ GvalQ (firstAugmentedBell (d := d)) 1 none≤1) ∧
    (paperGuessFloor d≤GvalQa (firstAugmentedBell (d := d)) 1 none ∧ GvalQa (firstAugmentedBell (d := d)) 1 none≤1) ∧
    (paperGuessFloor d≤GvalQc (firstAugmentedBell (d := d)) 1 none ∧ GvalQc (firstAugmentedBell (d := d)) 1 none≤1) :=
  first_value_conditioned_guessing_bounds hd

example {d : ℕ} [NeZero d] (hd : 4≤d) :
    1/(d : ℝ)^2<GvalQ (secondAugmentedBell (d := d)) 1 none ∧
    1/(d : ℝ)^2<GvalQa (secondAugmentedBell (d := d)) 1 none ∧
    1/(d : ℝ)^2<GvalQc (secondAugmentedBell (d := d)) 1 none := second_value_conditioned_strict_gap hd

example : (3 : ℝ)/32≤GvalQ (firstAugmentedBell (d := 4)) 1 none ∧
    (3 : ℝ)/32≤GvalQa (firstAugmentedBell (d := 4)) 1 none ∧
    (3 : ℝ)/32≤GvalQc (firstAugmentedBell (d := 4)) 1 none := first_four_Gval_three32

example : guessingMinEntropy (GvalQc (secondAugmentedBell (d := 4)) 1 none)≤
    5-Real.log 3/Real.log 2 := second_four_value_entropy_upper.2.2

example {d : ℕ} [NeZero d] {ε : Type} [Fintype ε] [DecidableEq ε]
    (σ : GuessLabel d → Mat ε) : ∃ Q : GuessPOVM d ε,
      povmObjective σ Q=finitePOVMValue σ ∧ ∀ R : GuessPOVM d ε,povmObjective σ R≤povmObjective σ Q :=
  finitePOVMValue_attained σ

example {d : ℕ} [NeZero d] {α β ι κ ε : Type}
    [Fintype ι] [Fintype κ] [Fintype ε] [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]
    (s : TripartiteOn d α β ι κ ε) (x : α) (y : β) (Q : GuessPOVM d ε) :
    forgetE (tripartiteBehavior (withEve s Q))=forgetE (tripartiteBehavior s) := withEve_marginal s Q

example {d : ℕ} [NeZero d] (hd : 2≤d) :
    GvalQ (firstAugmentedBell (d := d)) 1 none=
      sSup (optimizedFiniteScores (firstAugmentedBell (d := d)) 1 none) := first_GvalQ_nested hd

example {d : ℕ} [NeZero d] (m k : Ix d) :
    (∑ y,chi (m*y)*sourceCoeff y k)=if k=m-1 then (d : ℂ)*sourceCoeffBase k else 0 :=
  source_coefficient_DFT m k

example {d : ℕ} [NeZero d] :
    (∑ y,sourceBob (d := d) y)=
      ((1 : ℂ)/(Real.sin (Real.pi/(2*(d : ℝ))) : ℂ)) • (sourceClock d)ᴴ := source_fourier_zero

example (y : Ix 3) : sourceBob y=(1/3 : ℂ) •
      ((2 : ℂ) • sourceClock 3^2+(2*chi (2*y)) • cyclicShift 3-
        chi (y+1) • (cyclicShift 3^2*sourceClock 3)) := source_qutrit_operator y

example (g : GuessLabel 4) : uniformOneDimensionalGuess.effect g*uniformOneDimensionalGuess.effect g≠
    uniformOneDimensionalGuess.effect g := uniformGuess_not_projective g

example : (0 : ℝ)∈closure (Set.Ioi (0 : ℝ)) ∧ (0 : ℝ)∉closure {x : ℝ | 0<x ∧ x=0} :=
  closure_before_slice_control

end CyclicBell.General
