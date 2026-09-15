import CyclicBell.GeneralTripartite

/-! A genuine three-party arbitrary-Hilbert model, and an explicit embedding of
all finite mixed tensor strategies. Eve's effects are positive, not necessarily
projective. All statements are UNCOMPILED SOURCE CANDIDATES. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder InnerProductSpace
namespace CyclicBell.General
variable {d : ℕ} [NeZero d] {α β : Type*}
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The quadratic-form definition of positivity avoids a hidden norm/dimension
assumption or a restriction of Eve's POVM to projectors. -/
structure HilbertGuessPOVM (d : ℕ) [NeZero d] (H : Type*)
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] where
  effect : GuessLabel d → H →L[ℂ] H
  selfadjoint : ∀ g,star (effect g)=effect g
  positive : ∀ g v,0≤vectorEval v (effect g)
  complete : ∑ g,effect g=1

structure CommutingEveOn (d : ℕ) [NeZero d] (α β H : Type*)
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] where
  ab : CommutingOn d α β H
  eve : HilbertGuessPOVM d H
  aliceEve : ∀ x a g,(ab.alice x).effect a*eve.effect g=eve.effect g*(ab.alice x).effect a
  bobEve : ∀ y b g,(ab.bob y).effect b*eve.effect g=eve.effect g*(ab.bob y).effect b

def commutingExtendedBehavior (s : CommutingEveOn d α β H) : ExtendedBehavior d α β :=
  fun x y a b g => vectorEval s.ab.vector
    ((s.ab.alice x).effect a*(s.ab.bob y).effect b*s.eve.effect g)

/-- Positivity of P Q for a projection P commuting with positive Q is proved
through P Q P and the actual nonnegative quadratic form. -/
theorem commuting_projection_positive (P Q : H →L[ℂ] H)
    (hP : star P=P) (hPP : P*P=P) (hPQ : P*Q=Q*P)
    (hQ : ∀ v,0≤vectorEval v Q) (v : H) : 0≤vectorEval v (P*Q) := by
  have he : P*Q=P*Q*P := by
    calc
      P*Q=(P*P)*Q := by rw [hPP]
      _ = P*(P*Q) := mul_assoc _ _ _
      _ = P*(Q*P) := by rw [hPQ]
      _ = P*Q*P := (mul_assoc _ _ _).symm
  rw [he]
  change 0≤(@inner ℂ _ _ v (P (Q (P v)))).re
  rw [← ContinuousLinearMap.adjoint_inner_left]
  change 0≤(@inner ℂ _ _ ((star P) v) (Q (P v))).re
  rw [hP]
  exact hQ (P v)

theorem commutingExtended_nonnegative (s : CommutingEveOn d α β H)
    (x : α) (y : β) (a b : Ix d) (g : GuessLabel d) :
    0≤commutingExtendedBehavior s x y a b g := by
  apply commuting_projection_positive
    ((s.ab.alice x).effect a*(s.ab.bob y).effect b) (s.eve.effect g)
  · exact commuting_joint_selfadjoint s.ab x y a b
  · have h := commuting_joint_square s.ab x y a b
    rwa [commuting_joint_selfadjoint] at h
  · calc
      _ = (s.ab.alice x).effect a*((s.ab.bob y).effect b*s.eve.effect g) := mul_assoc _ _ _
      _ = (s.ab.alice x).effect a*(s.eve.effect g*(s.ab.bob y).effect b) := by rw [s.bobEve]
      _ = ((s.ab.alice x).effect a*s.eve.effect g)*(s.ab.bob y).effect b := (mul_assoc _ _ _).symm
      _ = _ := by rw [s.aliceEve,mul_assoc]
  · exact s.eve.positive g

theorem forgetE_commutingExtended (s : CommutingEveOn d α β H) :
    forgetE (commutingExtendedBehavior s)=commutingBehavior s.ab := by
  funext x y a b
  unfold forgetE commutingExtendedBehavior commutingBehavior
  rw [← vectorEval_sum,← Finset.mul_sum,s.eve.complete,mul_one]

theorem commutingExtended_normalized (s : CommutingEveOn d α β H) :
    ExtendedNormalized (commutingExtendedBehavior s) := by
  refine ⟨commutingExtended_nonnegative s,?_⟩
  intro x y
  change (∑ a,∑ b,forgetE (commutingExtendedBehavior s) x y a b)=1
  rw [forgetE_commutingExtended]
  exact commutingBehavior_normalized s.ab x y

variable {ι κ ε : Type*} [Fintype ι] [Fintype κ] [Fintype ε]
  [DecidableEq ι] [DecidableEq κ] [DecidableEq ε]

theorem matrixCLM_quadratic_positive (M : Mat ι) (hM : M.PosSemidef)
    (v : EuclideanSpace ℂ ι) : 0≤vectorEval v (matrixCLM M) := by
  obtain ⟨x,rfl⟩ := euclidVector_surjective v
  change 0≤(@inner ℂ _ _ (euclidVector x) (matrixCLM M (euclidVector x))).re
  rw [matrixCLM_on_vector,euclidVector_inner]
  simpa only [ip,dotProduct,Pi.star_apply] using hM.re_dotProduct_nonneg x

/-- A full purification of the ABE mixed state; Alice, Bob and Eve all act
trivially on the extra purification coordinate. -/
def tripartiteToCommuting (s : TripartiteOn d α β ι κ ε) :
    CommutingEveOn d α β
      (EuclideanSpace ℂ (((ι×κ)×ε)×((ι×κ)×ε))) where
  ab := {
    vector := purificationVector s.state
    normalized := purificationVector_normalized s.state
    alice := fun x => coordinateMeasurement
      (leftMeasurement (κ := (ι×κ)×ε)
        (leftMeasurement (κ := ε) (leftMeasurement (κ := κ) (s.alice x))))
    bob := fun y => coordinateMeasurement
      (leftMeasurement (κ := (ι×κ)×ε)
        (leftMeasurement (κ := ε) (rightMeasurement (ι := ι) (s.bob y))))
    cross := by
      intro x y a b
      change matrixCLM (kron (kron (kron ((s.alice x).effect a) 1) 1) 1)*
        matrixCLM (kron (kron (kron 1 ((s.bob y).effect b)) 1) 1)=_
      simp only [coordinateMeasurement,leftMeasurement,rightMeasurement,← matrixCLM_mul,kron_mul,mul_one,one_mul] }
  eve := {
    effect := fun g => matrixCLM (kron (kron (1 : Mat (ι×κ)) (s.eve.effect g)) (1 : Mat ((ι×κ)×ε)))
    selfadjoint := by
      intro g
      rw [← matrixCLM_star]
      simp only [kron_star,Matrix.conjTranspose_one,(s.eve.positive g).isHermitian.eq]
    positive := by
      intro g v
      apply matrixCLM_quadratic_positive
      exact advKron_positive _ _
        (advKron_positive _ _ Matrix.PosSemidef.one (s.eve.positive g)) Matrix.PosSemidef.one
    complete := by
      rw [← matrixCLM_sum,← kron_sum_left,← kron_sum_right,s.eve.complete,kron_one,kron_one,matrixCLM_one] }
  aliceEve := by
    intro x a g
    change matrixCLM (kron (kron (kron ((s.alice x).effect a) 1) 1) 1)*
      matrixCLM (kron (kron 1 (s.eve.effect g)) 1)=_
    simp only [coordinateMeasurement,leftMeasurement,rightMeasurement,← matrixCLM_mul,kron_mul,mul_one,one_mul]
  bobEve := by
    intro y b g
    change matrixCLM (kron (kron (kron 1 ((s.bob y).effect b)) 1) 1)*
      matrixCLM (kron (kron 1 (s.eve.effect g)) 1)=_
    simp only [coordinateMeasurement,leftMeasurement,rightMeasurement,← matrixCLM_mul,kron_mul,mul_one,one_mul]

theorem tripartiteToCommuting_behavior (s : TripartiteOn d α β ι κ ε) :
    commutingExtendedBehavior (tripartiteToCommuting s)=tripartiteBehavior s := by
  funext x y a b g
  change vectorEval (purificationVector s.state)
    (matrixCLM (kron (kron (kron ((s.alice x).effect a) 1) 1) 1)*
     matrixCLM (kron (kron (kron 1 ((s.bob y).effect b)) 1) 1)*
     matrixCLM (kron (kron 1 (s.eve.effect g)) 1))=_
  simp only [coordinateMeasurement,leftMeasurement,rightMeasurement,← matrixCLM_mul,kron_mul,mul_one,one_mul]
  exact purification_stateEval s.state _

end CyclicBell.General
