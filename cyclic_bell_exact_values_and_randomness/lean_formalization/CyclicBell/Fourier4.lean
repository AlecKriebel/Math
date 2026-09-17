import CyclicBell.MatrixAlgebra

/-! Four-point Fourier orthogonality for matrix-valued sequences.
Same-party matrices are completely arbitrary and need not commute.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Positive-exponent Fourier transform, as in the manuscript's Bhat. -/
def fourier4 (W : Fin 4 → Mat ι) (l : Fin 4) : Mat ι :=
  ∑ j : Fin 4, (Complex.I ^ (l.val * j.val)) • W j

theorem fourth_root_unit (y : Fin 4) :
    star (Complex.I ^ y.val) * Complex.I ^ y.val = 1 := by
  fin_cases y <;> norm_num

theorem fourth_root_orthogonality (j k : Fin 4) :
    (∑ l : Fin 4, star (Complex.I ^ (l.val * j.val)) *
      Complex.I ^ (l.val * k.val)) = if j = k then 4 else 0 := by
  fin_cases j <;> fin_cases k <;> norm_num [Fin.sum_univ_succ, pow_succ, mul_add, add_mul, Complex.I_mul_I]

/-- Matrix Parseval; the proof is a finite noncommutative polynomial expansion. -/
theorem fourier4_parseval (W : Fin 4 → Mat ι) :
    (∑ l : Fin 4, (fourier4 W l).conjTranspose * fourier4 W l) =
      (4 : ℂ) • (∑ j : Fin 4, (W j).conjTranspose * W j) := by
  classical
  have hexpand (l : Fin 4) :
      (fourier4 W l).conjTranspose * fourier4 W l =
        ∑ j : Fin 4, ∑ k : Fin 4,
          (star (Complex.I ^ (l.val * j.val)) * Complex.I ^ (l.val * k.val)) •
            ((W j).conjTranspose * W k) := by
    simp only [fourier4, Matrix.conjTranspose_sum, Matrix.conjTranspose_smul,
      Finset.sum_mul, Finset.mul_sum, smul_mul_assoc, mul_smul_comm, Finset.smul_sum, smul_smul]
    rw [Finset.sum_comm]
    simp only [mul_comm]
  simp_rw [hexpand]
  calc
    (∑ l : Fin 4, ∑ j : Fin 4, ∑ k : Fin 4,
       (star (Complex.I ^ (l.val * j.val)) * Complex.I ^ (l.val * k.val)) •
         ((W j).conjTranspose * W k)) =
      ∑ j : Fin 4, ∑ k : Fin 4,
       (∑ l : Fin 4, star (Complex.I ^ (l.val * j.val)) *
         Complex.I ^ (l.val * k.val)) • ((W j).conjTranspose * W k) := by
      simp only [Finset.sum_smul]
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro j _
      rw [Finset.sum_comm]
    _ = (4 : ℂ) • (∑ j : Fin 4, (W j).conjTranspose * W j) := by
      simp only [fourth_root_orthogonality]
      simp [Finset.smul_sum]

/-- Parseval plus unitary Bob observables gives exactly 16I, not 4I. -/
theorem fourier4_unitary_energy (B : Fin 4 → Mat ι)
    (hB : ∀ j, UnitaryRel (B j)) :
    (∑ l : Fin 4, (fourier4 B l).conjTranspose * fourier4 B l) =
      (16 : ℂ) • (1 : Mat ι) := by
  rw [fourier4_parseval]
  have hh (j : Fin 4) : (B j).conjTranspose * B j = 1 := (hB j).1
  simp only [hh]
  rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin]
  rw [← Nat.cast_smul_eq_nsmul ℂ 4 (1 : Mat ι), smul_smul]
  norm_num

def rotated (U : Mat ι) (y : Fin 4) : Mat ι := (Complex.I ^ y.val) • U

theorem rotated_unitary {U : Mat ι} (hU : UnitaryRel U) (y : Fin 4) :
    UnitaryRel (rotated U y) := hU.scalar (fourth_root_unit y)

/-- Degree at most three evaluation at i^y U, written as a Fourier transform. -/
def cyclePoly (a : Fin 4 → ℂ) (U : Mat ι) (y : Fin 4) : Mat ι :=
  fourier4 (fun j => a j • U ^ j.val) y

theorem cyclePoly_eq (a : Fin 4 → ℂ) (U : Mat ι) (y : Fin 4) :
    cyclePoly a U y = ∑ j : Fin 4, a j • rotated U y ^ j.val := by
  unfold cyclePoly fourier4
  apply Finset.sum_congr rfl
  intro j _
  simp only [rotated, smul_pow, smul_smul, ← pow_mul]
  congr 1
  ring

theorem cyclePoly_energy (a : Fin 4 → ℂ) {U : Mat ι} (hU : UnitaryRel U) :
    (∑ y : Fin 4, (cyclePoly a U y).conjTranspose * cyclePoly a U y) =
      (4 * ∑ j : Fin 4, star (a j) * a j) • (1 : Mat ι) := by
  unfold cyclePoly
  rw [fourier4_parseval]
  simp only [Matrix.conjTranspose_smul, smul_mul_assoc, mul_smul_comm, smul_smul]
  have hh (j : Fin 4) : (U ^ j.val).conjTranspose * U ^ j.val = 1 := (hU.pow j.val).1
  simp_rw [hh]
  rw [← Finset.sum_smul, smul_smul]
  simp only [mul_comm]

theorem power_commute {U B : Mat ι} (hc : U * B = B * U) (j : ℕ) :
    U ^ j * B = B * U ^ j := by
  induction j with
  | zero => simp
  | succ j hj =>
      calc
        U ^ (j + 1) * B = U ^ j * (U * B) := by simp [pow_succ, mul_assoc]
        _ = U ^ j * (B * U) := by rw [hc]
        _ = B * U ^ (j + 1) := by rw [← mul_assoc, hj]; simp [pow_succ, mul_assoc]

theorem cyclePoly_commute (a : Fin 4 → ℂ) {U B : Mat ι}
    (hc : U * B = B * U) (y : Fin 4) :
    cyclePoly a U y * B = B * cyclePoly a U y := by
  unfold cyclePoly fourier4
  simp only [Finset.sum_mul, Finset.mul_sum, smul_mul_assoc, mul_smul_comm]
  simp_rw [power_commute hc]

/-- Moving a unitary past the polynomial requires genuine commutation. -/
theorem commuting_right_energy {P B : Mat ι} (hB : UnitaryRel B)
    (hc : P * B = B * P) :
    (P * B).conjTranspose * (P * B) = P.conjTranspose * P := by
  rw [hc, Matrix.conjTranspose_mul]
  simp only [mul_assoc, hB.cancel_left]

/-! The source's inverse observable encoding, proved for arbitrary PVMs. -/

theorem fourth_root_power_orthogonality (a b : Fin 4) :
    (∑ j : Fin 4, star ((Complex.I ^ a.val) ^ j.val) * (Complex.I ^ b.val) ^ j.val) =
      if a = b then 4 else 0 := by
  fin_cases a <;> fin_cases b <;> norm_num [Fin.sum_univ_succ, pow_succ, mul_add, add_mul, Complex.I_mul_I]

theorem pvm_fourier_reconstruction {n : ℕ} (M : PVM n) (a : Fin 4) :
    (1 / 4 : ℂ) • (∑ j : Fin 4, star ((Complex.I ^ a.val) ^ j.val) • observable M ^ j.val) =
      M.effect a := by
  have hexpand :
      (∑ j : Fin 4, star ((Complex.I ^ a.val) ^ j.val) • observable M ^ j.val) =
      ∑ b : Fin 4, (∑ j : Fin 4,
        star ((Complex.I ^ a.val) ^ j.val) * (Complex.I ^ b.val) ^ j.val) • M.effect b := by
    simp only [observable_power, spectralSum, Finset.smul_sum, smul_smul, Finset.sum_smul]
    rw [Finset.sum_comm]
  rw [hexpand]
  simp only [fourth_root_power_orthogonality]
  have hcollapse : (∑ b : Fin 4, (if a = b then (4 : ℂ) else 0) • M.effect b) =
      (4 : ℂ) • M.effect a := by
    rw [Finset.sum_eq_single a]
    · simp
    · intro b _ hba
      simp [Ne.symm hba]
    · simp
  rw [hcollapse, smul_smul]
  norm_num

theorem fourth_root_negative_exponent (a j : Fin 4) :
    Complex.I ^ (-((a.val * j.val : ℕ) : ℤ)) = star ((Complex.I ^ a.val) ^ j.val) := by
  fin_cases a <;> fin_cases j <;> norm_num [zpow_neg, pow_succ, Complex.I_mul_I, Complex.inv_I, neg_inv] <;> norm_num [zpow_ofNat, pow_succ, Complex.I_mul_I]

/-- Exactly M_a = (1/4) sum_j i^(-a*j) A^j with integer negative exponents. -/
theorem pvm_source_fourier_reconstruction {n : ℕ} (M : PVM n) (a : Fin 4) :
    (1 / 4 : ℂ) • (∑ j : Fin 4,
      Complex.I ^ (-((a.val * j.val : ℕ) : ℤ)) • observable M ^ j.val) = M.effect a := by
  simp only [fourth_root_negative_exponent]
  exact pvm_fourier_reconstruction M a

end CyclicBell
