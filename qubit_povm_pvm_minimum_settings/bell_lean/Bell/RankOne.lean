import Bell.ProjectiveFiber

/-!
# Rank-one positive-stationarity obstruction

This is the algebraic rank-one branch of paper §9.2.  The hypotheses explicitly
state the null-ray conditions, projective distinctness, one-dimensional image,
and positive stationary weights.  Connecting these hypotheses to a physical
Bell maximizer remains part of the incidence/multiplier formalization.
-/

noncomputable section
open scoped BigOperators
namespace Bell.Lorentz

/-- The five coefficient rays are pairwise different projective points. -/
theorem coefficient_rays_projectively_distinct (i j : Fin 5)
    (h : SameRay (ray i) (ray j)) : i = j := by
  obtain ⟨s, hs, heq⟩ := h
  have h₀ := congrFun heq 0
  have h₁ := congrFun heq 1
  have h₂ := congrFun heq 2
  have h₃ := congrFun heq 3
  fin_cases i <;> fin_cases j <;> norm_num [ray] at h₀ h₁ h₂ h₃ ⊢

/-- An invertible real linear map preserves this projective distinctness. -/
theorem transformed_rays_projectively_distinct (T : V ≃ₗ[ℝ] V) (i j : Fin 5)
    (h : SameRay (T (ray i)) (T (ray j))) : i = j := by
  obtain ⟨s, hs, heq⟩ := h
  apply coefficient_rays_projectively_distinct i j
  refine ⟨s, hs, ?_⟩
  apply T.injective
  simpa only [map_smul] using heq

/-- A positive weighted stationary sum cannot consist of exactly one nonzero
vector.  This elementary statement also covers zero rows without division. -/
theorem positive_sum_not_singleton {ι : Type*} [Fintype ι] [DecidableEq ι]
    (v : ι → V) (weight : ι → ℝ) (j : ι)
    (hw : 0 < weight j) (hv : v j ≠ 0)
    (hother : ∀ i, i ≠ j → v i = 0)
    (hsum : ∑ i, weight i • v i = 0) : False := by
  have hs : (∑ i, weight i • v i) = weight j • v j := by
    apply Finset.sum_eq_single j
    · intro i _ hij
      rw [hother i hij, smul_zero]
    · intro h
      exact (h (Finset.mem_univ j)).elim
  have hz : weight j • v j = 0 := hs.symm.trans hsum
  exact hv ((smul_eq_zero.mp hz).resolve_left (ne_of_gt hw))

/-- Total projective injectivity rules out positive stationarity when all
nonzero images span one projective point.  This is not an assumption of the
fiber theorem: `projective_fiber_injective_of_sameRay` proves the implication
used here, including every exceptional source. -/
theorem rank_one_positive_stationarity_impossible
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (g : StrictParameters) (y : ι → V) (weight : ι → ℝ)
    (hnull : ∀ j, nullPolynomial g.a g.b g.c g.d (y j) = 0)
    (hdistinct : ∀ i j, SameRay (y i) (y j) → i = j)
    (hpositive : ∀ j, 0 < weight j)
    (hlive : ∃ j, phi (y j) ≠ 0)
    (hline : ∀ i j, phi (y i) ≠ 0 → phi (y j) ≠ 0 →
      SameRay (phi (y i)) (phi (y j)))
    (hstationary : ∑ j, weight j • phi (y j) = 0) : False := by
  obtain ⟨j, hj⟩ := hlive
  have hother : ∀ i, i ≠ j → phi (y i) = 0 := by
    intro i hij
    by_contra hi
    have hsame : SameRay (y i) (y j) :=
      projective_fiber_injective_of_sameRay g (y i) (y j)
        (hnull i) (hnull j) hi (hline i j hi hj)
    exact hij (hdistinct i j hsame)
  exact positive_sum_not_singleton (fun i => phi (y i)) weight j
    (hpositive j) hj hother hstationary

/-- Nonzero scalar multiples of one nonzero vector have the same projective
class.  The denominator is proved nonzero from the second nonzero image. -/
theorem images_on_line_sameRay (ξ : V) (u v : ℝ)
    (hu : u • ξ ≠ 0) (hv : v • ξ ≠ 0) : SameRay (u • ξ) (v • ξ) := by
  have hu' : u ≠ 0 := by
    intro h
    exact hu (by simp [h])
  have hv' : v ≠ 0 := by
    intro h
    exact hv (by simp [h])
  refine ⟨u/v, div_ne_zero hu' hv', ?_⟩
  rw [smul_smul, div_mul_cancel₀ _ hv']

/-- A concrete five-row rank-one formulation appropriate for the metric
Jacobian: all rows are multiples of a fixed nonzero vector and at least one
row is nonzero.  A separate differential calculation must identify these rows
with the physical metric differential. -/
theorem transformed_rank_one_obstruction
    (g : StrictParameters) (T : V ≃ₗ[ℝ] V)
    (weight coefficient : Fin 5 → ℝ) (ξ : V)
    (hnull : ∀ j, nullPolynomial g.a g.b g.c g.d (T (ray j)) = 0)
    (hpositive : ∀ j, 0 < weight j)
    (hξ : ξ ≠ 0) (hlive : ∃ j, coefficient j ≠ 0)
    (hrows : ∀ j, phi (T (ray j)) = coefficient j • ξ)
    (hstationary : ∑ j, weight j • phi (T (ray j)) = 0) : False := by
  apply rank_one_positive_stationarity_impossible g (fun j => T (ray j)) weight
    hnull (transformed_rays_projectively_distinct T) hpositive
  · obtain ⟨j, hj⟩ := hlive
    refine ⟨j, ?_⟩
    rw [hrows]
    exact smul_ne_zero hj hξ
  · intro i j hi hj
    rw [hrows i, hrows j] at hi hj ⊢
    exact images_on_line_sameRay ξ (coefficient i) (coefficient j) hi hj
  · exact hstationary

end Bell.Lorentz
