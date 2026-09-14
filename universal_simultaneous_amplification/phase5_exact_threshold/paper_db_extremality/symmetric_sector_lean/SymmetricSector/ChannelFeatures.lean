import SymmetricSector.PhysicalBridge

namespace SymmetricSector
noncomputable section
open Matrix
open scoped BigOperators

/-- The transpose of the good block, acting in the physical coefficient direction. -/
theorem phaseS_transpose_mulVec (N : ℕ) (v : Good N → ℚ) (i : Good N) :
    ((phaseS N)ᵀ *ᵥ v) i =
      ((i.val : ℚ) + 1) / (2 * N) * v i +
      ((N : ℚ) - i.val - 2) / (2 * N) * zeroExtend v ((i.val : ℤ) + 1) := by
  have he : ∀ j : Good N, (phaseS N)ᵀ i j * v j =
      (if (j.val : ℤ) = i.val then ((i.val : ℚ) + 1) / (2 * N) * v j else 0) +
      (if (j.val : ℤ) = (i.val : ℤ) + 1 then
        ((N : ℚ) - i.val - 2) / (2 * N) * v j else 0) := by
    intro j
    simp only [Matrix.transpose_apply, phaseS, coefficientK]
    split_ifs <;> try omega
    all_goals try { congr 1; congr 1 <;> ring }
  simp only [Matrix.mulVec, dotProduct, he, Finset.sum_add_distrib,
    sum_int_selector_mul, zeroExtend_at]

/-- The transpose of the coupling block, with the two correct neighboring
physical good coefficients and no out-of-range entries. -/
theorem phaseC_transpose_mulVec (N : ℕ) (v : Good N → ℚ) (i : Bad N) :
    ((phaseC N)ᵀ *ᵥ v) i =
      ((i.val : ℚ) + 1) / (2 * (i.val + 2) * N) * zeroExtend v i.val +
      ((N : ℚ) - i.val - 2) / (2 * (i.val + 2) * N) *
        zeroExtend v ((i.val : ℤ) + 1) := by
  have he : ∀ j : Good N, (phaseC N)ᵀ i j * v j =
      (if (j.val : ℤ) = i.val then
        ((i.val : ℚ) + 1) / (2 * (i.val + 2) * N) * v j else 0) +
      (if (j.val : ℤ) = (i.val : ℤ) + 1 then
        ((N : ℚ) - i.val - 2) / (2 * (i.val + 2) * N) * v j else 0) := by
    intro j
    simp only [Matrix.transpose_apply, phaseC, coefficientK]
    split_ifs <;> try omega
    all_goals try { congr 1; congr 1 <;> ring }
  simp only [Matrix.mulVec, dotProduct, he, Finset.sum_add_distrib,
    sum_int_selector_mul]

theorem coefficientK_good_action (N : ℕ) (c : Channel N → ℚ) (i : Good N) :
    (coefficientK N *ᵥ c) (.inl i) =
      ((i.val : ℚ) + 1) / (2 * N) * c (.inl i) +
      ((N : ℚ) - i.val - 2) / (2 * N) * zeroExtend (fun j => c (.inl j)) ((i.val : ℤ) + 1) -
      (1 / (N : ℚ)) * zeroExtend (fun j => c (.inr j)) i.val := by
  have hh : (coefficientK N *ᵥ c) (.inl i) =
      ((phaseS N)ᵀ *ᵥ (fun j => c (.inl j))) i -
        ((phaseD N)ᵀ *ᵥ (fun j => c (.inr j))) i := by
    simp only [Matrix.mulVec, dotProduct, Fintype.sum_sum_type,
      Matrix.transpose_apply, phaseS, phaseD, neg_mul, Finset.sum_neg_distrib, sub_neg_eq_add]
  rw [hh, phaseS_transpose_mulVec, phaseD_transpose_mulVec]

theorem coefficientK_bad_action (N : ℕ) (c : Channel N → ℚ) (i : Bad N) :
    (coefficientK N *ᵥ c) (.inr i) =
      ((i.val : ℚ) + 1) / (2 * (i.val + 2) * N) * zeroExtend (fun j => c (.inl j)) i.val +
      ((N : ℚ) - i.val - 2) / (2 * (i.val + 2) * N) *
        zeroExtend (fun j => c (.inl j)) ((i.val : ℤ) + 1) +
      (((N : ℚ) * i.val + i.val + 2) / (2 * (i.val + 2) * N) * c (.inr i) +
      ((i.val : ℚ) + 1) * i.val / (2 * (i.val + 2) * N) *
        zeroExtend (fun j => c (.inr j)) ((i.val : ℤ) - 1) +
      ((N : ℚ) - i.val - 4) / (2 * N) * zeroExtend (fun j => c (.inr j)) ((i.val : ℤ) + 1)) := by
  have hh : (coefficientK N *ᵥ c) (.inr i) =
      ((phaseC N)ᵀ *ᵥ (fun j => c (.inl j))) i +
        ((phaseQ N)ᵀ *ᵥ (fun j => c (.inr j))) i := by
    simp only [Matrix.mulVec, dotProduct, Fintype.sum_sum_type,
      Matrix.transpose_apply, phaseC, phaseQ]
  rw [hh, phaseC_transpose_mulVec, phaseQ_transpose_mulVec]

namespace Active

theorem coeffA_shift (N : ℕ) (c : Channel N → ℚ) (i : ℕ) :
    coeffA N c (i+1) = (zeroExtend (fun j => c (.inl j)) (i:ℤ) : ℝ) := by
  simp only [coeffA, goodAt, Nat.cast_add, Nat.cast_one, add_sub_cancel_right]

theorem coeffB_shift (N : ℕ) (c : Channel N → ℚ) (i : ℕ) :
    coeffB N c (i+2) = (zeroExtend (fun j => c (.inr j)) (i:ℤ) : ℝ) := by
  simp only [coeffB, badAt, Nat.cast_add, Nat.cast_ofNat, add_sub_cancel_right]

/-- The physical good coefficient action is precisely the actual finite
rational coefficient matrix, including the last retained good rank. -/
theorem featureCoeffA_coefficientK (N : ℕ) (c : Channel N → ℚ) (i : Good N) :
    featureCoeffA N (coeffA N c) (coeffB N c) (i.val+1) =
      ((coefficientK N *ᵥ c) (.inl i) : ℝ) := by
  have hr := congrArg (fun q : ℚ => (q:ℝ)) (coefficientK_good_action N c i)
  push_cast at hr
  rw [hr]
  simp only [featureCoeffA, coeffA_shift,
    show i.val+1+1=i.val+2 by omega, coeffB_shift, zeroExtend_at]
  push_cast
  ring

/-- The physical bad coefficient action is the actual finite rational matrix.
Its omitted lower/upper coefficient values are supplied by zero extension. -/
theorem featureCoeffB_coefficientK (N : ℕ) (hN : 3 ≤ N)
    (c : Channel N → ℚ) (i : Bad N) :
    featureCoeffB N (coeffA N c) (coeffB N c) (i.val+2) =
      ((coefficientK N *ᵥ c) (.inr i) : ℝ) := by
  have hr := congrArg (fun q : ℚ => (q:ℝ)) (coefficientK_bad_action N c i)
  push_cast at hr
  rw [hr]
  have hshift : (i.val:ℤ)+2-1-2=(i.val:ℤ)-1 := by ring
  simp only [featureCoeffB, show i.val+2-1=i.val+1 by omega,
    show i.val+2=i.val+1+1 by omega, coeffA_shift]
  simp only [coeffB, badAt]
  push_cast
  simp only [show (i.val:ℤ)+1+1-2=(i.val:ℤ) by ring,
    show (i.val:ℤ)+1+1+1-2=(i.val:ℤ)+1 by ring,
    zeroExtend_at]
  have hN0 : (N:ℝ) ≠ 0 := by exact_mod_cast (show N ≠ 0 by omega)
  have hi2 : (i.val:ℝ)+2 ≠ 0 := by positivity
  have hi2' : (i.val:ℝ)+1+1 ≠ 0 := by positivity
  field_simp
  <;> ring

/-- The absent rank-zero good coefficient is exactly zero. -/
@[simp] theorem coeffA_zero (N : ℕ) (c : Channel N → ℚ) : coeffA N c 0 = 0 := by
  simp only [coeffA, goodAt, Nat.cast_zero]
  rw [zeroExtend_of_negative _ (by norm_num), Rat.cast_zero]

@[simp] theorem coeffB_one (N : ℕ) (c : Channel N → ℚ) : coeffB N c 1 = 0 := by
  simp only [coeffB, badAt, Nat.cast_one]
  rw [zeroExtend_of_negative _ (by norm_num), Rat.cast_zero]

theorem coeffA_of_le (N : ℕ) (hN : 1 ≤ N) (c : Channel N → ℚ)
    (k : ℕ) (hk : N ≤ k) : coeffA N c k = 0 := by
  simp only [coeffA, goodAt]
  rw [zeroExtend_of_le _ (by omega), Rat.cast_zero]

theorem coeffB_of_le (N : ℕ) (hN : 2 ≤ N) (c : Channel N → ℚ)
    (k : ℕ) (hk : N ≤ k) : coeffB N c k = 0 := by
  simp only [coeffB, badAt]
  rw [zeroExtend_of_le _ (by omega), Rat.cast_zero]

/-- Real physical feature attached to the actual finite rational channel. -/
def coefficientFeature {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ)
    (c : Channel (n-1) → ℚ) : State n → ℝ :=
  feature δ (coeffA (n-1) c) (coeffB (n-1) c)

/-- Exact finite-channel intertwining with the genuine labeled complete kernel.
The top rank and the rank-one bad feature are handled by their proved feature
degeneracies, without assuming injectivity of the feature representation. -/
theorem K0_coefficientFeature {n : ℕ} (hn : 4 ≤ n)
    {δ : Matrix (Fin n) (Fin n) ℝ} (hδ : SymmetricBalanced δ)
    (c : Channel (n-1) → ℚ) :
    (K0 n).mulVec (coefficientFeature δ c) =
      coefficientFeature δ (coefficientK (n-1) *ᵥ c) := by
  funext y
  rw [coefficientFeature, K0_feature (by omega) hδ]
  by_cases htop : y.rank=n-1
  · simp only [coefficientFeature, feature, x_full_rank hδ y htop,
      z_full_rank hδ y htop, mul_zero, add_zero]
  · have hk := rank_pos y
    have hkN : y.rank < n-1 := lt_of_le_of_ne (rank_le y) htop
    let i : Good (n-1) := ⟨y.rank-1, by omega⟩
    have hi : i.val+1=y.rank := by dsimp [i]; omega
    have ha : featureCoeffA (n-1) (coeffA (n-1) c) (coeffB (n-1) c) y.rank =
        coeffA (n-1) (coefficientK (n-1) *ᵥ c) y.rank := by
      rw [← hi, featureCoeffA_coefficientK, coeffA_at]
    by_cases hbot : y.rank=1
    · simp only [coefficientFeature, feature, ha, z_singleton_rank hδ y hbot,
        mul_zero, add_zero]
    · let j : Bad (n-1) := ⟨y.rank-2, by omega⟩
      have hj : j.val+2=y.rank := by dsimp [j]; omega
      have hb : featureCoeffB (n-1) (coeffA (n-1) c) (coeffB (n-1) c) y.rank =
          coeffB (n-1) (coefficientK (n-1) *ᵥ c) y.rank := by
        rw [← hj, featureCoeffB_coefficientK (n-1) (by omega), coeffB_at]
      simp only [coefficientFeature, feature, ha, hb]

/-- The source vector in A.15 is exactly the physical first perturbation of
the proven rank Poisson potential, including both physical endpoint ranks. -/
theorem coefficientFeature_source {n : ℕ} (hn : 4 ≤ n)
    {δ : Matrix (Fin n) (Fin n) ℝ} (hδ : SymmetricBalanced δ) :
    coefficientFeature δ (source (n-1)) =
      (perturbation δ).mulVec (fun y => rankPotential (n-1) y.rank) := by
  funext y
  rw [perturbation_rankPotential hδ]
  by_cases htop : y.rank=n-1
  · simp only [coefficientFeature, feature, x_full_rank hδ y htop,
      z_full_rank hδ y htop, mul_zero, add_zero]
  · have hk := rank_pos y
    have hkN : y.rank < n-1 := lt_of_le_of_ne (rank_le y) htop
    let i : Good (n-1) := ⟨y.rank-1, by omega⟩
    have hi : i.val+1=y.rank := by dsimp [i]; omega
    have ha : coeffA (n-1) (source (n-1)) y.rank =
        (gradient (n-1) y.rank:ℝ)/2 := by
      rw [← hi, coeffA_at, source]
      push_cast
      rfl
    by_cases hbot : y.rank=1
    · simp only [coefficientFeature, feature, ha, z_singleton_rank hδ y hbot,
        mul_zero, add_zero]
    · let j : Bad (n-1) := ⟨y.rank-2, by omega⟩
      have hj : j.val+2=y.rank := by dsimp [j]; omega
      have hb : coeffB (n-1) (source (n-1)) y.rank =
          (gradient (n-1) (y.rank-1):ℝ)/(2*(y.rank:ℝ)) := by
        rw [← hj, coeffB_at, source]
        rw [show j.val+2-1=j.val+1 by omega]
        push_cast
        rfl
      simp only [coefficientFeature, feature, ha, hb]

theorem coefficientFeature_sub {n : ℕ} (δ : Matrix (Fin n) (Fin n) ℝ)
    (c d : Channel (n-1) → ℚ) :
    coefficientFeature δ (c-d) = coefficientFeature δ c-coefficientFeature δ d := by
  funext y
  simp only [coefficientFeature, feature, coeffA, coeffB, goodAt, badAt,
    zeroExtend, Pi.sub_apply]
  split_ifs <;> push_cast <;> ring

/-- The unique actual rational coefficient solution used by A.17. -/
def coefficientSolution (N : ℕ) : Channel N → ℚ :=
  (1-coefficientK N)⁻¹ *ᵥ source N

theorem coefficientSolution_equation (N : ℕ) (hN : 3 ≤ N) :
    coefficientSolution N-coefficientK N *ᵥ coefficientSolution N = source N := by
  have hunit := (1-coefficientK N).isUnit_iff_isUnit_det.mp
    (coefficient_system_isUnit N hN)
  have h : (1-coefficientK N) *ᵥ coefficientSolution N = source N := by
    rw [coefficientSolution, Matrix.mulVec_mulVec, Matrix.mul_nonsing_inv _ hunit,
      Matrix.one_mulVec]
  simpa only [Matrix.sub_mulVec, Matrix.one_mulVec] using h

/-- A genuine physical Poisson equation for the finite-channel solution.
This transports the proved rational inverse equation through the proved
labeled-kernel intertwining; no feature or scalar bridge is assumed. -/
theorem coefficientFeature_poisson {n : ℕ} (hn : 4 ≤ n)
    {δ : Matrix (Fin n) (Fin n) ℝ} (hδ : SymmetricBalanced δ) :
    coefficientFeature δ (coefficientSolution (n-1)) -
      (K0 n).mulVec (coefficientFeature δ (coefficientSolution (n-1))) =
      (perturbation δ).mulVec (fun y => rankPotential (n-1) y.rank) := by
  rw [K0_coefficientFeature hn hδ, ← coefficientFeature_sub,
    coefficientSolution_equation (n-1) (by omega), coefficientFeature_source hn hδ]

#print axioms featureCoeffA_coefficientK
#print axioms featureCoeffB_coefficientK
#print axioms K0_coefficientFeature
#print axioms coefficientFeature_source
#print axioms coefficientFeature_poisson

end Active
end
end SymmetricSector
