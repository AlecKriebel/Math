import CyclicBell.GeneralCommuting
import CyclicBell.GeneralSecondCoefficients
import CyclicBell.GeneralSecondSOS

/-! Independent arbitrary-Hilbert-space second-family bound. The SOS is
algebraic even without cross-party commutation; the allowed commuting quantum
model is a subclass. Actual source coefficients are substituted at the endpoint.
UNCOMPILED SOURCE CANDIDATES. -/
noncomputable section
open scoped BigOperators ComplexOrder InnerProductSpace
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {A : Type*} [CStarAlgebra A]

def algebraFourier (b : Ix d → A) (l : Ix d) : A := ∑ y,chi (l*y) • b y

theorem algebraFourier_energy (b : Ix d → A) :
    (∑ l,star (algebraFourier b l)*algebraFourier b l)=
      (d : ℂ) • ∑ y,star (b y)*b y := by
  have hexpand (l : Ix d) :
      star (algebraFourier b l)*algebraFourier b l =
        ∑ y : Ix d, ∑ z : Ix d,
          (star (chi (l*y))*chi (l*z)) • (star (b y)*b z) := by
    simp only [algebraFourier,star_sum,star_smul,Finset.sum_mul,Finset.mul_sum,
      smul_mul_assoc,mul_smul_comm,Finset.smul_sum,smul_smul]
    rw [Finset.sum_comm]
    simp only [mul_comm]
  simp_rw [hexpand]
  calc
    _ = ∑ y : Ix d, ∑ z : Ix d,
      (∑ l : Ix d, star (chi (l*y))*chi (l*z)) • (star (b y)*b z) := by
      simp only [Finset.sum_smul]
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro y _
      rw [Finset.sum_comm]
    _ = _ := by
      simp only [fourier_character_orthogonality]
      simp [Finset.smul_sum]

def operatorSecond (lam : Ix d → ℂ) (a b : Ix d → A) : A :=
  ∑ l,algebraHerm (star (lam l) • (a l*algebraFourier b l))
def algebraSecondResidual (lam : Ix d → ℂ) (a b : Ix d → A) (l : Ix d) : A :=
  ((d : ℂ)*lam l) • 1-a l*algebraFourier b l

theorem algebraSecondExpansion (lam : ℂ) (C : A) :
    star (((d : ℂ)*lam) • (1 : A)-C)*(((d : ℂ)*lam) • 1-C)=
      ((d : ℂ)^2*(star lam*lam)) • 1+star C*C-
        (d : ℂ) • (star lam • C+star (star lam • C)) := by
  simp only [star_sub,star_smul,star_one,sub_mul,mul_sub,smul_mul_assoc,
    mul_smul_comm,smul_smul,one_mul,mul_one,star_mul,star_star,star_natCast]
  module

/-- Source eq:second-sos, including the prefactor, in any complex C*-algebra. -/
theorem second_cstar_sos (lam : Ix d → ℂ) (hlam : ∑ l,star (lam l)*lam l=1)
    (a b : Ix d → A) (ha : ∀ l,StarUnitary (a l)) (hb : ∀ y,StarUnitary (b y)) :
    (d : ℂ) • (1 : A)-operatorSecond lam a b =
      (1/(2*d) : ℂ) • ∑ l,star (algebraSecondResidual lam a b l)*algebraSecondResidual lam a b l := by
  have hdC : (d : ℂ)≠0 := by exact_mod_cast (NeZero.ne d)
  have he (l : Ix d) : star (a l*algebraFourier b l)*(a l*algebraFourier b l)=
      star (algebraFourier b l)*algebraFourier b l := by
    simp only [star_mul]
    calc _=star (algebraFourier b l)*(star (a l)*a l)*algebraFourier b l := by noncomm_ring
         _=_ := by rw [(ha l).1,mul_one]
  have henergy : (∑ l,star (algebraFourier b l)*algebraFourier b l)=(d : ℂ)^2 • (1 : A) := by
    rw [algebraFourier_energy]
    simp only [(hb _).1]
    rw [Finset.sum_const, Finset.card_univ, ZMod.card]
    rw [← Nat.cast_smul_eq_nsmul ℂ d (1 : A), smul_smul, pow_two]
  have hcross : (∑ l : Ix d, (star (lam l) • (a l*algebraFourier b l)+
      star (star (lam l) • (a l*algebraFourier b l)))) = (2 : ℂ) • operatorSecond lam a b := by
    unfold operatorSecond algebraHerm
    rw [Finset.smul_sum]
    apply Finset.sum_congr rfl
    intro l _
    simp only [smul_smul]
    norm_num
  have hs : (∑ l,star (algebraSecondResidual lam a b l)*algebraSecondResidual lam a b l)=
      (2*(d : ℂ)^2) • (1 : A)-(2*d : ℂ) • operatorSecond lam a b := by
    unfold algebraSecondResidual
    simp_rw [algebraSecondExpansion,he]
    rw [Finset.sum_sub_distrib,Finset.sum_add_distrib,← Finset.sum_smul,
      ← Finset.mul_sum,hlam,mul_one,henergy,← Finset.smul_sum]
    rw [hcross,smul_smul]
    module
  rw [hs,smul_sub,smul_smul,smul_smul]
  have h₁ : (1/(2*d) : ℂ)*(2*(d : ℂ)^2)=d := by field_simp [hdC]; ring
  have h₂ : (1/(2*d) : ℂ)*(2*d)=1 := by field_simp [hdC]
  rw [h₁,h₂,one_smul]

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem second_commuting_hilbert_bound (hd : 2≤d) (ψ : H) (hψ : ‖ψ‖=1)
    (a b : Ix d → H →L[ℂ] H) (ha : ∀ l,StarUnitary (a l)) (hb : ∀ y,StarUnitary (b y)) :
    vectorEval ψ (operatorSecond generalLambda a b)≤d := by
  have h := congrArg (vectorEval ψ) (second_cstar_sos generalLambda
    (generalLambda_normalization hd) a b ha hb)
  have hc : (1/(2*d) : ℂ)=((1/(2*d) : ℝ) : ℂ) := by push_cast; rfl
  rw [hc] at h
  simp only [vectorEval_sub,show (d : ℂ)=((d : ℝ) : ℂ) by simp,
    vectorEval_real_smul,vectorEval_one ψ hψ,vectorEval_sum,vectorEval_square] at h
  have hp : 0≤∑ l,‖algebraSecondResidual generalLambda a b l ψ‖^2 :=
    Finset.sum_nonneg (fun _ _ => sq_nonneg _)
  have hdR : 0 < (d : ℝ) := dimension_pos
  have hpos : 0<(1/(2*d) : ℝ) := by positivity
  nlinarith

theorem second_augmented_commuting_hilbert_bound (hd : 2≤d) (ψ : H) (hψ : ‖ψ‖=1)
    (a b : Ix d → H →L[ℂ] H) (bextra : H →L[ℂ] H)
    (ha : ∀ l,StarUnitary (a l)) (hb : ∀ y,StarUnitary (b y))
    (he : StarUnitary bextra) :
    vectorEval ψ (operatorSecond generalLambda a b+algebraHerm (a 0*bextra))≤d+1 := by
  rw [vectorEval_add]
  exact add_le_add (second_commuting_hilbert_bound hd ψ hψ a b ha hb)
    (aligned_commuting_hilbert_bound ψ hψ _ (starUnitary_mul (ha 0) he))

/-- Actual projective measurement encoding in a general C*-algebra. Physical
validity contains only the PVM identities, not any bound or maximality premise. -/
structure AlgebraPVM (d : ℕ) [NeZero d] (A : Type*) [CStarAlgebra A] where
  effect : Ix d → A
  selfadjoint : ∀ j,star (effect j)=effect j
  idempotent : ∀ j,effect j*effect j=effect j
  orthogonal : ∀ j k,j≠k → effect j*effect k=0
  complete : ∑ j,effect j=1

def algebraEncoded (M : AlgebraPVM d A) : A := ∑ j,chi j • M.effect j

theorem algebraPVM_mul (M : AlgebraPVM d A) (f g : Ix d → ℂ) :
    (∑ j,f j • M.effect j)*(∑ k,g k • M.effect k)=∑ j,(f j*g j) • M.effect j := by
  simp only [Finset.sum_mul,Finset.mul_sum,smul_mul_assoc,mul_smul_comm,Finset.smul_sum,smul_smul]
  apply Finset.sum_congr rfl
  intro j _
  rw [Finset.sum_eq_single j]
  · rw [M.idempotent]
    simp [smul_smul,mul_comm]
  · intro k _ hkj; rw [M.orthogonal k j hkj,smul_zero]
  · simp

theorem algebraEncoded_unitary (M : AlgebraPVM d A) : StarUnitary (algebraEncoded M) := by
  have hs : star (algebraEncoded M)=∑ j,star (chi j) • M.effect j := by
    simp [algebraEncoded,star_sum,star_smul,M.selfadjoint]
  constructor
  · rw [hs,algebraEncoded,algebraPVM_mul]
    simpa only [chi_star_mul,one_smul] using M.complete
  · rw [hs,algebraEncoded,algebraPVM_mul]
    have hc (j : Ix d) : chi j*star (chi j)=1 := by simpa [mul_comm] using chi_star_mul j
    simpa only [hc,one_smul] using M.complete

theorem algebraEncoded_power (M : AlgebraPVM d A) (n : ℕ) :
    algebraEncoded M^n=∑ j,chi ((n : Ix d)*j) • M.effect j := by
  induction n with
  | zero => simpa using M.complete.symm
  | succ n ih =>
    rw [pow_succ,ih,algebraEncoded,algebraPVM_mul]
    congr 1; funext j
    simp [Nat.cast_add,add_mul,chi_add]

theorem algebraEncoded_order (M : AlgebraPVM d A) : algebraEncoded M^d=1 := by
  rw [algebraEncoded_power]
  simpa using M.complete

theorem algebraPVM_cross_commute (M N : AlgebraPVM d A)
    (h : ∀ j k,M.effect j*N.effect k=N.effect k*M.effect j) :
    algebraEncoded M*algebraEncoded N=algebraEncoded N*algebraEncoded M := by
  unfold algebraEncoded
  simp only [Finset.sum_mul,Finset.mul_sum,smul_mul_assoc,mul_smul_comm,Finset.smul_sum,smul_smul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl; intro j _
  apply Finset.sum_congr rfl; intro k _
  rw [h,mul_comm (chi j)]


/-- The Hilbert bound instantiated with actual arbitrary-dimensional PVMs.
Cross-party commutation is required for every pair of measurement effects. -/
theorem first_commuting_PVM_upper (hd : 2≤d) (ψ : H) (hψ : ‖ψ‖=1)
    (a : Fin 2 → AlgebraPVM d (H →L[ℂ] H))
    (b : AugmentedInputs d → AlgebraPVM d (H →L[ℂ] H))
    (hc : ∀ x y i j,(a x).effect i*(b y).effect j=(b y).effect j*(a x).effect i) :
    vectorEval ψ (operatorFirst (algebraEncoded (a 0)) (algebraEncoded (a 1))
      (fun y => algebraEncoded (b (some y)))+
      algebraHerm (algebraEncoded (a 0)*algebraEncoded (b none)))≤
      2/Real.sin (Real.pi/(2*d))+1 := by
  exact first_augmented_commuting_hilbert_bound hd ψ hψ _ _ _ _
    (algebraEncoded_unitary _) (algebraEncoded_unitary _) (algebraEncoded_unitary _)
    (fun y => algebraEncoded_unitary _)
    (fun y => algebraPVM_cross_commute _ _ (hc 0 (some y)))
    (fun y => algebraPVM_cross_commute _ _ (hc 1 (some y)))

theorem second_commuting_PVM_upper (hd : 2≤d) (ψ : H) (hψ : ‖ψ‖=1)
    (a : Ix d → AlgebraPVM d (H →L[ℂ] H))
    (b : AugmentedInputs d → AlgebraPVM d (H →L[ℂ] H))
    (hc : ∀ x y i j,(a x).effect i*(b y).effect j=(b y).effect j*(a x).effect i) :
    vectorEval ψ (operatorSecond generalLambda (fun l => algebraEncoded (a l))
      (fun y => algebraEncoded (b (some y)))+
      algebraHerm (algebraEncoded (a 0)*algebraEncoded (b none)))≤d+1 := by
  exact second_augmented_commuting_hilbert_bound hd ψ hψ _ _ _
    (fun l => algebraEncoded_unitary _) (fun y => algebraEncoded_unitary _) (algebraEncoded_unitary _)

end CyclicBell.General
