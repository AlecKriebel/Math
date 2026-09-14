import SymmetricSector.Analytic
import SymmetricSector.BlockBounds
import SymmetricSector.BlockActions
import SymmetricSector.GoodPhase

/-! Appendix A.22 for the actual binomial bad reward. The rational algebra
below is a bridge to the concrete matrix action, with all physical rank
restrictions and absent boundary coefficients explicit. -/
namespace SymmetricSector
open Matrix
open scoped BigOperators

def badRetentionRatio (N k : ℚ) : ℚ :=
  (N*(k-2)+k)/(2*k*N) + (N-k-1)*(k-2)/(2*N*(N-k)) +
    k*(N-k-1)/(2*(k+1)*N)

theorem bad_barrier_ratio_identity (N k : ℚ)
    (hN : 0 < N) (hk : 0 < k) (hkN : k < N) :
    7*N/25*(1-badRetentionRatio N k)-1 =
      barrierPolynomial N k / (50*k*(k+1)*(N-k)) := by
  have hk1 : k+1 ≠ 0 := by linarith
  have hNk : N-k ≠ 0 := by linarith
  unfold badRetentionRatio barrierPolynomial
  field_simp
  <;> ring

theorem bad_barrier_ratio_nonneg (N k : ℚ)
    (hN : 25 ≤ N) (hk : 2 ≤ k) (hkN : k < N) :
    1 ≤ 7*N/25*(1-badRetentionRatio N k) := by
  have hp := barrierPolynomial_pos N k hN (by linarith)
  have hd : 0 < 50*k*(k+1)*(N-k) := by
    have hk0 : 0 < k := by linarith
    have hk1 : 0 < k+1 := by linarith
    have hNk : 0 < N-k := by linarith
    positivity
  have he := bad_barrier_ratio_identity N k (by linarith) (by linarith) hkN
  have hh := div_pos hp hd
  linarith

def badExitRatio (N k : ℚ) : ℚ :=
  7/25/(N-2)*(k*(N-k-1)/(k+1)+(N-k)*(k-1)/k)

theorem bad_exit_ratio_identity (N k : ℚ) (hN : 3 ≤ N) (hk : 1 ≤ k) :
    14/25-badExitRatio N k =
      7*((N-3)*(2*k+1)+k*(k-1)*(2*k-1)+3)/(25*(N-2)*k*(k+1)) := by
  have hN2 : N-2 ≠ 0 := by linarith
  have hk0 : k ≠ 0 := by linarith
  have hk1 : k+1 ≠ 0 := by linarith
  unfold badExitRatio
  field_simp
  <;> ring

theorem bad_exit_ratio_le (N k : ℚ) (hN : 3 ≤ N) (hk : 1 ≤ k) :
    badExitRatio N k ≤ 14/25 := by
  have hNk : 0 ≤ (N-3)*(2*k+1) :=
    mul_nonneg (by linarith) (by linarith)
  have hkk : 0 ≤ k*(k-1)*(2*k-1) :=
    mul_nonneg (mul_nonneg (by linarith) (by linarith)) (by linarith)
  have hnum : 0 ≤ 7*((N-3)*(2*k+1)+k*(k-1)*(2*k-1)+3) := by linarith
  have hden : 0 ≤ 25*(N-2)*k*(k+1) :=
    mul_nonneg (mul_nonneg (mul_nonneg (by norm_num) (by linarith))
      (by linarith)) (by linarith)
  have he := bad_exit_ratio_identity N k hN hk
  have hp := div_nonneg hnum hden
  linarith

theorem choose_succ_ratio (m i : ℕ) (hi : i ≤ m) :
    (Nat.choose m (i+1):ℚ) = (Nat.choose m i:ℚ)*((m:ℚ)-i)/(i+1) := by
  have h := Nat.choose_succ_right_eq m i
  have hc : (Nat.choose m (i+1):ℚ)*(i+1) = (Nat.choose m i:ℚ)*((m:ℚ)-i) := by
    exact_mod_cast h
  exact (eq_div_iff (by positivity : (i+1:ℚ) ≠ 0)).2 hc

theorem choose_pred_ratio (m i : ℕ) (hi : 1 ≤ i) (him : i ≤ m) :
    (Nat.choose m (i-1):ℚ) = (Nat.choose m i:ℚ)*i/((m:ℚ)-i+1) := by
  have h := Nat.choose_succ_right_eq m (i-1)
  rw [Nat.sub_add_cancel hi] at h
  have hh : m-(i-1) = m-i+1 := by omega
  rw [hh] at h
  have hc : (Nat.choose m i:ℚ)*i = (Nat.choose m (i-1):ℚ)*((m:ℚ)-i+1) := by
    exact_mod_cast h
  apply (eq_div_iff ?_).2 hc.symm
  have hq : (i:ℚ) ≤ m := by exact_mod_cast him
  linarith

theorem negative_badReward_nonneg (N : ℕ) (i : Bad N) : 0 ≤ -badReward N i := by
  simp only [badReward, reward, neg_div, neg_neg]
  positivity

theorem badReward_upper_ratio (N : ℕ) (hN : 3 ≤ N) (i : Bad N) :
    zeroExtend (-badReward N) ((i.val:ℤ)+1) =
      (-badReward N i)*((N:ℚ)-i.val-3)/(i.val+1) := by
  have hi : i.val ≤ N-3 := by have := i.isLt; omega
  have hr := choose_succ_ratio (N-3) i.val hi
  rw [Nat.cast_sub hN, Nat.cast_ofNat] at hr
  by_cases ht : i.val+1 < N-2
  · have hh : 0 ≤ (i.val:ℤ)+1 ∧ (i.val:ℤ)+1 < ((N-2:ℕ):ℤ) := by omega
    simp only [zeroExtend, dif_pos hh, Pi.neg_apply, badReward, reward,
      neg_div, neg_neg]
    have he : ((i.val:ℤ)+1).toNat = i.val+1 := by omega
    simp only [he]
    rw [hr]
    ring
  · have he : (N:ℚ)-i.val-3 = 0 := by
      have h : N=i.val+3 := by omega
      have hq : (N:ℚ)=i.val+3 := by exact_mod_cast h
      linarith
    rw [zeroExtend_of_le _ (by omega), he]
    simp

theorem badReward_lower_ratio (N : ℕ) (hN : 3 ≤ N) (i : Bad N) :
    zeroExtend (-badReward N) ((i.val:ℤ)-1) =
      (-badReward N i)*i.val/((N:ℚ)-i.val-2) := by
  have hi : i.val ≤ N-3 := by have := i.isLt; omega
  by_cases ht : i.val=0
  · rw [ht, zeroExtend_of_negative _ (by norm_num)]
    simp
  · have hi1 : 1 ≤ i.val := by omega
    have hr := choose_pred_ratio (N-3) i.val hi1 hi
    rw [Nat.cast_sub hN, Nat.cast_ofNat] at hr
    have hh : 0 ≤ (i.val:ℤ)-1 ∧ (i.val:ℤ)-1 < ((N-2:ℕ):ℤ) := by omega
    simp only [zeroExtend, dif_pos hh, Pi.neg_apply, badReward, reward,
      neg_div, neg_neg]
    have he : ((i.val:ℤ)-1).toNat = i.val-1 := by omega
    simp only [he]
    rw [hr]
    ring

theorem choose_level_ratio (m i : ℕ) (hi : i ≤ m+1) :
    (Nat.choose m i:ℚ) = (Nat.choose (m+1) i:ℚ)*((m:ℚ)+1-i)/(m+1) := by
  have h := Nat.choose_mul_succ_eq m i
  have hc : (Nat.choose m i:ℚ)*(m+1) =
      (Nat.choose (m+1) i:ℚ)*((m:ℚ)+1-i) := by
    exact_mod_cast h
  exact (eq_div_iff (by positivity : (m+1:ℚ) ≠ 0)).2 hc

theorem choose_level_pred_ratio (m i : ℕ) (hi : 1 ≤ i) :
    (Nat.choose m (i-1):ℚ) = (Nat.choose (m+1) i:ℚ)*i/(m+1) := by
  have h := Nat.succ_mul_choose_eq m (i-1)
  rw [show Nat.succ (i-1)=i by omega] at h
  have hc : (Nat.choose m (i-1):ℚ)*(m+1) = (Nat.choose (m+1) i:ℚ)*i := by
    exact_mod_cast (show Nat.choose m (i-1)*(m+1) = Nat.choose (m+1) i*i by
      simpa only [Nat.succ_eq_add_one, Nat.mul_comm] using h)
  exact (eq_div_iff (by positivity : (m+1:ℚ) ≠ 0)).2 hc

theorem badReward_good_same_ratio (N : ℕ) (hN : 3 ≤ N) (i : Good N) :
    zeroExtend (-badReward N) (i.val:ℤ) =
      goodReward N i * (2*((N:ℚ)-i.val-2)/(N-2)) := by
  have hi : i.val ≤ N-2 := by have := i.isLt; omega
  have hpow : (2:ℚ)^(N-1) = 2*2^(N-2) := by
    rw [show N-1=(N-2)+1 by omega, pow_succ]
    ring
  by_cases ht : i.val < N-2
  · have hh : 0 ≤ (i.val:ℤ) ∧ (i.val:ℤ) < ((N-2:ℕ):ℤ) := by omega
    have hr := choose_level_ratio (N-3) i.val (by omega)
    rw [show N-3+1=N-2 by omega, Nat.cast_sub hN, Nat.cast_ofNat] at hr
    rw [show (N:ℚ)-3+1=N-2 by ring] at hr
    simp only [zeroExtend, dif_pos hh, Int.toNat_natCast, Pi.neg_apply,
      badReward, goodReward, reward, neg_div, neg_neg]
    rw [hr, hpow]
    have hN2 : (N:ℚ)-2 ≠ 0 := by
      have h : (3:ℚ) ≤ N := by exact_mod_cast hN
      linarith
    field_simp
    <;> ring
  · have he : (N:ℚ)-i.val-2 = 0 := by
      have h : N=i.val+2 := by omega
      have hq : (N:ℚ)=i.val+2 := by exact_mod_cast h
      linarith
    rw [zeroExtend_of_le _ (by omega), he]
    simp

theorem badReward_good_pred_ratio (N : ℕ) (hN : 3 ≤ N) (i : Good N) :
    zeroExtend (-badReward N) ((i.val:ℤ)-1) =
      goodReward N i * (2*i.val/(N-2)) := by
  have hi : i.val ≤ N-2 := by have := i.isLt; omega
  have hpow : (2:ℚ)^(N-1) = 2*2^(N-2) := by
    rw [show N-1=(N-2)+1 by omega, pow_succ]
    ring
  by_cases ht : i.val=0
  · rw [ht, zeroExtend_of_negative _ (by norm_num)]
    simp
  · have hh : 0 ≤ (i.val:ℤ)-1 ∧ (i.val:ℤ)-1 < ((N-2:ℕ):ℤ) := by omega
    have hr := choose_level_pred_ratio (N-3) i.val (by omega)
    rw [show N-3+1=N-2 by omega, Nat.cast_sub hN, Nat.cast_ofNat] at hr
    rw [show (N:ℚ)-3+1=N-2 by ring] at hr
    simp only [zeroExtend, dif_pos hh, Pi.neg_apply,
      badReward, goodReward, reward, neg_div, neg_neg]
    have he : ((i.val:ℤ)-1).toNat=i.val-1 := by omega
    simp only [he]
    rw [hr, hpow]
    have hN2 : (N:ℚ)-2 ≠ 0 := by
      have h : (3:ℚ) ≤ N := by exact_mod_cast hN
      linarith
    field_simp
    <;> ring

/-- The exact retention ratio for the actual binomial reward, including both
absent boundary coordinates. -/
theorem phaseQ_badReward (N : ℕ) (hN : 3 ≤ N) (i : Bad N) :
    (phaseQ N *ᵥ (-badReward N)) i =
      badRetentionRatio N (i.val+2)*(-badReward N i) := by
  rw [phaseQ_mulVec, badReward_upper_ratio N hN, badReward_lower_ratio N hN]
  simp only [Pi.neg_apply]
  unfold badRetentionRatio
  have hN0 : (N:ℚ) ≠ 0 := by exact_mod_cast (show N ≠ 0 by omega)
  have hNk : (N:ℚ)-i.val-2 ≠ 0 := by
    have h : (i.val+3:ℚ) ≤ N := by
      exact_mod_cast (show i.val+3 ≤ N by have := i.isLt; omega)
    linarith
  have hNk' : (N:ℚ)-(i.val+2) ≠ 0 := by intro h; apply hNk; linarith
  field_simp
  <;> ring

/-- The printed bad supersolution is a multiple of the actual bad reward. -/
def phaseWbar (N : ℕ) : Bad N → ℚ := (7*(N:ℚ)/25) • (-badReward N)

/-- The first inequality of A.22 for the specified finite matrix and source. -/
theorem phaseWbar_supersolution (N : ℕ) (hN : 25 ≤ N) :
    -badReward N ≤ (1-phaseQ N) *ᵥ phaseWbar N := by
  intro i
  simp only [Matrix.sub_mulVec, Matrix.one_mulVec, phaseWbar, Matrix.mulVec_smul,
    Pi.sub_apply, Pi.smul_apply, smul_eq_mul, Pi.neg_apply]
  rw [phaseQ_badReward N (by omega)]
  have hNq : (25:ℚ) ≤ N := by exact_mod_cast hN
  have hkN : (i.val+2:ℚ) < N := by
    exact_mod_cast (show i.val+2 < N by have := i.isLt; omega)
  have hr := bad_barrier_ratio_nonneg N (i.val+2) hNq
    (by have h : (0:ℚ) ≤ i.val := Nat.cast_nonneg _; linarith) hkN
  have hw := negative_badReward_nonneg N i
  have hm := mul_le_mul_of_nonneg_right hr hw
  nlinarith

/-- C acting on the concrete barrier has the claimed exact normalized ratio. -/
theorem phaseC_Wbar_ratio (N : ℕ) (hN : 3 ≤ N) (i : Good N) :
    (phaseC N *ᵥ phaseWbar N) i = badExitRatio N (i.val+1)*goodReward N i := by
  simp only [phaseWbar, Matrix.mulVec_smul, Pi.smul_apply, smul_eq_mul]
  rw [phaseC_mulVec, badReward_good_same_ratio N hN, badReward_good_pred_ratio N hN]
  unfold badExitRatio
  have hN0 : (N:ℚ) ≠ 0 := by exact_mod_cast (show N ≠ 0 by omega)
  have hN2 : (N:ℚ)-2 ≠ 0 := by
    have h : (3:ℚ) ≤ N := by exact_mod_cast hN
    linarith
  field_simp
  <;> ring

/-- The second inequality of A.22 includes the bottom and top good rows. -/
theorem phaseC_Wbar_le (N : ℕ) (hN : 3 ≤ N) :
    phaseC N *ᵥ phaseWbar N ≤ (14/25:ℚ) • goodReward N := by
  intro i
  rw [phaseC_Wbar_ratio N hN]
  change badExitRatio N (i.val+1)*goodReward N i ≤ 14/25*goodReward N i
  have hr := bad_exit_ratio_le N (i.val+1) (by exact_mod_cast hN)
    (by have h : (0:ℚ) ≤ i.val := Nat.cast_nonneg _; linarith)
  apply mul_le_mul_of_nonneg_right hr
  simp only [goodReward, reward]
  positivity

#print axioms phaseWbar_supersolution
#print axioms phaseC_Wbar_le

theorem mulVec_mono_of_nonneg {ι κ : Type*} [Fintype κ]
    (A : Matrix ι κ ℚ) (hA : ∀ i j, 0 ≤ A i j)
    {u v : κ → ℚ} (h : u ≤ v) : A *ᵥ u ≤ A *ᵥ v := by
  intro i
  exact Finset.sum_le_sum fun j _ => mul_le_mul_of_nonneg_left (h j) (hA i j)

theorem mulVec_nonneg_of_nonneg {ι κ : Type*} [Fintype κ]
    (A : Matrix ι κ ℚ) (hA : ∀ i j, 0 ≤ A i j)
    {v : κ → ℚ} (h : 0 ≤ v) : 0 ≤ A *ᵥ v := by
  intro i
  exact Finset.sum_nonneg fun j _ => mul_nonneg (hA i j) (h j)

theorem phaseW_nonneg (N : ℕ) (hN : 3 ≤ N) : 0 ≤ phaseW N := by
  exact mulVec_nonneg_of_nonneg _ (phaseQ_inverse_nonneg N hN)
    (negative_badReward_nonneg N)

/-- Positivity of the actual inverse turns A.22 into an upper bound on W. -/
theorem phaseW_le_Wbar (N : ℕ) (hN : 25 ≤ N) : phaseW N ≤ phaseWbar N := by
  have h := mulVec_mono_of_nonneg (1-phaseQ N)⁻¹
    (phaseQ_inverse_nonneg N (by omega)) (phaseWbar_supersolution N hN)
  rw [Matrix.mulVec_mulVec,
    Matrix.nonsing_inv_mul _ ((1-phaseQ N).isUnit_iff_isUnit_det.mp
      (phaseQ_isUnit N (by omega))), Matrix.one_mulVec] at h
  exact h

theorem phaseC_W_nonneg (N : ℕ) (hN : 3 ≤ N) : 0 ≤ phaseC N *ᵥ phaseW N := by
  exact mulVec_nonneg_of_nonneg _ (phaseC_nonneg N hN) (phaseW_nonneg N hN)

theorem phaseC_W_le (N : ℕ) (hN : 25 ≤ N) :
    phaseC N *ᵥ phaseW N ≤ (14/25:ℚ) • goodReward N := by
  exact (mulVec_mono_of_nonneg _ (phaseC_nonneg N (by omega))
    (phaseW_le_Wbar N hN)).trans (phaseC_Wbar_le N (by omega))

/-- Both A.25 bounds for the genuine inverse-defined f₀ and v. -/
theorem phaseF0_bounds (N : ℕ) (hN : 25 ≤ N) :
    (11/25:ℚ) • phaseV N ≤ phaseF0 N ∧ phaseF0 N ≤ phaseV N := by
  have hN3 : 3 ≤ N := by omega
  have hlo : (11/25:ℚ) • goodReward N ≤ goodReward N-phaseC N *ᵥ phaseW N := by
    intro i
    have h := phaseC_W_le N hN i
    simp only [Pi.smul_apply, smul_eq_mul, Pi.sub_apply] at h ⊢
    linarith
  have hhi : goodReward N-phaseC N *ᵥ phaseW N ≤ goodReward N := by
    intro i
    have h := phaseC_W_nonneg N hN3 i
    simp only [Pi.sub_apply, Pi.zero_apply] at h ⊢
    linarith
  constructor
  · have h := mulVec_mono_of_nonneg (1-phaseS N)⁻¹ (phaseS_inverse_nonneg N hN3) hlo
    rw [Matrix.mulVec_smul] at h
    exact h
  · exact mulVec_mono_of_nonneg _ (phaseS_inverse_nonneg N hN3) hhi

theorem phaseF0_pos (N : ℕ) (hN : 25 ≤ N) (i : Good N) : 0 < phaseF0 N i := by
  have h := (phaseF0_bounds N hN).1 i
  have hv := phaseV_pos N (by omega) i
  change 11/25*phaseV N i ≤ _ at h
  linarith

#print axioms phaseW_le_Wbar
#print axioms phaseF0_bounds
#print axioms phaseF0_pos

end SymmetricSector
