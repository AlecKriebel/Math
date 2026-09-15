import CyclicBell.GeneralPolarPhases
import CyclicBell.GeneralGuessing

/-! Actual manuscript coefficients, including l=0 and the Fourier phase.
Normalization is derived from an explicit signed geometric sum and Parseval,
not assumed and not delegated to an external certificate. Uncompiled source. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def coefficientAngle (d : ℕ) (l : Ix d) : ℝ := Real.pi*((l.val : ℝ)-1/2)/d

def generalLambda (l : Ix d) : ℂ :=
  (-1 : ℂ)^(l.val+1)*cis (Real.pi*(l.val : ℝ)*((l.val : ℝ)-1)/d) /
    ((d : ℂ)*(Real.sin (coefficientAngle d l) : ℂ))

def secondPrefactor (l : Ix d) : ℂ :=
  cis (-Real.pi*(l.val : ℝ)*((l.val : ℝ)-1+parityDelta d)/d)

def geometricRatio (l : Ix d) : ℂ := cis (2*coefficientAngle d l)
def polarTransform (l : Ix d) : ℂ := fourier (fun k => star (polarBase k)) l

theorem sign_exponent_bridge (n : ℕ) :
    (-1 : ℂ)^((n : ℤ)-1)=(-1 : ℂ)^(n+1) := by
  cases n with
  | zero => norm_num
  | succ n =>
    have he : ((n+1 : ℕ) : ℤ)-1=(n : ℤ) := by omega
    rw [he,zpow_natCast]
    have hn : n+1+1=n+2 := by omega
    rw [hn,pow_add]
    simp

/-- Eq:lambda with integer l-1, so the exceptional-looking l=0 sign is -1. -/
theorem generalLambda_literal (l : Ix d) :
    generalLambda l = (-1 : ℂ)^((l.val : ℤ)-1)*
      Complex.exp (((Real.pi*(l.val : ℝ)*((l.val : ℝ)-1)/d : ℝ) : ℂ)*Complex.I) /
      ((d : ℂ)*(Real.sin (Real.pi*((l.val : ℝ)-(1/2 : ℝ))/d) : ℂ)) := by
  rw [sign_exponent_bridge]
  rfl

theorem sign_cis_bridge (n : ℕ) :
    (-1 : ℂ)^(n+1)=cis (Real.pi*((n : ℝ)-1)) := by
  rw [← cis_pi,cis_pow]
  have ha : ((n+1 : ℕ) : ℝ)*Real.pi=Real.pi*((n : ℝ)-1)+2*Real.pi := by
    push_cast
    ring
  rw [ha,cis_add]
  have hp : cis (2*Real.pi)=1 := by simpa using cis_period_int 1
  rw [hp,mul_one]

@[simp] theorem secondPrefactor_norm (l : Ix d) : ‖secondPrefactor l‖=1 := cis_norm _
@[simp] theorem secondPrefactor_unit (l : Ix d) : star (secondPrefactor l)*secondPrefactor l=1 := cis_unit _

theorem coefficientAngle_sin_ne_zero (hd : 2≤d) (l : Ix d) :
    Real.sin (coefficientAngle d l)≠0 := by
  by_cases hl : l.val=0
  · have he : coefficientAngle d l=-halfMesh d := by unfold coefficientAngle halfMesh; rw [hl]; ring
    rw [he,Real.sin_neg]
    exact neg_ne_zero.mpr (ne_of_gt (sin_halfMesh_pos hd))
  · have hlo : (0 : ℝ)<(l.val : ℝ)-1/2 := by
      have hi : 1≤l.val := by omega
      have hiR : (1 : ℝ)≤l.val := by exact_mod_cast hi
      linarith
    have hhi : (l.val : ℝ)-1/2<d := by
      have hiR : (l.val : ℝ)<d := by exact_mod_cast ZMod.val_lt l
      linarith
    apply ne_of_gt
    apply Real.sin_pos_of_pos_of_lt_pi
    · unfold coefficientAngle
      exact div_pos (mul_pos Real.pi_pos hlo) dimension_pos
    · unfold coefficientAngle
      exact (div_lt_iff₀ dimension_pos).mpr (mul_lt_mul_of_pos_left hhi Real.pi_pos)

theorem geometricRatio_power (l : Ix d) : geometricRatio l^d=(-1 : ℂ) := by
  rw [geometricRatio,cis_pow]
  have ha : (d : ℝ)*(2*coefficientAngle d l)=2*Real.pi*l.val-Real.pi := by
    unfold coefficientAngle
    field_simp [ne_of_gt (dimension_pos (d := d))]
    ring
  rw [ha,cis_sub]
  have hp : cis (2*Real.pi*l.val)=1 := by simpa using cis_period_int (l.val : ℤ)
  rw [hp,one_mul,cis_pi]
  simp

theorem geometricRatio_ne_one (l : Ix d) : geometricRatio l≠1 := by
  intro h
  have hp := geometricRatio_power (d := d) l
  rw [h,one_pow] at hp
  norm_num at hp

/-- A finite geometric sum identity proved by induction. -/
theorem geometric_sum_mul (u : ℂ) (n : ℕ) :
    (∑ k ∈ Finset.range n,u^k)*(u-1)=u^n-1 := by
  induction n with
  | zero => simp
  | succ n ih => rw [Finset.sum_range_succ,add_mul,ih,pow_succ]; ring

theorem signed_geometric_mul (u : ℂ) (n D : ℕ) (hn : n≤D) :
    (∑ k ∈ Finset.range D,(if k<n then u^k else -(u^k)))*(u-1)=
      2*u^n-u^D-1 := by
  have hd : D=n+(D-n) := by omega
  have hsplit : (∑ k ∈ Finset.range D,(if k<n then u^k else -(u^k))) =
      2*(∑ k ∈ Finset.range n,u^k)-(∑ k ∈ Finset.range D,u^k) := by
    have hall := Finset.sum_range_add (fun k => u^k) n (D-n)
    have hsigned := Finset.sum_range_add (fun k => if k<n then u^k else -(u^k)) n (D-n)
    rw [← hd] at hall hsigned
    have hp : (∑ k ∈ Finset.range n,(if k<n then u^k else -(u^k)))=∑ k ∈ Finset.range n,u^k := by
      apply Finset.sum_congr rfl
      intro k hk
      rw [if_pos (Finset.mem_range.mp hk)]
    have hq : (∑ k ∈ Finset.range (D-n),(if n+k<n then u^(n+k) else -(u^(n+k)))) =
        -(∑ k ∈ Finset.range (D-n),u^(n+k)) := by
      simp [show ∀ k : ℕ,¬n+k<n by omega]
    rw [hp,hq] at hsigned
    rw [hsigned,hall]
    ring
  rw [hsplit,sub_mul,mul_assoc,geometric_sum_mul,geometric_sum_mul]
  ring

/-- Exact termwise Fourier orientation: plus l*t multiplies conjugate(s0t). -/
theorem polarTransform_signed_geometric (l : Ix d) :
    polarTransform l=cis (-Real.pi*parityDelta d/(2*d))*
      (∑ k ∈ Finset.range d,if k<phaseCut d then geometricRatio l^k else -(geometricRatio l^k)) := by
  unfold polarTransform fourier
  rw [← sum_representatives,Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k hk
  have hkd : k<d := Finset.mem_range.mp hk
  have hchar : chi (l*(k : Ix d))=cis (2*Real.pi*l.val*k/(d : ℝ)) := by
    have hi : l*(k : Ix d)=((l.val*k : ℕ) : Ix d) := by simp
    rw [hi]
    have hc := chi_cis_int (d := d) ((l.val*k : ℕ) : ℤ)
    push_cast at hc
    convert hc using 1 <;> first | simp only [Nat.cast_mul] | ring
  simp only [polarBase,halfRootSign,halfRootAngle,ZMod.val_natCast,Nat.mod_eq_of_lt hkd,
    geometricRatio,cis_pow,star_mul,hchar,← cis_neg]
  split_ifs <;> simp only [star_one,star_neg,one_mul,mul_one,neg_one_mul,mul_neg,neg_mul]
  all_goals
    simp only [← cis_add]
    congr 1
    unfold coefficientAngle
    push_cast
    ring

theorem polarTransform_mul_ratio (l : Ix d) :
    polarTransform l*(geometricRatio l-1)=
      2*cis (-Real.pi*parityDelta d/(2*d))*geometricRatio l^(phaseCut d) := by
  rw [polarTransform_signed_geometric,mul_assoc,signed_geometric_mul _ (phaseCut d) d (Nat.sub_le _ _),
    geometricRatio_power]
  ring

theorem d_lambda_prefactor (hd : 2≤d) (l : Ix d) :
    (d : ℂ)*generalLambda l*secondPrefactor l =
      cis (Real.pi*((l.val : ℝ)-1)-Real.pi*parityDelta d*l.val/d) /
        (Real.sin (coefficientAngle d l) : ℂ) := by
  have hdC : (d : ℂ)≠0 := by exact_mod_cast (NeZero.ne d)
  have hsC : (Real.sin (coefficientAngle d l) : ℂ)≠0 := by
    exact_mod_cast coefficientAngle_sin_ne_zero hd l
  unfold generalLambda secondPrefactor
  rw [sign_cis_bridge]
  have ha : Real.pi*((l.val : ℝ)-1)+Real.pi*l.val*((l.val : ℝ)-1)/d+
      (-Real.pi*l.val*((l.val : ℝ)-1+parityDelta d)/d) =
      Real.pi*((l.val : ℝ)-1)-Real.pi*parityDelta d*l.val/d := by ring
  have he := congrArg cis ha
  rw [cis_add,cis_add] at he
  rw [← he]
  field_simp only [hdC,hsC]
  ring

/-- The sign and r_l phase are included, not inferred from a common norm. -/
theorem d_lambda_prefactor_mul_ratio (hd : 2≤d) (l : Ix d) :
    ((d : ℂ)*generalLambda l*secondPrefactor l)*(geometricRatio l-1) =
      2*cis (-Real.pi*parityDelta d/(2*d))*geometricRatio l^(phaseCut d) := by
  have hs : (Real.sin (coefficientAngle d l) : ℂ)≠0 := by
    exact_mod_cast coefficientAngle_sin_ne_zero hd l
  rw [d_lambda_prefactor hd,geometricRatio,cis_chord_identity,cis_pow]
  have hn : (phaseCut d : ℝ)=((d : ℝ)+1-parityDelta d)/2 := by
    linarith [phaseCut_formula (d := d)]
  have ha : -Real.pi*parityDelta d/(2*d)+(phaseCut d : ℝ)*(2*coefficientAngle d l)=
      Real.pi/2+(Real.pi*((l.val : ℝ)-1)-Real.pi*parityDelta d*l.val/d)+coefficientAngle d l := by
    rw [hn]
    unfold coefficientAngle
    field_simp [ne_of_gt (dimension_pos (d := d))]
    ring
  have he := congrArg cis ha
  rw [cis_add,cis_add,cis_add] at he
  have hi : cis (Real.pi/2)=Complex.I := by simp [cis_exp,Complex.exp_mul_I]
  rw [hi] at he
  push_cast only [Complex.ofReal_mul,Complex.ofReal_ofNat]
  conv_rhs => rw [mul_assoc,he]
  field_simp only [hs]
  ring

/-- Exact source Fourier coefficient S_l=d lambda_l r_l. -/
theorem polarTransform_compression (hd : 2≤d) (l : Ix d) :
    polarTransform l=(d : ℂ)*generalLambda l*secondPrefactor l := by
  apply mul_right_cancel₀ (sub_ne_zero.mpr (geometricRatio_ne_one l))
  rw [polarTransform_mul_ratio,d_lambda_prefactor_mul_ratio hd]

/-- All-dimensional coefficient normalization from exact Fourier compression. -/
theorem generalLambda_normalization (hd : 2≤d) :
    (∑ l : Ix d,star (generalLambda l)*generalLambda l)=1 := by
  have hq : UnitPhases (fun k : Ix d => star (polarBase k)) := by
    intro k
    simpa [mul_comm] using polarBase_unit (d := d) k
  have hs := parseval (fun k : Ix d => star (polarBase k)) hq
  have hterm (l : Ix d) : powerSpectrum (fun k : Ix d => star (polarBase k)) l =
      (d : ℝ)^2*Complex.normSq (generalLambda l) := by
    change Complex.normSq (polarTransform l)=_
    rw [polarTransform_compression hd,Complex.normSq_mul,Complex.normSq_mul]
    have hr : Complex.normSq (secondPrefactor l)=1 := by
      rw [Complex.normSq_eq_norm_sq,secondPrefactor_norm]; norm_num
    rw [hr,mul_one]
    simp [pow_two]
  simp_rw [hterm] at hs
  rw [← Finset.mul_sum] at hs
  have hdR : (d : ℝ)^2≠0 := pow_ne_zero _ (ne_of_gt dimension_pos)
  have hsum : (∑ l : Ix d,Complex.normSq (generalLambda l))=1 := by
    apply mul_left_cancel₀ hdR
    simpa using hs
  change (∑ l : Ix d,(starRingEnd ℂ) (generalLambda l)*generalLambda l)=1
  simp_rw [← Complex.normSq_eq_conj_mul_self]
  rw [← Complex.ofReal_sum,hsum]
  simp

/-- Denominators and phases are nonzero for every coefficient, including l=0. -/
theorem generalLambda_ne_zero (hd : 2≤d) (l : Ix d) : generalLambda l≠0 := by
  unfold generalLambda
  apply div_ne_zero
  · exact mul_ne_zero (pow_ne_zero _ (by norm_num)) (cis_ne_zero _)
  · exact mul_ne_zero (by exact_mod_cast (NeZero.ne d))
      (by exact_mod_cast coefficientAngle_sin_ne_zero hd l)

end CyclicBell.General
