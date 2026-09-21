import Bell.Assembly

/-!
# Independent finite-label physical model and exact cardinal encoding

The source measurements below are matrix-valued families on arbitrary finite
types, not abbreviations for Fin-indexed measurements. Encoding transports
every effect, state, and complete Born table, and commutes with ordinary convex
hulls. No nonempty-output premise is imposed.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace Bell.FiniteLabels

universe u v

structure POVM (α : Type u) [Fintype α] where
  effect : α → Operator
  positive : ∀ a, (effect a).PosSemidef
  normalized : ∑ a, effect a = 1

structure PVM (α : Type u) [Fintype α] extends POVM α where
  idempotent : ∀ a, effect a * effect a = effect a
  orthogonal : ∀ a b, a ≠ b → effect a * effect b = 0

namespace POVM
variable {α : Type u} [Fintype α]

def encode (M : POVM α) : Bell.POVM (Fintype.card α) where
  effect k := M.effect ((Fintype.equivFin α).symm k)
  positive k := M.positive ((Fintype.equivFin α).symm k)
  normalized := (Equiv.sum_comp (Fintype.equivFin α).symm M.effect).trans M.normalized

def decode (M : Bell.POVM (Fintype.card α)) : POVM α where
  effect a := M.effect (Fintype.equivFin α a)
  positive a := M.positive (Fintype.equivFin α a)
  normalized := (Equiv.sum_comp (Fintype.equivFin α) M.effect).trans M.normalized

@[simp] theorem decode_encode (M : POVM α) : decode M.encode = M := by
  cases M
  simp only [decode, encode, Equiv.symm_apply_apply]

@[simp] theorem encode_decode (M : Bell.POVM (Fintype.card α)) : (decode M).encode = M := by
  cases M
  simp only [decode, encode, Equiv.apply_symm_apply]

def encoding : POVM α ≃ Bell.POVM (Fintype.card α) where
  toFun := encode
  invFun := decode
  left_inv := decode_encode
  right_inv := encode_decode

theorem nonempty_outcomes (M : POVM α) : Nonempty α := by
  classical
  by_contra h
  letI : IsEmpty α := not_nonempty_iff.mp h
  have hz : (0 : Operator) = 1 := by simpa using M.normalized
  have hc := congrArg (fun Q : Operator => Q 0 0) hz
  norm_num at hc

theorem no_empty_measurement [IsEmpty α] : IsEmpty (POVM α) :=
  ⟨fun M => isEmptyElim (Classical.choice M.nonempty_outcomes)⟩
end POVM

namespace PVM
variable {α : Type u} [Fintype α]

def encode (M : PVM α) : Bell.PVM (Fintype.card α) where
  toPOVM := M.toPOVM.encode
  idempotent k := M.idempotent ((Fintype.equivFin α).symm k)
  orthogonal k l h := M.orthogonal ((Fintype.equivFin α).symm k)
    ((Fintype.equivFin α).symm l) (fun he => h ((Fintype.equivFin α).symm.injective he))

def decode (M : Bell.PVM (Fintype.card α)) : PVM α where
  toPOVM := POVM.decode M.toPOVM
  idempotent a := M.idempotent (Fintype.equivFin α a)
  orthogonal a b h := M.orthogonal (Fintype.equivFin α a)
    (Fintype.equivFin α b) (fun he => h ((Fintype.equivFin α).injective he))

@[simp] theorem decode_encode (M : PVM α) : decode M.encode = M := by
  cases M
  simp only [decode, encode, POVM.decode_encode]

@[simp] theorem encode_decode (M : Bell.PVM (Fintype.card α)) : (decode M).encode = M := by
  cases M
  simp only [decode, encode, POVM.encode_decode]

def encoding : PVM α ≃ Bell.PVM (Fintype.card α) where
  toFun := encode
  invFun := decode
  left_inv := decode_encode
  right_inv := encode_decode
end PVM

variable {m n : ℕ} (AO : Fin m → Type u) (BO : Fin n → Type v)
variable [∀ x, Fintype (AO x)] [∀ y, Fintype (BO y)]

def architecture : Bell.Architecture :=
  ⟨m, n, fun x => Fintype.card (AO x), fun y => Fintype.card (BO y)⟩

abbrev Behavior := (x : Fin m) → (y : Fin n) → AO x → BO y → ℝ

structure Strategy where
  state : State
  alice : (x : Fin m) → POVM (AO x)
  bob : (y : Fin n) → POVM (BO y)

structure ProjectiveStrategy where
  state : State
  alice : (x : Fin m) → PVM (AO x)
  bob : (y : Fin n) → PVM (BO y)

def Strategy.behavior (s : Strategy AO BO) : Behavior AO BO :=
  fun x y a b => born s.state.density ((s.alice x).effect a) ((s.bob y).effect b)

def ProjectiveStrategy.toStrategy (s : ProjectiveStrategy AO BO) : Strategy AO BO where
  state := s.state
  alice x := (s.alice x).toPOVM
  bob y := (s.bob y).toPOVM

/-- A linear equivalence of entire tables, with one relabeling per input. -/
def behaviorEquiv : Behavior AO BO ≃ₗ[ℝ] Bell.Behavior (architecture AO BO) where
  toFun p x y a b := p x y ((Fintype.equivFin (AO x)).symm a)
    ((Fintype.equivFin (BO y)).symm b)
  invFun p x y a b := p x y (Fintype.equivFin (AO x) a) (Fintype.equivFin (BO y) b)
  left_inv := by intro p; funext x y a b; simp
  right_inv := by intro p; funext x y a b; simp
  map_add' := by intros; rfl
  map_smul' := by intros; rfl

/-- Relabeling keeps every finite mixture coefficient unchanged. -/
theorem finite_mixture_transport {κ : Type*} [Fintype κ] (w : κ → ℝ)
    (p : κ → Behavior AO BO) :
    behaviorEquiv AO BO (∑ k, w k • p k) =
      ∑ k, w k • behaviorEquiv AO BO (p k) := by
  simp only [map_sum, map_smul]

namespace Strategy

def encode (s : Strategy AO BO) : Bell.Strategy (architecture AO BO) where
  state := s.state
  alice x := (s.alice x).encode
  bob y := (s.bob y).encode

def decode (s : Bell.Strategy (architecture AO BO)) : Strategy AO BO where
  state := s.state
  alice x := POVM.decode (s.alice x)
  bob y := POVM.decode (s.bob y)

@[simp] theorem decode_encode (s : Strategy AO BO) : decode AO BO (encode AO BO s) = s := by
  cases s
  simp only [decode, encode, POVM.decode_encode]

@[simp] theorem encode_decode (s : Bell.Strategy (architecture AO BO)) :
    encode AO BO (decode AO BO s) = s := by
  cases s
  simp only [decode, encode, POVM.encode_decode]

def encoding : Strategy AO BO ≃ Bell.Strategy (architecture AO BO) where
  toFun := encode AO BO
  invFun := decode AO BO
  left_inv := decode_encode AO BO
  right_inv := encode_decode AO BO

@[simp] theorem encode_behavior (s : Strategy AO BO) :
    (encode AO BO s).behavior = behaviorEquiv AO BO (s.behavior AO BO) := rfl

@[simp] theorem decode_behavior (s : Bell.Strategy (architecture AO BO)) :
    (decode AO BO s).behavior AO BO = (behaviorEquiv AO BO).symm s.behavior := rfl
end Strategy

namespace ProjectiveStrategy

def encode (s : ProjectiveStrategy AO BO) : Bell.ProjectiveStrategy (architecture AO BO) where
  state := s.state
  alice x := (s.alice x).encode
  bob y := (s.bob y).encode

def decode (s : Bell.ProjectiveStrategy (architecture AO BO)) : ProjectiveStrategy AO BO where
  state := s.state
  alice x := PVM.decode (s.alice x)
  bob y := PVM.decode (s.bob y)

@[simp] theorem decode_encode (s : ProjectiveStrategy AO BO) :
    decode AO BO (encode AO BO s) = s := by
  cases s
  simp only [decode, encode, PVM.decode_encode]

@[simp] theorem encode_decode (s : Bell.ProjectiveStrategy (architecture AO BO)) :
    encode AO BO (decode AO BO s) = s := by
  cases s
  simp only [decode, encode, PVM.encode_decode]

def encoding : ProjectiveStrategy AO BO ≃ Bell.ProjectiveStrategy (architecture AO BO) where
  toFun := encode AO BO
  invFun := decode AO BO
  left_inv := decode_encode AO BO
  right_inv := encode_decode AO BO

@[simp] theorem encode_behavior (s : ProjectiveStrategy AO BO) :
    (encode AO BO s).toStrategy.behavior =
      behaviorEquiv AO BO ((s.toStrategy AO BO).behavior AO BO) := rfl

@[simp] theorem decode_behavior (s : Bell.ProjectiveStrategy (architecture AO BO)) :
    ((decode AO BO s).toStrategy AO BO).behavior AO BO =
      (behaviorEquiv AO BO).symm s.toStrategy.behavior := rfl
end ProjectiveStrategy

def rawPOVM : Set (Behavior AO BO) := Set.range (Strategy.behavior AO BO)
def rawPVM : Set (Behavior AO BO) :=
  Set.range (fun s : ProjectiveStrategy AO BO => (s.toStrategy AO BO).behavior AO BO)
def convexPOVM : Set (Behavior AO BO) := convexHull ℝ (rawPOVM AO BO)
def convexPVM : Set (Behavior AO BO) := convexHull ℝ (rawPVM AO BO)

theorem rawPOVM_transport : behaviorEquiv AO BO '' rawPOVM AO BO =
    Bell.rawPOVM (architecture AO BO) := by
  apply Set.Subset.antisymm
  · rintro p ⟨q, ⟨s, rfl⟩, rfl⟩
    exact ⟨Strategy.encode AO BO s, rfl⟩
  · rintro p ⟨s, rfl⟩
    refine ⟨(Strategy.decode AO BO s).behavior AO BO, ⟨_, rfl⟩, ?_⟩
    exact (behaviorEquiv AO BO).apply_symm_apply s.behavior

theorem rawPVM_transport : behaviorEquiv AO BO '' rawPVM AO BO =
    Bell.rawPVM (architecture AO BO) := by
  apply Set.Subset.antisymm
  · rintro p ⟨q, ⟨s, rfl⟩, rfl⟩
    exact ⟨ProjectiveStrategy.encode AO BO s, rfl⟩
  · rintro p ⟨s, rfl⟩
    refine ⟨((ProjectiveStrategy.decode AO BO s).toStrategy AO BO).behavior AO BO,
      ⟨_, rfl⟩, ?_⟩
    exact (behaviorEquiv AO BO).apply_symm_apply s.toStrategy.behavior

theorem convexPOVM_transport : behaviorEquiv AO BO '' convexPOVM AO BO =
    Bell.convexPOVM (architecture AO BO) := by
  exact ((behaviorEquiv AO BO).toLinearMap.image_convexHull (rawPOVM AO BO)).trans
    (congrArg (convexHull ℝ) (rawPOVM_transport AO BO))

theorem convexPVM_transport : behaviorEquiv AO BO '' convexPVM AO BO =
    Bell.convexPVM (architecture AO BO) := by
  exact ((behaviorEquiv AO BO).toLinearMap.image_convexHull (rawPVM AO BO)).trans
    (congrArg (convexHull ℝ) (rawPVM_transport AO BO))

theorem mem_rawPOVM_iff (p : Behavior AO BO) : p ∈ rawPOVM AO BO ↔
    behaviorEquiv AO BO p ∈ Bell.rawPOVM (architecture AO BO) := by
  rw [← rawPOVM_transport]
  simp only [Set.mem_image, (behaviorEquiv AO BO).injective.eq_iff, exists_eq_right]

theorem mem_rawPVM_iff (p : Behavior AO BO) : p ∈ rawPVM AO BO ↔
    behaviorEquiv AO BO p ∈ Bell.rawPVM (architecture AO BO) := by
  rw [← rawPVM_transport]
  simp only [Set.mem_image, (behaviorEquiv AO BO).injective.eq_iff, exists_eq_right]

theorem mem_convexPOVM_iff (p : Behavior AO BO) : p ∈ convexPOVM AO BO ↔
    behaviorEquiv AO BO p ∈ Bell.convexPOVM (architecture AO BO) := by
  rw [← convexPOVM_transport]
  simp only [Set.mem_image, (behaviorEquiv AO BO).injective.eq_iff, exists_eq_right]

theorem mem_convexPVM_iff (p : Behavior AO BO) : p ∈ convexPVM AO BO ↔
    behaviorEquiv AO BO p ∈ Bell.convexPVM (architecture AO BO) := by
  rw [← convexPVM_transport]
  simp only [Set.mem_image, (behaviorEquiv AO BO).injective.eq_iff, exists_eq_right]

theorem at_most_two_input_equality (hm : m ≤ 2) (hn : n ≤ 2) :
    convexPOVM AO BO = convexPVM AO BO := by
  apply Set.image_injective.mpr (behaviorEquiv AO BO).injective
  rw [convexPOVM_transport, convexPVM_transport]
  exact Bell.at_most_two_input_equality (architecture AO BO) hm hn

theorem two_input_equality (A : Fin 2 → Type u) (B : Fin 2 → Type v)
    [∀ x, Fintype (A x)] [∀ y, Fintype (B y)] :
    convexPOVM A B = convexPVM A B :=
  at_most_two_input_equality A B (by omega) (by omega)

theorem no_strategy_of_empty_alice (x : Fin m) [IsEmpty (AO x)] :
    IsEmpty (Strategy AO BO) :=
  ⟨fun s => isEmptyElim (Classical.choice (s.alice x).nonempty_outcomes)⟩

theorem no_strategy_of_empty_bob (y : Fin n) [IsEmpty (BO y)] :
    IsEmpty (Strategy AO BO) :=
  ⟨fun s => isEmptyElim (Classical.choice (s.bob y).nonempty_outcomes)⟩

theorem empty_hulls_of_no_strategy (h : IsEmpty (Strategy AO BO)) :
    convexPOVM AO BO = ∅ ∧ convexPVM AO BO = ∅ := by
  have hp : rawPOVM AO BO = ∅ := by
    apply Set.eq_empty_of_forall_not_mem
    rintro p ⟨s, hs⟩
    exact h.false s
  have hq : rawPVM AO BO = ∅ := by
    apply Set.eq_empty_of_forall_not_mem
    rintro p ⟨s, hs⟩
    exact h.false (s.toStrategy AO BO)
  simp [convexPOVM, convexPVM, hp, hq]

theorem no_input_strategy (A : Fin 0 → Type u) (B : Fin 0 → Type v)
    [∀ x, Fintype (A x)] [∀ y, Fintype (B y)] (ρ : State) :
    Nonempty (Strategy A B) :=
  ⟨⟨ρ, (fun x => Fin.elim0 x), (fun y => Fin.elim0 y)⟩⟩

end Bell.FiniteLabels
