import Bell.StrategyMaps
import Bell.ClassicalProduct

/-!
# Finite stochastic output processing

A channel is a nonnegative, normalized row family. Its product distribution
selects one deterministic output for every source label simultaneously. For
bipartite processing one selector fixes all inputs and both parties at once.
Thus stochastic processing preserves the convex PVM set; it need not preserve
the raw PVM set. Empty alphabets and zero probabilities are included.
-/
noncomputable section
open scoped BigOperators
namespace Bell

/-- A possibly dependent family of stochastic rows. No nonempty-alphabet
assumption is built into the definition: normalization determines existence. -/
structure StochasticFamily (I : Type*) (O : I → Type*) [∀ i, Fintype (O i)] where
  probability : (i : I) → O i → ℝ
  nonnegative : ∀ i a, 0 ≤ probability i a
  normalized : ∀ i, ∑ a, probability i a = 1

/-- A stochastic channel between arbitrary finite source and target alphabets. -/
abbrev StochasticChannel (S T : Type*) [Fintype T] :=
  StochasticFamily S (fun _ => T)

namespace StochasticFamily
variable {I : Type*} {O : I → Type*} [∀ i, Fintype (O i)]

/-- Deterministic rows may merge different source labels. -/
def deterministic (f : (i : I) → O i) : StochasticFamily I O := by
  classical
  exact ⟨fun i a => if f i = a then 1 else 0,
    fun i a => by dsimp; split_ifs <;> norm_num, fun i => by simp⟩

/-- Exactly the rowwise existence condition, also valid for an empty source. -/
theorem nonempty_iff : Nonempty (StochasticFamily I O) ↔ ∀ i, Nonempty (O i) := by
  classical
  constructor
  · rintro ⟨K⟩ i
    by_contra h
    letI : IsEmpty (O i) := not_nonempty_iff.mp h
    have := K.normalized i
    simp at this
  · intro h
    exact ⟨deterministic (fun i => Classical.choice (h i))⟩

variable [Fintype I] [DecidableEq I] [∀ i, DecidableEq (O i)]

/-- Probability of one complete deterministic selector. -/
def weight (K : StochasticFamily I O) (f : (i : I) → O i) : ℝ :=
  ∏ i, K.probability i (f i)

omit [DecidableEq I] [∀ i, DecidableEq (O i)] in
theorem weight_nonnegative (K : StochasticFamily I O) (f : (i : I) → O i) :
    0 ≤ K.weight f := Finset.prod_nonneg (fun i _ => K.nonnegative i (f i))

/-- Normalization requires neither a nonempty source nor positive row entries. -/
theorem weight_normalized (K : StochasticFamily I O) :
    (∑ f : (i : I) → O i, K.weight f) = 1 :=
  ClassicalProduct.total_mass_one K.probability K.normalized

/-- Exact channel reconstruction by deterministic rows, simultaneously for all rows. -/
theorem reconstruction (K : StochasticFamily I O) (i : I) (a : O i) :
    (∑ f : (i : I) → O i, K.weight f * (if f i = a then 1 else 0)) =
      K.probability i a := by
  simpa only [weight, ClassicalProduct.mass, eq_comm] using
    ClassicalProduct.marginal K.probability K.normalized i a

omit [DecidableEq I] [∀ i, DecidableEq (O i)] in
/-- A selected zero-probability entry gives that whole selector weight zero. -/
theorem weight_zero_of_entry_zero (K : StochasticFamily I O)
    (f : (i : I) → O i) (i : I) (h : K.probability i (f i) = 0) : K.weight f = 0 := by
  exact Finset.prod_eq_zero (Finset.mem_univ i) h

omit [DecidableEq I] [∀ i, DecidableEq (O i)] in
/-- An empty source has one empty selector, of weight one. -/
theorem weight_empty_source [IsEmpty I] (K : StochasticFamily I O)
    (f : (i : I) → O i) : K.weight f = 1 := by simp [weight]

end StochasticFamily

namespace StochasticChannel
variable {S T : Type*} [Fintype T]

/-- An empty target is allowed exactly when no source row exists. -/
theorem nonempty_iff : Nonempty (StochasticChannel S T) ↔ (Nonempty S → Nonempty T) := by
  rw [StochasticFamily.nonempty_iff]
  constructor
  · rintro h ⟨s⟩
    exact h s
  · intro h s
    exact h ⟨s⟩

theorem exists_of_empty_source [IsEmpty S] : Nonempty (StochasticChannel S T) :=
  nonempty_iff.mpr (fun h => h.elim (fun s => isEmptyElim s))

theorem no_channel_to_empty [Nonempty S] [IsEmpty T] :
    ¬ Nonempty (StochasticChannel S T) := by
  intro h
  exact not_nonempty_iff.mpr inferInstance (nonempty_iff.mp h inferInstance)

/-- The finite channel is a convex combination of complete deterministic
functions. This includes empty source/target types whenever a channel exists. -/
theorem decomposition [Fintype S] [DecidableEq S] [DecidableEq T]
    (K : StochasticChannel S T) :
    ∃ w : (S → T) → ℝ, (∀ f, 0 ≤ w f) ∧ (∑ f, w f) = 1 ∧
      ∀ s t, K.probability s t = ∑ f : S → T, w f * (if f s = t then 1 else 0) := by
  refine ⟨K.weight, K.weight_nonnegative, K.weight_normalized, ?_⟩
  intro s t
  exact (K.reconstruction s t).symm

end StochasticChannel

/-- Local stochastic output channels, with optional deterministic input selection.
Each output row may have an input-dependent source and target alphabet. -/
structure StochasticProcessing (A B : Architecture) where
  aliceInput : Fin B.aliceInputs → Fin A.aliceInputs
  bobInput : Fin B.bobInputs → Fin A.bobInputs
  aliceChannel : (x : Fin B.aliceInputs) →
    StochasticChannel (Fin (A.aliceOutputs (aliceInput x))) (Fin (B.aliceOutputs x))
  bobChannel : (y : Fin B.bobInputs) →
    StochasticChannel (Fin (A.bobOutputs (bobInput y))) (Fin (B.bobOutputs y))

namespace StochasticProcessing
variable {A B : Architecture} (T : StochasticProcessing A B)

/-- Processing acts on the complete ambient real behavior space. -/
def behavior : Behavior A →ₗ[ℝ] Behavior B where
  toFun p x y a b := ∑ c, ∑ d,
    (T.aliceChannel x).probability c a * (T.bobChannel y).probability d b *
      p (T.aliceInput x) (T.bobInput y) c d
  map_add' := by
    intro p q
    funext x y a b
    simp [Pi.add_apply, mul_add, Finset.sum_add_distrib]
  map_smul' := by
    intro r p
    funext x y a b
    simp only [Pi.smul_apply, smul_eq_mul, Finset.mul_sum, RingHom.id_apply]
    apply Finset.sum_congr rfl
    intro c _
    apply Finset.sum_congr rfl
    intro d _
    ring

abbrev AliceRows := (x : Fin B.aliceInputs) × Fin (A.aliceOutputs (T.aliceInput x))
abbrev BobRows := (y : Fin B.bobInputs) × Fin (A.bobOutputs (T.bobInput y))
abbrev AliceSelector := (i : T.AliceRows) → Fin (B.aliceOutputs i.1)
abbrev BobSelector := (i : T.BobRows) → Fin (B.bobOutputs i.1)

/-- ONE finite random variable fixes all source-label choices on both parties,
for all inputs at once; it does not depend on the observed input pair. -/
abbrev Selector := T.AliceSelector × T.BobSelector

def aliceFamily : StochasticFamily T.AliceRows (fun i => Fin (B.aliceOutputs i.1)) where
  probability i a := (T.aliceChannel i.1).probability i.2 a
  nonnegative i a := (T.aliceChannel i.1).nonnegative i.2 a
  normalized i := (T.aliceChannel i.1).normalized i.2

def bobFamily : StochasticFamily T.BobRows (fun i => Fin (B.bobOutputs i.1)) where
  probability i b := (T.bobChannel i.1).probability i.2 b
  nonnegative i b := (T.bobChannel i.1).nonnegative i.2 b
  normalized i := (T.bobChannel i.1).normalized i.2

def weight (k : T.Selector) : ℝ := T.aliceFamily.weight k.1 * T.bobFamily.weight k.2

def deterministicMap (k : T.Selector) : StrategyMap A B where
  aliceInput := T.aliceInput
  bobInput := T.bobInput
  aliceOutput x c := k.1 ⟨x,c⟩
  bobOutput y d := k.2 ⟨y,d⟩

theorem weight_nonnegative (k : T.Selector) : 0 ≤ T.weight k :=
  mul_nonneg (T.aliceFamily.weight_nonnegative k.1) (T.bobFamily.weight_nonnegative k.2)

theorem weight_normalized : (∑ k : T.Selector, T.weight k) = 1 := by
  simp only [weight, Fintype.sum_prod_type, ← Finset.mul_sum,
    StochasticFamily.weight_normalized, mul_one]

/-- The two specified channel entries are marginals of the same global selector. -/
theorem joint_reconstruction (x : Fin B.aliceInputs) (y : Fin B.bobInputs)
    (c : Fin (A.aliceOutputs (T.aliceInput x)))
    (d : Fin (A.bobOutputs (T.bobInput y)))
    (a : Fin (B.aliceOutputs x)) (b : Fin (B.bobOutputs y)) :
    (∑ k : T.Selector, T.weight k *
      (if k.1 ⟨x,c⟩ = a ∧ k.2 ⟨y,d⟩ = b then 1 else 0)) =
      (T.aliceChannel x).probability c a * (T.bobChannel y).probability d b := by
  rw [Fintype.sum_prod_type]
  calc
    _ = (∑ f : T.AliceSelector, T.aliceFamily.weight f * (if f ⟨x,c⟩ = a then 1 else 0)) *
        (∑ g : T.BobSelector, T.bobFamily.weight g * (if g ⟨y,d⟩ = b then 1 else 0)) := by
      rw [Finset.sum_mul]
      simp_rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro f _
      apply Finset.sum_congr rfl
      intro g _
      by_cases ha : f ⟨x,c⟩ = a <;> by_cases hb : g ⟨y,d⟩ = b <;>
        simp [weight, ha, hb]
    _ = _ := by
      rw [StochasticFamily.reconstruction, StochasticFamily.reconstruction]
      rfl

/-- The same finite convex combination reconstructs the entire behavior table. -/
theorem behavior_decomposition (p : Behavior A) :
    T.behavior p = ∑ k : T.Selector, T.weight k • (T.deterministicMap k).behavior p := by
  funext x y a b
  simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
  change (∑ c, ∑ d, (T.aliceChannel x).probability c a *
    (T.bobChannel y).probability d b * p (T.aliceInput x) (T.bobInput y) c d) =
    ∑ k : T.Selector, T.weight k * ∑ c, ∑ d,
      if k.1 ⟨x,c⟩ = a ∧ k.2 ⟨y,d⟩ = b then
        p (T.aliceInput x) (T.bobInput y) c d else 0
  simp_rw [Finset.mul_sum]
  conv_rhs => rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro c _
  conv_rhs => rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro d _
  rw [← T.joint_reconstruction x y c d a b, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro k _
  split_ifs <;> simp

/-- Each deterministic branch is an actual PVM coarsening, including mergers. -/
theorem deterministic_branch_mem_rawPVM (k : T.Selector) {p : Behavior A}
    (hp : p ∈ rawPVM A) : (T.deterministicMap k).behavior p ∈ rawPVM B :=
  (T.deterministicMap k).mem_rawPVM hp

/-- Arbitrary local finite stochastic output channels preserve convexPVM.
There is deliberately no assertion that a stochastic channel preserves rawPVM. -/
theorem mem_convexPVM {p : Behavior A} (hp : p ∈ convexPVM A) :
    T.behavior p ∈ convexPVM B := by
  rw [T.behavior_decomposition]
  apply (convex_convexHull ℝ (rawPVM B)).sum_mem
  · intro k _
    exact T.weight_nonnegative k
  · exact T.weight_normalized
  · intro k _
    exact (T.deterministicMap k).mem_convexPVM hp

/-- In particular every processed raw PVM behavior has a common-randomness
PVM realization on the original target architecture. -/
theorem rawPVM_mem_convexPVM {p : Behavior A} (hp : p ∈ rawPVM A) :
    T.behavior p ∈ convexPVM B :=
  T.mem_convexPVM (subset_convexHull ℝ (rawPVM A) hp)

end StochasticProcessing
end Bell
