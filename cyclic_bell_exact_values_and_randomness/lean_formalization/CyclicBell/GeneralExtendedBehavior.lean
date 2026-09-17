import CyclicBell.GeneralBehavior

/-! Real extended correlations and the actual guessing supremum. This module
has no physical strategy or witness assumptions.
The closure is taken on full extended arrays before imposing Bell equality. -/
noncomputable section
open scoped BigOperators Topology
namespace CyclicBell.General
variable {d : ℕ} [NeZero d] {α β : Type*}

abbrev GuessLabel (d : ℕ) := Ix d × Ix d
abbrev ExtendedBehavior (d : ℕ) [NeZero d] (α β : Type*) :=
  α → β → Ix d → Ix d → GuessLabel d → ℝ

def forgetE (r : ExtendedBehavior d α β) : BellBehavior d α β :=
  fun x y a b => ∑ g,r x y a b g

def guessingSuccess (r : ExtendedBehavior d α β) (x : α) (y : β) : ℝ :=
  ∑ a,∑ b,r x y a b (a,b)

/-- Only ordinary probability requirements, with no Bell hypothesis. -/
def ExtendedNormalized (r : ExtendedBehavior d α β) : Prop :=
  (∀ x y a b g,0≤r x y a b g) ∧ (∀ x y,(∑ a,∑ b,∑ g,r x y a b g)=1)

theorem forgetE_continuous : Continuous (forgetE (d := d) (α := α) (β := β)) := by
  unfold forgetE
  fun_prop

theorem guessingSuccess_continuous (x : α) (y : β) :
    Continuous (fun r : ExtendedBehavior d α β => guessingSuccess r x y) := by
  unfold guessingSuccess
  fun_prop

theorem extendedNormalized_isClosed :
    IsClosed {r : ExtendedBehavior d α β | ExtendedNormalized r} := by
  have hn : IsClosed {r : ExtendedBehavior d α β | ∀ x y a b g,0≤r x y a b g} := by
    simp only [Set.setOf_forall]
    exact isClosed_iInter fun x => isClosed_iInter fun y =>
      isClosed_iInter fun a => isClosed_iInter fun b => isClosed_iInter fun g =>
        isClosed_le continuous_const (by fun_prop)
  have ht : IsClosed {r : ExtendedBehavior d α β | ∀ x y,(∑ a,∑ b,∑ g,r x y a b g)=1} := by
    simp only [Set.setOf_forall]
    exact isClosed_iInter fun x => isClosed_iInter fun y =>
      isClosed_eq (by fun_prop) continuous_const
  exact hn.inter ht

theorem extendedNormalized_closure (S : Set (ExtendedBehavior d α β))
    (hS : ∀ r ∈ S,ExtendedNormalized r) :
    ∀ r ∈ closure S,ExtendedNormalized r :=
  closure_minimal hS extendedNormalized_isClosed

theorem guessingSuccess_nonnegative (r : ExtendedBehavior d α β)
    (hr : ExtendedNormalized r) (x : α) (y : β) : 0≤guessingSuccess r x y := by
  exact Finset.sum_nonneg fun a _ => Finset.sum_nonneg fun b _ => hr.1 x y a b (a,b)

theorem guessingSuccess_le_one (r : ExtendedBehavior d α β)
    (hr : ExtendedNormalized r) (x : α) (y : β) : guessingSuccess r x y≤1 := by
  calc
    guessingSuccess r x y ≤ ∑ a,∑ b,∑ g,r x y a b g := by
      apply Finset.sum_le_sum
      intro a _
      apply Finset.sum_le_sum
      intro b _
      exact Finset.single_le_sum (fun g _ => hr.1 x y a b g) (Finset.mem_univ (a,b))
    _ = 1 := hr.2 x y

theorem extended_marginal_normalized (r : ExtendedBehavior d α β)
    (hr : ExtendedNormalized r) (x : α) (y : β) :
    (∑ a,∑ b,forgetE r x y a b)=1 := hr.2 x y

/-- A fixed guess attaches a genuine deterministic classical Eve output. -/
def attachFixedGuess (p : BellBehavior d α β) (g : GuessLabel d) : ExtendedBehavior d α β :=
  fun x y a b h => if h=g then p x y a b else 0

theorem forgetE_attachFixedGuess (p : BellBehavior d α β) (g : GuessLabel d) :
    forgetE (attachFixedGuess p g)=p := by
  classical
  funext x y a b
  simp [forgetE,attachFixedGuess]

theorem guessingSuccess_attachFixedGuess (p : BellBehavior d α β) (g : GuessLabel d)
    (x : α) (y : β) : guessingSuccess (attachFixedGuess p g) x y=p x y g.1 g.2 := by
  classical
  rcases g with ⟨a,b⟩
  simp [guessingSuccess,attachFixedGuess,Prod.mk.injEq,ite_and]

def valueSlice (S : Set (ExtendedBehavior d α β)) (f : BellBehavior d α β → ℝ)
    (v : ℝ) : Set (ExtendedBehavior d α β) := {r | r ∈ S ∧ f (forgetE r)=v}

/-- Literal supremum over all compatible extended correlations and Eve POVMs.
No special value is built into this definition. -/
def valueGuessing (S : Set (ExtendedBehavior d α β)) (f : BellBehavior d α β → ℝ)
    (v : ℝ) (x : α) (y : β) : ℝ :=
  sSup ((fun r => guessingSuccess r x y) '' valueSlice S f v)

theorem valueGuessing_bddAbove (S : Set (ExtendedBehavior d α β))
    (hS : ∀ r ∈ S,ExtendedNormalized r) (f : BellBehavior d α β → ℝ)
    (v : ℝ) (x : α) (y : β) :
    BddAbove ((fun r => guessingSuccess r x y) '' valueSlice S f v) := by
  refine ⟨1,?_⟩
  rintro t ⟨r,hr,rfl⟩
  exact guessingSuccess_le_one r (hS r hr.1) x y

theorem le_valueGuessing_of_member (S : Set (ExtendedBehavior d α β))
    (hS : ∀ r ∈ S,ExtendedNormalized r) (f : BellBehavior d α β → ℝ)
    (v : ℝ) (x : α) (y : β) (r : ExtendedBehavior d α β)
    (hr : r ∈ S) (hv : f (forgetE r)=v) : guessingSuccess r x y≤valueGuessing S f v x y := by
  exact le_csSup (valueGuessing_bddAbove S hS f v x y) ⟨r,⟨hr,hv⟩,rfl⟩

theorem valueGuessing_le_one_of_nonempty (S : Set (ExtendedBehavior d α β))
    (hS : ∀ r ∈ S,ExtendedNormalized r) (f : BellBehavior d α β → ℝ)
    (v : ℝ) (x : α) (y : β) (hne : (valueSlice S f v).Nonempty) :
    valueGuessing S f v x y≤1 := by
  apply csSup_le (hne.image _)
  rintro t ⟨r,hr,rfl⟩
  exact guessingSuccess_le_one r (hS r hr.1) x y

/-- A single witness with proved membership supplies nonemptiness and a lower bound. -/
theorem valueGuessing_interval_from_witness (S : Set (ExtendedBehavior d α β))
    (hS : ∀ r ∈ S,ExtendedNormalized r) (f : BellBehavior d α β → ℝ)
    (v : ℝ) (x : α) (y : β) (r : ExtendedBehavior d α β)
    (hr : r ∈ S) (hv : f (forgetE r)=v) :
    guessingSuccess r x y≤valueGuessing S f v x y ∧ valueGuessing S f v x y≤1 := by
  exact ⟨le_valueGuessing_of_member S hS f v x y r hr hv,
    valueGuessing_le_one_of_nonempty S hS f v x y ⟨r,hr,hv⟩⟩

/-- Inclusion is used only when it is actually proved; no Qqa⊆Qqc premise is
introduced by the concrete model theorems. -/
theorem valueGuessing_mono (S T : Set (ExtendedBehavior d α β))
    (hT : ∀ r ∈ T,ExtendedNormalized r) (hST : S⊆T)
    (f : BellBehavior d α β → ℝ) (v : ℝ) (x : α) (y : β)
    (hne : (valueSlice S f v).Nonempty) :
    valueGuessing S f v x y≤valueGuessing T f v x y := by
  apply csSup_le (hne.image _)
  rintro t ⟨r,hr,rfl⟩
  exact le_valueGuessing_of_member T hT f v x y r (hST hr.1) hr.2

end CyclicBell.General
