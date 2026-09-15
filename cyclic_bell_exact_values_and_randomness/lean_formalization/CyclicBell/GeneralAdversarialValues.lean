import CyclicBell.GeneralCommutingGuessing
import CyclicBell.GeneralModelCounterexamples

/-! Literal adversarial q/qa/qc extended-correlation models and the paper's
value-conditioned guessing lower bounds. None of the validity predicates
contains Bell saturation. The qa closure precedes the equality slice.
UNCOMPILED SOURCE CANDIDATES: no axiom output or kernel checking exists yet. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder Topology
namespace CyclicBell.General
variable {d : ℕ} [NeZero d] {α β : Type}

/-- Finite, unrestricted local dimensions; arbitrary normalized mixed ABE state
and arbitrary Eve POVM. -/
def GuessQ (d : ℕ) [NeZero d] (α β : Type) : Set (ExtendedBehavior d α β) :=
  {r | ∃ (ι κ ε : Type) (fι : Fintype ι) (fκ : Fintype κ) (fε : Fintype ε),
    letI := fι
    letI := fκ
    letI := fε
    ∃ (eι : DecidableEq ι) (eκ : DecidableEq κ) (eε : DecidableEq ε),
    letI := eι
    letI := eκ
    letI := eε
    ∃ s : TripartiteOn d α β ι κ ε,tripartiteBehavior s=r}

/-- Closure of FULL extended correlations, not of saturated correlations and
not arbitrary extensions of a marginal already in Qqa. -/
def GuessQa (d : ℕ) [NeZero d] (α β : Type) : Set (ExtendedBehavior d α β) :=
  closure (GuessQ d α β)

def GuessQc (d : ℕ) [NeZero d] (α β : Type) : Set (ExtendedBehavior d α β) :=
  {r | ∃ (H : Type) (nH : NormedAddCommGroup H),
    letI := nH
    ∃ (iH : InnerProductSpace ℂ H),
    letI := iH
    ∃ (cH : CompleteSpace H),
    letI := cH
    ∃ s : CommutingEveOn d α β H,commutingExtendedBehavior s=r}

def GvalQ (f : BellBehavior d α β → ℝ) (x : α) (y : β) : ℝ :=
  valueGuessing (GuessQ d α β) f (betaQ f) x y

def GvalQa (f : BellBehavior d α β → ℝ) (x : α) (y : β) : ℝ :=
  valueGuessing (GuessQa d α β) f (betaQa f) x y

def GvalQc (f : BellBehavior d α β → ℝ) (x : α) (y : β) : ℝ :=
  valueGuessing (GuessQc d α β) f (betaQc f) x y

theorem tripartiteBehavior_mem_GuessQ {ι κ ε : Type}
    [Fintype ι] [Fintype κ] [Fintype ε]
    [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]
    (s : TripartiteOn d α β ι κ ε) : tripartiteBehavior s∈GuessQ d α β := by
  exact ⟨ι,κ,ε,inferInstance,inferInstance,inferInstance,inferInstance,inferInstance,
    inferInstance,s,rfl⟩

theorem commutingExtended_mem_GuessQc {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (s : CommutingEveOn d α β H) :
    commutingExtendedBehavior s∈GuessQc d α β :=
  ⟨H,inferInstance,inferInstance,inferInstance,s,rfl⟩

theorem GuessQ_subset_GuessQa : GuessQ d α β⊆GuessQa d α β := subset_closure

theorem GuessQ_subset_GuessQc : GuessQ d α β⊆GuessQc d α β := by
  rintro r ⟨ι,κ,ε,fι,fκ,fε,eι,eκ,eε,s,rfl⟩
  letI := fι
  letI := fκ
  letI := fε
  letI := eι
  letI := eκ
  letI := eε
  rw [← tripartiteToCommuting_behavior s]
  exact commutingExtended_mem_GuessQc (tripartiteToCommuting s)

theorem GuessQ_normalized (r : ExtendedBehavior d α β) (hr : r∈GuessQ d α β) :
    ExtendedNormalized r := by
  rcases hr with ⟨ι,κ,ε,fι,fκ,fε,eι,eκ,eε,s,rfl⟩
  letI := fι
  letI := fκ
  letI := fε
  letI := eι
  letI := eκ
  letI := eε
  exact tripartiteBehavior_normalized s

theorem GuessQa_normalized (r : ExtendedBehavior d α β) (hr : r∈GuessQa d α β) :
    ExtendedNormalized r := extendedNormalized_closure _ GuessQ_normalized r hr

theorem GuessQc_normalized (r : ExtendedBehavior d α β) (hr : r∈GuessQc d α β) :
    ExtendedNormalized r := by
  rcases hr with ⟨H,nH,iH,cH,s,rfl⟩
  letI := nH
  letI := iH
  letI := cH
  exact commutingExtended_normalized s

/-- Forgetting Eve can be realized by grouping her finite tensor factor with
Bob and measuring its identity. No partial trace or purification is assumed. -/
def forgetTripartite {ι κ ε : Type} [Fintype ι] [Fintype κ] [Fintype ε]
    [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]
    (s : TripartiteOn d α β ι κ ε) : StrategyOn d α β ι (κ×ε) where
  state := {
    density := s.state.density.submatrix (Equiv.prodAssoc ι κ ε).symm (Equiv.prodAssoc ι κ ε).symm
    positive := s.state.positive.submatrix _
    normalized := by
      simpa only [Matrix.trace,Matrix.diag_apply,Matrix.submatrix_apply,
        Fintype.sum_prod_type,Equiv.prodAssoc_symm_apply] using s.state.normalized }
  alice := s.alice
  bob := fun y => leftMeasurement (κ := ε) (s.bob y)

theorem forgetTripartite_behavior {ι κ ε : Type} [Fintype ι] [Fintype κ] [Fintype ε]
    [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]
    (s : TripartiteOn d α β ι κ ε) : behavior (forgetTripartite s)=forgetE (tripartiteBehavior s) := by
  funext x y a b
  rw [tripartiteBehavior_marginal]
  simp [behavior,bornProbability,stateEval,forgetTripartite,leftMeasurement,
    Matrix.trace,Matrix.diag_apply,Matrix.mul_apply,Matrix.submatrix_apply,kron,
    Fintype.sum_prod_type,mul_assoc]

theorem GuessQ_marginal (r : ExtendedBehavior d α β) (hr : r∈GuessQ d α β) :
    forgetE r∈Qq d α β := by
  rcases hr with ⟨ι,κ,ε,fι,fκ,fε,eι,eκ,eε,s,rfl⟩
  letI := fι
  letI := fκ
  letI := fε
  letI := eι
  letI := eκ
  letI := eε
  rw [← forgetTripartite_behavior s]
  exact behavior_mem_Qq (forgetTripartite s)

theorem GuessQa_marginal (r : ExtendedBehavior d α β) (hr : r∈GuessQa d α β) :
    forgetE r∈Qqa d α β := by
  have hc : IsClosed {r : ExtendedBehavior d α β | forgetE r∈Qqa d α β} :=
    isClosed_closure.preimage forgetE_continuous
  exact closure_minimal (fun q hq => Qq_subset_Qqa (GuessQ_marginal q hq)) hc hr

theorem GuessQc_marginal (r : ExtendedBehavior d α β) (hr : r∈GuessQc d α β) :
    forgetE r∈Qqc d α β := by
  rcases hr with ⟨H,nH,iH,cH,s,rfl⟩
  letI := nH
  letI := iH
  letI := cH
  rw [forgetE_commutingExtended]
  exact commutingBehavior_mem_Qqc s.ab

/-- Nonemptiness, finite-to-qc membership, and success use the SAME complete
finite physical extension throughout the proof. -/
theorem finite_fixed_guess_three_models {ι κ : Type} [Fintype ι] [Fintype κ]
    [DecidableEq ι] [DecidableEq κ] (s : StrategyOn d α β ι κ) (g : GuessLabel d) :
    attachFixedGuess (behavior s) g∈GuessQ d α β ∧
    attachFixedGuess (behavior s) g∈GuessQa d α β ∧
    attachFixedGuess (behavior s) g∈GuessQc d α β := by
  have h : attachFixedGuess (behavior s) g∈GuessQ d α β := by
    rw [← trivialTripartite_behavior s g]
    exact tripartiteBehavior_mem_GuessQ _
  exact ⟨h,GuessQ_subset_GuessQa h,GuessQ_subset_GuessQc h⟩

/-- The three model maxima are supplied by the independent universal value
proofs. This helper never asserts that the fixed guess is the optimal adversary. -/
theorem three_model_Gval_interval {ι κ : Type} [Fintype ι] [Fintype κ]
    [DecidableEq ι] [DecidableEq κ] (s : StrategyOn d α β ι κ)
    (f : BellBehavior d α β → ℝ) (x : α) (y : β) (g : GuessLabel d)
    (hq : f (behavior s)=betaQ f) (hqa : f (behavior s)=betaQa f)
    (hqc : f (behavior s)=betaQc f) :
    (behavior s x y g.1 g.2≤GvalQ f x y ∧ GvalQ f x y≤1) ∧
    (behavior s x y g.1 g.2≤GvalQa f x y ∧ GvalQa f x y≤1) ∧
    (behavior s x y g.1 g.2≤GvalQc f x y ∧ GvalQc f x y≤1) := by
  obtain ⟨hm,hm',hm''⟩ := finite_fixed_guess_three_models s g
  have eqm : forgetE (attachFixedGuess (behavior s) g)=behavior s := forgetE_attachFixedGuess _ _
  have h₁ := valueGuessing_interval_from_witness (GuessQ d α β) GuessQ_normalized
    f (betaQ f) x y (attachFixedGuess (behavior s) g) hm (by rw [eqm]; exact hq)
  have h₂ := valueGuessing_interval_from_witness (GuessQa d α β) GuessQa_normalized
    f (betaQa f) x y (attachFixedGuess (behavior s) g) hm' (by rw [eqm]; exact hqa)
  have h₃ := valueGuessing_interval_from_witness (GuessQc d α β) GuessQc_normalized
    f (betaQc f) x y (attachFixedGuess (behavior s) g) hm'' (by rw [eqm]; exact hqc)
  simpa only [guessingSuccess_attachFixedGuess,GvalQ,GvalQa,GvalQc] using And.intro h₁ (And.intro h₂ h₃)

def paperGuessFloor (d : ℕ) : ℝ := 1/(d : ℝ)^2+
  2*Real.sin (Real.pi/(d : ℝ))*Real.sin (3*Real.pi/(d : ℝ))/
    ((d : ℝ)^2*((d : ℝ)-1))

/-- Manuscript eq:value-conditioned, first augmented family, all three actual
adversarial optimization domains. This is a lower bound, not an exact optimum. -/
theorem first_value_conditioned_guessing_bounds (hd : 4≤d) :
    (paperGuessFloor d≤GvalQ (firstAugmentedBell (d := d)) 1 none ∧
      GvalQ (firstAugmentedBell (d := d)) 1 none≤1) ∧
    (paperGuessFloor d≤GvalQa (firstAugmentedBell (d := d)) 1 none ∧
      GvalQa (firstAugmentedBell (d := d)) 1 none≤1) ∧
    (paperGuessFloor d≤GvalQc (firstAugmentedBell (d := d)) 1 none ∧
      GvalQc (firstAugmentedBell (d := d)) 1 none≤1) := by
  obtain ⟨s,hm,hq,hqa,hqc,hnu,hmarg,a,b,hab⟩ := first_three_model_counterexample hd
  obtain ⟨h₁,h₂,h₃⟩ := three_model_Gval_interval s firstAugmentedBell 1 none (a,b) hq hqa hqc
  exact ⟨⟨hab.trans h₁.1,h₁.2⟩,⟨hab.trans h₂.1,h₂.2⟩,⟨hab.trans h₃.1,h₃.2⟩⟩

theorem second_value_conditioned_guessing_bounds (hd : 4≤d) :
    (paperGuessFloor d≤GvalQ (secondAugmentedBell (d := d)) 1 none ∧
      GvalQ (secondAugmentedBell (d := d)) 1 none≤1) ∧
    (paperGuessFloor d≤GvalQa (secondAugmentedBell (d := d)) 1 none ∧
      GvalQa (secondAugmentedBell (d := d)) 1 none≤1) ∧
    (paperGuessFloor d≤GvalQc (secondAugmentedBell (d := d)) 1 none ∧
      GvalQc (secondAugmentedBell (d := d)) 1 none≤1) := by
  obtain ⟨s,hm,hq,hqa,hqc,hnu,hmarg,a,b,hab⟩ := second_three_model_counterexample hd
  obtain ⟨h₁,h₂,h₃⟩ := three_model_Gval_interval s secondAugmentedBell 1 none (a,b) hq hqa hqc
  exact ⟨⟨hab.trans h₁.1,h₁.2⟩,⟨hab.trans h₂.1,h₂.2⟩,⟨hab.trans h₃.1,h₃.2⟩⟩

theorem first_value_conditioned_strict_gap (hd : 4≤d) :
    1/(d : ℝ)^2<GvalQ (firstAugmentedBell (d := d)) 1 none ∧
    1/(d : ℝ)^2<GvalQa (firstAugmentedBell (d := d)) 1 none ∧
    1/(d : ℝ)^2<GvalQc (firstAugmentedBell (d := d)) 1 none := by
  obtain ⟨h₁,h₂,h₃⟩ := first_value_conditioned_guessing_bounds hd
  exact ⟨(quantitative_gap_positive hd).trans_le h₁.1,
    (quantitative_gap_positive hd).trans_le h₂.1,(quantitative_gap_positive hd).trans_le h₃.1⟩

theorem second_value_conditioned_strict_gap (hd : 4≤d) :
    1/(d : ℝ)^2<GvalQ (secondAugmentedBell (d := d)) 1 none ∧
    1/(d : ℝ)^2<GvalQa (secondAugmentedBell (d := d)) 1 none ∧
    1/(d : ℝ)^2<GvalQc (secondAugmentedBell (d := d)) 1 none := by
  obtain ⟨h₁,h₂,h₃⟩ := second_value_conditioned_guessing_bounds hd
  exact ⟨(quantitative_gap_positive hd).trans_le h₁.1,
    (quantitative_gap_positive hd).trans_le h₂.1,(quantitative_gap_positive hd).trans_le h₃.1⟩

/-- The literal d=4 floor is 1/12; the explicit table later strengthens it to
3/32. This control prevents confusing the general estimate with the exact table. -/
theorem paperGuessFloor_four : paperGuessFloor 4=(1 : ℝ)/12 := by
  unfold paperGuessFloor
  norm_num only [Nat.cast_ofNat]
  have hs : Real.sin (3*Real.pi/4)=Real.sin (Real.pi/4) := by
    rw [show 3*Real.pi/4=Real.pi-Real.pi/4 by ring,Real.sin_pi_sub]
  rw [hs,Real.sin_pi_div_four]
  nlinarith [Real.sq_sqrt (by norm_num : (0 : ℝ)≤2)]

end CyclicBell.General
