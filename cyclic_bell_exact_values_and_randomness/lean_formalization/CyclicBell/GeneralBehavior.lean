import CyclicBell.GeneralFirstBound
import CyclicBell.GeneralSecondBound
import Mathlib.Topology.Order.Basic
import Mathlib.Order.ConditionallyCompleteLattice.Basic

/-! Real behavior arrays and the manuscript Bell functionals. Continuity uses
the ordinary product topology and does not assume a quantum model is closed.
The reduced and augmented Bob input alphabets remain separate. -/
noncomputable section
open scoped BigOperators ComplexOrder Topology
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

abbrev BellBehavior (d : ℕ) (α β : Type*) := α → β → Ix d → Ix d → ℝ

/-- Positive-character encoding: the phase is a+b, with no Bob adjoint. -/
def probabilityCorrelator {α β : Type*} (p : BellBehavior d α β) (x : α) (y : β) : ℂ :=
  ∑ a : Ix d, ∑ b : Ix d, chi (a+b) * (p x y a b : ℂ)

def pullBehavior {α β α' β' : Type*} (f : α' → α) (g : β' → β)
    (p : BellBehavior d α β) : BellBehavior d α' β' :=
  fun x y a b => p (f x) (g y) a b

def firstReducedBell (p : BellBehavior d (Fin 2) (Ix d)) : ℝ :=
  ∑ y : Ix d, (probabilityCorrelator p 0 y + chi y * probabilityCorrelator p 1 y).re

def firstAugmentedBell (p : BellBehavior d (Fin 2) (AugmentedInputs d)) : ℝ :=
  firstReducedBell (pullBehavior id some p) + (probabilityCorrelator p 0 none).re

def secondReducedBell (p : BellBehavior d (Ix d) (Ix d)) : ℝ :=
  ∑ l : Ix d, (star (generalLambda l) *
    ∑ y : Ix d, chi (l*y) * probabilityCorrelator p l y).re

def secondAugmentedBell (p : BellBehavior d (Ix d) (AugmentedInputs d)) : ℝ :=
  secondReducedBell (pullBehavior id some p) + (probabilityCorrelator p 0 none).re

theorem probabilityCorrelator_pull {α β α' β' : Type*} (p : BellBehavior d α β)
    (f : α' → α) (g : β' → β) (x : α') (y : β') :
    probabilityCorrelator (pullBehavior f g p) x y = probabilityCorrelator p (f x) (g y) := rfl

theorem probabilityCorrelator_continuous {α β : Type*} (x : α) (y : β) :
    Continuous (fun p : BellBehavior d α β => probabilityCorrelator p x y) := by
  unfold probabilityCorrelator
  fun_prop

theorem pullBehavior_continuous {α β α' β' : Type*} (f : α' → α) (g : β' → β) :
    Continuous (pullBehavior (d := d) f g) := by
  unfold pullBehavior
  fun_prop

theorem firstReducedBell_continuous : Continuous (firstReducedBell (d := d)) := by
  unfold firstReducedBell probabilityCorrelator
  fun_prop

theorem firstAugmentedBell_continuous : Continuous (firstAugmentedBell (d := d)) := by
  unfold firstAugmentedBell
  exact (firstReducedBell_continuous.comp (pullBehavior_continuous id some)).add
    (Complex.continuous_re.comp (probabilityCorrelator_continuous 0 none))

theorem secondReducedBell_continuous : Continuous (secondReducedBell (d := d)) := by
  unfold secondReducedBell probabilityCorrelator
  fun_prop

theorem secondAugmentedBell_continuous : Continuous (secondAugmentedBell (d := d)) := by
  unfold secondAugmentedBell
  exact (secondReducedBell_continuous.comp (pullBehavior_continuous id some)).add
    (Complex.continuous_re.comp (probabilityCorrelator_continuous 0 none))

variable {ι κ : Type*} [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ]

/-- Input pullback changes neither the density nor any effect matrix. -/
def pullStrategy {α β α' β' : Type*} (s : StrategyOn d α β ι κ)
    (f : α' → α) (g : β' → β) : StrategyOn d α' β' ι κ where
  state := s.state
  alice := fun x => s.alice (f x)
  bob := fun y => s.bob (g y)

theorem behavior_pullStrategy {α β α' β' : Type*} (s : StrategyOn d α β ι κ)
    (f : α' → α) (g : β' → β) :
    behavior (pullStrategy s f g) = pullBehavior f g (behavior s) := rfl

theorem probabilityCorrelator_behavior {α β : Type*} (s : StrategyOn d α β ι κ)
    (x : α) (y : β) :
    probabilityCorrelator (behavior s) x y =
      Matrix.trace (s.state.density * kron (encoded (s.alice x)) (encoded (s.bob y))) := by
  exact (correlator_from_probabilities s.state (s.alice x) (s.bob y)).symm

theorem firstAugmentedBell_behavior (s : StrategyOn d (Fin 2) (AugmentedInputs d) ι κ) :
    firstAugmentedBell (behavior s) = firstValue s := by
  unfold firstAugmentedBell firstReducedBell firstValue
  simp only [probabilityCorrelator_pull, id_eq, probabilityCorrelator_behavior,
    kron_add_left, kron_smul_left, mul_add, mul_smul_comm, Matrix.trace_add,
    Matrix.trace_smul, smul_eq_mul, Complex.add_re, stateEval]

theorem secondAugmentedBell_behavior (s : StrategyOn d (Ix d) (AugmentedInputs d) ι κ) :
    secondAugmentedBell (behavior s) = secondValue s := by
  unfold secondAugmentedBell secondReducedBell secondValue
  simp only [probabilityCorrelator_pull, id_eq, probabilityCorrelator_behavior,
    secondFourier, moduleFourier, kron_sum_right, kron_smul_right,
    Finset.mul_sum, Matrix.trace_sum, Matrix.trace_smul, mul_smul_comm,
    smul_eq_mul, stateEval]

/-- Extending a closed scalar inequality to a closure is a topological theorem,
not an identification of Q_qa with Q_q or Q_qc. -/
theorem continuous_bound_on_closure {X : Type*} [TopologicalSpace X]
    (S : Set X) (f : X → ℝ) (hf : Continuous f) (M : ℝ)
    (hM : ∀ x ∈ S, f x ≤ M) : ∀ x ∈ closure S, f x ≤ M := by
  exact closure_minimal hM (isClosed_le hf continuous_const)

/-- sSup over reals is used only after both nonemptiness and boundedness are
exhibited. It is not assigned the witness value by definition. -/
def bellSupremum {X : Type*} (S : Set X) (f : X → ℝ) : ℝ := sSup (f '' S)

theorem bellSupremum_of_attained_bound {X : Type*} (S : Set X) (f : X → ℝ)
    (M : ℝ) (hM : ∀ x ∈ S, f x ≤ M) (w : X) (hw : w ∈ S) (hfw : f w = M) :
    bellSupremum S f = M := by
  have hne : (f '' S).Nonempty := ⟨f w, w, hw, rfl⟩
  have hb : BddAbove (f '' S) := ⟨M, by rintro v ⟨x,hx,rfl⟩; exact hM x hx⟩
  apply le_antisymm
  · exact csSup_le hne (by rintro v ⟨x,hx,rfl⟩; exact hM x hx)
  · rw [← hfw]
    exact le_csSup hb ⟨w,hw,rfl⟩

/-- Abstract assembly used only with the actual physical sets below. The upper
bound applies to every commuting behavior; closure gets its bound by continuity. -/
theorem three_model_suprema {X : Type*} [TopologicalSpace X] (q qc : Set X)
    (f : X → ℝ) (hf : Continuous f) (M : ℝ) (hq : q ⊆ qc)
    (hc : ∀ p ∈ qc, f p ≤ M) (w : X) (hw : w ∈ q) (hfw : f w = M) :
    bellSupremum q f = M ∧ bellSupremum (closure q) f = M ∧ bellSupremum qc f = M := by
  have hqbound : ∀ p ∈ q, f p ≤ M := fun p hp => hc p (hq hp)
  exact ⟨bellSupremum_of_attained_bound q f M hqbound w hw hfw,
    bellSupremum_of_attained_bound (closure q) f M
      (continuous_bound_on_closure q f hf M hqbound) w (subset_closure hw) hfw,
    bellSupremum_of_attained_bound qc f M hc w (hq hw) hfw⟩

end CyclicBell.General
