import CyclicBell.GeneralPhaseTables
import CyclicBell.GeneralSecondWitness
import CyclicBell.GeneralOperational

/-! Explicit transport between the two Bob-output conventions. The alternate
Bell functional is defined with adjointed Bob observables; no invariance of an
unchanged arbitrary functional is asserted. Guessing statements below concern
observed maximum entries and fixed deterministic guesses, not Eve optimization. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {ι κ : Type*} [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ]

/-- Negating outcome labels sends the encoded observable to its adjoint. -/
theorem negateMeasurement_encoded (M : Measurement d ι) :
    encoded (negateMeasurement M)=(encoded M).conjTranspose := by
  unfold encoded
  rw [measurement_spectral_star]
  change (∑ a,chi a • M.effect (-a))=∑ a,star (chi a) • M.effect a
  simpa only [neg_neg,chi_star] using
    sum_negate (fun a : Ix d => chi (-a) • M.effect a)

@[simp] theorem negateMeasurement_involutive (M : Measurement d ι) :
    negateMeasurement (negateMeasurement M)=M := by
  cases M
  simp only [negateMeasurement,neg_neg]

/-- Every Bob measurement is relabeled; the physical state and Alice's effects
are exactly those of the given strategy. -/
def negateBobOutcomes {α β : Type*} (s : StrategyOn d α β ι κ) : StrategyOn d α β ι κ where
  state := s.state
  alice := s.alice
  bob := fun y => negateMeasurement (s.bob y)

@[simp] theorem negateBobOutcomes_behavior {α β : Type*} (s : StrategyOn d α β ι κ)
    (x : α) (y : β) (a b : Ix d) :
    behavior (negateBobOutcomes s) x y a b=behavior s x y a (-b) := rfl

@[simp] theorem negateBobOutcomes_involutive {α β : Type*} (s : StrategyOn d α β ι κ) :
    negateBobOutcomes (negateBobOutcomes s)=s := by
  cases s
  simp only [negateBobOutcomes,negateMeasurement_involutive]

/-- The adjoint-convention Fourier combination retains the plus character in
its definition. Equivalently it is the adjoint of the opposite Fourier mode. -/
def secondAdjointFourier (B : Ix d → Mat κ) (l : Ix d) : Mat κ :=
  secondFourier (fun y => (B y).conjTranspose) l

theorem secondAdjointFourier_opposite_mode (B : Ix d → Mat κ) (l : Ix d) :
    secondAdjointFourier B l=(secondFourier B (-l)).conjTranspose := by
  simp only [secondAdjointFourier,secondFourier,moduleFourier,
    Matrix.conjTranspose_sum,Matrix.conjTranspose_smul,chi_star,neg_mul,neg_neg]

/-- Explicitly transported second Bell functional: both the Fourier terms and
the extra Bob setting use the adjointed encoded Bob observable. -/
def secondAdjointValue (s : StrategyOn d (Ix d) (AugmentedInputs d) ι κ) : ℝ :=
  (∑ l : Ix d,stateEval s.state.density (star (generalLambda l) •
    kron (encoded (s.alice l)) (secondAdjointFourier (fun y => encoded (s.bob (some y))) l)))+
    stateEval s.state.density (kron (encoded (s.alice 0)) ((encoded (s.bob none)).conjTranspose))

theorem secondAdjointValue_eq_relabel (s : StrategyOn d (Ix d) (AugmentedInputs d) ι κ) :
    secondAdjointValue s=secondValue (negateBobOutcomes s) := by
  simp only [secondAdjointValue,secondAdjointFourier,secondValue,negateBobOutcomes,
    negateMeasurement_encoded]

/-- Relabeling and transporting the convention together preserve the value. -/
theorem secondAdjointValue_negateBob (s : StrategyOn d (Ix d) (AugmentedInputs d) ι κ) :
    secondAdjointValue (negateBobOutcomes s)=secondValue s := by
  rw [secondAdjointValue_eq_relabel,negateBobOutcomes_involutive]

theorem secondAdjointValue_upper (hd : 2≤d)
    (s : StrategyOn d (Ix d) (AugmentedInputs d) ι κ) : secondAdjointValue s≤(d : ℝ)+1 := by
  rw [secondAdjointValue_eq_relabel]
  exact second_physical_upper hd _

/-- The actual cyclic witness in the alternate output convention. -/
def secondAdjointPermutationStrategy (hd : 2≤d) (σ : Equiv.Perm (Ix d)) :
    StrategyOn d (Ix d) (AugmentedInputs d) (Ix d) (Ix d) :=
  negateBobOutcomes (secondPermutationStrategy hd σ)

theorem secondAdjointPermutation_bob_encoded (hd : 2≤d) (σ : Equiv.Perm (Ix d))
    (y : AugmentedInputs d) :
    encoded ((secondAdjointPermutationStrategy hd σ).bob y)=
      (encoded ((secondPermutationStrategy hd σ).bob y)).conjTranspose :=
  negateMeasurement_encoded _

theorem secondAdjointPermutation_behavior (hd : 2≤d) (σ : Equiv.Perm (Ix d))
    (x : Ix d) (y : AugmentedInputs d) (a b : Ix d) :
    behavior (secondAdjointPermutationStrategy hd σ) x y a b=
      behavior (secondPermutationStrategy hd σ) x y a (-b) := rfl

theorem secondAdjointPermutation_attains (hd : 2≤d) (σ : Equiv.Perm (Ix d)) :
    secondAdjointValue (secondAdjointPermutationStrategy hd σ)=(d : ℝ)+1 := by
  rw [secondAdjointPermutationStrategy,secondAdjointValue_negateBob,secondPermutation_attains]

/-- Comparison is against every finite local dimension pair, using the
alternate functional on both the competitor and the relabeled witness. -/
theorem secondAdjointPermutation_maximal (hd : 2≤d) (σ : Equiv.Perm (Ix d))
    (t : StrategyOn d (Ix d) (AugmentedInputs d) ι κ) :
    secondAdjointValue t≤secondAdjointValue (secondAdjointPermutationStrategy hd σ) := by
  rw [secondAdjointPermutation_attains]
  exact secondAdjointValue_upper hd t

def relabelOutcomeTable (p : Ix d → Ix d → ℝ) (σ τ : Equiv.Perm (Ix d)) : Ix d → Ix d → ℝ :=
  fun a b => p (σ a) (τ b)

/-- Equality of value sets under any pair of bijective local output relabelings. -/
theorem relabelOutcomeTable_range (p : Ix d → Ix d → ℝ) (σ τ : Equiv.Perm (Ix d)) :
    Set.range (fun ab : Ix d×Ix d => relabelOutcomeTable p σ τ ab.1 ab.2)=
      Set.range (fun ab : Ix d×Ix d => p ab.1 ab.2) := by
  ext r
  constructor
  · rintro ⟨⟨a,b⟩,h⟩
    exact ⟨(σ a,τ b),h⟩
  · rintro ⟨⟨a,b⟩,h⟩
    refine ⟨(σ.symm a,τ.symm b),?_⟩
    simpa only [relabelOutcomeTable,Equiv.apply_symm_apply] using h

/-- Largest observed joint probability. The finite range makes this a genuine
attained maximum, independent of any adversarial side-information model. -/
def observedMaxEntry (p : Ix d → Ix d → ℝ) : ℝ := sSup (Set.range (fun ab : Ix d×Ix d => p ab.1 ab.2))

theorem observedMaxEntry_attained (p : Ix d → Ix d → ℝ) : ∃ a b,observedMaxEntry p=p a b := by
  have h := (Set.range_nonempty (fun ab : Ix d×Ix d => p ab.1 ab.2)).csSup_mem
    (Set.finite_range _)
  obtain ⟨⟨a,b⟩,hab⟩ := h
  exact ⟨a,b,hab.symm⟩

theorem le_observedMaxEntry (p : Ix d → Ix d → ℝ) (a b : Ix d) : p a b≤observedMaxEntry p :=
  le_csSup (Set.finite_range _).bddAbove ⟨(a,b),rfl⟩

theorem observedMaxEntry_relabel (p : Ix d → Ix d → ℝ) (σ τ : Equiv.Perm (Ix d)) :
    observedMaxEntry (relabelOutcomeTable p σ τ)=observedMaxEntry p := by
  unfold observedMaxEntry
  rw [relabelOutcomeTable_range]

theorem relabelOutcomeTable_uniform_iff (p : Ix d → Ix d → ℝ) (σ τ : Equiv.Perm (Ix d)) (c : ℝ) :
    (∀ a b,relabelOutcomeTable p σ τ a b=c) ↔ ∀ a b,p a b=c := by
  constructor
  · intro h a b
    simpa only [relabelOutcomeTable,Equiv.apply_symm_apply] using h (σ.symm a) (τ.symm b)
  · intro h a b
    exact h (σ a) (τ b)

theorem negateBob_observedMaxEntry {α β : Type*} (s : StrategyOn d α β ι κ) (x : α) (y : β) :
    observedMaxEntry (behavior (negateBobOutcomes s) x y)=observedMaxEntry (behavior s x y) :=
  observedMaxEntry_relabel (behavior s x y) (Equiv.refl _) (Equiv.neg _)

/-- A fixed guess is transported by the same output bijection. This is an
actual trivial-Eve success probability, without a claim about optimal Eve. -/
theorem negateBob_fixedGuessSuccess {α β : Type*} (s : StrategyOn d α β ι κ)
    (x : α) (y : β) (a b : Ix d) :
    fixedGuessSuccess (negateBobOutcomes s).state.density
      ((negateBobOutcomes s).alice x) ((negateBobOutcomes s).bob y) (a,b)=
    fixedGuessSuccess s.state.density (s.alice x) (s.bob y) (a,-b) := by
  rw [fixedGuessSuccess_eq,fixedGuessSuccess_eq]
  rfl

/-- The observed maximum is exactly the best deterministic fixed guess on
this realization, with the explicit one-dimensional Eve model above. -/
theorem observedMaxEntry_eq_bestFixedGuess {α β : Type*} (s : StrategyOn d α β ι κ)
    (x : α) (y : β) :
    observedMaxEntry (behavior s x y)=sSup (Set.range (fun g : Ix d×Ix d =>
      fixedGuessSuccess s.state.density (s.alice x) (s.bob y) g)) := by
  unfold observedMaxEntry
  apply congrArg sSup
  apply congrArg Set.range
  funext g
  rw [fixedGuessSuccess_eq]
  rfl

theorem negateBob_bestFixedGuess {α β : Type*} (s : StrategyOn d α β ι κ) (x : α) (y : β) :
    sSup (Set.range (fun g : Ix d×Ix d => fixedGuessSuccess
      (negateBobOutcomes s).state.density ((negateBobOutcomes s).alice x) ((negateBobOutcomes s).bob y) g))=
    sSup (Set.range (fun g : Ix d×Ix d => fixedGuessSuccess
      s.state.density (s.alice x) (s.bob y) g)) := by
  rw [← observedMaxEntry_eq_bestFixedGuess,← observedMaxEntry_eq_bestFixedGuess,
    negateBob_observedMaxEntry]

theorem secondAdjointSwap_nonuniform (hd : 4≤d) :
    ¬ ∀ a b,behavior (secondAdjointPermutationStrategy (by omega : 2≤d) (finalSwap d)) 1 none a b=
      1/(d : ℝ)^2 := by
  intro h
  apply swappedTarget_not_uniform hd
  intro a b
  have he := h a (-b)
  simpa only [secondAdjointPermutation_behavior,neg_neg,second_first_target_same,firstSwap_target hd] using he

theorem secondAdjointSwap_observedMaxEntry (hd : 4≤d) :
    observedMaxEntry (d := d) (behavior (secondAdjointPermutationStrategy (by omega : 2≤d) (finalSwap d)) 1 none)=
      observedMaxEntry (d := d) (swappedTarget d) := by
  rw [secondAdjointPermutationStrategy,negateBob_observedMaxEntry]
  apply congrArg (observedMaxEntry (d := d))
  funext a b
  rw [second_first_target_same,firstSwap_target hd]

/-- The concrete bias lower bound survives the convention change. -/
theorem secondAdjointSwap_quantitative (hd : 4≤d) :
    ∃ a b,1/(d : ℝ)^2+
      2*Real.sin (Real.pi/(d : ℝ))*Real.sin (3*Real.pi/(d : ℝ))/
        ((d : ℝ)^2*((d : ℝ)-1))≤
      behavior (secondAdjointPermutationStrategy (by omega : 2≤d) (finalSwap d)) 1 none a b := by
  obtain ⟨a,b,h⟩ := swappedTarget_quantitative (d := d) hd
  refine ⟨a,-b,?_⟩
  simpa only [secondAdjointPermutation_behavior,neg_neg,second_first_target_same,firstSwap_target hd] using h

end CyclicBell.General
