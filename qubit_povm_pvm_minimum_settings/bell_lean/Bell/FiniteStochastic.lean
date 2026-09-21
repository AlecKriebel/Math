import Bell.FiniteLabels
import Bell.StochasticProcessing

/-!
# Physical stochastic processing on arbitrary finite outcome labels

The map below is independently defined by weighted sums over the source label
types. Its exact commuting square with cardinal encoding transfers the proved
single-common-random-variable PVM construction to these physical source and
target models. Empty label types require no separate convention.
-/
noncomputable section
open scoped BigOperators
namespace Bell.FiniteLabels
universe u v w z

def encodeChannel {S : Type u} {T : Type v} [Fintype S] [Fintype T]
    (K : Bell.StochasticChannel S T) :
    Bell.StochasticChannel (Fin (Fintype.card S)) (Fin (Fintype.card T)) where
  probability s t := K.probability ((Fintype.equivFin S).symm s) ((Fintype.equivFin T).symm t)
  nonnegative s t := K.nonnegative ((Fintype.equivFin S).symm s) ((Fintype.equivFin T).symm t)
  normalized s := (Equiv.sum_comp (Fintype.equivFin T).symm
    (K.probability ((Fintype.equivFin S).symm s))).trans (K.normalized _)

structure StochasticProcessing {m n r s : ℕ}
    (AO : Fin m → Type u) (BO : Fin n → Type v)
    (CO : Fin r → Type w) (DO : Fin s → Type z)
    [∀ x, Fintype (AO x)] [∀ y, Fintype (BO y)]
    [∀ x, Fintype (CO x)] [∀ y, Fintype (DO y)] where
  aliceInput : Fin r → Fin m
  bobInput : Fin s → Fin n
  aliceChannel : (x : Fin r) → Bell.StochasticChannel (AO (aliceInput x)) (CO x)
  bobChannel : (y : Fin s) → Bell.StochasticChannel (BO (bobInput y)) (DO y)

namespace StochasticProcessing
variable {m n r s : ℕ}
variable {AO : Fin m → Type u} {BO : Fin n → Type v}
variable {CO : Fin r → Type w} {DO : Fin s → Type z}
variable [∀ x, Fintype (AO x)] [∀ y, Fintype (BO y)]
variable [∀ x, Fintype (CO x)] [∀ y, Fintype (DO y)]
variable (T : StochasticProcessing AO BO CO DO)

/-- Actual finite-label output probabilities, for all input pairs at once. -/
def behavior : Behavior AO BO →ₗ[ℝ] Behavior CO DO where
  toFun p x y a b := ∑ c, ∑ d,
    (T.aliceChannel x).probability c a * (T.bobChannel y).probability d b *
      p (T.aliceInput x) (T.bobInput y) c d
  map_add' := by
    intro p q
    funext x y a b
    simp [Pi.add_apply, mul_add, Finset.sum_add_distrib]
  map_smul' := by
    intro t p
    funext x y a b
    simp only [Pi.smul_apply, smul_eq_mul, Finset.mul_sum, RingHom.id_apply]
    apply Finset.sum_congr rfl
    intro c _
    apply Finset.sum_congr rfl
    intro d _
    ring

def encode : Bell.StochasticProcessing (architecture AO BO) (architecture CO DO) where
  aliceInput := T.aliceInput
  bobInput := T.bobInput
  aliceChannel x := encodeChannel (T.aliceChannel x)
  bobChannel y := encodeChannel (T.bobChannel y)

private theorem sum_encode {α : Type*} {β : Type*} [Fintype α] [Fintype β]
    (f : α → β → ℝ) :
    (∑ i : Fin (Fintype.card α), ∑ j : Fin (Fintype.card β),
      f ((Fintype.equivFin α).symm i) ((Fintype.equivFin β).symm j)) =
      ∑ a, ∑ b, f a b := by
  rw [Equiv.sum_comp (Fintype.equivFin α).symm
    (fun a => ∑ j : Fin (Fintype.card β), f a ((Fintype.equivFin β).symm j))]
  apply Finset.sum_congr rfl
  intro a _
  exact Equiv.sum_comp (Fintype.equivFin β).symm (f a)

/-- Relabeling commutes with the explicitly defined weighted Born table. -/
theorem encode_behavior (p : Behavior AO BO) :
    behaviorEquiv CO DO (T.behavior p) = T.encode.behavior (behaviorEquiv AO BO p) := by
  funext x y a b
  exact (sum_encode (fun c d =>
    (T.aliceChannel x).probability c ((Fintype.equivFin (CO x)).symm a) *
    (T.bobChannel y).probability d ((Fintype.equivFin (DO y)).symm b) *
    p (T.aliceInput x) (T.bobInput y) c d)).symm

/-- The complete table is one finite mixture, with the same selector for all
inputs and both parties, transported back to the original target labels. -/
theorem behavior_decomposition (p : Behavior AO BO) :
    T.behavior p = ∑ k : T.encode.Selector, T.encode.weight k •
      (behaviorEquiv CO DO).symm
        ((T.encode.deterministicMap k).behavior (behaviorEquiv AO BO p)) := by
  apply (behaviorEquiv CO DO).injective
  rw [T.encode_behavior, map_sum]
  simp only [map_smul, LinearEquiv.apply_symm_apply]
  exact T.encode.behavior_decomposition _

theorem deterministic_branch_mem_rawPVM (k : T.encode.Selector)
    {p : Behavior AO BO} (hp : p ∈ rawPVM AO BO) :
    (behaviorEquiv CO DO).symm
      ((T.encode.deterministicMap k).behavior (behaviorEquiv AO BO p)) ∈ rawPVM CO DO := by
  apply (mem_rawPVM_iff CO DO _).mpr
  simp only [LinearEquiv.apply_symm_apply]
  exact T.encode.deterministic_branch_mem_rawPVM k ((mem_rawPVM_iff AO BO p).mp hp)

theorem mem_convexPVM {p : Behavior AO BO} (hp : p ∈ convexPVM AO BO) :
    T.behavior p ∈ convexPVM CO DO := by
  apply (mem_convexPVM_iff CO DO _).mpr
  rw [T.encode_behavior]
  exact T.encode.mem_convexPVM ((mem_convexPVM_iff AO BO p).mp hp)

theorem rawPVM_mem_convexPVM {p : Behavior AO BO} (hp : p ∈ rawPVM AO BO) :
    T.behavior p ∈ convexPVM CO DO :=
  T.mem_convexPVM (subset_convexHull ℝ (rawPVM AO BO) hp)

end StochasticProcessing
end Bell.FiniteLabels
