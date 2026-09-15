import CyclicBell.GeneralAnchoredTables
import Mathlib.Analysis.Calculus.Deriv.Slope
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecificLimits.Basic

/-! Scalar min-entropy of the explicit standard tables, with the o(1) claim
stated as a literal sequential limit. This is not conditional entropy against
an adversary and does not use a Bell self-testing theorem. Uncompiled source. -/
noncomputable section
open scoped BigOperators Topology
open Filter
namespace CyclicBell.General

def standardJointMinEntropy (d : ℕ) : ℝ := -Real.log (standardPeak d)/Real.log 2

theorem standard_peak_literal (d : ℕ) :
    standardPeak d=1/(2*(d : ℝ)^3*Real.sin (Real.pi/(4*(d : ℝ)))^2) := by
  unfold standardPeak
  ring

theorem standard_entropy_exact (d : ℕ) :
    standardJointMinEntropy d=
      Real.log (2*(d : ℝ)^3*Real.sin (Real.pi/(4*(d : ℝ)))^2)/Real.log 2 := by
  rw [standardJointMinEntropy,standard_peak_literal,one_div,Real.log_inv]
  ring

/-- The attained entry really gives the min-entropy of every table. -/
theorem standard_table_entropy_package (d : ℕ) [NeZero d] (hd : 2≤d) (x y : Fin 2) :
    (∀ a b : Ix d,behavior (standardPhaseStrategy d) x y a b≤standardPeak d) ∧
    (∃ a b : Ix d,behavior (standardPhaseStrategy d) x y a b=standardPeak d) ∧
    standardJointMinEntropy d=
      Real.log (2*(d : ℝ)^3*Real.sin (Real.pi/(4*(d : ℝ)))^2)/Real.log 2 :=
  ⟨standard_behavior_le_peak hd x y,standard_behavior_hits_peak hd x y,standard_entropy_exact d⟩

theorem standard_entropy_gap_identity (d : ℕ) [NeZero d] (hd : 2≤d) :
    standardJointMinEntropy d-Real.log (d : ℝ)/Real.log 2=
      Real.log (2*((d : ℝ)*Real.sin (Real.pi/(4*(d : ℝ))))^2)/Real.log 2 := by
  have hd0 : (d : ℝ)≠0 := ne_of_gt (dimension_pos (d := d))
  have hs : 0<Real.sin (Real.pi/(4*(d : ℝ)))^2 :=
    (phase_fractional_sine_lower hd 4 1 (by omega) (by omega) (by omega) 0).1
  have hprod : 2*((d : ℝ)*Real.sin (Real.pi/(4*(d : ℝ))))^2≠0 := by
    rw [mul_pow]
    positivity
  rw [standard_entropy_exact]
  have he : 2*(d : ℝ)^3*Real.sin (Real.pi/(4*(d : ℝ)))^2=
      (d : ℝ)*(2*((d : ℝ)*Real.sin (Real.pi/(4*(d : ℝ))))^2) := by ring
  rw [he,Real.log_mul hd0 hprod]
  ring

/-- Punctured limit, necessary because Lean's real division has 0/0=0. -/
theorem phase_sine_over_argument_limit :
    Tendsto (fun x : ℝ => Real.sin x/x) (nhdsWithin 0 ({0}ᶜ : Set ℝ)) (nhds 1) := by
  simpa only [Real.cos_zero,zero_add,Real.sin_zero,sub_zero,smul_eq_mul,
    div_eq_mul_inv,mul_comm] using (Real.hasDerivAt_sin 0).tendsto_slope_zero

theorem phase_scaled_sine_limit :
    Tendsto (fun n : ℕ => (n : ℝ)*Real.sin (Real.pi/(4*(n : ℝ)))) atTop (nhds (Real.pi/4)) := by
  let t : ℕ → ℝ := fun n => (Real.pi/4)/(n : ℝ)
  have ht : Tendsto t atTop (nhds 0) := tendsto_const_div_atTop_nhds_zero_nat _
  have htnz : ∀ᶠ n : ℕ in atTop,t n≠0 := by
    filter_upwards [eventually_ge_atTop 1] with n hn
    have hnR : (0 : ℝ)<n := by exact_mod_cast (show 0<n by omega)
    exact ne_of_gt (div_pos (div_pos Real.pi_pos (by norm_num)) hnR)
  have htp : Tendsto t atTop (nhdsWithin 0 ({0}ᶜ : Set ℝ)) := by
    rw [nhdsWithin]
    exact tendsto_inf.mpr ⟨ht,tendsto_principal.mpr (by simpa using htnz)⟩
  have hratio := phase_sine_over_argument_limit.comp htp
  have hscaled := hratio.const_mul (Real.pi/4)
  have he : (fun n : ℕ => (Real.pi/4)*(Real.sin (t n)/t n))=
      (fun n : ℕ => (n : ℝ)*Real.sin (Real.pi/(4*(n : ℝ)))) := by
    funext n
    by_cases hn : n=0
    · simp [hn,t]
    · have hnR : (n : ℝ)≠0 := by exact_mod_cast hn
      have htR : t n≠0 := div_ne_zero (by positivity) hnR
      have harg : t n=Real.pi/(4*(n : ℝ)) := by dsimp [t]; ring
      rw [harg]
      field_simp [hnR,ne_of_gt Real.pi_pos]
  simpa only [Function.comp_def,mul_one,he] using hscaled

/-- Exactly the asymptotic statement in app:settings, in difference-limit form.
The finitely many small dimensions do not determine the limit. -/
theorem standard_entropy_asymptotic :
    Tendsto (fun d : ℕ => standardJointMinEntropy d-Real.log (d : ℝ)/Real.log 2)
      atTop (nhds (Real.log (Real.pi^2/8)/Real.log 2)) := by
  have hsq := (phase_scaled_sine_limit.pow 2).const_mul 2
  have hconstant : 2*(Real.pi/4)^2=Real.pi^2/8 := by ring
  rw [hconstant] at hsq
  have hlog := (Real.continuousAt_log (by positivity : Real.pi^2/8≠0)).tendsto.comp hsq
  have hdiv := hlog.div_const (Real.log 2)
  apply hdiv.congr'
  filter_upwards [eventually_ge_atTop 2] with d hd
  letI : NeZero d := ⟨by omega⟩
  exact (standard_entropy_gap_identity d hd).symm

end CyclicBell.General
