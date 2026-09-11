import Bell.BinaryParty
import Bell.ResidualStrategy
import Bell.ProjectiveBound

/-!
# Main theorem: arbitrary finite two-input architectures

The proof is over the actual complex-qubit strategy images and their ordinary
shared-randomness convex hulls. It does not assume universal equality, a
residual reduction theorem, multiplier positivity, or a rank-case oracle.
Each of those dependencies is supplied by an imported proof.

This is an uncompiled source completion attempt. Kernel validation and the
axiom audit are intentionally deferred to the user's later run.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder
namespace Bell

/-- A two-input party with at most three active outcomes has the residual
ordering unless both of its inputs are binary. -/
theorem two_three_ordering {n : Fin 2 → ℕ}
    (h : (∀ x, n x=2 ∨ n x=3) ∧ ∃ x, n x=2)
    (hn : ¬ ∀ x, n x=2) : ∃ d, n d=2 ∧ n (otherInput d)=3 := by
  obtain ⟨d,hd⟩ := h.2
  refine ⟨d,hd,?_⟩
  rcases h.1 (otherInput d) with ho|ho
  · exfalso
    apply hn
    intro x
    fin_cases d <;> fin_cases x <;> simp [otherInput] at hd ho ⊢ <;> assumption
  · exact ho

/-- No strict separator can attain its POVM maximum in a two-input architecture.
All support degeneracies are settled before invoking residual geometry. -/
theorem no_two_input_extreme_separator
    (AO BO : Fin 2 → ℕ) (s : Strategy ⟨2,2,AO,BO⟩)
    (f : Behavior ⟨2,2,AO,BO⟩ →ₗ[ℝ] ℝ)
    (hex : s.behavior ∈ Set.extremePoints ℝ (convexPOVM ⟨2,2,AO,BO⟩))
    (hmax : ∀ q ∈ convexPOVM ⟨2,2,AO,BO⟩, f q ≤ f s.behavior)
    (hstrict : ∀ q ∈ convexPVM ⟨2,2,AO,BO⟩, f q < f s.behavior) : False := by
  have hnot : s.behavior ∉ convexPVM ⟨2,2,AO,BO⟩ := by
    intro hp
    exact (lt_irrefl _ (hstrict _ hp))
  obtain ⟨t,ht⟩ := full_pure_of_not_mem_convexPVM s hnot
  have htex : t.behavior ∈ Set.extremePoints ℝ (convexPOVM ⟨2,2,AO,BO⟩) := by rwa [ht]
  have htmax : ∀ q ∈ convexPOVM ⟨2,2,AO,BO⟩, f q ≤ f t.behavior := by rwa [ht]
  have htstrict : ∀ q ∈ convexPVM ⟨2,2,AO,BO⟩, f q < f t.behavior := by rwa [ht]
  have htloc : t.behavior ∈ convexPVM ⟨2,2,AO,BO⟩ → False := by
    intro hp
    exact lt_irrefl _ (htstrict _ hp)
  have hndA : ∀ x, ¬ DeterministicMeasurement (t.alice x) := by
    intro x hx
    exact htloc (deterministic_alice_local AO BO t.toStrategy x hx)
  have hndB : ∀ y, ¬ DeterministicMeasurement (t.bob y) := by
    intro y hy
    exact htloc (deterministic_bob_local AO BO t.toStrategy y hy)
  have hA := extreme_two_or_three_outcomes AO BO t htex hndA
  have hsex : t.swap.behavior ∈ Set.extremePoints ℝ (convexPOVM ⟨2,2,BO,AO⟩) := by
    rw [t.swap_behavior]
    exact swap_extreme htex
  have hB := extreme_two_or_three_outcomes BO AO t.swap hsex hndB
  by_cases hb : ∀ y, Fintype.card (EffectSupport (t.bob y))=2
  · exact htloc (extreme_binary_bob_simulation AO BO t htex hndB hb)
  by_cases ha : ∀ x, Fintype.card (EffectSupport (t.alice x))=2
  · have hp := extreme_binary_bob_simulation BO AO t.swap hsex hndA ha
    have hs := swap_mem_convexPVM hp
    rw [t.swap_behavior] at hs
    exact htloc hs
  obtain ⟨dA,hA2,hA3⟩ := two_three_ordering hA ha
  obtain ⟨dB,hB2,hB3⟩ := two_three_ordering hB hb
  exact no_strict_extreme_binary_ternary AO BO t htex hndA hndB dA dB
    hA2 hA3 hB2 hB3 f htmax htstrict

/-- The full arbitrary-output equality, with no unproved theorem premise. -/
theorem two_input_convex_equality (AO BO : Fin 2 → ℕ) :
    convexPOVM ⟨2,2,AO,BO⟩ = convexPVM ⟨2,2,AO,BO⟩ := by
  apply Set.Subset.antisymm
  · intro p hp
    by_contra hnot
    obtain ⟨s,f,hex,hmax,hstrict⟩ := counterexample_has_extreme_maximum
      ⟨2,2,AO,BO⟩ p hp hnot
    exact no_two_input_extreme_separator AO BO s f hex hmax hstrict
  · exact convexPVM_subset_convexPOVM _

/-- The precise target proposition from `Targets`, now supplied unconditionally
by the source chain rather than taken as an argument to an assembly theorem. -/
theorem universal_two_input_equality : UniversalTwoInputEquality := by
  intro A ha hb
  rcases A with ⟨na,nb,AO,BO⟩
  change na=2 at ha
  change nb=2 at hb
  subst na
  subst nb
  exact two_input_convex_equality AO BO

/-- Equality also covers all architectures with at most two inputs per party,
including empty input sets and empty outcome alphabets whenever realizable. -/
theorem at_most_two_input_equality (A : Architecture)
    (ha : A.aliceInputs ≤ 2) (hb : A.bobInputs ≤ 2) :
    convexPOVM A = convexPVM A := by
  by_cases ha1 : A.aliceInputs ≤ 1
  · exact one_input_equality A (Or.inl ha1)
  by_cases hb1 : A.bobInputs ≤ 1
  · exact one_input_equality A (Or.inr hb1)
  exact universal_two_input_equality A (by omega) (by omega)

/-- The four principal claims stated at the start of the project. -/
theorem main_claims : MainClaims :=
  ⟨universal_two_input_equality,one_input_equality,projective_global_upper_bound,
    three_by_two_separation⟩

/-- The minimum input architecture, up to exchanging the two parties. -/
theorem minimum_inputs (A : Architecture) (hs : StrictSeparation A) :
    (3 ≤ A.aliceInputs ∧ 2 ≤ A.bobInputs) ∨
    (2 ≤ A.aliceInputs ∧ 3 ≤ A.bobInputs) :=
  minimum_inputs_of_equality_theorems one_input_equality universal_two_input_equality A hs

/-- The lower input threshold is attained by the paper's explicit separator. -/
theorem minimum_inputs_attained :
    StrictSeparation separatorArchitecture ∧
      separatorArchitecture.aliceInputs=3 ∧ separatorArchitecture.bobInputs=2 :=
  ⟨three_by_two_separation,rfl,rfl⟩

/-- An arbitrary two-input linear Bell test cannot separate the convexified
fixed-qubit models, independently of the sizes of its declared output alphabets. -/
theorem no_two_input_strict_separation (A : Architecture)
    (ha : A.aliceInputs ≤ 2) (hb : A.bobInputs ≤ 2) : ¬ StrictSeparation A :=
  no_strict_separation_of_equal_hulls A (at_most_two_input_equality A ha hb)

end Bell
