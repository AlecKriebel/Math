import CyclicBell.GeneralSecondWitness

/-! Closing the canonical/swapped comparison and the small-d permutation
boundary. These claims concern this explicit orbit, NOT all maximizers.
UNCOMPILED SOURCE CANDIDATES. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

theorem recurrence_nat_product (q w : Ix d → ℂ)
    (hr : ∀ j,q (j+1)=w j*q j) (n : ℕ) :
    q (n : Ix d)=(∏ k ∈ Finset.range n,w (k : Ix d))*q 0 := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Nat.cast_add,Nat.cast_one,hr,ih,Finset.prod_range_succ]
    ring

theorem prefix_reconstruct (q w : Ix d → ℂ) (h0 : q 0=1)
    (hr : ∀ j,q (j+1)=w j*q j) : prefix w=q := by
  funext j
  have h := recurrence_nat_product q w hr j.val
  simpa [ZMod.natCast_zmod_val,prefix,h0] using h.symm

theorem canonical_prefix (hd : 2≤d) : prefix (equalityRoot : Ix d → ℂ)=canonicalPhase :=
  prefix_reconstruct canonicalPhase equalityRoot canonicalPhase_zero (canonical_recurrence hd)

theorem first_canonical_target (hd : 2≤d) (a b : Ix d) :
    behavior (firstPermutationStrategy hd (Equiv.refl (Ix d))) 1 none a b=1/(d : ℝ)^2 := by
  rw [firstPermutation_target]
  change fourierTable (prefix (equalityRoot : Ix d → ℂ)) a b=_
  rw [canonical_prefix hd]
  exact (table_uniform_iff _).mpr canonical_flat a b

theorem second_canonical_target (hd : 2≤d) (a b : Ix d) :
    behavior (secondPermutationStrategy hd (Equiv.refl (Ix d))) 1 none a b=1/(d : ℝ)^2 := by
  rw [second_first_target_same,first_canonical_target]

theorem low_two_permutation_flat (κ : Equiv.Perm (Ix 2)) :
    FourierFlat (prefix (equalityRoot ∘ κ)) := by
  apply (flat_iff_autocorrelation _ (prefix_unit _ (phases_permuted _ equalityRoot_unit κ))).mpr
  intro t ht
  fin_cases t
  · exact False.elim (ht rfl)
  · exact permutation_lag_one (by norm_num) κ

theorem low_three_permutation_flat (κ : Equiv.Perm (Ix 3)) :
    FourierFlat (prefix (equalityRoot ∘ κ)) := by
  apply (flat_iff_autocorrelation _ (prefix_unit _ (phases_permuted _ equalityRoot_unit κ))).mpr
  intro t ht
  fin_cases t
  · exact False.elim (ht rfl)
  · exact permutation_lag_one (by norm_num) κ
  · have he : (2 : Ix 3)=-(1 : Ix 3) := by decide
    rw [he,autocorrelation_neg,permutation_lag_one (by norm_num),star_zero]

/-- No claim that arbitrary d=2 or d=3 Bell-value maximizers are rigid. -/
theorem low_dimension_orbit_uniform (hd : d=2 ∨ d=3) (κ : Equiv.Perm (Ix d)) :
    ∀ a b,fourierTable (prefix (equalityRoot ∘ κ)) a b=1/(d : ℝ)^2 := by
  apply (table_uniform_iff _).mpr
  rcases hd with rfl | rfl
  · exact low_two_permutation_flat κ
  · exact low_three_permutation_flat κ

/-- Two actual first-family maximizers with inequivalent designated behavior
under every pair of local output permutations at the target settings. -/
theorem first_behavior_nonuniqueness (hd : 4≤d) :
    ∃ s t : StrategyOn d (Fin 2) (AugmentedInputs d) (Ix d) (Ix d),
      firstValue s=scalarMaximum d+1 ∧ firstValue t=scalarMaximum d+1 ∧
      (∀ a b,behavior s 1 none a b=1/(d : ℝ)^2) ∧
      ∀ α β : Equiv.Perm (Ix d),¬ (∀ a b,behavior s 1 none a b=behavior t 1 none (α a) (β b)) := by
  refine ⟨firstPermutationStrategy (by omega) (Equiv.refl _),
    firstPermutationStrategy (by omega) (finalSwap d),
    firstPermutation_attains (by omega) _,firstPermutation_attains (by omega) _,
    first_canonical_target (by omega),?_⟩
  intro α β h
  apply no_uniform_relabeling hd α β
  intro a b
  rw [← firstSwap_target hd,← h a b,first_canonical_target]

theorem second_behavior_nonuniqueness (hd : 4≤d) :
    ∃ s t : StrategyOn d (Ix d) (AugmentedInputs d) (Ix d) (Ix d),
      secondValue s=d+1 ∧ secondValue t=d+1 ∧
      (∀ a b,behavior s 1 none a b=1/(d : ℝ)^2) ∧
      ∀ α β : Equiv.Perm (Ix d),¬ (∀ a b,behavior s 1 none a b=behavior t 1 none (α a) (β b)) := by
  refine ⟨secondPermutationStrategy (by omega) (Equiv.refl _),
    secondPermutationStrategy (by omega) (finalSwap d),
    secondPermutation_attains (by omega) _,secondPermutation_attains (by omega) _,
    second_canonical_target (by omega),?_⟩
  intro α β h
  apply no_uniform_relabeling hd α β
  intro a b
  have he := h a b
  rw [second_canonical_target,second_first_target_same,firstSwap_target hd] at he
  exact he.symm

end CyclicBell.General
