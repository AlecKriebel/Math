import Bell.StochasticProcessing

/-! Anonymous semantic contracts for stochastic processing. -/
noncomputable section
open scoped BigOperators
namespace Bell

-- No inhabitedness premise on the two finite alphabets.
example {S T : Type*} [Fintype S] [Fintype T] [DecidableEq S] [DecidableEq T]
    (K : StochasticChannel S T) :
    ∃ w : (S → T) → ℝ, (∀ f, 0 ≤ w f) ∧ (∑ f, w f) = 1 ∧
      ∀ s t, K.probability s t = ∑ f : S → T, w f * (if f s = t then 1 else 0) :=
  StochasticChannel.decomposition K

example : Nonempty (StochasticChannel (Fin 0) (Fin 0)) :=
  StochasticChannel.exists_of_empty_source

example : Nonempty (StochasticChannel (Fin 0) (Fin 3)) :=
  StochasticChannel.exists_of_empty_source

example : ¬ Nonempty (StochasticChannel (Fin 1) (Fin 0)) :=
  StochasticChannel.no_channel_to_empty

example (K : StochasticChannel (Fin 0) (Fin 0)) (f : Fin 0 → Fin 0) : K.weight f = 1 :=
  K.weight_empty_source f

example {S T : Type*} [Fintype S] [Fintype T]
    (K : StochasticChannel S T) (f : S → T) (s : S)
    (h : K.probability s (f s) = 0) : K.weight f = 0 :=
  K.weight_zero_of_entry_zero f s h

-- Each merged projector is still idempotent, without injectivity of the map.
example {n m : ℕ} (N : PVM n) (f : Fin n → Fin m) (b : Fin m) :
    (coarsenPVM N f).effect b * (coarsenPVM N f).effect b = (coarsenPVM N f).effect b :=
  (coarsenPVM N f).idempotent b

-- One weight family reconstructs the WHOLE table, not separately chosen entries.
example {A B : Architecture} (T : StochasticProcessing A B) (p : Behavior A) :
    T.behavior p = ∑ k : T.Selector, T.weight k • (T.deterministicMap k).behavior p :=
  T.behavior_decomposition p

example {A B : Architecture} (T : StochasticProcessing A B) {p : Behavior A}
    (hp : p ∈ convexPVM A) : T.behavior p ∈ convexPVM B := T.mem_convexPVM hp

-- A processed raw PVM has a convex PVM realization; no raw closure is asserted.
example {A B : Architecture} (T : StochasticProcessing A B) {p : Behavior A}
    (hp : p ∈ rawPVM A) : T.behavior p ∈ convexPVM B := T.rawPVM_mem_convexPVM hp

end Bell
