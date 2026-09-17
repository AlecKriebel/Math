import CyclicBell.GeneralOperational
import CyclicBell.GeneralSupportAlgebra
import Mathlib.Algebra.BigOperators.Ring.Finset

/-! One-input nonsignalling locality and a pure, perfectly guessable realization.
Output types may depend on Bob's input. Zero-probability Alice outcomes are
handled explicitly; no conditional distribution divides by zero.
-/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {Y O : Type*} [Fintype Y] [Fintype O] [DecidableEq Y] [DecidableEq O]
variable {B : Y → Type*} [∀ y,Fintype (B y)] [∀ y,DecidableEq (B y)] [∀ y,Nonempty (B y)]

structure OneInputBehavior (Y O : Type*) [Fintype Y] [Fintype O]
    (B : Y → Type*) [∀ y,Fintype (B y)] where
  joint : (y : Y) → O → B y → ℝ
  marginal : O → ℝ
  nonnegative : ∀ y a b,0≤joint y a b
  marginal_nonnegative : ∀ a,0≤marginal a
  marginal_normalized : ∑ a,marginal a=1
  nonsignalling : ∀ y a,∑ b,joint y a b=marginal a

def oneConditional (p : OneInputBehavior Y O B) (y : Y) (a : O) (b : B y) : ℝ :=
  if p.marginal a=0 then (if b=Classical.choice (inferInstance : Nonempty (B y)) then 1 else 0)
  else p.joint y a b/p.marginal a

theorem oneConditional_nonnegative (p : OneInputBehavior Y O B) (y : Y) (a : O) (b : B y) :
    0≤oneConditional p y a b := by
  unfold oneConditional
  split_ifs <;> first | exact zero_le_one | exact le_refl 0 | exact div_nonneg (p.nonnegative y a b) (p.marginal_nonnegative a)

theorem oneConditional_normalized (p : OneInputBehavior Y O B) (y : Y) (a : O) :
    (∑ b,oneConditional p y a b)=1 := by
  by_cases h : p.marginal a=0
  · simp [oneConditional,h]
  · simp only [oneConditional,h,if_false,← Finset.sum_div,p.nonsignalling]
    exact div_self h

theorem zero_marginal_joint (p : OneInputBehavior Y O B) (y : Y) (a : O)
    (h : p.marginal a=0) (b : B y) : p.joint y a b=0 := by
  have hs : (∑ b,p.joint y a b)=0 := by rw [p.nonsignalling,h]
  exact (Finset.sum_eq_zero_iff_of_nonneg (fun b _ => p.nonnegative y a b)).mp hs b (Finset.mem_univ b)

theorem marginal_times_conditional (p : OneInputBehavior Y O B) (y : Y) (a : O) (b : B y) :
    p.marginal a*oneConditional p y a b=p.joint y a b := by
  by_cases h : p.marginal a=0
  · rw [h,zero_mul,zero_marginal_joint p y a h b]
  · simp [oneConditional,h,mul_div_cancel₀]

theorem dependent_product_normalization (r : (y : Y) → B y → ℝ)
    (hr : ∀ y,∑ b,r y b=1) : (∑ f : (∀ y,B y),∏ y,r y (f y))=1 := by
  have hp := Finset.prod_univ_sum (fun y => (Finset.univ : Finset (B y))) r
  simpa [hr] using hp.symm

/-- Explicit splitting of a dependent assignment into its y entry and all
remaining entries. This keeps finite-output alphabets genuinely input dependent. -/
def assignmentSplit (y : Y) : (∀ j,B j) ≃ B y × (∀ j : {j : Y // j≠y},B j.1) where
  toFun f := (f y,fun j => f j.1)
  invFun x j := if h : j=y then h.symm ▸ x.1 else x.2 ⟨j,h⟩
  left_inv f := by funext j; dsimp; split_ifs with h <;> subst_vars <;> rfl
  right_inv x := by
    rcases x with ⟨b,f⟩
    apply Prod.ext
    · simp
    · funext j; simp [j.2]

theorem assignment_product_split (r : (j : Y) → B j → ℝ) (f : ∀ j,B j) (y : Y) :
    (∏ j,r j (f j))=r y (f y)*∏ j : {j : Y // j≠y},r j.1 (f j.1) := by
  classical
  rw [← Finset.mul_prod_erase Finset.univ _ (Finset.mem_univ y)]
  congr 1
  exact Finset.prod_bij (fun j hj => ⟨j,by simpa using (Finset.mem_erase.mp hj).1⟩)
    (by simp) (by intro; simp_all) (by intro j _; exact ⟨j.1,by simp [j.2],rfl⟩) (by simp)

theorem dependent_product_marginal (r : (j : Y) → B j → ℝ)
    (hr : ∀ j,∑ b,r j b=1) (y : Y) (b : B y) :
    (∑ f : (∀ j,B j),(if f y=b then ∏ j,r j (f j) else 0))=r y b := by
  classical
  have hy (c : B y) (f : ∀ j : {j : Y // j≠y},B j.1) :
      (assignmentSplit (B := B) y).symm (c,f) y=c := by
    simp [assignmentSplit]
  have hj (c : B y) (f : ∀ j : {j : Y // j≠y},B j.1) (j : {j : Y // j≠y}) :
      (assignmentSplit (B := B) y).symm (c,f) j.1=f j := by
    simp [assignmentSplit,j.2]
  rw [← (assignmentSplit (B := B) y).symm.sum_comp]
  simp only [Fintype.sum_prod_type]
  simp_rw [assignment_product_split r _ y,hy,hj]
  rw [Finset.sum_eq_single b]
  · simp only [eq_self_iff_true,if_true]
    rw [← Finset.mul_sum]
    have hn := dependent_product_normalization (Y := {j : Y // j≠y})
      (B := fun j => B j.1) (fun j => r j.1) (fun j => hr j.1)
    simpa using congrArg (fun x : ℝ => r y b*x) hn
  · intro c _ hc
    simp [hc]
  · simp

abbrev StoredAssignments (O : Type*) {Y : Type*} (B : Y → Type*) := O × (∀ y,B y)

def hiddenWeight (p : OneInputBehavior Y O B) (label : StoredAssignments O B) : ℝ :=
  p.marginal label.1*∏ y,oneConditional p y label.1 (label.2 y)

theorem hiddenWeight_nonnegative (p : OneInputBehavior Y O B) (label : StoredAssignments O B) :
    0≤hiddenWeight p label :=
  mul_nonneg (p.marginal_nonnegative label.1)
    (Finset.prod_nonneg (fun y _ => oneConditional_nonnegative p y label.1 (label.2 y)))

theorem hiddenWeight_normalized (p : OneInputBehavior Y O B) : (∑ label,hiddenWeight p label)=1 := by
  simp only [hiddenWeight,Fintype.sum_prod_type,← Finset.mul_sum]
  simp_rw [dependent_product_normalization _ (fun y => oneConditional_normalized p y _),mul_one]
  exact p.marginal_normalized

/-- The complete nonsignalling behavior is represented by ONE shared hidden
variable, storing Bob's outputs at every input simultaneously. -/
theorem one_input_local (p : OneInputBehavior Y O B) (y : Y) (a : O) (b : B y) :
    (∑ label : StoredAssignments O B,if label.1=a ∧ label.2 y=b then hiddenWeight p label else 0)=p.joint y a b := by
  classical
  simp only [Fintype.sum_prod_type,hiddenWeight]
  rw [Finset.sum_eq_single a]
  · have he (f : ∀ j,B j) :
        (if f y=b then p.marginal a*∏ j,oneConditional p j a (f j) else 0)=
        p.marginal a*(if f y=b then ∏ j,oneConditional p j a (f j) else 0) := by split_ifs <;> simp_all
    simp only [eq_self_iff_true,true_and]
    simp_rw [he]
    rw [← Finset.mul_sum,dependent_product_marginal _ (fun j => oneConditional_normalized p j a),
      marginal_times_conditional]
  · intro a' _ ha'; simp [ha']
  · simp

/-! Pure quantum realization of any finite shared hidden variable. -/
variable {L Aout Bout : Type*} [Fintype L] [DecidableEq L]
  [Fintype Aout] [DecidableEq Aout] [Fintype Bout] [DecidableEq Bout]

def groupingProjector (f : L → Aout) (a : Aout) : Mat L :=
  Matrix.diagonal (fun label => if f label=a then 1 else 0)

theorem grouping_positive (f : L → Aout) (a : Aout) : (groupingProjector f a).PosSemidef := by
  apply Matrix.PosSemidef.diagonal
  intro label
  change (0 : ℂ) ≤ if f label=a then 1 else 0
  split_ifs <;> norm_num

theorem grouping_idempotent (f : L → Aout) (a : Aout) :
    groupingProjector f a*groupingProjector f a=groupingProjector f a := by
  rw [groupingProjector,Matrix.diagonal_mul_diagonal]
  apply congrArg Matrix.diagonal
  funext label
  dsimp only
  split_ifs <;> norm_num

theorem grouping_orthogonal (f : L → Aout) (a b : Aout) (hab : a≠b) :
    groupingProjector f a*groupingProjector f b=0 := by
  rw [groupingProjector,groupingProjector,Matrix.diagonal_mul_diagonal]
  ext label μ
  by_cases h : label=μ <;> simp [Matrix.diagonal_apply,h]
  aesop

theorem grouping_complete (f : L → Aout) : (∑ a,groupingProjector f a)=1 := by
  ext label μ
  by_cases h : label=μ <;> simp [groupingProjector,Matrix.diagonal_apply,h,Matrix.one_apply,Matrix.sum_apply]

/-- Coefficients of sum_lambda sqrt(mu_lambda)|lambda,lambda,lambda>. -/
def storedPurification (μ : L → ℝ) : Matrix (L×L) L ℂ :=
  fun ab e => if ab.1=ab.2 ∧ ab.1=e then (Real.sqrt (μ ab.1) : ℂ) else 0

theorem storedPurification_normalized (μ : L → ℝ) (hμ : ∀ label,0≤μ label)
    (hn : ∑ label,μ label=1) : frobeniusSq (storedPurification μ)=1 := by
  simp [frobeniusSq,storedPurification,Fintype.sum_prod_type,Complex.normSq_ofReal,
    Real.mul_self_sqrt,hμ,hn,apply_ite,ite_and]

theorem storedPurification_born (μ : L → ℝ) (hμ : ∀ label,0≤μ label)
    (fa : L → Aout) (fb : L → Bout) (a : Aout) (b : Bout) :
    bornProbability (storedPurification μ*(storedPurification μ).conjTranspose)
      (groupingProjector fa a) (groupingProjector fb b)=
      ∑ label,if fa label=a ∧ fb label=b then μ label else 0 := by
  unfold bornProbability stateEval
  simp only [Matrix.trace,Matrix.diag_apply,Matrix.mul_apply,Matrix.conjTranspose_apply,
    storedPurification,kron,groupingProjector,Matrix.diagonal_apply,Fintype.sum_prod_type]
  simp [Complex.mul_re,Complex.mul_im,Real.mul_self_sqrt,hμ,Finset.sum_ite_irrel,
    ← Finset.sum_add_distrib,apply_ite,ite_and]
  apply Finset.sum_congr rfl
  intro label _
  rw [Finset.sum_eq_single label]
  · split_ifs <;> simp_all
  · intro other _ hne
    simp [Ne.symm hne]
  · simp

/-- Eve's conditional matrix is diagonal on exactly the stored assignments
with the observed pair, so the grouping PVM guesses with certainty. -/
theorem storedPurification_conditional (μ : L → ℝ) (hμ : ∀ label,0≤μ label)
    (fa : L → Aout) (fb : L → Bout) (a : Aout) (b : Bout) :
    conditionalE (storedPurification μ) (kron (groupingProjector fa a) (groupingProjector fb b))=
      Matrix.diagonal (fun label => if fa label=a ∧ fb label=b then (μ label : ℂ) else 0) := by
  ext e f
  by_cases hef : e=f
  · subst f
    simp [conditionalE,reducedE,storedPurification,Matrix.mul_apply,Matrix.transpose_apply,
      Matrix.map_apply,groupingProjector,kron,Matrix.diagonal_apply,Fintype.sum_prod_type,
      Real.mul_self_sqrt,hμ,apply_ite,ite_and]
    split_ifs <;> simp_all [← Complex.ofReal_mul]
  · simp [conditionalE,reducedE,storedPurification,Matrix.mul_apply,Matrix.transpose_apply,
    Matrix.map_apply,groupingProjector,kron,Matrix.diagonal_apply,Fintype.sum_prod_type,
    Real.mul_self_sqrt,hμ,apply_ite,ite_and,hef,Ne.symm hef]

def storedEveGuess (fa : L → Aout) (fb : L → Bout) (a : Aout) (b : Bout) : Mat L :=
  groupingProjector (fun label => (fa label,fb label)) (a,b)

theorem storedEve_complete (fa : L → Aout) (fb : L → Bout) :
    (∑ a,∑ b,storedEveGuess fa fb a b)=1 := by
  simpa only [Fintype.sum_prod_type,storedEveGuess] using
    (grouping_complete (fun label => (fa label,fb label)))

theorem storedEve_success_one (μ : L → ℝ) (hμ : ∀ label,0≤μ label) (hn : ∑ label,μ label=1)
    (fa : L → Aout) (fb : L → Bout) :
    (∑ a,∑ b,(Matrix.trace (storedEveGuess fa fb a b*
      conditionalE (storedPurification μ) (kron (groupingProjector fa a) (groupingProjector fb b)))).re)=1 := by
  simp_rw [storedPurification_conditional μ hμ]
  unfold storedEveGuess groupingProjector
  simp only [Matrix.diagonal_mul_diagonal,Matrix.trace_diagonal,Complex.re_sum]
  rw [Finset.sum_comm]
  apply Eq.trans (Finset.sum_congr rfl (fun b _ => by rw [Finset.sum_comm]))
  rw [Finset.sum_comm]
  simpa [Prod.mk.injEq,ite_and,apply_ite] using hn

/-- Full one-input physical baseline, with positive normalized hidden weights,
an actual normalized PURE tripartite state, actual projectors (validated above),
full behavior reconstruction, and guessing success one at every Bob input. -/
theorem one_input_pure_projective_perfect_guess (p : OneInputBehavior Y O B) :
    frobeniusSq (storedPurification (hiddenWeight p))=1 ∧
    (∀ y a b,bornProbability
      (storedPurification (hiddenWeight p)*(storedPurification (hiddenWeight p)).conjTranspose)
      (groupingProjector (fun label : StoredAssignments O B => label.1) a)
      (groupingProjector (fun label : StoredAssignments O B => label.2 y) b)=p.joint y a b) ∧
    ∀ y,(∑ a,∑ b,(Matrix.trace
      (storedEveGuess (fun label : StoredAssignments O B => label.1) (fun label => label.2 y) a b*
        conditionalE (storedPurification (hiddenWeight p))
          (kron (groupingProjector (fun label : StoredAssignments O B => label.1) a)
            (groupingProjector (fun label : StoredAssignments O B => label.2 y) b)))).re)=1 := by
  refine ⟨storedPurification_normalized _ (hiddenWeight_nonnegative p) (hiddenWeight_normalized p),?_,?_⟩
  · intro y a b
    rw [storedPurification_born _ (hiddenWeight_nonnegative p),one_input_local]
  · intro y
    exact storedEve_success_one _ (hiddenWeight_nonnegative p) (hiddenWeight_normalized p) _ _

end CyclicBell.General
