import SymmetricSector.BlockBounds

/-! Concrete banded actions of the actual Schur blocks. Every absent boundary
entry is represented by a zero extension of the finite vector. -/
namespace SymmetricSector
open Matrix
open scoped BigOperators

/-- Zero extension by the zero-based integer coordinate. -/
def zeroExtend {m : ℕ} (v : Fin m → ℚ) (k : ℤ) : ℚ :=
  if h : 0 ≤ k ∧ k < m then v ⟨k.toNat, by omega⟩ else 0

/-- Good physical ranks start at one. -/
def goodAt (N : ℕ) (v : Good N → ℚ) (k : ℤ) : ℚ := zeroExtend v (k - 1)
/-- Bad physical ranks start at two. -/
def badAt (N : ℕ) (v : Bad N → ℚ) (k : ℤ) : ℚ := zeroExtend v (k - 2)

@[simp] theorem zeroExtend_at {m : ℕ} (v : Fin m → ℚ) (i : Fin m) :
    zeroExtend v (i.val : ℤ) = v i := by
  simp [zeroExtend, i.isLt]

 theorem zeroExtend_of_negative {m : ℕ} (v : Fin m → ℚ) {k : ℤ} (hk : k < 0) :
    zeroExtend v k = 0 := by
  simp [zeroExtend, show ¬0 ≤ k by omega]

 theorem zeroExtend_of_le {m : ℕ} (v : Fin m → ℚ) {k : ℤ} (hk : m ≤ k) :
    zeroExtend v k = 0 := by
  simp [zeroExtend, show ¬k < m by omega]

 theorem zeroExtend_nonneg {m : ℕ} (v : Fin m → ℚ) (hv : ∀ i, 0 ≤ v i) (k : ℤ) :
    0 ≤ zeroExtend v k := by
  unfold zeroExtend
  split_ifs
  · exact hv _
  · exact le_refl _

@[simp] theorem zeroExtend_mul {m : ℕ} (v : Fin m → ℚ) (c : ℚ) (k : ℤ) :
    zeroExtend (fun i => c * v i) k = c * zeroExtend v k := by
  unfold zeroExtend
  split_ifs <;> simp

@[simp] theorem zeroExtend_add {m : ℕ} (v w : Fin m → ℚ) (k : ℤ) :
    zeroExtend (v + w) k = zeroExtend v k + zeroExtend w k := by
  unfold zeroExtend
  split_ifs <;> simp

@[simp] theorem zeroExtend_sub {m : ℕ} (v w : Fin m → ℚ) (k : ℤ) :
    zeroExtend (v - w) k = zeroExtend v k - zeroExtend w k := by
  unfold zeroExtend
  split_ifs <;> simp

@[simp] theorem goodAt_at (N : ℕ) (v : Good N → ℚ) (i : Good N) :
    goodAt N v ((i.val : ℤ) + 1) = v i := by simp [goodAt]

@[simp] theorem badAt_at (N : ℕ) (v : Bad N → ℚ) (i : Bad N) :
    badAt N v ((i.val : ℤ) + 2) = v i := by simp [badAt]

/-- A selector sum over a finite vector is exactly its integer zero extension. -/
theorem sum_int_selector {m : ℕ} (v : Fin m → ℚ) (k : ℤ) :
    (∑ j : Fin m, if (j.val : ℤ) = k then v j else 0) = zeroExtend v k := by
  by_cases hk : 0 ≤ k ∧ k < m
  · let i : Fin m := ⟨k.toNat, by omega⟩
    have he : (i.val : ℤ) = k := by dsimp [i]; omega
    have hs : ∀ j : Fin m, (j.val : ℤ) = k ↔ j = i := by
      intro j
      constructor
      · intro h; apply Fin.ext; dsimp [i]; omega
      · rintro rfl; exact he
    simp only [hs, Finset.sum_ite_eq', Finset.mem_univ, if_true]
    simp [zeroExtend, hk, i]
  · have hs : ∀ j : Fin m, (j.val : ℤ) ≠ k := by
      intro j he
      have hj := j.isLt
      omega
    simp [hs, zeroExtend, hk]

 theorem sum_int_selector_mul {m : ℕ} (v : Fin m → ℚ) (k : ℤ) (c : ℚ) :
    (∑ j : Fin m, if (j.val : ℤ) = k then c * v j else 0) = c * zeroExtend v k := by
  have hi : ∀ j : Fin m, (if (j.val : ℤ) = k then c * v j else 0) =
      c * (if (j.val : ℤ) = k then v j else 0) := by
    intro j; split_ifs <;> simp
  simp only [hi, ← Finset.mul_sum, sum_int_selector]

/-- The transpose of D has one surviving selector; the top good boundary has none. -/
theorem phaseD_transpose_mulVec (N : ℕ) (v : Bad N → ℚ) (i : Good N) :
    ((phaseD N)ᵀ *ᵥ v) i = (1 / (N : ℚ)) * zeroExtend v i.val := by
  simp only [Matrix.mulVec, dotProduct, Matrix.transpose_apply, phaseD, coefficientK]
  have he : ∀ j : Bad N,
      -(if j.val = i.val then (-1 : ℚ) / N else 0) * v j =
      if (j.val : ℤ) = i.val then (1 / (N : ℚ)) * v j else 0 := by
    intro j
    by_cases h : j.val = i.val
    · simp [h]; ring
    · have hz : (j.val : ℤ) ≠ i.val := by exact_mod_cast h
      simp [h, hz]
  simp only [he, sum_int_selector_mul]

/-- The diagonal and two neighboring entries of Q transpose, with absent
finite-vector coordinates explicitly zero. -/
theorem phaseQ_transpose_mulVec (N : ℕ) (v : Bad N → ℚ) (i : Bad N) :
    ((phaseQ N)ᵀ *ᵥ v) i =
      ((N : ℚ) * i.val + i.val + 2) / (2 * (i.val + 2) * N) * v i +
      ((i.val : ℚ) + 1) * i.val / (2 * (i.val + 2) * N) *
        zeroExtend v ((i.val : ℤ) - 1) +
      ((N : ℚ) - i.val - 4) / (2 * N) * zeroExtend v ((i.val : ℤ) + 1) := by
  have he : ∀ j : Bad N, (phaseQ N)ᵀ i j * v j =
      (if (j.val : ℤ) = i.val then
        ((N : ℚ) * i.val + i.val + 2) / (2 * (i.val + 2) * N) * v j else 0) +
      (if (j.val : ℤ) = (i.val : ℤ) - 1 then
        ((i.val : ℚ) + 1) * i.val / (2 * (i.val + 2) * N) * v j else 0) +
      (if (j.val : ℤ) = (i.val : ℤ) + 1 then
        ((N : ℚ) - i.val - 4) / (2 * N) * v j else 0) := by
    intro j
    simp only [Matrix.transpose_apply, phaseQ, coefficientK]
    split_ifs <;> try omega
    all_goals try { congr 1; congr 1 <;> ring }
  simp only [Matrix.mulVec, dotProduct, he, Finset.sum_add_distrib,
    sum_int_selector_mul, zeroExtend_at]

/-- The concrete Q action has exactly its diagonal, successor, and predecessor. -/
theorem phaseQ_mulVec (N : ℕ) (v : Bad N → ℚ) (i : Bad N) :
    (phaseQ N *ᵥ v) i =
      ((N : ℚ) * i.val + i.val + 2) / (2 * (i.val + 2) * N) * v i +
      ((i.val : ℚ) + 2) * (i.val + 1) / (2 * (i.val + 3) * N) *
        zeroExtend v ((i.val : ℤ) + 1) +
      ((N : ℚ) - i.val - 3) / (2 * N) * zeroExtend v ((i.val : ℤ) - 1) := by
  have he : ∀ j : Bad N, phaseQ N i j * v j =
      (if (j.val : ℤ) = i.val then
        ((N : ℚ) * i.val + i.val + 2) / (2 * (i.val + 2) * N) * v j else 0) +
      (if (j.val : ℤ) = (i.val : ℤ) + 1 then
        ((i.val : ℚ) + 2) * (i.val + 1) / (2 * (i.val + 3) * N) * v j else 0) +
      (if (j.val : ℤ) = (i.val : ℤ) - 1 then
        ((N : ℚ) - i.val - 3) / (2 * N) * v j else 0) := by
    intro j
    have hj₀ : (j.val : ℤ) = i.val ↔ j.val = i.val := by omega
    have hjPlus : (j.val : ℤ) = (i.val : ℤ) + 1 ↔ j.val = i.val + 1 := by omega
    have hjMinus : (j.val : ℤ) = (i.val : ℤ) - 1 ↔ i.val = j.val + 1 := by omega
    simp only [phaseQ, coefficientK, hj₀, hjPlus, hjMinus]
    split_ifs
    all_goals try omega
    all_goals simp only [add_zero, zero_add, zero_mul]
    · have hn : j.val = i.val := by omega
      rw [hn]; congr 1; congr 1 <;> ring
    · have hn : j.val = i.val + 1 := by omega
      rw [hn]; push_cast; congr 1; congr 1 <;> ring
    · have hn : i.val = j.val + 1 := by omega
      have hq : (i.val : ℚ) = j.val + 1 := by exact_mod_cast hn
      rw [hq]; congr 1; congr 1 <;> ring
  simp only [Matrix.mulVec, dotProduct, he, Finset.sum_add_distrib,
    sum_int_selector_mul, zeroExtend_at]

/-- C connects a good rank only to the two adjacent bad coordinates. -/
theorem phaseC_mulVec (N : ℕ) (v : Bad N → ℚ) (i : Good N) :
    (phaseC N *ᵥ v) i =
      ((i.val : ℚ) + 1) / (2 * (i.val + 2) * N) * zeroExtend v i.val +
      ((N : ℚ) - i.val - 1) / (2 * (i.val + 1) * N) *
        zeroExtend v ((i.val : ℤ) - 1) := by
  have he : ∀ j : Bad N, phaseC N i j * v j =
      (if (j.val : ℤ) = i.val then
        ((i.val : ℚ) + 1) / (2 * (i.val + 2) * N) * v j else 0) +
      (if (j.val : ℤ) = (i.val : ℤ) - 1 then
        ((N : ℚ) - i.val - 1) / (2 * (i.val + 1) * N) * v j else 0) := by
    intro j
    have hj₀ : (j.val : ℤ) = i.val ↔ i.val = j.val := by omega
    have hjMinus : (j.val : ℤ) = (i.val : ℤ) - 1 ↔ i.val = j.val + 1 := by omega
    simp only [phaseC, coefficientK, hj₀, hjMinus]
    split_ifs with hd hl
    all_goals try omega
    all_goals simp only [add_zero, zero_add, zero_mul]
    · rw [hd]; congr 1; congr 1 <;> ring
    · have hq : (i.val : ℚ) = j.val + 1 := by exact_mod_cast (show i.val = j.val + 1 by omega)
      rw [hq]; congr 1; congr 1 <;> ring
  simp only [Matrix.mulVec, dotProduct, he, Finset.sum_add_distrib,
    sum_int_selector_mul]

/-- S is the concrete lower bidiagonal good block. -/
theorem phaseS_mulVec (N : ℕ) (v : Good N → ℚ) (i : Good N) :
    (phaseS N *ᵥ v) i =
      ((i.val : ℚ) + 1) / (2 * N) * v i +
      ((N : ℚ) - i.val - 1) / (2 * N) * zeroExtend v ((i.val : ℤ) - 1) := by
  have he : ∀ j : Good N, phaseS N i j * v j =
      (if (j.val : ℤ) = i.val then ((i.val : ℚ) + 1) / (2 * N) * v j else 0) +
      (if (j.val : ℤ) = (i.val : ℤ) - 1 then
        ((N : ℚ) - i.val - 1) / (2 * N) * v j else 0) := by
    intro j
    have hj₀ : (j.val : ℤ) = i.val ↔ j.val = i.val := by omega
    have hjMinus : (j.val : ℤ) = (i.val : ℤ) - 1 ↔ i.val = j.val + 1 := by omega
    simp only [phaseS, coefficientK, hj₀, hjMinus]
    split_ifs with hd hl
    all_goals try omega
    all_goals simp only [add_zero, zero_add, zero_mul]
    · rw [hd]
    · have hq : (i.val : ℚ) = j.val + 1 := by exact_mod_cast (show i.val = j.val + 1 by omega)
      rw [hq]
  simp only [Matrix.mulVec, dotProduct, he, Finset.sum_add_distrib,
    sum_int_selector_mul, zeroExtend_at]

/-- D is the single selector from the corresponding good coordinate. -/
theorem phaseD_mulVec (N : ℕ) (v : Good N → ℚ) (i : Bad N) :
    (phaseD N *ᵥ v) i = (1 / (N : ℚ)) * zeroExtend v i.val := by
  simp only [Matrix.mulVec, dotProduct, phaseD, coefficientK]
  have he : ∀ j : Good N,
      -(if i.val = j.val then (-1 : ℚ) / N else 0) * v j =
      if (j.val : ℤ) = i.val then (1 / (N : ℚ)) * v j else 0 := by
    intro j
    by_cases h : i.val = j.val
    · simp [h]; ring
    · have hz : (j.val : ℤ) ≠ i.val := by omega
      simp [h, hz]
  simp only [he, sum_int_selector_mul]

#print axioms phaseS_mulVec
#print axioms phaseC_mulVec
#print axioms phaseD_mulVec
#print axioms phaseQ_mulVec
#print axioms phaseQ_transpose_mulVec
#print axioms phaseD_transpose_mulVec

end SymmetricSector
