import CyclicBell.GeneralPhaseBounds

/-! The third Bob measurement is explicitly appended to the preceding four
physical tables. Its matching and cross-table conclusions are about this
construction only. They do not exclude another third-setting design.
Uncompiled proof-source candidates. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def anchoredStandardStrategy (d : ℕ) [NeZero d] (c : Fin 2) :
    StrategyOn d (Fin 2) (Option (Fin 2)) (Ix d) (Ix d) where
  state := entangledState d
  alice x := phaseAlice (standardAlpha x)
  bob y := match y with
    | some y => phaseBob (standardBeta y)
    | none => phaseBob (standardAlpha c)

theorem anchored_preserves_standard (c x y : Fin 2) (a b : Ix d) :
    behavior (anchoredStandardStrategy d c) x (some y) a b=
      behavior (standardPhaseStrategy d) x y a b := rfl

theorem anchored_matching (c : Fin 2) (a b : Ix d) :
    behavior (anchoredStandardStrategy d c) c none a b=
      if a=b then 1/(d : ℝ) else 0 :=
  phasePair_equal_offsets (standardAlpha c) a b

theorem anchor_displacement_rep (c x : Fin 2) (hxc : x≠c) (a b : Ix d) :
    ∃ n : ℤ,(a.val : ℝ)-(b.val : ℝ)+standardAlpha x-standardAlpha c=(n : ℝ)+1/2 := by
  fin_cases c <;> fin_cases x
  · exact (hxc rfl).elim
  · refine ⟨(a.val : ℤ)-b.val-1,?_⟩
    norm_num [standardAlpha]; push_cast; ring
  · refine ⟨(a.val : ℤ)-b.val,?_⟩
    norm_num [standardAlpha]; push_cast; ring
  · exact (hxc rfl).elim

theorem anchored_cross_formula (hd : 2≤d) (c x : Fin 2) (hxc : x≠c) (a b : Ix d) :
    behavior (anchoredStandardStrategy d c) x none a b=
      1/((d : ℝ)^3*Real.sin (Real.pi*
        ((a.val : ℝ)-(b.val : ℝ)+standardAlpha x-standardAlpha c)/d)^2) := by
  obtain ⟨n,he⟩ := anchor_displacement_rep c x hxc a b
  have hl := phase_fractional_sine_lower hd 2 1 (by omega) (by omega) (by omega) n
  have hn : Real.sin (Real.pi*((a.val : ℝ)-(b.val : ℝ)+standardAlpha x-standardAlpha c)/d)≠0 := by
    intro hz
    rw [he] at hz
    have hp := hl.1.trans_le hl.2
    norm_num [hz] at hp
  change phasePairProbability (standardAlpha x) (standardAlpha c) a b=_
  rw [phasePair_sine_formula _ _ _ _ hn,sineKernel]
  have hnumer : Real.sin (Real.pi*((a.val : ℝ)-(b.val : ℝ)+standardAlpha x-standardAlpha c))^2=1 := by
    rw [he,phase_sin_sq_integer_shift]
    rw [show Real.pi*(1/2 : ℝ)=Real.pi/2 by ring,Real.sin_pi_div_two,one_pow]
  rw [hnumer]

theorem anchored_cross_le_peak (hd : 2≤d) (c x : Fin 2) (hxc : x≠c) (a b : Ix d) :
    behavior (anchoredStandardStrategy d c) x none a b≤anchorPeak d := by
  obtain ⟨n,he⟩ := anchor_displacement_rep c x hxc a b
  have hl := phase_fractional_sine_lower hd 2 1 (by omega) (by omega) (by omega) n
  rw [anchored_cross_formula hd c x hxc,he]
  unfold anchorPeak
  have h0 : 0<(d : ℝ)^3*Real.sin (Real.pi/(2*(d : ℝ)))^2 := by positivity
  have h1 : 0<(d : ℝ)^3*Real.sin (Real.pi*((n : ℝ)+1/2)/d)^2 :=
    mul_pos (pow_pos dimension_pos _) (by simpa using hl.1.trans_le hl.2)
  apply (div_le_div_iff₀ h1 h0).mpr
  simpa only [one_mul] using
    mul_le_mul_of_nonneg_left hl.2 (pow_nonneg dimension_pos.le 3)

theorem anchored_cross_hits_peak (hd : 2≤d) (c x : Fin 2) (hxc : x≠c) :
    behavior (anchoredStandardStrategy d c) x none (0 : Ix d) 0=anchorPeak d := by
  rw [anchored_cross_formula hd c x hxc]
  fin_cases c <;> fin_cases x
  · exact (hxc rfl).elim
  · norm_num [standardAlpha]
    rw [show Real.pi*(-(1/2) : ℝ)/d= -(Real.pi/(2*(d : ℝ))) by ring,Real.sin_neg,neg_sq]
    rfl
  · simp [standardAlpha,anchorPeak,div_eq_mul_inv,mul_assoc]
  · exact (hxc rfl).elim

theorem anchorPeak_gt_uniform (hd : 3≤d) : 1/(d : ℝ)^2<anchorPeak d := by
  by_cases h3 : d=3
  · subst d
    norm_num [anchorPeak,show Real.pi/(2*(3 : ℝ))=Real.pi/6 by ring,Real.sin_pi_div_six]
  have hD : 0<(d : ℝ) := dimension_pos
  have hD4 : (4 : ℝ)≤d := by exact_mod_cast (show 4≤d by omega)
  let t := Real.pi/(2*(d : ℝ))
  have ht : 0<t := by dsimp [t]; positivity
  have hs := Real.sin_sq_lt_sq (ne_of_gt ht)
  have hp2 : Real.pi^2≤16 := by nlinarith [Real.pi_pos,Real.pi_le_four]
  have he : (d : ℝ)*t^2=Real.pi^2/(4*(d : ℝ)) := by dsimp [t]; field_simp; ring
  have hsmall : (d : ℝ)*Real.sin t^2<1 := by
    have hh := mul_lt_mul_of_pos_left hs hD
    rw [he] at hh
    have hh' : Real.pi^2/(4*(d : ℝ))≤1 := (div_le_one (by positivity)).mpr (by nlinarith)
    exact hh.trans_le hh'
  have hsinpos : 0<Real.sin t := by
    apply Real.sin_pos_of_pos_of_lt_pi ht
    dsimp [t]
    exact div_lt_self Real.pi_pos (by linarith)
  unfold anchorPeak
  change 1/(d : ℝ)^2<1/((d : ℝ)^3*Real.sin t^2)
  apply (div_lt_div_iff₀ (by positivity) (by positivity)).mpr
  nlinarith [mul_pos (show 0<(d : ℝ)^2 by positivity) (sub_pos.mpr hsmall)]

theorem anchored_cross_nonuniform (hd : 3≤d) (c x : Fin 2) (hxc : x≠c) :
    (∀ a b : Ix d,behavior (anchoredStandardStrategy d c) x none a b≤anchorPeak d) ∧
    behavior (anchoredStandardStrategy d c) x none (0 : Ix d) 0=anchorPeak d ∧
    1/(d : ℝ)^2<anchorPeak d ∧
    ¬(∀ a b : Ix d,behavior (anchoredStandardStrategy d c) x none a b=1/(d : ℝ)^2) := by
  have hh := anchored_cross_hits_peak (by omega : 2≤d) c x hxc
  have hg := anchorPeak_gt_uniform hd
  refine ⟨anchored_cross_le_peak (by omega) c x hxc,hh,hg,?_⟩
  intro hu
  rw [hu] at hh
  linarith

/-- The d=2 exception is an equality statement for every entry, not an
extrapolation from the maximum alone. -/
theorem anchored_qubit_cross_uniform (c x : Fin 2) (hxc : x≠c) (a b : Ix 2) :
    behavior (anchoredStandardStrategy 2 c) x none a b=1/4 := by
  rw [anchored_cross_formula (by omega) c x hxc]
  fin_cases c <;> fin_cases x <;> try exact (hxc rfl).elim
  all_goals fin_cases a <;> fin_cases b <;> norm_num [standardAlpha]
  all_goals first
    | rw [show Real.pi*(-(1/2) : ℝ)/2= -(Real.pi/4) by ring,Real.sin_neg,neg_sq,Real.sin_pi_div_four]; norm_num
    | rw [show Real.pi*(1/2 : ℝ)/2=Real.pi/4 by ring,Real.sin_pi_div_four]; norm_num
    | rw [show Real.pi*(3/2 : ℝ)/2=Real.pi-Real.pi/4 by ring,Real.sin_pi_sub,Real.sin_pi_div_four]; norm_num
    | rw [show Real.pi*(-(3/2) : ℝ)/2= -(Real.pi-Real.pi/4) by ring,Real.sin_neg,neg_sq,Real.sin_pi_sub,Real.sin_pi_div_four]; norm_num

end CyclicBell.General
