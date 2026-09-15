import CyclicBell.GeneralCommutingModel
import CyclicBell.GeneralSupportAlgebra
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
Explicit physical finite-to-commuting bridge. A positive trace-one density is
purified by vectorizing its actual positive square root, with a separate identity
environment. Coordinate matrices act on Euclidean Hilbert space, not on the
supremum-norm function space. No embedding or Born identity is an axiom/field.
UNCOMPILED SOURCE CANDIDATES; pinned-library elaboration remains untested.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder InnerProductSpace
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {ι κ ν : Type*} [Fintype ι] [Fintype κ] [Fintype ν]
variable [DecidableEq ι] [DecidableEq κ] [DecidableEq ν]

def euclidVector (v : ι → ℂ) : EuclideanSpace ℂ ι := (WithLp.equiv 2 (ι → ℂ)).symm v

def matrixCLM (M : Mat ι) : EuclideanSpace ℂ ι →L[ℂ] EuclideanSpace ℂ ι :=
  LinearMap.toContinuousLinearMap (Matrix.toEuclideanLin M)

theorem euclidVector_surjective : Function.Surjective (euclidVector (ι := ι)) :=
  (WithLp.equiv 2 (ι → ℂ)).symm.surjective

theorem euclidVector_inner (u v : ι → ℂ) :
    inner ℂ (euclidVector u) (euclidVector v) = ip u v := by
  simp [euclidVector,EuclideanSpace.inner_piLp_equiv_symm,ip,dotProduct,mul_comm]

/-- This is the standard matrix-vector action, including the basis order. -/
theorem matrixCLM_on_vector (M : Mat ι) (v : ι → ℂ) :
    matrixCLM M (euclidVector v) = euclidVector (M *ᵥ v) := by
  exact Matrix.toEuclideanLin_apply_piLp_equiv_symm M v

theorem matrixCLM_mul (M N : Mat ι) : matrixCLM (M*N) = matrixCLM M * matrixCLM N := by
  apply ContinuousLinearMap.ext
  intro v
  obtain ⟨x,rfl⟩ := euclidVector_surjective v
  change matrixCLM (M*N) (euclidVector x) = matrixCLM M (matrixCLM N (euclidVector x))
  simp only [matrixCLM_on_vector,Matrix.mulVec_mulVec]

theorem matrixCLM_add (M N : Mat ι) : matrixCLM (M+N) = matrixCLM M + matrixCLM N := by
  simp only [matrixCLM,map_add]

theorem matrixCLM_smul (z : ℂ) (M : Mat ι) : matrixCLM (z • M) = z • matrixCLM M := by
  simp only [matrixCLM,map_smul]

theorem matrixCLM_one : matrixCLM (1 : Mat ι) = 1 := by
  apply ContinuousLinearMap.ext
  intro v
  obtain ⟨x,rfl⟩ := euclidVector_surjective v
  change matrixCLM (1 : Mat ι) (euclidVector x) = euclidVector x
  rw [matrixCLM_on_vector,Matrix.one_mulVec]

theorem matrixCLM_zero : matrixCLM (0 : Mat ι) = 0 := by
  simp only [matrixCLM,map_zero]

theorem matrixCLM_sum {J : Type*} [Fintype J] (M : J → Mat ι) :
    matrixCLM (∑ j,M j) = ∑ j,matrixCLM (M j) := by
  simp only [matrixCLM,map_sum]

/-- The adjoint is conjugate transpose, not entrywise conjugation/transpose. -/
theorem matrixCLM_star (M : Mat ι) : matrixCLM M.conjTranspose = star (matrixCLM M) := by
  apply ContinuousLinearMap.ext
  intro x
  apply ext_inner_right ℂ
  intro y
  change inner ℂ (Matrix.toEuclideanLin M.conjTranspose x) y =
    inner ℂ ((matrixCLM M).adjoint x) y
  rw [Matrix.toEuclideanLin_conjTranspose_eq_adjoint,
    LinearMap.adjoint_inner_left,ContinuousLinearMap.adjoint_inner_left]
  rfl

def vectorize (L : Matrix ι ν ℂ) : ι × ν → ℂ := fun i => L i.1 i.2

theorem vectorize_ip_trace (L M : Matrix ι ν ℂ) :
    ip (vectorize L) (vectorize M) = Matrix.trace (L.conjTranspose*M) := by
  simp only [vectorize,ip,Fintype.sum_prod_type,Matrix.trace,Matrix.diag_apply,
    Matrix.mul_apply,Matrix.conjTranspose_apply]
  exact Finset.sum_comm

theorem kron_one_vectorize (T : Mat ι) (L : Matrix ι ν ℂ) :
    kron T (1 : Mat ν) *ᵥ vectorize L = vectorize (T*L) := by
  funext v
  rcases v with ⟨i,e⟩
  simp [kron,vectorize,Matrix.mulVec,dotProduct,Matrix.mul_apply,Fintype.sum_prod_type]

theorem vectorize_moment (L : Matrix ι ν ℂ) (T : Mat ι) :
    hilbertMoment (euclidVector (vectorize L)) (matrixCLM (kron T (1 : Mat ν))) =
      Matrix.trace ((L*L.conjTranspose)*T) := by
  unfold hilbertMoment
  rw [matrixCLM_on_vector,euclidVector_inner,kron_one_vectorize,vectorize_ip_trace]
  calc
    Matrix.trace (L.conjTranspose*(T*L)) = Matrix.trace ((T*L)*L.conjTranspose) :=
      Matrix.trace_mul_comm _ _
    _ = Matrix.trace ((L*L.conjTranspose)*T) := by
      rw [mul_assoc,Matrix.trace_mul_comm]

/-- Arbitrary mixed state: no rank, faithfulness or spectral-shape assumption. -/
def purificationVector (ρ : StateOn ι) : EuclideanSpace ℂ (ι × ι) :=
  euclidVector (vectorize (stateFactor ρ))

theorem purificationVector_inner (ρ : StateOn ι) :
    inner ℂ (purificationVector ρ) (purificationVector ρ) = 1 := by
  unfold purificationVector
  rw [euclidVector_inner,vectorize_ip_trace,Matrix.trace_mul_comm,
    stateFactor_gram,ρ.normalized]

theorem purificationVector_normalized (ρ : StateOn ι) : ‖purificationVector ρ‖ = 1 := by
  have h := congrArg Complex.re (purificationVector_inner ρ)
  simp only [inner_self_eq_norm_sq_to_K] at h
  norm_num at h
  nlinarith [norm_nonneg (purificationVector ρ)]

theorem purification_moment (ρ : StateOn ι) (T : Mat ι) :
    hilbertMoment (purificationVector ρ) (matrixCLM (kron T (1 : Mat ι))) =
      Matrix.trace (ρ.density*T) := by
  rw [purificationVector,vectorize_moment,stateFactor_gram]

theorem purification_stateEval (ρ : StateOn ι) (T : Mat ι) :
    vectorEval (purificationVector ρ) (matrixCLM (kron T (1 : Mat ι))) = stateEval ρ.density T := by
  exact congrArg Complex.re (purification_moment ρ T)

/-- Hermitian idempotence proves positivity for tensor-extended effects. -/
theorem hermitian_idempotent_positive (T : Mat ι) (hT : T.IsHermitian) (hI : T*T=T) :
    T.PosSemidef := by
  have h := Matrix.posSemidef_conjTranspose_mul_self T
  rwa [hT.eq,hI] at h

def leftMeasurement (M : Measurement d ι) : Measurement d (ι × κ) where
  effect := fun a => kron (M.effect a) 1
  positive := by
    intro a
    apply hermitian_idempotent_positive
    · simp [Matrix.IsHermitian,kron_star,(M.positive a).isHermitian.eq]
    · simp [kron_mul,M.idempotent]
  complete := by rw [← kron_sum_left,M.complete,kron_one]
  idempotent := by intro a; simp [kron_mul,M.idempotent]
  orthogonal := by
    intro a b hab
    rw [kron_mul,M.orthogonal a b hab]
    ext i j
    simp [kron]

def rightMeasurement (M : Measurement d κ) : Measurement d (ι × κ) where
  effect := fun a => kron 1 (M.effect a)
  positive := by
    intro a
    apply hermitian_idempotent_positive
    · simp [Matrix.IsHermitian,kron_star,(M.positive a).isHermitian.eq]
    · simp [kron_mul,M.idempotent]
  complete := by rw [← kron_sum_right,M.complete,kron_one]
  idempotent := by intro a; simp [kron_mul,M.idempotent]
  orthogonal := by
    intro a b hab
    rw [kron_mul,M.orthogonal a b hab]
    ext i j
    simp [kron]

def coordinateMeasurement (M : Measurement d ι) :
    AlgebraPVM d (EuclideanSpace ℂ ι →L[ℂ] EuclideanSpace ℂ ι) where
  effect := fun a => matrixCLM (M.effect a)
  selfadjoint := by intro a; rw [← matrixCLM_star,(M.positive a).isHermitian.eq]
  idempotent := by intro a; rw [← matrixCLM_mul,M.idempotent]
  orthogonal := by intro a b hab; rw [← matrixCLM_mul,M.orthogonal a b hab,matrixCLM_zero]
  complete := by rw [← matrixCLM_sum,M.complete,matrixCLM_one]

/-- Complete explicit tensor-to-commuting strategy. The last coordinate is the
environment; neither party measures it. Cross-party effects commute by tensor
placement, rather than by an additional assumption on the input strategy. -/
def finiteToCommuting {α β : Type*} (s : StrategyOn d α β ι κ) :
    CommutingOn d α β (EuclideanSpace ℂ ((ι×κ)×(ι×κ))) where
  vector := purificationVector s.state
  normalized := purificationVector_normalized s.state
  alice := fun x => coordinateMeasurement
    (leftMeasurement (κ := ι×κ) (leftMeasurement (κ := κ) (s.alice x)))
  bob := fun y => coordinateMeasurement
    (leftMeasurement (κ := ι×κ) (rightMeasurement (ι := ι) (s.bob y)))
  cross := by
    intro x y a b
    change matrixCLM (kron (kron ((s.alice x).effect a) 1) 1) *
        matrixCLM (kron (kron 1 ((s.bob y).effect b)) 1) = _
    simp only [← matrixCLM_mul,kron_mul,one_mul,mul_one]

/-- Equality of the entire real behavior, not merely the chosen Bell value. -/
theorem finiteToCommuting_behavior {α β : Type*} (s : StrategyOn d α β ι κ) :
    commutingBehavior (finiteToCommuting s) = behavior s := by
  funext x y a b
  change vectorEval (purificationVector s.state)
    (matrixCLM (kron (kron ((s.alice x).effect a) (1 : Mat κ)) (1 : Mat (ι×κ))) *
     matrixCLM (kron (kron (1 : Mat ι) ((s.bob y).effect b)) (1 : Mat (ι×κ)))) = _
  simp only [← matrixCLM_mul,kron_mul,one_mul,mul_one]
  exact purification_stateEval s.state _

end CyclicBell.General
