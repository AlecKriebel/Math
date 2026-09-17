import CyclicBell.GeneralPhases

/-! All-dimensional scalar extremum. The proof uses a centered cosine grid,
a telescoping sine identity, and reduction to a fundamental interval. This
checks the scalar step, not an operator/CFC transport theorem.  -/
noncomputable section
open scoped BigOperators
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

def halfMesh (d : ℕ) : ℝ := Real.pi / (2*d)
def mesh (d : ℕ) : ℝ := Real.pi / d
def scalarMaximum (d : ℕ) : ℝ := 2 / Real.sin (halfMesh d)
def cosineGrid (d : ℕ) (s : ℝ) : ℝ :=
  ∑ k ∈ Finset.range d, |Real.cos (s+(k : ℝ)*mesh d)|
def scalarSum (z : ℂ) : ℝ := ∑ y : Ix d, ‖1+chi y*z‖

theorem mesh_pos : 0<mesh d := div_pos Real.pi_pos dimension_pos

theorem halfMesh_pos : 0<halfMesh d := by
  unfold halfMesh
  exact div_pos Real.pi_pos (mul_pos (by norm_num) dimension_pos)

theorem sin_halfMesh_pos (hd : 2≤d) : 0<Real.sin (halfMesh d) := by
  apply Real.sin_pos_of_pos_of_lt_pi halfMesh_pos
  unfold halfMesh
  have hn : (1 : ℝ)<2*d := by exact_mod_cast (show 1<2*d by omega)
  exact div_lt_self Real.pi_pos hn

theorem halfMesh_eq : halfMesh d=mesh d/2 := by unfold halfMesh mesh; ring

theorem mesh_mul_dimension : (d : ℝ)*mesh d=Real.pi := by
  unfold mesh
  field_simp [ne_of_gt (dimension_pos (d := d))]

/-- Finite telescope, independent of trigonometry. -/
theorem sum_range_successor_sub (f : ℕ → ℝ) (n : ℕ) :
    (∑ k ∈ Finset.range n,(f (k+1)-f k))=f n-f 0 := by
  induction n with
  | zero => simp
  | succ n ih => rw [Finset.sum_range_succ,ih]; ring

theorem abs_cos_add_pi (x : ℝ) : |Real.cos (x+Real.pi)|=|Real.cos x| := by
  simp [Real.cos_add]

theorem cosineGrid_period (s : ℝ) : cosineGrid d (s+mesh d)=cosineGrid d s := by
  let f : ℕ → ℝ := fun k => |Real.cos (s+(k : ℝ)*mesh d)|
  have he : f d=f 0 := by
    dsimp [f]
    rw [mesh_mul_dimension]
    simpa using abs_cos_add_pi s
  have hs := sum_range_successor_sub f d
  rw [Finset.sum_sub_distrib,he,sub_self] at hs
  have hshift : cosineGrid d (s+mesh d)=∑ k ∈ Finset.range d,f (k+1) := by
    unfold cosineGrid
    apply Finset.sum_congr rfl
    intro k hk
    dsimp [f]
    congr 2
    push_cast
    ring
  rw [hshift]
  change (∑ k ∈ Finset.range d,f (k+1))=∑ k ∈ Finset.range d,f k
  linarith

theorem cosineGrid_nat_period (s : ℝ) (n : ℕ) :
    cosineGrid d (s+(n : ℝ)*mesh d)=cosineGrid d s := by
  induction n with
  | zero => simp
  | succ n ih =>
    have he : s+((n+1 : ℕ) : ℝ)*mesh d=(s+(n : ℝ)*mesh d)+mesh d := by
      push_cast; ring
    rw [he,cosineGrid_period,ih]

theorem cosineGrid_int_period (s : ℝ) (n : ℤ) :
    cosineGrid d (s+(n : ℝ)*mesh d)=cosineGrid d s := by
  cases n with
  | ofNat n => simpa using cosineGrid_nat_period s n
  | negSucc n =>
    have h := cosineGrid_nat_period (d := d) (s-((n+1 : ℕ) : ℝ)*mesh d) (n+1)
    have ha : s-((n+1 : ℕ) : ℝ)*mesh d+((n+1 : ℕ) : ℝ)*mesh d=s := by ring
    rw [ha] at h
    simpa only [Int.cast_negSucc,Nat.cast_add,Nat.cast_one,sub_eq_add_neg,neg_mul] using h.symm

/-- The centered mesh has no cosine sign changes inside the closed sector. -/
theorem centered_grid_nonnegative (hd : 2≤d) {t : ℝ}
    (ht : -halfMesh d≤t ∧ t≤halfMesh d) {k : ℕ} (hk : k<d) :
    0≤Real.cos (t-Real.pi/2+((k : ℝ)+1/2)*mesh d) := by
  apply Real.cos_nonneg_of_mem_Icc
  have hp := mesh_pos (d := d)
  have hm := mesh_mul_dimension (d := d)
  have hk0 : (0 : ℝ)≤k := Nat.cast_nonneg _
  have hk1 : (k : ℝ)+1≤d := by exact_mod_cast hk
  rw [halfMesh_eq] at ht
  constructor <;> nlinarith [mul_nonneg hk0 hp.le,
    mul_le_mul_of_nonneg_right hk1 hp.le]

/-- Exact finite trigonometric sum, by endpoint cancellation. -/
theorem centered_grid_sum (hd : 2≤d) (t : ℝ) :
    (∑ k ∈ Finset.range d,Real.cos (t-Real.pi/2+((k : ℝ)+1/2)*mesh d)) =
      Real.cos t / Real.sin (halfMesh d) := by
  let f : ℕ → ℝ := fun k => Real.sin (t-Real.pi/2+(k : ℝ)*mesh d)
  have step (k : ℕ) :
      2*Real.sin (halfMesh d)*Real.cos (t-Real.pi/2+((k : ℝ)+1/2)*mesh d) =
        f (k+1)-f k := by
    let x := t-Real.pi/2+((k : ℝ)+1/2)*mesh d
    have hplus : t-Real.pi/2+((k+1 : ℕ) : ℝ)*mesh d=x+halfMesh d := by
      dsimp [x]; rw [halfMesh_eq]; push_cast; ring
    have hminus : t-Real.pi/2+(k : ℝ)*mesh d=x-halfMesh d := by
      dsimp [x]; rw [halfMesh_eq]; ring
    dsimp [f]
    rw [hplus,hminus,Real.sin_add,Real.sin_sub]
    dsimp [x]
    ring
  have htel := sum_range_successor_sub f d
  have hend : f d-f 0=2*Real.cos t := by
    dsimp [f]
    rw [mesh_mul_dimension]
    have he : t-Real.pi/2+Real.pi=t+Real.pi/2 := by ring
    rw [he]
    simp [Real.sin_add,Real.sin_sub]
    ring
  rw [hend] at htel
  have hs : 2*Real.sin (halfMesh d)*
      (∑ k ∈ Finset.range d,Real.cos (t-Real.pi/2+((k : ℝ)+1/2)*mesh d)) =
      2*Real.cos t := by
    rw [Finset.mul_sum]
    simpa only [step] using htel
  apply (eq_div_iff (ne_of_gt (sin_halfMesh_pos hd))).mpr
  nlinarith

/-- One formula covers both parity branches after centering the grid. -/
theorem cosineGrid_sector (hd : 2≤d) {t : ℝ}
    (ht : -halfMesh d≤t ∧ t≤halfMesh d) :
    cosineGrid d (parityDelta d*mesh d/2+t)=Real.cos t/Real.sin (halfMesh d) := by
  obtain ⟨m,hm⟩ := parity_shift_even (d := d)
  have hs : parityDelta d*mesh d/2+t =
      (t-Real.pi/2+halfMesh d)+(m : ℝ)*mesh d := by
    have hmul := congrArg (fun r : ℝ => r*mesh d) hm
    dsimp only at hmul
    rw [halfMesh_eq]
    have hdim := mesh_mul_dimension (d := d)
    nlinarith
  rw [hs,cosineGrid_nat_period]
  unfold cosineGrid
  have he : (∑ k ∈ Finset.range d,
      |Real.cos (t-Real.pi/2+halfMesh d+(k : ℝ)*mesh d)|) =
      ∑ k ∈ Finset.range d,Real.cos (t-Real.pi/2+((k : ℝ)+1/2)*mesh d) := by
    apply Finset.sum_congr rfl
    intro k hk
    have ha : t-Real.pi/2+halfMesh d+(k : ℝ)*mesh d=
      t-Real.pi/2+((k : ℝ)+1/2)*mesh d := by rw [halfMesh_eq]; ring
    rw [ha,abs_of_nonneg (centered_grid_nonnegative hd ht (Finset.mem_range.mp hk))]
  rw [he,centered_grid_sum hd]

def sectorIndex (d : ℕ) (s : ℝ) : ℤ :=
  ⌊(s-parityDelta d*mesh d/2+halfMesh d)/mesh d⌋
def sectorOffset (d : ℕ) (s : ℝ) : ℝ :=
  s-parityDelta d*mesh d/2-(sectorIndex d s : ℝ)*mesh d

theorem sectorOffset_bounds (s : ℝ) :
    -halfMesh d≤sectorOffset d s ∧ sectorOffset d s<halfMesh d := by
  have hp := mesh_pos (d := d)
  have hlo := Int.floor_le ((s-parityDelta d*mesh d/2+halfMesh d)/mesh d)
  have hhi := Int.lt_floor_add_one ((s-parityDelta d*mesh d/2+halfMesh d)/mesh d)
  have hl : (sectorIndex d s : ℝ)*mesh d≤s-parityDelta d*mesh d/2+halfMesh d :=
    (le_div_iff₀ hp).mp hlo
  have hu : s-parityDelta d*mesh d/2+halfMesh d<((sectorIndex d s : ℝ)+1)*mesh d :=
    (div_lt_iff₀ hp).mp hhi
  unfold sectorOffset
  rw [halfMesh_eq] at *
  constructor <;> linarith

theorem cosineGrid_reduced (hd : 2≤d) (s : ℝ) :
    cosineGrid d s=Real.cos (sectorOffset d s)/Real.sin (halfMesh d) := by
  have hs : s=(parityDelta d*mesh d/2+sectorOffset d s)+(sectorIndex d s : ℝ)*mesh d := by
    unfold sectorOffset; ring
  conv_lhs => rw [hs]
  rw [cosineGrid_int_period]
  exact cosineGrid_sector hd ⟨(sectorOffset_bounds s).1,(sectorOffset_bounds s).2.le⟩

theorem cis_double_plus_one (t : ℝ) :
    1+cis (2*t)=(2*Real.cos t : ℂ)*cis t := by
  rw [show 2*t=t+t by ring,cis_add]
  simp only [cis_exp,Complex.exp_mul_I]
  apply Complex.ext <;>
    simp [Complex.mul_re,Complex.mul_im,Complex.cos_ofReal_re,Complex.sin_ofReal_re,Real.sin_sq_add_cos_sq] <;>
    nlinarith [Real.sin_sq_add_cos_sq t]

theorem norm_one_add_cis_double (t : ℝ) : ‖1+cis (2*t)‖=2*|Real.cos t| := by
  rw [cis_double_plus_one,norm_mul,cis_norm,mul_one]
  have he : (2 : ℂ)*(Real.cos t : ℂ) = ((2*Real.cos t : ℝ) : ℂ) := by push_cast; rfl
  rw [he, Complex.norm_real, Real.norm_eq_abs, abs_mul]
  norm_num

theorem sum_representatives {R : Type*} [AddCommMonoid R] (f : Ix d → R) :
    (∑ k ∈ Finset.range d,f (k : Ix d))=∑ k : Ix d,f k := by
  classical
  refine Finset.sum_bij (s := Finset.range d) (t := Finset.univ) (fun k _ => (k : Ix d)) ?_ ?_ ?_ ?_
  · intro k hk; simp
  · intro i hi j hj hij
    have h := congrArg ZMod.val hij
    simpa [ZMod.val_natCast,Nat.mod_eq_of_lt (Finset.mem_range.mp hi),
      Nat.mod_eq_of_lt (Finset.mem_range.mp hj)] using h
  · intro j hj
    refine ⟨j.val,Finset.mem_range.mpr (ZMod.val_lt j),?_⟩
    simp
  · intro k hk; rfl

theorem scalarSum_angle (s : ℝ) : scalarSum (d := d) (cis (2*s))=2*cosineGrid d s := by
  unfold scalarSum
  rw [← sum_representatives]
  have he (k : ℕ) : ‖1+chi (k : Ix d)*cis (2*s)‖=
      2*|Real.cos (s+(k : ℝ)*mesh d)| := by
    have hc : chi (k : Ix d)=cis (2*Real.pi*k/(d : ℝ)) := by
      simpa using chi_cis_int (d := d) (k : ℤ)
    rw [hc,← cis_add]
    have ha : 2*Real.pi*k/(d : ℝ)+2*s=2*(s+(k : ℝ)*mesh d) := by unfold mesh; ring
    rw [ha,norm_one_add_cis_double]
  simp_rw [he]
  rw [← Finset.mul_sum]
  rfl

/-- Sharp upper bound and exact equality test in the chosen angular sector. -/
theorem scalar_angle_bound (hd : 2≤d) (s : ℝ) :
    scalarSum (d := d) (cis (2*s))≤scalarMaximum d ∧
    (scalarSum (d := d) (cis (2*s))=scalarMaximum d ↔ sectorOffset d s=0) := by
  rw [scalarSum_angle,cosineGrid_reduced hd]
  have hp := sin_halfMesh_pos hd
  have hc := Real.cos_le_one (sectorOffset d s)
  have hb := sectorOffset_bounds (d := d) s
  have ha : halfMesh d<Real.pi := by
    unfold halfMesh
    exact div_lt_self Real.pi_pos (by exact_mod_cast (show 1<2*d by omega))
  have he := Real.cos_eq_one_iff_of_lt_of_lt
    (show -(2*Real.pi)<sectorOffset d s by linarith [Real.pi_pos])
    (show sectorOffset d s<2*Real.pi by linarith [Real.pi_pos])
  unfold scalarMaximum
  constructor
  · apply (le_div_iff₀ hp).mpr
    have hh : (2*(Real.cos (sectorOffset d s)/Real.sin (halfMesh d)))*Real.sin (halfMesh d)=
        2*Real.cos (sectorOffset d s) := by field_simp
    rw [hh]
    linarith
  · constructor
    · intro h
      apply he.mp
      have hh := congrArg (fun x : ℝ => x*Real.sin (halfMesh d)) h
      field_simp at hh
      linarith
    · intro h
      rw [h,Real.cos_zero]
      ring

/-- Actual unit-circle quantifier, not just the explicit equality roots. -/
theorem scalar_bound (hd : 2≤d) (z : ℂ) (hz : ‖z‖=1) :
    scalarSum (d := d) z≤scalarMaximum d := by
  let w : Circle := ⟨z,by change dist z 0 = 1; simpa only [dist_zero_right] using hz⟩
  have hw : cis (Complex.arg z)=z := congrArg (fun v : Circle => (v : ℂ)) (Circle.exp_arg w)
  have h := (scalar_angle_bound (d := d) hd (Complex.arg z/2)).1
  rw [show 2*(Complex.arg z/2)=Complex.arg z by ring,hw] at h
  exact h

/-- Each literal manuscript equality root attains the sharp scalar bound. -/
theorem equalityRoot_scalar_attainment (hd : 2≤d) (k : Ix d) :
    scalarSum (d := d) (equalityRoot k)=scalarMaximum d := by
  rw [equalityRoot_cis]
  have he : Real.pi*(2*k.val+parityDelta d)/(d : ℝ)=
      2*(parityDelta d*mesh d/2+(k.val : ℝ)*mesh d) := by unfold mesh; ring
  rw [he,scalarSum_angle,cosineGrid_nat_period]
  have ht : -halfMesh d≤(0 : ℝ) ∧ (0 : ℝ)≤halfMesh d := by
    constructor <;> linarith [halfMesh_pos (d := d)]
  have hg := cosineGrid_sector (d := d) hd ht
  simp only [add_zero, Real.cos_zero] at hg
  rw [hg]
  unfold scalarMaximum
  ring

@[simp] theorem cis_re (x : ℝ) : (cis x).re=Real.cos x := by
  simp [cis_exp,Complex.exp_mul_I,Complex.cos_ofReal_re]

theorem cis_eq_one_small {x : ℝ} (hx : -Real.pi≤x ∧ x≤Real.pi) :
    cis x=1 ↔ x=0 := by
  constructor
  · intro h
    have hr := congrArg Complex.re h
    simp only [cis_re,Complex.one_re] at hr
    apply (Real.cos_eq_one_iff_of_lt_of_lt
      (show -(2*Real.pi)<x by linarith [Real.pi_pos])
      (show x<2*Real.pi by linarith [Real.pi_pos])).mp hr
  · rintro rfl
    exact cis_zero

theorem parity_constant : cis (Real.pi*parityDelta d)=(-1 : ℂ)^(d-1) := by
  have hd0 : 0<d := NeZero.pos d
  by_cases he : Even d
  · obtain ⟨m,hm⟩ := he
    have hp : Even d := ⟨m,hm⟩
    have hn : d-1=2*(m-1)+1 := by omega
    rw [parityDelta,if_pos hp,Nat.cast_one,mul_one,cis_pi,hn,pow_add,pow_mul]
    simp
  · obtain ⟨m,hm⟩ := (Nat.even_or_odd d).resolve_left he
    have hn : d-1=2*m := by omega
    rw [parityDelta,if_neg he,Nat.cast_zero,mul_zero,cis_zero,hn,pow_mul]
    simp

/-- Power equation in the very same sector used to prove the scalar bound. -/
theorem sector_power_equation (s : ℝ) :
    cis (2*s)^d=cis (Real.pi*parityDelta d)*cis (2*d*sectorOffset d s) := by
  have he : (d : ℝ)*(2*s)=
      Real.pi*parityDelta d+2*d*sectorOffset d s+2*Real.pi*(sectorIndex d s : ℝ) := by
    unfold sectorOffset mesh
    field_simp [ne_of_gt (dimension_pos (d := d))]
    ring
  rw [cis_pow,he,cis_add,cis_period_int,mul_one,cis_add]

theorem sector_power_iff (hd : 2≤d) (s : ℝ) :
    cis (2*s)^d=(-1 : ℂ)^(d-1) ↔ sectorOffset d s=0 := by
  rw [sector_power_equation,← parity_constant]
  have hcancel : cis (Real.pi*parityDelta d)*cis (2*d*sectorOffset d s)=
      cis (Real.pi*parityDelta d) ↔ cis (2*d*sectorOffset d s)=1 := by
    constructor
    · intro h
      apply mul_left_cancel₀ (cis_ne_zero (Real.pi*parityDelta d))
      simpa using h
    · intro h
      rw [h,mul_one]
  rw [hcancel]
  have hb := sectorOffset_bounds (d := d) s
  have hp : 0<(2 : ℝ)*d := by positivity
  have hh : (2 : ℝ)*d*halfMesh d=Real.pi := by
    unfold halfMesh
    field_simp [ne_of_gt (dimension_pos (d := d))]
  have hr : -Real.pi≤2*d*sectorOffset d s ∧ 2*d*sectorOffset d s≤Real.pi := by
    constructor <;> nlinarith [mul_le_mul_of_nonneg_left hb.1 hp.le,
      mul_le_mul_of_nonneg_left hb.2.le hp.le]
  rw [cis_eq_one_small hr]
  exact mul_eq_zero.trans (or_iff_right (ne_of_gt hp))

/-- Full scalar equality characterization from lem:scalar in the manuscript. -/
theorem scalar_equality_iff (hd : 2≤d) (z : ℂ) (hz : ‖z‖=1) :
    scalarSum (d := d) z=scalarMaximum d ↔ z^d=(-1 : ℂ)^(d-1) := by
  let w : Circle := ⟨z,by change dist z 0 = 1; simpa only [dist_zero_right] using hz⟩
  have hw : cis (Complex.arg z)=z := congrArg (fun v : Circle => (v : ℂ)) (Circle.exp_arg w)
  have h := (scalar_angle_bound (d := d) hd (Complex.arg z/2)).2
  have hp := sector_power_iff (d := d) hd (Complex.arg z/2)
  rw [show 2*(Complex.arg z/2)=Complex.arg z by ring,hw] at h hp
  exact h.trans hp.symm

theorem equalityRoot_power (hd : 2≤d) (k : Ix d) :
    equalityRoot k ^ d=(-1 : ℂ)^(d-1) := by
  apply (scalar_equality_iff hd _ ?_).mp (equalityRoot_scalar_attainment hd k)
  rw [equalityRoot, norm_mul, equalityBase, cis_norm, chi_norm, mul_one]

/-- The phase polar denominators do not vanish on the scalar equality set. -/
theorem equalityRoot_no_bad_phase (hd : 2≤d) (y k : Ix d) :
    1+chi y*equalityRoot k≠0 := by
  have hm : chi y*equalityRoot k=equalityRoot (y+k) := by
    simp [equalityRoot,chi_add]
    ring
  intro h
  rw [hm] at h
  have he : equalityRoot (y+k)=(-1 : ℂ) := by linear_combination h
  have hp := equalityRoot_power hd (y+k)
  rw [he] at hp
  have hd' : d=(d-1)+1 := by omega
  have hpow : (-1 : ℂ)^d=-((-1 : ℂ)^(d-1)) := by
    conv_lhs => rw [hd']
    rw [pow_succ]
    ring
  rw [hpow] at hp
  have hn : (-1 : ℂ)^(d-1)≠0 := pow_ne_zero _ (by norm_num)
  apply hn
  linear_combination (-1/2 : ℂ)*hp

end CyclicBell.General
