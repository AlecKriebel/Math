import Bell.ConeCompression

/-!
# One-binary-party simulation for complete finite output architectures

Both binary measurements are retained as PVMs. The other party's entire
steered assemblage is compressed and split once, then a single balanced cone
polytope supplies the common-randomness mixture for BOTH inputs simultaneously.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder
namespace Bell
open Lorentz QubitGeometry

private theorem effectSpan_rank_le_support {n : ℕ} (N : POVM n) :
    Module.finrank ℝ (effectSpan N) ≤ Fintype.card (EffectSupport N) := by
  have h := (activeEffectMap N).finrank_range_add_finrank_ker
  simp only [Module.finrank_fintype_fun_eq_card,← effectSpan] at h
  omega

theorem binary_span_sum_le_three (BO : Fin 2 → ℕ) (N : (y : Fin 2) → PVM (BO y))
    (hc : ∀ y, Fintype.card (EffectSupport (N y).toPOVM) ≤ 2) :
    Module.finrank ℝ (effectSpan (N 0).toPOVM ⊔ effectSpan (N 1).toPOVM) ≤ 3 := by
  let S := effectSpan (N 0).toPOVM
  let T := effectSpan (N 1).toPOVM
  have hS : Module.finrank ℝ S ≤ 2 := (effectSpan_rank_le_support _).trans (hc 0)
  have hT : Module.finrank ℝ T ≤ 2 := (effectSpan_rank_le_support _).trans (hc 1)
  have hi : 0 < Module.finrank ℝ (S ⊓ T) := by
    by_contra! h
    have hz : Module.finrank ℝ (S ⊓ T)=0 := by omega
    have he := Submodule.finrank_eq_zero.mp hz
    have hu : timeUnit ∈ S ⊓ T := ⟨timeUnit_mem_effectSpan _,timeUnit_mem_effectSpan _⟩
    rw [he] at hu
    have h0 := congrFun hu 0
    norm_num [timeUnit] at h0
  have hsum := S.finrank_sup_add_finrank_inf_eq T
  omega

def PieceIndex (AO : Fin 2 → ℕ) := (x : Fin 2) × (Fin (AO x) × Fin 2)

private def pieceVector (AO BO : Fin 2 → ℕ) (a : Assemblage ⟨2,2,BO,AO⟩)
    (n d : V) (j : PieceIndex AO) : V :=
  nullPiece d (compress n (coordinates (a.steered j.1 j.2.1))) j.2.2

/-- Deleting zero split pieces and regrouping by the original input/output
returns exactly the compressed steered effect. -/
private theorem regroup_live_pieces (AO BO : Fin 2 → ℕ)
    (a : Assemblage ⟨2,2,BO,AO⟩) (n d : V)
    (fallback : (x : Fin 2) → Fin (AO x)) (x : Fin 2) (b : Fin (AO x)) :
    ConeCircuits.outcomeVector AO
      (fun j : {j : PieceIndex AO // pieceVector AO BO a n d j ≠ 0} => pieceVector AO BO a n d j)
      (fun j => j.val.1) (fun j => j.val.2.1) fallback (fun _ => 1) x b =
      compress n (coordinates (a.steered x b)) := by
  classical
  unfold ConeCircuits.outcomeVector
  rw [Fintype.sum_subtype]
  have hremove : (∑ j : PieceIndex AO, if h : pieceVector AO BO a n d j ≠ 0 then
      (if j.1=x ∧ ConeCircuits.declaredLabel AO (fun k => k.val.1)
        (fun k => k.val.2.1) fallback x ⟨j,h⟩=b then (1 : ℝ) • pieceVector AO BO a n d j else 0)
      else 0) =
      ∑ j : PieceIndex AO, if h : j.1=x then
        (if Fin.cast (congrArg AO h) j.2.1=b then pieceVector AO BO a n d j else 0) else 0 := by
    apply Finset.sum_congr rfl
    intro j _
    by_cases hz : pieceVector AO BO a n d j=0
    · simp [hz]
    · by_cases hi : j.1=x <;> simp [hz,hi,ConeCircuits.declaredLabel]
  rw [hremove]
  change (∑ j : (x : Fin 2) × (Fin (AO x) × Fin 2), _) = _
  rw [Fintype.sum_sigma]
  fin_cases x <;>
    simp [Fintype.sum_prod_type,Fin.sum_univ_succ,pieceVector,nullPiece_sum]

/-- A strategy with two binary-support PVMs on Bob is PVM-simulable for
arbitrary finite Alice outputs and arbitrary declared zero labels on Bob. -/
theorem binary_bob_simulation (AO BO : Fin 2 → ℕ) (s : Strategy ⟨2,2,AO,BO⟩)
    (N : (y : Fin 2) → PVM (BO y)) (hN : ∀ y, s.bob y=(N y).toPOVM)
    (hc : ∀ y, Fintype.card (EffectSupport (N y).toPOVM) ≤ 2) :
    s.behavior ∈ convexPVM ⟨2,2,AO,BO⟩ := by
  classical
  let a := (swapStrategy s).toAssemblage
  let S := effectSpan (N 0).toPOVM ⊔ effectSpan (N 1).toPOVM
  obtain ⟨n,hn0,hnunit,hnkill⟩ := exists_unit_annihilator S
    (binary_span_sum_le_three BO N hc) (le_sup_left (timeUnit_mem_effectSpan (N 0).toPOVM))
  obtain ⟨d,hd0,hdunit,hnd⟩ := exists_spatial_unit_perpendicular n
  have hnN : ∀ y b, dotProduct n (coordinates ((N y).effect b))=0 := by
    intro y b
    apply hnkill
    fin_cases y
    · exact le_sup_left (effect_coordinates_mem_span _ b)
    · exact le_sup_right (effect_coordinates_mem_span _ b)
  let I := {j : PieceIndex AO // pieceVector AO BO a n d j ≠ 0}
  let v : I → V := fun j => pieceVector AO BO a n d j
  let side : I → Fin 2 := fun j => j.val.1
  let label : (j : I) → Fin (AO (side j)) := fun j => j.val.2.1
  let fallback : (x : Fin 2) → Fin (AO x) := fun x => defaultOutput (s.alice x)
  have hv : ∀ j, FutureNull (v j) := by
    intro j
    rcases nullPiece_null_or_zero d hd0 hdunit
      (compress_future n hn0 hnunit (positive_coordinates (a.positive j.val.1 j.val.2.1))) j.val.2.2 with hz|hp
    · exact (j.property hz).elim
    · exact hp
  have hvH : ∀ j, v j ∈ LinearMap.ker (dotLinear n) := by
    intro j
    exact nullPiece_in_plane n d _ hn0 hnd (compress_orthogonal n _ hnunit) _
  have hregroup : ∀ x b, ConeCircuits.outcomeVector AO v side label fallback (fun _ => 1) x b =
      compress n (coordinates (a.steered x b)) := by
    exact regroup_live_pieces AO BO a n d fallback
  have hside : ∀ x, ConeCircuits.sideSum v side (fun _ => 1) x=compress n (coordinates a.reduced) := by
    intro x
    rw [← ConeCircuits.outcomeVector_sum AO v side label fallback]
    simp_rw [hregroup]
    rw [← map_sum,← map_sum,a.commonSum x]
  have htime : (coordinates a.reduced) 0=1/2 := by
    have ht := pauli_trace (coordinates a.reduced)
    rw [pauli_coordinates a.reducedPositive.isHermitian,a.reducedNormalized] at ht
    have he := congrArg Complex.re ht
    simp only [Complex.one_re,Complex.ofReal_re] at he
    linarith
  have hw : (fun _ : I => (1 : ℝ)) ∈ ConeCircuits.Weights v side := by
    refine ⟨fun _ => zero_le_one, ?_, ?_⟩
    · rw [ConeCircuits.balance_sideSum,hside,hside,sub_self]
    · rw [ConeCircuits.mass_sideSum,hside,hside,compress_time n _ hn0,htime]
      norm_num
  have hsim := ConeCircuits.circuit_section_mem_convexPVM AO BO N v side label fallback hv
    (LinearMap.ker (dotLinear n)) hvH (normalHyperplane_dim_le_three n hnunit) (fun _ => 1) hw
  have heq : ConeCircuits.behaviorMap AO BO N v side label fallback (fun _ => 1)=s.behavior := by
    funext x y b c
    change localTrace ((N y).effect c)
      (pauli (ConeCircuits.outcomeVector AO v side label fallback (fun _ => 1) x b))=s.behavior x y b c
    rw [hregroup]
    have hp : localTrace ((N y).effect c) (pauli (compress n (coordinates (a.steered x b))))=
        localTrace ((N y).effect c) (a.steered x b) := by
      rw [← pauli_coordinates ((N y).positive c).isHermitian,
        ← pauli_coordinates (a.positive x b).isHermitian]
      simp only [localTrace_apply,pauli_trace_product,Complex.ofReal_re,coordinates_pauli]
      rw [compress_pairing n _ _ (hnN y c)]
    rw [hp]
    have hb := congrFun (congrFun (congrFun (congrFun
      (swapStrategy s).toAssemblage_behavior y) x) c) b
    have hs := congrFun (congrFun (congrFun (congrFun (swapStrategy_behavior s) y) x) c) b
    change localTrace ((s.bob y).effect c) (a.steered x b)=_ at hb
    rw [hN y] at hb
    exact hb.trans hs
  rw [heq] at hsim
  exact hsim

/-- At an extreme full-rank behavior, an entire two-by-two active local
architecture is already a binary PVM architecture. -/
theorem extreme_binary_bob_simulation (AO BO : Fin 2 → ℕ)
    (s : FullPureStrategy ⟨2,2,AO,BO⟩)
    (hex : s.behavior ∈ Set.extremePoints ℝ (convexPOVM ⟨2,2,AO,BO⟩))
    (hnd : ∀ y, ¬ DeterministicMeasurement (s.bob y))
    (hc : ∀ y, Fintype.card (EffectSupport (s.bob y))=2) :
    s.behavior ∈ convexPVM ⟨2,2,AO,BO⟩ := by
  let N : (y : Fin 2) → PVM (BO y) := fun y =>
    (s.bob y).toPVMOfTwoNull
      (extreme_nondeterministic_effects_null s.swap (by rw [s.swap_behavior]; exact swap_extreme hex) y 0 (hnd y))
      (by simpa [Fintype.card_subtype] using (hc y).le)
  exact binary_bob_simulation AO BO s.toStrategy N (fun _ => rfl) (fun y => by simpa [N] using (hc y).le)

end Bell
