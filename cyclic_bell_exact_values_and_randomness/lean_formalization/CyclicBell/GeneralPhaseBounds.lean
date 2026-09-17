import CyclicBell.GeneralPhaseTables
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds

/-! Exact maxima and nonuniformity of the physical settings-appendix tables.
These are properties of an explicit realization, not a self-testing theorem
or a no-go theorem for all two-input experiments. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

theorem phase_sin_sq_integer_shift (u : ℝ) (n : ℤ) :
    Real.sin (Real.pi*((n : ℝ)+u))^2=Real.sin (Real.pi*u)^2 := by
  have hc : Real.cos ((n : ℝ)*Real.pi)^2=1 := by
    nlinarith [Real.sin_sq_add_cos_sq ((n : ℝ)*Real.pi),Real.sin_int_mul_pi n]
  rw [show Real.pi*((n : ℝ)+u)=Real.pi*u+(n : ℝ)*Real.pi by ring,
    Real.sin_add,Real.sin_int_mul_pi]
  simp only [mul_zero,add_zero,mul_pow,hc,mul_one]

/-- Folding an arbitrary lifted output difference into [0,d) does not make its
fractional part zero. No assertion about a nearest representative is assumed. -/
theorem phase_fractional_sine_lower (hd : 2≤d) (q r : ℕ)
    (hq : 2≤q) (hr : 1≤r) (hrq : r<q) (n : ℤ) :
    0<Real.sin (Real.pi/((q : ℝ)*d))^2 ∧
    Real.sin (Real.pi/((q : ℝ)*d))^2≤
      Real.sin (Real.pi*((n : ℝ)+(r : ℝ)/q)/(d : ℝ))^2 := by
  have hD : 0<(d : ℝ) := dimension_pos
  have hQ : 0<(q : ℝ) := by exact_mod_cast (show 0<q by omega)
  have hD2 : (2 : ℝ)≤d := by exact_mod_cast hd
  have hQ2 : (2 : ℝ)≤q := by exact_mod_cast hq
  have hrR : (1 : ℝ)≤r := by exact_mod_cast hr
  have hrqR : (r : ℝ)+1≤q := by exact_mod_cast (Nat.succ_le_of_lt hrq)
  let t : ℝ := (n : ℝ)+(r : ℝ)/q
  let k : ℤ := ⌊t/(d : ℝ)⌋
  let z : ℤ := n-(d : ℤ)*k
  let u : ℝ := (z : ℝ)+(r : ℝ)/q
  have hu : u=t-(k : ℝ)*d := by dsimp [u,t,z] <;> push_cast <;> ring
  have hlo : 0≤u := by
    have h := (le_div_iff₀ hD).mp (Int.floor_le (t/(d : ℝ)))
    change (k : ℝ)*d≤t at h
    rw [hu]
    linarith
  have hhi : u<(d : ℝ) := by
    have h := (div_lt_iff₀ hD).mp (Int.lt_floor_add_one (t/(d : ℝ)))
    change t<((k : ℝ)+1)*d at h
    rw [hu]
    linarith
  have hfpos : 0<(r : ℝ)/q := div_pos (by linarith) hQ
  have hfless : (r : ℝ)/q<1 := (div_lt_one hQ).mpr (by linarith)
  have hzlo : 0≤z := by
    by_contra hz
    have h : (z : ℝ)≤-1 := by exact_mod_cast (show z≤-1 by omega)
    dsimp [u] at hlo
    linarith
  have hzhi : z≤(d : ℤ)-1 := by
    by_contra hz
    have h : (d : ℝ)≤z := by exact_mod_cast (show (d : ℤ)≤z by omega)
    dsimp [u] at hhi
    linarith
  have hfraclo : 1/(q : ℝ)≤(r : ℝ)/q :=
    div_le_div_of_nonneg_right hrR hQ.le
  have hfrachi : (r : ℝ)/q≤1-1/(q : ℝ) := by
    apply (div_le_iff₀ hQ).mpr
    have h : (1-1/(q : ℝ))*q=(q : ℝ)-1 := by field_simp <;> ring
    rw [h]
    linarith
  have hub : 1/(q : ℝ)≤u ∧ u≤(d : ℝ)-1/(q : ℝ) := by
    have hzloR : (0 : ℝ)≤z := by exact_mod_cast hzlo
    have hzhiR : (z : ℝ)≤(d : ℝ)-1 := by exact_mod_cast hzhi
    dsimp [u]
    constructor <;> linarith
  let a := Real.pi/((q : ℝ)*d)
  let x := Real.pi*u/(d : ℝ)
  have ha : 0<a := by dsimp [a]; positivity
  have haπ : a<Real.pi := by
    dsimp [a]
    exact div_lt_self Real.pi_pos (by nlinarith)
  have hx : a≤x ∧ x≤Real.pi-a := by
    have hm0 := mul_le_mul_of_nonneg_left hub.1 Real.pi_pos.le
    have hm1 := mul_le_mul_of_nonneg_left hub.2 Real.pi_pos.le
    dsimp [a,x]
    constructor
    · apply (le_div_iff₀ hD).mpr
      convert hm0 using 1 <;> field_simp <;> ring
    · apply (div_le_iff₀ hD).mpr
      convert hm1 using 1 <;> field_simp <;> ring
  have hsinpos : 0<Real.sin a := Real.sin_pos_of_pos_of_lt_pi ha haπ
  have hsin : Real.sin a≤Real.sin x := by
    by_cases hxhalf : x≤Real.pi/2
    · exact Real.sin_le_sin_of_le_of_le_pi_div_two (by linarith [Real.pi_pos]) hxhalf hx.1
    · have h := Real.sin_le_sin_of_le_of_le_pi_div_two
        (show -(Real.pi/2)≤a by linarith [Real.pi_pos])
        (show Real.pi-x≤Real.pi/2 by linarith)
        (show a≤Real.pi-x by linarith [hx.2])
      simpa only [Real.sin_pi_sub] using h
  have hsq : Real.sin a^2≤Real.sin x^2 := by
    nlinarith [mul_nonneg (sub_nonneg.mpr hsin)
      (add_nonneg hsinpos.le (hsinpos.le.trans hsin))]
  have hperiod : Real.sin (Real.pi*t/d)^2=Real.sin x^2 := by
    have ht : t/(d : ℝ)=(k : ℝ)+u/(d : ℝ) := by
      rw [hu]; field_simp <;> ring
    rw [show Real.pi*t/d=Real.pi*(t/(d : ℝ)) by ring,ht,phase_sin_sq_integer_shift]
    dsimp [x]
    rw [mul_div_assoc]
  exact ⟨by dsimp [a] at hsinpos; positivity,by change _≤Real.sin (Real.pi*t/d)^2; rw [hperiod]; exact hsq⟩

def standardAlpha (x : Fin 2) : ℝ := if x=0 then 0 else -1/2
def standardBeta (y : Fin 2) : ℝ := if y=0 then -1/4 else -3/4
def standardDelta (x y : Fin 2) : ℝ := standardAlpha x-standardBeta y

def standardPhaseStrategy (d : ℕ) [NeZero d] :
    StrategyOn d (Fin 2) (Fin 2) (Ix d) (Ix d) where
  state := entangledState d
  alice x := phaseAlice (standardAlpha x)
  bob y := phaseBob (standardBeta y)

def standardPeak (d : ℕ) : ℝ :=
  (1/2 : ℝ)/((d : ℝ)^3*Real.sin (Real.pi/(4*(d : ℝ)))^2)

def anchorPeak (d : ℕ) : ℝ :=
  1/((d : ℝ)^3*Real.sin (Real.pi/(2*(d : ℝ)))^2)

theorem standard_delta_table :
    standardDelta 0 0=1/4 ∧ standardDelta 0 1=3/4 ∧
    standardDelta 1 0= -1/4 ∧ standardDelta 1 1=1/4 := by
  norm_num [standardDelta,standardAlpha,standardBeta]

theorem standard_displacement_rep (x y : Fin 2) (a b : Ix d) :
    ∃ n : ℤ,∃ r : ℕ,1≤r ∧ r<4 ∧
      (a.val : ℝ)-(b.val : ℝ)+standardDelta x y=(n : ℝ)+(r : ℝ)/4 := by
  fin_cases x <;> fin_cases y
  · refine ⟨(a.val : ℤ)-b.val,1,by omega,by omega,?_⟩
    norm_num [standardDelta,standardAlpha,standardBeta] <;> push_cast <;> ring
  · refine ⟨(a.val : ℤ)-b.val,3,by omega,by omega,?_⟩
    norm_num [standardDelta,standardAlpha,standardBeta] <;> push_cast <;> ring
  · refine ⟨(a.val : ℤ)-b.val-1,3,by omega,by omega,?_⟩
    norm_num [standardDelta,standardAlpha,standardBeta] <;> push_cast <;> ring
  · refine ⟨(a.val : ℤ)-b.val,1,by omega,by omega,?_⟩
    norm_num [standardDelta,standardAlpha,standardBeta] <;> push_cast <;> ring

theorem standard_denominator_positive (hd : 2≤d) (x y : Fin 2) (a b : Ix d) :
    0<Real.sin (Real.pi*((a.val : ℝ)-(b.val : ℝ)+standardDelta x y)/d)^2 := by
  obtain ⟨n,r,hr,hr4,he⟩ := standard_displacement_rep x y a b
  rw [he]
  exact (phase_fractional_sine_lower hd 4 r (by omega) hr hr4 n).1.trans_le
    (phase_fractional_sine_lower hd 4 r (by omega) hr hr4 n).2

theorem standard_numerator (x y : Fin 2) (a b : Ix d) :
    Real.sin (Real.pi*((a.val : ℝ)-(b.val : ℝ)+standardDelta x y))^2=1/2 := by
  have he : (a.val : ℝ)-(b.val : ℝ)+standardDelta x y=
      (((a.val : ℤ)-b.val : ℤ) : ℝ)+standardDelta x y := by push_cast; ring
  rw [he,phase_sin_sq_integer_shift]
  have hquarter : Real.sin (Real.pi/4)^2=(1/2 : ℝ) := by
    rw [Real.sin_pi_div_four,div_pow,Real.sq_sqrt (by norm_num : (0 : ℝ)≤2)]
    norm_num
  fin_cases x <;> fin_cases y <;> norm_num [standardDelta,standardAlpha,standardBeta]
  · rw [show Real.pi*(1/4 : ℝ)=Real.pi/4 by ring]
    exact hquarter
  · rw [
      show Real.pi*(3/4 : ℝ)=Real.pi-Real.pi/4 by ring,Real.sin_pi_sub]
    exact hquarter
  · rw [show Real.pi*(1/4 : ℝ)=Real.pi/4 by ring]
    exact hquarter
  · rw [show Real.pi*(1/4 : ℝ)=Real.pi/4 by ring]
    exact hquarter

/-- The manuscript's four displayed tables, not a surrogate table definition. -/
theorem standard_behavior_formula (hd : 2≤d) (x y : Fin 2) (a b : Ix d) :
    behavior (standardPhaseStrategy d) x y a b=
      (1/2 : ℝ)/((d : ℝ)^3*Real.sin
        (Real.pi*((a.val : ℝ)-(b.val : ℝ)+standardDelta x y)/d)^2) := by
  change phasePairProbability (standardAlpha x) (standardBeta y) a b=_
  have hn : Real.sin (Real.pi*((a.val : ℝ)-(b.val : ℝ)+standardAlpha x-standardBeta y)/d)≠0 := by
    intro h
    have hp := standard_denominator_positive hd x y a b
    have he : (a.val : ℝ)-(b.val : ℝ)+standardDelta x y=
        (a.val : ℝ)-(b.val : ℝ)+standardAlpha x-standardBeta y := by unfold standardDelta; ring
    rw [he,h] at hp
    norm_num at hp
  rw [phasePair_sine_formula _ _ _ _ hn]
  have he : (a.val : ℝ)-(b.val : ℝ)+standardAlpha x-standardBeta y=
      (a.val : ℝ)-(b.val : ℝ)+standardDelta x y := by unfold standardDelta; ring
  rw [sineKernel,he,standard_numerator]

theorem standard_behavior_le_peak (hd : 2≤d) (x y : Fin 2) (a b : Ix d) :
    behavior (standardPhaseStrategy d) x y a b≤standardPeak d := by
  obtain ⟨n,r,hr,hr4,he⟩ := standard_displacement_rep x y a b
  obtain ⟨hpos,hbound⟩ := phase_fractional_sine_lower hd 4 r (by omega) hr hr4 n
  rw [standard_behavior_formula hd,he]
  unfold standardPeak
  have hden0 : 0<(d : ℝ)^3*Real.sin (Real.pi/(4*(d : ℝ)))^2 := by positivity
  have hden1 : 0<(d : ℝ)^3*Real.sin (Real.pi*((n : ℝ)+(r : ℝ)/4)/d)^2 := by
    exact mul_pos (pow_pos dimension_pos _) (hpos.trans_le hbound)
  apply (div_le_div_iff₀ hden1 hden0).mpr
  exact mul_le_mul_of_nonneg_left
    (mul_le_mul_of_nonneg_left hbound (pow_nonneg dimension_pos.le _)) (by norm_num)

theorem standard_behavior_hits_peak (hd : 2≤d) (x y : Fin 2) :
    ∃ a b : Ix d,behavior (standardPhaseStrategy d) x y a b=standardPeak d := by
  have hv : (1 : Ix d).val=1 := by
    rw [ZMod.val_one_eq_one_mod,Nat.mod_eq_of_lt (by omega)]
  have hquarter (t : ℝ) (ht : t=1/4 ∨ t= -(1/4)) :
      (1/2 : ℝ)/((d : ℝ)^3*Real.sin (Real.pi*t/d)^2)=standardPeak d := by
    rcases ht with rfl | rfl
    · rw [show Real.pi*(1/4 : ℝ)/d=Real.pi/(4*(d : ℝ)) by ring]
      rfl
    · rw [show Real.pi*(-(1/4) : ℝ)/d= -(Real.pi/(4*(d : ℝ))) by ring,
        Real.sin_neg,neg_sq]
      rfl
  fin_cases x <;> fin_cases y
  · refine ⟨0,0,?_⟩
    rw [standard_behavior_formula hd]
    apply hquarter
    left
    norm_num [standardDelta,standardAlpha,standardBeta]
  · refine ⟨0,1,?_⟩
    rw [standard_behavior_formula hd]
    apply hquarter
    right
    norm_num [standardDelta,standardAlpha,standardBeta,hv]
  · refine ⟨0,0,?_⟩
    rw [standard_behavior_formula hd]
    apply hquarter
    right
    norm_num [standardDelta,standardAlpha,standardBeta]
  · refine ⟨0,0,?_⟩
    rw [standard_behavior_formula hd]
    apply hquarter
    left
    norm_num [standardDelta,standardAlpha,standardBeta]

theorem standardPeak_gt_uniform (hd : 2≤d) : 1/(d : ℝ)^2<standardPeak d := by
  have hD : 0<(d : ℝ) := dimension_pos
  have hD2 : (2 : ℝ)≤d := by exact_mod_cast hd
  let t := Real.pi/(4*(d : ℝ))
  have ht : 0<t := by dsimp [t]; positivity
  have hs := Real.sin_sq_lt_sq (ne_of_gt ht)
  have hp2 : Real.pi^2≤16 := by nlinarith [Real.pi_pos,Real.pi_le_four]
  have he : 2*(d : ℝ)*t^2=Real.pi^2/(8*(d : ℝ)) := by dsimp [t]; field_simp <;> ring
  have hsmall : 2*(d : ℝ)*Real.sin t^2<1 := by
    have hh := mul_lt_mul_of_pos_left hs (show 0<2*(d : ℝ) by positivity)
    rw [he] at hh
    have hh' : Real.pi^2/(8*(d : ℝ))≤1 := (div_le_one (by positivity)).mpr (by nlinarith)
    exact hh.trans_le hh'
  have hsinpos : 0<Real.sin t := by
    apply Real.sin_pos_of_pos_of_lt_pi ht
    dsimp [t]
    exact div_lt_self Real.pi_pos (by linarith)
  unfold standardPeak
  change 1/(d : ℝ)^2<(1/2 : ℝ)/((d : ℝ)^3*Real.sin t^2)
  apply (div_lt_div_iff₀ (by positivity) (by positivity)).mpr
  nlinarith [mul_pos (show 0<(d : ℝ)^2 by positivity) (sub_pos.mpr hsmall)]

/-- Complete physical statement for every standard input pair; no self-testing
or adversarial privacy claim is made. -/
theorem standard_tables_nonuniform (hd : 2≤d) (x y : Fin 2) :
    (∀ a b : Ix d,behavior (standardPhaseStrategy d) x y a b≤standardPeak d) ∧
    (∃ a b : Ix d,behavior (standardPhaseStrategy d) x y a b=standardPeak d) ∧
    1/(d : ℝ)^2<standardPeak d ∧
    ¬(∀ a b : Ix d,behavior (standardPhaseStrategy d) x y a b=1/(d : ℝ)^2) := by
  have hh := standard_behavior_hits_peak hd x y
  have hg := standardPeak_gt_uniform hd
  refine ⟨standard_behavior_le_peak hd x y,hh,hg,?_⟩
  intro hu
  obtain ⟨a,b,hab⟩ := hh
  rw [hu] at hab
  linarith

end CyclicBell.General
