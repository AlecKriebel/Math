import Bell.UphillDirection

/-!
# Deterministic replacement and strict multiplier positivity

Reconstructed from the mathematical shortcut recorded in the prior conversation.
This is NEW source, not a recovered copy of a formerly missing module.

The conclusion is conditional on the explicitly displayed stationarity equation,
null incidence, positive state pairings, and strict score gaps. These hypotheses
are NOT asserted for all physical strategies here. No full two-input theorem is
claimed. This source has not been compiled in the present environment.
-/
noncomputable section
open scoped BigOperators Matrix
namespace Bell.Lorentz.DeterministicGap

/-- The input partition of the five coefficient rays. -/
def sameInput (i j : Fin 5) : Prop := (i.val < 2) ↔ (j.val < 2)

instance (i j : Fin 5) : Decidable (sameInput i j) := by
  unfold sameInput
  infer_instance

/-- Reset one complete input to its deterministic outcome j. -/
def reset (j : Fin 5) : Endomorphism where
  toFun := fun x =>
    if j = 0 then ![x 0, x 0, x 2, x 3]
    else if j = 1 then ![x 1, x 1, x 2, x 3]
    else if j = 2 then ![x 0 + x 2, x 1 + x 2, 0, 0]
    else if j = 3 then ![x 0 + x 3, x 1 + x 3, 0, 0]
    else ![x 0, x 1, 0, 0]
  map_add' := by
    intro x y
    fin_cases j <;> funext i <;> fin_cases i <;>
      simp [Matrix.cons_val, Pi.add_apply] <;> ring
  map_smul' := by
    intro t x
    fin_cases j <;> funext i <;> fin_cases i <;>
      simp [Matrix.cons_val, Pi.smul_apply, smul_eq_mul] <;> ring

theorem reset_ray (j k : Fin 5) :
    reset j (ray k) =
      if k = j then unitVector else if sameInput k j then 0 else ray k := by
  fin_cases j <;> fin_cases k <;> funext i <;> fin_cases i <;>
    simp [Matrix.cons_val, reset, sameInput, ray, unitVector]

theorem reset_unit (j : Fin 5) : reset j unitVector = unitVector := by
  fin_cases j <;> funext i <;> fin_cases i <;>
    simp [Matrix.cons_val, reset, unitVector]

theorem reset_idempotent (j : Fin 5) : (reset j).comp (reset j) = reset j := by
  apply LinearMap.ext
  intro x
  funext i
  fin_cases j <;> fin_cases i <;>
    simp [Matrix.cons_val, reset, LinearMap.comp_apply]

/-- Null unchanged rays leave precisely the selected outcome's contribution. -/
theorem compatibility_reset (B : Bilinear) (lam : Fin 5 → ℝ)
    (hnull : ∀ k, B (ray k) (ray k) = 0) (j : Fin 5) :
    compatibility B lam (reset j) = lam j * B (ray j) unitVector := by
  unfold compatibility
  rw [Finset.sum_eq_single j]
  · rw [reset_ray]
    simp
  · intro k _ hkj
    rw [reset_ray]
    by_cases hblock : sameInput k j
    · simp [hkj, hblock]
    · simp [hkj, hblock, hnull]
  · intro hj
    exact (hj (Finset.mem_univ j)).elim

theorem compatibility_id (B : Bilinear) (lam : Fin 5 → ℝ)
    (hnull : ∀ k, B (ray k) (ray k) = 0) :
    compatibility B lam LinearMap.id = 0 := by
  simp [compatibility, hnull]

/-- Exact gap identity with the sign of the paper's stationarity equation. -/
theorem stationary_gap (B : Bilinear) (lam : Fin 5 → ℝ)
    (hnull : ∀ k, B (ray k) (ray k) = 0)
    (F : Endomorphism →ₗ[ℝ] ℝ) (l : V →ₗ[ℝ] ℝ) (α : ℝ)
    (stationary : ∀ W, F W = α * l (W unitVector) - 2 * compatibility B lam W)
    (j : Fin 5) :
    F LinearMap.id - F (reset j) = 2 * lam j * B (ray j) unitVector := by
  rw [stationary LinearMap.id, stationary (reset j),
    compatibility_id B lam hnull, compatibility_reset B lam hnull,
    reset_unit, LinearMap.id_apply]
  ring

/-- Strict deterministic gaps and positive pairings force positive multipliers.
No semidefinite duality premise is used. Stationarity remains a premise. -/
theorem multipliers_positive (B : Bilinear) (lam : Fin 5 → ℝ)
    (hnull : ∀ k, B (ray k) (ray k) = 0)
    (hfuture : ∀ j, 0 < B (ray j) unitVector)
    (F : Endomorphism →ₗ[ℝ] ℝ) (l : V →ₗ[ℝ] ℝ) (α : ℝ)
    (stationary : ∀ W, F W = α * l (W unitVector) - 2 * compatibility B lam W)
    (strictGap : ∀ j, F (reset j) < F LinearMap.id) : ∀ j, 0 < lam j := by
  intro j
  have hpos : 0 < 2 * lam j * B (ray j) unitVector := by
    rw [← stationary_gap B lam hnull F l α stationary j]
    exact sub_pos.mpr (strictGap j)
  by_contra! hnonpos
  have hleft : 2 * lam j ≤ 0 := by linarith
  have hprod := mul_nonpos_of_nonpos_of_nonneg hleft (le_of_lt (hfuture j))
  linarith

/-- The individual multipliers can be recovered from the deterministic gaps. -/
theorem multiplier_formula (B : Bilinear) (lam : Fin 5 → ℝ)
    (hnull : ∀ k, B (ray k) (ray k) = 0)
    (F : Endomorphism →ₗ[ℝ] ℝ) (l : V →ₗ[ℝ] ℝ) (α : ℝ)
    (stationary : ∀ W, F W = α * l (W unitVector) - 2 * compatibility B lam W)
    (j : Fin 5) (hj : B (ray j) unitVector ≠ 0) :
    lam j = (F LinearMap.id - F (reset j)) / (2 * B (ray j) unitVector) := by
  apply (eq_div_iff (mul_ne_zero (by norm_num : (2 : ℝ) ≠ 0) hj)).2
  calc
    lam j * (2 * B (ray j) unitVector) = 2 * lam j * B (ray j) unitVector := by ring
    _ = F LinearMap.id - F (reset j) :=
      (stationary_gap B lam hnull F l α stationary j).symm

end Bell.Lorentz.DeterministicGap
