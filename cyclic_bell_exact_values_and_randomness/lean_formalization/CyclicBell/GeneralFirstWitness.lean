import CyclicBell.GeneralFirstBound
import CyclicBell.GeneralPolarPhases
import CyclicBell.GeneralGuessing

/-! Physical attainment and nonuniformity for the first augmented family in every d>=4.
All state/PVM fields are constructed before the Bell value is evaluated.
Universal maximality uses GeneralFirstBound, which has no witness imports.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def permutationAlice (hd : 2≤d) (κ : Equiv.Perm (Ix d)) (x : Fin 2) : Measurement d (Ix d) :=
  if x=0 then fourierMeasurement d else
    cycleMeasurement (equalityRoot ∘ κ) (phases_permuted _ equalityRoot_unit κ)
      (by rw [show (∏ j,(equalityRoot ∘ κ) j)=∏ j,equalityRoot j from product_permuted _ κ]
          exact equalityRoot_product hd)

def permutationBob (κ : Equiv.Perm (Ix d)) : AugmentedInputs d → Measurement d (Ix d)
  | none => fourierMeasurement d
  | some y => cycleMeasurement (fun j => star (polarPhase y (κ j)))
      (by intro j; simpa [mul_comm] using polarPhase_unit (d := d) y (κ j))
      (by rw [product_permuted (fun j => star (polarPhase y j)) κ]
          simpa only [star_prod,star_one] using congrArg star (polarPhase_product y))

def firstPermutationStrategy (hd : 2≤d) (κ : Equiv.Perm (Ix d)) :
    StrategyOn d (Fin 2) (AugmentedInputs d) (Ix d) (Ix d) where
  state := entangledState d
  alice := permutationAlice hd κ
  bob := permutationBob κ

@[simp] theorem permutationAlice_zero (hd : 2≤d) (κ : Equiv.Perm (Ix d)) :
    encoded (permutationAlice hd κ 0)=cyclicShift d := by
  simp [permutationAlice,fourierMeasurement_encoding]

@[simp] theorem permutationAlice_one (hd : 2≤d) (κ : Equiv.Perm (Ix d)) :
    encoded (permutationAlice hd κ 1)=weightedCycle (equalityRoot ∘ κ) := by
  simp [permutationAlice,cycleMeasurement_encoding]

@[simp] theorem permutationBob_none (κ : Equiv.Perm (Ix d)) :
    encoded (permutationBob κ none)=cyclicShift d := fourierMeasurement_encoding (d := d)

@[simp] theorem permutationBob_some (κ : Equiv.Perm (Ix d)) (y : Ix d) :
    encoded (permutationBob κ (some y))=
      entryConjugate (weightedCycle (polarPhase y ∘ κ)) := by
  rw [permutationBob,cycleMeasurement_encoding,weighted_entry_conjugate]
  rfl

theorem entangled_stateEval (T : Mat (Ix d × Ix d)) :
    stateEval (entangledState d).density T=(expectation (maximallyEntangled d) T).re := by
  exact congrArg Complex.re (expectation_eq_trace (maximallyEntangled d) T).symm

theorem firstPermutation_term (hd : 2≤d) (κ : Equiv.Perm (Ix d)) (y : Ix d) :
    stateEval (entangledState d).density
      (kron (encoded (permutationAlice hd κ 0)+chi y • encoded (permutationAlice hd κ 1))
        (encoded (permutationBob κ (some y)))) =
          (∑ k : Ix d,‖1+chi y*equalityRoot k‖)/(d : ℝ) := by
  rw [permutationAlice_zero,permutationAlice_one,permutationBob_some,entangled_stateEval,
    weighted_entry_conjugate]
  have he : cyclicShift d+chi y • weightedCycle (equalityRoot ∘ κ)=
      weightedCycle (fun j => 1+chi y*equalityRoot (κ j)) := by
    simpa only [cyclicShift,one_smul,one_mul,Function.comp_apply]
      using weighted_linear (fun _ : Ix d => (1 : ℂ)) (equalityRoot ∘ κ) 1 (chi y)
  rw [he,phi_weighted]
  simp only [Function.comp_apply,polarPhase_conjugate_factor hd]
  rw [sum_permuted (fun k => (‖1+chi y*equalityRoot k‖ : ℂ)) κ]
  have hc : (∑ k : Ix d,(‖1+chi y*equalityRoot k‖ : ℂ))/(d : ℂ) =
      (((∑ k : Ix d,‖1+chi y*equalityRoot k‖)/(d : ℝ) : ℝ) : ℂ) := by
    push_cast
    rfl
  rw [hc,Complex.ofReal_re]

/-- Evaluation of the actual first functional. -/
theorem firstPermutation_attains (hd : 2≤d) (κ : Equiv.Perm (Ix d)) :
    firstValue (firstPermutationStrategy hd κ)=scalarMaximum d+1 := by
  unfold firstValue
  change (∑ y : Ix d,stateEval (entangledState d).density
    (kron (encoded (permutationAlice hd κ 0)+chi y • encoded (permutationAlice hd κ 1))
      (encoded (permutationBob κ (some y)))))+
    stateEval (entangledState d).density
      (kron (encoded (permutationAlice hd κ 0)) (encoded (permutationBob κ none)))=_
  simp_rw [firstPermutation_term hd κ]
  rw [permutationAlice_zero,permutationBob_none,entangled_stateEval,
    (added_first_harmonics (equalityRoot : Ix d → ℂ) κ).1,Complex.one_re]
  congr 1
  rw [← Finset.sum_div,Finset.sum_comm]
  change (∑ k : Ix d,scalarSum (d := d) (equalityRoot k))/(d : ℝ)=scalarMaximum d
  simp_rw [equalityRoot_scalar_attainment hd]
  simp only [Finset.sum_const,Finset.card_univ,ZMod.card,nsmul_eq_mul]
  field_simp [ne_of_gt (dimension_pos (d := d))]

/-- The complete first-harmonic matrix does not depend on the permutation. -/
theorem firstPermutation_harmonics (hd : 2≤d) (κ : Equiv.Perm (Ix d)) (y : Ix d) :
    expectation (maximallyEntangled d)
      (kron (encoded (permutationAlice hd κ 0)) (encoded (permutationBob κ (some y)))) =
        (∑ k,star (polarPhase y k))/(d : ℂ) ∧
    expectation (maximallyEntangled d)
      (kron (encoded (permutationAlice hd κ 1)) (encoded (permutationBob κ (some y)))) =
        (∑ k,equalityRoot k*star (polarPhase y k))/(d : ℂ) := by
  simp only [permutationAlice_zero,permutationAlice_one,permutationBob_some]
  exact first_harmonic_permutation equalityRoot (polarPhase y) κ

/-- Target outcome table through the actual PVMs in the full strategy. -/
theorem firstPermutation_target (hd : 2≤d) (κ : Equiv.Perm (Ix d)) (a b : Ix d) :
    behavior (firstPermutationStrategy hd κ) 1 none a b =
      fourierTable («prefix» (equalityRoot ∘ κ)) a b := by
  change bornProbability (entangledState d).density
    ((permutationAlice hd κ 1).effect a) ((permutationBob κ none).effect b)=_
  simp only [permutationAlice,show (1 : Fin 2)≠0 by decide,if_false,
    permutationBob,cycleMeasurement]
  exact target_born_table _ _ _ _

theorem firstSwap_target (hd : 4≤d) (a b : Ix d) :
    behavior (firstPermutationStrategy (by omega : 2≤d) (finalSwap d)) 1 none a b=
      swappedTarget d a b := by
  rw [firstPermutation_target,swappedTarget_fourier]
  rfl

/-- Every finite-dimensional competitor is bounded by this concrete strategy.
Neither the witness nor any definition is assumed maximal. -/
theorem firstPermutation_maximal (hd : 2≤d) (κ : Equiv.Perm (Ix d))
    {ι ν : Type*} [Fintype ι] [Fintype ν] [DecidableEq ι] [DecidableEq ν]
    (t : StrategyOn d (Fin 2) (AugmentedInputs d) ι ν) :
    firstValue t≤firstValue (firstPermutationStrategy hd κ) := by
  rw [firstPermutation_attains]
  exact first_physical_upper hd t

/-- Main all-dimensional first-family source endpoint. The universal quantifier
runs over every pair of finite local dimensions; the witness is the full PVM
strategy on C^d tensor C^d. The extra Bob input is Option.none. -/
theorem first_all_dimension_counterexample (hd : 4≤d) :
    ∃ s : StrategyOn d (Fin 2) (AugmentedInputs d) (Ix d) (Ix d),
      firstValue s=2/Real.sin (Real.pi/(2*d))+1 ∧
      (∀ nA nB : ℕ,∀ t : StrategyOn d (Fin 2) (AugmentedInputs d) (Fin nA) (Fin nB),
        firstValue t≤firstValue s) ∧
      (∀ a b,(∑ b',behavior s 1 none a b')=1/(d : ℝ) ∧
        (∑ a',behavior s 1 none a' b)=1/(d : ℝ)) ∧
      (¬ ∀ a b,behavior s 1 none a b=1/(d : ℝ)^2) ∧
      (∃ a b,1/(d : ℝ)^2+
        2*Real.sin (Real.pi/(d : ℝ))*Real.sin (3*Real.pi/(d : ℝ))/
          ((d : ℝ)^2*((d : ℝ)-1)) ≤ behavior s 1 none a b) := by
  let s := firstPermutationStrategy (d := d) (by omega : 2≤d) (finalSwap d)
  refine ⟨s,firstPermutation_attains (by omega) _,?_,?_,?_,?_⟩
  · intro nA nB t
    exact firstPermutation_maximal (by omega) _ t
  · intro a b
    dsimp [s]
    simp_rw [firstSwap_target hd]
    exact swappedTarget_marginals a b
  · simpa only [s,firstSwap_target hd] using swappedTarget_not_uniform (d := d) hd
  · simpa only [s,firstSwap_target hd] using swappedTarget_quantitative (d := d) hd

end CyclicBell.General
