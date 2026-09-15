import CyclicBell.GeneralCommuting
import CyclicBell.GeneralCoveragePolarAlgebra

/-! The literal polar positive-factor identity with actual CFC square roots.
The polar decomposition is supplied, as in the manuscript lemma. Its initial
isometry equation is a defining property of the canonical polar factor. All
commutation and mixed square-root identities are derived, including at kernels.
-/
noncomputable section
open scoped ComplexOrder
namespace CyclicBell.General.Coverage
variable {A : Type*} [CStarAlgebra A] [PartialOrder A] [StarOrderedRing A]

/-- Positive square roots respect conjugation by a unitary, by uniqueness. -/
theorem sqrt_unitary_conjugation (a u : A) (ha : 0≤a) (hu : StarUnitary u) :
    CFC.sqrt (u*a*star u)=u*CFC.sqrt a*star u := by
  apply CFC.sqrt_unique _ (conjugate_nonneg' CFC.sqrt_nonneg u)
  calc
    _ = u*(CFC.sqrt a*(star u*u)*CFC.sqrt a)*star u := by noncomm_ring
    _ = _ := by rw [hu.1,mul_one,CFC.sqrt_mul_sqrt_self a ha]

/-- The commutation premise concerns a, not its square root. -/
theorem sqrt_commutes_unitary (a b : A) (ha : 0≤a) (hb : StarUnitary b)
    (hab : a*b=b*a) : CFC.sqrt a*b=b*CFC.sqrt a := by
  have he : b*a*star b=a := by rw [← hab,mul_assoc,hb.2,mul_one]
  have hs := sqrt_unitary_conjugation a b ha hb
  rw [he] at hs
  have h := congrArg (fun x : A => x*b) hs
  simpa only [mul_assoc,hb.1,mul_one] using h

/-- Support-isometry passes from a positive operator to its positive root.
This uses the C*-zero-product norm identity, not an inverse or a closed range. -/
theorem initial_isometry_sqrt (V Q : A) (hQ : 0≤Q) (hInitial : (star V*V)*Q=Q) :
    (star V*V)*CFC.sqrt Q=CFC.sqrt Q := by
  let D := star V*V-1
  have hDQ : D*Q=0 := by simp only [D,sub_mul,hInitial,one_mul,sub_self]
  have hH : star (CFC.sqrt Q)=CFC.sqrt Q := IsSelfAdjoint.of_nonneg CFC.sqrt_nonneg
  have he : (D*CFC.sqrt Q)*star (D*CFC.sqrt Q)=0 := by
    calc
      _ = D*(CFC.sqrt Q*CFC.sqrt Q)*star D := by rw [star_mul,hH]; noncomm_ring
      _ = _ := by rw [CFC.sqrt_mul_sqrt_self Q hQ,hDQ,zero_mul]
  have hz := (CStarRing.mul_star_self_eq_zero_iff _).mp he
  simpa only [D,sub_mul,one_mul,sub_eq_zero] using hz

/-- Exact left modulus from a polar factor and its actual initial isometry. -/
theorem polar_left_modulus (C V : A)
    (hpolar : C=V*CFC.sqrt (star C*C))
    (hInitial : (star V*V)*CFC.sqrt (star C*C)=CFC.sqrt (star C*C)) :
    CFC.sqrt (C*star C)=V*CFC.sqrt (star C*C)*star V := by
  apply CFC.sqrt_unique _ (conjugate_nonneg' CFC.sqrt_nonneg V)
  have hQ : star (CFC.sqrt (star C*C))=CFC.sqrt (star C*C) :=
    IsSelfAdjoint.of_nonneg CFC.sqrt_nonneg
  calc
    _ = V*(CFC.sqrt (star C*C)*CFC.sqrt (star C*C))*star V :=
      transportedRoot_square V (CFC.sqrt (star C*C)) hInitial
    _ = C*star C := by
      conv_rhs => rw [hpolar]
      simp only [star_mul,hQ]
      noncomm_ring

/-- The transported positive root is the literal left half-modulus. -/
theorem polar_left_half_modulus (C V : A)
    (hpolar : C=V*CFC.sqrt (star C*C))
    (hInitial : (star V*V)*CFC.sqrt (star C*C)=CFC.sqrt (star C*C)) :
    CFC.sqrt (CFC.sqrt (C*star C))=V*CFC.sqrt (CFC.sqrt (star C*C))*star V := by
  have hs := initial_isometry_sqrt V (CFC.sqrt (star C*C)) CFC.sqrt_nonneg hInitial
  apply CFC.sqrt_unique _ (conjugate_nonneg' CFC.sqrt_nonneg V)
  calc
    _ = V*(CFC.sqrt (CFC.sqrt (star C*C))*CFC.sqrt (CFC.sqrt (star C*C)))*star V :=
      transportedRoot_square V (CFC.sqrt (CFC.sqrt (star C*C))) hs
    _ = V*CFC.sqrt (star C*C)*star V := by rw [CFC.sqrt_mul_sqrt_self _ CFC.sqrt_nonneg]
    _ = _ := (polar_left_modulus C V hpolar hInitial).symm

/-- Manuscript lem:polar, with CFC definitions of both absolute values and
half-powers. Canonical polar decomposition supplies the first two premises.
No cross relation, factor commutation, or nonvanishing assumption is a premise. -/
theorem canonical_polar_positive_factor_identity (C V B : A)
    (hpolar : C=V*CFC.sqrt (star C*C))
    (hInitial : (star V*V)*CFC.sqrt (star C*C)=CFC.sqrt (star C*C))
    (hB : StarUnitary B) (hCB : C*B=B*C) :
    let P := CFC.sqrt (CFC.sqrt (C*star C))-V*CFC.sqrt (CFC.sqrt (star C*C))*B
    (1/2 : ℂ) • (CFC.sqrt (star C*C)+CFC.sqrt (C*star C))-algebraHerm (C*B)=
      (1/2 : ℂ) • (star P*P) := by
  let Q := CFC.sqrt (star C*C)
  let H := CFC.sqrt Q
  have hQ : 0≤Q := CFC.sqrt_nonneg
  have hH : star H=H := IsSelfAdjoint.of_nonneg CFC.sqrt_nonneg
  have hHH : H*H=Q := CFC.sqrt_mul_sqrt_self Q hQ
  have hSH : (star V*V)*H=H := initial_isometry_sqrt V Q hQ hInitial
  have hstarCB : star C*B=B*star C := by
    have h := congrArg star (star_commute_of_unitary hB hCB.symm)
    simpa only [star_mul,star_star] using h
  have hprod : (star C*C)*B=B*(star C*C) := by
    rw [mul_assoc,hCB,← mul_assoc,hstarCB,mul_assoc]
  have hQB : Q*B=B*Q := sqrt_commutes_unitary _ B (star_mul_self_nonneg C) hB hprod
  have he := supportedPolarResidual_square V H B hH hSH hB.1 (by rw [hHH,hQB])
  dsimp only at he ⊢
  rw [hHH,← hpolar] at he
  rw [polar_left_half_modulus C V hpolar hInitial]
  change (1/2 : ℂ) • (Q+CFC.sqrt (C*star C))-algebraHerm (C*B)=
    (1/2 : ℂ) • (star (transportedRoot V H-V*H*B)*(transportedRoot V H-V*H*B))
  rw [he,polar_left_modulus C V hpolar hInitial]
  rw [← hpolar]
  unfold algebraHerm
  module

/-- Explicit arbitrary complete Hilbert-space specialization of lem:polar. -/
theorem canonical_polar_hilbert_positive_factor_identity
    {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (C V B : H →L[ℂ] H)
    (hpolar : C=V*CFC.sqrt (star C*C))
    (hInitial : (star V*V)*CFC.sqrt (star C*C)=CFC.sqrt (star C*C))
    (hB : StarUnitary B) (hCB : C*B=B*C) :
    let P := CFC.sqrt (CFC.sqrt (C*star C))-V*CFC.sqrt (CFC.sqrt (star C*C))*B
    (1/2 : ℂ) • (CFC.sqrt (star C*C)+CFC.sqrt (C*star C))-algebraHerm (C*B)=
      (1/2 : ℂ) • (star P*P) :=
  canonical_polar_positive_factor_identity C V B hpolar hInitial hB hCB

end CyclicBell.General.Coverage
