import CyclicBell.GeneralCommutingModel
import CyclicBell.GeneralCoverageGNS
import CyclicBell.GeneralCoverageUltralimit
import Mathlib.LinearAlgebra.Finsupp.Defs
import Mathlib.Data.Finsupp.Basic

/-! Word moments of actual commuting PVM realizations. This is the concrete
input to the ultralimit/GNS closure argument; no realization is assumed for a
limiting kernel. -/
noncomputable section
open scoped BigOperators InnerProductSpace ComplexOrder
namespace CyclicBell.General.Coverage
variable {d : ℕ} [NeZero d] {α β : Type}
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

abbrev WordGenerator (d : ℕ) (α β : Type*) := Sum (α × Ix d) (β × Ix d)
abbrev MomentWord (d : ℕ) (α β : Type*) := List (WordGenerator d α β)

def sourceGenerator (s : CommutingOn d α β H) : WordGenerator d α β → (H →L[ℂ] H)
  | .inl (x,a) => (s.alice x).effect a
  | .inr (y,b) => (s.bob y).effect b

def sourceWordAction (s : CommutingOn d α β H) : MomentWord d α β → (H →L[ℂ] H)
  | [] => 1
  | g::w => sourceGenerator s g * sourceWordAction s w

def sourceWordVector (s : CommutingOn d α β H) (w : MomentWord d α β) : H :=
  sourceWordAction s w s.vector

def sourceKernel (s : CommutingOn d α β H) (u v : MomentWord d α β) : ℂ :=
  ⟪sourceWordVector s u,sourceWordVector s v⟫_ℂ

def sourcePolynomialVector (s : CommutingOn d α β H) (c : MomentWord d α β →₀ ℂ) : H :=
  c.sum (fun w z => z • sourceWordVector s w)

theorem sourceGenerator_selfadjoint (s : CommutingOn d α β H) (g : WordGenerator d α β) :
    star (sourceGenerator s g)=sourceGenerator s g := by
  rcases g with ⟨x,a⟩|⟨y,b⟩
  · exact (s.alice x).selfadjoint a
  · exact (s.bob y).selfadjoint b

theorem sourceGenerator_idempotent (s : CommutingOn d α β H) (g : WordGenerator d α β) :
    sourceGenerator s g * sourceGenerator s g=sourceGenerator s g := by
  rcases g with ⟨x,a⟩|⟨y,b⟩
  · exact (s.alice x).idempotent a
  · exact (s.bob y).idempotent b

theorem sourceGenerator_contract (s : CommutingOn d α β H) (g : WordGenerator d α β) (v : H) :
    ‖sourceGenerator s g v‖≤‖v‖ := by
  let P := sourceGenerator s g
  have hs : star P * P = P := by rw [sourceGenerator_selfadjoint,sourceGenerator_idempotent]
  have he := vectorEval_square v P
  rw [hs] at he
  have hb : vectorEval v P≤‖v‖*‖P v‖ :=
    (Complex.re_le_norm _).trans (norm_inner_le_norm v (P v))
  change ‖P v‖≤‖v‖
  by_cases ht : ‖P v‖=0
  · simpa only [ht] using norm_nonneg v
  · apply (mul_le_mul_right (lt_of_le_of_ne (norm_nonneg (P v)) (Ne.symm ht))).mp
    simpa only [he,pow_two] using hb

@[simp] theorem sourceWordVector_nil (s : CommutingOn d α β H) : sourceWordVector s []=s.vector := rfl
@[simp] theorem sourceWordVector_cons (s : CommutingOn d α β H) (g : WordGenerator d α β)
    (w : MomentWord d α β) : sourceWordVector s (g::w)=sourceGenerator s g (sourceWordVector s w) := rfl

theorem sourceWordVector_norm_le_one (s : CommutingOn d α β H) (w : MomentWord d α β) :
    ‖sourceWordVector s w‖≤1 := by
  induction w with
  | nil => exact s.normalized.le
  | cons g w ih => exact (sourceGenerator_contract s g _).trans ih

theorem sourceKernel_bound (s : CommutingOn d α β H) (u v : MomentWord d α β) :
    ‖sourceKernel s u v‖≤1 := by
  apply (norm_inner_le_norm _ _).trans
  exact (mul_le_mul (sourceWordVector_norm_le_one s u) (sourceWordVector_norm_le_one s v)
    (norm_nonneg _) (by norm_num)).trans_eq (one_mul 1)

theorem sourceKernel_hermitian (s : CommutingOn d α β H) (u v : MomentWord d α β) :
    star (sourceKernel s v u)=sourceKernel s u v := inner_conj_symm _ _

theorem sourceKernel_normalized (s : CommutingOn d α β H) : sourceKernel s [] []=1 := by
  simp [sourceKernel,inner_self_eq_norm_sq_to_K,s.normalized]

theorem sourceKernel_move_generator (s : CommutingOn d α β H)
    (g : WordGenerator d α β) (u v : MomentWord d α β) :
    sourceKernel s (g::u) v=sourceKernel s u (g::v) := by
  unfold sourceKernel
  simp only [sourceWordVector_cons]
  have h := (sourceGenerator s g).adjoint_inner_left (sourceWordVector s v) (sourceWordVector s u)
  change ⟪(star (sourceGenerator s g)) (sourceWordVector s u),sourceWordVector s v⟫_ℂ = _ at h
  rwa [sourceGenerator_selfadjoint] at h

theorem sourceKernel_idempotent (s : CommutingOn d α β H)
    (g : WordGenerator d α β) (u v : MomentWord d α β) :
    sourceKernel s u (g::g::v)=sourceKernel s u (g::v) := by
  unfold sourceKernel
  simp only [sourceWordVector_cons]
  rw [← ContinuousLinearMap.mul_apply,sourceGenerator_idempotent]

theorem sourceKernel_alice_orthogonal (s : CommutingOn d α β H)
    (x : α) (a b : Ix d) (hab : a≠b) (u v : MomentWord d α β) :
    sourceKernel s u (.inl (x,a)::.inl (x,b)::v)=0 := by
  unfold sourceKernel
  simp only [sourceWordVector_cons,sourceGenerator]
  rw [← ContinuousLinearMap.mul_apply,(s.alice x).orthogonal a b hab]
  simp

theorem sourceKernel_bob_orthogonal (s : CommutingOn d α β H)
    (y : β) (a b : Ix d) (hab : a≠b) (u v : MomentWord d α β) :
    sourceKernel s u (.inr (y,a)::.inr (y,b)::v)=0 := by
  unfold sourceKernel
  simp only [sourceWordVector_cons,sourceGenerator]
  rw [← ContinuousLinearMap.mul_apply,(s.bob y).orthogonal a b hab]
  simp

theorem sourceKernel_alice_complete (s : CommutingOn d α β H)
    (x : α) (u v : MomentWord d α β) :
    (∑ a,sourceKernel s u (.inl (x,a)::v))=sourceKernel s u v := by
  simp only [sourceKernel,sourceWordVector_cons,sourceGenerator,← inner_sum]
  rw [← ContinuousLinearMap.sum_apply,(s.alice x).complete]
  rfl

theorem sourceKernel_bob_complete (s : CommutingOn d α β H)
    (y : β) (u v : MomentWord d α β) :
    (∑ b,sourceKernel s u (.inr (y,b)::v))=sourceKernel s u v := by
  simp only [sourceKernel,sourceWordVector_cons,sourceGenerator,← inner_sum]
  rw [← ContinuousLinearMap.sum_apply,(s.bob y).complete]
  rfl

theorem sourceKernel_cross (s : CommutingOn d α β H)
    (x : α) (y : β) (a b : Ix d) (u v : MomentWord d α β) :
    sourceKernel s u (.inl (x,a)::.inr (y,b)::v)=
      sourceKernel s u (.inr (y,b)::.inl (x,a)::v) := by
  simp only [sourceKernel,sourceWordVector_cons,sourceGenerator]
  rw [← ContinuousLinearMap.mul_apply,← ContinuousLinearMap.mul_apply,s.cross]

theorem sourceKernel_behavior (s : CommutingOn d α β H) (x : α) (y : β) (a b : Ix d) :
    sourceKernel s [] [.inl (x,a),.inr (y,b)]=(commutingBehavior s x y a b : ℂ) := by
  rw [commutingBehavior_complex]
  rfl

def wordPrepend (g : WordGenerator d α β) :
    (MomentWord d α β →₀ ℂ) →ₗ[ℂ] (MomentWord d α β →₀ ℂ) :=
  Finsupp.lmapDomain ℂ ℂ (List.cons g)

theorem sourceKernel_quadratic (s : CommutingOn d α β H)
    (c e : MomentWord d α β →₀ ℂ) :
    kernelInner (sourceKernel s) c e=⟪sourcePolynomialVector s c,sourcePolynomialVector s e⟫_ℂ := by
  simp only [kernelInner,sourcePolynomialVector,Finsupp.sum_inner,Finsupp.inner_sum,
    inner_smul_left,inner_smul_right,sourceKernel,Finsupp.sum]
  simp only [sum_inner,inner_sum,inner_smul_left,inner_smul_right,Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro u _
  apply Finset.sum_congr rfl
  intro v _
  simp only [Complex.star_def]
  ring

theorem sourceKernel_positive (s : CommutingOn d α β H) (c : MomentWord d α β →₀ ℂ) :
    0≤(kernelInner (sourceKernel s) c c).re := by
  rw [sourceKernel_quadratic]
  exact inner_self_nonneg (𝕜 := ℂ) (x := sourcePolynomialVector s c)

theorem sourcePolynomial_prepend (s : CommutingOn d α β H)
    (g : WordGenerator d α β) (c : MomentWord d α β →₀ ℂ) :
    sourcePolynomialVector s (wordPrepend g c)=sourceGenerator s g (sourcePolynomialVector s c) := by
  unfold sourcePolynomialVector wordPrepend
  change (Finsupp.mapDomain (List.cons g) c).sum _ = _
  rw [Finsupp.sum_mapDomain_index (by intro w; simp) (by intro w z t; simp [add_smul])]
  simp only [sourceWordVector_cons,Finsupp.sum,map_sum,map_smul]

theorem sourceKernel_prepend_contract (s : CommutingOn d α β H)
    (g : WordGenerator d α β) (c : MomentWord d α β →₀ ℂ) :
    (kernelInner (sourceKernel s) (wordPrepend g c) (wordPrepend g c)).re≤
      (kernelInner (sourceKernel s) c c).re := by
  rw [sourceKernel_quadratic,sourceKernel_quadratic,sourcePolynomial_prepend]
  change RCLike.re (⟪sourceGenerator s g (sourcePolynomialVector s c),sourceGenerator s g (sourcePolynomialVector s c)⟫_ℂ) ≤ RCLike.re (⟪sourcePolynomialVector s c,sourcePolynomialVector s c⟫_ℂ)
  rw [← norm_sq_eq_re_inner,← norm_sq_eq_re_inner]
  exact pow_le_pow_left₀ (norm_nonneg _) (sourceGenerator_contract s g (sourcePolynomialVector s c)) 2

section Limits
variable {J : Type*} (U : Ultrafilter J) (Hn : J → Type*)
  [∀ n,NormedAddCommGroup (Hn n)] [∀ n,InnerProductSpace ℂ (Hn n)] [∀ n,CompleteSpace (Hn n)]
  (s : ∀ n,CommutingOn d α β (Hn n))

include s in
theorem sourceKernel_bounded (u v : MomentWord d α β) :
    BoundedFamily (fun n => sourceKernel (s n) u v) :=
  ⟨1,fun n => sourceKernel_bound (s n) u v⟩

def limitEntry (u v : MomentWord d α β) : ℂ := ultraLimit U (fun n => sourceKernel (s n) u v)

theorem sourceQuadratic_bounded (c e : MomentWord d α β →₀ ℂ) :
    BoundedFamily (fun n => kernelInner (sourceKernel (s n)) c e) := by
  unfold kernelInner Finsupp.sum
  apply BoundedFamily.sum
  intro u
  apply BoundedFamily.sum
  intro v
  exact ((BoundedFamily.const (star (c u))).mul (sourceKernel_bounded Hn s u v)).mul
    (BoundedFamily.const (e v))

theorem limitEntry_quadratic (c e : MomentWord d α β →₀ ℂ) :
    kernelInner (limitEntry U Hn s) c e = ultraLimit U (fun n => kernelInner (sourceKernel (s n)) c e) := by
  unfold kernelInner Finsupp.sum
  rw [ultraLimit_sum]
  · apply Finset.sum_congr rfl
    intro u _
    rw [ultraLimit_sum]
    · apply Finset.sum_congr rfl
      intro v _
      rw [ultraLimit_mul _ _ _
        ((BoundedFamily.const (star (c u))).mul (sourceKernel_bounded Hn s u v))
        (BoundedFamily.const (e v)),ultraLimit_smul _ _ _ (sourceKernel_bounded Hn s u v),ultraLimit_const]
      rfl
    · intro v _
      exact ((BoundedFamily.const (star (c u))).mul (sourceKernel_bounded Hn s u v)).mul
        (BoundedFamily.const (e v))
  · intro u _
    apply BoundedFamily.sum
    intro v
    exact ((BoundedFamily.const (star (c u))).mul (sourceKernel_bounded Hn s u v)).mul
      (BoundedFamily.const (e v))

def limitingKernel : PositiveKernel (MomentWord d α β) where
  entry := limitEntry U Hn s
  hermitian := by
    intro u v
    unfold limitEntry
    rw [← ultraLimit_star _ _ (sourceKernel_bounded Hn s v u)]
    congr 1
    funext n
    exact sourceKernel_hermitian (s n) u v
  positive := by
    intro c
    rw [limitEntry_quadratic]
    exact ultraLimit_re_nonneg U _ (sourceQuadratic_bounded Hn s c c)
      (Filter.Eventually.of_forall (fun n => sourceKernel_positive (s n) c))

theorem limitEntry_normalized : limitEntry U Hn s [] []=1 := by
  simp [limitEntry,sourceKernel_normalized]

theorem limitEntry_prepend_contract (g : WordGenerator d α β) (c : MomentWord d α β →₀ ℂ) :
    (kernelInner (limitEntry U Hn s) (wordPrepend g c) (wordPrepend g c)).re≤
      (kernelInner (limitEntry U Hn s) c c).re := by
  rw [limitEntry_quadratic,limitEntry_quadratic]
  have h := ultraLimit_re_nonneg U _
    ((sourceQuadratic_bounded Hn s c c).sub
      (sourceQuadratic_bounded Hn s (wordPrepend g c) (wordPrepend g c)))
    (Filter.Eventually.of_forall (fun n => by
      simpa only [Complex.sub_re] using sub_nonneg.mpr (sourceKernel_prepend_contract (s n) g c)))
  rw [ultraLimit_sub _ _ _ (sourceQuadratic_bounded Hn s c c)
    (sourceQuadratic_bounded Hn s (wordPrepend g c) (wordPrepend g c)),Complex.sub_re] at h
  exact sub_nonneg.mp h

theorem limitEntry_move_generator (g : WordGenerator d α β) (u v : MomentWord d α β) :
    limitEntry U Hn s (g::u) v=limitEntry U Hn s u (g::v) := by
  unfold limitEntry
  congr 1
  funext n
  exact sourceKernel_move_generator (s n) g u v

theorem limitEntry_idempotent (g : WordGenerator d α β) (u v : MomentWord d α β) :
    limitEntry U Hn s u (g::g::v)=limitEntry U Hn s u (g::v) := by
  unfold limitEntry
  congr 1
  funext n
  exact sourceKernel_idempotent (s n) g u v

theorem limitEntry_alice_orthogonal (x : α) (a b : Ix d) (hab : a≠b) (u v : MomentWord d α β) :
    limitEntry U Hn s u (.inl (x,a)::.inl (x,b)::v)=0 := by
  simp only [limitEntry,sourceKernel_alice_orthogonal _ _ _ _ hab,ultraLimit_const]

theorem limitEntry_bob_orthogonal (y : β) (a b : Ix d) (hab : a≠b) (u v : MomentWord d α β) :
    limitEntry U Hn s u (.inr (y,a)::.inr (y,b)::v)=0 := by
  simp only [limitEntry,sourceKernel_bob_orthogonal _ _ _ _ hab,ultraLimit_const]

theorem limitEntry_alice_complete (x : α) (u v : MomentWord d α β) :
    (∑ a,limitEntry U Hn s u (.inl (x,a)::v))=limitEntry U Hn s u v := by
  unfold limitEntry
  rw [← ultraLimit_sum U Finset.univ _ (fun a _ => sourceKernel_bounded Hn s u (.inl (x,a)::v))]
  congr 1
  funext n
  exact sourceKernel_alice_complete (s n) x u v

theorem limitEntry_bob_complete (y : β) (u v : MomentWord d α β) :
    (∑ b,limitEntry U Hn s u (.inr (y,b)::v))=limitEntry U Hn s u v := by
  unfold limitEntry
  rw [← ultraLimit_sum U Finset.univ _ (fun b _ => sourceKernel_bounded Hn s u (.inr (y,b)::v))]
  congr 1
  funext n
  exact sourceKernel_bob_complete (s n) y u v

theorem limitEntry_cross (x : α) (y : β) (a b : Ix d) (u v : MomentWord d α β) :
    limitEntry U Hn s u (.inl (x,a)::.inr (y,b)::v)=
      limitEntry U Hn s u (.inr (y,b)::.inl (x,a)::v) := by
  unfold limitEntry
  congr 1
  funext n
  exact sourceKernel_cross (s n) x y a b u v

end Limits

/-- The empty/length-two moments retain the ordinary limit of the actual
probabilities. Finiteness of input sets is only needed later to extract a
sequence from topological closure, not for this convergence implication. -/
theorem limitEntry_behavior_of_tendsto (Hn : ℕ → Type*)
    [∀ n,NormedAddCommGroup (Hn n)] [∀ n,InnerProductSpace ℂ (Hn n)] [∀ n,CompleteSpace (Hn n)]
    (s : ∀ n,CommutingOn d α β (Hn n)) (p : BellBehavior d α β)
    (hp : Filter.Tendsto (fun n => commutingBehavior (s n)) Filter.atTop (nhds p))
    (x : α) (y : β) (a b : Ix d) :
    limitEntry naturalUltrafilter Hn s [] [.inl (x,a),.inr (y,b)]=(p x y a b : ℂ) := by
  unfold limitEntry
  simp only [sourceKernel_behavior]
  apply ultraLimit_natural_of_tendsto
  have h := tendsto_pi_nhds.mp (tendsto_pi_nhds.mp
    (tendsto_pi_nhds.mp (tendsto_pi_nhds.mp hp x) y) a) b
  exact Complex.continuous_ofReal.continuousAt.tendsto.comp h

end CyclicBell.General.Coverage
