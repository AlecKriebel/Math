import Bell.FiniteLabels

/-! Anonymous contracts for independent labels and degenerate alphabets. -/
noncomputable section
open scoped BigOperators
open Bell
namespace Bell.FiniteLabels
universe u v

-- Source measurements are actual matrix-valued records over Bool.
example (M : POVM Bool) : POVM.decode M.encode = M := POVM.decode_encode M
example (M : PVM (Option Bool)) : PVM.decode M.encode = M := PVM.decode_encode M

-- The principal equality specializes to non-Fin outcome types.
example : convexPOVM (fun _ : Fin 2 => Bool) (fun _ : Fin 2 => Option Bool) =
    convexPVM (fun _ : Fin 2 => Bool) (fun _ : Fin 2 => Option Bool) :=
  two_input_equality _ _

example : convexPOVM (fun x : Fin 2 => Option (Fin (x.val + 1)))
      (fun y : Fin 2 => Bool × Fin (y.val + 1)) =
    convexPVM (fun x : Fin 2 => Option (Fin (x.val + 1)))
      (fun y : Fin 2 => Bool × Fin (y.val + 1)) :=
  two_input_equality _ _

-- Input-dependent, universe-polymorphic labels require only Fintype instances.
example (AO : Fin 2 → Type u) (BO : Fin 2 → Type v)
    [∀ x, Fintype (AO x)] [∀ y, Fintype (BO y)] :
    convexPOVM AO BO = convexPVM AO BO := two_input_equality AO BO

example {m n : ℕ} (AO : Fin m → Type) (BO : Fin n → Type)
    [∀ x, Fintype (AO x)] [∀ y, Fintype (BO y)] (s : Strategy AO BO) :
    Strategy.decode AO BO (Strategy.encode AO BO s) = s :=
  Strategy.decode_encode AO BO s

example {m n : ℕ} (AO : Fin m → Type) (BO : Fin n → Type)
    [∀ x, Fintype (AO x)] [∀ y, Fintype (BO y)] (s : Strategy AO BO)
    (x : Fin m) (y : Fin n) (a : AO x) (b : BO y) :
    (Strategy.encode AO BO s).behavior x y (Fintype.equivFin (AO x) a)
      (Fintype.equivFin (BO y) b) =
        born s.state.density ((s.alice x).effect a) ((s.bob y).effect b) := by
  simp [Bell.Strategy.behavior, Strategy.encode, POVM.encode]

example (AO BO : Fin 2 → Type) [∀ x, Fintype (AO x)] [∀ y, Fintype (BO y)]
    (p : Behavior AO BO) : p ∈ convexPVM AO BO ↔
      behaviorEquiv AO BO p ∈ Bell.convexPVM (architecture AO BO) :=
  mem_convexPVM_iff AO BO p

-- A declared empty outcome alphabet at an existing input rules out a strategy.
example : IsEmpty (POVM Empty) := POVM.no_empty_measurement

example : convexPOVM (fun _ : Fin 1 => Empty) (fun _ : Fin 2 => Bool) = ∅ ∧
    convexPVM (fun _ : Fin 1 => Empty) (fun _ : Fin 2 => Bool) = ∅ :=
  empty_hulls_of_no_strategy _ _ (no_strategy_of_empty_alice _ _ 0)

example : convexPOVM (fun _ : Fin 2 => Bool) (fun _ : Fin 1 => Empty) = ∅ ∧
    convexPVM (fun _ : Fin 2 => Bool) (fun _ : Fin 1 => Empty) = ∅ :=
  empty_hulls_of_no_strategy _ _ (no_strategy_of_empty_bob _ _ 0)

-- Empty input sets impose no measurement obligations, even with Empty labels.
example (ρ : State) :
    Nonempty (Strategy (fun _ : Fin 0 => Empty) (fun _ : Fin 0 => Empty)) :=
  no_input_strategy _ _ ρ

end Bell.FiniteLabels
