import CyclicBell.GeneralScalar
import CyclicBell.GeneralChirp

/-! Actual final-two swap in every d>=4. The target distribution below is
computed from a normalized tensor state and PVMs, not defined by its Fourier
formula. Bell maximality is a separate obligation; it is not assumed here.
All proofs are uncompiled candidates. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def finalSwap (d : ℕ) [NeZero d] : Equiv.Perm (Ix d) := Equiv.swap (-2) (-1)
def swappedWeight (j : Ix d) : ℂ := equalityRoot (finalSwap d j)
def swappedPhase : Ix d → ℂ := «prefix» swappedWeight

theorem negative_representative {k : ℕ} (hk : 0<k) (hkd : k≤d) :
    (-(k : Ix d)).val=d-k := by
  have hlt : d-k<d := by omega
  have he : ((d-k : ℕ) : Ix d)=-(k : Ix d) := by
    have hsum : ((d-k : ℕ) : Ix d)+(k : Ix d)=0 := by
      rw [← Nat.cast_add,Nat.sub_add_cancel hkd]
      simp
    linear_combination hsum
  rw [← he,ZMod.val_natCast,Nat.mod_eq_of_lt hlt]

/-- Natural-index bridge to the literal final entries (d-2,d-1). -/
theorem finalSwap_representatives (hd : 4≤d) :
    (-2 : Ix d).val=d-2 ∧ (-1 : Ix d).val=d-1 ∧
    finalSwap d (-2)=(-1) ∧ finalSwap d (-1)=(-2) := by
  refine ⟨by simpa using (negative_representative (d := d) (k := 2) (by omega) (by omega)),
    by simpa using (negative_representative (d := d) (k := 1) (by omega) (by omega)),?_,?_⟩ <;>
    simp [finalSwap]

theorem finalSwap_away (j : Ix d) (h₂ : j≠-2) (h₁ : j≠-1) :
    finalSwap d j=j := by simp [finalSwap,Equiv.swap_apply_def,h₂,h₁]

theorem swappedWeight_unit : UnitPhases (swappedWeight : Ix d → ℂ) := by
  intro j
  exact equalityRoot_unit (finalSwap d j)

theorem swappedWeight_product (hd : 4≤d) : (∏ j : Ix d,swappedWeight j)=1 := by
  unfold swappedWeight
  rw [product_permuted,equalityRoot_product (by omega)]

theorem swappedPhase_unit : UnitPhases (swappedPhase : Ix d → ℂ) :=
  prefix_unit _ swappedWeight_unit

theorem swappedPhase_recurrence (hd : 4≤d) (j : Ix d) :
    swappedPhase (j+1)=swappedWeight j*swappedPhase j :=
  prefix_recurrence _ (swappedWeight_product hd) j

/-- Only two directed edges contribute to the adjacent-product change.
The edge joining the swapped labels reverses order, so its product is unchanged. -/
theorem swap_adjacent_sum (hd : 4≤d) (z : Ix d → ℂ) :
    (∑ j,z (finalSwap d j)*z (finalSwap d (j+1))) - (∑ j,z j*z (j+1)) =
      (z (-1)-z (-2))*(z (-3)-z 0) := by
  have h1 : (1 : Ix d)≠0 := by simpa using (natCast_ne_zero_of_lt (d := d) (k := 1) (by omega) (by omega))
  have h2 : (2 : Ix d)≠0 := natCast_ne_zero_of_lt (d := d) (k := 2) (by omega) (by omega)
  have h3 : (3 : Ix d)≠0 := natCast_ne_zero_of_lt (d := d) (k := 3) (by omega) (by omega)
  have h21 : (-2 : Ix d)≠-1 := by intro h; apply h1; linear_combination -h
  have h31 : (-3 : Ix d)≠-1 := by intro h; apply h2; linear_combination -h
  have h32 : (-3 : Ix d)≠-2 := by intro h; apply h1; linear_combination -h
  have h01 : (0 : Ix d)≠-1 := by intro h; apply h1; linear_combination h
  have h02 : (0 : Ix d)≠-2 := by intro h; apply h2; linear_combination h
  have point (j : Ix d) :
      z (finalSwap d j)*z (finalSwap d (j+1))-z j*z (j+1) =
        (if j=-3 then z (-3)*(z (-1)-z (-2)) else 0) +
        (if j=-1 then (z (-2)-z (-1))*z 0 else 0) := by
    by_cases hj3 : j=-3
    · subst j
      have hs : (-3 : Ix d)+1=-2 := by ring
      rw [hs]
      simp [finalSwap,Equiv.swap_apply_def,h31,h32]
      ring
    · by_cases hj2 : j=-2
      · subst j
        have hs : (-2 : Ix d)+1=-1 := by ring
        rw [hs]
        simp [finalSwap,Equiv.swap_apply_def,h21,hj3,mul_comm]
      · by_cases hj1 : j=-1
        · subst j
          simp [finalSwap,Equiv.swap_apply_def,h01,h02,h21.symm,hj3]
          ring
        · have hn2 : j+1≠-2 := by intro h; apply hj3; linear_combination h
          have hn1 : j+1≠-1 := by intro h; apply hj2; linear_combination h
          simp [finalSwap_away j hj2 hj1,finalSwap_away (j+1) hn2 hn1,hj3,hj1]
  rw [← Finset.sum_sub_distrib]
  simp_rw [point]
  rw [Finset.sum_add_distrib]
  simp
  ring

/-- The exact nonzero autocorrelation identity from eq:R2. -/
theorem swapped_R2 (hd : 4≤d) :
    autocorrelation (swappedPhase : Ix d → ℂ) 2 =
      (equalityRoot (d := d) (-1)-equalityRoot (d := d) (-2))*(equalityRoot (d := d) (-3)-equalityRoot (d := d) 0) := by
  rw [recurrence_lag_two swappedPhase swappedWeight swappedPhase_unit (swappedPhase_recurrence hd)]
  have h := swap_adjacent_sum (d := d) hd (equalityRoot : Ix d → ℂ)
  rw [equalityRoot_pair_sum_zero (by omega),sub_zero] at h
  exact h

theorem swapped_R2_ne_zero (hd : 4≤d) :
    autocorrelation (swappedPhase : Ix d → ℂ) 2≠0 := by
  rw [swapped_R2 hd]
  apply mul_ne_zero
  · apply sub_ne_zero.mpr
    intro h
    have he := equalityRoot_injective h
    have h1 : (1 : Ix d)≠0 := by simpa using (natCast_ne_zero_of_lt (d := d) (k := 1) (by omega) (by omega))
    apply h1
    linear_combination he
  · apply sub_ne_zero.mpr
    intro h
    have he := equalityRoot_injective h
    have h3 : (3 : Ix d)≠0 := natCast_ne_zero_of_lt (d := d) (k := 3) (by omega) (by omega)
    apply h3
    linear_combination -he

/-- Exact convention-sensitive relation of the target PVM to the swap cycle. -/
theorem swapped_target_encoding (hd : 4≤d) :
    encoded (phaseMeasurement (swappedPhase : Ix d → ℂ) swappedPhase_unit)=
      weightedCycle swappedWeight :=
  phaseMeasurement_encoding _ _ swappedPhase_unit (swappedPhase_recurrence hd)

def swappedTarget (d : ℕ) [NeZero d] (a b : Ix d) : ℝ :=
  bornProbability (entangledState d).density
    ((phaseMeasurement swappedPhase swappedPhase_unit).effect a)
    ((fourierMeasurement d).effect b)

theorem swappedTarget_fourier (a b : Ix d) :
    swappedTarget d a b=fourierTable swappedPhase a b := target_born_table _ _ _ _

theorem swappedTarget_nonnegative (a b : Ix d) : 0≤swappedTarget d a b := by
  rw [swappedTarget_fourier]
  exact table_nonnegative _ _ _

theorem swappedTarget_marginals (a b : Ix d) :
    (∑ b',swappedTarget d a b')=1/(d : ℝ) ∧
    (∑ a',swappedTarget d a' b)=1/(d : ℝ) := by
  simp only [swappedTarget_fourier]
  exact ⟨table_row_sum _ swappedPhase_unit a,table_column_sum _ swappedPhase_unit b⟩

theorem swappedTarget_normalized : (∑ a,∑ b,swappedTarget d a b)=1 := by
  simp only [swappedTarget_fourier]
  exact table_normalized _ swappedPhase_unit

/-- Physical nonuniformity for every d>=4; this is NOT yet a Bell optimality claim. -/
theorem swappedTarget_not_uniform (hd : 4≤d) :
    ¬ ∀ a b,swappedTarget d a b=1/(d : ℝ)^2 := by
  simp only [swappedTarget_fourier]
  exact nonzero_lag_not_uniform _ swappedPhase_unit 2
    (natCast_ne_zero_of_lt (d := d) (k := 2) (by omega) (by omega)) (swapped_R2_ne_zero hd)

/-- A normalized finite distribution that is not uniform has an above-uniform
entry; no particular output is asserted to optimize over realizations. -/
theorem exists_above_uniform {ι : Type*} [Fintype ι] [Nonempty ι]
    (p : ι → ℝ) (hp : ∑ i,p i=1)
    (hnu : ¬ ∀ i,p i=1/(Fintype.card ι : ℝ)) :
    ∃ i,1/(Fintype.card ι : ℝ)<p i := by
  classical
  by_contra h
  push_neg at h
  have hn : (Fintype.card ι : ℝ)≠0 := by exact_mod_cast Fintype.card_ne_zero
  have hs : (∑ i : ι,1/(Fintype.card ι : ℝ))=1 := by simp [hn]
  apply hnu
  have heq := (Finset.sum_eq_sum_iff_of_le (s := Finset.univ)
    (fun i _ => h i)).mp (hp.trans hs.symm)
  intro i
  exact heq i (Finset.mem_univ i)

/-- Operational randomness obstruction for this realization: a constant guess
of one output pair succeeds more often than 1/d^2. -/
theorem swappedTarget_guessing_gap (hd : 4≤d) :
    ∃ a b,1/(d : ℝ)^2<swappedTarget d a b := by
  have hp : (∑ ab : Ix d × Ix d,swappedTarget d ab.1 ab.2)=1 := by
    simpa [Fintype.sum_prod_type] using swappedTarget_normalized (d := d)
  have hnu : ¬ ∀ ab : Ix d × Ix d,
      swappedTarget d ab.1 ab.2=1/(Fintype.card (Ix d × Ix d) : ℝ) := by
    simpa [Fintype.card_prod,ZMod.card,pow_two] using swappedTarget_not_uniform (d := d) hd
  obtain ⟨⟨a,b⟩,hab⟩ := exists_above_uniform _ hp hnu
  exact ⟨a,b,by simpa [Fintype.card_prod,ZMod.card,pow_two] using hab⟩

/-- Consolidated all-d physical target endpoint, without claiming a Bell bound. -/
theorem all_dimension_physical_nonuniformity (hd : 4≤d) :
    (∑ a,∑ b,swappedTarget d a b)=1 ∧
    (∀ a b,(∑ b',swappedTarget d a b')=1/(d : ℝ) ∧
      (∑ a',swappedTarget d a' b)=1/(d : ℝ)) ∧
    (¬ ∀ a b,swappedTarget d a b=1/(d : ℝ)^2) ∧
    (∃ a b,1/(d : ℝ)^2<swappedTarget d a b) :=
  ⟨swappedTarget_normalized,swappedTarget_marginals,
    swappedTarget_not_uniform hd,swappedTarget_guessing_gap hd⟩

end CyclicBell.General
