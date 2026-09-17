import CyclicBell.GeneralSecondWitness
import CyclicBell.GeneralBehavior

/-! Complete complex first-harmonic moments of the physical second-family
permutation strategy. The formulas cover every Alice input and every Bob input,
including the alignment setting. They assert no invariance of higher harmonics
or of the full outcome distribution. -/

noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

/-- Every reduced-input correlator, with the manuscript's complex phase. -/
theorem secondPermutation_correlator (hd : 2≤d)
    (κ : Equiv.Perm (Ix d)) (l y : Ix d) :
    expectation (maximallyEntangled d)
      (kron (encoded (secondAlice hd κ l))
        (encoded (permutationBob κ (some y)))) =
      generalLambda l * chi (-(l*y)) := by
  rw [secondAlice_encoding,permutationBob_some,weighted_entry_conjugate,
    weighted_entry_conjugate,phi_weighted]
  simp only [Function.comp_apply]
  rw [sum_permuted (fun j => star (secondWeight l j)*star (polarPhase y j)) κ]
  have hs : (∑ j : Ix d,star (secondWeight l j)*star (polarPhase y j)) =
      star (secondPrefactor l)*(chi (-(l*y))*polarTransform l) := by
    calc
      _ = star (secondPrefactor l)*
          ∑ j : Ix d,chi (l*j)*star (polarPhase j y) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro j _
        simp only [secondWeight,star_mul,chi_star,neg_neg,polarPhase]
        rw [add_comm y j]
        ring
      _ = _ := by rw [polarTransform_shift]
  rw [hs,polarTransform_compression hd]
  have hn : (d : ℂ)≠0 := by exact_mod_cast NeZero.ne d
  calc
    _ = (star (secondPrefactor l)*secondPrefactor l)*
        (generalLambda l*chi (-(l*y))) := by field_simp; ring
    _ = _ := by rw [secondPrefactor_unit,one_mul]

/-- The extra Bob input gives the complete Kronecker-delta Alice column. -/
theorem secondPermutation_extra_correlator (hd : 2≤d)
    (κ : Equiv.Perm (Ix d)) (l : Ix d) :
    expectation (maximallyEntangled d)
      (kron (encoded (secondAlice hd κ l))
        (encoded (permutationBob κ none))) =
      if l=0 then 1 else 0 := by
  rw [secondAlice_encoding,permutationBob_none,weighted_entry_conjugate,
    cyclicShift,phi_weighted]
  simp only [mul_one,Function.comp_apply]
  rw [sum_permuted (fun j => star (secondWeight l j)) κ]
  simp only [secondWeight,star_mul,chi_star,neg_neg]
  rw [←Finset.sum_mul,character_sum]
  split_ifs with hl
  · subst l
    simp [secondPrefactor,show (d : ℂ)≠0 by exact_mod_cast NeZero.ne d]
  · simp

/-- All local complex first moments vanish, including the extra Bob setting. -/
theorem secondPermutation_local_moments_zero (hd : 2≤d)
    (κ : Equiv.Perm (Ix d)) :
    (∀ l : Ix d,expectation (maximallyEntangled d)
      (kron (encoded (secondAlice hd κ l)) 1)=0) ∧
    (∀ y : AugmentedInputs d,expectation (maximallyEntangled d)
      (kron 1 (encoded (permutationBob κ y)))=0) := by
  constructor
  · intro l
    rw [phi_trace,Matrix.transpose_one,Matrix.mul_one,
      secondAlice_encoding,weighted_entry_conjugate,weighted_trace_zero hd,zero_div]
  · intro y
    rw [phi_trace,Matrix.one_mul,Matrix.trace_transpose]
    cases y with
    | none => rw [permutationBob_none,cyclicShift,weighted_trace_zero hd,zero_div]
    | some y => rw [permutationBob_some,weighted_entry_conjugate,weighted_trace_zero hd,zero_div]

/-- The complete d-by-(d+1) matrix of first-harmonic expectation values. -/
theorem secondPermutation_first_harmonic_matrix (hd : 2≤d)
    (κ : Equiv.Perm (Ix d)) (l : Ix d) (y : AugmentedInputs d) :
    expectation (maximallyEntangled d)
      (kron (encoded ((secondPermutationStrategy hd κ).alice l))
        (encoded ((secondPermutationStrategy hd κ).bob y))) =
      match y with
      | none => if l=0 then 1 else 0
      | some y => generalLambda l*chi (-(l*y)) := by
  cases y with
  | none => exact secondPermutation_extra_correlator hd κ l
  | some y => exact secondPermutation_correlator hd κ l y

/-- Physical second-family strategies have the same complete matrix of complex
first-harmonic correlators for every permutation of the equality phases. -/
theorem secondPermutation_first_harmonic_matrix_invariant (hd : 2≤d)
    (κ τ : Equiv.Perm (Ix d)) :
    (fun l y => expectation (maximallyEntangled d)
      (kron (encoded ((secondPermutationStrategy hd κ).alice l))
        (encoded ((secondPermutationStrategy hd κ).bob y)))) =
    (fun l y => expectation (maximallyEntangled d)
      (kron (encoded ((secondPermutationStrategy hd τ).alice l))
        (encoded ((secondPermutationStrategy hd τ).bob y)))) := by
  funext l y
  rw [secondPermutation_first_harmonic_matrix,secondPermutation_first_harmonic_matrix]

/-- The same matrix read directly from the physical Born behavior. -/
theorem secondPermutation_behavior_correlator (hd : 2≤d)
    (κ : Equiv.Perm (Ix d)) (l : Ix d) (y : AugmentedInputs d) :
    probabilityCorrelator (behavior (secondPermutationStrategy hd κ)) l y =
      match y with
      | none => if l=0 then 1 else 0
      | some y => generalLambda l*chi (-(l*y)) := by
  rw [probabilityCorrelator_behavior]
  change Matrix.trace (projector (maximallyEntangled d) *
    kron (encoded (secondAlice hd κ l)) (encoded (permutationBob κ y))) = _
  rw [←expectation_eq_trace]
  exact secondPermutation_first_harmonic_matrix hd κ l y

/-- Permutation independence of the entire complex correlator array of the
actual physical behavior, rather than just equality of its Bell sum. -/
theorem secondPermutation_behavior_correlators_invariant (hd : 2≤d)
    (κ τ : Equiv.Perm (Ix d)) :
    probabilityCorrelator (behavior (secondPermutationStrategy hd κ)) =
      probabilityCorrelator (behavior (secondPermutationStrategy hd τ)) := by
  funext l y
  rw [secondPermutation_behavior_correlator,secondPermutation_behavior_correlator]

/-- All local first moments, expressed with the strategy's actual density. -/
theorem secondPermutation_physical_local_moments_zero (hd : 2≤d)
    (κ : Equiv.Perm (Ix d)) :
    (∀ l : Ix d,Matrix.trace ((secondPermutationStrategy hd κ).state.density *
      kron (encoded ((secondPermutationStrategy hd κ).alice l)) 1)=0) ∧
    (∀ y : AugmentedInputs d,Matrix.trace ((secondPermutationStrategy hd κ).state.density *
      kron 1 (encoded ((secondPermutationStrategy hd κ).bob y)))=0) := by
  obtain ⟨ha,hb⟩ := secondPermutation_local_moments_zero hd κ
  constructor
  · intro l
    exact (expectation_eq_trace (maximallyEntangled d) _).symm.trans (ha l)
  · intro y
    exact (expectation_eq_trace (maximallyEntangled d) _).symm.trans (hb y)

/-- Complete first-moment package for manuscript thm:second: both kinds of
complex correlator and every Alice/Bob local first moment. -/
theorem secondPermutation_complete_first_moments (hd : 2≤d)
    (κ : Equiv.Perm (Ix d)) :
    (∀ l y : Ix d,probabilityCorrelator (behavior (secondPermutationStrategy hd κ)) l (some y)=
      generalLambda l*chi (-(l*y))) ∧
    (∀ l : Ix d,probabilityCorrelator (behavior (secondPermutationStrategy hd κ)) l none=
      if l=0 then 1 else 0) ∧
    (∀ l : Ix d,Matrix.trace ((secondPermutationStrategy hd κ).state.density *
      kron (encoded ((secondPermutationStrategy hd κ).alice l)) 1)=0) ∧
    (∀ y : AugmentedInputs d,Matrix.trace ((secondPermutationStrategy hd κ).state.density *
      kron 1 (encoded ((secondPermutationStrategy hd κ).bob y)))=0) := by
  exact ⟨fun l y => secondPermutation_behavior_correlator hd κ l (some y),
    fun l => secondPermutation_behavior_correlator hd κ l none,
    secondPermutation_physical_local_moments_zero hd κ⟩

end CyclicBell.General
