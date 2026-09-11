import Bell.StrategyMaps
import Bell.DeterministicInput

/-!
# Finite balanced Lorentz-cone circuits

A normalized nonnegative balance in a three-dimensional cone section lies in
the closed convex hull of balances having at most two active rays on either
side. The target hull used below is already compact, so its closure adds no
behaviors. The proof is a finite-dimensional extreme-point argument with exact
support counts, not numerical circuit enumeration.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder Topology
open Set Filter
namespace Bell.ConeCircuits
open Bell Lorentz QubitGeometry
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

private theorem fin_two_cases (x : Fin 2) : x=0 ∨ x=1 := by
  fin_cases x <;> simp

def sign (x : Fin 2) : ℝ := if x=0 then 1 else -1

def balance (v : ι → V) (side : ι → Fin 2) : (ι → ℝ) →ₗ[ℝ] V where
  toFun w := ∑ i, (sign (side i)*w i) • v i
  map_add' := by intros; simp [mul_add,add_smul,Finset.sum_add_distrib]
  map_smul' := by
    intro t w
    change (∑ i, (sign (side i) * (t * w i)) • v i) =
      t • ∑ i, (sign (side i) * w i) • v i
    rw [Finset.smul_sum]
    apply Finset.sum_congr rfl
    intro i _
    rw [smul_smul]
    congr 1
    ring

def mass (v : ι → V) : (ι → ℝ) →ₗ[ℝ] ℝ where
  toFun w := ∑ i, w i*(v i) 0
  map_add' := by intros; simp [add_mul,Finset.sum_add_distrib]
  map_smul' := by intros; simp [smul_eq_mul,mul_assoc,Finset.mul_sum]

def Weights (v : ι → V) (side : ι → Fin 2) : Set (ι → ℝ) :=
  {w | (∀ i, 0 ≤ w i) ∧ balance v side w=0 ∧ mass v w=1}

def sideSum (v : ι → V) (side : ι → Fin 2) (w : ι → ℝ) (x : Fin 2) : V :=
  ∑ i, if side i=x then w i • v i else 0

def support (w : ι → ℝ) : Finset ι := Finset.univ.filter (fun i => 0 < w i)

def sideSupport (side : ι → Fin 2) (w : ι → ℝ) (x : Fin 2) : Finset ι :=
  (support w).filter (fun i => side i=x)

theorem weights_convex (v : ι → V) (side : ι → Fin 2) : Convex ℝ (Weights v side) := by
  intro w hw z hz a b ha hb hab
  refine ⟨fun i => add_nonneg (mul_nonneg ha (hw.1 i)) (mul_nonneg hb (hz.1 i)), ?_, ?_⟩
  · simp only [map_add,map_smul,hw.2.1,hz.2.1,smul_zero,add_zero]
  · simp only [map_add,map_smul,hw.2.2,hz.2.2,smul_eq_mul,mul_one,hab]

theorem weights_isClosed (v : ι → V) (side : ι → Fin 2) : IsClosed (Weights v side) := by
  unfold Weights
  have hn : IsClosed {w : ι → ℝ | ∀ i, 0 ≤ w i} := by
    simpa only [Set.setOf_forall] using
      isClosed_iInter fun i : ι =>
        isClosed_le (continuous_const : Continuous fun _ : ι → ℝ => (0 : ℝ))
          (continuous_apply i)
  exact hn.inter
    ((isClosed_eq (by unfold balance; fun_prop) continuous_const).inter
      (isClosed_eq (by unfold mass; fun_prop) continuous_const))

theorem weights_isCompact (v : ι → V) (side : ι → Fin 2)
    (ht : ∀ i, 0 < (v i) 0) : IsCompact (Weights v side) := by
  have hb : IsCompact {w : ι → ℝ | ∀ i, w i ∈ Icc 0 ((v i) 0)⁻¹} :=
    isCompact_pi_infinite fun i => isCompact_Icc
  apply hb.of_isClosed_subset (weights_isClosed v side)
  intro w hw i
  refine ⟨hw.1 i, ?_⟩
  have he : w i*(v i) 0 ≤ 1 := by
    rw [← hw.2.2]
    exact Finset.single_le_sum (fun j _ => mul_nonneg (hw.1 j) (ht j).le) (Finset.mem_univ i)
  have he' := (le_div_iff₀ (ht i)).mpr he
  simpa only [one_div] using he'

theorem balance_sideSum (v : ι → V) (side : ι → Fin 2) (w : ι → ℝ) :
    balance v side w=sideSum v side w 0-sideSum v side w 1 := by
  rw [sideSum,sideSum,← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro i _
  rcases fin_two_cases (side i) with hi|hi <;> simp [balance,sign,hi]

theorem mass_sideSum (v : ι → V) (side : ι → Fin 2) (w : ι → ℝ) :
    mass v w=(sideSum v side w 0) 0+(sideSum v side w 1) 0 := by
  simp only [sideSum,Finset.sum_apply,← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  rcases fin_two_cases (side i) with hi|hi <;> simp [mass,Pi.smul_apply,smul_eq_mul,hi]

theorem sideSum_equal {v : ι → V} {side : ι → Fin 2} {w : ι → ℝ}
    (hw : w ∈ Weights v side) : sideSum v side w 0=sideSum v side w 1 := by
  exact sub_eq_zero.mp ((balance_sideSum v side w).symm.trans hw.2.1)

theorem sideSum_time_half {v : ι → V} {side : ι → Fin 2} {w : ι → ℝ}
    (hw : w ∈ Weights v side) (x : Fin 2) : (sideSum v side w x) 0=1/2 := by
  have he := congrFun (sideSum_equal hw) 0
  have hm := mass_sideSum v side w
  rw [hw.2.2] at hm
  fin_cases x <;> dsimp at * <;> linarith

theorem sideSupport_nonempty {v : ι → V} {side : ι → Fin 2} {w : ι → ℝ}
    (hw : w ∈ Weights v side) (x : Fin 2) : (sideSupport side w x).Nonempty := by
  by_contra hn
  have hz : ∀ i, side i=x → w i=0 := by
    intro i hi
    have hnot : ¬0<w i := by
      intro hp
      exact hn ⟨i,by simp [sideSupport,support,hi,hp]⟩
    exact le_antisymm (not_lt.mp hnot) (hw.1 i)
  have he := sideSum_time_half hw x
  have hs : sideSum v side w x=0 := by
    apply Finset.sum_eq_zero
    intro i _
    by_cases hi : side i=x <;> simp [hi,hz i]
  simp [hs] at he

/-- An extreme balance has no nonzero relation supported on its positive weights. -/
theorem extreme_relation_zero (v : ι → V) (side : ι → Fin 2) (w : ι → ℝ)
    (hext : w ∈ Set.extremePoints ℝ (Weights v side))
    (d : ι → ℝ) (hsupp : ∀ i, w i=0 → d i=0)
    (hb : balance v side d=0) (hm : mass v d=0) : d=0 := by
  let c := fun i => d i/w i
  obtain ⟨ε,hε,_,_,hc⟩ := exists_positive_perturbation c
    (Matrix.PosDef.one : (1 : Operator).PosDef) (Matrix.isHermitian_zero : (0 : Operator).IsHermitian)
  have hpos (i : ι) : 0 ≤ w i+ε*d i ∧ 0 ≤ w i-ε*d i := by
    by_cases hi : w i=0
    · simp [hi,hsupp i hi]
    · have hw : 0 < w i := lt_of_le_of_ne (hext.1.1 i) (Ne.symm hi)
      have hp := mul_nonneg hw.le (hc i).1.le
      have hm := mul_nonneg hw.le (hc i).2.le
      dsimp [c] at hp hm
      field_simp [hi] at hp hm
      constructor <;> nlinarith
  have hp : w+ε • d ∈ Weights v side := by
    refine ⟨fun i => (hpos i).1, ?_, ?_⟩ <;>
      simp [map_add,map_smul,hb,hm,hext.1.2.1,hext.1.2.2]
  have hn : w-ε • d ∈ Weights v side := by
    refine ⟨fun i => (hpos i).2, ?_, ?_⟩ <;>
      simp [map_sub,map_smul,hb,hm,hext.1.2.1,hext.1.2.2]
  have he := (extreme_midpoint hext hp hn (by module)).1
  funext i
  have hi := congrFun he i
  simp only [Pi.add_apply,Pi.smul_apply,smul_eq_mul] at hi
  have hdi : ε*d i=0 := by linarith
  exact (mul_eq_zero.mp hdi).resolve_left hε.ne'

/-- A three-dimensional cone section has at most four active circuit rays. -/
theorem extreme_support_le_four (v : ι → V) (side : ι → Fin 2)
    (H : Submodule ℝ V) (hvH : ∀ i, v i ∈ H) (hH : Module.finrank ℝ H ≤ 3)
    (w : ι → ℝ) (hext : w ∈ Set.extremePoints ℝ (Weights v side)) :
    (support w).card ≤ 4 := by
  classical
  let I := {i : ι // 0<w i}
  let extend : (I → ℝ) →ₗ[ℝ] (ι → ℝ) :=
    { toFun := fun c i => if h : 0<w i then c ⟨i,h⟩ else 0
      map_add' := by intros; funext i; by_cases hi : 0 < w i <;> simp [hi]
      map_smul' := by intros; funext i; by_cases hi : 0 < w i <;> simp [hi] }
  let f : (I → ℝ) →ₗ[ℝ] (H × ℝ) :=
    { toFun := fun c => (⟨balance v side (extend c),
        H.sum_mem fun i _ => H.smul_mem _ (hvH i)⟩,mass v (extend c))
      map_add' := by intros; ext <;> simp [map_add]
      map_smul' := by intros; ext <;> simp [map_smul] }
  have hi : Function.Injective f := by
    intro c d h
    have hz : f (c-d)=0 := by rw [map_sub,h,sub_self]
    have hb := congrArg (fun p : H × ℝ => (p.1 : V)) hz
    have hm := congrArg Prod.snd hz
    have he := extreme_relation_zero v side w hext (extend (c-d))
      (by intro i hi; simp [extend,hi]) hb hm
    funext i
    have hci := congrFun he i
    apply sub_eq_zero.mp
    simpa [extend,i.property] using hci
  have hd := LinearMap.finrank_le_finrank_of_injective hi
  have hd' : Fintype.card I ≤ Module.finrank ℝ H+1 := by
    simpa using hd
  have hc : Fintype.card I=(support w).card := by simp [I,support,Fintype.card_subtype]
  omega

theorem future_nonnegative_smul {x : V} (hx : Future x) {t : ℝ} (ht : 0 ≤ t) : Future (t • x) := by
  rw [← pauli_posSemidef_iff,map_smul]
  exact posSemidef_real_smul ((pauli_posSemidef_iff x).mpr hx) ht

theorem future_sum {κ : Type*} [Fintype κ] (x : κ → V) (hx : ∀ k, Future (x k)) :
    Future (∑ k, x k) := by
  rw [← pauli_posSemidef_iff,map_sum]
  exact positive_sum _ fun k => (pauli_posSemidef_iff (x k)).mpr (hx k)

theorem sideSum_future {v : ι → V} {side : ι → Fin 2} {w : ι → ℝ}
    (hv : ∀ i, FutureNull (v i)) (hw : w ∈ Weights v side) (x : Fin 2) :
    Future (sideSum v side w x) := by
  apply future_sum
  intro i
  by_cases hi : side i=x
  · simpa [hi] using future_nonnegative_smul ⟨(hv i).1.le,(hv i).2.ge⟩ (hw.1 i)
  · simp [hi,Future,lorentzSquare]

private theorem singleton_side_sum {v : ι → V} {side : ι → Fin 2} {w : ι → ℝ}
    (hw : w ∈ Weights v side) {x : Fin 2} {i : ι}
    (hi : sideSupport side w x={i}) : sideSum v side w x=w i • v i := by
  have him : i ∈ sideSupport side w x := by simp [hi]
  have hit : side i=x := (Finset.mem_filter.mp him).2
  unfold sideSum
  rw [Finset.sum_eq_single i]
  · simp [hit]
  · intro j _ hji
    by_cases hj : side j=x
    · have hwj : w j=0 := by
        have hnot : ¬0<w j := by
          intro hpos
          have hm : j ∈ sideSupport side w x := by simp [sideSupport,support,hj,hpos]
          simp [hi,hji] at hm
        exact le_antisymm (not_lt.mp hnot) (hw.1 j)
      simp [hj,hwj]
    · simp [hj]
  · simp

/-- If one side consists of one null ray, all rays of the opposite side have
that same direction. This excludes the putative 1-versus-3 extreme circuit. -/
theorem extreme_singleton_other_le_one (v : ι → V) (side : ι → Fin 2)
    (hv : ∀ i, FutureNull (v i)) (w : ι → ℝ)
    (hext : w ∈ Set.extremePoints ℝ (Weights v side))
    (x : Fin 2) (i : ι) (hi : sideSupport side w x={i}) :
    (sideSupport side w (otherInput x)).card ≤ 1 := by
  classical
  by_contra! hcard
  obtain ⟨j,hj,k,hk,hjk⟩ := Finset.one_lt_card.mp hcard
  have hji : 0<w j := (Finset.mem_filter.mp (Finset.mem_filter.mp hj).1).2
  have hki : 0<w k := (Finset.mem_filter.mp (Finset.mem_filter.mp hk).1).2
  have hjs : side j=otherInput x := (Finset.mem_filter.mp hj).2
  have hks : side k=otherInput x := (Finset.mem_filter.mp hk).2
  have him : i ∈ sideSupport side w x := by simp [hi]
  have hwi : 0<w i := (Finset.mem_filter.mp (Finset.mem_filter.mp him).1).2
  have hcommon : sideSum v side w (otherInput x)=w i • v i := by
    have hb := sideSum_equal hext.1
    have hs := singleton_side_sum hext.1 hi
    fin_cases x <;> simpa [otherInput] using (by first | exact hb.trans hs | exact hb.symm.trans hs)
  have hdir (l : ι) (hl : l ∈ sideSupport side w (otherInput x)) :
      v l=((v l) 0/(v i) 0) • v i := by
    have hwl : 0<w l := (Finset.mem_filter.mp (Finset.mem_filter.mp hl).1).2
    have hls := (Finset.mem_filter.mp hl).2
    have htotal : FutureNull (w i • v i) := by
      refine ⟨mul_pos hwi (hv i).1, ?_⟩
      calc
        lorentzSquare (w i • v i) = (w i)^2 * lorentzSquare (v i) := by
          simp only [lorentzSquare,Pi.smul_apply,smul_eq_mul]
          ring
        _ = 0 := by rw [(hv i).2,mul_zero]
    have hpart : Future (w l • v l) := future_nonnegative_smul
      ⟨(hv l).1.le,(hv l).2.ge⟩ hwl.le
    have hrest : Future (w i • v i-w l • v l) := by
      have hs : w i • v i-w l • v l=
          ∑ a : {a : ι // a ≠ l}, if side a=otherInput x then w a • v a else 0 := by
        rw [← hcommon]
        have ht := Fintype.sum_eq_add_sum_subtype_ne
          (fun a => if side a=otherInput x then w a • v a else 0) l
        simpa [sideSum,hls] using (eq_sub_of_add_eq' ht.symm).symm
      rw [hs]
      apply future_sum
      intro a
      by_cases ha : side a=otherInput x
      · simpa [ha] using future_nonnegative_smul
          ⟨(hv a).1.le,(hv a).2.ge⟩ (hext.1.1 a)
      · simp [ha,Future,lorentzSquare]
    have he := future_between_null htotal hpart hrest
    ext a
    have hea := congrFun he a
    simp only [Pi.smul_apply,smul_eq_mul] at hea ⊢
    field_simp [hwi.ne',(hv i).1.ne',hwl.ne'] at hea ⊢
    apply mul_left_cancel₀ (mul_ne_zero hwl.ne' hwi.ne')
    calc
      (w l * w i) * (v l a * v i 0) = w l * v l a * (w i * v i 0) := by ring
      _ = w l * v l 0 * (w i * v i a) := hea
      _ = (w l * w i) * (v l 0 * v i a) := by ring
  have hrel : (v k) 0 • v j=(v j) 0 • v k := by
    rw [hdir j hj,hdir k hk]
    ext a
    simp only [Pi.smul_apply,smul_eq_mul]
    field_simp [(hv i).1.ne']
    <;> ring
  let d : ι → ℝ := fun a => (if a=j then (v k) 0 else 0)-(if a=k then (v j) 0 else 0)
  have hd : d=0 := by
    apply extreme_relation_zero v side w hext d
    · intro a ha
      have haj : a ≠ j := by intro h; subst a; linarith
      have hak : a ≠ k := by intro h; subst a; linarith
      simp [d,haj,hak]
    · simp [d,balance,sub_smul,mul_sub,Finset.sum_sub_distrib,hjs,hks,← mul_smul]
      rw [mul_smul,mul_smul,hrel,sub_self]
    · simp [d,mass,sub_mul,Finset.sum_sub_distrib,hjk,Ne.symm hjk]
      ring
  have hj0 := congrFun hd j
  simp [d,hjk] at hj0
  exact (hv k).1.ne' hj0

theorem side_card_sum (side : ι → Fin 2) (w : ι → ℝ) :
    (sideSupport side w 0).card+(sideSupport side w 1).card=(support w).card := by
  have hd : Disjoint (sideSupport side w 0) (sideSupport side w 1) := by
    apply Finset.disjoint_left.mpr
    intro i hi hj
    have h0 := (Finset.mem_filter.mp hi).2
    have h1 := (Finset.mem_filter.mp hj).2
    have : (0 : Fin 2)=1 := h0.symm.trans h1
    exact (by decide : (0 : Fin 2) ≠ 1) this
  have hu : sideSupport side w 0 ∪ sideSupport side w 1=support w := by
    ext i
    rcases fin_two_cases (side i) with hi|hi <;> simp [sideSupport,hi]
  rw [← hu,Finset.card_union_of_disjoint hd]

theorem extreme_side_card_le_two (v : ι → V) (side : ι → Fin 2)
    (hv : ∀ i, FutureNull (v i)) (H : Submodule ℝ V)
    (hvH : ∀ i, v i ∈ H) (hH : Module.finrank ℝ H ≤ 3)
    (w : ι → ℝ) (hext : w ∈ Set.extremePoints ℝ (Weights v side)) :
    ∀ x, (sideSupport side w x).card ≤ 2 := by
  have htot := extreme_support_le_four v side H hvH hH w hext
  have hs := side_card_sum side w
  have hn0 := Finset.card_pos.mpr (sideSupport_nonempty hext.1 0)
  have hn1 := Finset.card_pos.mpr (sideSupport_nonempty hext.1 1)
  intro x
  by_contra! hx
  have hother : (sideSupport side w (otherInput x)).card=1 := by
    rcases fin_two_cases x with rfl | rfl
    · change (sideSupport side w 1).card = 1
      omega
    · change (sideSupport side w 0).card = 1
      omega
  obtain ⟨i,hi⟩ := Finset.card_eq_one.mp hother
  have he := extreme_singleton_other_le_one v side hv w hext (otherInput x) i hi
  have hoo : otherInput (otherInput x)=x := by fin_cases x <;> rfl
  rw [hoo] at he
  omega

/-- Transfer every balance into any closed convex target containing the binary
circuits. Applied below to the ACTUAL compact PVM hull, not an abstract simulator. -/
theorem all_weights_map_into {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (v : ι → V) (side : ι → Fin 2) (hv : ∀ i, FutureNull (v i))
    (H : Submodule ℝ V) (hvH : ∀ i, v i ∈ H) (hH : Module.finrank ℝ H ≤ 3)
    (f : (ι → ℝ) →ₗ[ℝ] E) (S : Set E) (hS : Convex ℝ S) (hSc : IsClosed S)
    (hbinary : ∀ w ∈ Weights v side, (∀ x, (sideSupport side w x).card ≤ 2) → f w ∈ S) :
    ∀ w ∈ Weights v side, f w ∈ S := by
  have hc : Convex ℝ {w | f w ∈ S} := by
    intro w hw z hz a b ha hb hab
    change f (a • w+b • z) ∈ S
    rw [map_add,map_smul,map_smul]
    exact hS hw hz ha hb hab
  have hclosed : IsClosed {w | f w ∈ S} := hSc.preimage f.continuous_of_finiteDimensional
  exact contains_compact_of_contains_extreme
    (weights_isCompact v side (fun i => (hv i).1)) (weights_convex v side) hc hclosed
    (fun w hw => hbinary w hw.1 (extreme_side_card_le_two v side hv H hvH hH w hw))

end Bell.ConeCircuits

end


/-!
# Binary cone circuits give complete fixed-qubit PVM behaviors

Circuit outcomes are initially refined by the finite ray index. Whitening the
common reduced state produces at most two nonzero rank-one effects per input,
hence an actual PVM. The refined outcomes are then coarsened back to their
original declared labels. Singular reduced states use the explicit product model.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder
namespace Bell.ConeCircuits
open Bell Lorentz QubitGeometry
variable {ι : Type*} [Fintype ι] [DecidableEq ι]
variable (AO BO : Fin 2 → ℕ)
variable (N : (y : Fin 2) → PVM (BO y))
variable (v : ι → V) (side : ι → Fin 2)
variable (label : (i : ι) → Fin (AO (side i)))
variable (fallback : (x : Fin 2) → Fin (AO x))

def declaredLabel (x : Fin 2) (i : ι) : Fin (AO x) :=
  if h : side i=x then Fin.cast (congrArg AO h) (label i) else fallback x

def outcomeVector (w : ι → ℝ) (x : Fin 2) (a : Fin (AO x)) : V :=
  ∑ i, if side i=x ∧ declaredLabel AO side label fallback x i=a then w i • v i else 0

theorem outcomeVector_sum (w : ι → ℝ) (x : Fin 2) :
    (∑ a, outcomeVector AO v side label fallback w x a)=sideSum v side w x := by
  simp only [outcomeVector]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  by_cases hi : side i=x <;> simp [hi]

/-- The linear map keeps both inputs and all original output labels. -/
def behaviorMap : (ι → ℝ) →ₗ[ℝ] Behavior ⟨2,2,AO,BO⟩ where
  toFun w x y a b := localTrace ((N y).effect b)
    (pauli (outcomeVector AO v side label fallback w x a))
  map_add' := by
    intro w z
    funext x y a b
    unfold outcomeVector
    have he : (∑ i, if side i=x ∧ declaredLabel AO side label fallback x i=a then
        (w i+z i) • v i else 0) =
      (∑ i, if side i=x ∧ declaredLabel AO side label fallback x i=a then w i • v i else 0)+
      (∑ i, if side i=x ∧ declaredLabel AO side label fallback x i=a then z i • v i else 0) := by
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro i _
      split_ifs <;> simp [add_smul]
    simp only [Pi.add_apply,he,map_add]
  map_smul' := by
    intro t w
    funext x y a b
    unfold outcomeVector
    have he : (∑ i, if side i=x ∧ declaredLabel AO side label fallback x i=a then
        (t*w i) • v i else 0) =
      t • (∑ i, if side i=x ∧ declaredLabel AO side label fallback x i=a then w i • v i else 0) := by
      rw [Finset.smul_sum]
      apply Finset.sum_congr rfl
      intro i _
      split_ifs <;> simp [mul_smul]
    simp only [Pi.smul_apply,smul_eq_mul,he,map_smul,RingHom.id_apply]

/-- The same table viewed as an assemblage on the fixed binary-measurement party. -/
def circuitAssemblage (hv : ∀ i, FutureNull (v i)) (w : ι → ℝ)
    (hw : w ∈ Weights v side) : Assemblage ⟨2,2,BO,AO⟩ where
  alice y := (N y).toPOVM
  reduced := pauli (sideSum v side w 0)
  reducedPositive := (pauli_posSemidef_iff _).mpr (sideSum_future hv hw 0)
  reducedNormalized := by rw [pauli_trace,sideSum_time_half hw]; norm_num
  steered x a := pauli (outcomeVector AO v side label fallback w x a)
  positive := by
    intro x a
    rw [outcomeVector,map_sum]
    apply positive_sum
    intro i
    by_cases hi : side i=x ∧ declaredLabel AO side label fallback x i=a
    · simpa [hi] using posSemidef_real_smul (hv i).posSemidef (hw.1 i)
    · simp [hi,Matrix.PosSemidef.zero]
  commonSum := by
    intro x
    rw [← map_sum,outcomeVector_sum]
    congr 1
    fin_cases x
    · rfl
    · exact (sideSum_equal hw).symm

/-- Refinement with one declared outcome for each finite ray index. -/
def refinedAssemblage (hv : ∀ i, FutureNull (v i)) (w : ι → ℝ)
    (hw : w ∈ Weights v side) : Assemblage ⟨2,2,BO,fun _ => Fintype.card ι⟩ where
  alice y := (N y).toPOVM
  reduced := pauli (sideSum v side w 0)
  reducedPositive := (pauli_posSemidef_iff _).mpr (sideSum_future hv hw 0)
  reducedNormalized := by rw [pauli_trace,sideSum_time_half hw]; norm_num
  steered x k := if side ((Fintype.equivFin ι).symm k)=x then
    w ((Fintype.equivFin ι).symm k) • pauli (v ((Fintype.equivFin ι).symm k)) else 0
  positive x k := by
    split_ifs
    · exact posSemidef_real_smul (hv _).posSemidef (hw.1 _)
    · exact Matrix.PosSemidef.zero
  commonSum := by
    intro x
    rw [Equiv.sum_comp (Fintype.equivFin ι).symm
      (fun i : ι => if side i=x then w i • pauli (v i) else 0)]
    have he : (∑ i, if side i=x then w i • pauli (v i) else 0)=pauli (sideSum v side w x) := by
      simp [sideSum,map_sum,map_smul,apply_ite]
    rw [he]
    congr 1
    fin_cases x
    · rfl
    · exact (sideSum_equal hw).symm

def coarsening : StrategyMap ⟨2,2,BO,fun _ => Fintype.card ι⟩ ⟨2,2,BO,AO⟩ where
  aliceInput := id
  bobInput := id
  aliceOutput := fun _ => id
  bobOutput x k := declaredLabel AO side label fallback x ((Fintype.equivFin ι).symm k)

theorem coarsening_refined_behavior (hv : ∀ i, FutureNull (v i)) (w : ι → ℝ)
    (hw : w ∈ Weights v side) :
    (coarsening AO BO side label fallback).behavior
      (refinedAssemblage BO N v side hv w hw).behavior =
      (circuitAssemblage AO BO N v side label fallback hv w hw).behavior := by
  classical
  funext y x b a
  change (∑ c, ∑ k, if c=b ∧ declaredLabel AO side label fallback x
      ((Fintype.equivFin ι).symm k)=a then
      localTrace ((N y).effect c)
        (if side ((Fintype.equivFin ι).symm k)=x then
          w ((Fintype.equivFin ι).symm k) • pauli (v ((Fintype.equivFin ι).symm k)) else 0)
      else 0) = _
  rw [Finset.sum_eq_single b]
  · simp only [and_true,true_and]
    rw [Equiv.sum_comp (Fintype.equivFin ι).symm
      (fun i : ι => if declaredLabel AO side label fallback x i=a then
        localTrace ((N y).effect b) (if side i=x then w i • pauli (v i) else 0) else 0)]
    change _=localTrace ((N y).effect b) (pauli (outcomeVector AO v side label fallback w x a))
    rw [outcomeVector,map_sum,map_sum]
    apply Finset.sum_congr rfl
    intro i _
    by_cases hi : side i=x <;> by_cases hl : declaredLabel AO side label fallback x i=a <;>
      simp [hi,hl,map_smul]
  · intro c _ hcb
    simp [hcb]
  · simp

/-- At most two active null components become projective after common-state
whitening. No arbitrary-output effect is assumed itself projective beforehand. -/
def binaryRefinedProjective (hv : ∀ i, FutureNull (v i)) (w : ι → ℝ)
    (hw : w ∈ Weights v side) (hbinary : ∀ x, (sideSupport side w x).card ≤ 2)
    (hdet : IsUnit (pauli (sideSum v side w 0)).det) :
    ProjectiveStrategy ⟨2,2,BO,fun _ => Fintype.card ι⟩ := by
  classical
  let a := refinedAssemblage BO N v side hv w hw
  refine ⟨(a.purifiedStrategy hdet).state,N,fun x => ?_⟩
  let M := a.purifiedBob hdet x
  have hnull : ∀ k, (M.effect k).det=0 := by
    intro k
    change ((a.root⁻¹ * (if side ((Fintype.equivFin ι).symm k)=x then
        w ((Fintype.equivFin ι).symm k) • pauli (v ((Fintype.equivFin ι).symm k)) else 0) *
        a.root⁻¹.conjTranspose).transpose).det=0
    split_ifs
    · simp [Matrix.det_mul,Matrix.det_smul,pauli_det,(hv _).2]
    · simp
  have hsub : ∀ k, M.effect k ≠ 0 →
      (Fintype.equivFin ι).symm k ∈ sideSupport side w x := by
    intro k hk
    have hs : side ((Fintype.equivFin ι).symm k)=x := by
      by_contra hn
      apply hk
      simp [M,Assemblage.purifiedBob,a,refinedAssemblage,hn]
    have hp : 0<w ((Fintype.equivFin ι).symm k) := by
      by_contra! hn
      have hz := le_antisymm hn (hw.1 _)
      apply hk
      simp [M,Assemblage.purifiedBob,a,refinedAssemblage,hs,hz]
    simp [sideSupport,support,hs,hp]
  have hcard : (Finset.univ.filter (fun k => M.effect k ≠ 0)).card ≤ 2 := by
    let f : {k : Fin (Fintype.card ι) // M.effect k ≠ 0} →
        {i // i ∈ sideSupport side w x} := fun k => ⟨(Fintype.equivFin ι).symm k,hsub k k.property⟩
    have hi : Function.Injective f := by
      intro k l h
      apply Subtype.ext
      exact (Fintype.equivFin ι).symm.injective (congrArg Subtype.val h)
    have hc : Fintype.card {k : Fin (Fintype.card ι) // M.effect k ≠ 0} ≤
        (sideSupport side w x).card := by
      simpa only [Fintype.card_coe] using Fintype.card_le_of_injective f hi
    simpa [Fintype.card_subtype] using hc.trans (hbinary x)
  exact M.toPVMOfTwoNull hnull hcard

theorem binary_circuit_mem_convexPVM (hv : ∀ i, FutureNull (v i)) (w : ι → ℝ)
    (hw : w ∈ Weights v side) (hbinary : ∀ x, (sideSupport side w x).card ≤ 2) :
    behaviorMap AO BO N v side label fallback w ∈ convexPVM ⟨2,2,AO,BO⟩ := by
  classical
  let a := circuitAssemblage AO BO N v side label fallback hv w hw
  have he : swapBehavior ⟨2,2,BO,AO⟩ a.behavior = behaviorMap AO BO N v side label fallback w := rfl
  have hs : a.behavior ∈ convexPVM ⟨2,2,BO,AO⟩ := by
    by_cases hd : a.reduced.det=0
    · exact a.singular_mem_convexPVM hd
    · let hu : IsUnit (pauli (sideSum v side w 0)).det := isUnit_iff_ne_zero.mpr hd
      let r := refinedAssemblage BO N v side hv w hw
      let p := binaryRefinedProjective BO N v side hv w hw hbinary hu
      have hbeh : p.toStrategy.behavior=r.behavior := r.purified_behavior hu
      have hp : r.behavior ∈ convexPVM ⟨2,2,BO,fun _ => Fintype.card ι⟩ :=
        subset_convexHull ℝ _ ⟨p,hbeh⟩
      have hmap := (coarsening AO BO side label fallback).mem_convexPVM hp
      rw [coarsening_refined_behavior] at hmap
      exact hmap
  rw [← he]
  exact swap_mem_convexPVM hs

/-- The whole balanced cone section, not only its sparse extreme points, gives
finite shared-randomness mixtures of fixed-qubit PVM strategies. -/
theorem circuit_section_mem_convexPVM
    (hv : ∀ i, FutureNull (v i)) (H : Submodule ℝ V)
    (hvH : ∀ i, v i ∈ H) (hH : Module.finrank ℝ H ≤ 3)
    (w : ι → ℝ) (hw : w ∈ Weights v side) :
    behaviorMap AO BO N v side label fallback w ∈ convexPVM ⟨2,2,AO,BO⟩ :=
  all_weights_map_into v side hv H hvH hH (behaviorMap AO BO N v side label fallback)
    (convexPVM ⟨2,2,AO,BO⟩) (convex_convexHull ℝ _) (convexPVM_isClosed _)
    (binary_circuit_mem_convexPVM AO BO N v side label fallback hv) w hw

end Bell.ConeCircuits
