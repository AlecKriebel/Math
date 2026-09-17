import CyclicBell.GeneralWitness

/-! Weighted-cycle powers, traces and first-harmonic blindness in arbitrary d.
No Bell maximality is inferred merely from these constructive identities.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

/-- Exact entry formula for EVERY natural power, not only the d-th power. -/
theorem weighted_power_entry (w : Ix d → ℂ) (r : ℕ) (i j : Ix d) :
    (weightedCycle w ^ r) i j =
      if i=j+(r : Ix d) then ∏ k ∈ Finset.range r,w (j+(k : Ix d)) else 0 := by
  induction r generalizing i j with
  | zero => simp [Matrix.one_apply]
  | succ r ih =>
    rw [pow_succ',Matrix.mul_apply]
    simp only [ih]
    rw [Finset.sum_eq_single (j+(r : Ix d))]
    · simp only [if_pos rfl,weightedCycle]
      rw [Finset.prod_range_succ]
      simp only [Nat.cast_add,Nat.cast_one,add_assoc]
      split_ifs <;> ring
    · intro k _ hk
      rw [if_neg hk,mul_zero]
    · simp

/-- Literal manuscript identity, including arbitrary non-unit weights. -/
theorem weighted_full_power (w : Ix d → ℂ) :
    weightedCycle w ^ d = (∏ j,w j) • (1 : Mat (Ix d)) := by
  ext i j
  rw [weighted_power_entry]
  simp only [ZMod.natCast_self,add_zero,Matrix.smul_apply,smul_eq_mul,Matrix.one_apply]
  have hp : (∏ k ∈ Finset.range d,w (j+(k : Ix d))) = ∏ k,w k := by
    rw [prod_representatives (fun k => w (j+k))]
    exact Fintype.prod_equiv (Equiv.addLeft j) _ _ (fun _ => rfl)
  rw [hp]
  split_ifs <;> ring

theorem weighted_entry_conjugate (w : Ix d → ℂ) :
    entryConjugate (weightedCycle w) = weightedCycle (fun j => star (w j)) := by
  ext i j
  simp only [entryConjugate,weightedCycle]
  split_ifs <;> simp

theorem weighted_linear (w v : Ix d → ℂ) (a b : ℂ) :
    a • weightedCycle w + b • weightedCycle v =
      weightedCycle (fun j => a*w j + b*v j) := by
  ext i j
  simp only [Matrix.add_apply,Matrix.smul_apply,smul_eq_mul,weightedCycle]
  split_ifs <;> ring

/-- Both coefficients are multiplied, not one conjugated, in the Phi trace. -/
theorem phi_weighted (w v : Ix d → ℂ) :
    expectation (maximallyEntangled d) (kron (weightedCycle w) (weightedCycle v)) =
      (∑ j,w j*v j)/(d : ℂ) := by
  rw [phi_trace]
  congr 1
  simp only [Matrix.trace,Matrix.diag_apply,Matrix.mul_apply,Matrix.transpose_apply,
    weightedCycle]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _
  rw [Finset.sum_eq_single (j+1)]
  · simp
  · intro i _ hi; simp [hi]
  · simp

/-- A finite residue inequality is proved from representatives, not primality. -/
theorem natCast_ne_zero_of_lt {k : ℕ} (hk : 0<k) (hkd : k<d) : (k : Ix d) ≠ 0 := by
  intro h
  have he := congrArg ZMod.val h
  simpa [ZMod.val_natCast,Nat.mod_eq_of_lt hkd,Nat.ne_of_gt hk] using he

theorem weighted_trace_zero (hd : 2≤d) (w : Ix d → ℂ) :
    Matrix.trace (weightedCycle w)=0 := by
  have h1 : (1 : Ix d) ≠ 0 := by simpa using natCast_ne_zero_of_lt (d := d) (k := 1) (by omega) (by omega)
  unfold Matrix.trace
  apply Finset.sum_eq_zero
  intro j _
  change (if j=j+1 then w j else 0)=0
  have hj : j ≠ j+1 := by
    intro h
    apply h1
    linear_combination -h
  simp [hj]

theorem product_from_recurrence (q w : Ix d → ℂ) (hq : UnitPhases q)
    (hr : ∀ j,q (j+1)=w j*q j) : ∏ j,w j=1 := by
  have hq0 (j : Ix d) : q j ≠ 0 := by
    intro h
    have := hq j
    simp [h] at this
  have hp : (∏ j,q j) ≠ 0 := Finset.prod_ne_zero_iff.mpr (fun j _ => hq0 j)
  have he : (∏ j,w j)*(∏ j,q j) = ∏ j,q j := by
    rw [← Finset.prod_mul_distrib]
    simp_rw [← hr]
    exact Fintype.prod_equiv (Equiv.addRight (1 : Ix d)) _ _ (fun _ => rfl)
  apply mul_right_cancel₀ hp
  simpa using he

theorem phases_permuted (z : Ix d → ℂ) (hz : UnitPhases z) (κ : Equiv.Perm (Ix d)) :
    UnitPhases (z ∘ κ) := by intro j; exact hz (κ j)

theorem product_permuted (z : Ix d → ℂ) (κ : Equiv.Perm (Ix d)) :
    (∏ j,z (κ j)) = ∏ j,z j := Fintype.prod_equiv κ _ _ (fun _ => rfl)

theorem sum_permuted (z : Ix d → ℂ) (κ : Equiv.Perm (Ix d)) :
    (∑ j,z (κ j)) = ∑ j,z j := Fintype.sum_equiv κ _ _ (fun _ => rfl)

/-- Complete complex correlator identities, before taking real parts. -/
theorem first_harmonic_permutation (z s : Ix d → ℂ) (κ : Equiv.Perm (Ix d)) :
    expectation (maximallyEntangled d)
      (kron (cyclicShift d) (entryConjugate (weightedCycle (s ∘ κ)))) =
        (∑ j,star (s j))/(d : ℂ) ∧
    expectation (maximallyEntangled d)
      (kron (weightedCycle (z ∘ κ)) (entryConjugate (weightedCycle (s ∘ κ)))) =
        (∑ j,z j*star (s j))/(d : ℂ) := by
  rw [weighted_entry_conjugate]
  constructor
  · rw [cyclicShift,phi_weighted]
    simp only [one_mul,Function.comp_apply]
    rw [sum_permuted (fun j => star (s j)) κ]
  · rw [phi_weighted]
    simp only [Function.comp_apply]
    rw [sum_permuted (fun j => z j*star (s j)) κ]

theorem added_first_harmonics (z : Ix d → ℂ) (κ : Equiv.Perm (Ix d)) :
    expectation (maximallyEntangled d) (kron (cyclicShift d) (cyclicShift d))=1 ∧
    expectation (maximallyEntangled d) (kron (weightedCycle (z ∘ κ)) (cyclicShift d))=
      (∑ j,z j)/(d : ℂ) := by
  constructor
  · rw [cyclicShift,phi_weighted]
    have hd : (d : ℂ) ≠ 0 := by exact_mod_cast (NeZero.ne d)
    simp [ZMod.card,hd]
  · rw [cyclicShift,phi_weighted]
    simp only [mul_one,Function.comp_apply]
    rw [sum_permuted]

theorem recurrence_lag_one (q w : Ix d → ℂ) (hq : UnitPhases q)
    (hr : ∀ j,q (j+1)=w j*q j) : autocorrelation q 1=∑ j,w j := by
  unfold autocorrelation
  apply Finset.sum_congr rfl
  intro j _
  rw [hr]
  calc
    w j*q j*star (q j)=w j*(star (q j)*q j) := by ring
    _=w j := by rw [hq j]; ring

theorem recurrence_lag_two (q w : Ix d → ℂ) (hq : UnitPhases q)
    (hr : ∀ j,q (j+1)=w j*q j) : autocorrelation q 2=∑ j,w j*w (j+1) := by
  unfold autocorrelation
  apply Finset.sum_congr rfl
  intro j _
  rw [show j+2=(j+1)+1 by ring,hr,hr]
  calc
    w (j+1)*(w j*q j)*star (q j)=w j*w (j+1)*(star (q j)*q j) := by ring
    _=_ := by rw [hq j]; ring

/-- Rank-one projectors are genuinely transported by conjugation; the Bob
observable construction does not confuse entry conjugation with adjoint. -/
theorem conjugate_measurement_encoding (w : Ix d → ℂ) (hw : UnitPhases w)
    (hp : ∏ j,w j=1) :
    encoded (cycleMeasurement (fun j => star (w j))
      (by intro j; simpa [mul_comm] using hw j)
      (by simpa using congrArg star hp)) = entryConjugate (weightedCycle w) := by
  rw [cycleMeasurement_encoding,weighted_entry_conjugate]

end CyclicBell.General
