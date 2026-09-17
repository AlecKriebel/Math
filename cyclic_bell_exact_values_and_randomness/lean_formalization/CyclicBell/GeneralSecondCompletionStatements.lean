import CyclicBell.GeneralSecondMoments
import CyclicBell.GeneralSecondResiduals
import CyclicBell.GeneralOutcomeRelabeling

/-! Expanded statement checks for the clauses added from manuscript thm:second.
The Born sums, actual density, literal residual and transported Bell convention
remain visible at the interfaces, independently of their proof implementations. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

example (hd : 2≤d) (σ : Equiv.Perm (Ix d)) (l y : Ix d) :
    (∑ a : Ix d, ∑ b : Ix d, chi (a+b) *
      (behavior (secondPermutationStrategy hd σ) l (some y) a b : ℂ)) =
      generalLambda l * chi (-(l*y)) :=
  secondPermutation_behavior_correlator hd σ l (some y)

example (hd : 2≤d) (σ : Equiv.Perm (Ix d)) (l : Ix d) :
    (∑ a : Ix d, ∑ b : Ix d, chi (a+b) *
      (behavior (secondPermutationStrategy hd σ) l none a b : ℂ)) =
      if l=0 then 1 else 0 :=
  secondPermutation_behavior_correlator hd σ l none

example (hd : 2≤d) (σ τ : Equiv.Perm (Ix d)) :
    (fun l y => ∑ a : Ix d, ∑ b : Ix d, chi (a+b) *
      (behavior (secondPermutationStrategy hd σ) l y a b : ℂ)) =
    (fun l y => ∑ a : Ix d, ∑ b : Ix d, chi (a+b) *
      (behavior (secondPermutationStrategy hd τ) l y a b : ℂ)) :=
  secondPermutation_behavior_correlators_invariant hd σ τ

example (hd : 2≤d) (σ : Equiv.Perm (Ix d)) :
    (∀ l : Ix d, Matrix.trace ((secondPermutationStrategy hd σ).state.density *
      kron (encoded ((secondPermutationStrategy hd σ).alice l)) 1)=0) ∧
    (∀ y : AugmentedInputs d, Matrix.trace ((secondPermutationStrategy hd σ).state.density *
      kron 1 (encoded ((secondPermutationStrategy hd σ).bob y)))=0) :=
  secondPermutation_physical_local_moments_zero hd σ

example (hd : 2≤d) (σ : Equiv.Perm (Ix d)) (l : Ix d) :
    applyOp (((d : ℂ)*generalLambda l) • (1 : Mat (Ix d × Ix d)) -
      kron (encoded ((secondPermutationStrategy hd σ).alice l))
        (secondFourier (fun y => encoded ((secondPermutationStrategy hd σ).bob (some y))) l))
      (maximallyEntangled d)=0 :=
  secondPermutation_residual_zero hd σ l

example (hd : 2≤d) (σ : Equiv.Perm (Ix d)) :
    applyOp ((1 : Mat (Ix d × Ix d)) -
      kron (encoded ((secondPermutationStrategy hd σ).alice 0))
        (encoded ((secondPermutationStrategy hd σ).bob none)))
      (maximallyEntangled d)=0 :=
  secondPermutation_aligned_residual_zero hd σ

example {ι : Type*} [Fintype ι] [DecidableEq ι] (M : Measurement d ι) :
    (∑ b : Ix d, chi b • M.effect (-b))=(∑ b : Ix d, chi b • M.effect b).conjTranspose :=
  negateMeasurement_encoded M

example {ι ν : Type*} [Fintype ι] [Fintype ν] [DecidableEq ι] [DecidableEq ν]
    (s : StrategyOn d (Ix d) (AugmentedInputs d) ι ν) :
    (∑ l : Ix d,stateEval (negateBobOutcomes s).state.density (star (generalLambda l) •
      kron (encoded ((negateBobOutcomes s).alice l))
        (secondFourier (fun y => (encoded ((negateBobOutcomes s).bob (some y))).conjTranspose) l)))+
      stateEval (negateBobOutcomes s).state.density
        (kron (encoded ((negateBobOutcomes s).alice 0))
          (encoded ((negateBobOutcomes s).bob none)).conjTranspose)=secondValue s :=
  secondAdjointValue_negateBob s

example (hd : 2≤d) (σ : Equiv.Perm (Ix d)) (x : Ix d) (y : AugmentedInputs d)
    (a b : Ix d) :
    behavior (secondAdjointPermutationStrategy hd σ) x y a b=
      behavior (secondPermutationStrategy hd σ) x y a (-b) :=
  secondAdjointPermutation_behavior hd σ x y a b

end CyclicBell.General
