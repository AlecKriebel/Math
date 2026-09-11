import Bell.Purification

/-!
# Finite positive qubit measurements: boundaries and small perturbations

All statements use the actual complex PSD cone. A zero-trace PSD effect is
zero, rank-one boundaries are exposed rays, and Hermitian perturbations of a
strictly positive operator remain positive in a two-sided neighborhood.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder Topology
open Filter Set
namespace Bell
open QubitGeometry Lorentz

theorem positive_sum {ι n : Type*} [Fintype ι] [Fintype n]
    (A : ι → Matrix n n ℂ) (hA : ∀ i, (A i).PosSemidef) : (∑ i, A i).PosSemidef := by
  classical
  have hsum (s : Finset ι) : (∑ i ∈ s, A i).PosSemidef := by
    induction s using Finset.induction_on with
    | empty => simpa using (Matrix.PosSemidef.zero : (0 : Matrix n n ℂ).PosSemidef)
    | @insert i s hi ih => simpa [hi] using (hA i).add ih
  exact hsum Finset.univ

theorem positive_coordinates {A : Operator} (hA : A.PosSemidef) : Future (coordinates A) := by
  rw [← pauli_posSemidef_iff, pauli_coordinates hA.isHermitian]
  exact hA

theorem positive_trace_zero_iff {A : Operator} (hA : A.PosSemidef) :
    (Matrix.trace A).re = 0 ↔ A = 0 := by
  constructor
  · intro h
    have ht : (coordinates A) 0 = 0 := by
      have he := pauli_trace (coordinates A)
      rw [pauli_coordinates hA.isHermitian] at he
      have her := congrArg Complex.re he
      simp only [Complex.ofReal_re] at her
      linarith
    have hc := future_time_zero (positive_coordinates hA) ht
    rw [← pauli_coordinates hA.isHermitian, hc, map_zero]
  · rintro rfl
    simp

theorem positive_trace_positive {A : Operator} (hA : A.PosSemidef) (hne : A ≠ 0) :
    0 < (Matrix.trace A).re :=
  lt_of_le_of_ne (positive_trace_nonneg hA) (Ne.symm fun h => hne ((positive_trace_zero_iff hA).mp h))

theorem positive_null_coordinates {A : Operator} (hA : A.PosSemidef)
    (hne : A ≠ 0) (hdet : A.det = 0) : FutureNull (coordinates A) := by
  refine ⟨future_nonzero_time (positive_coordinates hA) ?_, ?_⟩
  · intro hc
    apply hne
    rw [← pauli_coordinates hA.isHermitian, hc, map_zero]
  · have hd := pauli_det (coordinates A)
    rw [pauli_coordinates hA.isHermitian, hdet] at hd
    exact_mod_cast hd.symm

theorem positive_definite_coordinates {A : Operator} (hA : A.PosDef) :
    FutureTimelike (coordinates A) := by
  refine ⟨future_nonzero_time (positive_coordinates hA.posSemidef) ?_, ?_⟩
  · intro hc
    have hzero : A = 0 := by rw [← pauli_coordinates hA.isHermitian, hc, map_zero]
    have hdet := hA.det_pos
    simp [hzero] at hdet
  · have hd := pauli_det (coordinates A)
    rw [pauli_coordinates hA.isHermitian] at hd
    have hpos := hA.det_pos
    rw [hd] at hpos
    exact_mod_cast hpos

theorem isOpen_futureTimelike : IsOpen {x : V | FutureTimelike x} := by
  exact (isOpen_lt continuous_const (continuous_apply 0)).inter
    (isOpen_lt continuous_const (show Continuous lorentzSquare by
      unfold lorentzSquare; fun_prop))

theorem eventually_positive_perturbation {A H : Operator}
    (hA : A.PosDef) (hH : H.IsHermitian) :
    ∀ᶠ t : ℝ in 𝓝 0, (A + t • H).PosDef := by
  have ht : Continuous (fun t : ℝ => coordinates A + t • coordinates H) := by fun_prop
  have he := (ht.continuousAt (x := 0)).preimage_mem_nhds
    (isOpen_futureTimelike.mem_nhds (by simpa using positive_definite_coordinates hA))
  filter_upwards [he] with t ht
  have hp := FutureTimelike.posDef ht
  simpa [map_add, map_smul, pauli_coordinates hA.isHermitian, pauli_coordinates hH] using hp

/-- Finite coefficient perturbations can be made positive simultaneously. -/
theorem exists_positive_perturbation {ι : Type*} [Fintype ι]
    (c : ι → ℝ) {A H : Operator} (hA : A.PosDef) (hH : H.IsHermitian) :
    ∃ ε : ℝ, 0 < ε ∧ (A + ε • H).PosDef ∧ (A - ε • H).PosDef ∧
      ∀ i, 0 < 1 + ε*c i ∧ 0 < 1 - ε*c i := by
  have hp := eventually_positive_perturbation hA hH
  have hm : ∀ᶠ t : ℝ in 𝓝 0, (A - t • H).PosDef := by
    have hc : Tendsto (fun t : ℝ => -t) (𝓝 0) (𝓝 0) := by
      simpa using (continuous_neg.continuousAt (x := (0 : ℝ))).tendsto
    simpa [sub_eq_add_neg, neg_smul] using hc.eventually hp
  have hw : ∀ᶠ t : ℝ in 𝓝 0, ∀ i, 0 < 1+t*c i ∧ 0 < 1-t*c i := by
    apply Filter.eventually_all.mpr
    intro i
    have hp : ∀ᶠ t : ℝ in 𝓝 0, 0 < 1+t*c i :=
      (show ContinuousAt (fun t : ℝ => 1+t*c i) 0 by fun_prop).eventually (Ioi_mem_nhds (by norm_num))
    have hm : ∀ᶠ t : ℝ in 𝓝 0, 0 < 1-t*c i :=
      (show ContinuousAt (fun t : ℝ => 1-t*c i) 0 by fun_prop).eventually (Ioi_mem_nhds (by norm_num))
    exact hp.and hm

  have hpos : ∀ᶠ t : ℝ in 𝓝[>] 0, 0 < t := self_mem_nhdsWithin
  obtain ⟨ε, hε, hpε, hmε, hwε⟩ :=
    (hpos.and ((hp.and (hm.and hw)).filter_mono nhdsWithin_le_nhds)).exists
  exact ⟨ε, hε, hpε, hmε, hwε⟩

/-- Cayley-Hamilton specialized to two by two matrices, proved entrywise. -/
theorem qubit_cayley_hamilton_entrywise (A : Operator) :
    A*A - Matrix.trace A • A + A.det • (1 : Operator) = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Matrix.trace, Matrix.det_fin_two, Fin.sum_univ_succ,
      Matrix.one_apply, smul_eq_mul] <;> ring

theorem determinant_complement (A : Operator) : (1-A).det = 1 - Matrix.trace A + A.det := by
  simp [Matrix.det_fin_two, Matrix.trace, Fin.sum_univ_succ, Matrix.one_apply]
  ring

/-- A binary rank-one resolution of the identity is projective. -/
theorem rank_one_binary_projector {A B : Operator} (hA : A.PosSemidef)
    (hB : B.PosSemidef) (hsum : A+B = 1) (hAd : A.det = 0) (hBd : B.det = 0) :
    A*A = A ∧ B*B = B ∧ A*B = 0 ∧ B*A = 0 := by
  have hBval : B = 1-A := by rw [← hsum]; abel
  have htA : Matrix.trace A = 1 := by
    have he := determinant_complement A
    rw [← hBval, hBd, hAd] at he
    linear_combination he
  have htB : Matrix.trace B = 1 := by
    have he := congrArg Matrix.trace hsum
    simp [Matrix.trace_add, Matrix.trace_one, htA] at he
    linear_combination he
  have hAA : A*A = A := by
    have he := qubit_cayley_hamilton_entrywise A
    exact sub_eq_zero.mp (by simpa [htA, hAd] using he)
  have hBB : B*B = B := by
    have he := qubit_cayley_hamilton_entrywise B
    exact sub_eq_zero.mp (by simpa [htB, hBd] using he)
  refine ⟨hAA, hBB, ?_, ?_⟩ <;> rw [hBval] <;> simp [mul_sub, sub_mul, hAA]

/-- Any nonnegative decomposition of a nonzero null cone vector stays on its
exposed ray. No output is assumed nonzero. -/
theorem future_between_null {x y : V} (hx : FutureNull x)
    (hy : Future y) (hxy : Future (x-y)) :
    y = (y 0 / x 0) • x := by
  have hpx := future_pair_nonnegative hy hxy
  have hqsum : lorentzSquare x = lorentzSquare y + lorentzSquare (x-y) +
      2*lorentzPair y (x-y) := by
    unfold lorentzSquare lorentzPair
    simp only [Pi.sub_apply]
    ring
  have hyq : lorentzSquare y = 0 := by nlinarith [hx.2, hy.2, hxy.2]
  have hpair : lorentzPair y x = 0 := by
    have he : lorentzPair y x = lorentzSquare y + lorentzPair y (x-y) := by
      unfold lorentzSquare lorentzPair
      simp only [Pi.sub_apply]
      ring
    nlinarith [hx.2, hy.2, hxy.2, hqsum]
  by_cases hz : y = 0
  · simp [hz]
  · have hyt := future_nonzero_time hy hz
    obtain ⟨t, ht, hty⟩ := null_pair_zero_sameRay ⟨hyt, hyq⟩ hx hpair
    have htval : t = y 0/x 0 := by
      have he := congrFun hty 0
      simp only [Pi.smul_apply, smul_eq_mul] at he
      apply (eq_div_iff hx.1.ne').mpr
      exact he.symm
    simpa [htval] using hty

theorem positive_below_rank_one {A B : Operator} (hA : A.PosSemidef)
    (hAn : A ≠ 0) (hAd : A.det = 0) (hB : B.PosSemidef) (hAB : (A-B).PosSemidef) :
    B = ((Matrix.trace B).re / (Matrix.trace A).re) • A := by
  have he := future_between_null (positive_null_coordinates hA hAn hAd)
    (positive_coordinates hB) (by simpa using positive_coordinates hAB)
  have hp := congrArg pauli he
  rw [map_smul, pauli_coordinates hB.isHermitian, pauli_coordinates hA.isHermitian] at hp
  convert hp using 2
  have hta := congrArg Complex.re (pauli_trace (coordinates A))
  have htb := congrArg Complex.re (pauli_trace (coordinates B))
  rw [pauli_coordinates hA.isHermitian] at hta
  rw [pauli_coordinates hB.isHermitian] at htb
  simp only [Complex.ofReal_re] at hta htb
  rw [hta, htb]
  ring

/-- Off-diagonal complement in a complete measurement is positive. -/
theorem POVM.complement_positive {n : ℕ} (M : POVM n) (a : Fin n) :
    (1-M.effect a).PosSemidef := by
  classical
  have hsum : (∑ b : {b : Fin n // b ≠ a}, M.effect b) = 1-M.effect a := by
    have he := Fintype.sum_eq_add_sum_subtype_ne M.effect a
    rw [M.normalized] at he
    rw [he]
    abel
  rw [← hsum]
  exact positive_sum _ fun b => M.positive b

/-- A POVM with at most two nonzero rank-one effects is a PVM with precisely
its declared labels, including unused zero projectors. -/
def POVM.toPVMOfTwoNull {n : ℕ} (M : POVM n)
    (hnull : ∀ a, (M.effect a).det = 0)
    (hcard : (Finset.univ.filter (fun a => M.effect a ≠ 0)).card ≤ 2) : PVM n := by
  classical
  have hprops : (∀ a, M.effect a * M.effect a = M.effect a) ∧
      (∀ a b, a ≠ b → M.effect a * M.effect b = 0) := by
    classical
    let t := Finset.univ.filter (fun a => M.effect a ≠ 0)
    have hsum : ∑ a ∈ t, M.effect a = 1 := by
      have hi (a : Fin n) : (if M.effect a ≠ 0 then M.effect a else 0) = M.effect a := by
        split_ifs with h <;> simp_all
      simpa only [t, Finset.sum_filter, hi] using M.normalized
    have hne : t.Nonempty := by
      apply Finset.nonempty_iff_ne_empty.mpr
      intro he
      have hc := congrArg (fun A : Operator => A 0 0) hsum
      simp [he] at hc
    obtain ⟨a, ha⟩ := hne
    have hsecond : (t.erase a).Nonempty := by
      apply Finset.nonempty_iff_ne_empty.mpr
      intro he
      have ht : t = {a} := by simpa [he] using (Finset.insert_erase ha).symm
      have hA : M.effect a = 1 := by simpa [ht] using hsum
      have hc := hnull a
      simp [hA] at hc
    obtain ⟨b, hb⟩ := hsecond
    have hba : b ≠ a := (Finset.mem_erase.mp hb).1
    have hbt : b ∈ t := (Finset.mem_erase.mp hb).2
    have ht : t = {a,b} := by
      symm
      apply Finset.eq_of_subset_of_card_le
      · exact Finset.insert_subset ha (Finset.singleton_subset_iff.mpr hbt)
      · simpa [hba, Ne.symm hba] using hcard
    have hAB : M.effect a + M.effect b = 1 := by simpa [ht, hba, Ne.symm hba] using hsum
    obtain ⟨haa,hbb,hab,hba'⟩ := rank_one_binary_projector (M.positive a) (M.positive b)
      hAB (hnull a) (hnull b)
    have hz : ∀ c, c ≠ a → c ≠ b → M.effect c = 0 := by
      intro c hca hcb
      by_contra hn
      have hc : c ∈ t := Finset.mem_filter.mpr ⟨Finset.mem_univ c, hn⟩
      simp [ht, hca, hcb] at hc
    constructor
    · intro c
      by_cases hca : c=a
      · simpa [hca] using haa
      by_cases hcb : c=b
      · simpa [hcb] using hbb
      simp [hz c hca hcb]
    · intro c d hcd
      by_cases hca : c=a <;> by_cases hcb : c=b <;>
        by_cases hda : d=a <;> by_cases hdb : d=b <;>
        simp_all [hz]
  exact ⟨M, hprops.1, hprops.2⟩

/-- Strictly positive real scaling preserves positive definiteness. -/
theorem posDef_real_smul {A : Operator} (hA : A.PosDef) {t : ℝ} (ht : 0 < t) :
    (t • A).PosDef := by
  apply posDef_of_posSemidef_det_ne_zero (posSemidef_real_smul hA.posSemidef ht.le)
  rw [show t • A = (t : ℂ) • A from rfl, Matrix.det_smul]
  exact mul_ne_zero (pow_ne_zero _ (by exact_mod_cast ht.ne')) hA.det_pos.ne'

end Bell
