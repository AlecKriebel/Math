import Bell.EntrywiseTopology
import Bell.FiniteConvexCompactness
import Bell.Purification

/-!
# Compactness and extreme maximizing behaviors in the actual quantum model

The parameter space uses Gram FACTORS, not an unproved closedness theorem for
PSD matrices. Normalization bounds the squared norm of every Gram entry, and
all constraints are polynomial. Thus raw images and their ordinary convex
hulls are compact for every fixed finite architecture, including empty cases.
-/
noncomputable section
open Set
open scoped BigOperators Matrix ComplexOrder Topology Bell.Entrywise
namespace Bell

abbrev GramData (A : Architecture) := JointOperator ×
  (((x : Fin A.aliceInputs) → Fin (A.aliceOutputs x) → Operator) ×
   ((y : Fin A.bobInputs) → Fin (A.bobOutputs y) → Operator))

def gramMatrix {n : Type*} [Fintype n] (B : Matrix n n ℂ) : Matrix n n ℂ :=
  B.conjTranspose * B

def GramValid (A : Architecture) (d : GramData A) : Prop :=
  Matrix.trace (gramMatrix d.1) = 1 ∧
  (∀ x, ∑ a, gramMatrix (d.2.1 x a) = 1) ∧
  (∀ y, ∑ b, gramMatrix (d.2.2 y b) = 1)

def GramProjective (A : Architecture) (d : GramData A) : Prop :=
  GramValid A d ∧
  (∀ x a, gramMatrix (d.2.1 x a) * gramMatrix (d.2.1 x a) = gramMatrix (d.2.1 x a)) ∧
  (∀ x a b, a ≠ b → gramMatrix (d.2.1 x a) * gramMatrix (d.2.1 x b) = 0) ∧
  (∀ y b, gramMatrix (d.2.2 y b) * gramMatrix (d.2.2 y b) = gramMatrix (d.2.2 y b)) ∧
  (∀ y a b, a ≠ b → gramMatrix (d.2.2 y a) * gramMatrix (d.2.2 y b) = 0)

def gramBehavior (A : Architecture) (d : GramData A) : Behavior A :=
  fun x y a b => born (gramMatrix d.1) (gramMatrix (d.2.1 x a)) (gramMatrix (d.2.2 y b))

def gramStrategy (A : Architecture) (d : GramData A) (hd : GramValid A d) : Strategy A where
  state := ⟨gramMatrix d.1, Matrix.posSemidef_conjTranspose_mul_self _, hd.1⟩
  alice := fun x => ⟨fun a => gramMatrix (d.2.1 x a),
    fun _ => Matrix.posSemidef_conjTranspose_mul_self _, hd.2.1 x⟩
  bob := fun y => ⟨fun b => gramMatrix (d.2.2 y b),
    fun _ => Matrix.posSemidef_conjTranspose_mul_self _, hd.2.2 y⟩

def gramProjectiveStrategy (A : Architecture) (d : GramData A)
    (hd : GramProjective A d) : ProjectiveStrategy A where
  state := (gramStrategy A d hd.1).state
  alice := fun x => ⟨(gramStrategy A d hd.1).alice x, hd.2.1 x, hd.2.2.1 x⟩
  bob := fun y => ⟨(gramStrategy A d hd.1).bob y, hd.2.2.2.1 y, hd.2.2.2.2 y⟩

/-- Every PSD matrix has a square Gram factor; no rank/purity restriction is made. -/
theorem strategy_has_gram_data {A : Architecture} (s : Strategy A) :
    ∃ d : GramData A, GramValid A d ∧ gramBehavior A d = s.behavior := by
  classical
  obtain ⟨C, hC⟩ := Matrix.posSemidef_iff_eq_transpose_mul_self.mp s.state.positive
  choose L hL using fun x a => Matrix.posSemidef_iff_eq_transpose_mul_self.mp ((s.alice x).positive a)
  choose R hR using fun y b => Matrix.posSemidef_iff_eq_transpose_mul_self.mp ((s.bob y).positive b)
  refine ⟨(C, L, R), ⟨?_, ?_, ?_⟩, ?_⟩
  · simpa only [gramMatrix, ← hC] using s.state.normalized
  · intro x
    simpa only [gramMatrix, ← hL] using (s.alice x).normalized
  · intro y
    simpa only [gramMatrix, ← hR] using (s.bob y).normalized
  · funext x y a b
    simp only [gramBehavior, Strategy.behavior, gramMatrix, ← hC, ← hL, ← hR]

theorem rawPOVM_eq_gram_image (A : Architecture) :
    rawPOVM A = gramBehavior A '' {d | GramValid A d} := by
  apply Set.Subset.antisymm
  · rintro p ⟨s, rfl⟩
    obtain ⟨d, hd, he⟩ := strategy_has_gram_data s
    exact ⟨d, hd, he⟩
  · rintro p ⟨d, hd, rfl⟩
    exact ⟨gramStrategy A d hd, rfl⟩

theorem rawPVM_eq_gram_image (A : Architecture) :
    rawPVM A = gramBehavior A '' {d | GramProjective A d} := by
  classical
  apply Set.Subset.antisymm
  · rintro p ⟨s, rfl⟩
    obtain ⟨C, hC⟩ := Matrix.posSemidef_iff_eq_transpose_mul_self.mp s.state.positive
    choose L hL using fun x a => Matrix.posSemidef_iff_eq_transpose_mul_self.mp ((s.alice x).positive a)
    choose R hR using fun y b => Matrix.posSemidef_iff_eq_transpose_mul_self.mp ((s.bob y).positive b)
    refine ⟨(C, L, R), ?_, ?_⟩
    · refine ⟨⟨?_, ?_, ?_⟩, ?_, ?_, ?_, ?_⟩
      · simpa only [gramMatrix, ← hC] using s.state.normalized
      · intro x; simpa only [gramMatrix, ← hL] using (s.alice x).normalized
      · intro y; simpa only [gramMatrix, ← hR] using (s.bob y).normalized
      · intro x a; simpa only [gramMatrix, ← hL] using (s.alice x).idempotent a
      · intro x a b hab; simpa only [gramMatrix, ← hL] using (s.alice x).orthogonal a b hab
      · intro y b; simpa only [gramMatrix, ← hR] using (s.bob y).idempotent b
      · intro y a b hab; simpa only [gramMatrix, ← hR] using (s.bob y).orthogonal a b hab
    · funext x y a b
      simp only [gramBehavior, ProjectiveStrategy.toStrategy, Strategy.behavior,
        gramMatrix, ← hC, ← hL, ← hR]
  · rintro p ⟨d, hd, rfl⟩
    exact ⟨gramProjectiveStrategy A d hd, rfl⟩

/-- Exact Frobenius identity, used only to bound individual Gram factors. -/
theorem trace_gram_norms {n : Type*} [Fintype n] (B : Matrix n n ℂ) :
    (Matrix.trace (gramMatrix B)).re = ∑ i, ∑ j, ‖B i j‖^2 := by
  have ht (z : ℂ) : (star z * z).re = ‖z‖^2 := by
    rw [pow_two, Complex.norm_mul_self_eq_normSq]
    simp [Complex.normSq_apply, Complex.mul_re]
  simp only [gramMatrix, Matrix.trace, Matrix.diag_apply, Matrix.mul_apply, Matrix.conjTranspose_apply,
    Complex.re_sum, ht]
  exact Finset.sum_comm

theorem entry_norm_sq_le_trace_gram {n : Type*} [Fintype n]
    (B : Matrix n n ℂ) (i j : n) : ‖B i j‖^2 ≤ (Matrix.trace (gramMatrix B)).re := by
  rw [trace_gram_norms]
  exact (Finset.single_le_sum (fun k _ => sq_nonneg ‖B i k‖) (Finset.mem_univ j)).trans
    (Finset.single_le_sum (fun k _ => Finset.sum_nonneg fun l _ => sq_nonneg ‖B k l‖)
      (Finset.mem_univ i))

def matrixBox (n : Type*) : Set (Matrix n n ℂ) :=
  {B | ∀ i j, ‖B i j‖ ≤ 2}

theorem matrixBox_isCompact (n : Type*) : IsCompact (matrixBox n) := by
  have hc := isCompact_pi_infinite fun _ : n =>
    isCompact_pi_infinite fun _ : n => isCompact_closedBall (0 : ℂ) 2
  simpa only [matrixBox, Metric.mem_closedBall, dist_zero_right] using hc

def gramBox (A : Architecture) : Set (GramData A) :=
  matrixBox Joint ×ˢ
    ({L | ∀ x a, L x a ∈ matrixBox Qubit} ×ˢ {R | ∀ y b, R y b ∈ matrixBox Qubit})

theorem gramBox_isCompact (A : Architecture) : IsCompact (gramBox A) := by
  exact (matrixBox_isCompact Joint).prod
    ((isCompact_pi_infinite fun _ => isCompact_pi_infinite fun _ => matrixBox_isCompact Qubit).prod
      (isCompact_pi_infinite fun _ => isCompact_pi_infinite fun _ => matrixBox_isCompact Qubit))

theorem gramValid_subset_box (A : Architecture) : {d | GramValid A d} ⊆ gramBox A := by
  intro d hd
  have hstate : ∀ i j, ‖d.1 i j‖ ≤ 2 := by
    intro i j
    have h := entry_norm_sq_le_trace_gram d.1 i j
    rw [hd.1] at h
    norm_num at h
    nlinarith [norm_nonneg (d.1 i j)]
  have hmeasurement {n : ℕ} (L : Fin n → Operator)
      (hL : ∑ a, gramMatrix (L a) = 1) : ∀ a i j, ‖L a i j‖ ≤ 2 := by
    intro a i j
    have htotal : ∑ b, (Matrix.trace (gramMatrix (L b))).re = 2 := by
      have h := congrArg (fun M : Operator => (Matrix.trace M).re) hL
      simpa [Matrix.trace_sum, Matrix.trace_one] using h
    have hone := entry_norm_sq_le_trace_gram (L a) i j
    have htwo : (Matrix.trace (gramMatrix (L a))).re ≤ 2 := by
      rw [← htotal]
      apply Finset.single_le_sum (f := fun b => (Matrix.trace (gramMatrix (L b))).re)
      · intro b _
        rw [trace_gram_norms]
        positivity
      · exact Finset.mem_univ a
    nlinarith [norm_nonneg (L a i j)]
  exact ⟨hstate, (fun x => hmeasurement _ (hd.2.1 x)), fun y => hmeasurement _ (hd.2.2 y)⟩

private theorem isClosed_forall {X : Type*} [TopologicalSpace X] {ι : Sort*}
    {p : X → ι → Prop} (h : ∀ i, IsClosed {x | p x i}) :
    IsClosed {x | ∀ i, p x i} := by
  simpa only [Set.setOf_forall] using isClosed_iInter h

theorem gramValid_isClosed (A : Architecture) : IsClosed {d : GramData A | GramValid A d} := by
  unfold GramValid
  apply IsClosed.inter
  · exact isClosed_eq (by unfold gramMatrix; fun_prop) continuous_const
  · apply IsClosed.inter
    · exact isClosed_forall fun x => isClosed_eq (by unfold gramMatrix; fun_prop) continuous_const
    · exact isClosed_forall fun y => isClosed_eq (by unfold gramMatrix; fun_prop) continuous_const

theorem gramProjective_isClosed (A : Architecture) : IsClosed {d : GramData A | GramProjective A d} := by
  unfold GramProjective
  apply (gramValid_isClosed A).inter
  refine IsClosed.inter ?_ (IsClosed.inter ?_ (IsClosed.inter ?_ ?_))
  · exact isClosed_forall fun x => isClosed_forall fun a =>
      isClosed_eq (by unfold gramMatrix; fun_prop) (by unfold gramMatrix; fun_prop)
  · exact isClosed_forall fun x => isClosed_forall fun a =>
      isClosed_forall fun b => isClosed_forall fun _ =>
        isClosed_eq (by unfold gramMatrix; fun_prop) continuous_const
  · exact isClosed_forall fun y => isClosed_forall fun b =>
      isClosed_eq (by unfold gramMatrix; fun_prop) (by unfold gramMatrix; fun_prop)
  · exact isClosed_forall fun y => isClosed_forall fun a =>
      isClosed_forall fun b => isClosed_forall fun _ =>
        isClosed_eq (by unfold gramMatrix; fun_prop) continuous_const

theorem gramBehavior_continuous (A : Architecture) : Continuous (gramBehavior A) := by
  unfold gramBehavior born gramMatrix tensor Matrix.trace
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply]
  fun_prop

theorem rawPOVM_isCompact (A : Architecture) : IsCompact (rawPOVM A) := by
  rw [rawPOVM_eq_gram_image]
  exact ((gramBox_isCompact A).of_isClosed_subset (gramValid_isClosed A)
    (gramValid_subset_box A)).image (gramBehavior_continuous A)

theorem rawPVM_isCompact (A : Architecture) : IsCompact (rawPVM A) := by
  rw [rawPVM_eq_gram_image]
  exact ((gramBox_isCompact A).of_isClosed_subset (gramProjective_isClosed A)
    (fun _ hd => gramValid_subset_box A hd.1)).image (gramBehavior_continuous A)

theorem convexPOVM_isCompact (A : Architecture) : IsCompact (convexPOVM A) :=
  compact_convexHull (rawPOVM_isCompact A)

theorem convexPVM_isCompact (A : Architecture) : IsCompact (convexPVM A) :=
  compact_convexHull (rawPVM_isCompact A)

theorem convexPVM_isClosed (A : Architecture) : IsClosed (convexPVM A) :=
  (convexPVM_isCompact A).isClosed

/-- A counterexample produces a PURELY BEHAVIORAL extreme maximizing point.
Its existence and unrandomized realization are established here, rather than
silently assuming extremality of an arbitrary numerical optimizer. -/
theorem counterexample_has_extreme_maximum (A : Architecture)
    (p : Behavior A) (hp : p ∈ convexPOVM A) (hnot : p ∉ convexPVM A) :
    ∃ (s : Strategy A) (f : Behavior A →ₗ[ℝ] ℝ),
      s.behavior ∈ Set.extremePoints ℝ (convexPOVM A) ∧
      (∀ q ∈ convexPOVM A, f q ≤ f s.behavior) ∧
      (∀ q ∈ convexPVM A, f q < f s.behavior) := by
  obtain ⟨l, c, hl, hcp⟩ := geometric_hahn_banach_closed_point
    (convex_convexHull ℝ (rawPVM A)) (convexPVM_isClosed A) hnot
  let face : Set (Behavior A) := {x ∈ convexPOVM A | ∀ q ∈ convexPOVM A, l q ≤ l x}
  have hf : IsExposed ℝ (convexPOVM A) face := fun _ => ⟨l, rfl⟩
  obtain ⟨m, hm, hmax⟩ := (convexPOVM_isCompact A).exists_isMaxOn ⟨p, hp⟩ l.continuous.continuousOn
  obtain ⟨e, he⟩ := (hf.isCompact (convexPOVM_isCompact A)).extremePoints_nonempty ⟨m, hm, hmax⟩
  have hex := hf.isExtreme.extremePoints_subset_extremePoints he
  have hraw : e ∈ rawPOVM A := extremePoints_convexHull_subset hex
  obtain ⟨s, rfl⟩ := hraw
  refine ⟨s, l.toLinearMap, hex, he.1.2, ?_⟩
  intro q hq
  have hq' := hl q hq
  have hp' := he.1.2 p hp
  change l q < l s.behavior
  linarith

end Bell
