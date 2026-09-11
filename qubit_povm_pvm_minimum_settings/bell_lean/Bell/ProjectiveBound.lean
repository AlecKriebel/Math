import Bell.ProjectiveSOS
import Bell.Targets

/-!
# End-to-end physical PVM upper bound and 3-by-2 separation

This module removes `ProjectiveGlobalUpperBound` as an assumed premise of the
separation proof. The actual complex density matrix and all declared PVM effects
are used. A ternary qubit PVM must have a zero effect, and each of the three
possible zero positions is covered by an explicit operator SOS.

The rational bound 289/10 is strictly stronger than the upper bound U printed
in the paper. Neither bound is claimed to be the exact global optimum.

STATUS: complete proof-source attempt for this branch, NOT kernel-checked yet.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace Bell

/-- Finite weighted Born sums are tensor expectations of the signed effects. -/
theorem weighted_born_sum {m n : ℕ} (ρ : JointOperator)
    (M : Fin m → Operator) (N : Fin n → Operator)
    (α : Fin m → ℝ) (β : Fin n → ℝ) :
    (∑ a, ∑ b, α a * β b * born ρ (M a) (N b)) =
      expectation ρ (tensor (∑ a, α a • M a) (∑ b, β b • N b)) := by
  simp only [tensor_sum_left, tensor_sum_right, tensor_smul_left, tensor_smul_right,
    map_sum, map_smul, smul_eq_mul, born_eq_expectation, mul_assoc, Finset.mul_sum]
  rw [Finset.sum_comm]
  simp only [mul_left_comm]

theorem alice_signed_sum (M : POVM 3) :
    (∑ a, aliceSign a • M.effect a) = 1 - (2 : ℝ) • M.effect 1 := by
  rw [← M.normalized]
  norm_num [aliceSign, Fin.sum_univ_succ, two_smul]
  abel

theorem bob_signed_sum (N : POVM 2) :
    (∑ b, bobSign b • N.effect b) = 1 - (2 : ℝ) • N.effect 1 := by
  rw [← N.normalized]
  norm_num [bobSign, Fin.sum_univ_succ, two_smul]
  abel

/-- The auxiliary choice affects only observable 2, not the CHSH observables. -/
def projectiveAlice (s : ProjectiveStrategy separatorArchitecture) (k : Fin 3) :
    SOS.AliceObservables :=
  ![pvmSignObservable (s.alice 0) 1,
    pvmSignObservable (s.alice 1) 1,
    projectionInvolution ((s.alice 2).effect k) ((s.alice 2).positive k).isHermitian.eq
      ((s.alice 2).idempotent k)]

def projectiveBob (s : ProjectiveStrategy separatorArchitecture) : SOS.BobObservables :=
  ![pvmSignObservable (s.bob 0) 1, pvmSignObservable (s.bob 1) 1]

theorem projective_correlation (s : ProjectiveStrategy separatorArchitecture)
    (x : Fin 3) (y : Fin 2) :
    correlation s.toStrategy.behavior x y = expectation s.state.density
      (tensor (pvmSignObservable (s.alice x) 1).matrix
        (pvmSignObservable (s.bob y) 1).matrix) := by
  unfold correlation
  change (∑ a, ∑ b, aliceSign a * bobSign b *
    born s.state.density ((s.alice x).effect a) ((s.bob y).effect b)) = _
  rw [weighted_born_sum, alice_signed_sum, bob_signed_sum]
  simp only [pvmSignObservable_matrix]

/-- The Bell operator before choosing which auxiliary label is zero. -/
def physicalBellOperator (s : ProjectiveStrategy separatorArchitecture) : JointOperator :=
  (10 : ℝ) • SOS.chsh (projectiveAlice s 0) (projectiveBob s) +
  (3/5 : ℝ) • tensor ((s.alice 2).effect 0) ((s.bob 0).effect 0) +
  (3/5 : ℝ) • tensor ((s.alice 2).effect 1) ((s.bob 0).effect 1) +
  (4/5 : ℝ) • tensor ((s.alice 2).effect 2) ((s.bob 1).effect 0)

theorem physical_bell_expectation (s : ProjectiveStrategy separatorArchitecture) :
    bellScore s.toStrategy.behavior = expectation s.state.density (physicalBellOperator s) := by
  simp only [bellScore, physicalBellOperator, projective_correlation,
    SOS.chsh, projectiveAlice, projectiveBob, tensor_add_right, tensor_sub_right,
    map_add, map_sub, map_smul, smul_eq_mul, Matrix.cons_val_zero, Matrix.cons_val_one]
  simp only [Strategy.behavior, ProjectiveStrategy.toStrategy, born_eq_expectation]
  ring

theorem binary_effect_complement (N : POVM 2) : N.effect 0 = 1 - N.effect 1 := by
  apply eq_sub_iff_add_eq.mpr
  simpa [Fin.sum_univ_succ] using N.normalized

theorem auxiliary_complement_of_zero1 (M : POVM 3) (hz : M.effect 1 = 0) :
    M.effect 2 = 1 - M.effect 0 := by
  apply eq_sub_iff_add_eq.mpr
  have h := M.normalized
  rw [add_comm]
  simpa [Fin.sum_univ_succ, hz] using h

theorem auxiliary_complement_of_zero0 (M : POVM 3) (hz : M.effect 0 = 0) :
    M.effect 2 = 1 - M.effect 1 := by
  apply eq_sub_iff_add_eq.mpr
  have h := M.normalized
  rw [add_comm]
  simpa [Fin.sum_univ_succ, hz] using h

theorem auxiliary_complement_of_zero2 (M : POVM 3) (hz : M.effect 2 = 0) :
    M.effect 1 = 1 - M.effect 0 := by
  apply eq_sub_iff_add_eq.mpr
  have h := M.normalized
  rw [add_comm]
  simpa [Fin.sum_univ_succ, hz] using h

set_option maxHeartbeats 0 in
/-- Every {0,2}-supported auxiliary PVM has the certified operator form. -/
theorem physical_bell_zero1 (s : ProjectiveStrategy separatorArchitecture)
    (hz : (s.alice 2).effect 1 = 0) :
    physicalBellOperator s = SOS.bell02 (projectiveAlice s 0) (projectiveBob s) := by
  have hm := auxiliary_complement_of_zero1 (s.alice 2).toPOVM hz
  have hb0 := binary_effect_complement (s.bob 0).toPOVM
  have hb1 := binary_effect_complement (s.bob 1).toPOVM
  norm_num [physicalBellOperator, SOS.bell02, SOS.chsh, projectiveAlice, projectiveBob,
    pvmSignObservable_matrix, projectionInvolution, Matrix.cons_val_two, hz, hm, hb0, hb1]
  ext i j
  norm_num [Matrix.add_apply, Matrix.sub_apply, Matrix.smul_apply,
    Pi.smul_apply, Complex.real_smul]
  ring

set_option maxHeartbeats 0 in
/-- Every {0,1}-supported auxiliary PVM has the short-SOS operator form. -/
theorem physical_bell_zero2 (s : ProjectiveStrategy separatorArchitecture)
    (hz : (s.alice 2).effect 2 = 0) :
    physicalBellOperator s = SOS.bell01 (projectiveAlice s 0) (projectiveBob s) := by
  have hm := auxiliary_complement_of_zero2 (s.alice 2).toPOVM hz
  have hb0 := binary_effect_complement (s.bob 0).toPOVM
  norm_num [physicalBellOperator, SOS.bell01, SOS.chsh, projectiveAlice, projectiveBob,
    pvmSignObservable_matrix, projectionInvolution, Matrix.cons_val_two, hz, hm, hb0]
  ext i j
  norm_num [Matrix.add_apply, Matrix.sub_apply, Matrix.smul_apply,
    Pi.smul_apply, Complex.real_smul]
  ring

set_option maxHeartbeats 0 in
/-- Every {1,2}-supported auxiliary PVM is handled by the explicit CHSH switch. -/
theorem physical_bell_zero0 (s : ProjectiveStrategy separatorArchitecture)
    (hz : (s.alice 2).effect 0 = 0) :
    physicalBellOperator s = SOS.bell02
      (SOS.switchedAlice (projectiveAlice s 1)) (SOS.switchedBob (projectiveBob s)) := by
  have hm := auxiliary_complement_of_zero0 (s.alice 2).toPOVM hz
  have hb0 := binary_effect_complement (s.bob 0).toPOVM
  have hb1 := binary_effect_complement (s.bob 1).toPOVM
  norm_num [physicalBellOperator, SOS.bell02, SOS.chsh, SOS.switchedAlice, SOS.switchedBob,
    projectiveAlice, projectiveBob, pvmSignObservable_matrix, projectionInvolution,
    QubitInvolution.neg, Matrix.cons_val_two, hz, hm, hb0, hb1]
  ext i j
  norm_num [Matrix.add_apply, Matrix.sub_apply, Matrix.smul_apply,
    Pi.smul_apply, Complex.real_smul]
  ring

/-- The full physical upper bound, with every ternary support and degeneracy covered. -/
theorem projective_strategy_rational_upper (s : ProjectiveStrategy separatorArchitecture) :
    bellScore s.toStrategy.behavior ≤ 289/10 := by
  rw [physical_bell_expectation]
  rcases ternary_pvm_has_zero (s.alice 2) with h0 | h1 | h2
  · rw [physical_bell_zero0 s h0]
    exact SOS.bell02_upper s.state _ _
  · rw [physical_bell_zero1 s h1]
    exact SOS.bell02_upper s.state _ _
  · rw [physical_bell_zero2 s h2]
    exact SOS.bell01_upper s.state _ _

/-- Raw-strategy quantification, not a stand-in scalar feasible region. -/
theorem raw_projective_rational_upper :
    ∀ p ∈ rawPVM separatorArchitecture, bellScore p ≤ 289/10 := by
  rintro p ⟨s,rfl⟩
  exact projective_strategy_rational_upper s

theorem sqrtTwo_rational_lower : (707/500 : ℝ) < sqrtTwo := by
  by_contra hn
  have hu : sqrtTwo ≤ 707/500 := le_of_not_gt hn
  have hp := mul_nonneg (sub_nonneg.mpr hu) (le_of_lt sqrtTwo_pos)
  nlinarith [sqrtTwo_sq]

theorem rational_bound_lt_paper_upper : (289/10 : ℝ) < upper := by
  unfold upper
  nlinarith [sqrtTwo_rational_lower]

theorem rational_bound_lt_witness : (289/10 : ℝ) < lower := by
  unfold lower
  nlinarith [sqrtTwo_rational_lower]

/-- The original target proposition is now supplied without an assumed upper bound. -/
theorem projective_global_upper_bound : ProjectiveGlobalUpperBound := by
  intro p hp
  exact le_trans (raw_projective_rational_upper p hp) (le_of_lt rational_bound_lt_paper_upper)

theorem convex_projective_rational_upper :
    ∀ p ∈ convexPVM separatorArchitecture, bellScore p ≤ 289/10 :=
  linear_bound_on_convexHull bellLinear (rawPVM separatorArchitecture) (289/10)
    raw_projective_rational_upper

/-- Unconditional proof-source statement of the paper's 3-by-2 separation. -/
theorem three_by_two_separation : StrictSeparation separatorArchitecture := by
  refine ⟨bellLinear,witnessBehavior,witness_mem_convex,?_⟩
  intro q hq
  change bellScore q < bellScore witnessBehavior
  rw [witness_value]
  exact lt_of_le_of_lt (convex_projective_rational_upper q hq) rational_bound_lt_witness

/-- A certified margin strictly greater than 1/50; no exact-optimum claim. -/
theorem witness_margin_over_projective (q : Behavior separatorArchitecture)
    (hq : q ∈ convexPVM separatorArchitecture) :
    (1/50 : ℝ) < bellScore witnessBehavior - bellScore q := by
  rw [witness_value]
  unfold lower
  have hu := convex_projective_rational_upper q hq
  nlinarith [sqrtTwo_rational_lower]

end Bell
