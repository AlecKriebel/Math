import CyclicBell.GeneralPOVMMaximum
import CyclicBell.GeneralAdversarialEntropy

/-! The finite-q flattened extended-correlation supremum equals the outer
supremum of the actual attained fixed-realization POVM maxima. The nonempty
saturation hypothesis of the generic helper is discharged for both families.
No maximum over all realizations is asserted. UNCOMPILED SOURCE. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d] {α β : Type}

def optimizedFiniteScores (f : BellBehavior d α β → ℝ) (x : α) (y : β) : Set ℝ :=
  {t | ∃ (ι κ ε : Type) (fι : Fintype ι) (fκ : Fintype κ) (fε : Fintype ε),
    letI := fι
    letI := fκ
    letI := fε
    ∃ (eι : DecidableEq ι) (eκ : DecidableEq κ) (eε : DecidableEq ε),
    letI := eι
    letI := eκ
    letI := eε
    ∃ s : TripartiteOn d α β ι κ ε,
      f (forgetE (tripartiteBehavior s))=betaQ f ∧
      finitePOVMValue (tripartiteConditionals s x y)=t}

/-- Optimizing Eve does not change the full observed behavior or its Bell score. -/
theorem optimizedFiniteScore_realized (f : BellBehavior d α β → ℝ) (x : α) (y : β)
    (t : ℝ) (ht : t∈optimizedFiniteScores f x y) :
    ∃ r : ExtendedBehavior d α β,r∈GuessQ d α β ∧
      f (forgetE r)=betaQ f ∧ guessingSuccess r x y=t := by
  rcases ht with ⟨ι,κ,ε,fι,fκ,fε,eι,eκ,eε,s,hs,he⟩
  letI := fι
  letI := fκ
  letI := fε
  letI := eι
  letI := eκ
  letI := eε
  obtain ⟨Q,hmargin,hatt,hinterval,hmax⟩ := fixed_realization_guessing_maximum s x y
  refine ⟨tripartiteBehavior (withEve s Q),tripartiteBehavior_mem_GuessQ _,?_,hatt.trans he⟩
  rw [hmargin]
  exact hs

theorem optimizedFiniteScores_bddAbove (f : BellBehavior d α β → ℝ) (x : α) (y : β) :
    BddAbove (optimizedFiniteScores f x y) := by
  refine ⟨1,?_⟩
  intro t ht
  obtain ⟨r,hr,hscore,hguess⟩ := optimizedFiniteScore_realized f x y t ht
  rw [← hguess]
  exact guessingSuccess_le_one r (GuessQ_normalized r hr) x y

theorem finitePOVMValue_mem_optimized {ι κ ε : Type}
    [Fintype ι] [Fintype κ] [Fintype ε] [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]
    (s : TripartiteOn d α β ι κ ε) (f : BellBehavior d α β → ℝ) (x : α) (y : β)
    (hs : f (forgetE (tripartiteBehavior s))=betaQ f) :
    finitePOVMValue (tripartiteConditionals s x y)∈optimizedFiniteScores f x y := by
  exact ⟨ι,κ,ε,inferInstance,inferInstance,inferInstance,
    inferInstance,inferInstance,inferInstance,s,hs,rfl⟩

theorem success_le_fixedPOVMValue {ι κ ε : Type}
    [Fintype ι] [Fintype κ] [Fintype ε] [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]
    (s : TripartiteOn d α β ι κ ε) (x : α) (y : β) :
    guessingSuccess (tripartiteBehavior s) x y≤finitePOVMValue (tripartiteConditionals s x y) := by
  obtain ⟨Q,hmargin,hatt,hinterval,hmax⟩ := fixed_realization_guessing_maximum s x y
  have h := hmax s.eve
  rw [hatt] at h
  simpa only [withEve] using h

/-- A nonempty saturation set is required because the generic score need not
attain its quantum supremum. Both manuscript families supply the witness. -/
theorem finite_nested_supremum_eq {ι κ ε : Type}
    [Fintype ι] [Fintype κ] [Fintype ε] [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]
    (s : TripartiteOn d α β ι κ ε) (f : BellBehavior d α β → ℝ) (x : α) (y : β)
    (hs : f (forgetE (tripartiteBehavior s))=betaQ f) :
    GvalQ f x y=sSup (optimizedFiniteScores f x y) := by
  have hn : (optimizedFiniteScores f x y).Nonempty :=
    ⟨_,finitePOVMValue_mem_optimized s f x y hs⟩
  have hr : tripartiteBehavior s∈valueSlice (GuessQ d α β) f (betaQ f) :=
    ⟨tripartiteBehavior_mem_GuessQ s,hs⟩
  apply le_antisymm
  · change sSup ((fun r => guessingSuccess r x y) '' valueSlice (GuessQ d α β) f (betaQ f))≤_
    have hne : ((fun r => guessingSuccess r x y) '' valueSlice (GuessQ d α β) f (betaQ f)).Nonempty :=
      ⟨_,tripartiteBehavior s,hr,rfl⟩
    apply csSup_le hne
    rintro t ⟨r,⟨hmodel,hscore⟩,rfl⟩
    rcases hmodel with ⟨i,j,e,fi,fj,fe,ei,ej,ee,R,hR⟩
    letI := fi
    letI := fj
    letI := fe
    letI := ei
    letI := ej
    letI := ee
    subst r
    exact (success_le_fixedPOVMValue R x y).trans
      (le_csSup (optimizedFiniteScores_bddAbove f x y)
        (finitePOVMValue_mem_optimized R f x y hscore))
  · apply csSup_le hn
    intro t ht
    obtain ⟨r,hmodel,hscore,hguess⟩ := optimizedFiniteScore_realized f x y t ht
    rw [← hguess]
    exact le_valueGuessing_of_member (GuessQ d α β) GuessQ_normalized f (betaQ f) x y r hmodel hscore

/-- Literal finite-q outer supremum of fixed-realization maxima, first family. -/
theorem first_GvalQ_nested (hd : 2≤d) :
    GvalQ (firstAugmentedBell (d := d)) 1 none=
      sSup (optimizedFiniteScores (firstAugmentedBell (d := d)) 1 none) := by
  let s₀ := firstPermutationStrategy hd (Equiv.refl (Ix d))
  let s := trivialTripartite s₀ (0,0)
  apply finite_nested_supremum_eq s
  rw [trivialTripartite_marginal,firstAugmentedBell_behavior]
  exact (firstPermutation_attains hd _).trans (first_augmented_values_q_qa_qc hd).1.symm

theorem second_GvalQ_nested (hd : 2≤d) :
    GvalQ (secondAugmentedBell (d := d)) 1 none=
      sSup (optimizedFiniteScores (secondAugmentedBell (d := d)) 1 none) := by
  let s₀ := secondPermutationStrategy hd (Equiv.refl (Ix d))
  let s := trivialTripartite s₀ (0,0)
  apply finite_nested_supremum_eq s
  rw [trivialTripartite_marginal,secondAugmentedBell_behavior]
  exact (secondPermutation_attains hd _).trans (second_augmented_values_q_qa_qc hd).1.symm

end CyclicBell.General
