import CyclicBell.GeneralOperational
import CyclicBell.GeneralCommuting
import CyclicBell.GeneralSupportAlgebra

/-! Binary benchmark: the actual two-square SOS and privacy from on-state
relations. No global anticommutation is inferred from saturation. The private
conditional states use GeneralOperational's actual sandwich/partial trace.
UNCOMPILED SOURCE CANDIDATES; prior-art benchmark, not a novelty claim. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder InnerProductSpace
namespace CyclicBell.General
variable {ι ε : Type*} [Fintype ι] [Fintype ε] [DecidableEq ι] [DecidableEq ε]

def HermitianInvolution (A : Mat ι) : Prop := A.IsHermitian ∧ A*A=1

def binaryScoreOperator (A₀ A₁ B₀ B₁ : Mat ι) : Mat ι :=
  A₀*B₀-(2 : ℂ) • (A₀*B₁)+(2 : ℂ) • (A₁*B₀)+(2 : ℂ) • (A₁*B₁)

def binaryResidual₀ (A₀ B₀ B₁ : Mat ι) : Mat ι :=
  (Real.sqrt 3 : ℂ) • A₀-B₀+(2 : ℂ) • B₁

def binaryResidual₁ (A₁ B₀ B₁ : Mat ι) : Mat ι :=
  (Real.sqrt 3 : ℂ) • A₁-B₀-B₁

def BinaryCross (A₀ A₁ B₀ B₁ : Mat ι) : Prop :=
  A₀*B₀=B₀*A₀ ∧ A₀*B₁=B₁*A₀ ∧ A₁*B₀=B₀*A₁ ∧ A₁*B₁=B₁*A₁

theorem sqrt_three_positive : 0<Real.sqrt 3 := Real.sqrt_pos.2 (by norm_num)

theorem sqrt_three_square : (Real.sqrt 3 : ℂ)^2=3 := by
  norm_cast
  exact Real.sq_sqrt (by norm_num)

/-- Eq:binary-sos. The two Bob anticommutator terms cancel, rather than being
set to zero or made commuting by an extra hypothesis. -/
theorem binary_operator_sos (A₀ A₁ B₀ B₁ : Mat ι)
    (hA₀ : HermitianInvolution A₀) (hA₁ : HermitianInvolution A₁)
    (hB₀ : HermitianInvolution B₀) (hB₁ : HermitianInvolution B₁)
    (hc : BinaryCross A₀ A₁ B₀ B₁) :
    ((3*Real.sqrt 3 : ℝ) : ℂ) • (1 : Mat ι)-binaryScoreOperator A₀ A₁ B₀ B₁=
      (1/(2*(Real.sqrt 3 : ℂ))) •
        ((binaryResidual₀ A₀ B₀ B₁).conjTranspose*binaryResidual₀ A₀ B₀ B₁)+
      (1/(Real.sqrt 3 : ℂ)) •
        ((binaryResidual₁ A₁ B₀ B₁).conjTranspose*binaryResidual₁ A₁ B₀ B₁) := by
  have hs : (Real.sqrt 3 : ℂ)≠0 := by exact_mod_cast ne_of_gt sqrt_three_positive
  rcases hc with ⟨hc00,hc01,hc10,hc11⟩
  unfold binaryResidual₀ binaryResidual₁ binaryScoreOperator
  simp only [Matrix.conjTranspose_add,Matrix.conjTranspose_sub,Matrix.conjTranspose_smul,
    hA₀.1.eq,hA₁.1.eq,hB₀.1.eq,hB₁.1.eq,star_natCast,Complex.conj_ofReal,
    Matrix.add_mul,Matrix.mul_add,Matrix.sub_mul,Matrix.mul_sub,Matrix.smul_mul,Matrix.mul_smul,smul_smul,
    hA₀.2,hA₁.2,hB₀.2,hB₁.2,← hc00,← hc01,← hc10,← hc11]
  ext i j
  simp only [Matrix.add_apply,Matrix.sub_apply,Matrix.smul_apply,smul_eq_mul]
  push_cast
  field_simp
  linear_combination (3*(Real.sqrt 3 : ℂ)*(1 : Mat ι) i j)*(sqrt_three_square)

/-- Purification coefficients define the reduced AB state, not an assumed
faithful density. The environment may have any finite dimension. -/
def amplitudeState (T : Matrix ι ε ℂ) (hT : frobeniusSq T=1) : StateOn ι where
  density := T*T.conjTranspose
  positive := by
    simpa only [Matrix.conjTranspose_conjTranspose] using
      Matrix.posSemidef_conjTranspose_mul_self T.conjTranspose
  normalized := by rw [trace_gram_frobenius,hT]; norm_num

theorem amplitude_square (T : Matrix ι ε ℂ) (R : Mat ι) :
    stateEval (T*T.conjTranspose) (R.conjTranspose*R)=frobeniusSq (R*T) := by
  unfold stateEval
  have ht : Matrix.trace ((T*T.conjTranspose)*(R.conjTranspose*R))=
      Matrix.trace ((R*T)*(R*T).conjTranspose) := by
    rw [Matrix.conjTranspose_mul]
    rw [Matrix.trace_mul_cycle' (T*T.conjTranspose) R.conjTranspose R]
    simp only [Matrix.mul_assoc]
  rw [ht,trace_gram_frobenius,Complex.ofReal_re]

theorem binary_mixed_upper (ρ : StateOn ι) (A₀ A₁ B₀ B₁ : Mat ι)
    (hA₀ : HermitianInvolution A₀) (hA₁ : HermitianInvolution A₁)
    (hB₀ : HermitianInvolution B₀) (hB₁ : HermitianInvolution B₁)
    (hc : BinaryCross A₀ A₁ B₀ B₁) :
    stateEval ρ.density (binaryScoreOperator A₀ A₁ B₀ B₁)≤3*Real.sqrt 3 := by
  have h := congrArg (stateEval ρ.density) (binary_operator_sos A₀ A₁ B₀ B₁ hA₀ hA₁ hB₀ hB₁ hc)
  have h₀ : (1/(2*(Real.sqrt 3 : ℂ)))=((1/(2*Real.sqrt 3) : ℝ) : ℂ) := by push_cast; rfl
  have h₁ : (1/(Real.sqrt 3 : ℂ))=((1/Real.sqrt 3 : ℝ) : ℂ) := by push_cast; rfl
  simp only [stateEval_sub,stateEval_add,h₀,h₁,stateEval_real_smul,stateEval_one ρ.normalized] at h
  have hp₀ := stateEval_square_nonnegative ρ.positive (binaryResidual₀ A₀ B₀ B₁)
  have hp₁ := stateEval_square_nonnegative ρ.positive (binaryResidual₁ A₁ B₀ B₁)
  have hc₀ : 0<1/(2*Real.sqrt 3) := by positivity
  have hc₁ : 0<1/Real.sqrt 3 := by positivity
  nlinarith

theorem binary_saturation_residuals (T : Matrix ι ε ℂ) (hT : frobeniusSq T=1)
    (A₀ A₁ B₀ B₁ : Mat ι)
    (hA₀ : HermitianInvolution A₀) (hA₁ : HermitianInvolution A₁)
    (hB₀ : HermitianInvolution B₀) (hB₁ : HermitianInvolution B₁)
    (hc : BinaryCross A₀ A₁ B₀ B₁)
    (hsat : stateEval (T*T.conjTranspose) (binaryScoreOperator A₀ A₁ B₀ B₁)=3*Real.sqrt 3) :
    binaryResidual₀ A₀ B₀ B₁*T=0 ∧ binaryResidual₁ A₁ B₀ B₁*T=0 := by
  have h := congrArg (stateEval (amplitudeState T hT).density)
    (binary_operator_sos A₀ A₁ B₀ B₁ hA₀ hA₁ hB₀ hB₁ hc)
  have h₀ : (1/(2*(Real.sqrt 3 : ℂ)))=((1/(2*Real.sqrt 3) : ℝ) : ℂ) := by push_cast; rfl
  have h₁ : (1/(Real.sqrt 3 : ℂ))=((1/Real.sqrt 3 : ℝ) : ℂ) := by push_cast; rfl
  simp only [stateEval_sub,stateEval_add,h₀,h₁,stateEval_real_smul,
    stateEval_one (amplitudeState T hT).normalized,amplitudeState,amplitude_square,hsat] at h
  have hnorm : stateEval (T*T.conjTranspose) (1 : Mat ι)=1 := by
    unfold stateEval
    rw [Matrix.mul_one,trace_gram_frobenius,hT]
    norm_num
  rw [hnorm] at h
  have hp₀ := frobeniusSq_nonnegative (binaryResidual₀ A₀ B₀ B₁*T)
  have hp₁ := frobeniusSq_nonnegative (binaryResidual₁ A₁ B₀ B₁*T)
  have hc₀ : 0<1/(2*Real.sqrt 3) := by positivity
  have hc₁ : 0<1/Real.sqrt 3 := by positivity
  constructor <;> apply (frobeniusSq_eq_zero _).mp <;> nlinarith

/-! Elementary partial-trace identities used by the privacy proof. -/
theorem effectKernelE_add (T : Matrix ι ε ℂ) (X Y : Mat ι) :
    effectKernelE T (X+Y)=effectKernelE T X+effectKernelE T Y := by
  simp [effectKernelE,Matrix.transpose_add,Matrix.mul_add,Matrix.add_mul]

theorem effectKernelE_adjoint (T : Matrix ι ε ℂ) (X : Mat ι) :
    (effectKernelE T X).conjTranspose=effectKernelE T X.conjTranspose := by
  ext e f
  simp only [effectKernelE,Matrix.conjTranspose_apply,Matrix.mul_apply,
    Matrix.transpose_apply,Matrix.map_apply,star_sum,star_mul,star_star,
    Finset.mul_sum,Finset.sum_mul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl; intro i _
  apply Finset.sum_congr rfl; intro j _
  ring

theorem effectKernelE_left_stabilizer (T : Matrix ι ε ℂ) (S X : Mat ι)
    (hS : S.IsHermitian) (hST : S*T=T) : effectKernelE T (S*X)=effectKernelE T X := by
  have hs : S.transpose*T.map star=T.map star := by
    have hh := congrArg (fun R : Matrix ι ε ℂ => R.map star) hST
    have hconj : S.map star=S.transpose := by
      ext i j; have hx := congrFun (congrFun hS.eq j) i
      simpa [Matrix.conjTranspose_apply] using hx
    change (S*T).map (starRingEnd ℂ) = T.map (starRingEnd ℂ) at hh
    rw [Matrix.map_mul] at hh
    change S.map star * T.map star = T.map star at hh
    rw [hconj] at hh
    exact hh
  simp only [effectKernelE,Matrix.transpose_mul,Matrix.mul_assoc,hs]

theorem effectKernelE_anti_stabilizer (T : Matrix ι ε ℂ) (S X : Mat ι)
    (hS : S.IsHermitian) (hST : S*T=T) (hanti : (S*X+X*S)*T=0) :
    effectKernelE T X=0 := by
  have he : (S*X)*T=(-1 : ℂ) • (X*T) := by
    have ha := hanti
    rw [Matrix.add_mul,Matrix.mul_assoc X,hST] at ha
    simpa [neg_smul] using eq_neg_of_add_eq_zero_left ha
  have h₁ := effectKernelE_on_state T (S*X) ((-1 : ℂ) • X)
    (by simpa [Matrix.smul_mul] using he)
  rw [effectKernelE_left_stabilizer T S X hS hST,effectKernelE_smul] at h₁
  ext e f
  have h := congrFun (congrFun h₁ e) f
  simp only [Matrix.smul_apply,smul_eq_mul] at h
  change effectKernelE T X e f = 0
  linear_combination (1/2 : ℂ)*h

def binaryXA (A₀ A₁ : Mat ι) : Mat ι := (1/(Real.sqrt 3 : ℂ)) • (A₀+(2 : ℂ) • A₁)
def binaryZB (B₀ B₁ : Mat ι) : Mat ι := (1/(Real.sqrt 3 : ℂ)) • (B₀-(2 : ℂ) • B₁)

/-- The structural step is proved from the two on-state residuals, not from
assumed global Clifford/Pauli or anticommutator relations. -/
theorem binary_on_state_structure (T : Matrix ι ε ℂ) (A₀ A₁ B₀ B₁ : Mat ι)
    (hA₀ : HermitianInvolution A₀) (hA₁ : HermitianInvolution A₁)
    (hB₀ : HermitianInvolution B₀) (hB₁ : HermitianInvolution B₁)
    (hc : BinaryCross A₀ A₁ B₀ B₁)
    (hr₀ : binaryResidual₀ A₀ B₀ B₁*T=0)
    (hr₁ : binaryResidual₁ A₁ B₀ B₁*T=0) :
    B₀*T=binaryXA A₀ A₁*T ∧ binaryZB B₀ B₁*T=A₀*T ∧
    (binaryXA A₀ A₁*binaryXA A₀ A₁)*T=T ∧
    (binaryZB B₀ B₁*binaryZB B₀ B₁)*T=T ∧
    (A₀*binaryXA A₀ A₁+binaryXA A₀ A₁*A₀)*T=0 ∧
    (binaryZB B₀ B₁*B₀+B₀*binaryZB B₀ B₁)*T=0 := by
  have hs : (Real.sqrt 3 : ℂ)≠0 := by exact_mod_cast ne_of_gt sqrt_three_positive
  rcases hc with ⟨hc00,hc01,hc10,hc11⟩
  have hratio : (Real.sqrt 3 : ℂ)/3=1/(Real.sqrt 3 : ℂ) := by
    apply (div_eq_div_iff (by norm_num) hs).mpr
    simpa [pow_two] using sqrt_three_square
  have hb : B₀*T=binaryXA A₀ A₁*T := by
    have he : B₀*T=((Real.sqrt 3 : ℂ)/3) • ((A₀+(2 : ℂ) • A₁)*T) := by
      ext i e
      have h0 := congrFun (congrFun hr₀ i) e
      have h1 := congrFun (congrFun hr₁ i) e
      simp only [binaryResidual₀,binaryResidual₁,Matrix.add_mul,Matrix.sub_mul,Matrix.smul_mul,
        Matrix.add_apply,Matrix.sub_apply,Matrix.smul_apply,smul_eq_mul,Matrix.zero_apply] at h0 h1
      simp only [Matrix.add_mul,Matrix.smul_mul,Matrix.add_apply,Matrix.smul_apply,smul_eq_mul]
      linear_combination (-1/3 : ℂ)*h0+(-2/3 : ℂ)*h1
    simpa only [hratio,binaryXA,Matrix.smul_mul] using he
  have hz : binaryZB B₀ B₁*T=A₀*T := by
    ext i e
    have h0 := congrFun (congrFun hr₀ i) e
    simp only [binaryResidual₀,Matrix.add_mul,Matrix.sub_mul,Matrix.smul_mul,
      Matrix.add_apply,Matrix.sub_apply,Matrix.smul_apply,smul_eq_mul,Matrix.zero_apply] at h0
    simp only [binaryZB,Matrix.sub_mul,Matrix.smul_mul,Matrix.sub_apply,
      Matrix.smul_apply,smul_eq_mul]
    field_simp [hs]
    linear_combination -h0
  have hXB : binaryXA A₀ A₁*B₀=B₀*binaryXA A₀ A₁ := by
    simp [binaryXA,Matrix.add_mul,Matrix.mul_add,Matrix.smul_mul,Matrix.mul_smul,hc00,hc10]
  have hZA : binaryZB B₀ B₁*A₀=A₀*binaryZB B₀ B₁ := by
    simp [binaryZB,Matrix.sub_mul,Matrix.mul_sub,Matrix.smul_mul,Matrix.mul_smul,hc00,hc01]
  have hXX : (binaryXA A₀ A₁*binaryXA A₀ A₁)*T=T := by
    rw [Matrix.mul_assoc,← hb,← Matrix.mul_assoc,hXB,Matrix.mul_assoc,← hb,← Matrix.mul_assoc,hB₀.2,Matrix.one_mul]
  have hZZ : (binaryZB B₀ B₁*binaryZB B₀ B₁)*T=T := by
    rw [Matrix.mul_assoc,hz,← Matrix.mul_assoc,hZA,Matrix.mul_assoc,hz,← Matrix.mul_assoc,hA₀.2,Matrix.one_mul]
  have hxpoly : A₀*binaryXA A₀ A₁+binaryXA A₀ A₁*A₀=
      (Real.sqrt 3 : ℂ) • (binaryXA A₀ A₁*binaryXA A₀ A₁-1) := by
    unfold binaryXA
    simp only [Matrix.mul_add,Matrix.add_mul,Matrix.smul_mul,Matrix.mul_smul,smul_add,smul_sub,
      smul_smul,hA₀.2,hA₁.2]
    ext i j
    simp only [Matrix.add_apply,Matrix.sub_apply,Matrix.smul_apply,smul_eq_mul]
    field_simp [hs]
    ring_nf
    linear_combination ((1 : Mat ι) i j*(Real.sqrt 3 : ℂ)^5)*sqrt_three_square
  have hzpoly : binaryZB B₀ B₁*B₀+B₀*binaryZB B₀ B₁=
      (Real.sqrt 3 : ℂ) • (binaryZB B₀ B₁*binaryZB B₀ B₁-1) := by
    unfold binaryZB
    simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.smul_mul,Matrix.mul_smul,smul_sub,
      smul_smul,hB₀.2,hB₁.2]
    ext i j
    simp only [Matrix.add_apply,Matrix.sub_apply,Matrix.smul_apply,smul_eq_mul]
    field_simp [hs]
    ring_nf
    linear_combination ((1 : Mat ι) i j*(Real.sqrt 3 : ℂ)^5)*sqrt_three_square
  refine ⟨hb,hz,hXX,hZZ,?_,?_⟩
  · rw [hxpoly,Matrix.smul_mul,Matrix.sub_mul,hXX,Matrix.one_mul,sub_self,smul_zero]
  · rw [hzpoly,Matrix.smul_mul,Matrix.sub_mul,hZZ,Matrix.one_mul,sub_self,smul_zero]

/-- All three nontrivial OPERATOR-valued binary Fourier coefficients vanish. -/
theorem binary_private_moments (T : Matrix ι ε ℂ) (A₀ A₁ B₀ B₁ : Mat ι)
    (hA₀ : HermitianInvolution A₀) (hA₁ : HermitianInvolution A₁)
    (hB₀ : HermitianInvolution B₀) (hB₁ : HermitianInvolution B₁)
    (hc : BinaryCross A₀ A₁ B₀ B₁)
    (hr₀ : binaryResidual₀ A₀ B₀ B₁*T=0)
    (hr₁ : binaryResidual₁ A₁ B₀ B₁*T=0) :
    effectKernelE T A₀=0 ∧ effectKernelE T B₀=0 ∧ effectKernelE T (A₀*B₀)=0 := by
  obtain ⟨hb,hz,hXX,hZZ,hantiX,hantiZ⟩ :=
    binary_on_state_structure T A₀ A₁ B₀ B₁ hA₀ hA₁ hB₀ hB₁ hc hr₀ hr₁
  have hX : (binaryXA A₀ A₁).IsHermitian := by
    simp [Matrix.IsHermitian,binaryXA,Matrix.conjTranspose_smul,Matrix.conjTranspose_add,hA₀.1.eq,hA₁.1.eq]
  have hZ : (binaryZB B₀ B₁).IsHermitian := by
    simp [Matrix.IsHermitian,binaryZB,Matrix.conjTranspose_smul,Matrix.conjTranspose_sub,hB₀.1.eq,hB₁.1.eq]
  rcases hc with ⟨hc00,hc01,hc10,hc11⟩
  have hXB : binaryXA A₀ A₁*B₀=B₀*binaryXA A₀ A₁ := by
    simp [binaryXA,Matrix.add_mul,Matrix.mul_add,Matrix.smul_mul,Matrix.mul_smul,hc00,hc10]
  have hZA : binaryZB B₀ B₁*A₀=A₀*binaryZB B₀ B₁ := by
    simp [binaryZB,Matrix.sub_mul,Matrix.mul_sub,Matrix.smul_mul,Matrix.mul_smul,hc00,hc01]
  have hSA : (binaryXA A₀ A₁*B₀).IsHermitian := by
    simpa [Matrix.IsHermitian,Matrix.conjTranspose_mul,hX.eq,hB₀.1.eq] using hXB.symm
  have hSB : (A₀*binaryZB B₀ B₁).IsHermitian := by
    simpa [Matrix.IsHermitian,Matrix.conjTranspose_mul,hZ.eq,hA₀.1.eq] using hZA
  have hSAT : (binaryXA A₀ A₁*B₀)*T=T := by rw [Matrix.mul_assoc,hb,← Matrix.mul_assoc,hXX]
  have hSBT : (A₀*binaryZB B₀ B₁)*T=T := by rw [Matrix.mul_assoc,hz,← Matrix.mul_assoc,hA₀.2,Matrix.one_mul]
  have hSAanti : ((binaryXA A₀ A₁*B₀)*A₀+A₀*(binaryXA A₀ A₁*B₀))*T=0 := by
    calc _=B₀*((binaryXA A₀ A₁*A₀+A₀*binaryXA A₀ A₁)*T) := by
           rw [hXB]
           simp only [Matrix.mul_add,Matrix.add_mul,← Matrix.mul_assoc,hc00]
         _=0 := by rw [add_comm,hantiX,Matrix.mul_zero]
  have hSBanti : ((A₀*binaryZB B₀ B₁)*B₀+B₀*(A₀*binaryZB B₀ B₁))*T=0 := by
    calc _=A₀*((binaryZB B₀ B₁*B₀+B₀*binaryZB B₀ B₁)*T) := by
           simp only [Matrix.mul_add,Matrix.add_mul,← Matrix.mul_assoc,← hc00]
         _=0 := by rw [hantiZ,Matrix.mul_zero]
  refine ⟨effectKernelE_anti_stabilizer T _ A₀ hSA hSAT hSAanti,
    effectKernelE_anti_stabilizer T _ B₀ hSB hSBT hSBanti,?_⟩
  have hroute : (A₀*B₀)*T=(A₀*binaryXA A₀ A₁)*T := by rw [Matrix.mul_assoc,hb,Matrix.mul_assoc]
  have hjoint := effectKernelE_on_state T _ _ hroute
  have hjHerm : (effectKernelE T (A₀*B₀)).conjTranspose=effectKernelE T (A₀*B₀) := by
    rw [effectKernelE_adjoint,Matrix.conjTranspose_mul,hA₀.1.eq,hB₀.1.eq,← hc00]
  have hanti : (binaryXA A₀ A₁*A₀)*T=((-1 : ℂ) • (A₀*binaryXA A₀ A₁))*T := by
    have hh := hantiX
    rw [Matrix.add_mul] at hh
    simpa [neg_smul,Matrix.smul_mul] using eq_neg_of_add_eq_zero_right hh
  have hk := effectKernelE_on_state T _ _ hanti
  rw [effectKernelE_smul] at hk
  rw [hjoint,effectKernelE_adjoint,Matrix.conjTranspose_mul,hX.eq,hA₀.1.eq,hk] at hjHerm
  ext e f
  have hh := congrFun (congrFun hjHerm e) f
  simp only [Matrix.smul_apply,smul_eq_mul] at hh
  rw [hjoint]
  change effectKernelE T (A₀*binaryXA A₀ A₁) e f = 0
  linear_combination (-1/2 : ℂ)*hh

def binaryEffect (A : Mat ι) (a : Fin 2) : Mat ι :=
  (1/2 : ℂ) • (1+(-1 : ℂ)^a.val • A)

theorem binaryEffect_hermitian (A : Mat ι) (hA : A.IsHermitian) (a : Fin 2) :
    (binaryEffect A a).IsHermitian := by
  fin_cases a <;> simp [binaryEffect,Matrix.IsHermitian,Matrix.conjTranspose_smul,
    Matrix.conjTranspose_add,hA.eq]

theorem binaryEffect_idempotent (A : Mat ι) (hA : A*A=1) (a : Fin 2) :
    binaryEffect A a*binaryEffect A a=binaryEffect A a := by
  fin_cases a <;> simp [binaryEffect,Matrix.smul_mul,Matrix.mul_smul,smul_smul,Matrix.add_mul,Matrix.mul_add,hA]
  all_goals module

theorem binaryEffect_positive (A : Mat ι) (hA : HermitianInvolution A) (a : Fin 2) :
    (binaryEffect A a).PosSemidef := by
  have hp := Matrix.posSemidef_conjTranspose_mul_self (binaryEffect A a)
  rwa [(binaryEffect_hermitian A hA.1 a).eq,binaryEffect_idempotent A hA.2 a] at hp

theorem binaryEffect_complete (A : Mat ι) : (∑ a : Fin 2,binaryEffect A a)=1 := by
  simp [Fin.sum_univ_succ,binaryEffect]
  module

theorem binaryEffect_orthogonal (A : Mat ι) (hA : A*A=1) (a b : Fin 2) (hab : a≠b) :
    binaryEffect A a*binaryEffect A b=0 := by
  fin_cases a <;> fin_cases b <;> try contradiction
  all_goals simp [binaryEffect,Matrix.smul_mul,Matrix.mul_smul,smul_smul,Matrix.add_mul,Matrix.mul_add,hA]
  all_goals module

/-- Manuscript binary privacy endpoint for arbitrary finite purifying Eve.
The hypothesis is the actual scalar maximum, not the on-state identities or
privacy being concluded. Actual sandwiches give the conditional E matrices. -/
theorem binary_saturation_privacy (T : Matrix ι ε ℂ) (hT : frobeniusSq T=1)
    (A₀ A₁ B₀ B₁ : Mat ι)
    (hA₀ : HermitianInvolution A₀) (hA₁ : HermitianInvolution A₁)
    (hB₀ : HermitianInvolution B₀) (hB₁ : HermitianInvolution B₁)
    (hc : BinaryCross A₀ A₁ B₀ B₁)
    (hsat : stateEval (T*T.conjTranspose) (binaryScoreOperator A₀ A₁ B₀ B₁)=3*Real.sqrt 3) :
    ∀ a b : Fin 2,conditionalE T (binaryEffect A₀ a*binaryEffect B₀ b)=
      (1/4 : ℂ) • reducedE T := by
  obtain ⟨hr₀,hr₁⟩ := binary_saturation_residuals T hT A₀ A₁ B₀ B₁ hA₀ hA₁ hB₀ hB₁ hc hsat
  obtain ⟨hmA,hmB,hmAB⟩ := binary_private_moments T A₀ A₁ B₀ B₁ hA₀ hA₁ hB₀ hB₁ hc hr₀ hr₁
  intro a b
  have hcomm : binaryEffect A₀ a*binaryEffect B₀ b=binaryEffect B₀ b*binaryEffect A₀ a := by
    unfold binaryEffect
    simp only [Matrix.smul_mul,Matrix.mul_smul,smul_smul,Matrix.add_mul,Matrix.mul_add,Matrix.one_mul,Matrix.mul_one,hc.1]
    module
  have hHerm : (binaryEffect A₀ a*binaryEffect B₀ b).IsHermitian := by
    simpa [Matrix.IsHermitian,Matrix.conjTranspose_mul,
      (binaryEffect_hermitian A₀ hA₀.1 a).eq,(binaryEffect_hermitian B₀ hB₀.1 b).eq] using hcomm.symm
  have hId : (binaryEffect A₀ a*binaryEffect B₀ b)*(binaryEffect A₀ a*binaryEffect B₀ b)=
      binaryEffect A₀ a*binaryEffect B₀ b := by
    calc _=(binaryEffect A₀ a*binaryEffect A₀ a)*(binaryEffect B₀ b*binaryEffect B₀ b) := by
           rw [Matrix.mul_assoc,← Matrix.mul_assoc (binaryEffect B₀ b),← hcomm]
           simp only [Matrix.mul_assoc]
         _=_ := by rw [binaryEffect_idempotent A₀ hA₀.2,binaryEffect_idempotent B₀ hB₀.2]
  rw [conditionalE_effectKernel T _ hHerm hId]
  unfold binaryEffect
  simp only [Matrix.smul_mul,Matrix.mul_smul,smul_smul,Matrix.add_mul,Matrix.mul_add,Matrix.one_mul,Matrix.mul_one,
    effectKernelE_smul,effectKernelE_add,hmA,hmB,hmAB,smul_zero,add_zero,zero_add]
  have hI : effectKernelE T (1 : Mat ι)=reducedE T := by simp [effectKernelE,reducedE]
  rw [hI]
  norm_num

end CyclicBell.General
