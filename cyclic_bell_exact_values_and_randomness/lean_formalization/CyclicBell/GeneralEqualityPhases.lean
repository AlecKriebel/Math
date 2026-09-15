import CyclicBell.GeneralPolarPhases
import CyclicBell.GeneralFiniteSpectrum

/-! Equality-root completeness and adjacent reflection signs, with the wrap
between d-1 and 0 included. Pure scalar input to supported rigidity.
UNCOMPILED SOURCE CANDIDATES. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

theorem cis_eq_one_iff (t : ℝ) : cis t=1 ↔ ∃ n : ℤ,t=2*Real.pi*n := by
  have h : cis t=1 ↔ Circle.exp t=1 := by
    change ((Circle.exp t : Circle) : ℂ) = ((1 : Circle) : ℂ) ↔ Circle.exp t = 1
    exact Subtype.coe_injective.eq_iff
  rw [h,Circle.exp_eq_one]
  simp [mul_comm]

theorem unit_power_root_character (z : ℂ) (hz : ‖z‖=1) (hp : z^d=1) :
    ∃ k : Ix d,z=chi k := by
  let w : Circle := ⟨z,by change dist z 0 = 1; simpa only [dist_zero_right] using hz⟩
  have he : cis (Complex.arg z)=z := congrArg (fun v : Circle => (v : ℂ)) (Circle.exp_arg w)
  have hp' : cis ((d : ℝ)*Complex.arg z)=1 := by rw [← cis_pow,he,hp]
  obtain ⟨n,hn⟩ := (cis_eq_one_iff _).mp hp'
  refine ⟨(n : Ix d),?_⟩
  rw [chi_cis_int,← he]
  congr 1
  apply (eq_div_iff (ne_of_gt (dimension_pos (d := d)))).mpr
  linarith

theorem equalityBase_power : equalityBase d^d=(-1 : ℂ)^(d-1) := by
  rw [equalityBase,cis_pow]
  have h : (d : ℝ)*(Real.pi*parityDelta d/(d : ℝ))=Real.pi*parityDelta d := by
    field_simp [ne_of_gt (dimension_pos (d := d))]
  rw [h,parity_constant]

/-- All equality roots occur in the explicit list, not merely some of them. -/
theorem equalityRoot_complete (z : ℂ) (hz : ‖z‖=1) (hp : z^d=(-1 : ℂ)^(d-1)) :
    ∃ k : Ix d,z=equalityRoot k := by
  have hb : equalityBase d≠0 := cis_ne_zero _
  have hr : ‖z/equalityBase d‖=1 := by rw [norm_div,hz,equalityBase,cis_norm,div_one]
  have hp' : (z/equalityBase d)^d=1 := by
    rw [div_pow,hp,equalityBase_power]
    exact div_self (pow_ne_zero _ (by norm_num))
  obtain ⟨k,hk⟩ := unit_power_root_character _ hr hp'
  refine ⟨k,?_⟩
  have he := (div_eq_iff hb).mp hk
  simpa [equalityRoot,mul_comm] using he

theorem equalityRoot_complete_iff (hd : 2≤d) (z : ℂ) (hz : ‖z‖=1) :
    z^d=(-1 : ℂ)^(d-1) ↔ ∃ k : Ix d,z=equalityRoot k := by
  constructor
  · exact equalityRoot_complete z hz
  · rintro ⟨k,rfl⟩
    exact equalityRoot_power hd k

def equalityIndicator (d : ℕ) (z : ℂ) : ℂ := if z^d=(-1 : ℂ)^(d-1) then 1 else 0

def scalarPolarPhase (y : Ix d) (z : ℂ) : ℂ := (1+chi y*z)/(‖1+chi y*z‖ : ℂ)

theorem scalarPolarPhase_at_root (hd : 2≤d) (y k : Ix d) :
    scalarPolarPhase y (equalityRoot k)=polarPhase y k := (polarPhase_eq_quotient hd y k).symm

theorem good_phase_nonzero (hd : 2≤d) (y : Ix d) (z : ℂ) (hz : ‖z‖=1)
    (hp : z^d=(-1 : ℂ)^(d-1)) : 1+chi y*z≠0 := by
  obtain ⟨k,rfl⟩ := equalityRoot_complete z hz hp
  exact equalityRoot_no_bad_phase hd y k

theorem polarPhase_square (y k : Ix d) : polarPhase y k^2=chi y*equalityRoot k := by
  have he : chi y*equalityRoot k=equalityRoot (y+k) := by
    apply add_left_cancel (a := (1 : ℂ))
    exact linear_at_root y k
  rw [he]
  unfold polarPhase polarBase halfRootSign
  split_ifs <;> rw [mul_pow] <;> simp only [one_pow,one_mul,neg_one_sq]
  all_goals rw [cis_pow]; norm_num only [Nat.cast_ofNat]; exact (equalityRoot_halfAngle _).symm

/-- Half-angle increment with exactly one negative transition. -/
theorem polarBase_adjacent (hd : 2≤d) (j : Ix d) :
    polarBase (j+1)=cis (Real.pi/(d : ℝ))*polarBase j*
      (if j=reflectionLabel d then -1 else 1) := by
  have hj := ZMod.val_lt j
  have hcutpos : 0<phaseCut d := by unfold phaseCut; omega
  have hcutlt : phaseCut d<d := by unfold phaseCut; omega
  have hlabelval : (reflectionLabel d).val=phaseCut d-1 := by
    unfold reflectionLabel
    rw [ZMod.val_natCast,Nat.mod_eq_of_lt (by omega)]
  by_cases hwrap : j.val+1=d
  · have hjv : j.val=d-1 := by omega
    have hj1 : j+1=0 := by
      apply ZMod.val_injective
      rw [residue_add_val]
      have hv1 : (1 : Ix d).val=1 := by
        rw [← Nat.cast_one,ZMod.val_natCast,Nat.mod_eq_of_lt (by omega)]
      simp [hv1,hwrap]
    have hne : j≠reflectionLabel d := by
      intro h; have hh := congrArg ZMod.val h; rw [hlabelval] at hh; omega
    have hs0 : halfRootSign d (0 : Ix d)=1 := by simp [halfRootSign,hcutpos]
    have hsj : halfRootSign d j=-1 := by simp [halfRootSign,hjv]; omega
    have ha : halfRootAngle d j+Real.pi/(d : ℝ)=halfRootAngle d 0+Real.pi := by
      unfold halfRootAngle
      rw [hjv,Nat.cast_sub (by omega : 1≤d)]
      simp only [ZMod.val_zero,Nat.cast_zero,Nat.cast_one]
      field_simp [ne_of_gt (dimension_pos (d := d))]
      ring
    rw [hj1,if_neg hne,polarBase,polarBase,hs0,hsj,one_mul,mul_one]
    calc
      _ = -cis (halfRootAngle d j+Real.pi/(d : ℝ)) := by rw [ha,cis_add,cis_pi]; ring
      _ = _ := by rw [cis_add]; ring
  · have hnext : (j+1).val=j.val+1 := by
      rw [residue_add_val]
      have hv1 : (1 : Ix d).val=1 := by
        rw [← Nat.cast_one,ZMod.val_natCast,Nat.mod_eq_of_lt (by omega)]
      rw [hv1,Nat.mod_eq_of_lt (by omega)]
    have ha : halfRootAngle d (j+1)=Real.pi/(d : ℝ)+halfRootAngle d j := by
      unfold halfRootAngle
      rw [hnext]
      push_cast
      ring
    have hsign : halfRootSign d (j+1)=halfRootSign d j*(if j=reflectionLabel d then -1 else 1) := by
      have he : j=reflectionLabel d ↔ j.val=phaseCut d-1 := by
        constructor
        · intro h; rw [h,hlabelval]
        · intro h; apply ZMod.val_injective; rw [h,hlabelval]
      unfold halfRootSign
      simp only [hnext,he]
      split_ifs <;> norm_num <;> omega
    rw [polarBase,ha,cis_add,hsign,polarBase]
    ring

theorem polarPhase_adjacent (hd : 2≤d) (y k : Ix d) :
    polarPhase (y+1) k=cis (Real.pi/(d : ℝ))*polarPhase y k*
      (if k=reflectionLabel d-y then -1 else 1) := by
  have h := polarBase_adjacent hd (y+k)
  have hi : y+k=reflectionLabel d ↔ k=reflectionLabel d-y := by constructor <;> intro h <;> linear_combination h
  simpa [polarPhase,add_assoc,add_left_comm,add_comm,hi] using h

theorem reflection_phase_power : cis (Real.pi/(d : ℝ))^d=-1 := by
  rw [cis_pow]
  have h : (d : ℝ)*(Real.pi/(d : ℝ))=Real.pi := by
    field_simp [ne_of_gt (dimension_pos (d := d))]
  rw [h,cis_pi]

end CyclicBell.General
