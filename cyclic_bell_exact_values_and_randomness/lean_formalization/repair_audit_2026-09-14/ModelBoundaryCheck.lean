import CyclicBell.GeneralCorrelationValues
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General

/-- The normalized-state structure cannot be inhabited on the empty carrier. -/
example : IsEmpty (StateOn Empty) := by
  refine ⟨fun s => ?_⟩
  have h := s.normalized
  simpa [Matrix.trace] using h

/-- Model nonemptiness is supplied by an actual state and PVM witness, not a
convention for the supremum of an empty set. -/
example {d : ℕ} [NeZero d] (hd : 2 ≤ d) :
    (Qq d (Fin 2) (Ix d)).Nonempty := by
  exact ⟨_, behavior_mem_Qq (firstReducedStrategy hd (Equiv.refl (Ix d)))⟩

example {d : ℕ} [NeZero d] (hd : 2 ≤ d) :
    (Qqc d (Ix d) (AugmentedInputs d)).Nonempty := by
  exact ⟨_, Qq_subset_Qqc (behavior_mem_Qq
    (secondPermutationStrategy hd (Equiv.refl (Ix d))))⟩

end CyclicBell.General
