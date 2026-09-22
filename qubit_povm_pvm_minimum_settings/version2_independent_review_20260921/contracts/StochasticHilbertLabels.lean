import Bell.HilbertFiniteLabels
import Bell.FiniteStochastic

/- Independent review contract: combine all new interfaces and expose the
processed original tensor-Born table in the conclusion. -/
noncomputable section
open scoped BigOperators TensorProduct
namespace IndependentStochasticLabels
open Bell
universe u v w z
variable {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]
  [FiniteDimensional ℂ E] [FiniteDimensional ℂ F]
variable {m n r q : ℕ}
variable (AO : Fin m → Type u) (BO : Fin n → Type v)
  (CO : Fin r → Type w) (DO : Fin q → Type z)
  [∀ x, Fintype (AO x)] [∀ y, Fintype (BO y)]
  [∀ x, Fintype (CO x)] [∀ y, Fintype (DO y)]

theorem physical_processed_simulation
    (s : HilbertFiniteLabels.Strategy E F AO BO)
    (T : FiniteLabels.StochasticProcessing AO BO CO DO)
    (hE : Module.finrank ℂ E ≤ 2) (hF : Module.finrank ℂ F ≤ 2)
    (hm : m ≤ 2) (hn : n ≤ 2) :
    ∃ (ι : Type) (_ : Fintype ι) (weights : ι → ℝ)
      (t : ι → HilbertFiniteLabels.ProjectiveStrategy
        Hilbert.QubitSpace Hilbert.QubitSpace CO DO),
      (∀ i, 0 ≤ weights i) ∧ (∑ i, weights i) = 1 ∧
      (∑ i, weights i • ((t i).toStrategy CO DO).behavior CO DO) =
      (fun x y a b => ∑ c, ∑ d,
        (T.aliceChannel x).probability c a * (T.bobChannel y).probability d b *
        (LinearMap.trace ℂ (E ⊗[ℂ] F)
          (s.state.density * TensorProduct.map
            ((s.alice (T.aliceInput x)).effect c)
            ((s.bob (T.bobInput y)).effect d))).re) := by
  classical
  have hp := T.mem_convexPVM (s.two_input_simulable AO BO hE hF hm hn)
  change T.behavior (s.behavior AO BO) ∈
    convexHull ℝ (FiniteLabels.rawPVM CO DO) at hp
  obtain ⟨ι, hi, weights, p, hw, hsum, hp, he⟩ :=
    mem_convexHull_iff_exists_fintype.mp hp
  letI : Fintype ι := hi
  choose t ht using hp
  refine ⟨ι, hi, weights,
    fun i => HilbertFiniteLabels.ofQubitProjectiveStrategy CO DO (t i), hw, hsum, ?_⟩
  simpa only [HilbertFiniteLabels.ofQubitProjectiveStrategy_behavior, ht] using he

-- Empty row families are legitimate; an existing row with empty targets is not.
example : Nonempty (StochasticChannel Empty Empty) :=
  StochasticChannel.exists_of_empty_source
example : ¬ Nonempty (StochasticChannel Bool Empty) :=
  StochasticChannel.no_channel_to_empty

-- Arbitrary named labels include input-dependent empty alphabets, without
-- silently imposing an inhabitedness assumption on the equality theorem.
def EdgeLabel (x : Fin 2) : Type := if x = 0 then Empty else Bool
instance (x : Fin 2) : Fintype (EdgeLabel x) := by
  unfold EdgeLabel
  split <;> infer_instance

example : FiniteLabels.convexPOVM EdgeLabel (fun _ : Fin 2 => Option Bool) =
    FiniteLabels.convexPVM EdgeLabel (fun _ : Fin 2 => Option Bool) :=
  FiniteLabels.two_input_equality _ _

#print axioms physical_processed_simulation
end IndependentStochasticLabels
