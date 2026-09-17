import CyclicBell.GeneralCycles
import CyclicBell.GeneralPhases

/-! Literal complex phase functions, the parity-correct canonical chirp, and
canonical Fourier flatness in every d>=2. No Gauss-sum black box is assumed.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def chirpNat (d n : ℕ) : ℂ :=
  cis (Real.pi*((n : ℝ)*((n : ℝ)-1+parityDelta d))/(d : ℝ))

def canonicalPhase (j : Ix d) : ℂ := chirpNat d j.val

@[simp] theorem canonicalPhase_zero : canonicalPhase (0 : Ix d)=1 := by
  simp [canonicalPhase,chirpNat]

theorem canonicalPhase_unit : UnitPhases (canonicalPhase : Ix d → ℂ) := by
  intro j
  exact cis_unit _

theorem chirpNat_period (n : ℕ) : chirpNat d (n+d)=chirpNat d n := by
  obtain ⟨m,hm⟩ := parity_shift_even (d := d)
  have hd : (d : ℝ)≠0 := ne_of_gt dimension_pos
  have hang : Real.pi*(((n+d : ℕ) : ℝ)*(((n+d : ℕ) : ℝ)-1+parityDelta d))/(d : ℝ) =
      Real.pi*((n : ℝ)*((n : ℝ)-1+parityDelta d))/(d : ℝ) +
        2*Real.pi*((n+m : ℕ) : ℝ) := by
    push_cast
    field_simp
    linear_combination Real.pi*(d : ℝ)*hm
  unfold chirpNat
  rw [hang,cis_add]
  have hp : cis (2*Real.pi*((n+m : ℕ) : ℝ))=1 := by
    simpa using cis_period_int ((n+m : ℕ) : ℤ)
  rw [hp,mul_one]

/-- Only the one-wrap case is needed for adding two representatives. -/
theorem chirpNat_mod {n : ℕ} (hn : n<2*d) : chirpNat d (n%d)=chirpNat d n := by
  by_cases hnd : n<d
  · rw [Nat.mod_eq_of_lt hnd]
  · have hdn : d≤n := by omega
    have hlow : n-d<d := by omega
    have hn' : n=(n-d)+d := by omega
    conv_lhs => rw [hn',Nat.add_mod,Nat.mod_self,add_zero,Nat.mod_mod,Nat.mod_eq_of_lt hlow]
    conv_rhs => rw [hn']
    exact (chirpNat_period (d := d) (n-d)).symm

theorem residue_add_val (j t : Ix d) : (j+t).val=(j.val+t.val)%d := by
  conv_lhs => rw [← ZMod.natCast_zmod_val j,← ZMod.natCast_zmod_val t]
  rw [← Nat.cast_add,ZMod.val_natCast]

/-- Difference of the two quadratic phases leaves a linear character. -/
theorem canonical_ratio (j t : Ix d) :
    canonicalPhase (j+t)*star (canonicalPhase j) = canonicalPhase t*chi (t*j) := by
  have hj := ZMod.val_lt j
  have ht := ZMod.val_lt t
  rw [canonicalPhase,residue_add_val,chirpNat_mod (by omega)]
  change chirpNat d (j.val+t.val)*star (chirpNat d j.val) = chirpNat d t.val*chi (t*j)
  have hchi : chi (t*j) = cis (2*Real.pi*t.val*j.val/(d : ℝ)) := by
    have hnat : ((t.val*j.val : ℕ) : Ix d)=t*j := by simp
    rw [← hnat]
    simpa [Int.cast_natCast,Nat.cast_mul, mul_assoc] using chi_cis_int (d := d) ((t.val*j.val : ℕ) : ℤ)
  rw [chirpNat,chirpNat,chirpNat,← cis_sub,hchi,← cis_add]
  congr 1
  push_cast
  ring

theorem canonical_first_phase (hd : 2≤d) : canonicalPhase (1 : Ix d)=equalityBase d := by
  have hval : (1 : Ix d).val=1 := by
    rw [← Nat.cast_one,ZMod.val_natCast,Nat.mod_eq_of_lt (show 1<d by omega)]
  simp [canonicalPhase,hval,chirpNat,equalityBase]

theorem canonical_recurrence (hd : 2≤d) (j : Ix d) :
    canonicalPhase (j+1)=equalityRoot j*canonicalPhase j := by
  have h := canonical_ratio j 1
  rw [canonical_first_phase hd,one_mul] at h
  have hunit := canonicalPhase_unit (d := d) j
  calc
    canonicalPhase (j+1) = (canonicalPhase (j+1)*star (canonicalPhase j))*canonicalPhase j := by
      rw [mul_assoc,hunit,mul_one]
    _ = equalityRoot j*canonicalPhase j := by rw [h]; rfl

theorem equalityRoot_product (hd : 2≤d) : (∏ j : Ix d,equalityRoot j)=1 :=
  product_from_recurrence canonicalPhase equalityRoot canonicalPhase_unit (canonical_recurrence hd)

theorem canonical_autocorrelation (t : Ix d) :
    autocorrelation canonicalPhase t=if t=0 then (d : ℂ) else 0 := by
  simp only [autocorrelation,canonical_ratio,← Finset.mul_sum]
  rw [character_sum]
  by_cases ht : t=0
  · simp [ht]
  · simp [ht]

/-- All-dimensional canonical flatness, not a bounded numerical check. -/
theorem canonical_flat : FourierFlat (canonicalPhase : Ix d → ℂ) := by
  apply (flat_iff_autocorrelation _ canonicalPhase_unit).mpr
  intro t ht
  simp [canonical_autocorrelation,ht]

theorem canonical_uniform (a b : Ix d) :
    bornProbability (entangledState d).density
      ((phaseMeasurement canonicalPhase canonicalPhase_unit).effect a)
      ((fourierMeasurement d).effect b)=1/(d : ℝ)^2 := by
  rw [target_born_table]
  exact (table_uniform_iff _).mpr canonical_flat a b

theorem equalityRoot_sum_zero (hd : 2≤d) : (∑ j : Ix d,equalityRoot j)=0 := by
  have h1 : (1 : Ix d)≠0 := by simpa using natCast_ne_zero_of_lt (d := d) (k := 1) (by omega) (by omega)
  simp only [equalityRoot,← Finset.mul_sum]
  have hs := character_sum (1 : Ix d)
  simpa [one_mul,h1] using congrArg (fun z : ℂ => equalityBase d*z) hs

theorem equalityRoot_pair_sum_zero (hd : 3≤d) :
    (∑ j : Ix d,equalityRoot j*equalityRoot (j+1))=0 := by
  have h2 : (2 : Ix d)≠0 := by simpa using natCast_ne_zero_of_lt (d := d) (k := 2) (by omega) (by omega)
  have he (j : Ix d) : equalityRoot j*equalityRoot (j+1) =
      equalityBase d^2*chi (1 : Ix d)*chi ((2 : Ix d)*j) := by
    simp only [equalityRoot,chi_add]
    rw [show (2 : Ix d)*j=j+j by ring,chi_add]
    ring
  simp_rw [he]
  rw [← Finset.mul_sum,character_sum,if_neg h2,mul_zero]

/-- Every permutation has vanishing first lag in this family. -/
theorem permutation_lag_one (hd : 2≤d) (κ : Equiv.Perm (Ix d)) :
    autocorrelation («prefix» (equalityRoot ∘ κ)) 1=0 := by
  have hw := phases_permuted equalityRoot equalityRoot_unit κ
  have hp : ∏ j,equalityRoot (κ j)=1 := by rw [product_permuted,equalityRoot_product hd]
  rw [recurrence_lag_one _ _ (prefix_unit _ hw) (prefix_recurrence _ hp)]
  simp only [Function.comp_apply]
  rw [sum_permuted,equalityRoot_sum_zero hd]

end CyclicBell.General
