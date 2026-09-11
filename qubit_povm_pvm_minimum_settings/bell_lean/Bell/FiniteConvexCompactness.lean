import Bell.Quantum
import Mathlib.Analysis.Convex.Caratheodory
import Mathlib.Analysis.Convex.KreinMilman
import Mathlib.LinearAlgebra.AffineSpace.FiniteDimensional

/-!
# Finite-dimensional convex hulls without an unproved compactness premise

Carathéodory reduces the hull to a FINITE union of continuous images of compact
simplex-by-point-family sets. This is ordinary convex hull, not its closure.
The distinction is needed when later converting closed-hull arguments back into
finite shared-randomness mixtures.
-/
noncomputable section
open Set Affine
open scoped BigOperators Topology
namespace Bell

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- Closed probability simplex, with empty index types allowed. -/
def probabilitySimplex (ι : Type*) [Fintype ι] : Set (ι → ℝ) :=
  {w | (∀ i, 0 ≤ w i) ∧ ∑ i, w i = 1}

theorem probabilitySimplex_isCompact (ι : Type*) [Fintype ι] :
    IsCompact (probabilitySimplex ι) := by
  have hc : IsCompact {w : ι → ℝ | ∀ i, w i ∈ Icc (0 : ℝ) 1} :=
    isCompact_pi_infinite fun _ => isCompact_Icc
  apply hc.of_isClosed_subset
  · exact (isClosed_setOf_forall fun i => isClosed_le continuous_const (continuous_apply i)).inter
      (isClosed_eq (by fun_prop) continuous_const)
  · intro w hw i
    refine ⟨hw.1 i, ?_⟩
    calc
      w i ≤ ∑ j, w j := Finset.single_le_sum (fun j _ => hw.1 j) (Finset.mem_univ i)
      _ = 1 := hw.2

/-- Convex combinations with exactly n slots; slots of weight zero are harmless. -/
def combinations (n : ℕ) (S : Set E) : Set E :=
  (fun p : (Fin n → ℝ) × (Fin n → E) => ∑ i, p.1 i • p.2 i) ''
    (probabilitySimplex (Fin n) ×ˢ {v | ∀ i, v i ∈ S})

theorem combinations_isCompact (n : ℕ) {S : Set E} (hS : IsCompact S) :
    IsCompact (combinations n S) := by
  exact ((probabilitySimplex_isCompact (Fin n)).prod
    (isCompact_pi_infinite fun _ => hS)).image (by fun_prop)

theorem combinations_subset_convexHull (n : ℕ) (S : Set E) :
    combinations n S ⊆ convexHull ℝ S := by
  rintro x ⟨⟨w, v⟩, ⟨⟨hw, hn⟩, hv⟩, rfl⟩
  exact mem_convexHull_of_exists_fintype w v hw hn hv rfl

/-- A quantitative finite-slot version, retaining empty and lower-dimensional
architectures rather than imposing a nonempty-output hypothesis. -/
theorem convexHull_eq_finite_combinations [FiniteDimensional ℝ E] (S : Set E) :
    convexHull ℝ S = ⋃ n : Fin (Module.finrank ℝ E + 2), combinations n.val S := by
  classical
  apply Set.Subset.antisymm
  · intro x hx
    let t := Caratheodory.minCardFinsetOfMemConvexHull hx
    have htS : (t : Set E) ⊆ S := Caratheodory.minCardFinsetOfMemConvexHull_subseteq hx
    have hti : AffineIndependent ℝ ((↑) : t → E) :=
      Caratheodory.affineIndependent_minCardFinsetOfMemConvexHull hx
    have htx : x ∈ convexHull ℝ (t : Set E) :=
      Caratheodory.mem_minCardFinsetOfMemConvexHull hx
    obtain ⟨w, hw, hsum, hxsum⟩ := Finset.mem_convexHull'.mp htx
    have htne : t.Nonempty := by
      by_contra hn
      have he : t=∅ := Finset.not_nonempty_iff_eq_empty.mp hn
      simp [he] at hsum
    letI : Nonempty t := ⟨⟨htne.choose,htne.choose_spec⟩⟩
    have hcard : t.card ≤ Module.finrank ℝ E + 1 := by
      have hc := hti.finrank_vectorSpan_add_one
      have hd := Submodule.finrank_le (vectorSpan ℝ (Set.range ((↑) : t → E)))
      have hc' : Module.finrank ℝ (vectorSpan ℝ (Set.range ((↑) : t → E)))+1=t.card := by
        simpa using hc
      omega
    let e : Fin t.card ≃ t := (Fintype.equivFin t).symm
    let w' : Fin t.card → ℝ := fun i => w (e i)
    let v' : Fin t.card → E := fun i => (e i).val
    have hsum' : ∑ i, w' i = 1 := by
      rw [show (∑ i, w' i) = ∑ j : t, w j from Equiv.sum_comp e (fun j : t => w j)]
      simpa using hsum
    have hxsum' : (∑ i, w' i • v' i) = x := by
      rw [show (∑ i, w' i • v' i) = ∑ j : t, w j • (j : E) from
        Equiv.sum_comp e (fun j : t => w j • (j : E))]
      simpa using hxsum
    apply Set.mem_iUnion.mpr
    refine ⟨⟨t.card, by omega⟩, ⟨(w', v'), ⟨⟨?_, hsum'⟩, ?_⟩, hxsum'⟩⟩
    · intro i
      exact hw _ (e i).property
    · intro i
      exact htS (e i).property
  · exact Set.iUnion_subset fun n => combinations_subset_convexHull n.val S

/-- Compactness of the ordinary shared-randomness hull in finite dimensions. -/
theorem compact_convexHull [FiniteDimensional ℝ E] {S : Set E} (hS : IsCompact S) :
    IsCompact (convexHull ℝ S) := by
  rw [convexHull_eq_finite_combinations]
  exact isCompact_iUnion fun n => combinations_isCompact n.val hS

/-- Midpoint perturbations at an extreme point must be stationary as points,
not merely equal in the chosen objective. -/
theorem extreme_midpoint {S : Set E} {x a b : E}
    (hx : x ∈ Set.extremePoints ℝ S) (ha : a ∈ S) (hb : b ∈ S)
    (hab : (1/2 : ℝ) • a + (1/2 : ℝ) • b = x) : a = x ∧ b = x := by
  exact hx.2 ha hb ⟨1/2, 1/2, by norm_num, by norm_num, by norm_num, hab⟩

/-- Unequal positive mixing weights are needed by common-span filtering. -/
theorem extreme_positive_combination {S : Set E} {x a b : E} {s t : ℝ}
    (hx : x ∈ Set.extremePoints ℝ S) (ha : a ∈ S) (hb : b ∈ S)
    (hs : 0 < s) (ht : 0 < t) (hst : s+t = 1) (hab : s • a + t • b = x) :
    a = x ∧ b = x := hx.2 ha hb ⟨s, t, hs, ht, hst, hab⟩

/-- A closed convex set containing all extreme points of a compact convex set
contains the whole set. This will implement the finite cone-circuit reduction. -/
theorem contains_compact_of_contains_extreme
    {K S : Set E} (hK : IsCompact K) (hKc : Convex ℝ K)
    (hSc : Convex ℝ S) (hSclosed : IsClosed S)
    (hext : Set.extremePoints ℝ K ⊆ S) : K ⊆ S := by
  rw [← closure_convexHull_extremePoints hK hKc]
  exact closure_minimal (convexHull_min hext hSc) hSclosed

end Bell
