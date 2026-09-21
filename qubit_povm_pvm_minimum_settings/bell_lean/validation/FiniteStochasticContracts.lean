import Bell.FiniteStochastic

/-! The arbitrary-label stochastic endpoint is a physical hull statement. -/
noncomputable section
open Bell
namespace Bell.FiniteLabels
universe u v w z

example {m n r s : ℕ}
    (AO : Fin m → Type u) (BO : Fin n → Type v)
    (CO : Fin r → Type w) (DO : Fin s → Type z)
    [∀ x, Fintype (AO x)] [∀ y, Fintype (BO y)]
    [∀ x, Fintype (CO x)] [∀ y, Fintype (DO y)]
    (T : StochasticProcessing AO BO CO DO) (p : Behavior AO BO) :
    behaviorEquiv CO DO (T.behavior p) =
      T.encode.behavior (behaviorEquiv AO BO p) := T.encode_behavior p

example {m n r s : ℕ}
    (AO : Fin m → Type u) (BO : Fin n → Type v)
    (CO : Fin r → Type w) (DO : Fin s → Type z)
    [∀ x, Fintype (AO x)] [∀ y, Fintype (BO y)]
    [∀ x, Fintype (CO x)] [∀ y, Fintype (DO y)]
    (T : StochasticProcessing AO BO CO DO) (p : Behavior AO BO)
    (hp : p ∈ convexPVM AO BO) : T.behavior p ∈ convexPVM CO DO :=
  T.mem_convexPVM hp

example (T : StochasticProcessing (fun _ : Fin 2 => Bool) (fun _ : Fin 2 => Option Bool)
    (fun _ : Fin 1 => Option Bool) (fun _ : Fin 2 => Bool))
    (p : Behavior (fun _ : Fin 2 => Bool) (fun _ : Fin 2 => Option Bool))
    (hp : p ∈ rawPVM _ _) : T.behavior p ∈ convexPVM _ _ :=
  T.rawPVM_mem_convexPVM hp

-- Encoding an empty-to-empty channel does not add a nonempty premise.
example (K : Bell.StochasticChannel Empty Empty) :
    Bell.StochasticChannel (Fin (Fintype.card Empty)) (Fin (Fintype.card Empty)) :=
  encodeChannel K

-- A valid channel cannot map an existing source row into an empty target.
example : ¬ Nonempty (Bell.StochasticChannel Bool Empty) :=
  Bell.StochasticChannel.no_channel_to_empty

end Bell.FiniteLabels
