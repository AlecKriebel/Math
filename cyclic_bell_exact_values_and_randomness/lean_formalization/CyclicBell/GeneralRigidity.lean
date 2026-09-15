import CyclicBell.GeneralReflectionRank

/-! Complete finite-dimensional supported-multiplicity source chain.
The final theorem starts with an arbitrary mixed-state PVM strategy and its
actual first-family scalar value. Support cancellation, invariance, polar
kernels, reflection powers and dimension summation are all dependencies.
UNCOMPILED: no claim of accepted Lean proof or a commuting-model rigidity result. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.General
variable {d : ℕ} [NeZero d]
variable {ι ν : Type*} [Fintype ι] [Fintype ν] [DecidableEq ι] [DecidableEq ν]

def rootFilter (U : Mat ι) (k : Ix d) : Mat ι :=
  (d : ℂ)⁻¹ • ∑ r : Ix d,chi (-(k*r)) • ((star (equalityBase d)) • U)^r.val

theorem rootFilter_at_root (k j : Ix d) :
    (d : ℂ)⁻¹*(∑ r : Ix d,chi (-(k*r))*(star (equalityBase d)*equalityRoot j)^r.val)=
      if j=k then 1 else 0 := by
  have hb : star (equalityBase d)*equalityBase d=1 := cis_unit _
  have he (r : Ix d) : chi (-(k*r))*(star (equalityBase d)*equalityRoot j)^r.val=
      chi (r*(j-k)) := by
    rw [equalityRoot,← mul_assoc,hb,one_mul,chi_pow,ZMod.natCast_zmod_val,← chi_add]
    congr 1
    ring
  simp_rw [he]
  have hc := character_sum (j-k)
  simp only [mul_comm] at hc
  rw [hc]
  by_cases hj : j=k
  · simp [hj,ne_of_gt (dimension_pos (d := d))]
  · simp [sub_ne_zero.mpr hj,hj]

theorem rootProjection_filter_on_support (hd : 2≤d) (U : Mat ι) (hU : UnitaryRel U)
    (T : Matrix ι ν ℂ) (hE : equalitySupport (d := d) U hU*T=T) (k : Ix d) :
    rootProjection U hU k*T=rootFilter U k*T := by
  have h := equality_supported_action hd U hU T hE
    (fun z => if z=equalityRoot k then 1 else 0)
    (fun z => (d : ℂ)⁻¹*(∑ r : Ix d,chi (-(k*r))*(star (equalityBase d)*z)^r.val))
    (fun j => by rw [equalityRoot_injective.eq_iff,rootFilter_at_root])
  simpa [rootProjection,finiteSpectralProjection,rootFilter] using h

theorem rootFilter_intertwines (U : Mat ι) (T : Matrix ι ν ℂ) (W : Mat ν)
    (h : U*T=T*W) (k : Ix d) : rootFilter (d := d) U k*T=T*rootFilter W k := by
  have hs : (star (equalityBase d) • U)*T=T*(star (equalityBase d) • W) := by
    simp only [smul_mul_assoc,mul_smul_comm,h]
  unfold rootFilter
  simp only [smul_mul_assoc,mul_smul_comm,Finset.sum_mul,Finset.mul_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro r _
  rw [smul_mul_assoc,mul_smul_comm,matrix_intertwiner_pow _ T _ hs r.val]

theorem rootProjection_preserves_support (hd : 2≤d) (U : Mat ι) (hU : UnitaryRel U)
    (T : Matrix ι ν ℂ) (W : Mat ν) (hE : equalitySupport (d := d) U hU*T=T)
    (hW : U*T=T*W) (k : Ix d) : matrixRange (rootProjection U hU k*T)≤matrixRange T := by
  rw [rootProjection_filter_on_support hd U hU T hE,rootFilter_intertwines U T W hW]
  exact matrixRange_mul_le T _

theorem rootProjection_sum_on_support (hd : 2≤d) (U : Mat ι) (hU : UnitaryRel U)
    (T : Matrix ι ν ℂ) (hE : equalitySupport (d := d) U hU*T=T) :
    (∑ k : Ix d,rootProjection U hU k)*T=T := by
  have h := equality_supported_action hd U hU T hE
    (fun z => ∑ k : Ix d,if z=equalityRoot k then (1 : ℂ) else 0) (fun _ => 1)
    (fun j => by simp [equalityRoot_injective.eq_iff])
  simpa [rootProjection,finiteSpectralProjection] using h

theorem rootProjection_orthogonal (U : Mat ι) (hU : UnitaryRel U) (j k : Ix d) :
    rootProjection U hU j*rootProjection U hU k=if j=k then rootProjection U hU k else 0 := by
  rw [rootProjection,rootProjection,finiteSpectralProjection_mul,equalityRoot_injective.eq_iff]
  split_ifs with h
  · subst k; rfl
  · rfl

def supportedEigenspace (T : Matrix ι ν ℂ) (U : Mat ι) (z : ℂ) : Submodule ℂ (ι → ℂ) :=
  matrixRange T ⊓ LinearMap.ker (U-z • 1).mulVecLin

/-- Finite CFC evaluates on an eigenvector by its scalar eigenvalue. -/
theorem finiteCalc_eigenvector (U : Mat ι) (hU : UnitaryRel U) (f : ℂ → ℂ)
    (z : ℂ) (v : ι → ℂ) (hv : U*ᵥv=z • v) : finiteCalc U hU f*ᵥv=f z • v := by
  let T : Matrix ι (Fin 1) ℂ := fun i _ => v i
  have hT : (U-z • 1)*T=0 := by
    ext i j
    have h := congrArg (fun w : ι → ℂ => w i) hv
    simpa [T,Matrix.mul_apply,Matrix.mulVec,sub_mul,smul_mul_assoc] using sub_eq_zero.mpr h
  have h := finiteCalc_zero_transfer U hU (fun w => w-z) (fun w => f w-f z) T
    (fun w hw => by rw [sub_eq_zero.mp hw]; simp) (by simpa using hT)
  simp only [finiteCalc_sub,finiteCalc_const,sub_mul,smul_mul_assoc,one_mul] at h
  have hi := congrArg (fun Q : Matrix ι (Fin 1) ℂ => Q · 0) h
  simpa [T,Matrix.mul_apply,Matrix.mulVec,sub_eq_zero] using hi

theorem rootProjection_range_eigenspace (hd : 2≤d) (U : Mat ι) (hU : UnitaryRel U)
    (T : Matrix ι ν ℂ) (W : Mat ν) (hE : equalitySupport (d := d) U hU*T=T)
    (hW : U*T=T*W) (k : Ix d) :
    matrixRange (rootProjection U hU k*T)=supportedEigenspace T U (equalityRoot k) := by
  apply le_antisymm
  · rintro x ⟨v,hv⟩
    refine ⟨rootProjection_preserves_support hd U hU T W hE hW k ⟨v,hv⟩,?_⟩
    change (U-equalityRoot k • 1)*ᵥx=0
    rw [← hv,Matrix.mulVecLin_apply,Matrix.mulVec_mulVec]
    have he : (U-equalityRoot k • 1)*(rootProjection U hU k*T)=0 := by
      rw [← mul_assoc,sub_mul,finiteSpectralProjection_eigen,smul_mul_assoc,one_mul,sub_self,zero_mul]
    rw [he,Matrix.zero_mulVec]
  · rintro x ⟨hx,hux⟩
    obtain ⟨v,hv⟩ := hx
    have he : U*ᵥx=equalityRoot k • x := by
      change (U-equalityRoot k • 1)*ᵥx=0 at hux
      simpa [Matrix.sub_mulVec,Matrix.smul_mulVec] using hux
    have hp : rootProjection U hU k*ᵥx=x := by
      have h := finiteCalc_eigenvector U hU (fun z => if z=equalityRoot k then 1 else 0)
        (equalityRoot k) x he
      simpa [rootProjection,finiteSpectralProjection] using h
    refine ⟨v,?_⟩
    rw [Matrix.mulVecLin_apply,← Matrix.mulVec_mulVec,hv,hp]

theorem adjoint_intertwiner (U : Mat ι) (T : Matrix ι ν ℂ) (W : Mat ν)
    (hU : UnitaryRel U) (hW : UnitaryRel W) (h : U*T=T*W) : U.conjTranspose*T=T*W.conjTranspose := by
  have he := congrArg (fun Q : Matrix ι ν ℂ => U.conjTranspose*Q*W.conjTranspose) h
  simpa [mul_assoc,hU.1,hW.2] using he.symm

/-- The reflection hypotheses are obtained from Bob's order-d measurements and
the adjacent scalar phases. No reflection-rank condition is assumed. -/
theorem quantum_root_rank_lower (hd : 2≤d)
    {κ : Type*} [Fintype κ] [DecidableEq κ]
    (s : StrategyOn d (Fin 2) (AugmentedInputs d) ι κ)
    (hs : firstValue s=scalarMaximum d+1) (k : Ix d) :
    let U := (encoded (s.alice 0)).conjTranspose*encoded (s.alice 1)
    let hU := (encoded_unitary (s.alice 0)).adjoint.mul (encoded_unitary (s.alice 1))
    let T := aliceAmplitude (stateFactor s.state)
    T.rank≤d*(rootProjection U hU k*T).rank := by
  dsimp only
  let A := encoded (s.alice 0)
  let U := A.conjTranspose*encoded (s.alice 1)
  let hU := (encoded_unitary (s.alice 0)).adjoint.mul (encoded_unitary (s.alice 1))
  let T := aliceAmplitude (stateFactor s.state)
  let B := fun y : Ix d => bobRight (ε := ι × κ) (encoded (s.bob (some y)))
  let y : Ix d := reflectionLabel d-k
  let V := A*supportedPhase U hU y
  let E := rootProjection U hU k
  let η := cis (Real.pi/(d : ℝ))
  obtain ⟨hE,_,_,hV,_⟩ := quantum_supported_routing hd s hs
  have hy : reflectionLabel d-y=k := by unfold y; ring
  have hr0 := congrArg (fun Q : Matrix ι (κ × (ι × κ)) ℂ => A*Q)
    (supported_adjacent_reflection hd U hU T hE y)
  rw [hy] at hr0
  have hr : (V*(1-2 • E))*T=T*(η⁻¹ • (B (y+1)).conjTranspose) := by
    have hn : η≠0 := cis_ne_zero _
    have hscaled := congrArg (fun Q : Matrix ι (κ × (ι × κ)) ℂ => η⁻¹ • Q) hr0
    simpa [V,E,η,mul_assoc,mul_smul_comm,smul_smul,hn,hV (y+1)] using hscaled.symm
  have hb (t : Ix d) : (B t).conjTranspose^d=1 := by
    rw [← Matrix.conjTranspose_pow,bobRight_order (encoded_order (s.bob (some t))),Matrix.conjTranspose_one]
  have hd' : (η⁻¹ • (B (y+1)).conjTranspose)^d=-1 := by
    rw [smul_pow,hb,inv_pow,reflection_phase_power]
    norm_num
  exact relative_reflection_rank d V E T (B y).conjTranspose
    (η⁻¹ • (B (y+1)).conjTranspose) (hV y) hr (hb y) hd'

/-- Full supported-multiplicity theorem, phrased using the actual reduced
state support. Equal roots have positive, equal eigenspace multiplicity. -/
theorem supported_multiplicity_rigidity (hd : 2≤d)
    {κ : Type*} [Fintype κ] [DecidableEq κ]
    (s : StrategyOn d (Fin 2) (AugmentedInputs d) ι κ)
    (hs : firstValue s=2/Real.sin (Real.pi/(2*d))+1) :
    let U := (encoded (s.alice 0)).conjTranspose*encoded (s.alice 1)
    preservesRange U (aliceSupport s.state) ∧
    preservesRange U.conjTranspose (aliceSupport s.state) ∧
    ∃ r : ℕ,0<r ∧
      (∀ k : Ix d,Module.finrank ℂ (aliceSupport s.state ⊓
        LinearMap.ker (U-equalityRoot k • 1).mulVecLin)=r) ∧
      Module.finrank ℂ (aliceSupport s.state)=d*r := by
  dsimp only
  let A := encoded (s.alice 0)
  let U := A.conjTranspose*encoded (s.alice 1)
  let hU := (encoded_unitary (s.alice 0)).adjoint.mul (encoded_unitary (s.alice 1))
  let T := aliceAmplitude (stateFactor s.state)
  let D := bobRight (ε := ι × κ) (encoded (s.bob none))
  let B := bobRight (ε := ι × κ) (encoded (s.bob (some (0 : Ix d))))
  let W := (D*B.conjTranspose)^2
  have hW : UnitaryRel W := ((bobRight_unitary (encoded_unitary _)).mul
    (bobRight_unitary (encoded_unitary _)).adjoint).pow 2
  obtain ⟨hE,_,_,_,hUT⟩ := quantum_supported_routing hd s hs
  have hK : aliceSupport s.state=matrixRange T := aliceSupport_amplitude s.state
  have hpres := preserves_of_intertwiner T U W hUT
  have hpres' := preserves_of_intertwiner T U.conjTranspose W.conjTranspose
    (adjoint_intertwiner U T W hU hW hUT)
  refine ⟨hK.symm ▸ hpres,hK.symm ▸ hpres',?_⟩
  let r : Ix d → ℕ := fun k => (rootProjection U hU k*T).rank
  have hsum : (∑ k,r k)=T.rank := sum_supported_projection_ranks (rootProjection U hU) T
    (rootProjection_sum_on_support hd U hU T hE) (rootProjection_orthogonal U hU)
    (rootProjection_preserves_support hd U hU T W hE hUT)
  have hlo (k : Ix d) : T.rank≤d*r k := quantum_root_rank_lower hd s hs k
  obtain ⟨heq,hconst,_⟩ := equal_ranks_from_lower_bounds T.rank r hsum hlo
  have hn : 0<T.rank := by
    have hk : matrixRange T≠⊥ := hK ▸ aliceSupport_nonzero s.state
    exact Submodule.finrank_pos.mpr hk
  have hr : 0<r 0 := by
    have h := heq 0
    by_contra hnot
    have hz : r 0=0 := by omega
    rw [hz,mul_zero] at h
    omega
  refine ⟨r 0,hr,?_,?_⟩
  · intro k
    rw [hK,← rootProjection_range_eigenspace hd U hU T W hE hUT k]
    exact hconst k 0
  · rw [hK]
    exact heq 0

/-- The advertised divisibility is now a corollary of the complete chain. -/
theorem supported_dimension_divisible (hd : 2≤d)
    {κ : Type*} [Fintype κ] [DecidableEq κ]
    (s : StrategyOn d (Fin 2) (AugmentedInputs d) ι κ)
    (hs : firstValue s=2/Real.sin (Real.pi/(2*d))+1) :
    d∣Module.finrank ℂ (aliceSupport s.state) := by
  obtain ⟨_,_,r,_,_,he⟩ := supported_multiplicity_rigidity hd s hs
  exact ⟨r,he⟩

end CyclicBell.General
