import Bell.DeterministicGap
import Bell.DeterministicInput
import Bell.IncidenceAlgebra
import Bell.RankZeroSimulation

/-!
# From incidence coefficient actions to physical deterministic replacements

The table is the complete labelled 2-by-2 table, including the unused third
binary label. Its definition is a real-linear map of the actual probability
block. Resetting a coefficient input is identified entry by entry with the
physical deterministic measurement replacement.

The resulting multiplier theorem no longer assumes strict deterministic gaps:
it derives them from membership of the physical replacements in the PVM hull.
Incidence stationarity and the coordinate representation remain explicit inputs
until they are derived by the subsequent reduction and calculus modules.
-/
noncomputable section
open scoped BigOperators Matrix
namespace Bell.Lorentz

/-- Recover all declared probabilities from the four-by-four block. -/
def tableOfBlock : M →ₗ[ℝ] Behavior binaryTernaryArchitecture where
  toFun := fun P x y a b => matrixPair P (effectRay x a) (effectRay y b)
  map_add' := by intro P Q; funext x y a b; simp
  map_smul' := by intro t P; funext x y a b; simp

@[simp]
theorem tableOfBlock_apply (P : M) (x y : Fin 2) (a b : Fin 3) :
    tableOfBlock P x y a b = matrixPair P (effectRay x a) (effectRay y b) := rfl

/-- Coefficient action on the entire block, not on one observed marginal. -/
def actedBlock (P : M) : Endomorphism →ₗ[ℝ] M where
  toFun := fun W => P * matrixOfLinear W
  map_add' := by intro W Z; simp [Matrix.mul_add]
  map_smul' := by intro t W; simp [Matrix.mul_smul]

@[simp]
theorem actedBlock_mulVec (P : M) (W : Endomorphism) (x : V) :
    actedBlock P W *ᵥ x = P *ᵥ W x := by
  simp [actedBlock, Matrix.mulVec_mulVec, matrixOfLinear_mulVec]

@[simp]
theorem actedBlock_id (P : M) : actedBlock P LinearMap.id = P := by
  simp [actedBlock]

def actedTable (P : M) : Endomorphism →ₗ[ℝ] Behavior binaryTernaryArchitecture :=
  tableOfBlock.comp (actedBlock P)

@[simp]
theorem actedTable_apply (P : M) (W : Endomorphism) (x y : Fin 2) (a b : Fin 3) :
    actedTable P W x y a b = matrixPair P (effectRay x a) (W (effectRay y b)) := by
  simp [actedTable, matrixPair]

theorem sum_effectRay (y : Fin 2) : (∑ b : Fin 3, effectRay y b) = unitVector := by
  fin_cases y <;> funext i <;> fin_cases i <;>
    norm_num [effectRay, ray, unitVector, Fin.sum_univ_succ]

theorem tableOfBlock_bob_marginal (P : M) (x y : Fin 2) (a : Fin 3) :
    (∑ b : Fin 3, tableOfBlock P x y a b) = matrixPair P (effectRay x a) unitVector := by
  simp only [tableOfBlock_apply, ← map_sum, sum_effectRay]

/-- Explicit action on every declared effect, including the zero label. -/
theorem reset_effectRay (j : Fin 5) (y : Fin 2) (b : Fin 3) :
    DeterministicGap.reset j (effectRay y b) =
      if y = rayInput j then (if b = rayLabel j then unitVector else 0)
      else effectRay y b := by
  fin_cases j <;> fin_cases y <;> fin_cases b <;>
    funext i <;> fin_cases i <;>
    norm_num [DeterministicGap.reset, effectRay, ray, unitVector, rayInput, rayLabel]

theorem actedTable_reset (P : M) (j : Fin 5) (x y : Fin 2) (a b : Fin 3) :
    actedTable P (DeterministicGap.reset j) x y a b =
      if y = rayInput j then
        (∑ c : Fin 3, tableOfBlock P x (otherInput (rayInput j)) a c) *
          (if b = rayLabel j then 1 else 0)
      else tableOfBlock P x (otherInput (rayInput j)) a b := by
  rw [actedTable_apply, reset_effectRay, tableOfBlock_bob_marginal]
  by_cases hy : y = rayInput j
  · by_cases hb : b = rayLabel j <;> simp [hy, hb]
  · have ho := eq_otherInput_of_ne (rayInput j) y hy
    simp [hy, ho]

theorem actedTable_reset_physical (s : Strategy binaryTernaryArchitecture) (P : M)
    (represented : s.behavior = tableOfBlock P) (j : Fin 5) :
    actedTable P (DeterministicGap.reset j) = (replaceBobRay s j).behavior := by
  funext x y a b
  rw [actedTable_reset]
  change _ = (replaceBobInput s (rayInput j) (rayLabel j)).behavior x y a b
  rw [replacement_behavior, represented]

/-- A normalization covector for the W-coordinate stationarity equation. -/
def blockUnitCovector (P : M) : V →ₗ[ℝ] ℝ := matrixPair P unitVector

@[simp]
theorem blockMass_actedBlock (P : M) (W : Endomorphism) :
    blockMass (actedBlock P W) = blockUnitCovector P (W unitVector) := by
  simp [blockMass, blockUnitCovector, matrixPair]

theorem weightedPairing_actedBlock (G Y : M) (λ : Fin 5 → ℝ) (W : Endomorphism) :
    weightedPairing λ Y (actedBlock (G * Y) W) =
      compatibility (pullbackForm G (linearOfMatrix Y)) λ W := by
  simp [weightedPairing, compatibility, pullbackForm, matrixPair,
    Matrix.mulVec_mulVec]

/-- The positivity implication now has a genuine physical source for its
strict-gap premise. No local-POVM duality theorem is used. -/
theorem multipliers_positive_from_physical_separator
    (s : Strategy binaryTernaryArchitecture) (G Y : M)
    (represented : s.behavior = tableOfBlock (G * Y))
    (λ : Fin 5 → ℝ) (α : ℝ)
    (hnull : ∀ j, matrixPair G (Y *ᵥ ray j) (Y *ᵥ ray j) = 0)
    (hfuture : ∀ j, 0 < matrixPair G (Y *ᵥ ray j) (Y *ᵥ unitVector))
    (f : Behavior binaryTernaryArchitecture →ₗ[ℝ] ℝ)
    (stationary : ∀ P, f (tableOfBlock P) =
      α * blockMass P - 2 * weightedPairing λ Y P)
    (strictSeparator : ∀ p ∈ convexPVM binaryTernaryArchitecture, f p < f s.behavior) :
    ∀ j, 0 < λ j := by
  let B := pullbackForm G (linearOfMatrix Y)
  let F := f.comp (actedTable (G * Y))
  apply DeterministicGap.multipliers_positive B λ hnull hfuture F
    (blockUnitCovector (G * Y)) α
  · intro W
    change f (tableOfBlock (actedBlock (G * Y) W)) = _
    rw [stationary, blockMass_actedBlock, weightedPairing_actedBlock]
  · intro j
    change f (actedTable (G * Y) (DeterministicGap.reset j)) <
      f (actedTable (G * Y) LinearMap.id)
    rw [actedTable_reset_physical s (G * Y) represented j]
    simpa only [actedTable, LinearMap.comp_apply, actedBlock_id, ← represented] using
      strict_gap_to_deterministic_replacements s f strictSeparator j

/-- The block convention agrees with the earlier labelled rank-zero simulator. -/
theorem tableOfBlock_eq_transformedMetricTable (g : StrictParameters) (T : V ≃ₗ[ℝ] V) :
    tableOfBlock (metric g.a g.b g.c g.d * matrixOfLinear T.toLinearMap) =
      transformedMetricTable g T := by
  funext x y a b
  simp [tableOfBlock, transformedMetricTable, matrixPair,
    Matrix.mulVec_mulVec, matrixOfLinear_mulVec]

end Bell.Lorentz
