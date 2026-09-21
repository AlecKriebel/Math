import Bell.HilbertSimulation
import Bell.FiniteLabels
import Bell.SimulationCorollaries

/-! One composed physical source model: arbitrary finite-dimensional complex
Hilbert spaces and arbitrary finite, input-dependent outcome types. Effects are
actual source endomorphisms and probabilities are source tensor Born traces.
Cardinal encoding and the Hilbert embedding preserve the complete labeled table.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder TensorProduct InnerProductSpace
namespace Bell.HilbertFiniteLabels

universe u v
variable (E F : Type*) [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]
  [FiniteDimensional ℂ E] [FiniteDimensional ℂ F]

structure POVM (α : Type u) [Fintype α] where
  effect : α → E →ₗ[ℂ] E
  positive : ∀ a, Hilbert.PositiveOperator (effect a)
  normalized : ∑ a, effect a = 1

structure PVM (α : Type u) [Fintype α] extends POVM E α where
  idempotent : ∀ a, effect a * effect a = effect a
  orthogonal : ∀ a b, a ≠ b → effect a * effect b = 0

variable {E F}
namespace POVM
variable {α : Type u} [Fintype α]

def encode (M : POVM E α) : Hilbert.POVM E (Fintype.card α) where
  effect k := M.effect ((Fintype.equivFin α).symm k)
  positive k := M.positive ((Fintype.equivFin α).symm k)
  normalized := (Equiv.sum_comp (Fintype.equivFin α).symm M.effect).trans M.normalized

def decode (M : Hilbert.POVM E (Fintype.card α)) : POVM E α where
  effect a := M.effect (Fintype.equivFin α a)
  positive a := M.positive (Fintype.equivFin α a)
  normalized := (Equiv.sum_comp (Fintype.equivFin α) M.effect).trans M.normalized

@[simp] theorem decode_encode (M : POVM E α) : decode M.encode = M := by
  cases M
  simp only [decode, encode, Equiv.symm_apply_apply]

@[simp] theorem encode_decode (M : Hilbert.POVM E (Fintype.card α)) : (decode M).encode = M := by
  cases M
  simp only [decode, encode, Equiv.apply_symm_apply]
end POVM

namespace PVM
variable {α : Type u} [Fintype α]

def encode (M : PVM E α) : Hilbert.PVM E (Fintype.card α) where
  toPOVM := M.toPOVM.encode
  idempotent k := M.idempotent ((Fintype.equivFin α).symm k)
  orthogonal k l h := M.orthogonal _ _ (fun he => h ((Fintype.equivFin α).symm.injective he))

def decode (M : Hilbert.PVM E (Fintype.card α)) : PVM E α where
  toPOVM := POVM.decode M.toPOVM
  idempotent a := M.idempotent (Fintype.equivFin α a)
  orthogonal a b h := M.orthogonal _ _ (fun he => h ((Fintype.equivFin α).injective he))

@[simp] theorem decode_encode (M : PVM E α) : decode M.encode = M := by
  cases M
  simp only [decode, encode, POVM.decode_encode]

@[simp] theorem encode_decode (M : Hilbert.PVM E (Fintype.card α)) : (decode M).encode = M := by
  cases M
  simp only [decode, encode, POVM.encode_decode]
end PVM

variable {m n : ℕ} (AO : Fin m → Type u) (BO : Fin n → Type v)
variable [∀ x, Fintype (AO x)] [∀ y, Fintype (BO y)]

abbrev Behavior := FiniteLabels.Behavior AO BO

variable (E F)
structure Strategy where
  state : Hilbert.State E F
  alice : (x : Fin m) → POVM E (AO x)
  bob : (y : Fin n) → POVM F (BO y)

structure ProjectiveStrategy where
  state : Hilbert.State E F
  alice : (x : Fin m) → PVM E (AO x)
  bob : (y : Fin n) → PVM F (BO y)

variable {E F}
def Strategy.behavior (s : Strategy E F AO BO) : Behavior AO BO :=
  fun x y a b => Hilbert.born s.state.density ((s.alice x).effect a) ((s.bob y).effect b)

def ProjectiveStrategy.toStrategy (s : ProjectiveStrategy E F AO BO) : Strategy E F AO BO where
  state := s.state
  alice x := (s.alice x).toPOVM
  bob y := (s.bob y).toPOVM

namespace Strategy

def encode (s : Strategy E F AO BO) : Hilbert.Strategy E F (FiniteLabels.architecture AO BO) where
  state := s.state
  alice x := (s.alice x).encode
  bob y := (s.bob y).encode

def decode (s : Hilbert.Strategy E F (FiniteLabels.architecture AO BO)) : Strategy E F AO BO where
  state := s.state
  alice x := POVM.decode (s.alice x)
  bob y := POVM.decode (s.bob y)

@[simp] theorem encode_behavior (s : Strategy E F AO BO) :
    (s.encode AO BO).behavior = FiniteLabels.behaviorEquiv AO BO (s.behavior AO BO) := rfl

@[simp] theorem decode_behavior (s : Hilbert.Strategy E F (FiniteLabels.architecture AO BO)) :
    (decode AO BO s).behavior AO BO = (FiniteLabels.behaviorEquiv AO BO).symm s.behavior := rfl

@[simp] theorem decode_encode (s : Strategy E F AO BO) : decode AO BO (encode AO BO s) = s := by
  cases s
  simp only [decode, encode, POVM.decode_encode]

@[simp] theorem encode_decode (s : Hilbert.Strategy E F (FiniteLabels.architecture AO BO)) :
    encode AO BO (decode AO BO s) = s := by
  cases s
  simp only [decode, encode, POVM.encode_decode]

def toQubit (s : Strategy E F AO BO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) : FiniteLabels.Strategy AO BO :=
  FiniteLabels.Strategy.decode AO BO ((s.encode AO BO).toQubit hE hF)

@[simp] theorem toQubit_behavior (s : Strategy E F AO BO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    (s.toQubit AO BO hE hF).behavior AO BO = s.behavior AO BO := by
  rw [toQubit, FiniteLabels.Strategy.decode_behavior, Hilbert.Strategy.toQubit_behavior,
    encode_behavior, LinearEquiv.symm_apply_apply]

end Strategy

namespace ProjectiveStrategy

def encode (s : ProjectiveStrategy E F AO BO) :
    Hilbert.ProjectiveStrategy E F (FiniteLabels.architecture AO BO) where
  state := s.state
  alice x := (s.alice x).encode
  bob y := (s.bob y).encode

def decode (s : Hilbert.ProjectiveStrategy E F (FiniteLabels.architecture AO BO)) :
    ProjectiveStrategy E F AO BO where
  state := s.state
  alice x := PVM.decode (s.alice x)
  bob y := PVM.decode (s.bob y)

@[simp] theorem encode_behavior (s : ProjectiveStrategy E F AO BO) :
    (s.encode AO BO).toStrategy.behavior =
      FiniteLabels.behaviorEquiv AO BO ((s.toStrategy AO BO).behavior AO BO) := rfl

@[simp] theorem decode_behavior (s : Hilbert.ProjectiveStrategy E F (FiniteLabels.architecture AO BO)) :
    ((decode AO BO s).toStrategy AO BO).behavior AO BO =
      (FiniteLabels.behaviorEquiv AO BO).symm s.toStrategy.behavior := rfl

def toQubit (s : ProjectiveStrategy E F AO BO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    FiniteLabels.ProjectiveStrategy AO BO :=
  FiniteLabels.ProjectiveStrategy.decode AO BO ((s.encode AO BO).toQubit hE hF)

@[simp] theorem toQubit_behavior (s : ProjectiveStrategy E F AO BO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    ((s.toQubit AO BO hE hF).toStrategy AO BO).behavior AO BO =
      (s.toStrategy AO BO).behavior AO BO := by
  rw [toQubit, FiniteLabels.ProjectiveStrategy.decode_behavior,
    Hilbert.ProjectiveStrategy.toQubit_behavior, encode_behavior, LinearEquiv.symm_apply_apply]

end ProjectiveStrategy

/-- Both conventions are removed simultaneously in this exact representation. -/
theorem Strategy.behavior_mem_rawPOVM (s : Strategy E F AO BO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    s.behavior AO BO ∈ FiniteLabels.rawPOVM AO BO :=
  ⟨s.toQubit AO BO hE hF, s.toQubit_behavior AO BO hE hF⟩

theorem ProjectiveStrategy.behavior_mem_rawPVM (s : ProjectiveStrategy E F AO BO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2) :
    (s.toStrategy AO BO).behavior AO BO ∈ FiniteLabels.rawPVM AO BO :=
  ⟨s.toQubit AO BO hE hF, s.toQubit_behavior AO BO hE hF⟩

def ofQubitStrategy (s : FiniteLabels.Strategy AO BO) :
    Strategy Hilbert.QubitSpace Hilbert.QubitSpace AO BO :=
  Strategy.decode AO BO (Hilbert.ofQubitStrategy (FiniteLabels.Strategy.encode AO BO s))

theorem ofQubitStrategy_behavior (s : FiniteLabels.Strategy AO BO) :
    (ofQubitStrategy AO BO s).behavior AO BO = s.behavior AO BO := by
  rw [ofQubitStrategy, Strategy.decode_behavior, Hilbert.ofQubitStrategy_behavior,
    FiniteLabels.Strategy.encode_behavior, LinearEquiv.symm_apply_apply]

def ofQubitProjectiveStrategy (s : FiniteLabels.ProjectiveStrategy AO BO) :
    ProjectiveStrategy Hilbert.QubitSpace Hilbert.QubitSpace AO BO :=
  ProjectiveStrategy.decode AO BO
    (Hilbert.ofQubitProjectiveStrategy (FiniteLabels.ProjectiveStrategy.encode AO BO s))

theorem ofQubitProjectiveStrategy_behavior (s : FiniteLabels.ProjectiveStrategy AO BO) :
    ((ofQubitProjectiveStrategy AO BO s).toStrategy AO BO).behavior AO BO =
      (s.toStrategy AO BO).behavior AO BO := by
  rw [ofQubitProjectiveStrategy, ProjectiveStrategy.decode_behavior,
    Hilbert.ofQubitProjectiveStrategy_behavior, FiniteLabels.ProjectiveStrategy.encode_behavior,
    LinearEquiv.symm_apply_apply]

/-- The main equality acts on the same arbitrary-label Born table just embedded. -/
theorem Strategy.two_input_simulable (s : Strategy E F AO BO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2)
    (hm : m ≤ 2) (hn : n ≤ 2) :
    s.behavior AO BO ∈ FiniteLabels.convexPVM AO BO := by
  rw [← FiniteLabels.at_most_two_input_equality AO BO hm hn]
  exact subset_convexHull ℝ _ (s.behavior_mem_rawPOVM AO BO hE hF)

/-- One finite random variable chooses a complete projective strategy, retaining
all original finite outcome labels, after both model-convention bridges. -/
theorem finite_projective_simulation (s : Strategy E F AO BO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2)
    (hm : m ≤ 2) (hn : n ≤ 2) :
    ∃ (ι : Type) (_ : Fintype ι) (w : ι → ℝ)
      (t : ι → FiniteLabels.ProjectiveStrategy AO BO),
      (∀ i, 0 ≤ w i) ∧ (∑ i, w i) = 1 ∧
        (∑ i, w i • ((t i).toStrategy AO BO).behavior AO BO) = s.behavior AO BO := by
  classical
  have hp := s.two_input_simulable AO BO hE hF hm hn
  change s.behavior AO BO ∈ convexHull ℝ (FiniteLabels.rawPVM AO BO) at hp
  obtain ⟨ι,hi,w,p,hw,hn,hp,he⟩ := mem_convexHull_iff_exists_fintype.mp hp
  letI : Fintype ι := hi
  choose t ht using hp
  refine ⟨ι,hi,w,t,hw,hn,?_⟩
  simpa only [ht] using he

/-- Actual Hilbert-space projective branches with the original outcome types. -/
theorem finite_source_projective_simulation (s : Strategy E F AO BO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2)
    (hm : m ≤ 2) (hn : n ≤ 2) :
    ∃ (ι : Type) (_ : Fintype ι) (w : ι → ℝ)
      (t : ι → ProjectiveStrategy Hilbert.QubitSpace Hilbert.QubitSpace AO BO),
      (∀ i, 0 ≤ w i) ∧ (∑ i, w i) = 1 ∧
        (∑ i, w i • ((t i).toStrategy AO BO).behavior AO BO) = s.behavior AO BO := by
  obtain ⟨ι, hi, w, t, hw, hsum, he⟩ := finite_projective_simulation AO BO s hE hF hm hn
  letI : Fintype ι := hi
  refine ⟨ι, hi, w, fun i => ofQubitProjectiveStrategy AO BO (t i), hw, hsum, ?_⟩
  simpa only [ofQubitProjectiveStrategy_behavior] using he

/-- A union over the independently defined Hilbert source strategies, retaining
arbitrary finite labels. It is not a fixed-dimension-one raw-set equality. -/
def rawPOVM : Set (Behavior AO BO) :=
  {p | ∃ (E F : Hilbert.Space) (s : Strategy E F AO BO), s.behavior AO BO = p}

def rawPVM : Set (Behavior AO BO) :=
  {p | ∃ (E F : Hilbert.Space) (s : ProjectiveStrategy E F AO BO),
    (s.toStrategy AO BO).behavior AO BO = p}

def convexPOVM : Set (Behavior AO BO) := convexHull ℝ (rawPOVM AO BO)
def convexPVM : Set (Behavior AO BO) := convexHull ℝ (rawPVM AO BO)

theorem rawPOVM_eq_fixed (A : Fin m → Type u) (B : Fin n → Type v)
    [∀ x, Fintype (A x)] [∀ y, Fintype (B y)] :
    rawPOVM A B = FiniteLabels.rawPOVM A B := by
  ext p
  constructor
  · rintro ⟨E, F, s, rfl⟩
    exact s.behavior_mem_rawPOVM A B E.dimension F.dimension
  · rintro ⟨s, rfl⟩
    exact ⟨Hilbert.qubitSpace, Hilbert.qubitSpace, ofQubitStrategy A B s,
      ofQubitStrategy_behavior A B s⟩

theorem rawPVM_eq_fixed (A : Fin m → Type u) (B : Fin n → Type v)
    [∀ x, Fintype (A x)] [∀ y, Fintype (B y)] :
    rawPVM A B = FiniteLabels.rawPVM A B := by
  ext p
  constructor
  · rintro ⟨E, F, s, rfl⟩
    exact s.behavior_mem_rawPVM A B E.dimension F.dimension
  · rintro ⟨s, rfl⟩
    exact ⟨Hilbert.qubitSpace, Hilbert.qubitSpace, ofQubitProjectiveStrategy A B s,
      ofQubitProjectiveStrategy_behavior A B s⟩

theorem convexPOVM_eq_fixed : convexPOVM AO BO = FiniteLabels.convexPOVM AO BO := by
  rw [convexPOVM, rawPOVM_eq_fixed]
  rfl

theorem convexPVM_eq_fixed : convexPVM AO BO = FiniteLabels.convexPVM AO BO := by
  rw [convexPVM, rawPVM_eq_fixed]
  rfl

/-- The principal equality after composing both formerly implicit conventions. -/
theorem at_most_two_input_equality (hm : m ≤ 2) (hn : n ≤ 2) :
    convexPOVM AO BO = convexPVM AO BO := by
  rw [convexPOVM_eq_fixed, convexPVM_eq_fixed]
  exact FiniteLabels.at_most_two_input_equality AO BO hm hn

theorem no_strategy_of_empty_alice (x : Fin m) [IsEmpty (AO x)] :
    IsEmpty (Strategy E F AO BO) := by
  refine ⟨fun s => ?_⟩
  have h := ((s.encode AO BO).aliceSelected x).isLt
  simpa [FiniteLabels.architecture] using h

theorem no_strategy_of_empty_bob (y : Fin n) [IsEmpty (BO y)] :
    IsEmpty (Strategy E F AO BO) := by
  refine ⟨fun s => ?_⟩
  have h := ((s.encode AO BO).bobSelected y).isLt
  simpa [FiniteLabels.architecture] using h

end Bell.HilbertFiniteLabels
