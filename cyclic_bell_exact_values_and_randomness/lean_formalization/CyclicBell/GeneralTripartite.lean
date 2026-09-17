import CyclicBell.GeneralExtendedBehavior
import CyclicBell.GeneralHilbertBridge
import CyclicBell.GeneralOperational

/-! Actual finite tripartite tensor model. Eve is an arbitrary POVM, not a PVM.
The mixed-state Born formula is connected to the sandwich/partial trace.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d] {α β : Type*}
variable {ι κ ε : Type*} [Fintype ι] [Fintype κ] [Fintype ε]
variable [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]

/-- No idempotence or orthogonality condition is imposed on Eve. -/
structure GuessPOVM (d : ℕ) [NeZero d] (ε : Type*) [Fintype ε] [DecidableEq ε] where
  effect : GuessLabel d → Mat ε
  positive : ∀ g,(effect g).PosSemidef
  complete : ∑ g,effect g=1

structure TripartiteOn (d : ℕ) [NeZero d] (α β ι κ ε : Type*)
    [Fintype ι] [Fintype κ] [Fintype ε]
    [DecidableEq ι] [DecidableEq κ] [DecidableEq ε] where
  state : StateOn ((ι×κ)×ε)
  alice : α → Measurement d ι
  bob : β → Measurement d κ
  eve : GuessPOVM d ε

/-- Square-root Gram factorization proves positivity for arbitrary tensor
positive matrices, rather than only idempotent measurement effects. -/
theorem advKron_positive (A : Mat ι) (B : Mat κ)
    (hA : A.PosSemidef) (hB : B.PosSemidef) : (kron A B).PosSemidef := by
  have h := Matrix.posSemidef_conjTranspose_mul_self (kron hA.sqrt hB.sqrt)
  rwa [kron_star,hA.posSemidef_sqrt.isHermitian.eq,hB.posSemidef_sqrt.isHermitian.eq,
    kron_mul,hA.sqrt_mul_self,hB.sqrt_mul_self] at h

theorem advKron_trace (A : Mat ι) (B : Mat κ) :
    Matrix.trace (kron A B)=Matrix.trace A*Matrix.trace B := by
  simp only [Matrix.trace,Matrix.diag_apply,kron,Fintype.sum_prod_type,
    Finset.sum_mul,Finset.mul_sum]
  rw [Finset.sum_comm]

theorem advStateEval_positive (ρ X : Mat ι) (hρ : ρ.PosSemidef) (hX : X.PosSemidef) :
    0≤stateEval ρ X := by
  have h := stateEval_square_nonnegative hρ hX.sqrt
  rwa [hX.posSemidef_sqrt.isHermitian.eq,hX.sqrt_mul_self] at h

def tripartiteBehavior (s : TripartiteOn d α β ι κ ε) : ExtendedBehavior d α β :=
  fun x y a b g => stateEval s.state.density
    (kron (kron ((s.alice x).effect a) ((s.bob y).effect b)) (s.eve.effect g))

theorem tripartiteBehavior_nonnegative (s : TripartiteOn d α β ι κ ε)
    (x : α) (y : β) (a b : Ix d) (g : GuessLabel d) :
    0≤tripartiteBehavior s x y a b g := by
  apply advStateEval_positive _ _ s.state.positive
  exact advKron_positive _ _
    (advKron_positive _ _ ((s.alice x).positive a) ((s.bob y).positive b)) (s.eve.positive g)

theorem tripartiteBehavior_marginal (s : TripartiteOn d α β ι κ ε)
    (x : α) (y : β) (a b : Ix d) :
    forgetE (tripartiteBehavior s) x y a b = stateEval s.state.density
      (kron (kron ((s.alice x).effect a) ((s.bob y).effect b)) (1 : Mat ε)) := by
  unfold forgetE tripartiteBehavior
  rw [← stateEval_sum,← kron_sum_right,s.eve.complete]

theorem tripartiteBehavior_normalized (s : TripartiteOn d α β ι κ ε) :
    ExtendedNormalized (tripartiteBehavior s) := by
  refine ⟨tripartiteBehavior_nonnegative s,?_⟩
  intro x y
  change (∑ a,∑ b,forgetE (tripartiteBehavior s) x y a b)=1
  simp only [tripartiteBehavior_marginal]
  have hsum : (∑ a,∑ b,kron
      (kron ((s.alice x).effect a) ((s.bob y).effect b)) (1 : Mat ε))=1 := by
    simp only [← kron_sum_left,← kron_sum_right,(s.alice x).complete,
      (s.bob y).complete,kron_one]
  simp only [← stateEval_sum]
  rw [hsum,stateEval_one s.state.normalized]

/-- The actual unnormalized Eve state after the joint projective outcome. -/
def mixedConditionalE (ρ : Mat (ι×ε)) (P : Mat ι) : Mat ε :=
  partialE (kron P (1 : Mat ε)*ρ*(kron P (1 : Mat ε)).conjTranspose)

/-- Trace-pairing characterization of the entrywise partial trace. -/
theorem partialE_pairing (R : Mat (ι×ε)) (Q : Mat ε) :
    Matrix.trace (Q*partialE R)=Matrix.trace (R*kron (1 : Mat ι) Q) := by
  simp only [Matrix.trace,Matrix.diag_apply,Matrix.mul_apply,partialE,kron,
    Fintype.sum_prod_type,Finset.mul_sum]
  simp only [Matrix.one_apply,ite_mul,mul_ite,mul_one,mul_zero,zero_mul,Finset.sum_ite_eq,Finset.sum_ite_eq',Finset.mem_univ,ite_true]
  conv_lhs =>
    arg 2
    ext x
    rw [Finset.sum_comm]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro e _
  rw [Finset.sum_comm]
  simp only [Finset.sum_ite_eq,Finset.mem_univ,ite_true,one_mul]
  apply Finset.sum_congr rfl
  intro f _
  simp [mul_comm]

/-- Sandwich/Born equivalence uses projectivity only on the observed AB side.
Q may be any matrix; in the physical application it is an arbitrary POVM effect. -/
theorem mixedConditionalE_Born (ρ : Mat (ι×ε)) (P : Mat ι) (Q : Mat ε)
    (hP : P.IsHermitian) (hPP : P*P=P) :
    Matrix.trace (Q*mixedConditionalE ρ P)=Matrix.trace (ρ*kron P Q) := by
  rw [mixedConditionalE,partialE_pairing,kron_star,hP.eq,Matrix.conjTranspose_one]
  let S := kron P (1 : Mat ε)
  let E := kron (1 : Mat ι) Q
  change Matrix.trace (S*ρ*S*E)=_
  calc
    Matrix.trace (S*ρ*S*E)=Matrix.trace (S*(ρ*(S*E))) := by
      congr 1; noncomm_ring
    _ = Matrix.trace ((ρ*(S*E))*S) := Matrix.trace_mul_comm _ _
    _ = Matrix.trace (ρ*(S*E*S)) := by congr 1; noncomm_ring
    _ = _ := by simp only [S,E,kron_mul,mul_one,one_mul,hPP]

theorem tripartiteBehavior_instrument (s : TripartiteOn d α β ι κ ε)
    (x : α) (y : β) (a b : Ix d) (g : GuessLabel d) :
    tripartiteBehavior s x y a b g =
      (Matrix.trace (s.eve.effect g*mixedConditionalE s.state.density
        (kron ((s.alice x).effect a) ((s.bob y).effect b)))).re := by
  symm
  apply congrArg Complex.re
  apply mixedConditionalE_Born
  · simp [Matrix.IsHermitian,kron_star,((s.alice x).positive a).isHermitian.eq,
      ((s.bob y).positive b).isHermitian.eq]
  · simp [kron_mul,(s.alice x).idempotent,(s.bob y).idempotent]

/-- A complete deterministic-guess POVM on the genuine one-dimensional space. -/
def scalarGuessPOVM (g : GuessLabel d) : GuessPOVM d (Fin 1) where
  effect := fun h => if h=g then 1 else 0
  positive := by intro h; split_ifs <;> first | exact Matrix.PosSemidef.one | exact Matrix.PosSemidef.zero
  complete := by
    classical
    simp

def trivialTripartite (s : StrategyOn d α β ι κ) (g : GuessLabel d) :
    TripartiteOn d α β ι κ (Fin 1) where
  state := {
    density := kron s.state.density 1
    positive := advKron_positive _ _ s.state.positive Matrix.PosSemidef.one
    normalized := by rw [advKron_trace,s.state.normalized]; norm_num [Matrix.trace,Fin.sum_univ_succ] }
  alice := s.alice
  bob := s.bob
  eve := scalarGuessPOVM g

theorem trivialTripartite_behavior (s : StrategyOn d α β ι κ) (g : GuessLabel d) :
    tripartiteBehavior (trivialTripartite s g)=attachFixedGuess (behavior s) g := by
  classical
  funext x y a b h
  change stateEval (kron s.state.density (1 : Mat (Fin 1)))
    (kron (kron ((s.alice x).effect a) ((s.bob y).effect b))
      (if h=g then (1 : Mat (Fin 1)) else 0)) = _
  by_cases hh : h=g
  · simp only [hh,ite_true,stateEval,kron_mul,one_mul,advKron_trace]
    simp [attachFixedGuess,hh,behavior,bornProbability,stateEval,Matrix.trace,Fin.sum_univ_succ]
  · simp [hh,stateEval,kron,attachFixedGuess,Matrix.mul_apply,Matrix.trace]

theorem trivialTripartite_marginal (s : StrategyOn d α β ι κ) (g : GuessLabel d) :
    forgetE (tripartiteBehavior (trivialTripartite s g))=behavior s := by
  rw [trivialTripartite_behavior,forgetE_attachFixedGuess]

theorem trivialTripartite_success (s : StrategyOn d α β ι κ) (g : GuessLabel d)
    (x : α) (y : β) : guessingSuccess (tripartiteBehavior (trivialTripartite s g)) x y =
      behavior s x y g.1 g.2 := by
  rw [trivialTripartite_behavior,guessingSuccess_attachFixedGuess]

end CyclicBell.General
