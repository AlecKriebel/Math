import CyclicBell.Cycle4
import CyclicBell.Fourier4

/-!
Complete finite-dimensional witness, with every PVM constructed from an
orthonormal basis. ζ is the actual complex exponential defined in Phases;
it is not an abstract root satisfying unproved certificate equations.

The target PVMs are deliberately the identical objects used by D4.targetBorn.
Other measurements are supplied by the proved weighted-cycle PVM constructor.
There are no score or maximality assumptions in any constructor.

UNCOMPILED SOURCE: acceptance and dependency reports require the offline run.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.D4
attribute [local simp] Matrix.cons_val_two Matrix.cons_val_three Matrix.cons_val_four
set_option maxRecDepth 20000
set_option maxHeartbeats 16000000

/-- Second-family Alice weights, including first-family settings 0 and 1. -/
def aliceExponents : Fin 4 → Fin 4 → ℕ :=
  !![0,0,0,0; 2,6,14,10; 8,0,0,8; 2,14,6,10]

/-- Exponents of the polar V_y, BEFORE entrywise conjugation. -/
def polarExponents : Fin 4 → Fin 4 → ℕ :=
  !![1,3,15,13; 3,13,1,15; 13,15,3,1; 15,1,13,3]

/-- Bob weights are conjugates of the polar weights, not their adjoints. -/
def bobExponents : Fin 4 → Fin 4 → ℕ :=
  !![15,13,1,3; 13,3,15,1; 3,1,13,15; 1,15,3,13]

def aliceWeights (l j : Fin 4) : ℂ := zeta ^ aliceExponents l j
def bobWeights (y j : Fin 4) : ℂ := zeta ^ bobExponents y j

def witnessA (l : Fin 4) : Op 4 := weighted (aliceWeights l)
def witnessB (y : Fin 4) : Op 4 := weighted (bobWeights y)

theorem aliceWeights_unit (l j : Fin 4) :
    star (aliceWeights l j) * aliceWeights l j = 1 := zeta_pow_unit _

theorem bobWeights_unit (y j : Fin 4) :
    star (bobWeights y j) * bobWeights y j = 1 := zeta_pow_unit _

theorem zeta_pow_32 : zeta ^ 32 = 1 := by
  rw [show (32 : ℕ) = 16 * 2 by decide, pow_mul, zeta_sixteen]
  norm_num

theorem aliceWeights_product (l : Fin 4) :
    aliceWeights l 0 * aliceWeights l 1 * aliceWeights l 2 * aliceWeights l 3 = 1 := by
  change zeta ^ aliceExponents l 0 * zeta ^ aliceExponents l 1 *
    zeta ^ aliceExponents l 2 * zeta ^ aliceExponents l 3 = 1
  rw [← pow_add, ← pow_add, ← pow_add]
  fin_cases l <;> norm_num [aliceExponents, zeta_sixteen, zeta_pow_32]

theorem bobWeights_product (y : Fin 4) :
    bobWeights y 0 * bobWeights y 1 * bobWeights y 2 * bobWeights y 3 = 1 := by
  change zeta ^ bobExponents y 0 * zeta ^ bobExponents y 1 *
    zeta ^ bobExponents y 2 * zeta ^ bobExponents y 3 = 1
  rw [← pow_add, ← pow_add, ← pow_add]
  fin_cases y <;> norm_num [bobExponents, zeta_pow_32]

def aliceCyclePVM (l : Fin 4) : PVM 4 :=
  cyclePVM (aliceWeights l) (aliceWeights_unit l) (aliceWeights_product l)
def bobCyclePVM (y : Fin 4) : PVM 4 :=
  cyclePVM (bobWeights y) (bobWeights_unit y) (bobWeights_product y)

theorem aliceCycle_encoding (l : Fin 4) : observable (aliceCyclePVM l) = witnessA l :=
  cyclePVM_encoding _ _ _
theorem bobCycle_encoding (y : Fin 4) : observable (bobCyclePVM y) = witnessB y :=
  cyclePVM_encoding _ _ _

theorem weighted_one : weighted (fun _ => 1) = shift := by
  simp [weighted]

theorem witnessA_zero : witnessA 0 = shift := by
  change weighted (aliceWeights 0) = shift
  have he : aliceWeights 0 = fun _ => 1 := by funext j; fin_cases j <;> norm_num [aliceWeights, aliceExponents]
  rw [he, weighted_one]

theorem witnessA_one : witnessA 1 = swappedObservable := by
  change weighted (aliceWeights 1) = weighted swappedWeights
  apply congrArg weighted
  funext j
  simpa [aliceWeights, aliceExponents] using (old_weights_phase_bridge j).symm

/-- Alice has four PVMs in family F, and the first two are the same in family I. -/
def secondAlicePVM : Fin 4 → PVM 4 :=
  ![bobTargetPVM, aliceTargetPVM, aliceCyclePVM 2, aliceCyclePVM 3]
def firstAlicePVM : Fin 2 → PVM 4 := ![bobTargetPVM, aliceTargetPVM]
def allBobPVM : Fin 5 → PVM 4 :=
  ![bobCyclePVM 0, bobCyclePVM 1, bobCyclePVM 2, bobCyclePVM 3, bobTargetPVM]

def firstStrategy : Strategy 2 4 4 where
  state := targetState
  alice := firstAlicePVM
  bob := allBobPVM

def secondStrategy : Strategy 4 4 4 where
  state := targetState
  alice := secondAlicePVM
  bob := allBobPVM

theorem secondAlice_encoding (l : Fin 4) :
    observable (secondStrategy.alice l) = witnessA l := by
  fin_cases l
  · simpa [secondStrategy, secondAlicePVM, witnessA_zero] using bob_encoding
  · simpa [secondStrategy, secondAlicePVM, witnessA_one] using alice_encoding
  · exact aliceCycle_encoding 2
  · exact aliceCycle_encoding 3

theorem firstAlice_zero_encoding : observable (firstStrategy.alice 0) = witnessA 0 := by
  simpa [firstStrategy, firstAlicePVM, witnessA_zero] using bob_encoding

theorem firstAlice_one_encoding : observable (firstStrategy.alice 1) = witnessA 1 := by
  simpa [firstStrategy, firstAlicePVM, witnessA_one] using alice_encoding

theorem allBob_reduced_encoding (y : Fin 4) :
    observable (allBobPVM (reducedBob y)) = witnessB y := by
  fin_cases y
  · simpa [allBobPVM, reducedBob] using bobCycle_encoding 0
  · simpa [allBobPVM, reducedBob] using bobCycle_encoding 1
  · simpa [allBobPVM, reducedBob] using bobCycle_encoding 2
  · simpa [allBobPVM, reducedBob] using bobCycle_encoding 3

theorem firstBob_encoding (y : Fin 4) :
    observable (firstStrategy.bob (reducedBob y)) = witnessB y := allBob_reduced_encoding y

theorem secondBob_encoding (y : Fin 4) :
    observable (secondStrategy.bob (reducedBob y)) = witnessB y := allBob_reduced_encoding y

theorem firstBob_added_encoding : observable (firstStrategy.bob 4) = shift := bob_encoding

theorem secondBob_added_encoding : observable (secondStrategy.bob 4) = shift := bob_encoding

theorem witnessA_unitary (l : Fin 4) : UnitaryRel (witnessA l) :=
  weighted_unitary _ (aliceWeights_unit l) (aliceWeights_product l)

theorem witnessB_unitary (y : Fin 4) : UnitaryRel (witnessB y) :=
  weighted_unitary _ (bobWeights_unit y) (bobWeights_product y)

theorem witnessA_fourth (l : Fin 4) : witnessA l ^ 4 = 1 :=
  weighted_fourth_power _ (aliceWeights_unit l) (aliceWeights_product l)

theorem witnessB_fourth (y : Fin 4) : witnessB y ^ 4 = 1 :=
  weighted_fourth_power _ (bobWeights_unit y) (bobWeights_product y)

theorem shift_unitary : UnitaryRel shift := by
  rw [← bob_encoding]
  exact observable_unitary _

theorem shift_conjugate : entryConj shift = shift := by
  ext i j
  simp [entryConj, shift_entry]

/-! Explicit source-convention bridges. -/

theorem root_product_with_polar (y j : Fin 4) :
    bobWeights y j * zeta ^ polarExponents y j = 1 := by
  unfold bobWeights
  rw [← pow_add]
  fin_cases y <;> fin_cases j <;> norm_num [bobExponents, polarExponents]

theorem bobWeights_are_polar_conjugates (y j : Fin 4) :
    bobWeights y j = star (zeta ^ polarExponents y j) := by
  apply mul_right_cancel₀ (pow_ne_zero _ zeta_ne_zero)
  rw [root_product_with_polar, zeta_pow_unit]

theorem bob_manuscript_bridge (y : Fin 4) :
    witnessB y = entryConj (weighted (fun j => zeta ^ polarExponents y j)) := by
  rw [weighted_conjugate]
  change weighted (bobWeights y) = weighted _
  apply congrArg weighted
  funext j
  exact bobWeights_are_polar_conjugates y j

/-- Source's η and its exact d=4 D_l, with integer exponents. -/
def eta : ℂ := Complex.exp (((Real.pi / 4 : ℝ) : ℂ) * Complex.I)
def sourceD (l : Fin 4) : Op 4 :=
  (eta ^ (-((l.val : ℤ) * (l.val : ℤ)))) •
    weighted (fun j => Complex.I ^ (-((l.val : ℤ) * ((kappa j).val : ℤ))))

theorem inv_eq_star_of_unit {z : ℂ} (hz : star z * z = 1) : z⁻¹ = star z := by
  have hn : z ≠ 0 := by intro hzero; simp [hzero] at hz
  apply mul_right_cancel₀ hn
  rw [inv_mul_cancel₀ hn, hz]

theorem eta_unit : star eta * eta = 1 := by
  change star (Complex.exp _) * Complex.exp _ = 1
  rw [eta_bridge]
  exact zeta_pow_unit 2

theorem star_neg_power {z : ℂ} (hz : star z * z = 1) (m : ℕ) :
    star (z ^ (-(m : ℤ))) = z ^ m := by
  have hp : star (z ^ m) * z ^ m = 1 := by
    rw [star_pow, ← mul_pow, hz, one_pow]
  rw [zpow_neg, zpow_natCast, inv_eq_star_of_unit hp, star_star]

/-- The matrix named D_l in eq:second-A is conjugated, not adjointed. -/
theorem secondAlice_manuscript_bridge (l : Fin 4) : witnessA l = entryConj (sourceD l) := by
  have hI : star Complex.I * Complex.I = 1 := by norm_num
  apply Matrix.ext
  intro i j
  simp only [witnessA, weighted_entry, entryConj, sourceD, Matrix.smul_apply,
    smul_eq_mul, star_mul]
  have hshift : star (shift i j) = shift i j := by simp [shift_entry]
  rw [hshift]
  have he : star (eta ^ (-((l.val : ℤ) * (l.val : ℤ)))) = eta ^ (l.val * l.val) := by
    have hcast : (l.val : ℤ) * (l.val : ℤ) = ((l.val * l.val : ℕ) : ℤ) := by norm_cast
    rw [hcast, star_neg_power eta_unit]
  have hi : star (Complex.I ^ (-((l.val : ℤ) * ((kappa j).val : ℤ)))) =
      Complex.I ^ (l.val * (kappa j).val) := by
    have hcast : (l.val : ℤ) * ((kappa j).val : ℤ) = ((l.val * (kappa j).val : ℕ) : ℤ) := by norm_cast
    rw [hcast, star_neg_power hI]
  rw [he, hi]
  have hw : aliceWeights l j = eta ^ (l.val * l.val) * Complex.I ^ (l.val * (kappa j).val) := by
    rw [eta, eta_bridge, ← zeta_four]
    unfold aliceWeights
    simp only [← pow_mul, ← pow_add]
    conv_lhs => rw [zeta_pow_mod]
    conv_rhs => rw [zeta_pow_mod]
    congr 1
    fin_cases l <;> fin_cases j <;> decide
  rw [hw]
  ring

/-- Both physical strategies really share the same designated projectors. -/
theorem witness_target_projectors (a b : Fin 4) :
    (firstStrategy.alice 1).effect a = projector (v a) ∧
    (firstStrategy.bob 4).effect b = projector (u b) ∧
    (secondStrategy.alice 1).effect a = projector (v a) ∧
    (secondStrategy.bob 4).effect b = projector (u b) := by
  exact ⟨rfl, rfl, rfl, rfl⟩

/-- Endpoint B's complete validity data, without any attainment premise. -/
theorem complete_witness_validity :
    ip phi phi = 1 ∧
    firstStrategy.state.density.PosSemidef ∧ Matrix.trace firstStrategy.state.density = 1 ∧
    secondStrategy.state.density.PosSemidef ∧ Matrix.trace secondStrategy.state.density = 1 ∧
    (∀ x : Fin 2, (∑ a, (firstStrategy.alice x).effect a) = 1) ∧
    (∀ l : Fin 4, (∑ a, (secondStrategy.alice l).effect a) = 1) ∧
    (∀ y : Fin 5, (∑ b, (allBobPVM y).effect b) = 1) ∧
    (∀ l : Fin 4, UnitaryRel (witnessA l) ∧ witnessA l ^ 4 = 1) ∧
    (∀ y : Fin 4, UnitaryRel (witnessB y) ∧ witnessB y ^ 4 = 1) := by
  exact ⟨phi_normalized, firstStrategy.state.positive, firstStrategy.state.normalized,
    secondStrategy.state.positive, secondStrategy.state.normalized,
    fun x => (firstStrategy.alice x).complete,
    fun l => (secondStrategy.alice l).complete,
    fun y => (allBobPVM y).complete,
    fun l => ⟨witnessA_unitary l, witnessA_fourth l⟩,
    fun y => ⟨witnessB_unitary y, witnessB_fourth y⟩⟩

end CyclicBell.D4
