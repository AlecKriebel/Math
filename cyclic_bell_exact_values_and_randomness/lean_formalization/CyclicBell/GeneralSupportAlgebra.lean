import CyclicBell.GeneralModel
import CyclicBell.GeneralFiniteSpectrum
import Mathlib.Data.Matrix.Rank

/-! Coordinate support and purification lemmas, including nonfaithful states.
The support is the range of the REDUCED density, not the whole Alice space.
Rectangular amplitude matrices represent any finite purifying environment.
UNCOMPILED SOURCE CANDIDATES. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {ι κ ε ν : Type*} [Fintype ι] [Fintype κ] [Fintype ε] [Fintype ν]
variable [DecidableEq ι] [DecidableEq κ] [DecidableEq ε] [DecidableEq ν]

def matrixRange (T : Matrix ι ν ℂ) : Submodule ℂ (ι → ℂ) := LinearMap.range T.mulVecLin

def frobeniusSq (T : Matrix ι ν ℂ) : ℝ := ∑ i,∑ j,Complex.normSq (T i j)

theorem frobeniusSq_nonnegative (T : Matrix ι ν ℂ) : 0≤frobeniusSq T :=
  Finset.sum_nonneg (fun i _ => Finset.sum_nonneg (fun j _ => Complex.normSq_nonneg _))

theorem frobeniusSq_eq_zero (T : Matrix ι ν ℂ) : frobeniusSq T=0 ↔ T=0 := by
  constructor
  · intro h
    ext i j
    have hi : (∑ k,Complex.normSq (T i k))=0 :=
      (Finset.sum_eq_zero_iff_of_nonneg (fun i _ =>
        Finset.sum_nonneg (fun j _ => Complex.normSq_nonneg _))).mp h i (Finset.mem_univ i)
    have hij := (Finset.sum_eq_zero_iff_of_nonneg (fun k _ => Complex.normSq_nonneg _)).mp hi j
      (Finset.mem_univ j)
    exact Complex.normSq_eq_zero.mp hij
  · rintro rfl
    simp [frobeniusSq]

theorem trace_gram_frobenius (T : Matrix ι ν ℂ) :
    Matrix.trace (T*T.conjTranspose)=(frobeniusSq T : ℂ) := by
  simp only [Matrix.trace,Matrix.diag_apply,Matrix.mul_apply,Matrix.conjTranspose_apply,
    Complex.mul_conj,frobeniusSq,Complex.ofReal_sum]

theorem matrixRange_mul_le (T : Matrix ι κ ℂ) (S : Matrix κ ν ℂ) :
    matrixRange (T*S)≤matrixRange T := by
  rintro x ⟨v,hv⟩
  refine ⟨S*ᵥv,?_⟩
  simpa only [Matrix.mulVecLin_apply,Matrix.mulVec_mulVec] using hv

theorem matrixRange_gram (T : Matrix ι ν ℂ) :
    matrixRange (T*T.conjTranspose)=matrixRange T := by
  apply Submodule.eq_of_le_of_finrank_eq (matrixRange_mul_le _ _)
  exact Matrix.rank_self_mul_conjTranspose T

/-- R annihilates the amplitude iff it annihilates the reduced-state support. -/
theorem support_cancellation (R : Mat ι) (T : Matrix ι ν ℂ) :
    R*T=0 ↔ ∀ x : matrixRange (T*T.conjTranspose),R*ᵥ(x : ι → ℂ)=0 := by
  rw [matrixRange_gram]
  constructor
  · intro h x
    obtain ⟨v,hv⟩ := x.property
    rw [← hv,Matrix.mulVecLin_apply,Matrix.mulVec_mulVec,h,Matrix.zero_mulVec]
  · intro h
    ext i j
    have hj : T*ᵥ(Pi.single j 1)∈matrixRange T := ⟨Pi.single j 1,rfl⟩
    have he := congrArg (fun v : ι → ℂ => v i) (h ⟨_,hj⟩)
    simpa [Matrix.mulVec_mulVec,Matrix.mulVec_single] using he

/-- Two-sided range invariance follows from an exact unitary intertwiner. -/
theorem range_intertwiner (T : Matrix ι ν ℂ) (A : Mat ι) (B : Mat ν)
    (hB : UnitaryRel B) (h : A*T=T*B) :
    (matrixRange T).map A.mulVecLin=matrixRange T := by
  have he : matrixRange (A*T)=(matrixRange T).map A.mulVecLin := by
    unfold matrixRange
    rw [Matrix.mulVecLin_mul,LinearMap.range_comp]
  rw [← he,h]
  apply le_antisymm (matrixRange_mul_le T B)
  have ht : T=(T*B)*B.conjTranspose := by rw [mul_assoc,hB.2,mul_one]
  nth_rw 1 [ht]
  exact matrixRange_mul_le _ _

theorem unitary_transpose {A : Mat ι} (hA : UnitaryRel A) : UnitaryRel A.transpose := by
  constructor
  · have h := congrArg Matrix.transpose hA.2
    simpa only [Matrix.transpose_mul,Matrix.transpose_one,Matrix.transpose_conjTranspose] using h
  · have h := congrArg Matrix.transpose hA.1
    simpa only [Matrix.transpose_mul,Matrix.transpose_one,Matrix.transpose_conjTranspose] using h

/-- The positive square root is an actual purification factor for every mixed state. -/
def stateFactor (ρ : StateOn ι) : Mat ι := ρ.positive.sqrt

theorem stateFactor_gram (ρ : StateOn ι) : stateFactor ρ*(stateFactor ρ).conjTranspose=ρ.density := by
  rw [(ρ.positive.posSemidef_sqrt).isHermitian.eq]
  exact ρ.positive.sqrt_mul_self

theorem stateFactor_normalized (ρ : StateOn ι) : frobeniusSq (stateFactor ρ)=1 := by
  have h := congrArg Matrix.trace (stateFactor_gram ρ)
  rw [trace_gram_frobenius,ρ.normalized] at h
  exact_mod_cast h

theorem state_square_frobenius (ρ : StateOn ι) (R : Mat ι) :
    stateEval ρ.density (R.conjTranspose*R)=frobeniusSq (R*stateFactor ρ) := by
  unfold stateEval
  rw [← stateFactor_gram ρ]
  have ht : Matrix.trace ((stateFactor ρ*(stateFactor ρ).conjTranspose)*(R.conjTranspose*R))=
      Matrix.trace ((R*stateFactor ρ)*(R*stateFactor ρ).conjTranspose) := by
    rw [Matrix.conjTranspose_mul]
    simp only [mul_assoc]
    rw [Matrix.trace_mul_comm]
    simp only [mul_assoc]
  rw [ht,trace_gram_frobenius,Complex.ofReal_re]

theorem state_square_zero_iff (ρ : StateOn ι) (R : Mat ι) :
    stateEval ρ.density (R.conjTranspose*R)=0 ↔ R*stateFactor ρ=0 := by
  rw [state_square_frobenius,frobeniusSq_eq_zero]

/-- Positive residual terms vanish individually. -/
theorem finite_positive_sum_zero {J : Type*} [Fintype J] (f : J → ℝ)
    (hf : ∀ j,0≤f j) (hs : ∑ j,f j=0) : ∀ j,f j=0 := by
  exact fun j => (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => hf j)).mp hs j (Finset.mem_univ j)

/-- Flatten a purification factor across Alice:(Bob,Eve). -/
def aliceAmplitude (L : Matrix (ι × κ) ε ℂ) : Matrix ι (κ × ε) ℂ :=
  fun i j => L (i,j.1) j.2

def bobRight (B : Mat κ) : Mat (κ × ε) := kron B.transpose 1

def partialTraceBob (ρ : Mat (ι × κ)) : Mat ι := fun i j => ∑ b,ρ (i,b) (j,b)

theorem amplitude_reduced (L : Matrix (ι × κ) ε ℂ) :
    partialTraceBob (L*L.conjTranspose)=aliceAmplitude L*(aliceAmplitude L).conjTranspose := by
  ext i j
  simp only [partialTraceBob,Matrix.mul_apply,Matrix.conjTranspose_apply,
    aliceAmplitude,Fintype.sum_prod_type]

theorem amplitude_left (A : Mat ι) (L : Matrix (ι × κ) ε ℂ) :
    aliceAmplitude (aliceLift (κ := κ) A*L)=A*aliceAmplitude L := by
  ext i ⟨b,e⟩
  simp [aliceAmplitude,aliceLift,kron,Matrix.mul_apply,Fintype.sum_prod_type]

theorem amplitude_right (B : Mat κ) (L : Matrix (ι × κ) ε ℂ) :
    aliceAmplitude (bobLift (ι := ι) B*L)=aliceAmplitude L*bobRight (ε := ε) B := by
  ext i ⟨b,e⟩
  simp [aliceAmplitude,bobLift,bobRight,kron,Matrix.mul_apply,Fintype.sum_prod_type,mul_comm]

theorem amplitude_tensor (A : Mat ι) (B : Mat κ) (L : Matrix (ι × κ) ε ℂ) :
    aliceAmplitude (kron A B*L)=A*aliceAmplitude L*bobRight (ε := ε) B := by
  rw [← lift_product,mul_assoc,amplitude_left,amplitude_right]
  simp [mul_assoc]

@[simp] theorem amplitude_add (L M : Matrix (ι × κ) ε ℂ) :
    aliceAmplitude (L+M)=aliceAmplitude L+aliceAmplitude M := rfl
@[simp] theorem amplitude_sub (L M : Matrix (ι × κ) ε ℂ) :
    aliceAmplitude (L-M)=aliceAmplitude L-aliceAmplitude M := rfl
@[simp] theorem amplitude_zero : aliceAmplitude (0 : Matrix (ι × κ) ε ℂ)=0 := rfl

theorem amplitude_injective : Function.Injective (aliceAmplitude : Matrix (ι × κ) ε ℂ → _) := by
  intro L M h
  ext ⟨i,b⟩ e
  exact congrArg (fun T : Matrix ι (κ × ε) ℂ => T i (b,e)) h

theorem bobRight_unitary {B : Mat κ} (hB : UnitaryRel B) :
    UnitaryRel (bobRight (ε := ε) B) := kron_unitary (unitary_transpose hB) UnitaryRel.one

theorem kron_pow (A : Mat ι) (B : Mat κ) (n : ℕ) : kron A B^n=kron (A^n) (B^n) := by
  induction n with
  | zero => simp
  | succ n ih => rw [pow_succ,ih,kron_mul,pow_succ,pow_succ]

theorem bobRight_order {d : ℕ} {B : Mat κ} (hB : B^d=1) :
    bobRight (ε := ε) B^d=1 := by
  simp [bobRight,kron_pow,← Matrix.transpose_pow,hB]

def aliceSupport (ρ : StateOn (ι × κ)) : Submodule ℂ (ι → ℂ) := matrixRange (partialTraceBob ρ.density)

theorem aliceSupport_amplitude (ρ : StateOn (ι × κ)) :
    aliceSupport ρ=matrixRange (aliceAmplitude (stateFactor ρ)) := by
  unfold aliceSupport
  rw [← stateFactor_gram ρ,amplitude_reduced,matrixRange_gram]

theorem aliceSupport_nonzero (ρ : StateOn (ι × κ)) : aliceSupport ρ≠⊥ := by
  rw [aliceSupport_amplitude]
  intro h
  have he : aliceAmplitude (stateFactor ρ)=0 := by
    ext i ⟨b,e⟩
    have hv : aliceAmplitude (stateFactor ρ)*ᵥ(Pi.single (b,e) 1)∈
        matrixRange (aliceAmplitude (stateFactor ρ)) := ⟨_,rfl⟩
    rw [h,Submodule.mem_bot] at hv
    simpa [Matrix.mulVec_single] using congrArg (fun v : ι → ℂ => v i) hv
  have hf : stateFactor ρ=0 := amplitude_injective he
  have hn := stateFactor_normalized ρ
  simp [hf,frobeniusSq] at hn

def preservesRange (A : Mat ι) (K : Submodule ℂ (ι → ℂ)) : Prop :=
  ∀ x,x∈K → A*ᵥx∈K

def restrictMatrix (A : Mat ι) (K : Submodule ℂ (ι → ℂ)) (h : preservesRange A K) : K →ₗ[ℂ] K where
  toFun x := ⟨A*ᵥx,h x x.property⟩
  map_add' x y := Subtype.ext (Matrix.mulVec_add A x y)
  map_smul' c x := Subtype.ext (Matrix.mulVec_smul A c x)

theorem preserves_of_intertwiner (T : Matrix ι ν ℂ) (A : Mat ι) (B : Mat ν) (h : A*T=T*B) :
    preservesRange A (matrixRange T) := by
  rintro x ⟨v,hv⟩
  refine ⟨B*ᵥv,?_⟩
  rw [← hv,Matrix.mulVecLin_apply,Matrix.mulVec_mulVec,h,Matrix.mulVec_mulVec]

/-- Kernel-safe cancellation on a specified spectral support. The two premises
are explicit range/kernel evidence, not an inverse assumption. -/
theorem supported_kernel_cancel (H J E : Mat ι) (Q : Matrix ι ν ℂ)
    (hJ : J*H=E) (hE : E*Q=Q) (hH : H*Q=0) : Q=0 := by
  rw [← hE,← hJ,mul_assoc,hH,mul_zero]

end CyclicBell.General
