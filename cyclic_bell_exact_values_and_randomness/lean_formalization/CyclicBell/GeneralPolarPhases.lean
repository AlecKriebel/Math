import CyclicBell.GeneralScalar
import CyclicBell.GeneralChirp

/-! Explicit half-angle phases for both families. Product-one admissibility
is proved, rather than included in a strategy definition. These phases are
identified with (1+omega^y z_k)/norm(1+omega^y z_k) including their signs.
UNCOMPILED SOURCE CANDIDATES. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def phaseCut (d : ℕ) : ℕ := d-d/2
def halfRootAngle (d : ℕ) (j : Ix d) : ℝ := Real.pi*(2*j.val+parityDelta d)/(2*d)
def halfRootSign (d : ℕ) (j : Ix d) : ℂ := if j.val<phaseCut d then 1 else -1
def polarBase (j : Ix d) : ℂ := halfRootSign d j*cis (halfRootAngle d j)
def polarPhase (y k : Ix d) : ℂ := polarBase (y+k)

theorem parity_half_dimension : (d : ℝ)-1+parityDelta d=2*(d/2 : ℕ) := by
  rcases Nat.even_or_odd d with he|ho
  · obtain ⟨m,hm⟩ := he
    have hp : Even d := ⟨m,hm⟩
    have hd : d=2*m := by omega
    have hdiv : d/2=m := by omega
    simp only [parityDelta,if_pos hp,Nat.cast_one,hdiv]
    have hc : (d : ℝ)=2*m := by exact_mod_cast hd
    linarith
  · obtain ⟨m,hm⟩ := ho
    have hp : ¬Even d := by rintro ⟨k,hk⟩; omega
    have hd : d=2*m+1 := by omega
    have hdiv : d/2=m := by omega
    simp only [parityDelta,if_neg hp,Nat.cast_zero,hdiv]
    have hc : (d : ℝ)=2*m+1 := by exact_mod_cast hd
    linarith

theorem phaseCut_formula : 2*(phaseCut d : ℝ)=(d : ℝ)+1-parityDelta d := by
  have hhalf := parity_half_dimension (d := d)
  have hle : d/2≤d := Nat.div_le_self _ _
  unfold phaseCut
  rw [Nat.cast_sub hle]
  linarith

theorem halfRootAngle_bounds (hd : 2≤d) (j : Ix d) :
    0≤halfRootAngle d j ∧ halfRootAngle d j<Real.pi := by
  have hj := ZMod.val_lt j
  have hδ := parityDelta_cases (d := d)
  have hn : 0≤(2*j.val+parityDelta d : ℝ) := by positivity
  have hlt : (2*j.val+parityDelta d : ℝ)<2*d := by
    rcases hδ with hδ|hδ <;> rw [hδ] <;> exact_mod_cast (by omega)
  constructor
  · exact div_nonneg (mul_nonneg Real.pi_pos.le hn) (by positivity)
  · apply (div_lt_iff₀ (by positivity : (0 : ℝ)<2*d)).mpr
    exact mul_lt_mul_of_pos_left hlt Real.pi_pos

theorem halfRootAngle_sides (j : Ix d) :
    (j.val<phaseCut d → halfRootAngle d j<Real.pi/2) ∧
    (¬j.val<phaseCut d → Real.pi/2<halfRootAngle d j) := by
  have hf := phaseCut_formula (d := d)
  have hdR : (0 : ℝ)<d := dimension_pos
  constructor
  · intro hj
    have hjR : (j.val : ℝ)+1≤phaseCut d := by exact_mod_cast hj
    unfold halfRootAngle
    apply (div_lt_iff₀ (by positivity : (0 : ℝ)<2*d)).mpr
    nlinarith [Real.pi_pos,mul_lt_mul_of_pos_left
      (show (2*j.val+parityDelta d : ℝ)<d by linarith) Real.pi_pos]
  · intro hj
    have hjR : (phaseCut d : ℝ)≤j.val := by exact_mod_cast (show phaseCut d≤j.val by omega)
    unfold halfRootAngle
    apply (lt_div_iff₀ (by positivity : (0 : ℝ)<2*d)).mpr
    nlinarith [Real.pi_pos,mul_lt_mul_of_pos_left
      (show (d : ℝ)<2*j.val+parityDelta d by linarith) Real.pi_pos]

theorem halfRoot_cos_sign (hd : 2≤d) (j : Ix d) :
    (j.val<phaseCut d → 0<Real.cos (halfRootAngle d j)) ∧
    (¬j.val<phaseCut d → Real.cos (halfRootAngle d j)<0) := by
  have hb := halfRootAngle_bounds hd j
  have hs := halfRootAngle_sides (d := d) j
  constructor
  · intro h
    have hc := Real.cos_lt_cos_of_nonneg_of_le_pi hb.1
      (show Real.pi/2≤Real.pi by linarith [Real.pi_pos]) (hs.1 h)
    simpa using hc
  · intro h
    have hc := Real.cos_lt_cos_of_nonneg_of_le_pi
      (show (0 : ℝ)≤Real.pi/2 by positivity) hb.2.le (hs.2 h)
    simpa using hc

theorem equalityRoot_halfAngle (j : Ix d) : equalityRoot j=cis (2*halfRootAngle d j) := by
  rw [equalityRoot_cis]
  congr 1
  unfold halfRootAngle
  ring

theorem polarBase_unit : UnitPhases (polarBase : Ix d → ℂ) := by
  intro j
  unfold polarBase halfRootSign
  split_ifs <;> simp [mul_assoc,cis_unit]

theorem polarPhase_unit (y : Ix d) : UnitPhases (polarPhase y : Ix d → ℂ) := by
  intro k
  exact polarBase_unit (y+k)

/-- The exact half-angle phase, rather than a numerical polar decomposition. -/
theorem polarBase_factor (hd : 2≤d) (j : Ix d) :
    polarBase j*(‖1+equalityRoot j‖ : ℂ)=1+equalityRoot j := by
  rw [equalityRoot_halfAngle,norm_one_add_cis_double,cis_double_plus_one]
  unfold polarBase halfRootSign
  by_cases hj : j.val<phaseCut d
  · rw [if_pos hj,abs_of_pos ((halfRoot_cos_sign hd j).1 hj)]
    push_cast
    ring
  · rw [if_neg hj,abs_of_neg ((halfRoot_cos_sign hd j).2 hj)]
    push_cast
    ring

theorem linear_at_root (y k : Ix d) :
    1+chi y*equalityRoot k=1+equalityRoot (y+k) := by
  simp only [equalityRoot,chi_add]
  ring

theorem polarPhase_factor (hd : 2≤d) (y k : Ix d) :
    polarPhase y k*(‖1+chi y*equalityRoot k‖ : ℂ)=1+chi y*equalityRoot k := by
  rw [linear_at_root]
  exact polarBase_factor hd (y+k)

theorem polarPhase_eq_quotient (hd : 2≤d) (y k : Ix d) :
    polarPhase y k=(1+chi y*equalityRoot k)/(‖1+chi y*equalityRoot k‖ : ℂ) := by
  apply (eq_div_iff ?_).mpr (polarPhase_factor hd y k)
  exact_mod_cast (norm_ne_zero_iff.mpr (equalityRoot_no_bad_phase hd y k))

/-- Unitarity gives the conjugated factor needed in the Phi trace. -/
theorem polarPhase_conjugate_factor (hd : 2≤d) (y k : Ix d) :
    (1+chi y*equalityRoot k)*star (polarPhase y k)=(‖1+chi y*equalityRoot k‖ : ℂ) := by
  rw [← polarPhase_factor hd y k]
  have hs := polarPhase_unit (d := d) y k
  calc
    (polarPhase y k*(‖1+chi y*equalityRoot k‖ : ℂ))*star (polarPhase y k) =
        (star (polarPhase y k)*polarPhase y k)*(‖1+chi y*equalityRoot k‖ : ℂ) := by ring
    _=_ := by rw [hs,one_mul]

theorem sum_natCast_range (n : ℕ) :
    (∑ k ∈ Finset.range n,(k : ℝ))=(n : ℝ)*((n : ℝ)-1)/2 := by
  induction n with
  | zero => simp
  | succ n ih => rw [Finset.sum_range_succ,ih]; push_cast; ring

theorem prod_cis_range (f : ℕ → ℝ) (n : ℕ) :
    (∏ k ∈ Finset.range n,cis (f k))=cis (∑ k ∈ Finset.range n,f k) := by
  induction n with
  | zero => simp
  | succ n ih => rw [Finset.prod_range_succ,Finset.sum_range_succ,ih,cis_add]

theorem prod_sign_range (n D : ℕ) (hn : n≤D) :
    (∏ k ∈ Finset.range D,(if k<n then (1 : ℂ) else -1))=(-1 : ℂ)^(D-n) := by
  have hd : D=n+(D-n) := by omega
  rw [hd,Finset.prod_range_add]
  have hp : (∏ k ∈ Finset.range n,(if k<n then (1 : ℂ) else -1))=1 := by
    apply Finset.prod_eq_one
    intro k hk
    rw [if_pos (Finset.mem_range.mp hk)]
  have hq : (∏ k ∈ Finset.range (D-n),(if n+k<n then (1 : ℂ) else -1))=(-1 : ℂ)^(D-n) := by
    simp [show ∀ k : ℕ,¬n+k<n by omega]
  rw [hp,one_mul,hq]
  congr 1
  omega

/-- Product one is an output of the arithmetic, not an assumed witness field. -/
theorem polarBase_product : (∏ j : Ix d,polarBase j)=1 := by
  have hn : phaseCut d≤d := Nat.sub_le _ _
  have hc : d-phaseCut d=d/2 := by unfold phaseCut; omega
  rw [← prod_representatives]
  have he (k : ℕ) (hk : k<d) : polarBase (k : Ix d)=
      (if k<phaseCut d then (1 : ℂ) else -1)*
        cis (Real.pi*(2*(k : ℝ)+parityDelta d)/(2*d)) := by
    simp [polarBase,halfRootSign,halfRootAngle,ZMod.val_natCast,Nat.mod_eq_of_lt hk]
  rw [Finset.prod_congr rfl (fun k hk => he k (Finset.mem_range.mp hk)),Finset.prod_mul_distrib,
    prod_sign_range _ _ hn,prod_cis_range]
  have hsum : (∑ k ∈ Finset.range d,Real.pi*(2*(k : ℝ)+parityDelta d)/(2*d))=
      Real.pi*(d/2 : ℕ) := by
    simp only [mul_add,add_div,Finset.sum_add_distrib,← Finset.mul_sum,← Finset.sum_div]
    rw [sum_natCast_range]
    simp only [Finset.sum_const,Finset.card_range,nsmul_eq_mul]
    have hh := parity_half_dimension (d := d)
    field_simp [ne_of_gt (dimension_pos (d := d))]
    linear_combination Real.pi*(d : ℝ)*hh
  rw [hsum,hc]
  have hcis : cis (Real.pi*(d/2 : ℕ))=(-1 : ℂ)^(d/2) := by
    rw [← cis_pi, cis_pow]
    congr 1
    ring
  rw [hcis,← pow_add]
  have hn2 : d/2+d/2=2*(d/2) := by omega
  rw [hn2,pow_mul]
  simp

theorem polarPhase_product (y : Ix d) : (∏ k : Ix d,polarPhase y k)=1 := by
  unfold polarPhase
  have h := Fintype.prod_equiv (Equiv.addLeft y) polarBase polarBase (fun _ => rfl)
  exact h.trans polarBase_product

/-- The half-angle sign computation also fixes the adjacent reflection label.
This is the scalar input to the later supported-multiplicity argument. -/
def reflectionLabel (d : ℕ) [NeZero d] : Ix d := ((phaseCut d-1 : ℕ) : Ix d)

end CyclicBell.General
