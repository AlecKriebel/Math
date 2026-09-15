import CyclicBell.GeneralFourier

/-! Pure complex phase and parity data, independent of every concrete quantum
witness. This separation keeps the arbitrary-dimensional upper-bound import
graph free of construction/attainment modules. Uncompiled source. -/
noncomputable section
open scoped BigOperators
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def cis (t : ℝ) : ℂ := (Circle.exp t : ℂ)

@[simp] theorem cis_exp (t : ℝ) : cis t = Complex.exp ((t : ℂ)*Complex.I) :=
  Circle.coe_exp t

@[simp] theorem cis_zero : cis 0=1 := by simp [cis]

@[simp] theorem cis_add (x y : ℝ) : cis (x+y)=cis x*cis y := by
  simp [cis,Circle.exp_add]

@[simp] theorem cis_norm (t : ℝ) : ‖cis t‖=1 := (Circle.exp t).norm_coe

@[simp] theorem cis_normSq (t : ℝ) : Complex.normSq (cis t)=1 := by
  rw [Complex.normSq_eq_norm_sq,cis_norm]
  norm_num

@[simp] theorem cis_unit (t : ℝ) : star (cis t)*cis t=1 := by
  change (starRingEnd ℂ) (cis t)*cis t=1
  rw [← Complex.normSq_eq_conj_mul_self,cis_normSq]
  norm_num

@[simp] theorem cis_ne_zero (t : ℝ) : cis t≠0 := by
  intro h
  have hn := cis_norm t
  rw [h, norm_zero] at hn
  exact zero_ne_one hn

@[simp] theorem cis_neg (t : ℝ) : cis (-t)=star (cis t) := by
  apply mul_right_cancel₀ (cis_ne_zero t)
  rw [← cis_add,neg_add_cancel,cis_zero,cis_unit]

theorem cis_sub (x y : ℝ) : cis (x-y)=cis x*star (cis y) := by
  rw [sub_eq_add_neg,cis_add,cis_neg]

@[simp] theorem cis_period_int (n : ℤ) : cis (2*Real.pi*n)=1 := by
  exact congrArg (fun z : Circle => (z : ℂ)) (Circle.exp_two_pi_mul_int n)

@[simp] theorem cis_pi : cis Real.pi = -1 := by
  rw [cis_exp,Complex.exp_pi_mul_I]

theorem cis_pow (t : ℝ) (n : ℕ) : cis t ^ n=cis ((n : ℝ)*t) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ,ih,← cis_add]
    congr 1
    push_cast
    ring

theorem chi_cis_int (j : ℤ) : chi (j : Ix d)=cis (2*Real.pi*j/(d : ℝ)) := by
  rw [chi_intCast,cis_exp]
  congr 1
  push_cast
  ring

theorem chi_cis_val (j : Ix d) : chi j=cis (2*Real.pi*j.val/(d : ℝ)) := by
  simpa only [ZMod.natCast_zmod_val,Int.cast_natCast] using chi_cis_int (d := d) (j.val : ℤ)

def parityDelta (d : ℕ) : ℕ := if Even d then 1 else 0

theorem parityDelta_cases : parityDelta d=0 ∨ parityDelta d=1 := by
  unfold parityDelta
  split_ifs <;> simp

/-- Exactly the parity condition required for the chirp to be cyclic. -/
theorem parity_shift_even : ∃ m : ℕ, (d : ℝ)-1+parityDelta d=2*m := by
  rcases Nat.even_or_odd d with he|ho
  · obtain ⟨m,hm⟩ := he
    refine ⟨m,?_⟩
    have hd : Even d := ⟨m,hm⟩
    simp only [parityDelta,if_pos hd,Nat.cast_one]
    have hc : (d : ℝ)=m+m := by exact_mod_cast hm
    linarith
  · obtain ⟨m,hm⟩ := ho
    refine ⟨m,?_⟩
    have hne : ¬ Even d := by
      intro he
      obtain ⟨k,hk⟩ := he
      omega
    simp only [parityDelta,if_neg hne,Nat.cast_zero,add_zero]
    have hc : (d : ℝ)=2*m+1 := by exact_mod_cast (show d=2*m+1 by omega)
    linarith

def equalityBase (d : ℕ) : ℂ := cis (Real.pi*parityDelta d/(d : ℝ))

def equalityRoot (j : Ix d) : ℂ := equalityBase d * chi j

theorem equalityRoot_unit : UnitPhases (equalityRoot : Ix d → ℂ) := by
  intro j
  simp only [equalityRoot,star_mul]
  calc
    (star (chi j)*star (equalityBase d))*(equalityBase d*chi j) =
        (star (equalityBase d)*equalityBase d)*(star (chi j)*chi j) := by ring
    _=1 := by rw [equalityBase, cis_unit, chi_star_mul]; norm_num

theorem equalityRoot_injective : Function.Injective (equalityRoot : Ix d → ℂ) := by
  intro i j h
  apply chi_injective
  exact mul_left_cancel₀ (cis_ne_zero _) h

/-- Explicit manuscript equality root exp(pi*i*(2j+delta)/d). -/
theorem equalityRoot_cis (j : Ix d) :
    equalityRoot j=cis (Real.pi*(2*j.val+parityDelta d)/(d : ℝ)) := by
  rw [equalityRoot,equalityBase,chi_cis_val,← cis_add]
  congr 1
  ring


end CyclicBell.General
