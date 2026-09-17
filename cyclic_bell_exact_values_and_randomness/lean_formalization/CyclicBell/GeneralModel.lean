import CyclicBell.GeneralFourier
import CyclicBell.TraceCalculus

/-! Finite-dimensional tensor strategies with ARBITRARY outcome number d and
ARBITRARY finite local coordinate types. These structures have only physical
fields; no Bell bound, equality spectrum, attainment or output table is assumed.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {ι κ : Type*} [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ]

structure StateOn (ι : Type*) [Fintype ι] where
  density : Matrix ι ι ℂ
  positive : density.PosSemidef
  normalized : Matrix.trace density = 1

structure Measurement (d : ℕ) [NeZero d] (ι : Type*) [Fintype ι] [DecidableEq ι] where
  effect : Ix d → Matrix ι ι ℂ
  positive : ∀ a, (effect a).PosSemidef
  complete : ∑ a, effect a = 1
  idempotent : ∀ a, effect a * effect a = effect a
  orthogonal : ∀ a b, a ≠ b → effect a * effect b = 0

def encoded (M : Measurement d ι) : Mat ι := ∑ a, chi a • M.effect a

def kron (A : Mat ι) (B : Mat κ) : Mat (ι × κ) :=
  fun i j => A i.1 j.1 * B i.2 j.2

def vectorTensor (u : ι → ℂ) (v : κ → ℂ) : ι × κ → ℂ :=
  fun i => u i.1 * v i.2

def bornProbability (ρ : Mat (ι × κ)) (M : Mat ι) (N : Mat κ) : ℝ :=
  stateEval ρ (kron M N)

/-- Option.none is the extra Bob input d; Option.some y is reduced input y. -/
abbrev AugmentedInputs (d : ℕ) := Option (Ix d)

structure StrategyOn (d : ℕ) [NeZero d] (α β ι κ : Type*)
    [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ] where
  state : StateOn (ι × κ)
  alice : α → Measurement d ι
  bob : β → Measurement d κ

def behavior {α β : Type*} (s : StrategyOn d α β ι κ)
    (x : α) (y : β) (a b : Ix d) : ℝ :=
  bornProbability s.state.density ((s.alice x).effect a) ((s.bob y).effect b)

/-- The new tensor is exactly the old coordinate formula on Fin types. -/
theorem kron_eq_tensor {nA nB : ℕ} (A : Op nA) (B : Op nB) :
    kron A B = CyclicBell.tensor A B := rfl

@[simp] theorem kron_mul (A C : Mat ι) (B D : Mat κ) :
    kron A B * kron C D = kron (A*C) (B*D) := by
  ext i j
  simp only [kron, Matrix.mul_apply, Fintype.sum_prod_type,
    Finset.sum_mul, Finset.mul_sum]
  rw [Finset.sum_comm (f := fun k l => A i.1 l * C l j.1 * (B i.2 k * D k j.2))]
  apply Finset.sum_congr rfl
  intro k _
  apply Finset.sum_congr rfl
  intro l _
  ring

@[simp] theorem kron_star (A : Mat ι) (B : Mat κ) :
    (kron A B).conjTranspose = kron A.conjTranspose B.conjTranspose := by
  ext i j
  simp [kron, Matrix.conjTranspose_apply, mul_comm]

@[simp] theorem kron_one : kron (1 : Mat ι) (1 : Mat κ) = 1 := by
  ext ⟨i,k⟩ ⟨j,l⟩
  by_cases h : i=j <;> by_cases h' : k=l <;>
    simp [kron, Matrix.one_apply, h, h', Prod.mk.injEq]

@[simp] theorem kron_add_left (A C : Mat ι) (B : Mat κ) :
    kron (A+C) B = kron A B + kron C B := by ext i j; simp [kron, add_mul]

@[simp] theorem kron_add_right (A : Mat ι) (B D : Mat κ) :
    kron A (B+D) = kron A B + kron A D := by ext i j; simp [kron, mul_add]

@[simp] theorem kron_smul_left (z : ℂ) (A : Mat ι) (B : Mat κ) :
    kron (z • A) B = z • kron A B := by ext i j; simp [kron, mul_assoc]

@[simp] theorem kron_smul_right (z : ℂ) (A : Mat ι) (B : Mat κ) :
    kron A (z • B) = z • kron A B := by ext i j; simp [kron]; ring

@[simp] theorem kron_sum_left {ν : Type*} [Fintype ν] (A : ν → Mat ι) (B : Mat κ) :
    kron (∑ a, A a) B = ∑ a, kron (A a) B := by ext i j; simp [kron, Matrix.sum_apply, Finset.sum_apply, Finset.sum_mul]

@[simp] theorem kron_sum_right {ν : Type*} [Fintype ν] (A : Mat ι) (B : ν → Mat κ) :
    kron A (∑ b, B b) = ∑ b, kron A (B b) := by ext i j; simp [kron, Matrix.sum_apply, Finset.sum_apply, Finset.mul_sum]

theorem kron_unitary {A : Mat ι} {B : Mat κ} (hA : UnitaryRel A) (hB : UnitaryRel B) :
    UnitaryRel (kron A B) := by
  constructor <;> simp only [kron_star, kron_mul, hA.1,hA.2,hB.1,hB.2,kron_one]

def aliceLift (A : Mat ι) : Mat (ι × κ) := kron A 1

def bobLift (B : Mat κ) : Mat (ι × κ) := kron 1 B

@[simp] theorem lift_product (A : Mat ι) (B : Mat κ) :
    aliceLift (κ := κ) A * bobLift (ι := ι) B = kron A B := by
  simp [aliceLift,bobLift]

@[simp] theorem lift_commute (A : Mat ι) (B : Mat κ) :
    aliceLift (κ := κ) A * bobLift (ι := ι) B =
      bobLift (ι := ι) B * aliceLift (κ := κ) A := by
  simp [aliceLift,bobLift]

/-- Functional calculus for a finite PVM by direct multiplication, with zero
outcomes allowed and no assumption of rank one or a full observable spectrum. -/
theorem measurement_spectral_mul (M : Measurement d ι) (f g : Ix d → ℂ) :
    (∑ a, f a • M.effect a) * (∑ b, g b • M.effect b) =
      ∑ a, (f a*g a) • M.effect a := by
  rw [Finset.sum_mul]
  simp_rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro a _
  rw [Finset.sum_eq_single a]
  · simp [smul_mul_assoc, mul_smul_comm, M.idempotent, smul_smul, mul_comm]
  · intro b _ hba
    simp [smul_mul_assoc, mul_smul_comm, M.orthogonal a b (Ne.symm hba)]
  · simp

theorem measurement_spectral_star (M : Measurement d ι) (f : Ix d → ℂ) :
    (∑ a, f a • M.effect a).conjTranspose = ∑ a, star (f a) • M.effect a := by
  simp only [Matrix.conjTranspose_sum, Matrix.conjTranspose_smul]
  congr 1
  funext a
  rw [(M.positive a).isHermitian.eq]

theorem encoded_unitary (M : Measurement d ι) : UnitaryRel (encoded M) := by
  constructor
  · unfold encoded
    rw [measurement_spectral_star, measurement_spectral_mul]
    simpa only [chi_star_mul, one_smul] using M.complete
  · unfold encoded
    rw [measurement_spectral_star, measurement_spectral_mul]
    have h (a : Ix d) : chi a * star (chi a) = 1 := by simpa [mul_comm] using chi_star_mul a
    simpa only [h, one_smul] using M.complete

theorem encoded_pow (M : Measurement d ι) (r : ℕ) :
    encoded M ^ r = ∑ a, chi ((r : Ix d)*a) • M.effect a := by
  induction r with
  | zero => simpa only [pow_zero, Nat.cast_zero, zero_mul, chi_zero, one_smul] using M.complete.symm
  | succ r ih =>
    rw [pow_succ, ih, encoded, measurement_spectral_mul]
    congr 1
    funext a
    simp [Nat.cast_add, add_mul, chi_add]

/-- Measurement outcomes entail order d; d is not constrained to be prime. -/
theorem encoded_order (M : Measurement d ι) : encoded M ^ d = 1 := by
  rw [encoded_pow]
  simpa only [ZMod.natCast_self, zero_mul, chi_zero, one_smul] using M.complete

def operatorPowers (T : Mat ι) (k : Ix d) : Mat ι := T ^ k.val

/-- Actual outcome projectors are recovered by inverse Fourier encoding. -/
theorem measurement_reconstruction (M : Measurement d ι) (a : Ix d) :
    M.effect a = (d : ℂ)⁻¹ •
      ∑ k, chi (-(a*k)) • operatorPowers (encoded M) k := by
  have hp (k : Ix d) : operatorPowers (encoded M) k =
      moduleFourier M.effect k := by
    simp only [operatorPowers, encoded_pow, ZMod.natCast_zmod_val, moduleFourier]
  simp_rw [hp]
  simpa [mul_comm] using moduleFourier_inversion M.effect a

theorem bornProbability_nonnegative (ρ : StateOn (ι × κ)) (M : Measurement d ι)
    (N : Measurement d κ) (a b : Ix d) :
    0 ≤ bornProbability ρ.density (M.effect a) (N.effect b) := by
  have h := stateEval_square_nonnegative ρ.positive (kron (M.effect a) (N.effect b))
  rw [kron_star, (M.positive a).isHermitian.eq, (N.positive b).isHermitian.eq,
    kron_mul, M.idempotent, N.idempotent] at h
  exact h

theorem bornProbability_left_marginal (ρ : StateOn (ι × κ)) (M : Measurement d ι)
    (N : Measurement d κ) (a : Ix d) :
    (∑ b, bornProbability ρ.density (M.effect a) (N.effect b)) =
      stateEval ρ.density (kron (M.effect a) 1) := by
  unfold bornProbability
  rw [← stateEval_sum, ← kron_sum_right, N.complete]

theorem bornProbability_right_marginal (ρ : StateOn (ι × κ)) (M : Measurement d ι)
    (N : Measurement d κ) (b : Ix d) :
    (∑ a, bornProbability ρ.density (M.effect a) (N.effect b)) =
      stateEval ρ.density (kron 1 (N.effect b)) := by
  unfold bornProbability
  rw [← stateEval_sum, ← kron_sum_left, M.complete]

theorem bornProbability_normalized (ρ : StateOn (ι × κ)) (M : Measurement d ι)
    (N : Measurement d κ) : (∑ a, ∑ b, bornProbability ρ.density (M.effect a) (N.effect b)) = 1 := by
  simp only [bornProbability_left_marginal]
  rw [← stateEval_sum, ← kron_sum_left, M.complete, kron_one, stateEval_one ρ.normalized]

def stateOnOfPure (ψ : ι → ℂ) (hψ : ip ψ ψ = 1) : StateOn ι where
  density := projector ψ
  positive := projector_positive ψ
  normalized := by simpa [Matrix.trace, projector, ip, mul_comm] using hψ

def measurementOfBasis (w : Ix d → ι → ℂ)
    (ho : ∀ a b, ip (w a) (w b) = if a=b then 1 else 0)
    (hc : ∑ a, projector (w a) = 1) : Measurement d ι where
  effect := fun a => projector (w a)
  positive := fun a => projector_positive (w a)
  complete := hc
  idempotent := by
    intro a
    rw [projector_mul]
    ext i j
    simp [ho, projector]
  orthogonal := by
    intro a b hab
    rw [projector_mul]
    ext i j
    simp [ho, hab]

theorem kron_projector (u : ι → ℂ) (v : κ → ℂ) :
    kron (projector u) (projector v) = projector (vectorTensor u v) := by
  ext i j
  simp [kron, projector, vectorTensor]
  ring

theorem physical_rank_one_born (ψ : ι × κ → ℂ) (u : ι → ℂ) (v : κ → ℂ) :
    bornProbability (projector ψ) (projector u) (projector v) =
      Complex.normSq (ip (vectorTensor u v) ψ) := by
  unfold bornProbability stateEval
  rw [kron_projector, ← expectation_eq_trace, expectation_projector]
  exact (congrArg Complex.re
    (Complex.normSq_eq_conj_mul_self (z := ip (vectorTensor u v) ψ))).symm

/-- Honest behavior-to-correlator bridge: probabilities determine the same
encoded operator expectation, including the PLUS exponent convention. -/
theorem correlator_from_born (ρ : StateOn (ι × κ)) (M : Measurement d ι)
    (N : Measurement d κ) :
    Matrix.trace (ρ.density * kron (encoded M) (encoded N)) =
      ∑ a, ∑ b, chi (a+b) * Matrix.trace (ρ.density * kron (M.effect a) (N.effect b)) := by
  simp only [encoded,kron_sum_left,kron_sum_right,kron_smul_left,kron_smul_right,
    smul_smul,Finset.mul_sum,Matrix.trace_sum,mul_smul_comm,Matrix.trace_smul,
    smul_eq_mul,chi_add]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro a _
  apply Finset.sum_congr rfl
  intro b _
  ring


/-- Reality of a physical expectation is proved, not silently assumed when
passing from complex correlators to real Born probabilities. -/
theorem trace_hermitian_product_real (R X : Mat ι)
    (hR : R.IsHermitian) (hX : X.IsHermitian) :
    Matrix.trace (R*X)=((Matrix.trace (R*X)).re : ℂ) := by
  have hc : star (Matrix.trace (R*X))=Matrix.trace (R*X) := by
    rw [← Matrix.trace_conjTranspose,Matrix.conjTranspose_mul,hR.eq,hX.eq,Matrix.trace_mul_comm]
  apply Complex.ext
  · simp
  · have h := congrArg Complex.im hc
    change -(Matrix.trace (R*X)).im = (Matrix.trace (R*X)).im at h
    simp only [Complex.ofReal_im]
    linarith

theorem bornProbability_complex_trace (ρ : StateOn (ι×κ)) (M : Measurement d ι)
    (N : Measurement d κ) (a b : Ix d) :
    Matrix.trace (ρ.density*kron (M.effect a) (N.effect b))=
      (bornProbability ρ.density (M.effect a) (N.effect b) : ℂ) := by
  apply trace_hermitian_product_real _ _ ρ.positive.isHermitian
  simp [Matrix.IsHermitian,kron_star,(M.positive a).isHermitian.eq,(N.positive b).isHermitian.eq]

/-- The first harmonic is a linear functional of the ACTUAL REAL probabilities. -/
theorem correlator_from_probabilities (ρ : StateOn (ι×κ)) (M : Measurement d ι)
    (N : Measurement d κ) :
    Matrix.trace (ρ.density*kron (encoded M) (encoded N))=
      ∑ a,∑ b,chi (a+b)*(bornProbability ρ.density (M.effect a) (N.effect b) : ℂ) := by
  rw [correlator_from_born]
  simp_rw [bornProbability_complex_trace]

end CyclicBell.General
