import CyclicBell.GeneralOneInput

/-! The Bob-one-input orientation of prop:one-input. The behavior has arbitrary
input-dependent Alice output alphabets. The proof constructs and evaluates the
actual Alice/Bob grouping projectors in the reversed order; it does not assume
a party-swap equivalence or identify the two sides by naming alone.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {X O : Type*} [Fintype X] [Fintype O] [DecidableEq X] [DecidableEq O]
variable {A : X → Type*} [∀ x,Fintype (A x)] [∀ x,DecidableEq (A x)] [∀ x,Nonempty (A x)]

/-- Bob has one input; `O` is his outcome set. Validity contains only probability
and nonsignalling constraints, not a locality or guessing conclusion. -/
structure RightOneInputBehavior (X O : Type*) [Fintype X] [Fintype O]
    (A : X → Type*) [∀ x,Fintype (A x)] where
  joint : (x : X) → A x → O → ℝ
  marginal : O → ℝ
  nonnegative : ∀ x a b,0≤joint x a b
  marginal_nonnegative : ∀ b,0≤marginal b
  marginal_normalized : ∑ b,marginal b=1
  nonsignalling : ∀ x b,∑ a,joint x a b=marginal b

def reversedOneInput (p : RightOneInputBehavior X O A) : OneInputBehavior X O A where
  joint := fun x b a => p.joint x a b
  marginal := p.marginal
  nonnegative := fun x b a => p.nonnegative x a b
  marginal_nonnegative := p.marginal_nonnegative
  marginal_normalized := p.marginal_normalized
  nonsignalling := p.nonsignalling

/-- The hidden variable stores Bob's only output and ALL of Alice's input-
dependent outputs simultaneously. -/
def rightHiddenWeight (p : RightOneInputBehavior X O A) : StoredAssignments O A → ℝ :=
  hiddenWeight (reversedOneInput p)

theorem rightHiddenWeight_nonnegative (p : RightOneInputBehavior X O A) (label : StoredAssignments O A) :
    0≤rightHiddenWeight p label := hiddenWeight_nonnegative (reversedOneInput p) label

theorem rightHiddenWeight_normalized (p : RightOneInputBehavior X O A) :
    (∑ label,rightHiddenWeight p label)=1 := hiddenWeight_normalized (reversedOneInput p)

theorem right_one_input_local (p : RightOneInputBehavior X O A) (x : X) (a : A x) (b : O) :
    (∑ label : StoredAssignments O A,if label.2 x=a ∧ label.1=b then rightHiddenWeight p label else 0)=
      p.joint x a b := by
  simpa only [rightHiddenWeight,reversedOneInput,and_comm]
    using one_input_local (reversedOneInput p) x b a

/-- Source prop:one-input in the other orientation. `storedPurification` is
symmetric in its first two coordinates, but the grouping measurements are now
literally Alice's stored-input output and Bob's single stored output. -/
theorem right_one_input_pure_projective_perfect_guess (p : RightOneInputBehavior X O A) :
    frobeniusSq (storedPurification (rightHiddenWeight p))=1 ∧
    (∀ x a b,bornProbability
      (storedPurification (rightHiddenWeight p)*(storedPurification (rightHiddenWeight p)).conjTranspose)
      (groupingProjector (fun label : StoredAssignments O A => label.2 x) a)
      (groupingProjector (fun label : StoredAssignments O A => label.1) b)=p.joint x a b) ∧
    ∀ x,(∑ a,∑ b,(Matrix.trace
      (storedEveGuess (fun label : StoredAssignments O A => label.2 x) (fun label => label.1) a b*
        conditionalE (storedPurification (rightHiddenWeight p))
          (kron (groupingProjector (fun label : StoredAssignments O A => label.2 x) a)
            (groupingProjector (fun label : StoredAssignments O A => label.1) b)))).re)=1 := by
  refine ⟨storedPurification_normalized _ (rightHiddenWeight_nonnegative p)
    (rightHiddenWeight_normalized p),?_,?_⟩
  · intro x a b
    rw [storedPurification_born _ (rightHiddenWeight_nonnegative p),right_one_input_local]
  · intro x
    exact storedEve_success_one _ (rightHiddenWeight_nonnegative p) (rightHiddenWeight_normalized p) _ _

/-- Positivity, completeness and projectivity of the reversed measurements and
Eve's guessing PVM. These are mathematical properties of the matrices used in
the preceding theorem, not hypotheses supplied by its caller. -/
theorem right_one_input_measurement_validity (p : RightOneInputBehavior X O A) (x : X) :
    (∀ a,(groupingProjector (fun label : StoredAssignments O A => label.2 x) a).PosSemidef) ∧
    (∀ b,(groupingProjector (fun label : StoredAssignments O A => label.1) b).PosSemidef) ∧
    (∑ a,groupingProjector (fun label : StoredAssignments O A => label.2 x) a)=1 ∧
    (∑ b,groupingProjector (fun label : StoredAssignments O A => label.1) b)=1 ∧
    (∀ a a',a≠a' → groupingProjector (fun label : StoredAssignments O A => label.2 x) a*
      groupingProjector (fun label : StoredAssignments O A => label.2 x) a'=0) ∧
    (∀ b b',b≠b' → groupingProjector (fun label : StoredAssignments O A => label.1) b*
      groupingProjector (fun label : StoredAssignments O A => label.1) b'=0) ∧
    (∀ a b,(storedEveGuess (fun label : StoredAssignments O A => label.2 x) (fun label => label.1) a b).PosSemidef) ∧
    (∑ a,∑ b,storedEveGuess (fun label : StoredAssignments O A => label.2 x) (fun label => label.1) a b)=1 := by
  exact ⟨fun a => grouping_positive _ a,fun b => grouping_positive _ b,
    grouping_complete _,grouping_complete _,fun a a' h => grouping_orthogonal _ a a' h,
    fun b b' h => grouping_orthogonal _ b b' h,fun a b => grouping_positive _ (a,b),
    storedEve_complete _ _⟩

end CyclicBell.General
