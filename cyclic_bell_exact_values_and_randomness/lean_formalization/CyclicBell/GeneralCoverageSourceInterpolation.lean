import CyclicBell.GeneralSecondCoefficients
import CyclicBell.GeneralSourceFourier

/-!
Exact finite Fourier interpolation of the conjugate polar phase used in
manuscript app:attainment. This is a scalar bridge; physical Bob validity still
requires its application to the literal source matrices and an order proof.
-/

noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def sourcePolarCoefficient (l : Ix d) : ℂ :=
  generalLambda l * secondPrefactor l * (equalityBase d)^l.val

def sourceInversePolarPolynomial (z : ℂ) : ℂ :=
  ∑ l : Ix d, sourcePolarCoefficient l * (star z)^l.val

/-- The Weyl triangular phases cancel; the remaining coefficient is the
literal signed cosecant, with the exceptional l=0 denominator retained. -/
theorem sourcePolarCoefficient_literal (l : Ix d) :
    sourcePolarCoefficient l = (-1 : ℂ)^(l.val+1) /
      ((d : ℂ)*(Real.sin (Real.pi*((l.val : ℝ)-1/2)/d) : ℂ)) := by
  have he : cis (Real.pi*(l.val : ℝ)*((l.val : ℝ)-1)/d) *
      secondPrefactor l * (equalityBase d)^l.val = 1 := by
    rw [secondPrefactor,equalityBase,cis_pow,←cis_add,←cis_add]
    have ha : Real.pi*(l.val : ℝ)*((l.val : ℝ)-1)/d +
        (-Real.pi*(l.val : ℝ)*((l.val : ℝ)-1+parityDelta d)/d) +
        (l.val : ℝ)*(Real.pi*parityDelta d/d) = 0 := by ring
    rw [ha,cis_zero]
  unfold sourcePolarCoefficient generalLambda coefficientAngle
  calc
    _ = (-1 : ℂ)^(l.val+1) *
        (cis (Real.pi*(l.val : ℝ)*((l.val : ℝ)-1)/d) *
          secondPrefactor l * (equalityBase d)^l.val) /
        ((d : ℂ)*(Real.sin (Real.pi*((l.val : ℝ)-1/2)/d) : ℂ)) := by ring
    _ = _ := by rw [he,mul_one]

theorem sourceRoot_inverse_character (l j : Ix d) :
    (equalityBase d)^l.val * (star (equalityRoot j))^l.val = chi (-(l*j)) := by
  have hb : equalityBase d * star (equalityBase d)=1 := by
    simpa only [mul_comm] using cis_unit (Real.pi*parityDelta d/d)
  have he : equalityBase d * star (equalityRoot j) = star (chi j) := by
    rw [equalityRoot,star_mul]
    calc
      equalityBase d * (star (chi j)*star (equalityBase d)) =
          (equalityBase d*star (equalityBase d))*star (chi j) := by ring
      _ = _ := by rw [hb,one_mul]
  rw [←mul_pow,he,chi_star,chi_pow,ZMod.natCast_zmod_val]
  congr 1
  ring

/-- Exact interpolation at every scalar equality root, in every d>=2. -/
theorem sourceInversePolarPolynomial_at_root (hd : 2≤d) (j : Ix d) :
    sourceInversePolarPolynomial (d := d) (equalityRoot j) = star (polarBase j) := by
  have hterm (l : Ix d) : sourcePolarCoefficient l * (star (equalityRoot j))^l.val =
      generalLambda l*secondPrefactor l*chi (-(l*j)) := by
    unfold sourcePolarCoefficient
    rw [mul_assoc,sourceRoot_inverse_character]
  unfold sourceInversePolarPolynomial
  simp_rw [hterm]
  have h := fourier_inversion (fun k : Ix d => star (polarBase k)) j
  change star (polarBase j) = (d : ℂ)⁻¹ * ∑ l, chi (-(l*j))*polarTransform l at h
  simp_rw [polarTransform_compression hd] at h
  have hdC : (d : ℂ)≠0 := by exact_mod_cast (NeZero.ne d)
  have he : (d : ℂ)⁻¹ * (∑ l : Ix d, chi (-(l*j))*((d : ℂ)*generalLambda l*secondPrefactor l)) =
      ∑ l : Ix d,generalLambda l*secondPrefactor l*chi (-(l*j)) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro l _
    field_simp only [hdC]
    ring
  rw [he] at h
  exact h.symm

theorem sourceInversePolarPolynomial_unit (hd : 2≤d) (j : Ix d) :
    star (sourceInversePolarPolynomial (d := d) (equalityRoot j)) *
      sourceInversePolarPolynomial (d := d) (equalityRoot j)=1 := by
  rw [sourceInversePolarPolynomial_at_root hd,star_star]
  simpa only [mul_comm] using polarBase_unit (d := d) j

/-- This fixes the conjugation of the source polar factor, rather than merely
proving that some scalar of the same norm exists. -/
theorem sourceInversePolarPolynomial_quotient (hd : 2≤d) (j : Ix d) :
    sourceInversePolarPolynomial (d := d) (equalityRoot j) =
      star ((1+equalityRoot j)/(‖1+equalityRoot j‖ : ℂ)) := by
  rw [sourceInversePolarPolynomial_at_root hd]
  have h := polarPhase_eq_quotient hd (0 : Ix d) j
  simpa only [polarPhase,zero_add,chi_zero,one_mul] using congrArg star h

end CyclicBell.General
