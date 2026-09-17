import CyclicBell.GeneralSecondBound
import CyclicBell.GeneralFirstWitness

/-! Second augmented-family attainment and nonuniform witnesses for every d>=4.
The construction connects the coefficient phases, complete PVMs, attained value
and target-measurement identification. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def secondTwist (l : Ix d) : ℂ := cis (-Real.pi*(l.val : ℝ)*((l.val : ℝ)-1)/d)
def secondWeight (l j : Ix d) : ℂ := secondPrefactor l*chi (-(l*j))

theorem consecutive_integer_phase (n : ℕ) : cis (-Real.pi*(n : ℝ)*((n : ℝ)-1))=1 := by
  induction n with
  | zero => simp
  | succ n ih =>
    have ha : -Real.pi*((n+1 : ℕ) : ℝ)*(((n+1 : ℕ) : ℝ)-1)=
        -Real.pi*(n : ℝ)*((n : ℝ)-1)+2*Real.pi*(-(n : ℤ)) := by push_cast; ring
    rw [ha,cis_add,ih,one_mul]
    simpa only [Int.cast_neg,Int.cast_natCast] using cis_period_int (-(n : ℤ))

theorem secondTwist_power (l : Ix d) : secondTwist l^d=1 := by
  rw [secondTwist,cis_pow]
  have ha : (d : ℝ)*(-Real.pi*l.val*((l.val : ℝ)-1)/d)=
      -Real.pi*l.val*((l.val : ℝ)-1) := by field_simp [ne_of_gt (dimension_pos (d := d))]; ring
  rw [ha,consecutive_integer_phase]

theorem secondWeight_factor (l j : Ix d) :
    secondWeight l j=secondTwist l*star (equalityRoot j)^l.val := by
  have hr : secondPrefactor l=secondTwist l*star (equalityBase d)^l.val := by
    unfold secondPrefactor secondTwist equalityBase
    rw [← cis_neg,cis_pow,← cis_add]
    congr 1
    ring
  unfold secondWeight equalityRoot
  rw [hr,star_mul,mul_pow,chi_star,chi_pow]
  simp only [ZMod.natCast_zmod_val,mul_neg,neg_mul]
  ring

theorem secondWeight_unit (l : Ix d) : UnitPhases (secondWeight l : Ix d → ℂ) := by
  intro j
  unfold secondWeight
  have hr := secondPrefactor_unit (d := d) l
  have hc := chi_star_mul (-(l*j))
  rw [star_mul]
  calc
    (star (chi (-(l*j)))*star (secondPrefactor l))*(secondPrefactor l*chi (-(l*j))) =
        (star (secondPrefactor l)*secondPrefactor l)*(star (chi (-(l*j)))*chi (-(l*j))) := by ring
    _=1 := by rw [hr,hc,mul_one]

theorem secondWeight_product (hd : 2≤d) (l : Ix d) : (∏ j : Ix d,secondWeight l j)=1 := by
  simp_rw [secondWeight_factor]
  rw [Finset.prod_mul_distrib,Finset.prod_const,Finset.card_univ,ZMod.card,secondTwist_power,
    one_mul,Finset.prod_pow,← star_prod,equalityRoot_product hd]
  simp

def secondAlice (hd : 2≤d) (κ : Equiv.Perm (Ix d)) (l : Ix d) : Measurement d (Ix d) :=
  cycleMeasurement (fun j => star (secondWeight l (κ j)))
    (by intro j; simpa [mul_comm] using secondWeight_unit (d := d) l (κ j))
    (by rw [product_permuted (fun j => star (secondWeight l j)) κ]
        simpa only [star_prod,star_one] using congrArg star (secondWeight_product hd l))

def secondPermutationStrategy (hd : 2≤d) (κ : Equiv.Perm (Ix d)) :
    StrategyOn d (Ix d) (AugmentedInputs d) (Ix d) (Ix d) where
  state := entangledState d
  alice := secondAlice hd κ
  bob := permutationBob κ

@[simp] theorem secondAlice_encoding (hd : 2≤d) (κ : Equiv.Perm (Ix d)) (l : Ix d) :
    encoded (secondAlice hd κ l)=entryConjugate (weightedCycle (secondWeight l ∘ κ)) := by
  rw [secondAlice,cycleMeasurement_encoding,weighted_entry_conjugate]
  rfl

theorem weighted_sum {ν : Type*} [Fintype ν] (c : ν → ℂ) (w : ν → Ix d → ℂ) :
    (∑ a,c a • weightedCycle (w a))=weightedCycle (fun j => ∑ a,c a*w a j) := by
  ext i j
  simp only [Matrix.smul_apply,smul_eq_mul,weightedCycle,Matrix.sum_apply,Finset.sum_apply]
  by_cases h : i=j+1 <;> simp [h]

theorem polarTransform_shift (l t : Ix d) :
    (∑ y,chi (l*y)*star (polarPhase y t))=chi (-(l*t))*polarTransform l := by
  have he : (∑ y,chi (l*y)*star (polarBase (y+t))) =
      ∑ k,chi (l*(k-t))*star (polarBase k) := by
    simpa using sum_translate (fun k : Ix d => chi (l*(k-t))*star (polarBase k)) t
  rw [show (∑ y,chi (l*y)*star (polarPhase y t))=
    ∑ y,chi (l*y)*star (polarBase (y+t)) by rfl,he]
  unfold polarTransform fourier
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [mul_sub,sub_eq_add_neg,chi_add]
  ring

/-- Literal operator compression, with exact phase and no adjoint ambiguity. -/
theorem secondPermutation_compression (hd : 2≤d) (κ : Equiv.Perm (Ix d)) (l : Ix d) :
    secondFourier (fun y => encoded (permutationBob κ (some y))) l=
      ((d : ℂ)*generalLambda l) • weightedCycle (secondWeight l ∘ κ) := by
  unfold secondFourier moduleFourier
  simp only [permutationBob_some,weighted_entry_conjugate]
  rw [weighted_sum]
  have hs (j : Ix d) : (∑ y,chi (l*y)*star (polarPhase y (κ j)))=
      ((d : ℂ)*generalLambda l)*secondWeight l (κ j) := by
    rw [polarTransform_shift,polarTransform_compression hd]
    unfold secondWeight
    ring
  simp only [Function.comp_apply,hs]
  ext i j
  simp only [weightedCycle,Matrix.smul_apply,smul_eq_mul,Function.comp_apply]
  split_ifs <;> ring

theorem secondWeight_zero (j : Ix d) : secondWeight (0 : Ix d) j=1 := by
  simp [secondWeight,secondPrefactor]

theorem secondWeight_one_conjugate (hd : 2≤d) (j : Ix d) :
    star (secondWeight (1 : Ix d) j)=equalityRoot j := by
  have hv : (1 : Ix d).val=1 := by
    rw [← Nat.cast_one,ZMod.val_natCast,Nat.mod_eq_of_lt (show 1<d by omega)]
  rw [secondWeight_factor]
  simp [hv,secondTwist]

@[simp] theorem secondAlice_zero (hd : 2≤d) (κ : Equiv.Perm (Ix d)) :
    encoded (secondAlice hd κ 0)=cyclicShift d := by
  rw [secondAlice_encoding,weighted_entry_conjugate]
  simp only [Function.comp_apply,secondWeight_zero,star_one]
  rfl

@[simp] theorem secondAlice_one (hd : 2≤d) (κ : Equiv.Perm (Ix d)) :
    encoded (secondAlice hd κ 1)=weightedCycle (equalityRoot ∘ κ) := by
  rw [secondAlice_encoding,weighted_entry_conjugate]
  simp only [Function.comp_apply,secondWeight_one_conjugate hd]
  rfl

/-- The actual l-th term is d*normSq(lambda_l), not merely a zero residual. -/
theorem secondPermutation_term (hd : 2≤d) (κ : Equiv.Perm (Ix d)) (l : Ix d) :
    stateEval (entangledState d).density
      (star (generalLambda l) • kron (encoded (secondAlice hd κ l))
        (secondFourier (fun y => encoded (permutationBob κ (some y))) l)) =
      (d : ℝ)*Complex.normSq (generalLambda l) := by
  rw [secondPermutation_compression hd,secondAlice_encoding,kron_smul_right,
    entangled_stateEval,expectation_smul,expectation_smul,weighted_entry_conjugate,phi_weighted]
  have he : (∑ j,star ((secondWeight l ∘ κ) j)*(secondWeight l ∘ κ) j)=(d : ℂ) := by
    simp only [Function.comp_apply]
    simp_rw [show ∀ j : Ix d, star (secondWeight l j) * secondWeight l j = 1 from secondWeight_unit l]
    simp [ZMod.card]
  rw [he,div_self (show (d : ℂ)≠0 by exact_mod_cast (NeZero.ne d)),mul_one]
  have hnorm := Complex.normSq_eq_conj_mul_self (z := generalLambda l)
  have hm : star (generalLambda l)*((d : ℂ)*generalLambda l)=
      (d : ℂ)*(Complex.normSq (generalLambda l) : ℂ) := by rw [hnorm]; simp only [Complex.star_def]; ring
  rw [hm]
  simp

theorem secondPermutation_attains (hd : 2≤d) (κ : Equiv.Perm (Ix d)) :
    secondValue (secondPermutationStrategy hd κ)=(d : ℝ)+1 := by
  unfold secondValue
  change (∑ l,stateEval (entangledState d).density
      (star (generalLambda l) • kron (encoded (secondAlice hd κ l))
        (secondFourier (fun y => encoded (permutationBob κ (some y))) l)))+
      stateEval (entangledState d).density
        (kron (encoded (secondAlice hd κ 0)) (encoded (permutationBob κ none)))=_
  simp_rw [secondPermutation_term hd κ]
  rw [secondAlice_zero,permutationBob_none,entangled_stateEval,
    (added_first_harmonics (equalityRoot : Ix d → ℂ) κ).1,Complex.one_re,← Finset.mul_sum]
  have hn := generalLambda_normalization (d := d) hd
  simp only [Complex.star_def, ← Complex.normSq_eq_conj_mul_self] at hn
  have hr := congrArg Complex.re hn
  simp only [Complex.re_sum,Complex.ofReal_re,Complex.one_re] at hr
  rw [hr,mul_one]

/-- Equality of observables implies equality of the PVMs with fixed output
encoding. This prevents a hidden output relabeling in the target bridge. -/
theorem measurement_effect_eq_of_encoded_eq {ι : Type*} [Fintype ι] [DecidableEq ι]
    (M N : Measurement d ι) (h : encoded M=encoded N) (a : Ix d) : M.effect a=N.effect a := by
  rw [measurement_reconstruction M a,h,← measurement_reconstruction N a]

theorem second_first_target_same (hd : 2≤d) (κ : Equiv.Perm (Ix d)) (a b : Ix d) :
    behavior (secondPermutationStrategy hd κ) 1 none a b=
      behavior (firstPermutationStrategy hd κ) 1 none a b := by
  have he : encoded (secondAlice hd κ (1 : Ix d))=encoded (permutationAlice hd κ (1 : Fin 2)) := by
    rw [secondAlice_one,permutationAlice_one]
  change bornProbability (entangledState d).density ((secondAlice hd κ 1).effect a)
      ((permutationBob κ none).effect b)=_
  rw [measurement_effect_eq_of_encoded_eq _ _ he a]
  rfl

theorem secondPermutation_maximal (hd : 2≤d) (κ : Equiv.Perm (Ix d))
    {ι ν : Type*} [Fintype ι] [Fintype ν] [DecidableEq ι] [DecidableEq ν]
    (t : StrategyOn d (Ix d) (AugmentedInputs d) ι ν) :
    secondValue t≤secondValue (secondPermutationStrategy hd κ) := by
  rw [secondPermutation_attains]
  exact second_physical_upper hd t

/-- All-dimensional second-family scalar-maximality counterexample, without
any claim about the exact supremal Eve guessing probability. -/
theorem second_all_dimension_counterexample (hd : 4≤d) :
    ∃ s : StrategyOn d (Ix d) (AugmentedInputs d) (Ix d) (Ix d),
      secondValue s=(d : ℝ)+1 ∧
      (∀ nA nB : ℕ,∀ t : StrategyOn d (Ix d) (AugmentedInputs d) (Fin nA) (Fin nB),
        secondValue t≤secondValue s) ∧
      (∀ a b,(∑ b',behavior s 1 none a b')=1/(d : ℝ) ∧
        (∑ a',behavior s 1 none a' b)=1/(d : ℝ)) ∧
      (¬ ∀ a b,behavior s 1 none a b=1/(d : ℝ)^2) ∧
      (∃ a b,1/(d : ℝ)^2+
        2*Real.sin (Real.pi/(d : ℝ))*Real.sin (3*Real.pi/(d : ℝ))/
          ((d : ℝ)^2*((d : ℝ)-1)) ≤ behavior s 1 none a b) := by
  let s := secondPermutationStrategy (d := d) (by omega : 2≤d) (finalSwap d)
  refine ⟨s,secondPermutation_attains (by omega) _,?_,?_,?_,?_⟩
  · intro nA nB t
    exact secondPermutation_maximal (by omega) _ t
  · intro a b
    dsimp [s]
    simp_rw [second_first_target_same,firstSwap_target hd]
    exact swappedTarget_marginals a b
  · simpa only [s,second_first_target_same,firstSwap_target hd]
      using swappedTarget_not_uniform (d := d) hd
  · simpa only [s,second_first_target_same,firstSwap_target hd]
      using swappedTarget_quantitative (d := d) hd

end CyclicBell.General
