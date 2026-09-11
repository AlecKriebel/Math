import Bell.RankZero

/-!
# Retaining the labels in the rank-zero simulation

The five-ray permutation preserves the binary pair and ternary triple. Here it
is converted to actual permutations of the declared three-label alphabets,
fixing the unused binary label. Thus the rank-zero table is proved to belong to
the same fixed labelled physical PVM hull, rather than just an isomorphic hull.

Verification evidence: see CERTIFICATION.md and reports/kernel_report.json.
-/
noncomputable section
open scoped BigOperators Matrix
namespace Bell.Lorentz

variable (π : Equiv.Perm (Fin 5))
variable (hπ : ∀ j, (π j).val < 2 ↔ j.val < 2)

def binaryLabelMap (a : Fin 3) : Fin 3 :=
  if h : a.val < 2 then
    ⟨(π ⟨a.val,by omega⟩).val,by
      have hb := (hπ (⟨a.val,by omega⟩ : Fin 5)).mpr h
      omega⟩
  else 2

def ternaryLabelMap (a : Fin 3) : Fin 3 :=
  ⟨(π ⟨a.val+2,by omega⟩).val-2,by
    have hl := (π (⟨a.val+2,by omega⟩ : Fin 5)).isLt
    omega⟩

theorem binaryLabelMap_injective : Function.Injective (binaryLabelMap π hπ) := by
  intro a b hab
  by_cases ha : a.val < 2 <;> by_cases hb : b.val < 2
  · have hval := congrArg Fin.val hab
    simp only [binaryLabelMap,dif_pos ha,dif_pos hb] at hval
    have he : (⟨a.val,by omega⟩ : Fin 5) = ⟨b.val,by omega⟩ :=
      π.injective (Fin.ext hval)
    exact Fin.ext (congrArg (fun j : Fin 5 => j.val) he)
  · have hval := congrArg Fin.val hab
    simp only [binaryLabelMap,dif_pos ha,dif_neg hb] at hval
    have hbound := (hπ (⟨a.val,by omega⟩ : Fin 5)).mpr ha
    norm_num at hval
    omega
  · have hval := congrArg Fin.val hab
    simp only [binaryLabelMap,dif_neg ha,dif_pos hb] at hval
    have hbound := (hπ (⟨b.val,by omega⟩ : Fin 5)).mpr hb
    norm_num at hval
    omega
  · apply Fin.ext
    have hla := a.isLt; have hlb := b.isLt
    omega

include hπ in
theorem ternaryLabelMap_injective : Function.Injective (ternaryLabelMap π) := by
  intro a b hab
  have hval := congrArg Fin.val hab
  change (π (⟨a.val+2,by omega⟩ : Fin 5)).val-2 =
    (π (⟨b.val+2,by omega⟩ : Fin 5)).val-2 at hval
  have ha : 2 ≤ (π (⟨a.val+2,by omega⟩ : Fin 5)).val := by
    have h := hπ (⟨a.val+2,by omega⟩ : Fin 5)
    change (π (⟨a.val+2,by omega⟩ : Fin 5)).val < 2 ↔ a.val + 2 < 2 at h
    omega
  have hb : 2 ≤ (π (⟨b.val+2,by omega⟩ : Fin 5)).val := by
    have h := hπ (⟨b.val+2,by omega⟩ : Fin 5)
    change (π (⟨b.val+2,by omega⟩ : Fin 5)).val < 2 ↔ b.val + 2 < 2 at h
    omega
  have hval' : (π (⟨a.val+2,by omega⟩ : Fin 5)).val =
      (π (⟨b.val+2,by omega⟩ : Fin 5)).val := by omega
  have he := π.injective (Fin.ext hval')
  have he' := congrArg (fun j : Fin 5 => j.val) he
  change a.val + 2 = b.val + 2 at he'
  apply Fin.ext
  omega

def binaryLabelPerm : Equiv.Perm (Fin 3) :=
  Equiv.ofBijective (binaryLabelMap π hπ)
    ⟨binaryLabelMap_injective π hπ,
      Finite.surjective_of_injective (binaryLabelMap_injective π hπ)⟩

def ternaryLabelPerm : Equiv.Perm (Fin 3) :=
  Equiv.ofBijective (ternaryLabelMap π)
    ⟨ternaryLabelMap_injective π hπ,
      Finite.surjective_of_injective (ternaryLabelMap_injective π hπ)⟩

def blockLabelPerm (x : Fin 2) : Equiv.Perm (Fin 3) :=
  if x = 0 then binaryLabelPerm π hπ else ternaryLabelPerm π hπ

def bobRayRelabeling : OutputRelabeling binaryTernaryArchitecture :=
  ⟨fun _ => Equiv.refl _, blockLabelPerm π hπ⟩

/-- A binary ray keeps its coefficient index under the padded label convention. -/
theorem effectRay_binary_index (j : Fin 5) (hj : j.val < 2) :
    effectRay 0 (⟨j.val,by omega⟩ : Fin 3) = ray j := by
  fin_cases j <;> simp [Matrix.cons_val, effectRay] at hj ⊢

/-- Ternary labels 0,1,2 correspond to coefficient indices 2,3,4. -/
theorem effectRay_ternary_index (j : Fin 5) (hj : 2 ≤ j.val) :
    effectRay 1 (⟨j.val-2,by have h := j.isLt; omega⟩ : Fin 3) = ray j := by
  fin_cases j <;> simp [Matrix.cons_val, effectRay] at hj ⊢

theorem effectRay_ternary_label (a : Fin 3) :
    effectRay 1 a = ray (⟨a.val+2,by have h := a.isLt; omega⟩ : Fin 5) := by
  fin_cases a <;> rfl

/-- The unchanged zero binary effect and every nonzero effect are handled. -/
theorem effectRay_under_transformation (T : V ≃ₗ[ℝ] V)
    (hT : ∀ j, T (ray j) = ray (π j)) (x : Fin 2) (a : Fin 3) :
    T (effectRay x a) = effectRay x (blockLabelPerm π hπ x a) := by
  fin_cases x
  · change T (effectRay 0 a) = effectRay 0 (blockLabelPerm π hπ 0 a)
    by_cases ha : a.val < 2
    · let j : Fin 5 := ⟨a.val,by omega⟩
      have hj : j.val < 2 := ha
      have hsource : effectRay 0 a = ray j := by
        simpa only [j] using effectRay_binary_index j hj
      rw [hsource,hT]
      change ray (π j) = effectRay 0 (binaryLabelMap π hπ a)
      simp only [binaryLabelMap,dif_pos ha]
      exact (effectRay_binary_index (π j) ((hπ j).mpr hj)).symm
    · have ha2 : a = 2 := by apply Fin.ext; have h := a.isLt; omega
      subst a
      simp [effectRay,blockLabelPerm,binaryLabelPerm,binaryLabelMap]
  · change T (effectRay 1 a) = effectRay 1 (blockLabelPerm π hπ 1 a)
    let j : Fin 5 := ⟨a.val+2,by have h := a.isLt; omega⟩
    have hj : 2 ≤ j.val := by dsimp [j]; omega
    have hpj : 2 ≤ (π j).val := by have h := hπ j; omega
    rw [effectRay_ternary_label,hT]
    change ray (π j) = effectRay 1 (ternaryLabelMap π a)
    exact (effectRay_ternary_index (π j) hpj).symm

/-- The full table on which the paper's rank-zero reduction acts. -/
def transformedMetricTable (g : StrictParameters) (T : V ≃ₗ[ℝ] V) :
    Behavior binaryTernaryArchitecture :=
  fun x y a b => dotProduct (effectRay x a)
    (metric g.a g.b g.c g.d *ᵥ T (effectRay y b))

theorem transformedMetricTable_relabel (g : StrictParameters) (T : V ≃ₗ[ℝ] V)
    (hT : ∀ j, T (ray j) = ray (π j)) :
    transformedMetricTable g T = relabelBehavior (bobRayRelabeling π hπ) (metricTable g) := by
  funext x y a b
  change dotProduct (effectRay x a) (metric g.a g.b g.c g.d *ᵥ T (effectRay y b)) =
    dotProduct (effectRay x a)
      (metric g.a g.b g.c g.d *ᵥ effectRay y (blockLabelPerm π hπ y b))
  rw [effectRay_under_transformation π hπ T hT]

/-- Complete labelled rank-zero simulation from the explicit incidence
hypotheses. The conclusion is membership in the actual complex-qubit PVM hull. -/
theorem rank_zero_transformed_table_mem (g : StrictParameters) (T : V ≃ₗ[ℝ] V)
    (hnull : ∀ j, nullPolynomial g.a g.b g.c g.d (T (ray j)) = 0)
    (hbase : ∀ j, phi (T (ray j)) = 0)
    (hfuture : ∀ j, 0 < timeFunctional g (T (ray j)))
    (hnormal : timeFunctional g (T unitVector) = 1) :
    transformedMetricTable g T ∈ convexPVM binaryTernaryArchitecture := by
  obtain ⟨π,hpartition,hT⟩ := rank_zero_normalized_rigidity g T
    hnull hbase hfuture hnormal
  rw [transformedMetricTable_relabel π hpartition g T hT]
  exact relabel_mem_convexPVM (bobRayRelabeling π hpartition) (metricTable g)
    (metricTable_mem_convexPVM g)

end Bell.Lorentz
