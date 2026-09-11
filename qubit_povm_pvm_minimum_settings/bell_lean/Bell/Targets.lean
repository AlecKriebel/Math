import Bell.Convexity
import Bell.Discrimination
import Bell.Transportation
import Bell.Lorentz
import Bell.LocalSimulation

/-!
# Target propositions and reusable conditional assembly

`UniversalTwoInputEquality`, `OneInputEquality`, `ProjectiveGlobalUpperBound`,
and `MainClaims` are definitions of propositions, not proofs by themselves.
The historical conditional helpers are retained with their original names.
`Assembly.lean` supplies their premises in the new end-to-end source draft;
`StrengthenedWitness.lean` supplies the separate Appendix B attainment draft.
Nothing in this interface file asserts that the draft has compiled.
-/

noncomputable section
open scoped BigOperators
namespace Bell

theorem bellScore_add (p q : Behavior separatorArchitecture) :
    bellScore (p+q)=bellScore p+bellScore q := by
  unfold bellScore correlation
  norm_num [Fin.sum_univ_succ,aliceSign,bobSign,Pi.add_apply]
  <;> ring

theorem bellScore_smul (r : ℝ) (p : Behavior separatorArchitecture) :
    bellScore (r • p)=r*bellScore p := by
  unfold bellScore correlation
  norm_num [Fin.sum_univ_succ,aliceSign,bobSign,Pi.smul_apply,smul_eq_mul]
  <;> ring

def bellLinear : Behavior separatorArchitecture →ₗ[ℝ] ℝ where
  toFun := bellScore
  map_add' := bellScore_add
  map_smul' := by
    intro r p
    simpa using bellScore_smul r p

/-- End-to-end target proposition for the global PVM bound in §3.2.
It quantifies over genuine physical strategies, not scalar stand-ins. -/
def ProjectiveGlobalUpperBound : Prop :=
  ∀ p ∈ rawPVM separatorArchitecture, bellScore p ≤ upper

/-- Main equality schema for input-dependent finite outputs. -/
def UniversalTwoInputEquality : Prop :=
  ∀ A : Architecture, A.aliceInputs=2 → A.bobInputs=2 →
    convexPOVM A=convexPVM A

/-- One-input equality used in the minimal-input corollary. -/
def OneInputEquality : Prop :=
  ∀ A : Architecture, (A.aliceInputs≤1 ∨ A.bobInputs≤1) →
    convexPOVM A=convexPVM A

/-- A strict separator in the actual common-randomness behavior model. -/
def StrictSeparation (A : Architecture) : Prop :=
  ∃ (f : Behavior A →ₗ[ℝ] ℝ) (p : Behavior A),
    p ∈ convexPOVM A ∧ ∀ q ∈ convexPVM A, f q < f p

/-- Separate target for the stronger explicit strategy of Appendix B. -/
def StrengthenedAttainment : Prop :=
  ∃ p ∈ rawPOVM separatorArchitecture, bellScore p=strengthenedLower

/-- The paper's principal equality/separation claims. `main_claims` in Assembly
is the new unconditional source attempt inhabiting this conjunction. Appendix B
attainment remains a separate proposition, supplied in StrengthenedWitness. -/
def MainClaims : Prop :=
  UniversalTwoInputEquality ∧ OneInputEquality ∧
  ProjectiveGlobalUpperBound ∧ StrictSeparation separatorArchitecture

/-- A raw PVM bound extends to the actual convex hull. This does not assert that
its premise `ProjectiveGlobalUpperBound` has been proved. -/
theorem convex_projective_bound_of_raw (h : ProjectiveGlobalUpperBound) :
    ∀ p ∈ convexPVM separatorArchitecture, bellScore p ≤ upper := by
  exact linear_bound_on_convexHull bellLinear (rawPVM separatorArchitecture) upper h

/-- Conditional, not an unconditional proof of Theorem 3.1. -/
theorem three_by_two_separation_of_projective_upper_bound
    (h : ProjectiveGlobalUpperBound) : StrictSeparation separatorArchitecture := by
  refine ⟨bellLinear,witnessBehavior,witness_mem_convex,?_⟩
  intro q hq
  change bellScore q < bellScore witnessBehavior
  rw [witness_value]
  exact lt_of_le_of_lt (convex_projective_bound_of_raw h q hq) strict_gap

theorem no_strict_separation_of_equal_hulls (A : Architecture)
    (h : convexPOVM A=convexPVM A) : ¬StrictSeparation A := by
  rintro ⟨f,p,hp,hs⟩
  have hp' : p ∈ convexPVM A := by rw [← h]; exact hp
  exact (lt_irrefl (f p)) (hs p hp')

/-- The arithmetic/logical last step of Corollary 9.4, conditional on both
equality theorems. The unconditional source client is `minimum_inputs`. -/
theorem minimum_inputs_of_equality_theorems
    (hone : OneInputEquality) (htwo : UniversalTwoInputEquality)
    (A : Architecture) (hs : StrictSeparation A) :
    (3≤A.aliceInputs ∧ 2≤A.bobInputs) ∨
    (2≤A.aliceInputs ∧ 3≤A.bobInputs) := by
  have ha2 : 2≤A.aliceInputs := by
    by_contra h
    have hsmall : A.aliceInputs≤1 := by omega
    exact no_strict_separation_of_equal_hulls A (hone A (Or.inl hsmall)) hs
  have hb2 : 2≤A.bobInputs := by
    by_contra h
    have hsmall : A.bobInputs≤1 := by omega
    exact no_strict_separation_of_equal_hulls A (hone A (Or.inr hsmall)) hs
  by_cases ha3 : 3≤A.aliceInputs
  · exact Or.inl ⟨ha3,hb2⟩
  by_cases hb3 : 3≤A.bobInputs
  · exact Or.inr ⟨ha2,hb3⟩
  have ha : A.aliceInputs=2 := by omega
  have hb : A.bobInputs=2 := by omega
  exact False.elim (no_strict_separation_of_equal_hulls A (htwo A ha hb) hs)

/-- Historical conditional helper, retained for compatibility. Its name does
not describe the current source inventory: Assembly now includes source
attempts supplying all three arguments. Compilation is still deferred. -/
theorem main_claims_of_missing_theorems
    (htwo : UniversalTwoInputEquality) (hone : OneInputEquality)
    (hupper : ProjectiveGlobalUpperBound) : MainClaims := by
  exact ⟨htwo,hone,hupper,three_by_two_separation_of_projective_upper_bound hupper⟩

end Bell
