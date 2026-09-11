import Bell.ProductLocality
import Bell.QuantumCompactness

/-!
# Every mixed two-qubit strategy has a qubit assemblage representation

The Gram rows of the density matrix define the steered operators. Full-rank
reduced states are purified on a second qubit without changing any complete
behavior table; singular reduced states are treated by product locality.
This removes the need for an extreme-eigenvector selection argument.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder
namespace Bell

def rowAmplitude (B : JointOperator) (k : Joint) : Operator :=
  fun i j => star (B k (i,j))

theorem gram_rows_density (B : JointOperator) :
    B.conjTranspose * B = ∑ k : Joint, pureDensity (rowAmplitude B k) := by
  ext i j
  simp [Matrix.mul_apply, Matrix.sum_apply, Matrix.conjTranspose_apply, rowAmplitude, pureDensity]

def State.amplitude (ρ : State) (k : Joint) : Operator :=
  rowAmplitude ρ.positive.sqrt k

theorem State.amplitudes_density (ρ : State) :
    ρ.density = ∑ k : Joint, pureDensity (ρ.amplitude k) := by
  change ρ.density = ∑ k, pureDensity (rowAmplitude ρ.positive.sqrt k)
  rw [← gram_rows_density]
  change ρ.density = ρ.positive.sqrt.conjTranspose * ρ.positive.sqrt
  rw [ρ.positive.posSemidef_sqrt.isHermitian.eq, ρ.positive.sqrt_mul_self]

def State.steer (ρ : State) (N : Operator) : Operator :=
  ∑ k : Joint, ρ.amplitude k * N.transpose * (ρ.amplitude k).conjTranspose

def State.reduced (ρ : State) : Operator := ρ.steer 1

theorem State.steer_positive (ρ : State) {N : Operator} (hN : N.PosSemidef) :
    (ρ.steer N).PosSemidef :=
  positive_sum _ fun k => hN.transpose.mul_mul_conjTranspose_same (ρ.amplitude k)

theorem State.steer_sum (ρ : State) {ι : Type*} [Fintype ι] (N : ι → Operator) :
    ρ.steer (∑ i, N i) = ∑ i, ρ.steer (N i) := by
  simp only [State.steer, Matrix.transpose_sum, Matrix.mul_sum, Matrix.sum_mul]
  exact Finset.sum_comm

theorem State.reduced_positive (ρ : State) : ρ.reduced.PosSemidef :=
  ρ.steer_positive Matrix.PosSemidef.one

theorem State.reduced_normalized (ρ : State) : Matrix.trace ρ.reduced = 1 := by
  change Matrix.trace (∑ k, ρ.amplitude k * (1 : Operator).transpose *
    (ρ.amplitude k).conjTranspose) = 1
  simp only [Matrix.transpose_one, mul_one, Matrix.trace_sum]
  rw [← ρ.normalized, ρ.amplitudes_density, Matrix.trace_sum]
  apply Finset.sum_congr rfl
  intro k _
  exact (pureDensity_trace _).symm

theorem State.born_steer (ρ : State) (M N : Operator) :
    born ρ.density M N = localTrace M (ρ.steer N) := by
  rw [ρ.amplitudes_density]
  unfold born
  rw [Matrix.sum_mul, Matrix.trace_sum]
  simp only [Complex.re_sum]
  change (∑ k, born (pureDensity (ρ.amplitude k)) M N) = _
  simp_rw [pureDensity_born]
  exact (map_sum (localTrace M) _ _).symm

def Strategy.toAssemblage {A : Architecture} (s : Strategy A) : Assemblage A where
  alice := s.alice
  reduced := s.state.reduced
  reducedPositive := s.state.reduced_positive
  reducedNormalized := s.state.reduced_normalized
  steered := fun y b => s.state.steer ((s.bob y).effect b)
  positive := fun y b => s.state.steer_positive ((s.bob y).positive b)
  commonSum := by
    intro y
    rw [← State.steer_sum, (s.bob y).normalized]
    rfl

theorem Strategy.toAssemblage_behavior {A : Architecture} (s : Strategy A) :
    s.toAssemblage.behavior = s.behavior := by
  funext x y a b
  exact (s.state.born_steer _ _).symm

/-- A pure strategy with a full Schmidt-rank coefficient matrix. -/
structure FullPureStrategy (A : Architecture) where
  coefficient : Operator
  coefficient_invertible : IsUnit coefficient.det
  normalized : Matrix.trace (coefficient * coefficient.conjTranspose) = 1
  alice : (x : Fin A.aliceInputs) → POVM (A.aliceOutputs x)
  bob : (y : Fin A.bobInputs) → POVM (A.bobOutputs y)

def FullPureStrategy.toStrategy {A : Architecture} (s : FullPureStrategy A) : Strategy A where
  state := pureState s.coefficient s.normalized
  alice := s.alice
  bob := s.bob

abbrev FullPureStrategy.behavior {A : Architecture} (s : FullPureStrategy A) : Behavior A :=
  s.toStrategy.behavior

/-- Every behavior outside the PVM hull has a full-Schmidt-rank pure two-qubit
realization. The claim holds without assuming extremality. -/
theorem full_pure_of_not_mem_convexPVM {A : Architecture} (s : Strategy A)
    (hnot : s.behavior ∉ convexPVM A) :
    ∃ t : FullPureStrategy A, t.behavior = s.behavior := by
  let a := s.toAssemblage
  have hd : a.reduced.det ≠ 0 := by
    intro hz
    have hloc := a.singular_mem_convexPVM hz
    rw [show a.behavior = s.behavior from s.toAssemblage_behavior] at hloc
    exact hnot hloc
  let hunit : IsUnit a.reduced.det := isUnit_iff_ne_zero.mpr hd
  refine ⟨⟨a.root, a.root_invertible hunit, ?_, a.alice, a.purifiedBob hunit⟩, ?_⟩
  · rw [a.root_hermitian, a.root_square, a.reducedNormalized]
  · change (a.purifiedStrategy hunit).behavior = s.behavior
    rw [a.purified_behavior, s.toAssemblage_behavior]

/-- Nonzero local effects have strictly positive marginals at full Schmidt rank. -/
theorem full_pure_marginal_positive {A : Architecture} (s : FullPureStrategy A)
    (x : Fin A.aliceInputs) (a : Fin (A.aliceOutputs x))
    (hne : (s.alice x).effect a ≠ 0) :
    0 < localTrace ((s.alice x).effect a)
      (s.coefficient * s.coefficient.conjTranspose) := by
  let C := s.coefficient
  let M := (s.alice x).effect a
  have hp : (C.conjTranspose * M * C).PosSemidef :=
    ((s.alice x).positive a).conjTranspose_mul_mul_same C
  have hne' : C.conjTranspose*M*C ≠ 0 := by
    intro hz
    apply hne
    have hc : IsUnit C.det := s.coefficient_invertible
    have hct : IsUnit C.conjTranspose.det := by
      rw [Matrix.det_conjTranspose]
      exact hc.map (starRingEnd ℂ)
    have he := congrArg (fun Q : Operator => C.conjTranspose⁻¹ * Q * C⁻¹) hz
    have hcancel : C.conjTranspose⁻¹ * (C.conjTranspose * M * C) * C⁻¹ = M := by
      calc
        _ = (C.conjTranspose⁻¹ * C.conjTranspose) * M * (C * C⁻¹) := by
          noncomm_ring
        _ = M := by
          rw [Matrix.nonsing_inv_mul _ hct, Matrix.mul_nonsing_inv _ hc, one_mul, mul_one]
    simpa only [hcancel, mul_zero, zero_mul] using he
  have ht := positive_trace_positive hp hne'
  change 0 < (Matrix.trace (M*(C*C.conjTranspose))).re
  rw [Matrix.mul_assoc, Matrix.trace_mul_comm C.conjTranspose (M * C), Matrix.mul_assoc] at ht
  exact ht

end Bell
