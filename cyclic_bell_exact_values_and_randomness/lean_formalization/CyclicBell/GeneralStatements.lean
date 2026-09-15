import CyclicBell.PhaseTableStatements
import CyclicBell.AdversarialStatements
import CyclicBell.ModelValueStatements
import CyclicBell.GeneralGuessing
import CyclicBell.GeneralSecondWitness
import CyclicBell.GeneralPermutation
import CyclicBell.GeneralSupportSaturation
import CyclicBell.GeneralEqualityPhases
import CyclicBell.GeneralRigidity
import CyclicBell.GeneralSecondCommuting
import CyclicBell.GeneralOperational
import CyclicBell.GeneralExposure
import CyclicBell.GeneralBinary
import CyclicBell.GeneralOneInput
import CyclicBell.GeneralConsequences
import CyclicBell.GeneralBinaryWitness
import CyclicBell.GeneralOrbitConsequences

/-! Expanded all-dimensional statements for an offline statement review.
These are source candidates, not executed tests or an independent-agent audit. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder Topology
namespace CyclicBell.GeneralStatementAudit
open General

example (d : ℕ) [NeZero d] (hd : 2≤d) (z : ℂ) (hz : ‖z‖=1) :
    (∑ y : ZMod d,‖1+ZMod.stdAddChar y*z‖)≤2/Real.sin (Real.pi/(2*d)) :=
  scalar_bound hd z hz

example (d : ℕ) [NeZero d] (hd : 2≤d) (z : ℂ) (hz : ‖z‖=1) :
    ((∑ y : ZMod d,‖1+ZMod.stdAddChar y*z‖)=2/Real.sin (Real.pi/(2*d))) ↔
      z^d=(-1 : ℂ)^(d-1) := scalar_equality_iff hd z hz

example (d : ℕ) [NeZero d] (w : ZMod d → ℂ) :
    weightedCycle w^d=(∏ j,w j) • (1 : Matrix (ZMod d) (ZMod d) ℂ) :=
  weighted_full_power w

example (d : ℕ) [NeZero d] (q : ZMod d → ℂ)
    (hq : ∀ j,star (q j)*q j=1) (a b : ZMod d) :
    (Matrix.trace ((entangledState d).density *
      kron ((phaseMeasurement q hq).effect a) ((fourierMeasurement d).effect b))).re =
        Complex.normSq (∑ j,ZMod.stdAddChar (-(a+b)*j)*q j)/(d : ℝ)^3 :=
  target_born_table q hq a b

example (d : ℕ) [NeZero d] (a b : ZMod d) :
    bornProbability (entangledState d).density
      ((phaseMeasurement canonicalPhase canonicalPhase_unit).effect a)
      ((fourierMeasurement d).effect b)=1/(d : ℝ)^2 := canonical_uniform a b

example (d : ℕ) [NeZero d] (hd : 4≤d) :
    autocorrelation (swappedPhase : ZMod d → ℂ) 2 =
      (equalityRoot (-1)-equalityRoot (-2))*(equalityRoot (-3)-equalityRoot 0) := swapped_R2 hd

example (d : ℕ) [NeZero d] (hd : 4≤d) :
    ¬ ∀ a b : ZMod d,bornProbability (entangledState d).density
      ((phaseMeasurement swappedPhase swappedPhase_unit).effect a)
      ((fourierMeasurement d).effect b)=1/(d : ℝ)^2 := swappedTarget_not_uniform hd

example (d : ℕ) [NeZero d] (hd : 4≤d) :
    ∃ a b : ZMod d,1/(d : ℝ)^2+
      2*Real.sin (Real.pi/(d : ℝ))*Real.sin (3*Real.pi/(d : ℝ))/
        ((d : ℝ)^2*((d : ℝ)-1)) ≤
      bornProbability (entangledState d).density
        ((phaseMeasurement swappedPhase swappedPhase_unit).effect a)
        ((fourierMeasurement d).effect b) := swappedTarget_quantitative hd

example (d : ℕ) [NeZero d] {E : Type*} [AddCommGroup E] [Module ℂ E]
    (σ : ZMod d → ZMod d → E) (ρ : E) :
    (∀ a b,σ a b=((d : ℂ)⁻¹)^2 • ρ) ↔
      (∑ a,∑ b,ZMod.stdAddChar ((0 : ZMod d)*a+0*b) • σ a b)=ρ ∧
      ∀ k l,(k,l)≠(0,0) → (∑ a,∑ b,ZMod.stdAddChar (k*a+l*b) • σ a b)=0 :=
  operator_uniform_iff σ ρ


/-! Universal bounds and support rigidity, with unrestricted local dimensions. -/
example (d nA nB : ℕ) [NeZero d] (hd : 2≤d)
    (s : StrategyOn d (Fin 2) (Option (ZMod d)) (Fin nA) (Fin nB)) :
    firstValue s≤2/Real.sin (Real.pi/(2*d))+1 := first_physical_upper hd s

example (d nA nB : ℕ) [NeZero d] (hd : 2≤d)
    (s : StrategyOn d (ZMod d) (Option (ZMod d)) (Fin nA) (Fin nB)) :
    secondValue s≤(d : ℝ)+1 := second_physical_upper hd s

example (d nA nB : ℕ) [NeZero d] (hd : 2≤d)
    (s : StrategyOn d (Fin 2) (Option (ZMod d)) (Fin nA) (Fin nB))
    (hs : firstValue s=2/Real.sin (Real.pi/(2*d))+1) :
    d∣Module.finrank ℂ (LinearMap.range (partialTraceBob s.state.density).mulVecLin) :=
  supported_dimension_divisible hd s hs

example (d nA nB : ℕ) [NeZero d] (hd : 2≤d)
    (s : StrategyOn d (Fin 2) (Option (ZMod d)) (Fin nA) (Fin nB))
    (hs : firstValue s=2/Real.sin (Real.pi/(2*d))+1) :
    let U := (encoded (s.alice 0)).conjTranspose*encoded (s.alice 1)
    preservesRange U (aliceSupport s.state) ∧ preservesRange U.conjTranspose (aliceSupport s.state) ∧
    ∃ r : ℕ,0<r ∧
      (∀ k : ZMod d,Module.finrank ℂ (aliceSupport s.state ⊓
        LinearMap.ker (U-equalityRoot k • 1).mulVecLin)=r) ∧
      Module.finrank ℂ (aliceSupport s.state)=d*r := supported_multiplicity_rigidity hd s hs

/-! No finite-dimensional hypothesis in these independently expanded bounds. -/
example (d : ℕ) [NeZero d] (hd : 2≤d) (H : Type*)
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (ψ : H) (hψ : ‖ψ‖=1) (a₀ a₁ : H →L[ℂ] H) (b : ZMod d → H →L[ℂ] H)
    (h₀ : star a₀*a₀=1 ∧ a₀*star a₀=1) (h₁ : star a₁*a₁=1 ∧ a₁*star a₁=1)
    (hb : ∀ y,star (b y)*b y=1 ∧ b y*star (b y)=1)
    (hc₀ : ∀ y,a₀*b y=b y*a₀) (hc₁ : ∀ y,a₁*b y=b y*a₁) :
    vectorEval ψ (∑ y : ZMod d,(1/2 : ℂ) •
      ((a₀+(ZMod.stdAddChar y : ℂ) • a₁)*b y+star ((a₀+(ZMod.stdAddChar y : ℂ) • a₁)*b y)))≤
      2/Real.sin (Real.pi/(2*d)) := first_commuting_hilbert_bound hd ψ hψ a₀ a₁ b h₀ h₁ hb hc₀ hc₁

example (d : ℕ) [NeZero d] (hd : 2≤d) (H : Type*)
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (ψ : H) (hψ : ‖ψ‖=1) (a b : ZMod d → H →L[ℂ] H)
    (ha : ∀ l,StarUnitary (a l)) (hb : ∀ y,StarUnitary (b y)) :
    vectorEval ψ (operatorSecond generalLambda a b)≤d := second_commuting_hilbert_bound hd ψ hψ a b ha hb

example (d : ℕ) [NeZero d] (hd : 2≤d) (l : ZMod d) :
    generalLambda l=(-1 : ℂ)^((l.val : ℤ)-1)*
      Complex.exp (((Real.pi*(l.val : ℝ)*((l.val : ℝ)-1)/d : ℝ) : ℂ)*Complex.I)/
        ((d : ℂ)*(Real.sin (Real.pi*((l.val : ℝ)-1/2)/d) : ℂ)) := generalLambda_literal l

example (d : ℕ) [NeZero d] (hd : 2≤d) :
    (∑ l : ZMod d,star (generalLambda l)*generalLambda l)=1 := generalLambda_normalization hd

example (d : ℕ) [NeZero d] (hd : 2≤d) (κ : Equiv.Perm (ZMod d)) :
    firstValue (firstPermutationStrategy hd κ)=2/Real.sin (Real.pi/(2*d))+1 := firstPermutation_attains hd κ

example (d : ℕ) [NeZero d] (hd : 2≤d) (κ : Equiv.Perm (ZMod d)) :
    secondValue (secondPermutationStrategy hd κ)=d+1 := secondPermutation_attains hd κ

example (d : ℕ) [NeZero d] (hd : 4≤d) :
    let s := firstPermutationStrategy (d := d) (by omega : 2≤d) (finalSwap d)
    firstValue s=scalarMaximum d+1 ∧
      ∃ g : ZMod d×ZMod d,1/(d : ℝ)^2<fixedGuessSuccess s.state.density (s.alice 1) (s.bob none) g :=
  first_all_dimension_physical_Eve_gap hd

example (d : ℕ) [NeZero d] (hd : 4≤d) (f : ℝ → ℝ)
    (hf : Filter.Tendsto f (nhdsWithin 0 (Set.Ioi 0)) (nhds 0)) :
    ¬ (∀ e : ℝ,0<e → ∀ s : StrategyOn d (Fin 2) (Option (ZMod d)) (ZMod d) (ZMod d),
      scalarMaximum d+1-firstValue s≤e → ∀ g : ZMod d×ZMod d,
        fixedGuessSuccess s.state.density (s.alice 1) (s.bob none) g≤1/(d : ℝ)^2+f e) :=
  first_no_value_only_endpoint_robustness hd f hf

example {ι ε : Type*} [Fintype ι] [Fintype ε] [DecidableEq ι] [DecidableEq ε]
    (T : Matrix ι ε ℂ) (hT : frobeniusSq T=1) (A₀ A₁ B₀ B₁ : Mat ι)
    (hA₀ : HermitianInvolution A₀) (hA₁ : HermitianInvolution A₁)
    (hB₀ : HermitianInvolution B₀) (hB₁ : HermitianInvolution B₁)
    (hc : BinaryCross A₀ A₁ B₀ B₁)
    (hsat : stateEval (T*T.conjTranspose) (binaryScoreOperator A₀ A₁ B₀ B₁)=3*Real.sqrt 3) :
    ∀ a b : Fin 2,partialE
      (kron (binaryEffect A₀ a*binaryEffect B₀ b) (1 : Mat ε)*
        projector (fun p : ι×ε => T p.1 p.2)*
        (kron (binaryEffect A₀ a*binaryEffect B₀ b) (1 : Mat ε)).conjTranspose)=
      (1/4 : ℂ) • reducedE T := by
  intro a b
  rw [← conditionalE_actual_sandwich]
  exact binary_saturation_privacy T hT A₀ A₁ B₀ B₁ hA₀ hA₁ hB₀ hB₁ hc hsat a b

example : -(Real.log (3/32)/Real.log 2)=5-Real.log 3/Real.log 2 := d4_entropy_exact

end CyclicBell.GeneralStatementAudit
