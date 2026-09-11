import Bell.ConeCircuits

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
