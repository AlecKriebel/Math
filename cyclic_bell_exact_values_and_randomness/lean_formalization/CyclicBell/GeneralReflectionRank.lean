import CyclicBell.GeneralSupportedPhases

/-! Reflection-rank inequality on a possibly nonfaithful amplitude, followed by
an explicit direct-sum dimension count. This file alone is NOT support rigidity;
GeneralRigidity supplies its hypotheses from quantum saturation.
UNCOMPILED SOURCE CANDIDATES. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {ι ν : Type*} [Fintype ι] [Fintype ν] [DecidableEq ι] [DecidableEq ν]

theorem matrix_rank_add_le (A B : Matrix ι ν ℂ) : (A+B).rank≤A.rank+B.rank := by
  have hi : matrixRange (A+B)≤matrixRange A ⊔ matrixRange B := by
    rintro x ⟨v,hv⟩
    rw [← hv,Matrix.mulVecLin_apply,Matrix.add_mulVec]
    exact Submodule.add_mem_sup ⟨v,rfl⟩ ⟨v,rfl⟩
  have hd := Submodule.finrank_sup_add_finrank_inf_eq (matrixRange A) (matrixRange B)
  have hm := Submodule.finrank_mono hi
  change (A+B).rank≤Module.finrank ℂ ↥(matrixRange A ⊔ matrixRange B) at hm
  change Module.finrank ℂ ↥(matrixRange A ⊔ matrixRange B)+
    Module.finrank ℂ ↥(matrixRange A ⊓ matrixRange B)=A.rank+B.rank at hd
  omega

theorem matrix_rank_smul_le (c : ℂ) (A : Matrix ι ν ℂ) : (c • A).rank≤A.rank := by
  have hi : matrixRange (c • A)≤matrixRange A := by
    rintro x ⟨v,hv⟩
    refine ⟨c • v,?_⟩
    simpa [Matrix.mulVec_smul,Matrix.smul_mulVec_assoc] using hv
  exact Submodule.finrank_mono hi

theorem matrix_rank_smul (c : ℂ) (hc : c≠0) (A : Matrix ι ν ℂ) : (c • A).rank=A.rank := by
  apply le_antisymm (matrix_rank_smul_le c A)
  have h := matrix_rank_smul_le c⁻¹ (c • A)
  simpa [smul_smul,hc] using h

/-- Rank control before the final power relation. No invertibility is needed
for V or the reflection away from the column space of T. -/
theorem relative_reflection_rank_step (V E : Mat ι) (T : Matrix ι ν ℂ) (C : Mat ν)
    (hV : V*T=T*C) (n : ℕ) :
    (((V*(1-2 • E))^n-V^n)*T).rank≤n*(E*T).rank := by
  let W := V*(1-2 • E)
  induction n with
  | zero => simp
  | succ n ih =>
    have he : (W^(n+1)-V^(n+1))*T=
        W*((W^n-V^n)*T)+(-2 : ℂ) • (V*(E*T)*C^n) := by
      have hp := matrix_intertwiner_pow V T C hV n
      rw [pow_succ',pow_succ']
      calc
        (W*W^n-V*V^n)*T=W*((W^n-V^n)*T)+(W-V)*(V^n*T) := by simp only [Matrix.sub_mul,Matrix.mul_sub,Matrix.mul_assoc]; abel
        _=W*((W^n-V^n)*T)+(W-V)*(T*C^n) := by rw [hp]
        _=_ := by
          unfold W
          simp only [Matrix.mul_sub,Matrix.mul_one,Matrix.sub_mul,Matrix.mul_smul,Matrix.smul_mul,Matrix.mul_assoc]
          ext i j
          simp only [Matrix.sub_apply,Matrix.add_apply,Matrix.smul_apply,Pi.smul_apply,smul_eq_mul,Matrix.neg_apply]
          ring
    rw [he]
    have ha := matrix_rank_add_le (W*((W^n-V^n)*T)) ((-2 : ℂ) • (V*(E*T)*C^n))
    have hleft := Matrix.rank_mul_le_right W ((W^n-V^n)*T)
    have hright := (matrix_rank_smul_le (-2 : ℂ) (V*(E*T)*C^n)).trans
      ((Matrix.rank_mul_le_left (V*(E*T)) (C^n)).trans (Matrix.rank_mul_le_right V (E*T)))
    calc
      _≤(((W^n-V^n)*T).rank)+(E*T).rank := by omega
      _≤n*(E*T).rank+(E*T).rank := Nat.add_le_add_right ih _
      _=(n+1)*(E*T).rank := by rw [Nat.add_mul,one_mul]

/-- Rectangular/support form of the manuscript's reflection-rank lemma. -/
theorem relative_reflection_rank (d : ℕ) (V E : Mat ι) (T : Matrix ι ν ℂ) (C D : Mat ν)
    (hV : V*T=T*C) (hR : (V*(1-2 • E))*T=T*D)
    (hC : C^d=1) (hD : D^d=-1) : T.rank≤d*(E*T).rank := by
  have h := relative_reflection_rank_step V E T C hV d
  have hc := matrix_intertwiner_pow V T C hV d
  have hd := matrix_intertwiner_pow (V*(1-2 • E)) T D hR d
  have he : ((V*(1-2 • E))^d-V^d)*T=(-2 : ℂ) • T := by
    rw [Matrix.sub_mul,hd,hc,hC,hD,Matrix.mul_one,Matrix.mul_neg,Matrix.mul_one]
    module
  rw [he,matrix_rank_smul (-2) (by norm_num)] at h
  exact h

variable {J : Type*} [Fintype J] [DecidableEq J]

/-- Explicit isomorphism between the supported space and the product of its
spectral components. Preservation of the support is a necessary hypothesis. -/
def projectionRangeEquiv (P : J → Mat ι) (T : Matrix ι ν ℂ)
    (hs : (∑ j,P j)*T=T)
    (ho : ∀ i j,P i*P j=if i=j then P j else 0)
    (hp : ∀ j,matrixRange (P j*T)≤matrixRange T) :
    matrixRange T ≃ₗ[ℂ] (∀ j,matrixRange (P j*T)) where
  toFun x j := ⟨P j*ᵥx,by
    obtain ⟨v,hv⟩ := x.property
    refine ⟨v,?_⟩
    change T *ᵥ v = (x : ι → ℂ) at hv
    rw [Matrix.mulVecLin_apply,← Matrix.mulVec_mulVec,hv]⟩
  invFun x := ⟨∑ j,(x j : ι → ℂ),Submodule.sum_mem _ (fun j _ => hp j (x j).property)⟩
  left_inv x := by
    apply Subtype.ext
    change (∑ j,P j*ᵥ(x : ι → ℂ))=(x : ι → ℂ)
    obtain ⟨v,hv⟩ := x.property
    change T *ᵥ v = (x : ι → ℂ) at hv
    rw [← hv]
    have hsum : (∑ j,P j) *ᵥ (T *ᵥ v) = ∑ j,P j *ᵥ (T *ᵥ v) := by
      ext i
      simp only [Matrix.mulVec,dotProduct,Matrix.sum_apply,Finset.sum_apply,Finset.sum_mul]
      rw [Finset.sum_comm]
    rw [← hsum,Matrix.mulVec_mulVec,hs]
  right_inv x := by
    funext i
    apply Subtype.ext
    change P i*ᵥ(∑ j,(x j : ι → ℂ))=(x i : ι → ℂ)
    change (P i).mulVecLin (∑ j,(x j : ι → ℂ)) = _
    rw [map_sum]
    simp only [Matrix.mulVecLin_apply]
    have he (j : J) : P i*ᵥ(x j : ι → ℂ)=if i=j then (x j : ι → ℂ) else 0 := by
      obtain ⟨v,hv⟩ := (x j).property
      rw [← hv,Matrix.mulVecLin_apply,Matrix.mulVec_mulVec,← Matrix.mul_assoc,ho]
      split_ifs <;> simp
    simp_rw [he]
    simp
  map_add' x y := by ext j i; simp [Matrix.mulVec_add]
  map_smul' c x := by ext j i; simp [Matrix.mulVec_smul]

theorem sum_supported_projection_ranks (P : J → Mat ι) (T : Matrix ι ν ℂ)
    (hs : (∑ j,P j)*T=T) (ho : ∀ i j,P i*P j=if i=j then P j else 0)
    (hp : ∀ j,matrixRange (P j*T)≤matrixRange T) :
    (∑ j,(P j*T).rank)=T.rank := by
  have h := (projectionRangeEquiv P T hs ho hp).finrank_eq
  rw [Module.finrank_pi_fintype] at h
  exact h.symm

/-- The rank lower bounds plus the full direct-sum dimension count force
EQUALITY of all multiplicities, not only a lower bound for each one. -/
theorem equal_ranks_from_lower_bounds {d : ℕ} [NeZero d] (n : ℕ) (r : Ix d → ℕ)
    (hs : (∑ j,r j)=n) (hl : ∀ j,n≤d*r j) :
    (∀ j,n=d*r j) ∧ (∀ j k,r j=r k) ∧ d∣n := by
  let f : Ix d → ℕ := fun j => d*r j-n
  have hf (j : Ix d) : f j+n=d*r j := Nat.sub_add_cancel (hl j)
  have hsum : (∑ j,f j)=0 := by
    have he := Finset.sum_congr rfl (fun j (_ : j∈Finset.univ) => hf j)
    rw [Finset.sum_add_distrib,Finset.sum_const,Finset.card_univ,ZMod.card,
      nsmul_eq_mul,← Finset.mul_sum,hs] at he
    norm_cast at he
    omega
  have he (j : Ix d) : n=d*r j := by
    have hj : f j=0 := (Finset.sum_eq_zero_iff).mp hsum j (Finset.mem_univ j)
    have hi := hf j
    omega
  refine ⟨he,?_,⟨r 0,(he 0)⟩⟩
  intro j k
  exact Nat.eq_of_mul_eq_mul_left (NeZero.pos d) ((he j).symm.trans (he k))

end CyclicBell.General
