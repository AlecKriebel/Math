import CyclicBell.PhysicalBounds
import CyclicBell.Guessing

/-!
# Public d=4 endpoints

All conclusions start with the original mixed-state/PVM physical model. The
universal bounds are imported independently from the concrete witness.
`IsFirstMaximizer` and `IsSecondMaximizer` compare with ALL finite-dimensional
strategies; their proofs, not their definitions, establish witness maximality.

Nothing here asserts the whole manuscript, all-dimensional d, qa/qc equality,
support-rigidity, uniqueness, or optimal guessing over all realizations.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell

/-- Actual comparison against all allowed finite-dimensional competitors. -/
def IsFirstMaximizer {nA nB : ℕ} (σ : Strategy 2 nA nB) : Prop :=
  ∀ (mA mB : ℕ) (τ : Strategy 2 mA mB),
    firstAugmentedValue τ ≤ firstAugmentedValue σ

def IsSecondMaximizer {nA nB : ℕ} (σ : Strategy 4 nA nB) : Prop :=
  ∀ (mA mB : ℕ) (τ : Strategy 4 mA mB),
    secondAugmentedValue τ ≤ secondAugmentedValue σ

namespace D4

theorem first_is_maximizer : IsFirstMaximizer firstStrategy := by
  intro mA mB τ
  rw [first_attainment]
  exact first_universal_upper τ

theorem second_is_maximizer : IsSecondMaximizer secondStrategy := by
  intro mA mB τ
  rw [second_attainment]
  exact second_universal_upper τ

/-- The designated distribution is calculated from state and projectors. -/
theorem first_behavior_table (a b : Fin 4) :
    behavior firstStrategy 1 4 a b = table a b := mixed_targetBorn_eq_table a b

theorem second_behavior_table (a b : Fin 4) :
    behavior secondStrategy 1 4 a b = table a b := mixed_targetBorn_eq_table a b

theorem first_target_eq : targetDistribution firstStrategy 1 = targetBorn := by
  funext a b
  rw [targetDistribution, first_behavior_table, targetBorn_eq_table]

theorem second_target_eq : targetDistribution secondStrategy 1 = targetBorn := by
  funext a b
  rw [targetDistribution, second_behavior_table, targetBorn_eq_table]

/-- Outcome-specific parity statements are exposed, not hidden in a definition. -/
theorem first_even_probability (a b : Fin 4) (hab : (a.val + b.val) % 2 = 0) :
    behavior firstStrategy 1 4 a b = 1 / 32 := by
  rw [first_behavior_table]
  simp [table, hab]

theorem first_odd_probability (a b : Fin 4) (hab : (a.val + b.val) % 2 = 1) :
    behavior firstStrategy 1 4 a b = 3 / 32 := by
  rw [first_behavior_table]
  simp [table, hab]

theorem second_even_probability (a b : Fin 4) (hab : (a.val + b.val) % 2 = 0) :
    behavior secondStrategy 1 4 a b = 1 / 32 := by
  rw [second_behavior_table]
  simp [table, hab]

theorem second_odd_probability (a b : Fin 4) (hab : (a.val + b.val) % 2 = 1) :
    behavior secondStrategy 1 4 a b = 3 / 32 := by
  rw [second_behavior_table]
  simp [table, hab]

/-- Literal maximum of the sixteen entries, expressed as an upper bound and
an attained entry, without requiring a separate finite-max API. -/
theorem first_target_maximum :
    (∀ a b : Fin 4, behavior firstStrategy 1 4 a b ≤ 3 / 32) ∧
    behavior firstStrategy 1 4 0 1 = 3 / 32 ∧ (1 : ℝ) / 16 < 3 / 32 := by
  have hp : ∀ a b, behavior firstStrategy 1 4 a b = targetBorn a b := by
    intro a b
    rw [first_behavior_table, targetBorn_eq_table]
  simp only [hp]
  exact ⟨target_le_three_thirtyseconds, target_01, by norm_num⟩

theorem second_target_maximum :
    (∀ a b : Fin 4, behavior secondStrategy 1 4 a b ≤ 3 / 32) ∧
    behavior secondStrategy 1 4 0 1 = 3 / 32 ∧ (1 : ℝ) / 16 < 3 / 32 := by
  have hp : ∀ a b, behavior secondStrategy 1 4 a b = targetBorn a b := by
    intro a b
    rw [second_behavior_table, targetBorn_eq_table]
  simp only [hp]
  exact ⟨target_le_three_thirtyseconds, target_01, by norm_num⟩

theorem first_target_normalization_and_marginals :
    (∀ a b, 0 ≤ behavior firstStrategy 1 4 a b) ∧
    (∑ a : Fin 4, ∑ b : Fin 4, behavior firstStrategy 1 4 a b) = 1 ∧
    (∀ a, (∑ b : Fin 4, behavior firstStrategy 1 4 a b) = 1 / 4) ∧
    (∀ b, (∑ a : Fin 4, behavior firstStrategy 1 4 a b) = 1 / 4) := by
  have hp : ∀ a b, behavior firstStrategy 1 4 a b = targetBorn a b := by
    intro a b; rw [first_behavior_table, targetBorn_eq_table]
  simp only [hp]
  exact ⟨target_nonnegative, target_normalized, alice_marginal, bob_marginal⟩

theorem second_target_normalization_and_marginals :
    (∀ a b, 0 ≤ behavior secondStrategy 1 4 a b) ∧
    (∑ a : Fin 4, ∑ b : Fin 4, behavior secondStrategy 1 4 a b) = 1 ∧
    (∀ a, (∑ b : Fin 4, behavior secondStrategy 1 4 a b) = 1 / 4) ∧
    (∀ b, (∑ a : Fin 4, behavior secondStrategy 1 4 a b) = 1 / 4) := by
  have hp : ∀ a b, behavior secondStrategy 1 4 a b = targetBorn a b := by
    intro a b; rw [second_behavior_table, targetBorn_eq_table]
  simp only [hp]
  exact ⟨target_nonnegative, target_normalized, alice_marginal, bob_marginal⟩

theorem first_nonuniform : ¬ ∀ a b : Fin 4, behavior firstStrategy 1 4 a b = 1 / 16 := by
  intro hu
  have h01 := hu 0 1
  rw [first_behavior_table] at h01
  norm_num [table] at h01

theorem second_nonuniform : ¬ ∀ a b : Fin 4, behavior secondStrategy 1 4 a b = 1 / 16 := by
  intro hu
  have h01 := hu 0 1
  rw [second_behavior_table] at h01
  norm_num [table] at h01

/-- The exhibited Eve is the fixed (0,1) guessing POVM on C^1. -/
theorem first_trivialEve_gap :
    trivialEveSuccess (targetDistribution firstStrategy 1) (0,1) = 3 / 32 ∧
    (1 : ℝ) / 16 < trivialEveSuccess (targetDistribution firstStrategy 1) (0,1) := by
  rw [trivialEve_success_eq, first_target_eq, target_01]
  constructor <;> norm_num

theorem second_trivialEve_gap :
    trivialEveSuccess (targetDistribution secondStrategy 1) (0,1) = 3 / 32 ∧
    (1 : ℝ) / 16 < trivialEveSuccess (targetDistribution secondStrategy 1) (0,1) := by
  rw [trivialEve_success_eq, second_target_eq, target_01]
  constructor <;> norm_num

/-- The trivial Eve instrument and conditional states are positive and normalized. -/
theorem witness_trivialEve_validity :
    (∀ a b, (trivialEveEffect (0,1) a b).PosSemidef) ∧
    (∑ a : Fin 4, ∑ b : Fin 4, trivialEveEffect (0,1) a b) = 1 ∧
    (∀ a b, (trivialConditional targetBorn a b).PosSemidef) ∧
    (∑ a : Fin 4, ∑ b : Fin 4, trivialConditional targetBorn a b) = 1 := by
  exact ⟨trivialEve_positive (0,1), trivialEve_complete (0,1),
    trivialConditional_positive targetBorn target_nonnegative,
    trivialConditional_total targetBorn target_normalized⟩

/-- The Eve conditional states come from sandwiching the actual physical
state and tracing AB after adjoining C^1, not from stipulating a probability. -/
theorem first_physical_Eve_bridge (a b : Fin 4) :
    actualTrivialConditional firstStrategy.state.density
      (tensor ((firstStrategy.alice 1).effect a) ((firstStrategy.bob 4).effect b)) =
      trivialConditional (targetDistribution firstStrategy 1) a b :=
  pvm_trivialEve_Born_bridge firstStrategy.state (firstStrategy.alice 1) (firstStrategy.bob 4) a b

theorem second_physical_Eve_bridge (a b : Fin 4) :
    actualTrivialConditional secondStrategy.state.density
      (tensor ((secondStrategy.alice 1).effect a) ((secondStrategy.bob 4).effect b)) =
      trivialConditional (targetDistribution secondStrategy 1) a b :=
  pvm_trivialEve_Born_bridge secondStrategy.state (secondStrategy.alice 1) (secondStrategy.bob 4) a b

theorem adjoined_witness_states_valid :
    (adjoinTrivialEve firstStrategy.state.density).PosSemidef ∧
    Matrix.trace (adjoinTrivialEve firstStrategy.state.density) = 1 ∧
    (adjoinTrivialEve secondStrategy.state.density).PosSemidef ∧
    Matrix.trace (adjoinTrivialEve secondStrategy.state.density) = 1 := by
  exact ⟨adjoinTrivialEve_positive firstStrategy.state.positive,
    (adjoinTrivialEve_trace _).trans firstStrategy.state.normalized,
    adjoinTrivialEve_positive secondStrategy.state.positive,
    (adjoinTrivialEve_trace _).trans secondStrategy.state.normalized⟩

/-- The displayed AB state is already pure, so C^1 really is a purification. -/
theorem trivialEve_purification :
    adjoinTrivialEve firstStrategy.state.density =
      projector (fun i : Joint 4 4 × Fin 1 => phi i.1) ∧
    ip (fun i : Joint 4 4 × Fin 1 => phi i.1)
      (fun i : Joint 4 4 × Fin 1 => phi i.1) = 1 := by
  constructor
  · exact adjoinTrivialEve_projector phi
  · simpa [ip, Fintype.sum_prod_type, Fin.sum_univ_succ] using phi_normalized

/-- First-family A+B+C+D+E endpoint. Physical PVM validity is carried by the
explicit Strategy value; source bridges and full validity are separate audited
statements. Competitors here range over ALL finite local dimensions. -/
theorem first_counterexample :
    (∀ nA nB : ℕ, ∀ σ : Strategy 2 nA nB,
      firstAugmentedValue σ ≤ 2 / Real.sin (Real.pi / 8) + 1) ∧
    firstAugmentedValue firstStrategy = 2 / Real.sin (Real.pi / 8) + 1 ∧
    IsFirstMaximizer firstStrategy ∧
    (∀ a b, behavior firstStrategy 1 4 a b =
      if (a.val + b.val) % 2 = 0 then 1 / 32 else 3 / 32) ∧
    (∑ a : Fin 4, ∑ b : Fin 4, behavior firstStrategy 1 4 a b) = 1 ∧
    (∀ a, (∑ b : Fin 4, behavior firstStrategy 1 4 a b) = 1 / 4) ∧
    (∀ b, (∑ a : Fin 4, behavior firstStrategy 1 4 a b) = 1 / 4) ∧
    (∀ a b, behavior firstStrategy 1 4 a b ≤ 3 / 32) ∧
    trivialEveSuccess (targetDistribution firstStrategy 1) (0,1) = 3 / 32 ∧
    (1 : ℝ) / 16 < trivialEveSuccess (targetDistribution firstStrategy 1) (0,1) ∧
    ¬ (∀ a b, behavior firstStrategy 1 4 a b = 1 / 16) := by
  exact ⟨fun _ _ σ => first_universal_upper σ, first_attainment, first_is_maximizer,
    first_behavior_table, first_target_normalization_and_marginals.2.1,
    first_target_normalization_and_marginals.2.2.1,
    first_target_normalization_and_marginals.2.2.2, first_target_maximum.1,
    first_trivialEve_gap.1, first_trivialEve_gap.2, first_nonuniform⟩

/-- Complete second-family F endpoint, without claiming to replace family I. -/
theorem second_counterexample :
    (∀ nA nB : ℕ, ∀ σ : Strategy 4 nA nB, secondAugmentedValue σ ≤ 5) ∧
    secondAugmentedValue secondStrategy = 5 ∧ IsSecondMaximizer secondStrategy ∧
    (∀ a b, behavior secondStrategy 1 4 a b =
      if (a.val + b.val) % 2 = 0 then 1 / 32 else 3 / 32) ∧
    (∑ a : Fin 4, ∑ b : Fin 4, behavior secondStrategy 1 4 a b) = 1 ∧
    (∀ a, (∑ b : Fin 4, behavior secondStrategy 1 4 a b) = 1 / 4) ∧
    (∀ b, (∑ a : Fin 4, behavior secondStrategy 1 4 a b) = 1 / 4) ∧
    (∀ a b, behavior secondStrategy 1 4 a b ≤ 3 / 32) ∧
    trivialEveSuccess (targetDistribution secondStrategy 1) (0,1) = 3 / 32 ∧
    (1 : ℝ) / 16 < trivialEveSuccess (targetDistribution secondStrategy 1) (0,1) ∧
    ¬ (∀ a b, behavior secondStrategy 1 4 a b = 1 / 16) := by
  exact ⟨fun _ _ σ => second_universal_upper σ, second_attainment, second_is_maximizer,
    second_behavior_table, second_target_normalization_and_marginals.2.1,
    second_target_normalization_and_marginals.2.2.1,
    second_target_normalization_and_marginals.2.2.2, second_target_maximum.1,
    second_trivialEve_gap.1, second_trivialEve_gap.2, second_nonuniform⟩

/-- Existential formulation: maximality is a proved conclusion of the witness. -/
theorem exists_first_nonuniform_maximizer :
    ∃ σ : Strategy 2 4 4, IsFirstMaximizer σ ∧
      ¬ (∀ a b, behavior σ 1 4 a b = 1 / 16) :=
  ⟨firstStrategy, first_is_maximizer, first_nonuniform⟩

theorem exists_second_nonuniform_maximizer :
    ∃ σ : Strategy 4 4 4, IsSecondMaximizer σ ∧
      ¬ (∀ a b, behavior σ 1 4 a b = 1 / 16) :=
  ⟨secondStrategy, second_is_maximizer, second_nonuniform⟩

/-- Negation of the first scalar-value implication, in the displayed normalization. -/
theorem first_scalar_value_does_not_force_uniform :
    ¬ (∀ nA nB : ℕ, ∀ σ : Strategy 2 nA nB,
      firstAugmentedValue σ = firstTargetValue →
        ∀ a b, behavior σ 1 4 a b = 1 / 16) := by
  intro hclaim
  exact first_nonuniform (hclaim 4 4 firstStrategy first_attainment)

theorem second_scalar_value_does_not_force_uniform :
    ¬ (∀ nA nB : ℕ, ∀ σ : Strategy 4 nA nB,
      secondAugmentedValue σ = 5 → ∀ a b, behavior σ 1 4 a b = 1 / 16) := by
  intro hclaim
  exact second_nonuniform (hclaim 4 4 secondStrategy second_attainment)

/-- Both explicit witnesses, with all finite-dimensional competitors quantified. -/
theorem main_d4_counterexamples :
    (∃ σ : Strategy 2 4 4,
      firstAugmentedValue σ = firstTargetValue ∧ IsFirstMaximizer σ ∧
      (∀ a b, behavior σ 1 4 a b = table a b) ∧
      trivialEveSuccess (targetDistribution σ 1) (0,1) = 3 / 32 ∧
      ¬ (∀ a b, behavior σ 1 4 a b = 1 / 16)) ∧
    (∃ σ : Strategy 4 4 4,
      secondAugmentedValue σ = 5 ∧ IsSecondMaximizer σ ∧
      (∀ a b, behavior σ 1 4 a b = table a b) ∧
      trivialEveSuccess (targetDistribution σ 1) (0,1) = 3 / 32 ∧
      ¬ (∀ a b, behavior σ 1 4 a b = 1 / 16)) := by
  exact ⟨⟨firstStrategy, first_attainment, first_is_maximizer, first_behavior_table,
    first_trivialEve_gap.1, first_nonuniform⟩,
    ⟨secondStrategy, second_attainment, second_is_maximizer, second_behavior_table,
    second_trivialEve_gap.1, second_nonuniform⟩⟩

end D4
end CyclicBell
