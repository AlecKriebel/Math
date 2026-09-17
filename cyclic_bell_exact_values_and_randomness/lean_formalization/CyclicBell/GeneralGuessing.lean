import CyclicBell.GeneralSwap

/-! Quantitative all-dimensional bias. A simple peak-minus-spectrum estimate
is slightly stronger than the manuscript estimate and implies its stated
bound. These are exact real/complex proofs, not numerical estimates.
No adversarial optimization over all Bell maximizers is asserted.  -/
noncomputable section
open scoped BigOperators
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

theorem cis_chord_identity (t : ℝ) :
    cis (2*t)-1=(2*Real.sin t : ℂ)*Complex.I*cis t := by
  rw [show 2*t=t+t by ring,cis_add]
  simp only [cis_exp,Complex.exp_mul_I,← Complex.ofReal_cos,← Complex.ofReal_sin]
  apply Complex.ext <;> simp only [Complex.mul_re,Complex.mul_im,Complex.add_re,Complex.add_im,
    Complex.sub_re,Complex.sub_im,Complex.one_re,Complex.one_im,Complex.ofReal_re,Complex.ofReal_im,
    Complex.I_re,Complex.I_im,Complex.re_ofNat,Complex.im_ofNat] <;>
    nlinarith [Real.sin_sq_add_cos_sq t]

theorem cis_chord_norm (t : ℝ) : ‖cis (2*t)-1‖=2*|Real.sin t| := by
  rw [cis_chord_identity,norm_mul,norm_mul,cis_norm,Complex.norm_I,
    mul_one,mul_one]
  rw [norm_mul,Complex.norm_real,Real.norm_eq_abs]
  norm_num

theorem root_difference_norm (j k : Ix d) :
    ‖equalityRoot j-equalityRoot k‖=‖chi (j-k)-1‖ := by
  have he : equalityRoot j-equalityRoot k=
      (equalityBase d*chi k)*(chi (j-k)-1) := by
    unfold equalityRoot
    have hc : chi k*chi (j-k)=chi j := by rw [← chi_add]; congr 1; ring
    linear_combination -(equalityBase d)*hc
  rw [he,norm_mul,norm_mul]
  rw [chi_norm,mul_one]
  change ‖cis (Real.pi*parityDelta d/d)‖*_=_
  rw [cis_norm,one_mul]

theorem short_chord (k : ℕ) :
    ‖chi (k : Ix d)-1‖=2*|Real.sin (Real.pi*k/(d : ℝ))| := by
  have hc : chi (k : Ix d)=cis (2*(Real.pi*k/(d : ℝ))) := by
    have hh := chi_cis_int (d := d) (k : ℤ)
    simp only [Int.cast_natCast] at hh
    rw [hh]
    congr 1
    push_cast
    ring
  rw [hc,cis_chord_norm]

theorem negative_chord (j : Ix d) : ‖chi (-j)-1‖=‖chi j-1‖ := by
  rw [← chi_star]
  have he : star (chi j)-1=star (chi j-1) := by simp
  rw [he,norm_star]

theorem sine_step_positive {k : ℕ} (hk : 0<k) (hkd : k<d) :
    0<Real.sin (Real.pi*k/(d : ℝ)) := by
  apply Real.sin_pos_of_pos_of_lt_pi
  · exact div_pos (mul_pos Real.pi_pos (by exact_mod_cast hk)) dimension_pos
  · apply (div_lt_iff₀ (dimension_pos (d := d))).mpr
    exact mul_lt_mul_of_pos_left (by exact_mod_cast hkd) Real.pi_pos

/-- Literal magnitude appearing in eq:R2. -/
theorem swapped_R2_norm (hd : 4≤d) :
    ‖autocorrelation (swappedPhase : Ix d → ℂ) 2‖ =
      4*Real.sin (Real.pi/(d : ℝ))*Real.sin (3*Real.pi/(d : ℝ)) := by
  rw [swapped_R2 hd,norm_mul,root_difference_norm,root_difference_norm]
  rw [show (-1 : Ix d)-(-2)=1 by ring,show (-3 : Ix d)-0=-(3 : Ix d) by ring]
  rw [negative_chord]
  have hch1 := short_chord (d := d) 1
  simp only [Nat.cast_one, mul_one] at hch1
  have hch3 := short_chord (d := d) 3
  norm_num only [Nat.cast_ofNat] at hch3
  rw [hch1,hch3]
  have h₁ := sine_step_positive (d := d) (k := 1) (by omega) (by omega)
  have h₃ := sine_step_positive (d := d) (k := 3) (by omega) (by omega)
  norm_num only [Nat.cast_one,Nat.cast_ofNat,mul_one] at h₁ h₃
  rw [abs_of_pos h₁,abs_of_pos h₃]
  rw [mul_comm Real.pi (3 : ℝ)]
  ring

/-- For a nonzero lag, subtracting the maximal Fourier power removes the
constant coefficient. The resulting weights are all nonnegative. -/
theorem autocorrelation_le_peak_excess (q : Ix d → ℂ) (hq : UnitPhases q)
    (t : Ix d) (ht : t≠0) (m : Ix d)
    (hm : ∀ k,powerSpectrum q k≤powerSpectrum q m) :
    ‖autocorrelation q t‖≤powerSpectrum q m-(d : ℝ) := by
  have hd : (d : ℝ)>0 := dimension_pos
  have hdC : (d : ℂ)≠0 := by exact_mod_cast (NeZero.ne d)
  have hs0 : (∑ k : Ix d,chi (-(k*t)))=0 := by
    simpa [neg_mul,mul_comm,ht] using character_sum (-t)
  have hdif : (∑ k,chi (-(k*t))*(powerSpectrum q k : ℂ)) =
      -(∑ k,chi (-(k*t))*((powerSpectrum q m-powerSpectrum q k : ℝ) : ℂ)) := by
    simp only [Complex.ofReal_sub,mul_sub,Finset.sum_sub_distrib,← Finset.sum_mul,hs0,zero_mul]
    ring
  rw [autocorrelation_inversion,hdif,norm_mul,norm_neg]
  have hnorm : ‖(d : ℂ)⁻¹‖=(d : ℝ)⁻¹ := by
    rw [norm_inv,Complex.norm_natCast]
  rw [hnorm]
  have hterm (k : Ix d) :
      ‖chi (-(k*t))*((powerSpectrum q m-powerSpectrum q k : ℝ) : ℂ)‖ =
        powerSpectrum q m-powerSpectrum q k := by
    rw [norm_mul,chi_norm,one_mul,Complex.norm_real,Real.norm_eq_abs,
      abs_of_nonneg (sub_nonneg.mpr (hm k))]
  have hsum : (∑ k,(powerSpectrum q m-powerSpectrum q k)) =
      (d : ℝ)*(powerSpectrum q m-d) := by
    rw [Finset.sum_sub_distrib,parseval q hq]
    simp only [Finset.sum_const,Finset.card_univ,ZMod.card,nsmul_eq_mul]
    ring
  calc
    (d : ℝ)⁻¹*‖∑ k,chi (-(k*t))*((powerSpectrum q m-powerSpectrum q k : ℝ) : ℂ)‖
        ≤ (d : ℝ)⁻¹*∑ k,‖chi (-(k*t))*((powerSpectrum q m-powerSpectrum q k : ℝ) : ℂ)‖ :=
      mul_le_mul_of_nonneg_left (norm_sum_le _ _) (inv_nonneg.mpr hd.le)
    _ = (d : ℝ)⁻¹*((d : ℝ)*(powerSpectrum q m-d)) := by simp_rw [hterm]; rw [hsum]
    _ = powerSpectrum q m-d := by field_simp

/-- A quantitative peak exists without assuming a particular maximizing label. -/
theorem exists_power_peak (q : Ix d → ℂ) (hq : UnitPhases q)
    (t : Ix d) (ht : t≠0) :
    ∃ m,(d : ℝ)+‖autocorrelation q t‖≤powerSpectrum q m := by
  obtain ⟨m,hm,hmall⟩ := Finset.exists_max_image Finset.univ (powerSpectrum q) Finset.univ_nonempty
  refine ⟨m,?_⟩
  have h := autocorrelation_le_peak_excess q hq t ht m (fun k => hmall k (Finset.mem_univ k))
  linarith

/-- Stronger than the displayed paper lower bound; its proof uses only a
single nonzero Fourier lag and exact normalization. -/
theorem exists_table_peak (q : Ix d → ℂ) (hq : UnitPhases q)
    (t : Ix d) (ht : t≠0) :
    ∃ a b,1/(d : ℝ)^2+‖autocorrelation q t‖/(d : ℝ)^3≤fourierTable q a b := by
  obtain ⟨m,hm⟩ := exists_power_peak q hq t ht
  refine ⟨-m,0,?_⟩
  simp only [fourierTable,add_zero,neg_neg]
  have hd : (d : ℝ)>0 := dimension_pos
  have h := (div_le_div_iff_of_pos_right (pow_pos hd 3)).mpr hm
  convert h using 1 <;> field_simp <;> ring

/-- The manuscript's quantitative bound, on an actual Born probability. -/
theorem swappedTarget_quantitative (hd : 4≤d) :
    ∃ a b,1/(d : ℝ)^2+
      2*Real.sin (Real.pi/(d : ℝ))*Real.sin (3*Real.pi/(d : ℝ))/
        ((d : ℝ)^2*((d : ℝ)-1)) ≤ swappedTarget d a b := by
  obtain ⟨a,b,hab⟩ := exists_table_peak (swappedPhase : Ix d → ℂ) swappedPhase_unit 2
    (natCast_ne_zero_of_lt (d := d) (k := 2) (by omega) (by omega))
  rw [swapped_R2_norm hd] at hab
  refine ⟨a,b,?_⟩
  rw [swappedTarget_fourier]
  apply le_trans ?_ hab
  have hdR : (4 : ℝ)≤d := by exact_mod_cast hd
  have hs₁ := sine_step_positive (d := d) (k := 1) (by omega) (by omega)
  have hs₃ := sine_step_positive (d := d) (k := 3) (by omega) (by omega)
  have hS : 0≤Real.sin (Real.pi/(d : ℝ))*Real.sin (3*Real.pi/(d : ℝ)) := by
    simpa [mul_comm] using mul_nonneg hs₁.le hs₃.le
  apply add_le_add_left
  apply (div_le_div_iff₀ (mul_pos (pow_pos (by linarith : (0 : ℝ)<d) 2) (by linarith))
    (pow_pos (by linarith : (0 : ℝ)<d) 3)).mpr
  nlinarith [mul_nonneg hS (show (0 : ℝ)≤(d : ℝ)^2*((d : ℝ)-2) from mul_nonneg (sq_nonneg _) (by linarith))]

theorem quantitative_gap_positive (hd : 4≤d) :
    1/(d : ℝ)^2 < 1/(d : ℝ)^2+
      2*Real.sin (Real.pi/(d : ℝ))*Real.sin (3*Real.pi/(d : ℝ))/
        ((d : ℝ)^2*((d : ℝ)-1)) := by
  apply lt_add_of_pos_right
  have hdR : (4 : ℝ)≤d := by exact_mod_cast hd
  have hs₁ := sine_step_positive (d := d) (k := 1) (by omega) (by omega)
  have hs₃ := sine_step_positive (d := d) (k := 3) (by omega) (by omega)
  apply div_pos
  · simpa [mul_comm,mul_left_comm,mul_assoc] using mul_pos (mul_pos (by norm_num : (0 : ℝ)<2) hs₁) hs₃
  · exact mul_pos (pow_pos (by linarith) 2) (by linarith)

/-- Any local output relabeling preserves uniformity, so the canonical and
swapped targets are inequivalent under such relabelings. -/
theorem no_uniform_relabeling (hd : 4≤d) (α β : Equiv.Perm (Ix d)) :
    ¬ ∀ a b,swappedTarget d (α a) (β b)=1/(d : ℝ)^2 := by
  intro h
  apply swappedTarget_not_uniform hd
  intro a b
  simpa using h (α.symm a) (β.symm b)

end CyclicBell.General
