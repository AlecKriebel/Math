import CyclicBell.GeneralCoverageSourceWeyl
import CyclicBell.GeneralCoverageSourceInterpolation

/-! Reindexing the literal source polynomial, including its wraparound term.
The k=d-1 term becomes the l=0 Fourier coefficient using z^d=(-1)^(d-1).
No resonant denominator is cancelled without a proof of nonvanishing. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def sourceLiteralInversePolar (z : ℂ) : ℂ :=
  ∑ k : Ix d, sourceCosecantCoefficient k * (star z)^(k.val+1)

theorem sourcePolarCoefficient_zero :
    sourcePolarCoefficient (0 : Ix d) =
      1 / ((d : ℂ)*(Real.sin (Real.pi/(2*(d : ℝ))) : ℂ)) := by
  rw [sourcePolarCoefficient_literal]
  have ha : Real.pi*((0 : ℝ)-1/2)/d = -(Real.pi/(2*(d : ℝ))) := by ring
  simp only [ZMod.val_zero,Nat.cast_zero,zero_add,pow_one,ha,Real.sin_neg,
    Complex.ofReal_neg,mul_neg,div_neg,neg_neg]
  ring

theorem sourceCosecantCoefficient_last :
    sourceCosecantCoefficient (-1 : Ix d) =
      (-1 : ℂ)^(d-1) / ((d : ℂ)*(Real.sin (Real.pi/(2*(d : ℝ))) : ℂ)) := by
  have hdR : (d : ℝ)≠0 := ne_of_gt (dimension_pos (d := d))
  have hcast : ((d-1 : ℕ) : ℝ)=(d : ℝ)-1 := by
    rw [Nat.cast_sub (Nat.one_le_iff_ne_zero.mpr (NeZero.ne d)), Nat.cast_one]
  have ha : Real.pi*(((d-1 : ℕ) : ℝ)+1/2)/(d : ℝ)=
      Real.pi-Real.pi/(2*(d : ℝ)) := by
    rw [hcast]
    field_simp only [hdR]
    ring
  simp only [sourceCosecantCoefficient,source_neg_one_val,ha,Real.sin_pi_sub]

theorem sourcePolarCoefficient_successor (k : Ix d) (hk : k.val+1<d) :
    sourcePolarCoefficient (k+1) = sourceCosecantCoefficient k := by
  have hv : (k+1).val=k.val+1 := by
    rw [successor_val,Nat.mod_eq_of_lt hk]
  rw [sourcePolarCoefficient_literal,hv]
  have ha : Real.pi*(((k.val+1 : ℕ) : ℝ)-1/2)/d =
      Real.pi*((k.val : ℝ)+1/2)/d := by push_cast; ring
  rw [ha,show k.val+1+1=k.val+2 by omega,pow_add]
  norm_num only [pow_two,neg_mul,one_mul,neg_neg,mul_one]
  rfl

theorem sourceLiteralInversePolar_term (hd : 2≤d) (j k : Ix d) :
    sourceCosecantCoefficient k * (star (equalityRoot j))^(k.val+1) =
      sourcePolarCoefficient (k+1) * (star (equalityRoot j))^(k+1).val := by
  by_cases hk : k=-1
  · subst k
    have hpow : (star (equalityRoot j))^d = (-1 : ℂ)^(d-1) := by
      rw [←star_pow,equalityRoot_power hd]
      simp only [star_pow,star_neg,star_one]
    rw [source_neg_one_val,Nat.sub_add_cancel (by omega : 1≤d),hpow,
      neg_add_cancel,sourcePolarCoefficient_zero,ZMod.val_zero,pow_zero,mul_one,
      sourceCosecantCoefficient_last]
    have hs : (-1 : ℂ)^(d-1)*(-1 : ℂ)^(d-1)=1 := by rw [←mul_pow]; norm_num
    calc
      _ = ((-1 : ℂ)^(d-1)*(-1 : ℂ)^(d-1)) /
          ((d : ℂ)*(Real.sin (Real.pi/(2*(d : ℝ))) : ℂ)) := by ring
      _ = _ := by rw [hs]
  · have hval : k.val≠d-1 := by
      intro h
      apply hk
      apply ZMod.val_injective
      rw [source_neg_one_val]
      exact h
    have hlt : k.val+1<d := by have := ZMod.val_lt k; omega
    have hv : (k+1).val=k.val+1 := by rw [successor_val,Nat.mod_eq_of_lt hlt]
    rw [sourcePolarCoefficient_successor k hlt,hv]

/-- Literal source cosecant sum equals the actual conjugate polar phase. -/
theorem sourceLiteralInversePolar_at_root (hd : 2≤d) (j : Ix d) :
    sourceLiteralInversePolar (d := d) (equalityRoot j) = star (polarBase j) := by
  unfold sourceLiteralInversePolar
  simp_rw [sourceLiteralInversePolar_term hd j]
  rw [sum_translate (fun l : Ix d => sourcePolarCoefficient l * (star (equalityRoot j))^l.val) 1]
  exact sourceInversePolarPolynomial_at_root hd j

theorem sourceLiteralInversePolar_quotient (hd : 2≤d) (j : Ix d) :
    sourceLiteralInversePolar (d := d) (equalityRoot j) =
      star ((1+equalityRoot j)/(‖1+equalityRoot j‖ : ℂ)) := by
  rw [sourceLiteralInversePolar_at_root hd]
  have h := polarPhase_eq_quotient hd (0 : Ix d) j
  simpa only [polarPhase,zero_add,chi_zero,one_mul] using congrArg star h

end CyclicBell.General
