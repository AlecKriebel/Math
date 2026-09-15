import CyclicBell.GeneralAdversarialValues
import Mathlib.Topology.Instances.Matrix

/-! Every fixed finite-Eve POVM objective has an attained maximum.
This uses the general Gram-factor compactness pattern inspected in the separate
qubit Bell project's QuantumCompactness, with a new arbitrary-dimension bound.
No qubit theorem, source cache or external verdict is imported. Uncompiled. -/
noncomputable section
open Set
open scoped BigOperators Matrix ComplexOrder Topology
namespace CyclicBell.General
variable {d : ℕ} [NeZero d] {ε : Type} [Fintype ε] [DecidableEq ε]

def eveGram (L : Mat ε) : Mat ε := Lᴴ*L

def EveGramValid (L : GuessLabel d → Mat ε) : Prop := ∑ g,eveGram (L g)=1

def eveGramPOVM (L : GuessLabel d → Mat ε) (hL : EveGramValid L) : GuessPOVM d ε where
  effect := fun g => eveGram (L g)
  positive := fun g => Matrix.posSemidef_conjTranspose_mul_self (L g)
  complete := hL

/-- Exact factorization of any finite POVM; no projectivity/rank-one premise. -/
theorem everyPOVM_has_Gram (Q : GuessPOVM d ε) :
    ∃ L : GuessLabel d → Mat ε,EveGramValid L ∧ ∀ g,eveGram (L g)=Q.effect g := by
  let L : GuessLabel d → Mat ε := fun g => (Q.positive g).sqrt
  have hL (g : GuessLabel d) : eveGram (L g)=Q.effect g := by
    rw [eveGram,(Q.positive g).posSemidef_sqrt.isHermitian.eq,(Q.positive g).sqrt_mul_self]
  have hn : EveGramValid L := by simpa only [EveGramValid,hL] using Q.complete
  exact ⟨L,hn,hL⟩

/-- Entrywise bound comes from normalization, not an a priori bounded POVM set. -/
theorem eveGram_trace (L : Mat ε) :
    (Matrix.trace (eveGram L)).re=∑ i,∑ j,‖L i j‖^2 := by
  have h (z : ℂ) : (star z*z).re=‖z‖^2 := by
    rw [← Complex.normSq_eq_conj_mul_self,Complex.ofReal_re,Complex.normSq_eq_norm_sq]
  simp only [eveGram,Matrix.trace,Matrix.diag_apply,Matrix.mul_apply,
    Matrix.conjTranspose_apply,Complex.re_sum,h]
  exact Finset.sum_comm

theorem eveGram_entry_le (L : Mat ε) (i j : ε) :
    ‖L i j‖^2≤(Matrix.trace (eveGram L)).re := by
  rw [eveGram_trace]
  exact (Finset.single_le_sum (fun k _ => sq_nonneg ‖L i k‖) (Finset.mem_univ j)).trans
    (Finset.single_le_sum (fun k _ => Finset.sum_nonneg fun l _ => sq_nonneg ‖L k l‖)
      (Finset.mem_univ i))

def EveGramBox (d : ℕ) [NeZero d] (ε : Type) [Fintype ε] : Set (GuessLabel d → Mat ε) :=
  {L | ∀ g i j,‖L g i j‖≤(Fintype.card ε : ℝ)+1}

theorem eveGramBox_compact : IsCompact (EveGramBox d ε) := by
  have hc := isCompact_pi_infinite fun _ : GuessLabel d =>
    isCompact_pi_infinite fun _ : ε => isCompact_pi_infinite fun _ : ε =>
      isCompact_closedBall (0 : ℂ) ((Fintype.card ε : ℝ)+1)
  simpa only [EveGramBox,Metric.mem_closedBall,dist_zero_right] using hc

theorem eveGramValid_box (L : GuessLabel d → Mat ε) (hL : EveGramValid L) :
    L∈EveGramBox d ε := by
  have htotal : (∑ g,(Matrix.trace (eveGram (L g))).re)=(Fintype.card ε : ℝ) := by
    have h := congrArg (fun M : Mat ε => (Matrix.trace M).re) hL
    simpa [Matrix.trace_sum,Matrix.trace_one] using h
  intro g i j
  have hone := eveGram_entry_le (L g) i j
  have htwo : (Matrix.trace (eveGram (L g))).re≤(Fintype.card ε : ℝ) := by
    rw [← htotal]
    exact Finset.single_le_sum (fun a _ => by rw [eveGram_trace]; positivity) (Finset.mem_univ g)
  have hc : (0 : ℝ)≤Fintype.card ε := Nat.cast_nonneg _
  nlinarith [norm_nonneg (L g i j),sq_nonneg (Fintype.card ε : ℝ)]

theorem eveGramValid_closed : IsClosed {L : GuessLabel d → Mat ε | EveGramValid L} := by
  unfold EveGramValid
  apply isClosed_eq _ continuous_const
  unfold eveGram
  apply continuous_pi
  intro i
  apply continuous_pi
  intro j
  simp only [Matrix.sum_apply,Matrix.mul_apply,Matrix.conjTranspose_apply]
  fun_prop

theorem eveGramValid_compact : IsCompact {L : GuessLabel d → Mat ε | EveGramValid L} :=
  eveGramBox_compact.of_isClosed_subset eveGramValid_closed eveGramValid_box

theorem eveGramValid_nonempty : Set.Nonempty {L : GuessLabel d → Mat ε | EveGramValid L} := by
  let L : GuessLabel d → Mat ε := fun g => if g=(0,0) then 1 else 0
  refine ⟨L,?_⟩
  simp [L,EveGramValid,eveGram]

def povmObjective (σ : GuessLabel d → Mat ε) (Q : GuessPOVM d ε) : ℝ :=
  ∑ g,(Matrix.trace (Q.effect g*σ g)).re

def eveGramObjective (σ : GuessLabel d → Mat ε) (L : GuessLabel d → Mat ε) : ℝ :=
  ∑ g,(Matrix.trace (eveGram (L g)*σ g)).re

theorem eveGramObjective_continuous (σ : GuessLabel d → Mat ε) : Continuous (eveGramObjective σ) := by
  unfold eveGramObjective eveGram Matrix.trace
  simp only [Matrix.diag_apply,Matrix.mul_apply,Matrix.conjTranspose_apply]
  fun_prop

/-- Even arbitrary conditional matrices give a continuous real objective on the
finite compact POVM set. Physical positivity is separately supplied below. -/
theorem finitePOVM_maximum_exists (σ : GuessLabel d → Mat ε) :
    ∃ Q : GuessPOVM d ε,∀ R : GuessPOVM d ε,povmObjective σ R≤povmObjective σ Q := by
  obtain ⟨L,hL,hmax⟩ := eveGramValid_compact.exists_isMaxOn
    eveGramValid_nonempty (eveGramObjective_continuous σ).continuousOn
  refine ⟨eveGramPOVM L hL,?_⟩
  intro R
  obtain ⟨K,hK,hR⟩ := everyPOVM_has_Gram R
  have he : povmObjective σ R=eveGramObjective σ K := by
    simp only [povmObjective,eveGramObjective,hR]
  rw [he]
  exact hmax hK

def finitePOVMValue (σ : GuessLabel d → Mat ε) : ℝ := sSup (Set.range (povmObjective σ))

theorem finitePOVMValue_attained (σ : GuessLabel d → Mat ε) :
    ∃ Q : GuessPOVM d ε,povmObjective σ Q=finitePOVMValue σ ∧
      ∀ R : GuessPOVM d ε,povmObjective σ R≤povmObjective σ Q := by
  obtain ⟨Q,hQ⟩ := finitePOVM_maximum_exists σ
  have hb : BddAbove (Set.range (povmObjective σ)) := by
    refine ⟨povmObjective σ Q,?_⟩
    rintro t ⟨R,rfl⟩
    exact hQ R
  have he : finitePOVMValue σ=povmObjective σ Q := by
    apply le_antisymm
    · apply csSup_le ⟨povmObjective σ Q,Q,rfl⟩
      rintro t ⟨R,rfl⟩
      exact hQ R
    · exact le_csSup hb ⟨Q,rfl⟩
  exact ⟨Q,he.symm,hQ⟩

/-- A useful exact dual bound for finite state discrimination. It is an algebraic
helper, not an external semidefinite solver certificate. -/
theorem povmObjective_dual_bound (σ : GuessLabel d → Mat ε) (Λ : Mat ε)
    (hΛ : ∀ g,(Λ-σ g).PosSemidef) (Q : GuessPOVM d ε) :
    povmObjective σ Q≤(Matrix.trace Λ).re := by
  have hn : 0≤∑ g,stateEval (Q.effect g) (Λ-σ g) := by
    apply Finset.sum_nonneg
    intro g _
    exact advStateEval_positive _ _ (Q.positive g) (hΛ g)
  have hc : (∑ g,stateEval (Q.effect g) Λ)=(Matrix.trace Λ).re := by
    unfold stateEval
    rw [← Complex.re_sum,← Matrix.trace_sum,← Finset.sum_mul,Q.complete,one_mul]
  simp only [stateEval_sub,Finset.sum_sub_distrib,hc] at hn
  change 0≤(Matrix.trace Λ).re-povmObjective σ Q at hn
  linarith

/-- A proved dual gap and an independently evaluated primal POVM identify the
fixed-realization optimum. No numerical certificate is trusted by this helper. -/
theorem finitePOVMValue_of_dual_attainment (σ : GuessLabel d → Mat ε) (Λ : Mat ε)
    (hΛ : ∀ g,(Λ-σ g).PosSemidef) (Q : GuessPOVM d ε)
    (hQ : povmObjective σ Q=(Matrix.trace Λ).re) : finitePOVMValue σ=(Matrix.trace Λ).re := by
  obtain ⟨R,hR,hmax⟩ := finitePOVMValue_attained σ
  apply le_antisymm
  · rw [← hR]
    exact povmObjective_dual_bound σ Λ hΛ R
  · rw [← hQ,← hR]
    exact hmax Q

variable {α β ι κ : Type} [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ]

def withEve (s : TripartiteOn d α β ι κ ε) (Q : GuessPOVM d ε) : TripartiteOn d α β ι κ ε :=
  { s with eve := Q }

def tripartiteConditionals (s : TripartiteOn d α β ι κ ε) (x : α) (y : β) : GuessLabel d → Mat ε :=
  fun g => mixedConditionalE s.state.density (kron ((s.alice x).effect g.1) ((s.bob y).effect g.2))

theorem withEve_marginal (s : TripartiteOn d α β ι κ ε) (Q : GuessPOVM d ε) :
    forgetE (tripartiteBehavior (withEve s Q))=forgetE (tripartiteBehavior s) := by
  funext x y a b
  simp only [tripartiteBehavior_marginal,withEve]

theorem guessingSuccess_objective (s : TripartiteOn d α β ι κ ε) (x : α) (y : β)
    (Q : GuessPOVM d ε) : guessingSuccess (tripartiteBehavior (withEve s Q)) x y=
      povmObjective (tripartiteConditionals s x y) Q := by
  unfold guessingSuccess povmObjective
  rw [Fintype.sum_prod_type]
  apply Finset.sum_congr rfl
  intro a _
  apply Finset.sum_congr rfl
  intro b _
  exact tripartiteBehavior_instrument (withEve s Q) x y a b (a,b)

/-- Actual fixed-realization G is attained by an arbitrary complete POVM, while
preserving the entire observed behavior. Not a maximum over realizations. -/
theorem fixed_realization_guessing_maximum (s : TripartiteOn d α β ι κ ε) (x : α) (y : β) :
    ∃ Q : GuessPOVM d ε,
      forgetE (tripartiteBehavior (withEve s Q))=forgetE (tripartiteBehavior s) ∧
      guessingSuccess (tripartiteBehavior (withEve s Q)) x y=
        finitePOVMValue (tripartiteConditionals s x y) ∧
      (0≤finitePOVMValue (tripartiteConditionals s x y) ∧
        finitePOVMValue (tripartiteConditionals s x y)≤1) ∧
      ∀ R : GuessPOVM d ε,guessingSuccess (tripartiteBehavior (withEve s R)) x y≤
        guessingSuccess (tripartiteBehavior (withEve s Q)) x y := by
  obtain ⟨Q,hQ,hmax⟩ := finitePOVMValue_attained (tripartiteConditionals s x y)
  have hs : guessingSuccess (tripartiteBehavior (withEve s Q)) x y=
      finitePOVMValue (tripartiteConditionals s x y) := (guessingSuccess_objective s x y Q).trans hQ
  refine ⟨Q,withEve_marginal s Q,hs,?_,?_⟩
  · rw [← hs]
    exact ⟨guessingSuccess_nonnegative _ (tripartiteBehavior_normalized _) _ _,
      guessingSuccess_le_one _ (tripartiteBehavior_normalized _) _ _⟩
  · intro R
    simpa only [guessingSuccess_objective] using hmax R

end CyclicBell.General
