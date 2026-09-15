import CyclicBell.FirstSOS
import CyclicBell.SecondSOS

/-!
Unconditional physical upper-bound candidates. The domains here are the
original `State`, `PVM`, and `Strategy` structures, not a surrogate strategy
class assuming a norm bound, a maximum, or an equality-phase spectrum.
Both nA and nB remain arbitrary. Mixed states are handled directly by traces.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell
set_option maxRecDepth 20000
set_option maxHeartbeats 12000000

variable {nA nB : ℕ}

def firstA₀ (σ : Strategy 2 nA nB) : JointOp nA nB :=
  liftAlice nB (observable (σ.alice 0))
def firstA₁ (σ : Strategy 2 nA nB) : JointOp nA nB :=
  liftAlice nB (observable (σ.alice 1))
def firstU (σ : Strategy 2 nA nB) : JointOp nA nB :=
  (firstA₀ σ).conjTranspose * firstA₁ σ
def firstB (σ : Strategy 2 nA nB) (y : Fin 4) : JointOp nA nB :=
  liftBob nA (observable (σ.bob (reducedBob y)))
def firstBstar (σ : Strategy 2 nA nB) : JointOp nA nB :=
  liftBob nA (observable (σ.bob 4))

theorem firstA₀_unitary (σ : Strategy 2 nA nB) : UnitaryRel (firstA₀ σ) :=
  tensor_unitary (observable_unitary _) UnitaryRel.one

theorem firstA₁_unitary (σ : Strategy 2 nA nB) : UnitaryRel (firstA₁ σ) :=
  tensor_unitary (observable_unitary _) UnitaryRel.one

theorem firstU_unitary (σ : Strategy 2 nA nB) : UnitaryRel (firstU σ) :=
  (firstA₀_unitary σ).adjoint.mul (firstA₁_unitary σ)

theorem firstB_unitary (σ : Strategy 2 nA nB) (y : Fin 4) : UnitaryRel (firstB σ y) :=
  tensor_unitary UnitaryRel.one (observable_unitary _)

theorem firstBstar_unitary (σ : Strategy 2 nA nB) : UnitaryRel (firstBstar σ) :=
  tensor_unitary UnitaryRel.one (observable_unitary _)

theorem first_cross_commutation (σ : Strategy 2 nA nB) (y : Fin 4) :
    firstU σ * firstB σ y = firstB σ y * firstU σ := by
  simp [firstU, firstA₀, firstA₁, firstB, liftAlice, liftBob, tensor_mul]

theorem first_raw_term_bridge (σ : Strategy 2 nA nB) (y : Fin 4) :
    FirstSOS.rawTerm (firstA₀ σ) (firstU σ) (firstB σ) y =
      tensor (observable (σ.alice 0) + Complex.I ^ y.val • observable (σ.alice 1))
        (observable (σ.bob (reducedBob y))) := by
  have hA := firstA₀_unitary σ
  unfold FirstSOS.rawTerm firstU rotated
  rw [mul_add, mul_one, mul_smul_comm]
  rw [hA.cancel_right]
  simp [firstA₀, firstA₁, firstB, liftAlice, liftBob, tensor_mul,
    add_mul, smul_mul_assoc]

theorem first_reduced_value_bridge (σ : Strategy 2 nA nB) :
    firstReducedValue σ = stateEval σ.state.density
      (FirstSOS.reducedOperator (firstA₀ σ) (firstU σ) (firstB σ)) := by
  unfold firstReducedValue FirstSOS.reducedOperator
  rw [stateEval_sum]
  apply Finset.sum_congr rfl
  intro y _
  rw [stateEval_herm _ _ σ.state.positive.1, first_raw_term_bridge]
  rfl

theorem first_augmented_value_bridge (σ : Strategy 2 nA nB) :
    firstAugmentedValue σ =
      stateEval σ.state.density (FirstSOS.reducedOperator (firstA₀ σ) (firstU σ) (firstB σ)) +
      stateEval σ.state.density (firstA₀ σ * firstBstar σ) := by
  rw [firstAugmentedValue, first_reduced_value_bridge]
  simp only [firstA₀, firstBstar, liftAlice_mul_liftBob]
  rfl

/-- The new first-family d=4 SOS instantiated in the physical tensor model. -/
theorem first_physical_sos (σ : Strategy 2 nA nB) :
    (firstTargetValue : ℂ) • (1 : JointOp nA nB) -
      (FirstSOS.reducedOperator (firstA₀ σ) (firstU σ) (firstB σ) +
        herm (firstA₀ σ * firstBstar σ)) =
      ((D4.s / 2 : ℝ) : ℂ) • FirstSOS.squareSum (firstA₀ σ) (firstU σ) (firstB σ) +
      (1 / 2 : ℂ) • ((1 - firstA₀ σ * firstBstar σ).conjTranspose *
        (1 - firstA₀ σ * firstBstar σ)) := by
  have he := FirstSOS.augmented_gap_identity (firstA₀_unitary σ) (firstU_unitary σ)
    (firstB σ) (firstB_unitary σ) (first_cross_commutation σ) (firstBstar_unitary σ)
  simpa only [FirstSOS.M_eq, firstTargetValue] using he

/-- Target A, with arbitrary mixed states and arbitrary finite local dimensions.
No positivity hypotheses on dimensions are needed by the algebra itself. -/
theorem first_universal_upper (σ : Strategy 2 nA nB) :
    firstAugmentedValue σ ≤ firstTargetValue := by
  rw [first_augmented_value_bridge]
  exact FirstSOS.augmented_upper σ.state.positive σ.state.normalized
    (firstA₀_unitary σ) (firstU_unitary σ) (firstB σ) (firstB_unitary σ)
    (first_cross_commutation σ) (firstBstar_unitary σ)

theorem first_upper_bound : FirstUpperBound := by
  intro nA nB _ _ σ
  exact first_universal_upper σ

/-! Second-family physical bridge. -/

def secondA (σ : Strategy 4 nA nB) (l : Fin 4) : JointOp nA nB :=
  liftAlice nB (observable (σ.alice l))
def secondB (σ : Strategy 4 nA nB) (y : Fin 4) : JointOp nA nB :=
  liftBob nA (observable (σ.bob (reducedBob y)))
def secondBstar (σ : Strategy 4 nA nB) : JointOp nA nB :=
  liftBob nA (observable (σ.bob 4))

theorem secondA_unitary (σ : Strategy 4 nA nB) (l : Fin 4) :
    UnitaryRel (secondA σ l) := tensor_unitary (observable_unitary _) UnitaryRel.one

theorem secondB_unitary (σ : Strategy 4 nA nB) (y : Fin 4) :
    UnitaryRel (secondB σ y) := tensor_unitary UnitaryRel.one (observable_unitary _)

theorem secondBstar_unitary (σ : Strategy 4 nA nB) :
    UnitaryRel (secondBstar σ) := tensor_unitary UnitaryRel.one (observable_unitary _)

theorem second_fourier_lift (σ : Strategy 4 nA nB) (l : Fin 4) :
    fourier4 (secondB σ) l = liftBob nA (bobFourier σ l) := by
  apply Matrix.ext
  intro i j
  simp only [fourier4, secondB, liftBob, bobFourier, tensor, Matrix.sum_apply, Finset.sum_apply,
    Matrix.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro y _
  ring

theorem second_reduced_value_bridge (σ : Strategy 4 nA nB) :
    secondReducedValue σ = stateEval σ.state.density
      (SecondSOS.reducedOperator sourceLambda (secondA σ) (secondB σ)) := by
  unfold secondReducedValue SecondSOS.reducedOperator
  rw [stateEval_sum]
  apply Finset.sum_congr rfl
  intro l _
  rw [stateEval_herm _ _ σ.state.positive.1, second_fourier_lift]
  simp only [secondA, liftAlice_mul_liftBob]
  rfl

theorem second_augmented_value_bridge (σ : Strategy 4 nA nB) :
    secondAugmentedValue σ = stateEval σ.state.density
      (SecondSOS.reducedOperator sourceLambda (secondA σ) (secondB σ)) +
      stateEval σ.state.density (secondA σ 0 * secondBstar σ) := by
  rw [secondAugmentedValue, second_reduced_value_bridge]
  simp only [secondA, secondBstar, liftAlice_mul_liftBob]
  rfl

/-- The actual second-family operator gap in the physical tensor model. -/
theorem second_physical_sos (σ : Strategy 4 nA nB) :
    (5 : ℂ) • (1 : JointOp nA nB) -
      (SecondSOS.reducedOperator sourceLambda (secondA σ) (secondB σ) +
        herm (secondA σ 0 * secondBstar σ)) =
      (1 / 8 : ℂ) • SecondSOS.squareSum sourceLambda (secondA σ) (secondB σ) +
      (1 / 2 : ℂ) • ((1 - secondA σ 0 * secondBstar σ).conjTranspose *
        (1 - secondA σ 0 * secondBstar σ)) := by
  apply SecondSOS.augmented_gap_identity _ _ _ _ _
    (secondA_unitary σ) (secondB_unitary σ) (secondBstar_unitary σ)
  simp only [D4.sourceLambda_eq]
  exact D4.lambda_normalization

/-- Target F's universal part, with the actual source coefficients. -/
theorem second_universal_upper (σ : Strategy 4 nA nB) :
    secondAugmentedValue σ ≤ 5 := by
  rw [second_augmented_value_bridge]
  apply SecondSOS.augmented_upper σ.state.positive σ.state.normalized sourceLambda _
    (secondA σ) (secondB σ) (secondBstar σ) (secondA_unitary σ)
    (secondB_unitary σ) (secondBstar_unitary σ)
  simp only [D4.sourceLambda_eq]
  exact D4.lambda_normalization

theorem second_upper_bound : SecondUpperBound := by
  intro nA nB _ _ σ
  exact second_universal_upper σ

end CyclicBell
