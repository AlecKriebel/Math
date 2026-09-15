import CyclicBell.GeneralCorrelationValues
import Mathlib.Topology.Sequences

/-! The ordinary-sequence input to the closure construction. Finite input
alphabets are explicit: they are the actual scenarios used in the paper. -/
noncomputable section
open scoped Topology
open Filter
namespace CyclicBell.General.Coverage
variable {d : ℕ} [NeZero d] {α β : Type} [Finite α] [Finite β]

theorem Qqa_approximating_commuting_sequence (p : BellBehavior d α β)
    (hp : p ∈ Qqa d α β) :
    ∃ (Hn : ℕ → Type) (nH : ∀ n,NormedAddCommGroup (Hn n)),
      letI := nH
      ∃ (iH : ∀ n,InnerProductSpace ℂ (Hn n)),
      letI := iH
      ∃ (cH : ∀ n,CompleteSpace (Hn n)),
      letI := cH
      ∃ (s : ∀ n,CommutingOn d α β (Hn n)),
        Tendsto (fun n => commutingBehavior (s n)) atTop (𝓝 p) := by
  obtain ⟨pseq,hmem,hlim⟩ := mem_closure_iff_seq_limit.mp hp
  have hqc : ∀ n,pseq n ∈ Qqc d α β := fun n => Qq_subset_Qqc (hmem n)
  choose Hn nH iH cH s hs using hqc
  exact ⟨Hn,nH,iH,cH,s,by simpa only [hs] using hlim⟩

theorem behavior_coordinate_complex_tendsto (pseq : ℕ → BellBehavior d α β)
    (p : BellBehavior d α β) (hp : Tendsto pseq atTop (𝓝 p))
    (x : α) (y : β) (a b : Ix d) :
    Tendsto (fun n => (pseq n x y a b : ℂ)) atTop (𝓝 (p x y a b : ℂ)) := by
  have hcoord : Continuous (fun q : BellBehavior d α β => q x y a b) := by
    fun_prop
  exact Complex.continuous_ofReal.continuousAt.tendsto.comp
    (hcoord.continuousAt.tendsto.comp hp)

end CyclicBell.General.Coverage
