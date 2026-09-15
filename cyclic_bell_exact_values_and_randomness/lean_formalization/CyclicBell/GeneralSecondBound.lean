import CyclicBell.GeneralSecondSOS
import CyclicBell.GeneralSecondCoefficients

/-! Unconditional physical second-family upper bound with the actual lambda.
The normalized-coefficient helper is instantiated and no coefficient premise
is left on the physical endpoint. Uncompiled source. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {ι κ : Type*} [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ]

def secondValue (s : StrategyOn d (Ix d) (AugmentedInputs d) ι κ) : ℝ :=
  (∑ l : Ix d,stateEval s.state.density (star (generalLambda l) •
    kron (encoded (s.alice l)) (secondFourier (fun y => encoded (s.bob (some y))) l)))+
    stateEval s.state.density (kron (encoded (s.alice 0)) (encoded (s.bob none)))

theorem secondFourier_bobLift (B : Ix d → Mat κ) (l : Ix d) :
    secondFourier (fun y => bobLift (ι := ι) (B y)) l = bobLift (secondFourier B l) := by
  simp [secondFourier,moduleFourier,bobLift,kron_sum_right,kron_smul_right]

/-- Quantifies over arbitrary finite local dimensions, not just C^d tensor C^d. -/
theorem second_physical_upper (hd : 2≤d)
    (s : StrategyOn d (Ix d) (AugmentedInputs d) ι κ) : secondValue s≤(d : ℝ)+1 := by
  let A : Ix d → Mat ι := fun l => encoded (s.alice l)
  let B : Ix d → Mat κ := fun y => encoded (s.bob (some y))
  have h := second_general_upper s.state generalLambda (generalLambda_normalization hd)
    (fun l => aliceLift (κ := κ) (A l)) (fun y => bobLift (ι := ι) (B y))
    (fun l => kron_unitary (encoded_unitary _) UnitaryRel.one)
    (fun y => kron_unitary UnitaryRel.one (encoded_unitary _))
  unfold secondReducedOperator at h
  simp_rw [secondFourier_bobLift,lift_product] at h
  rw [stateEval_sum] at h
  simp_rw [stateEval_herm _ _ s.state.positive.isHermitian] at h
  have ha := aligned_upper s.state.positive s.state.normalized
    (kron_unitary (encoded_unitary (s.alice 0)) (encoded_unitary (s.bob none)))
  exact add_le_add h ha

/-- The exact source SOS is instantiated rather than only its upper bound. -/
theorem second_source_sos (hd : 2≤d) (A B : Ix d → Mat ι)
    (hA : ∀ l,UnitaryRel (A l)) (hB : ∀ y,UnitaryRel (B y)) :
    (d : ℂ) • (1 : Mat ι)-secondReducedOperator generalLambda A B =
      (1/(2*d) : ℂ) • ∑ l,(secondResidual generalLambda A B l).conjTranspose*
        secondResidual generalLambda A B l :=
  second_general_sos generalLambda (generalLambda_normalization hd) A B hA hB

end CyclicBell.General
