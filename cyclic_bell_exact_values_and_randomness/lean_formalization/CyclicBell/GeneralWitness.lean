import CyclicBell.GeneralModel

/-! General weighted-cycle measurement construction and exact physical Born
bridge. The phase inputs are constrained only by unimodularity and the cyclic
recurrence, not by a Bell value or probability conclusion. SOURCE CANDIDATE. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

/-- Real amplitude used in Phi_d and Fourier eigenvectors. -/
def invSqrtDim (d : ℕ) : ℝ := (Real.sqrt (d : ℝ))⁻¹

theorem invSqrtDim_pos : 0 < invSqrtDim d := by
  exact inv_pos.mpr (Real.sqrt_pos.2 dimension_pos)

theorem invSqrtDim_sq : invSqrtDim d ^ 2 = (d : ℝ)⁻¹ := by
  unfold invSqrtDim
  rw [inv_pow, Real.sq_sqrt (le_of_lt dimension_pos)]

theorem invSqrtDim_complex_sq : ((invSqrtDim d : ℂ))^2 = (d : ℂ)⁻¹ := by
  simpa only [Complex.ofReal_pow, Complex.ofReal_inv, Complex.ofReal_natCast] using
    congrArg (fun x : ℝ => (x : ℂ)) (invSqrtDim_sq (d := d))

def maximallyEntangled (d : ℕ) : Ix d × Ix d → ℂ :=
  fun ij => if ij.1 = ij.2 then (invSqrtDim d : ℂ) else 0

def fourierVector (a : Ix d) : Ix d → ℂ :=
  fun j => (invSqrtDim d : ℂ) * chi (-(a*j))

def phasedVector (q : Ix d → ℂ) (a : Ix d) : Ix d → ℂ :=
  fun j => q j * fourierVector a j

/-- Column j is sent to row j+1, as in X|j>=|j+1>. -/
def weightedCycle (w : Ix d → ℂ) : Mat (Ix d) :=
  fun i j => if i = j+1 then w j else 0

def cyclicShift (d : ℕ) [NeZero d] : Mat (Ix d) := weightedCycle (fun _ => 1)

def entryConjugate {ι : Type*} (A : Mat ι) : Mat ι := fun i j => star (A i j)

theorem maximallyEntangled_normalized :
    ip (maximallyEntangled d) (maximallyEntangled d) = 1 := by
  have hd : (d : ℂ) ≠ 0 := by exact_mod_cast (NeZero.ne d)
  simp only [ip, maximallyEntangled, Fintype.sum_prod_type, apply_ite (star : ℂ → ℂ),
    star_zero, star_real, ite_mul, mul_ite, zero_mul, mul_zero]
  simp only [Finset.sum_ite_eq, Finset.sum_ite_eq', Finset.mem_univ, if_true]
  simp only [Finset.sum_const, Finset.card_univ, ZMod.card, nsmul_eq_mul]
  rw [← pow_two, invSqrtDim_complex_sq]
  exact mul_inv_cancel₀ hd

def entangledState (d : ℕ) [NeZero d] : StateOn (Ix d × Ix d) :=
  stateOnOfPure (maximallyEntangled d) maximallyEntangled_normalized

theorem fourierVector_orthonormal (a b : Ix d) :
    ip (fourierVector a) (fourierVector b) = if a=b then 1 else 0 := by
  have hd : (d : ℂ) ≠ 0 := by exact_mod_cast (NeZero.ne d)
  have he : ip (fourierVector a) (fourierVector b) =
      ((invSqrtDim d : ℂ))^2 * ∑ j, chi ((a-b)*j) := by
    simp only [ip, fourierVector, star_mul, star_real, chi_star, neg_neg,
      Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j _
    rw [sub_mul, chi_sub, chi_star]
    ring
  rw [he, invSqrtDim_complex_sq, character_sum]
  by_cases hab : a=b
  · simp [hab, hd]
  · simp [sub_ne_zero.mpr hab, hab]

theorem fourierVector_complete :
    (∑ a : Ix d, projector (fourierVector a)) = (1 : Mat (Ix d)) := by
  have hd : (d : ℂ) ≠ 0 := by exact_mod_cast (NeZero.ne d)
  ext i j
  have he : (∑ a : Ix d, projector (fourierVector a) i j) =
      ((invSqrtDim d : ℂ))^2 * ∑ a, chi ((j-i)*a) := by
    simp only [projector, fourierVector, star_mul, star_real,
      chi_star, neg_neg, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro a _
    rw [sub_mul, chi_sub, chi_star]
    have h₁ : a*i = i*a := mul_comm _ _
    have h₂ : a*j = j*a := mul_comm _ _
    rw [h₁, h₂]
    ring
  rw [Matrix.sum_apply]
  rw [he, invSqrtDim_complex_sq, character_sum]
  by_cases hij : i=j
  · simp [hij, Matrix.one_apply, hd]
  · simp [sub_ne_zero.mpr (Ne.symm hij), Matrix.one_apply, hij]

theorem phase_orthonormal (q : Ix d → ℂ) (hq : UnitPhases q) (a b : Ix d) :
    ip (phasedVector q a) (phasedVector q b) = if a=b then 1 else 0 := by
  calc
    ip (phasedVector q a) (phasedVector q b) = ip (fourierVector a) (fourierVector b) := by
      unfold ip phasedVector
      apply Finset.sum_congr rfl
      intro j _
      calc
        star (q j * fourierVector a j) * (q j * fourierVector b j) =
            (star (q j)*q j) * (star (fourierVector a j)*fourierVector b j) := by
          rw [star_mul]; ring
        _ = _ := by rw [hq j]; ring
    _ = _ := fourierVector_orthonormal a b

theorem phase_complete (q : Ix d → ℂ) (hq : UnitPhases q) :
    (∑ a, projector (phasedVector q a)) = (1 : Mat (Ix d)) := by
  ext i j
  have hu := congrFun (congrFun (fourierVector_complete (d := d)) i) j
  have he : (∑ a, projector (phasedVector q a) i j) =
      q i * star (q j) * (∑ a, projector (fourierVector a) i j) := by
    simp only [projector,phasedVector,star_mul,Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro a _
    ring
  rw [Matrix.sum_apply]
  rw [he]
  rw [Matrix.sum_apply] at hu
  rw [hu]
  by_cases hij : i=j
  · subst j
    simpa [Matrix.one_apply,mul_comm] using hq i
  · simp [Matrix.one_apply,hij]

def phaseMeasurement (q : Ix d → ℂ) (hq : UnitPhases q) : Measurement d (Ix d) :=
  measurementOfBasis (phasedVector q) (phase_orthonormal q hq) (phase_complete q hq)

def fourierMeasurement (d : ℕ) [NeZero d] : Measurement d (Ix d) :=
  measurementOfBasis fourierVector fourierVector_orthonormal fourierVector_complete

/-- Exact entrywise encoding, including the Fourier eigenvalue label. -/
theorem phase_encoded_entry (q : Ix d → ℂ) (hq : UnitPhases q) (i j : Ix d) :
    encoded (phaseMeasurement q hq) i j =
      if i=j+1 then q i * star (q j) else 0 := by
  have hd : (d : ℂ) ≠ 0 := by exact_mod_cast (NeZero.ne d)
  have he : encoded (phaseMeasurement q hq) i j =
      q i * star (q j) * ((invSqrtDim d : ℂ))^2 * ∑ a, chi ((1+j-i)*a) := by
    simp only [encoded,phaseMeasurement,measurementOfBasis,phasedVector,
      fourierVector,projector,Matrix.sum_apply,Finset.sum_apply,Matrix.smul_apply,smul_eq_mul,
      star_mul,star_real,chi_star,neg_neg,Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro a _
    have harg : (1+j-i)*a = a + -(a*i) + a*j := by ring
    rw [harg,chi_add,chi_add]
    ring
  rw [he,invSqrtDim_complex_sq,character_sum]
  have hz : (1+j-i : Ix d)=0 ↔ i=j+1 := by
    rw [sub_eq_zero]; exact ⟨fun h => h.symm.trans (add_comm _ _), fun h => (add_comm _ _).trans h.symm⟩
  by_cases hij : i=j+1
  · rw [if_pos (hz.mpr hij), if_pos hij]
    simp [hd,mul_assoc]
  · simp [mt hz.mp hij,hij]

/-- The cyclic recurrence is the only extra condition needed for encoding a
weighted shift. It will be constructed from product-one edge weights below. -/
theorem phaseMeasurement_encoding (q w : Ix d → ℂ) (hq : UnitPhases q)
    (hrec : ∀ j, q (j+1)=w j*q j) :
    encoded (phaseMeasurement q hq) = weightedCycle w := by
  ext i j
  rw [phase_encoded_entry]
  unfold weightedCycle
  by_cases hij : i=j+1
  · subst i
    simp only [if_pos rfl,hrec]
    calc
      w j*q j*star (q j) = w j*(star (q j)*q j) := by ring
      _ = w j := by rw [hq j]; ring
  · simp [hij]

theorem fourierMeasurement_encoding : encoded (fourierMeasurement d) = cyclicShift d := by
  have hq : UnitPhases (fun _ : Ix d => (1 : ℂ)) := by intro j; simp
  have he := phaseMeasurement_encoding (fun _ : Ix d => (1 : ℂ))
    (fun _ : Ix d => (1 : ℂ)) hq (by intro j; simp)
  have hv : phasedVector (fun _ : Ix d => (1 : ℂ)) = fourierVector := by
    funext a j; simp [phasedVector]
  simpa only [phaseMeasurement,fourierMeasurement,cyclicShift,
    measurementOfBasis,hv] using he

theorem basis_eigenvector (q : Ix d → ℂ) (hq : UnitPhases q) (a : Ix d) :
    applyOp (encoded (phaseMeasurement q hq)) (phasedVector q a) =
      fun j => chi a * phasedVector q a j := by
  funext i
  simp only [encoded,phaseMeasurement,measurementOfBasis,applyOp,
    Matrix.sum_apply,Finset.sum_apply,Matrix.smul_apply,smul_eq_mul,Finset.sum_mul]
  rw [Finset.sum_comm]
  have ht (b : Ix d) : (∑ j, (chi b * projector (phasedVector q b) i j) * phasedVector q a j) =
      chi b * phasedVector q b i * ip (phasedVector q b) (phasedVector q a) := by
    simp only [projector,ip,Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j _
    ring
  simp_rw [ht,phase_orthonormal q hq]
  simp

/-- The explicit vectors have norm one and distinct root labels, not unused outcomes. -/
theorem basis_vector_nonzero (q : Ix d → ℂ) (hq : UnitPhases q) (a : Ix d) :
    phasedVector q a ≠ 0 := by
  intro h
  have hn := phase_orthonormal q hq a a
  simp [h,ip] at hn

/-- Matrix-vector calculation fixes transpose, not adjoint, in vectorization. -/
theorem phi_apply (A B : Mat (Ix d)) (i k : Ix d) :
    applyOp (kron A B) (maximallyEntangled d) (i,k) =
      (invSqrtDim d : ℂ) * (A*B.transpose) i k := by
  simp only [applyOp,kron,maximallyEntangled,Fintype.sum_prod_type,
    mul_ite,mul_zero,Finset.sum_ite_eq, Finset.sum_ite_eq',Finset.mem_univ,if_true,
    Matrix.mul_apply,Matrix.transpose_apply,Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem phi_trace (A B : Mat (Ix d)) :
    expectation (maximallyEntangled d) (kron A B) =
      Matrix.trace (A*B.transpose)/(d : ℂ) := by
  unfold expectation ip
  simp only [Fintype.sum_prod_type,maximallyEntangled,apply_ite (star : ℂ → ℂ),star_zero,
    star_real,ite_mul,zero_mul,Finset.sum_ite_eq, Finset.sum_ite_eq',Finset.mem_univ,if_true]
  simp_rw [phi_apply]
  simp only [mul_assoc,← Finset.mul_sum]
  rw [← mul_assoc, ← pow_two,invSqrtDim_complex_sq]
  simp [Matrix.trace,Matrix.diag_apply,div_eq_mul_inv,mul_comm]

/-- Direct amplitude identity, BEFORE taking a modulus square. -/
theorem target_amplitude (q : Ix d → ℂ) (a b : Ix d) :
    ip (vectorTensor (phasedVector q a) (fourierVector b)) (maximallyEntangled d) =
      (invSqrtDim d : ℂ)^3 * star (fourier q (-(a+b))) := by
  simp only [ip,vectorTensor,maximallyEntangled,Fintype.sum_prod_type,
    mul_ite,mul_zero,Finset.sum_ite_eq, Finset.sum_ite_eq',Finset.mem_univ,if_true,
    phasedVector,fourierVector,star_mul,star_real,chi_star,neg_neg,
    fourier,star_sum,Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j _
  simp only [neg_mul,neg_neg,add_mul,chi_add]
  ring

/-- The manuscript's d^-3 Fourier table is derived from the density and PVMs. -/
theorem target_born_table (q : Ix d → ℂ) (hq : UnitPhases q) (a b : Ix d) :
    bornProbability (entangledState d).density ((phaseMeasurement q hq).effect a)
      ((fourierMeasurement d).effect b) = fourierTable q a b := by
  change bornProbability (projector (maximallyEntangled d))
    (projector (phasedVector q a)) (projector (fourierVector b)) = _
  rw [physical_rank_one_born,target_amplitude,Complex.normSq_mul,
    map_pow]
  change Complex.normSq (↑(invSqrtDim d) : ℂ) ^ 3 *
    Complex.normSq ((starRingEnd ℂ) (fourier q (-(a+b)))) = _
  rw [Complex.normSq_conj]
  have hn : Complex.normSq ((invSqrtDim d : ℂ)) = (d : ℝ)⁻¹ := by
    simpa [Complex.normSq_ofReal,pow_two] using invSqrtDim_sq (d := d)
  rw [hn]
  simp [fourierTable,powerSpectrum,div_eq_mul_inv,inv_pow,mul_comm]

/-- Complete distribution endpoint, independent of any Bell-optimality premise. -/
theorem target_distribution_package (q : Ix d → ℂ) (hq : UnitPhases q) :
    (∀ a b, bornProbability (entangledState d).density
      ((phaseMeasurement q hq).effect a) ((fourierMeasurement d).effect b) = fourierTable q a b) ∧
    (∑ a, ∑ b, fourierTable q a b) = 1 ∧
    (∀ a, (∑ b, fourierTable q a b) = 1/(d : ℝ)) ∧
    (∀ b, (∑ a, fourierTable q a b) = 1/(d : ℝ)) :=
  ⟨target_born_table q hq,table_normalized q hq,table_row_sum q hq,table_column_sum q hq⟩

/-- Product over natural representatives is the product over all residues. -/
theorem prod_representatives (f : Ix d → ℂ) :
    (∏ j ∈ Finset.range d, f (j : Ix d)) = ∏ j, f j := by
  classical
  refine Finset.prod_bij (fun j _ => (j : Ix d)) ?_ ?_ ?_ ?_
  · intro j hj; exact Finset.mem_univ _
  · intro i hi j hj hij
    have h := congrArg ZMod.val hij
    simpa [ZMod.val_natCast,Nat.mod_eq_of_lt (Finset.mem_range.mp hi),
      Nat.mod_eq_of_lt (Finset.mem_range.mp hj)] using h
  · intro j _
    exact ⟨j.val,Finset.mem_range.mpr (ZMod.val_lt j),ZMod.natCast_zmod_val j⟩
  · intro j _; rfl

def «prefix» (w : Ix d → ℂ) (j : Ix d) : ℂ := ∏ k ∈ Finset.range j.val, w (k : Ix d)

theorem phase_prod_unit (w : Ix d → ℂ) (hw : UnitPhases w) (s : Finset (Ix d)) :
    star (∏ j ∈ s, w j) * (∏ j ∈ s, w j) = 1 := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert j s hj ih =>
    rw [Finset.prod_insert hj,star_mul]
    calc
      (star (∏ k ∈ s,w k)*star (w j))*(w j*∏ k ∈ s,w k) =
          (star (w j)*w j)*(star (∏ k ∈ s,w k)*(∏ k ∈ s,w k)) := by ring
      _ = 1 := by rw [hw j,ih]; ring

theorem prefix_unit (w : Ix d → ℂ) (hw : UnitPhases w) : UnitPhases («prefix» w) := by
  intro j
  unfold «prefix»
  have h (r : ℕ) : star (∏ k ∈ Finset.range r,w (k : Ix d)) *
      (∏ k ∈ Finset.range r,w (k : Ix d)) = 1 := by
    induction r with
    | zero => simp
    | succ r ih =>
      rw [Finset.prod_range_succ,star_mul]
      calc
        (star (w (r : Ix d))*star (∏ k ∈ Finset.range r,w (k : Ix d))) *
            ((∏ k ∈ Finset.range r,w (k : Ix d))*w (r : Ix d)) =
          (star (∏ k ∈ Finset.range r,w (k : Ix d))*(∏ k ∈ Finset.range r,w (k : Ix d))) *
            (star (w (r : Ix d))*w (r : Ix d)) := by ring
        _ = 1 := by rw [ih,hw]; ring
  exact h j.val

@[simp] theorem prefix_zero (w : Ix d → ℂ) : «prefix» w 0 = 1 := by simp [«prefix»]

theorem successor_val (j : Ix d) : (j+1).val = (j.val+1)%d := by
  conv_lhs => rw [← ZMod.natCast_zmod_val j]
  rw [← Nat.cast_one,← Nat.cast_add,ZMod.val_natCast]

theorem prefix_recurrence (w : Ix d → ℂ) (hp : ∏ j, w j = 1) (j : Ix d) :
    «prefix» w (j+1) = w j * «prefix» w j := by
  have hj : j.val < d := ZMod.val_lt j
  by_cases hlt : j.val+1 < d
  · rw [«prefix»,successor_val,Nat.mod_eq_of_lt hlt,Finset.prod_range_succ]
    simp [«prefix»,ZMod.natCast_zmod_val,mul_comm]
  · have he : j.val+1=d := by omega
    have hfull := prod_representatives w
    rw [hp] at hfull
    have hrange : Finset.range d = Finset.range (j.val+1) := congrArg Finset.range he.symm
    rw [hrange,Finset.prod_range_succ,ZMod.natCast_zmod_val] at hfull
    rw [«prefix»,successor_val,he,Nat.mod_self]
    simp only [Finset.range_zero,Finset.prod_empty]
    simpa [«prefix»,mul_comm] using hfull.symm

def cycleMeasurement (w : Ix d → ℂ) (hw : UnitPhases w) (_hp : ∏ j,w j=1) :
    Measurement d (Ix d) := phaseMeasurement («prefix» w) (prefix_unit w hw)

theorem cycleMeasurement_encoding (w : Ix d → ℂ) (hw : UnitPhases w) (hp : ∏ j,w j=1) :
    encoded (cycleMeasurement w hw hp) = weightedCycle w :=
  phaseMeasurement_encoding («prefix» w) w (prefix_unit w hw) (prefix_recurrence w hp)

theorem weighted_order (w : Ix d → ℂ) (hw : UnitPhases w) (hp : ∏ j,w j=1) :
    weightedCycle w ^ d = 1 := by
  rw [← cycleMeasurement_encoding w hw hp]
  exact encoded_order _

theorem weighted_unitary (w : Ix d → ℂ) (hw : UnitPhases w) (hp : ∏ j,w j=1) :
    UnitaryRel (weightedCycle w) := by
  rw [← cycleMeasurement_encoding w hw hp]
  exact encoded_unitary _

theorem weighted_eigenbasis (w : Ix d → ℂ) (hw : UnitPhases w) (hp : ∏ j,w j=1) (a : Ix d) :
    applyOp (weightedCycle w) (phasedVector («prefix» w) a) =
      fun j => chi a * phasedVector («prefix» w) a j := by
  rw [← cycleMeasurement_encoding w hw hp]
  exact basis_eigenvector («prefix» w) (prefix_unit w hw) a

/-- A full physical family of d-outcome weighted-cycle measurements in every d. -/
theorem weighted_measurement_package (w : Ix d → ℂ) (hw : UnitPhases w) (hp : ∏ j,w j=1) :
    encoded (cycleMeasurement w hw hp) = weightedCycle w ∧
    UnitaryRel (weightedCycle w) ∧ weightedCycle w ^ d = 1 ∧
    (∀ a b, ip (phasedVector («prefix» w) a) (phasedVector («prefix» w) b) = if a=b then 1 else 0) ∧
    (∀ a, applyOp (weightedCycle w) (phasedVector («prefix» w) a) =
      fun j => chi a * phasedVector («prefix» w) a j) :=
  ⟨cycleMeasurement_encoding w hw hp,weighted_unitary w hw hp,weighted_order w hw hp,
    phase_orthonormal («prefix» w) (prefix_unit w hw),weighted_eigenbasis w hw hp⟩

end CyclicBell.General
