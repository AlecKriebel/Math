import CyclicBell.GeneralBehavior
import CyclicBell.GeneralSecondCommuting

/-! Actual vector-state commuting PVM behaviors, with unrestricted complete
complex Hilbert spaces. The nonnegative normalized probabilities and their
observable correlators are derived, not fields asserting a Bell conclusion.
UNCOMPILED SOURCE CANDIDATES. -/
noncomputable section
open scoped BigOperators ComplexOrder InnerProductSpace Topology
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable {α β : Type*}

structure CommutingOn (d : ℕ) [NeZero d] (α β H : Type*)
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] where
  vector : H
  normalized : ‖vector‖ = 1
  alice : α → AlgebraPVM d (H →L[ℂ] H)
  bob : β → AlgebraPVM d (H →L[ℂ] H)
  cross : ∀ x y a b,
    (alice x).effect a * (bob y).effect b = (bob y).effect b * (alice x).effect a

def hilbertMoment (ψ : H) (T : H →L[ℂ] H) : ℂ := inner ℂ ψ (T ψ)

theorem hilbertMoment_add (ψ : H) (S T : H →L[ℂ] H) :
    hilbertMoment ψ (S+T) = hilbertMoment ψ S + hilbertMoment ψ T := by
  simp [hilbertMoment,inner_add_right]

theorem hilbertMoment_smul (ψ : H) (z : ℂ) (T : H →L[ℂ] H) :
    hilbertMoment ψ (z • T) = z * hilbertMoment ψ T := by
  simp [hilbertMoment,inner_smul_right]

theorem hilbertMoment_sum {J : Type*} [Fintype J] (ψ : H) (T : J → H →L[ℂ] H) :
    hilbertMoment ψ (∑ j,T j) = ∑ j,hilbertMoment ψ (T j) := by
  simp [hilbertMoment,inner_sum]

theorem hilbertMoment_star (ψ : H) (T : H →L[ℂ] H) :
    star (hilbertMoment ψ T) = hilbertMoment ψ (star T) := by
  change star (inner ℂ ψ (T ψ)) = inner ℂ ψ (T.adjoint ψ)
  rw [T.adjoint_inner_right]
  exact inner_conj_symm (T ψ) ψ

theorem hilbertMoment_selfadjoint (ψ : H) (T : H →L[ℂ] H) (hT : star T = T) :
    hilbertMoment ψ T = (vectorEval ψ T : ℂ) := by
  have hs : star (hilbertMoment ψ T) = hilbertMoment ψ T := by
    rw [hilbertMoment_star,hT]
  apply Complex.ext
  · rfl
  · have hi := congrArg Complex.im hs
    change -(hilbertMoment ψ T).im = (hilbertMoment ψ T).im at hi
    change (hilbertMoment ψ T).im = 0
    linarith

theorem vectorEval_hermitianPart (ψ : H) (T : H →L[ℂ] H) :
    vectorEval ψ (algebraHerm T) = vectorEval ψ T := by
  change (hilbertMoment ψ (algebraHerm T)).re = (hilbertMoment ψ T).re
  rw [algebraHerm,hilbertMoment_smul,hilbertMoment_add,← hilbertMoment_star]
  simp [Complex.mul_re]
  ring

def commutingBehavior (s : CommutingOn d α β H) : BellBehavior d α β :=
  fun x y a b => vectorEval s.vector ((s.alice x).effect a * (s.bob y).effect b)

theorem commuting_joint_selfadjoint (s : CommutingOn d α β H)
    (x : α) (y : β) (a b : Ix d) :
    star ((s.alice x).effect a * (s.bob y).effect b) =
      (s.alice x).effect a * (s.bob y).effect b := by
  rw [star_mul,(s.bob y).selfadjoint,(s.alice x).selfadjoint,← s.cross]

theorem commuting_joint_square (s : CommutingOn d α β H)
    (x : α) (y : β) (a b : Ix d) :
    star ((s.alice x).effect a * (s.bob y).effect b) *
      ((s.alice x).effect a * (s.bob y).effect b) =
      (s.alice x).effect a * (s.bob y).effect b := by
  rw [star_mul,(s.bob y).selfadjoint,(s.alice x).selfadjoint]
  calc
    _ = (s.bob y).effect b * ((s.alice x).effect a * (s.alice x).effect a) *
        (s.bob y).effect b := by noncomm_ring
    _ = (s.alice x).effect a * (s.bob y).effect b := by
      rw [(s.alice x).idempotent,← s.cross,mul_assoc,(s.bob y).idempotent]

theorem commutingBehavior_nonnegative (s : CommutingOn d α β H)
    (x : α) (y : β) (a b : Ix d) : 0 ≤ commutingBehavior s x y a b := by
  unfold commutingBehavior
  rw [← commuting_joint_square s x y a b,vectorEval_square]
  exact sq_nonneg _

theorem commutingBehavior_left_marginal (s : CommutingOn d α β H)
    (x : α) (y : β) (a : Ix d) :
    (∑ b,commutingBehavior s x y a b) = vectorEval s.vector ((s.alice x).effect a) := by
  unfold commutingBehavior
  rw [← vectorEval_sum,← Finset.mul_sum,(s.bob y).complete,mul_one]

theorem commutingBehavior_right_marginal (s : CommutingOn d α β H)
    (x : α) (y : β) (b : Ix d) :
    (∑ a,commutingBehavior s x y a b) = vectorEval s.vector ((s.bob y).effect b) := by
  unfold commutingBehavior
  rw [← vectorEval_sum,← Finset.sum_mul,(s.alice x).complete,one_mul]

theorem commutingBehavior_normalized (s : CommutingOn d α β H) (x : α) (y : β) :
    (∑ a,∑ b,commutingBehavior s x y a b) = 1 := by
  simp only [commutingBehavior_left_marginal]
  rw [← vectorEval_sum,(s.alice x).complete,vectorEval_one s.vector s.normalized]

theorem commutingBehavior_complex (s : CommutingOn d α β H)
    (x : α) (y : β) (a b : Ix d) :
    (commutingBehavior s x y a b : ℂ) =
      hilbertMoment s.vector ((s.alice x).effect a * (s.bob y).effect b) := by
  exact (hilbertMoment_selfadjoint s.vector _ (commuting_joint_selfadjoint s x y a b)).symm

/-- Correlator equality with the real Born array; reality is proved above. -/
theorem probabilityCorrelator_commuting (s : CommutingOn d α β H) (x : α) (y : β) :
    probabilityCorrelator (commutingBehavior s) x y =
      hilbertMoment s.vector (algebraEncoded (s.alice x) * algebraEncoded (s.bob y)) := by
  unfold probabilityCorrelator algebraEncoded
  simp only [Finset.sum_mul,Finset.mul_sum,smul_mul_assoc,mul_smul_comm,smul_smul,
    hilbertMoment_sum,hilbertMoment_smul,commutingBehavior_complex,chi_add]

def pullCommuting {α' β' : Type*} (s : CommutingOn d α β H)
    (f : α' → α) (g : β' → β) : CommutingOn d α' β' H where
  vector := s.vector
  normalized := s.normalized
  alice := fun x => s.alice (f x)
  bob := fun y => s.bob (g y)
  cross := fun x y a b => s.cross (f x) (g y) a b

theorem commutingBehavior_pull {α' β' : Type*} (s : CommutingOn d α β H)
    (f : α' → α) (g : β' → β) :
    commutingBehavior (pullCommuting s f g) = pullBehavior f g (commutingBehavior s) := rfl

theorem firstReducedBell_commuting (s : CommutingOn d (Fin 2) (Ix d) H) :
    firstReducedBell (commutingBehavior s) = vectorEval s.vector
      (operatorFirst (algebraEncoded (s.alice 0)) (algebraEncoded (s.alice 1))
        (fun y => algebraEncoded (s.bob y))) := by
  unfold firstReducedBell operatorFirst
  simp only [vectorEval_sum,vectorEval_hermitianPart,add_mul,smul_mul_assoc,
    probabilityCorrelator_commuting]
  change (∑ y,(hilbertMoment s.vector _ + chi y * hilbertMoment s.vector _).re) = _
  simp only [← hilbertMoment_smul,← hilbertMoment_add]
  rfl

theorem secondReducedBell_commuting (s : CommutingOn d (Ix d) (Ix d) H) :
    secondReducedBell (commutingBehavior s) = vectorEval s.vector
      (operatorSecond generalLambda (fun l => algebraEncoded (s.alice l))
        (fun y => algebraEncoded (s.bob y))) := by
  unfold secondReducedBell operatorSecond
  simp only [probabilityCorrelator_commuting,vectorEval_sum,vectorEval_hermitianPart,
    algebraFourier,Finset.mul_sum,mul_smul_comm]
  simp only [← hilbertMoment_smul,← hilbertMoment_sum]
  rfl

theorem firstAugmentedBell_commuting (s : CommutingOn d (Fin 2) (AugmentedInputs d) H) :
    firstAugmentedBell (commutingBehavior s) = vectorEval s.vector
      (operatorFirst (algebraEncoded (s.alice 0)) (algebraEncoded (s.alice 1))
        (fun y => algebraEncoded (s.bob (some y))) +
        algebraHerm (algebraEncoded (s.alice 0) * algebraEncoded (s.bob none))) := by
  unfold firstAugmentedBell
  rw [← commutingBehavior_pull,firstReducedBell_commuting,probabilityCorrelator_commuting,
    vectorEval_add,vectorEval_hermitianPart]
  rfl

theorem secondAugmentedBell_commuting (s : CommutingOn d (Ix d) (AugmentedInputs d) H) :
    secondAugmentedBell (commutingBehavior s) = vectorEval s.vector
      (operatorSecond generalLambda (fun l => algebraEncoded (s.alice l))
        (fun y => algebraEncoded (s.bob (some y))) +
        algebraHerm (algebraEncoded (s.alice 0) * algebraEncoded (s.bob none))) := by
  unfold secondAugmentedBell
  rw [← commutingBehavior_pull,secondReducedBell_commuting,probabilityCorrelator_commuting,
    vectorEval_add,vectorEval_hermitianPart]
  rfl

theorem firstReducedBell_commuting_upper (hd : 2≤d) (s : CommutingOn d (Fin 2) (Ix d) H) :
    firstReducedBell (commutingBehavior s) ≤ scalarMaximum d := by
  rw [firstReducedBell_commuting]
  exact first_commuting_hilbert_bound hd s.vector s.normalized _ _ _
    (algebraEncoded_unitary _) (algebraEncoded_unitary _) (fun y => algebraEncoded_unitary _)
    (fun y => algebraPVM_cross_commute _ _ (s.cross 0 y))
    (fun y => algebraPVM_cross_commute _ _ (s.cross 1 y))

theorem secondReducedBell_commuting_upper (hd : 2≤d) (s : CommutingOn d (Ix d) (Ix d) H) :
    secondReducedBell (commutingBehavior s) ≤ (d : ℝ) := by
  rw [secondReducedBell_commuting]
  exact second_commuting_hilbert_bound hd s.vector s.normalized _ _
    (fun l => algebraEncoded_unitary _) (fun y => algebraEncoded_unitary _)

theorem firstAugmentedBell_commuting_upper (hd : 2≤d)
    (s : CommutingOn d (Fin 2) (AugmentedInputs d) H) :
    firstAugmentedBell (commutingBehavior s) ≤ scalarMaximum d+1 := by
  rw [firstAugmentedBell_commuting]
  exact first_commuting_PVM_upper hd s.vector s.normalized s.alice s.bob s.cross

theorem secondAugmentedBell_commuting_upper (hd : 2≤d)
    (s : CommutingOn d (Ix d) (AugmentedInputs d) H) :
    secondAugmentedBell (commutingBehavior s) ≤ (d : ℝ)+1 := by
  rw [secondAugmentedBell_commuting]
  exact second_commuting_PVM_upper hd s.vector s.normalized s.alice s.bob s.cross

end CyclicBell.General
