import CyclicBell.GeneralScalar
noncomputable section
namespace CyclicBell.General
theorem scalarMaximum_two : scalarMaximum 2=2*Real.sqrt 2 := by
  have h : Real.sqrt 2≠0 := ne_of_gt (Real.sqrt_pos.mpr (by norm_num))
  change 2/Real.sin (Real.pi/(2*(2 : ℝ)))=2*Real.sqrt 2
  norm_num only [show (2:ℝ)*2=4 by norm_num]
  rw [Real.sin_pi_div_four]
  field_simp [h]
  nlinarith [Real.sq_sqrt (show (0:ℝ)≤2 by norm_num)]

theorem scalarMaximum_three : scalarMaximum 3=4 := by
  change 2/Real.sin (Real.pi/(2*(3 : ℝ)))=4
  norm_num

/-- A rationalization identity needed for the d=4 radical in the manuscript. -/
theorem sqrt_four_radical_product :
    Real.sqrt (2-Real.sqrt 2)*Real.sqrt (4+2*Real.sqrt 2)=2 := by
  have hk0 : 0≤Real.sqrt 2 := Real.sqrt_nonneg _
  have hk2 : (Real.sqrt 2)^2=2 := Real.sq_sqrt (by norm_num)
  have hklt : Real.sqrt 2<2 := by nlinarith
  have ha : 0≤2-Real.sqrt 2 := by linarith
  have hb : 0≤4+2*Real.sqrt 2 := by positivity
  have hprod : (Real.sqrt (2-Real.sqrt 2)*Real.sqrt (4+2*Real.sqrt 2))^2=4 := by
    rw [mul_pow,Real.sq_sqrt ha,Real.sq_sqrt hb]
    nlinarith [hk2]
  have hnonneg := mul_nonneg (Real.sqrt_nonneg (2-Real.sqrt 2))
    (Real.sqrt_nonneg (4+2*Real.sqrt 2))
  nlinarith

theorem scalarMaximum_four : scalarMaximum 4=2*Real.sqrt (4+2*Real.sqrt 2) := by
  have hk : Real.sqrt 2<2 := by
    have h0 := Real.sqrt_nonneg (2:ℝ)
    have h2 := Real.sq_sqrt (show (0:ℝ)≤2 by norm_num)
    nlinarith
  have ha : Real.sqrt (2-Real.sqrt 2)≠0 := ne_of_gt (Real.sqrt_pos.mpr (by linarith))
  change 2/Real.sin (Real.pi/(2*(4 : ℝ)))=2*Real.sqrt (4+2*Real.sqrt 2)
  norm_num only [show (2:ℝ)*4=8 by norm_num]
  rw [Real.sin_pi_div_eight]
  field_simp [ha]
  nlinarith [sqrt_four_radical_product]

/-- Derived from the pinned library's cos(pi/5), not a decimal identity. -/
theorem sin_pi_div_ten_exact : Real.sin (Real.pi/10)=(Real.sqrt 5-1)/4 := by
  rw [← Real.cos_pi_div_two_sub]
  rw [show Real.pi/2-Real.pi/10=2*(Real.pi/5) by ring]
  rw [Real.cos_two_mul,Real.cos_pi_div_five]
  nlinarith [Real.sq_sqrt (show (0:ℝ)≤5 by norm_num)]

theorem scalarMaximum_five : scalarMaximum 5=2*(1+Real.sqrt 5) := by
  have hk : 1<Real.sqrt 5 := by
    have h0 := Real.sqrt_nonneg (5:ℝ)
    have h2 := Real.sq_sqrt (show (0:ℝ)≤5 by norm_num)
    nlinarith
  have hn : Real.sqrt 5-1≠0 := ne_of_gt (sub_pos.mpr hk)
  change 2/Real.sin (Real.pi/(2*(5 : ℝ)))=2*(1+Real.sqrt 5)
  norm_num only [show (2:ℝ)*5=10 by norm_num]
  rw [sin_pi_div_ten_exact]
  field_simp [hn]
  nlinarith [Real.sq_sqrt (show (0:ℝ)≤5 by norm_num)]

theorem sin_pi_div_twelve_exact : Real.sin (Real.pi/12)=(Real.sqrt 6-Real.sqrt 2)/4 := by
  rw [show Real.pi/12=Real.pi/4-Real.pi/6 by ring,Real.sin_sub,
    Real.sin_pi_div_four,Real.cos_pi_div_six,Real.cos_pi_div_four,Real.sin_pi_div_six]
  have hm : Real.sqrt 2*Real.sqrt 3=Real.sqrt 6 := by
    rw [← Real.sqrt_mul (show (0:ℝ)≤2 by norm_num)]
    norm_num
  nlinarith [hm]

theorem scalarMaximum_six : scalarMaximum 6=2*(Real.sqrt 6+Real.sqrt 2) := by
  have hk : Real.sqrt 2<Real.sqrt 6 := Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have hn : Real.sqrt 6-Real.sqrt 2≠0 := ne_of_gt (sub_pos.mpr hk)
  change 2/Real.sin (Real.pi/(2*(6 : ℝ)))=2*(Real.sqrt 6+Real.sqrt 2)
  norm_num only [show (2:ℝ)*6=12 by norm_num]
  rw [sin_pi_div_twelve_exact]
  field_simp [hn]
  nlinarith [Real.sq_sqrt (show (0:ℝ)≤6 by norm_num),
    Real.sq_sqrt (show (0:ℝ)≤2 by norm_num)]

/-- All five literal exact entries in tab:exact-values. -/
theorem small_dimension_exact_value_table :
    scalarMaximum 2=2*Real.sqrt 2 ∧ scalarMaximum 3=4 ∧
    scalarMaximum 4=2*Real.sqrt (4+2*Real.sqrt 2) ∧
    scalarMaximum 5=2*(1+Real.sqrt 5) ∧ scalarMaximum 6=2*(Real.sqrt 6+Real.sqrt 2) :=
  ⟨scalarMaximum_two,scalarMaximum_three,scalarMaximum_four,scalarMaximum_five,scalarMaximum_six⟩


end CyclicBell.General
