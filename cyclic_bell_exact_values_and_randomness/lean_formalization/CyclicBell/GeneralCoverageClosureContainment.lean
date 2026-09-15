import CyclicBell.GeneralCoverageClosureSequence
import CyclicBell.GeneralCoverageReconstruction

/-! Actual closure containment for the finite-input Bell scenarios. The limiting
Hilbert space and commuting PVMs are constructed from word moments; no presumed
closedness, limiting realization, or Qqa-to-Qqc embedding is an assumption. -/
noncomputable section
open scoped Topology
namespace CyclicBell.General
open Coverage
variable {d : ℕ} [NeZero d] {α β : Type}

theorem Qqc_isSeqClosed : IsSeqClosed (Qqc d α β) := by
  intro pseq p hseq hlim
  have hqc : ∀ n,pseq n ∈ Qqc d α β := hseq
  choose Hn nH iH cH s hs using hqc
  letI := nH
  letI := iH
  letI := cH
  have hlim' : Filter.Tendsto (fun n => commutingBehavior (s n)) Filter.atTop (𝓝 p) := by
    simpa only [hs] using hlim
  refine ⟨LimitHilbert naturalUltrafilter Hn s,inferInstance,inferInstance,inferInstance,
    reconstructedModel naturalUltrafilter Hn s,?_⟩
  funext x y a b
  apply Complex.ofReal_injective
  calc
    (commutingBehavior (reconstructedModel naturalUltrafilter Hn s) x y a b : ℂ) =
        limitEntry naturalUltrafilter Hn s [] [.inl (x,a),.inr (y,b)] :=
      reconstructedModel_behavior naturalUltrafilter Hn s x y a b
    _ = (p x y a b : ℂ) := limitEntry_behavior_of_tendsto Hn s p hlim' x y a b

theorem Qqc_isClosed [Finite α] [Finite β] : IsClosed (Qqc d α β) :=
  Qqc_isSeqClosed.isClosed

/-- The contextual inclusion displayed in the manuscript, for all of its
finite input/output scenarios, independently of any Bell objective. -/
theorem Qqa_subset_Qqc [Finite α] [Finite β] : Qqa d α β ⊆ Qqc d α β :=
  closure_minimal Qq_subset_Qqc Qqc_isClosed

theorem quantum_model_inclusions [Finite α] [Finite β] :
    Qq d α β ⊆ Qqa d α β ∧ Qqa d α β ⊆ Qqc d α β :=
  ⟨Qq_subset_Qqa,Qqa_subset_Qqc⟩

end CyclicBell.General
