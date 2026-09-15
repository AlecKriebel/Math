import CyclicBell.GeneralCoverageMomentModel
import CyclicBell.GeneralCoverageCompletionOperators

/-! Actual complete-Hilbert commuting model reconstructed from limits of actual
PVM word kernels. Every operator relation is checked on a dense vector span. -/
noncomputable section
open scoped BigOperators InnerProductSpace Topology
namespace CyclicBell.General.Coverage
variable {d : ℕ} [NeZero d] {α β : Type}
variable {J : Type*} (U : Ultrafilter J) (Hn : J → Type*)
variable [∀ n,NormedAddCommGroup (Hn n)] [∀ n,InnerProductSpace ℂ (Hn n)]
variable [∀ n,CompleteSpace (Hn n)] (s : ∀ n,CommutingOn d α β (Hn n))

abbrev LimitHilbert := KernelHilbert (limitingKernel U Hn s)

def limitVector (w : MomentWord d α β) : LimitHilbert U Hn s :=
  kernelVector (limitingKernel U Hn s) w

theorem limitVector_inner (u v : MomentWord d α β) :
    ⟪limitVector U Hn s u,limitVector U Hn s v⟫_ℂ = limitEntry U Hn s u v :=
  kernelVector_inner _ _ _

def limitGenerator (g : WordGenerator d α β) : LimitHilbert U Hn s →L[ℂ] LimitHilbert U Hn s :=
  completionOfBounded (wordPrepend g : KernelSpan (limitingKernel U Hn s) →ₗ[ℂ] _) 1
    (fun c => by
      simpa using (kernelSpan_contraction (limitingKernel U Hn s)
        (wordPrepend g) (limitEntry_prepend_contract U Hn s g) c))

theorem limitGenerator_vector (g : WordGenerator d α β) (w : MomentWord d α β) :
    limitGenerator U Hn s g (limitVector U Hn s w)=limitVector U Hn s (g::w) := by
  unfold limitGenerator limitVector kernelVector kernelEmbed
  simp only [UniformSpace.Completion.coe_toComplL]
  rw [completionOfBounded_coe]
  apply congrArg (fun c : KernelSpan (limitingKernel U Hn s) =>
    (c : UniformSpace.Completion (KernelSpan (limitingKernel U Hn s))))
  exact Finsupp.mapDomain_single

theorem limitVector_ext (x y : LimitHilbert U Hn s)
    (h : ∀ w,⟪limitVector U Hn s w,x⟫_ℂ = ⟪limitVector U Hn s w,y⟫_ℂ) : x=y := by
  apply ext_inner_left ℂ
  intro z
  have he : innerSLFlip ℂ x=innerSLFlip ℂ y := by
    apply ContinuousLinearMap.ext_on (kernelVector_dense_span (limitingKernel U Hn s))
    rintro _ ⟨w,rfl⟩
    exact h w
  exact congrArg (fun f => f z) he

theorem limitOperator_ext (A B : LimitHilbert U Hn s →L[ℂ] LimitHilbert U Hn s)
    (h : ∀ u v,⟪limitVector U Hn s u,A (limitVector U Hn s v)⟫_ℂ =
      ⟪limitVector U Hn s u,B (limitVector U Hn s v)⟫_ℂ) : A=B := by
  apply ContinuousLinearMap.ext_on (kernelVector_dense_span (limitingKernel U Hn s))
  rintro _ ⟨v,rfl⟩
  exact limitVector_ext U Hn s _ _ (fun u => h u v)

theorem limitGenerator_selfadjoint (g : WordGenerator d α β) :
    star (limitGenerator U Hn s g)=limitGenerator U Hn s g := by
  apply limitOperator_ext U Hn s
  intro u v
  change ⟪limitVector U Hn s u,(limitGenerator U Hn s g).adjoint (limitVector U Hn s v)⟫_ℂ = _
  rw [ContinuousLinearMap.adjoint_inner_right,limitGenerator_vector,limitGenerator_vector,
    limitVector_inner,limitVector_inner]
  exact limitEntry_move_generator U Hn s g u v

theorem limitGenerator_idempotent (g : WordGenerator d α β) :
    limitGenerator U Hn s g*limitGenerator U Hn s g=limitGenerator U Hn s g := by
  apply limitOperator_ext U Hn s
  intro u v
  simp only [ContinuousLinearMap.mul_apply,limitGenerator_vector,limitVector_inner]
  exact limitEntry_idempotent U Hn s g u v

theorem limitGenerator_alice_orthogonal (x : α) (a b : Ix d) (hab : a≠b) :
    limitGenerator U Hn s (.inl (x,a))*limitGenerator U Hn s (.inl (x,b))=0 := by
  apply limitOperator_ext U Hn s
  intro u v
  simp only [ContinuousLinearMap.mul_apply,limitGenerator_vector,limitVector_inner,
    ContinuousLinearMap.zero_apply,inner_zero_right]
  exact limitEntry_alice_orthogonal U Hn s x a b hab u v

theorem limitGenerator_bob_orthogonal (y : β) (a b : Ix d) (hab : a≠b) :
    limitGenerator U Hn s (.inr (y,a))*limitGenerator U Hn s (.inr (y,b))=0 := by
  apply limitOperator_ext U Hn s
  intro u v
  simp only [ContinuousLinearMap.mul_apply,limitGenerator_vector,limitVector_inner,
    ContinuousLinearMap.zero_apply,inner_zero_right]
  exact limitEntry_bob_orthogonal U Hn s y a b hab u v

theorem limitGenerator_alice_complete (x : α) :
    (∑ a,limitGenerator U Hn s (.inl (x,a)))=1 := by
  apply limitOperator_ext U Hn s
  intro u v
  simp only [ContinuousLinearMap.sum_apply,inner_sum,limitGenerator_vector,
    ContinuousLinearMap.one_apply,limitVector_inner]
  exact limitEntry_alice_complete U Hn s x u v

theorem limitGenerator_bob_complete (y : β) :
    (∑ b,limitGenerator U Hn s (.inr (y,b)))=1 := by
  apply limitOperator_ext U Hn s
  intro u v
  simp only [ContinuousLinearMap.sum_apply,inner_sum,limitGenerator_vector,
    ContinuousLinearMap.one_apply,limitVector_inner]
  exact limitEntry_bob_complete U Hn s y u v

theorem limitGenerator_cross (x : α) (y : β) (a b : Ix d) :
    limitGenerator U Hn s (.inl (x,a))*limitGenerator U Hn s (.inr (y,b))=
      limitGenerator U Hn s (.inr (y,b))*limitGenerator U Hn s (.inl (x,a)) := by
  apply limitOperator_ext U Hn s
  intro u v
  simp only [ContinuousLinearMap.mul_apply,limitGenerator_vector,limitVector_inner]
  exact limitEntry_cross U Hn s x y a b u v

def reconstructedModel : CommutingOn d α β (LimitHilbert U Hn s) where
  vector := limitVector U Hn s []
  normalized := by
    have h := norm_sq_eq_re_inner (𝕜 := ℂ) (limitVector U Hn s [])
    rw [limitVector_inner,limitEntry_normalized] at h
    have hn := norm_nonneg (limitVector U Hn s [])
    norm_num at h
    rcases h with h | h
    · exact h
    · linarith
  alice := fun x => {
    effect := fun a => limitGenerator U Hn s (.inl (x,a))
    selfadjoint := fun a => limitGenerator_selfadjoint U Hn s _
    idempotent := fun a => limitGenerator_idempotent U Hn s _
    orthogonal := limitGenerator_alice_orthogonal U Hn s x
    complete := limitGenerator_alice_complete U Hn s x }
  bob := fun y => {
    effect := fun b => limitGenerator U Hn s (.inr (y,b))
    selfadjoint := fun b => limitGenerator_selfadjoint U Hn s _
    idempotent := fun b => limitGenerator_idempotent U Hn s _
    orthogonal := limitGenerator_bob_orthogonal U Hn s y
    complete := limitGenerator_bob_complete U Hn s y }
  cross := limitGenerator_cross U Hn s

theorem reconstructedModel_behavior (x : α) (y : β) (a b : Ix d) :
    (commutingBehavior (reconstructedModel U Hn s) x y a b : ℂ)=
      limitEntry U Hn s [] [.inl (x,a),.inr (y,b)] := by
  rw [commutingBehavior_complex]
  change ⟪limitVector U Hn s [],
    (limitGenerator U Hn s (.inl (x,a))*limitGenerator U Hn s (.inr (y,b)))
      (limitVector U Hn s [])⟫_ℂ = _
  simp only [ContinuousLinearMap.mul_apply,limitGenerator_vector,limitVector_inner]

end CyclicBell.General.Coverage
