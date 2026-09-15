import CyclicBell.GeneralWitness
import CyclicBell.GeneralPhases

/-!
# Fourier-phase measurements in the settings appendix

Uncompiled source candidates. These are actual PVMs and Born probabilities on
Phi_d. No Bell maximum, uniformity, or formula for the answer is a validity field.
Alice's vectors have negative Fourier sign; Bob's have positive Fourier sign.
The scalar displacement is a.val-b.val+alpha-beta, with ordinary integer lifts.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]

/-- Pointwise phase; real offsets need not be integral. -/
def offsetPhase (α : ℝ) (j : Ix d) : ℂ :=
  cis (-(2*Real.pi*α*(j.val : ℝ)/(d : ℝ)))

theorem offsetPhase_unit (α : ℝ) : UnitPhases (offsetPhase (d := d) α) := by
  intro j
  exact cis_unit _

/-- Outcome inversion, not matrix conjugation. -/
def negateMeasurement {ι : Type*} [Fintype ι] [DecidableEq ι]
    (M : Measurement d ι) : Measurement d ι where
  effect b := M.effect (-b)
  positive b := M.positive (-b)
  complete := by rw [sum_negate]; exact M.complete
  idempotent b := M.idempotent (-b)
  orthogonal a b hab := M.orthogonal (-a) (-b) (by simpa using hab)

def phaseAlice (α : ℝ) : Measurement d (Ix d) :=
  phaseMeasurement (offsetPhase α) (offsetPhase_unit α)

def phaseBob (β : ℝ) : Measurement d (Ix d) :=
  negateMeasurement (phaseMeasurement (offsetPhase (-β)) (offsetPhase_unit (-β)))

def offsetAliceVector (α : ℝ) (a : Ix d) : Ix d → ℂ :=
  phasedVector (offsetPhase α) a

def offsetBobVector (β : ℝ) (b : Ix d) : Ix d → ℂ :=
  phasedVector (offsetPhase (-β)) (-b)

def phasePairProbability (α β : ℝ) (a b : Ix d) : ℝ :=
  bornProbability (entangledState d).density
    ((phaseAlice α).effect a) ((phaseBob β).effect b)

def phaseGeometricSum (d : ℕ) (t : ℝ) : ℂ :=
  ∑ j ∈ Finset.range d, cis (2*Real.pi*t*(j : ℝ)/(d : ℝ))

def sineKernel (d : ℕ) (t : ℝ) : ℝ :=
  Real.sin (Real.pi*t)^2 / ((d : ℝ)^3*Real.sin (Real.pi*t/(d : ℝ))^2)

/-- Range-to-ZMod conversion kept local to this appendix so checking its tables
requires no scalar-extremum or Bell-upper-bound module. -/
theorem phase_sum_representatives {R : Type*} [AddCommMonoid R] (f : Ix d → R) :
    (∑ k ∈ Finset.range d,f (k : Ix d))=∑ k : Ix d,f k := by
  apply Finset.sum_bij (fun k _ => (k : Ix d))
  · intro k hk; simp
  · intro i hi j hj hij
    have h := congrArg ZMod.val hij
    simpa [ZMod.val_natCast,Nat.mod_eq_of_lt (Finset.mem_range.mp hi),
      Nat.mod_eq_of_lt (Finset.mem_range.mp hj)] using h
  · intro j hj
    refine ⟨j.val,Finset.mem_range.mpr (ZMod.val_lt j),?_⟩
    simp
  · intro k hk; rfl

/-- Character multiplication is done in ZMod, but t in the geometric sum uses
ordinary representatives. This lemma makes that distinction explicit. -/
theorem chi_product_representatives (a j : Ix d) :
    chi (a*j)=cis (2*Real.pi*(a.val : ℝ)*(j.val : ℝ)/(d : ℝ)) := by
  have hr : a*j=((a.val*j.val : ℕ) : Ix d) := by
    rw [Nat.cast_mul,ZMod.natCast_zmod_val,ZMod.natCast_zmod_val]
  rw [hr]
  have hc := chi_cis_int (d := d) (a.val*j.val : ℤ)
  simpa [Int.cast_mul,Int.cast_natCast,mul_assoc] using hc

theorem offsetAliceVector_formula (α : ℝ) (a j : Ix d) :
    offsetAliceVector α a j=(invSqrtDim d : ℂ)*
      cis (-(2*Real.pi*((a.val : ℝ)+α)*(j.val : ℝ)/(d : ℝ))) := by
  unfold offsetAliceVector phasedVector fourierVector offsetPhase
  have hc : chi (-(a*j))=cis (-(2*Real.pi*(a.val : ℝ)*(j.val : ℝ)/(d : ℝ))) := by
    rw [← chi_star,chi_product_representatives,← cis_neg]
  rw [hc]
  calc
    _=(invSqrtDim d : ℂ)*(cis (-(2*Real.pi*α*(j.val : ℝ)/(d : ℝ)))*
      cis (-(2*Real.pi*(a.val : ℝ)*(j.val : ℝ)/(d : ℝ)))) := by ring
    _=_ := by rw [← cis_add]; congr 2; ring

theorem offsetBobVector_formula (β : ℝ) (b j : Ix d) :
    offsetBobVector β b j=(invSqrtDim d : ℂ)*
      cis (2*Real.pi*((b.val : ℝ)+β)*(j.val : ℝ)/(d : ℝ)) := by
  unfold offsetBobVector phasedVector fourierVector offsetPhase
  rw [show -((-b)*j)=b*j by ring,chi_product_representatives]
  calc
    _=(invSqrtDim d : ℂ)*(cis (-(2*Real.pi*(-β)*(j.val : ℝ)/(d : ℝ)))*
      cis (2*Real.pi*(b.val : ℝ)*(j.val : ℝ)/(d : ℝ))) := by ring
    _=_ := by rw [← cis_add]; congr 2; ring

theorem phasePair_amplitude (α β : ℝ) (a b : Ix d) :
    ip (vectorTensor (offsetAliceVector α a) (offsetBobVector β b))
      (maximallyEntangled d)=
      (invSqrtDim d : ℂ)^3*
        phaseGeometricSum d ((a.val : ℝ)-(b.val : ℝ)+α-β) := by
  have ht (j : Ix d) : star (offsetAliceVector α a j*offsetBobVector β b j)*
      (invSqrtDim d : ℂ)=(invSqrtDim d : ℂ)^3*
        cis (2*Real.pi*((a.val : ℝ)-(b.val : ℝ)+α-β)*(j.val : ℝ)/(d : ℝ)) := by
    rw [offsetAliceVector_formula,offsetBobVector_formula]
    simp only [star_mul,star_real,← cis_neg]
    calc
      _=(invSqrtDim d : ℂ)^3*(cis (-(-(2*Real.pi*((a.val : ℝ)+α)*j.val/d)))*
          cis (-(2*Real.pi*((b.val : ℝ)+β)*j.val/d))) := by ring
      _=_ := by rw [← cis_add]; congr 2; ring
  simp only [ip,vectorTensor,maximallyEntangled,Fintype.sum_prod_type,
    mul_ite,mul_zero,Finset.sum_ite_eq',Finset.mem_univ,if_true,ht]
  rw [← Finset.mul_sum]
  congr 1
  unfold phaseGeometricSum
  rw [← phase_sum_representatives]
  apply Finset.sum_congr rfl
  intro j hj
  rw [ZMod.val_natCast,Nat.mod_eq_of_lt (Finset.mem_range.mp hj)]

theorem phasePair_from_geometric (α β : ℝ) (a b : Ix d) :
    phasePairProbability α β a b=
      Complex.normSq (phaseGeometricSum d ((a.val : ℝ)-(b.val : ℝ)+α-β))/(d : ℝ)^3 := by
  change bornProbability (projector (maximallyEntangled d))
    (projector (offsetAliceVector α a)) (projector (offsetBobVector β b))=_
  rw [physical_rank_one_born,phasePair_amplitude,Complex.normSq_mul,map_pow]
  have hn : Complex.normSq (invSqrtDim d : ℂ)=(d : ℝ)⁻¹ := by
    rw [Complex.normSq_ofReal,← pow_two,invSqrtDim_sq]
  rw [hn]
  ring

/-- A finite geometric identity, including the resonant case. -/
theorem phaseGeometric_telescoping (t : ℝ) :
    (1-cis (2*Real.pi*t/(d : ℝ)))*phaseGeometricSum d t=1-cis (2*Real.pi*t) := by
  let r := cis (2*Real.pi*t/(d : ℝ))
  have hs (n : ℕ) : (1-r)*(∑ j ∈ Finset.range n,r^j)=1-r^n := by
    induction n with
    | zero => simp
    | succ n ih => rw [Finset.sum_range_succ,mul_add,ih,pow_succ]; ring
  have hp (j : ℕ) : r^j=cis (2*Real.pi*t*(j : ℝ)/(d : ℝ)) := by
    dsimp [r]
    rw [cis_pow]
    congr 1
    ring
  have hlast : r^d=cis (2*Real.pi*t) := by
    rw [hp]
    congr 1
    field_simp [ne_of_gt (dimension_pos (d := d))]
  have h := hs d
  rw [hlast] at h
  simpa only [hp,r,phaseGeometricSum] using h

theorem normSq_one_sub_cis_double (x : ℝ) :
    Complex.normSq (1-cis (2*x))=4*Real.sin x^2 := by
  rw [Complex.normSq_apply]
  simp only [Complex.sub_re,Complex.sub_im,Complex.one_re,Complex.one_im,
    cis_exp,Complex.exp_mul_I,Complex.add_re,Complex.add_im,Complex.ofReal_re,
    Complex.ofReal_im,Complex.mul_re,Complex.mul_im,Complex.I_re,Complex.I_im]
  simp only [mul_zero,mul_one,zero_mul,sub_zero,add_zero,zero_add]
  nlinarith [Real.sin_sq_add_cos_sq (2*x),
    Real.sin_sq_add_cos_sq x,Real.cos_two_mul x]

/-- No division by a vanishing sine is used in this identity. -/
theorem phaseGeometric_squared_identity (t : ℝ) :
    Real.sin (Real.pi*t/(d : ℝ))^2*Complex.normSq (phaseGeometricSum d t)=
      Real.sin (Real.pi*t)^2 := by
  have h := congrArg Complex.normSq (phaseGeometric_telescoping (d := d) t)
  rw [Complex.normSq_mul] at h
  have hsmall : 2*Real.pi*t/(d : ℝ)=2*(Real.pi*t/(d : ℝ)) := by ring
  have hbig : 2*Real.pi*t=2*(Real.pi*t) := by ring
  rw [hsmall,hbig,normSq_one_sub_cis_double,normSq_one_sub_cis_double] at h
  linarith

/-- The literal appendix probability formula, derived from the physical PVMs. -/
theorem phasePair_sine_formula (α β : ℝ) (a b : Ix d)
    (hn : Real.sin (Real.pi*((a.val : ℝ)-(b.val : ℝ)+α-β)/(d : ℝ))≠0) :
    phasePairProbability α β a b=sineKernel d ((a.val : ℝ)-(b.val : ℝ)+α-β) := by
  rw [phasePair_from_geometric]
  have h := phaseGeometric_squared_identity (d := d)
    ((a.val : ℝ)-(b.val : ℝ)+α-β)
  have hg : Complex.normSq (phaseGeometricSum d ((a.val : ℝ)-(b.val : ℝ)+α-β))=
      Real.sin (Real.pi*((a.val : ℝ)-(b.val : ℝ)+α-β))^2/
        Real.sin (Real.pi*((a.val : ℝ)-(b.val : ℝ)+α-β)/(d : ℝ))^2 := by
    apply (eq_div_iff (pow_ne_zero 2 hn)).mpr
    simpa [mul_comm] using h
  rw [hg]
  unfold sineKernel
  ring

theorem phasePair_nonnegative (α β : ℝ) (a b : Ix d) :
    0≤phasePairProbability α β a b :=
  bornProbability_nonnegative (entangledState d) (phaseAlice α) (phaseBob β) a b

theorem phasePair_normalized (α β : ℝ) :
    (∑ a : Ix d,∑ b : Ix d,phasePairProbability α β a b)=1 :=
  bornProbability_normalized (entangledState d) (phaseAlice α) (phaseBob β)

/-- Uniform local marginals do not imply a uniform joint table. -/
theorem phasePair_marginals (α β : ℝ) :
    (∀ a : Ix d,(∑ b,phasePairProbability α β a b)=1/(d : ℝ)) ∧
    (∀ b : Ix d,(∑ a,phasePairProbability α β a b)=1/(d : ℝ)) := by
  have hm (v : Ix d → ℂ) (hv : ip v v=1) :
      stateEval (entangledState d).density (kron (projector v) 1)=1/(d : ℝ) ∧
      stateEval (entangledState d).density (kron 1 (projector v))=1/(d : ℝ) := by
    have ht : Matrix.trace (projector v)=1 := by
      simpa [Matrix.trace,Matrix.diag_apply,projector,ip,mul_comm] using hv
    constructor
    · change (Matrix.trace (projector (maximallyEntangled d)*kron (projector v) 1)).re=_
      rw [← expectation_eq_trace,phi_trace,Matrix.transpose_one,mul_one,ht]
      simp
    · change (Matrix.trace (projector (maximallyEntangled d)*kron 1 (projector v))).re=_
      rw [← expectation_eq_trace,phi_trace,one_mul,Matrix.trace_transpose,ht]
      simp
  constructor
  · intro a
    change (∑ b,bornProbability (entangledState d).density
      ((phaseAlice α).effect a) ((phaseBob β).effect b))=_
    rw [bornProbability_left_marginal]
    exact (hm (offsetAliceVector α a)
      (by simpa [offsetAliceVector] using phase_orthonormal (offsetPhase α) (offsetPhase_unit α) a a)).1
  · intro b
    change (∑ a,bornProbability (entangledState d).density
      ((phaseAlice α).effect a) ((phaseBob β).effect b))=_
    rw [bornProbability_right_marginal]
    exact (hm (offsetBobVector β b)
      (by simpa [offsetBobVector] using phase_orthonormal (offsetPhase (-β)) (offsetPhase_unit (-β)) (-b) (-b))).2

/-- Opposite local phases perfectly match the same basis at equal offsets. -/
theorem phasePair_equal_offsets (α : ℝ) (a b : Ix d) :
    phasePairProbability α α a b=if a=b then 1/(d : ℝ) else 0 := by
  have hg : phaseGeometricSum d ((a.val : ℝ)-(b.val : ℝ)+α-α)=
      ∑ j : Ix d,chi ((a-b)*j) := by
    unfold phaseGeometricSum
    rw [← phase_sum_representatives]
    apply Finset.sum_congr rfl
    intro j hj
    -- Avoid the representative of a-b: split the character before taking lifts.
    rw [sub_mul,chi_sub,chi_product_representatives,chi_product_representatives,← cis_neg,← cis_add]
    rw [ZMod.val_natCast,Nat.mod_eq_of_lt (Finset.mem_range.mp hj)]
    congr 1
    ring
  rw [phasePair_from_geometric,hg,character_sum]
  by_cases hab : a=b
  · simp [hab,Complex.normSq_ofReal]
    field_simp [ne_of_gt (dimension_pos (d := d))]
  · simp [hab,sub_ne_zero.mpr hab]

end CyclicBell.General
