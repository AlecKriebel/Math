import CyclicBell.GeneralCoverageSourceOrder
import CyclicBell.GeneralCoverageSourceCanonical
import CyclicBell.GeneralCoverageSpectralMeasurement
import CyclicBell.GeneralFirstBound

/-! A physical strategy made from the literal source coefficient matrices,
with exact first-family attainment and the prescribed extra Bob observable. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def sourceBobMeasurement (hd : 2≤d) (y : Ix d) : Measurement d (Ix d) :=
  finiteOrderMeasurement (sourceBob y) (sourceBob_unitary hd y) (sourceBob_order hd y)

theorem sourceBobMeasurement_encoding (hd : 2≤d) (y : Ix d) :
    encoded (sourceBobMeasurement hd y)=sourceBob y := finiteOrderMeasurement_encoding _ _ _

theorem source_clock_adjoint_order : ((sourceClock d)ᴴ)^d=1 := by
  rw [←Matrix.conjTranspose_pow,source_clock_order,Matrix.conjTranspose_one]

def sourceAliceMeasurement (x : Fin 2) : Measurement d (Ix d) :=
  if x=0 then finiteOrderMeasurement (sourceClock d) source_clock_unitary source_clock_order
  else finiteOrderMeasurement (cyclicShift d) source_shift_unitary source_shift_order

def sourceAugmentedBob (hd : 2≤d) : AugmentedInputs d → Measurement d (Ix d)
  | none => finiteOrderMeasurement ((sourceClock d)ᴴ) source_clock_unitary.adjoint source_clock_adjoint_order
  | some y => sourceBobMeasurement hd y

def sourcePhysicalStrategy (hd : 2≤d) : StrategyOn d (Fin 2) (AugmentedInputs d) (Ix d) (Ix d) where
  state := entangledState d
  alice := sourceAliceMeasurement
  bob := sourceAugmentedBob hd

theorem sourcePhysicalStrategy_encodings (hd : 2≤d) :
    encoded ((sourcePhysicalStrategy hd).alice 0)=sourceClock d ∧
    encoded ((sourcePhysicalStrategy hd).alice 1)=cyclicShift d ∧
    encoded ((sourcePhysicalStrategy hd).bob none)=(sourceClock d)ᴴ ∧
    (∀ y,encoded ((sourcePhysicalStrategy hd).bob (some y))=sourceBob y) := by
  simp only [sourcePhysicalStrategy,sourceAliceMeasurement,show (0 : Fin 2)=0 from rfl,if_true,
    show (1 : Fin 2)≠0 by decide,if_false,sourceAugmentedBob,
    finiteOrderMeasurement_encoding,sourceBobMeasurement_encoding]
  exact ⟨trivial,trivial,trivial,fun _ => trivial⟩

theorem source_bell_operator_sum :
    (∑ y : Ix d,kron (sourcePencil y) (sourceBob y))=
      ((1 : ℂ)/(Real.sin (Real.pi/(2*(d : ℝ))) : ℂ)) •
        (kron (sourceClock d) (sourceClock d)ᴴ + kron (cyclicShift d) (cyclicShift d)) := by
  simp only [sourcePencil,kron_add_left,kron_smul_left]
  rw [Finset.sum_add_distrib]
  have h0 : (∑ y : Ix d,kron (sourceClock d) (sourceBob y))=
      kron (sourceClock d) (∑ y : Ix d,sourceBob y) := by
    ext i j
    simp only [kron,Matrix.sum_apply,Finset.mul_sum]
  have h1 : (∑ y : Ix d,chi y • kron (cyclicShift d) (sourceBob y))=
      kron (cyclicShift d) (∑ y : Ix d,chi y • sourceBob y) := by
    ext i j
    simp only [kron,Matrix.sum_apply,Matrix.smul_apply,smul_eq_mul,Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro y _
    ring
  rw [h0,h1,source_fourier_zero,source_fourier_one,kron_smul_right,kron_smul_right,smul_add]

theorem source_phi_clock :
    expectation (maximallyEntangled d) (kron (sourceClock d) (sourceClock d)ᴴ)=1 := by
  rw [phi_trace]
  have ht : ((sourceClock d)ᴴ)ᵀ=(sourceClock d)ᴴ := by
    rw [sourceClock,Matrix.diagonal_conjTranspose,Matrix.diagonal_transpose]
  rw [ht,source_clock_unitary.2,Matrix.trace_one]
  simp only [ZMod.card]
  exact div_self (by exact_mod_cast NeZero.ne d)

theorem source_phi_shift :
    expectation (maximallyEntangled d) (kron (cyclicShift d) (cyclicShift d))=1 := by
  rw [phi_trace,←source_shift_adjoint,source_shift_unitary.2,Matrix.trace_one]
  simp only [ZMod.card]
  exact div_self (by exact_mod_cast NeZero.ne d)

/-- Exact complex Bell correlator sum of the literal source matrices. -/
theorem source_reduced_expectation :
    (∑ y : Ix d,expectation (maximallyEntangled d) (kron (sourcePencil y) (sourceBob y)))=
      ((2/Real.sin (Real.pi/(2*(d : ℝ))) : ℝ) : ℂ) := by
  rw [←expectation_sum,source_bell_operator_sum,expectation_smul,expectation_add,
    source_phi_clock,source_phi_shift]
  push_cast
  ring

/-- Actual positive state and d-outcome PVM strategy, with source Z, X,
literal Bob coefficients, and extra Z†, attains manuscript thm:exact and
cor:first-augmented. -/
theorem sourcePhysicalStrategy_attains (hd : 2≤d) :
    firstValue (sourcePhysicalStrategy hd)=2/Real.sin (Real.pi/(2*d))+1 := by
  obtain ⟨h0,h1,hb,hbr⟩ := sourcePhysicalStrategy_encodings hd
  have hv (T : Mat (Ix d × Ix d)) : stateEval (entangledState d).density T=
      (expectation (maximallyEntangled d) T).re :=
    congrArg Complex.re (expectation_eq_trace (maximallyEntangled d) T).symm
  unfold firstValue
  simp only [h0,h1,hb,hbr]
  change (∑ y : Ix d,stateEval (entangledState d).density (kron (sourcePencil y) (sourceBob y)))+
    stateEval (entangledState d).density (kron (sourceClock d) (sourceClock d)ᴴ)=_
  simp_rw [hv]
  rw [source_phi_clock,Complex.one_re,←Complex.re_sum,source_reduced_expectation,Complex.ofReal_re]

end CyclicBell.General
