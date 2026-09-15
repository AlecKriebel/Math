import CyclicBell.Witness
import CyclicBell.TraceCalculus

/-!
Exact attainment of BOTH actual manuscript functionals. Universal optimality
is not inferred here from the witness alone; Endpoints imports PhysicalBounds
separately. The coefficient formula is sourceLambda, not a fitted replacement.
UNCOMPILED SOURCE CANDIDATE.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.D4
attribute [local simp] Matrix.cons_val_two Matrix.cons_val_three Matrix.cons_val_four
set_option maxRecDepth 25000
set_option maxHeartbeats 20000000

/-- The sixteen scalar Fourier identities underlying eq:Fourier-compression.
Only real algebra after the proved ζ power table is used. -/
theorem witness_fourier_weights (l j : Fin 4) :
    (∑ y : Fin 4, Complex.I ^ (l.val * y.val) * bobWeights y j) =
      (4 * lambda l) * star (aliceWeights l j) := by
  fin_cases l <;> fin_cases j <;>
    norm_num [bobWeights, aliceWeights, bobExponents, aliceExponents, lambda,
      Fin.sum_univ_succ, zeta_cube] <;>
    simp only [zeta_components] <;>
    apply Complex.ext <;>
    norm_num [Complex.mul_re, Complex.mul_im, h_eq_k, Complex.I_pow_eq_pow_mod] <;>
    norm_num <;>
    nlinarith [k_alpha, k_beta, show 2 * alpha = c + s by unfold alpha; ring,
      show 2 * beta = s - c by unfold beta; ring]

/-- Exact Fourier compression with the source's phase and complex conjugation. -/
theorem witness_fourier_compression (l : Fin 4) :
    fourier4 witnessB l = (4 * lambda l) • entryConj (witnessA l) := by
  apply Matrix.ext
  intro i j
  simp only [fourier4, witnessB, witnessA, weighted_conjugate, weighted_entry,
    Matrix.sum_apply, Matrix.smul_apply, smul_eq_mul]
  calc
    (∑ y : Fin 4, Complex.I ^ (l.val * y.val) * (shift i j * bobWeights y j)) =
        shift i j * (∑ y : Fin 4, Complex.I ^ (l.val * y.val) * bobWeights y j) := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro y _
          ring
    _ = _ := by rw [witness_fourier_weights]; ring

theorem witness_source_fourier_compression (l : Fin 4) :
    fourier4 witnessB l = (4 * sourceLambda l) • entryConj (witnessA l) := by
  rw [sourceLambda_eq, witness_fourier_compression]

/-- Literal eq:Fourier-compression, with the manuscript's D_l. -/
theorem witness_source_D_compression (l : Fin 4) :
    fourier4 witnessB l = (4 * sourceLambda l) • sourceD l := by
  rw [witness_source_fourier_compression, secondAlice_manuscript_bridge, entryConj_involutive]

/-- Complex expectation, before a real part is taken. -/
theorem witness_compressed_correlator (l : Fin 4) :
    expectation phi (tensor (witnessA l) (fourier4 witnessB l)) = 4 * lambda l := by
  rw [witness_fourier_compression, tensor_smul_right, expectation_smul,
    phi_unitary_pair _ (witnessA_unitary l), mul_one]

theorem witness_source_compressed_correlator (l : Fin 4) :
    expectation phi (tensor (witnessA l) (fourier4 witnessB l)) = 4 * sourceLambda l := by
  rw [sourceLambda_eq, witness_compressed_correlator]

/-- Collect exactly the y=0 and y=1 Fourier modes of the actual first operator. -/
theorem first_witness_operator_collection :
    (∑ y : Fin 4, tensor (witnessA 0 + Complex.I ^ y.val • witnessA 1) (witnessB y)) =
      tensor (witnessA 0) (fourier4 witnessB 0) +
      tensor (witnessA 1) (fourier4 witnessB 1) := by
  simp [fourier4, tensor_add_left, tensor_smul_left, tensor_sum_right,
    tensor_smul_right, Finset.sum_add_distrib]

/-- Pure density bridge is applied to the actual first functional, without
replacing its definition by a precomputed scalar. -/
theorem first_reduced_attainment_complex :
    (∑ y : Fin 4,
      Matrix.trace (firstStrategy.state.density *
        tensor (observable (firstStrategy.alice 0) +
          Complex.I ^ y.val • observable (firstStrategy.alice 1))
          (observable (firstStrategy.bob (reducedBob y))))) = 8 * (alpha : ℂ) := by
  simp only [firstAlice_zero_encoding, firstAlice_one_encoding, firstBob_encoding]
  change (∑ y : Fin 4, Matrix.trace (projector phi *
    tensor (witnessA 0 + Complex.I ^ y.val • witnessA 1) (witnessB y))) = _
  simp only [trace_pure_tensor]
  rw [← expectation_sum, first_witness_operator_collection, expectation_add,
    witness_compressed_correlator, witness_compressed_correlator]
  norm_num [lambda] <;> ring

theorem first_reduced_attainment : firstReducedValue firstStrategy = 8 * alpha := by
  have hc := congrArg Complex.re first_reduced_attainment_complex
  simpa [firstReducedValue] using hc

theorem aligned_witness_expectation : expectation phi (tensor shift shift) = 1 := by
  simpa only [shift_conjugate] using phi_unitary_pair shift shift_unitary

theorem first_aligned_attainment :
    (Matrix.trace (firstStrategy.state.density * tensor
      (observable (firstStrategy.alice 0)) (observable (firstStrategy.bob 4)))).re = 1 := by
  rw [firstAlice_zero_encoding, witnessA_zero, firstBob_added_encoding]
  change (Matrix.trace (projector phi * tensor shift shift)).re = 1
  rw [trace_pure_tensor, aligned_witness_expectation]
  norm_num

/-- Target C, with exactly the manuscript's trigonometric normalization. -/
theorem first_attainment : firstAugmentedValue firstStrategy = firstTargetValue := by
  rw [firstAugmentedValue, first_reduced_attainment, first_aligned_attainment]
  unfold firstTargetValue
  have hc := first_constant_bridge
  have ha := alpha_in_s
  nlinarith [hc, ha]

theorem second_bob_fourier (l : Fin 4) : bobFourier secondStrategy l = fourier4 witnessB l := by
  simp only [bobFourier, fourier4, secondBob_encoding]

theorem second_reduced_attainment_complex :
    (∑ l : Fin 4, Matrix.trace (secondStrategy.state.density *
      (star (sourceLambda l) • tensor (observable (secondStrategy.alice l))
        (bobFourier secondStrategy l)))) = 4 := by
  simp only [secondAlice_encoding, second_bob_fourier]
  change (∑ l : Fin 4, Matrix.trace (projector phi *
    (star (sourceLambda l) • tensor (witnessA l) (fourier4 witnessB l)))) = 4
  simp only [← expectation_eq_trace, expectation_smul, witness_source_compressed_correlator]
  calc
    (∑ l : Fin 4, star (sourceLambda l) * (4 * sourceLambda l)) =
        4 * (∑ l : Fin 4, star (lambda l) * lambda l) := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro l _
          rw [sourceLambda_eq]
          ring
    _ = 4 := by rw [lambda_normalization]; ring

theorem second_reduced_attainment : secondReducedValue secondStrategy = 4 := by
  have hc := congrArg Complex.re second_reduced_attainment_complex
  simpa [secondReducedValue] using hc

theorem second_aligned_attainment :
    (Matrix.trace (secondStrategy.state.density * tensor
      (observable (secondStrategy.alice 0)) (observable (secondStrategy.bob 4)))).re = 1 := by
  rw [secondAlice_encoding, witnessA_zero, secondBob_added_encoding]
  change (Matrix.trace (projector phi * tensor shift shift)).re = 1
  rw [trace_pure_tensor, aligned_witness_expectation]
  norm_num

/-- Full second-family scalar attainment, independent of its universal bound. -/
theorem second_attainment : secondAugmentedValue secondStrategy = 5 := by
  rw [secondAugmentedValue, second_reduced_attainment, second_aligned_attainment]
  norm_num

/-! Explicit second-family residual annihilation, in addition to scalar evaluation. -/

theorem phi_unitary_invariance (A : Op 4) (hA : UnitaryRel A) :
    applyOp (tensor A (entryConj A)) phi = phi := by
  funext i
  have hu := congrFun (congrFun hA.2 i.1) i.2
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply] at hu
  change (∑ j : Joint 4 4, A i.1 j.1 * star (A i.2 j.2) * phi j) = phi i
  simp only [phi, Fintype.sum_prod_type]
  simp only [mul_ite, mul_zero, Finset.sum_ite_eq', Finset.sum_ite_eq, Finset.mem_univ, if_true]
  rw [← Finset.sum_mul, hu]
  by_cases hi : i.1 = i.2 <;> simp [Matrix.one_apply, hi]

theorem second_witness_residual_zero (l : Fin 4) :
    applyOp ((4 * sourceLambda l) • (1 : JointOp 4 4) -
      tensor (observable (secondStrategy.alice l)) (bobFourier secondStrategy l)) phi = 0 := by
  rw [secondAlice_encoding, second_bob_fourier, witness_source_fourier_compression,
    tensor_smul_right]
  have hinv := phi_unitary_invariance (witnessA l) (witnessA_unitary l)
  funext i
  have hv := congrFun hinv i
  simp only [applyOp] at hv
  simp only [applyOp, Matrix.sub_apply, Matrix.smul_apply, smul_eq_mul,
    sub_mul, Finset.sum_sub_distrib, mul_assoc, ← Finset.mul_sum]
  simp only [Matrix.one_apply, ite_mul, zero_mul, Finset.sum_ite_eq', Finset.mem_univ,
    Finset.sum_ite_eq, if_true, one_mul, hv, sub_self, Pi.zero_apply]

end CyclicBell.D4
