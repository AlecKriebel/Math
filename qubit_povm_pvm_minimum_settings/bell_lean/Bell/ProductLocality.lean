import Bell.MeasurementGeometry
import Bell.ClassicalProduct
import Bell.LocalSimulation

/-! # Product behaviors and singular reduced-state locality

The hidden variable chooses complete deterministic response assignments for
both parties. A singular nonzero reduced qubit state forces every assemblage
outcome onto its exposed ray and therefore gives a product behavior.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder
namespace Bell

/-- Arbitrary finite input-dependent stochastic response rows define an actual
finite common-randomness mixture of identity/zero qubit PVMs. -/
theorem product_behavior_mem_convexPVM (A : Architecture)
    (p : (x : Fin A.aliceInputs) → Fin (A.aliceOutputs x) → ℝ)
    (q : (y : Fin A.bobInputs) → Fin (A.bobOutputs y) → ℝ)
    (hp : ∀ x a, 0 ≤ p x a) (hq : ∀ y b, 0 ≤ q y b)
    (hnp : ∀ x, ∑ a, p x a = 1) (hnq : ∀ y, ∑ b, q y b = 1) :
    (fun x y a b => p x a * q y b) ∈ convexPVM A := by
  classical
  let IA := (x : Fin A.aliceInputs) → Fin (A.aliceOutputs x)
  let IB := (y : Fin A.bobInputs) → Fin (A.bobOutputs y)
  let w : IA × IB → ℝ := fun k => ClassicalProduct.mass p k.1 * ClassicalProduct.mass q k.2
  have hw : ∀ k, 0 ≤ w k := by
    intro k
    exact mul_nonneg (Finset.prod_nonneg fun x _ => hp x (k.1 x))
      (Finset.prod_nonneg fun y _ => hq y (k.2 y))
  have hn : ∑ k, w k = 1 := by
    simp only [w, Fintype.sum_prod_type, ← Finset.mul_sum, ← Finset.sum_mul,
      ClassicalProduct.total_mass_one p hnp, ClassicalProduct.total_mass_one q hnq, mul_one]
  have hm := finite_local_mixture_mem_convexPVM A w Prod.fst Prod.snd hw hn
  have heq : (∑ k : IA × IB, w k • deterministicTable A k.1 k.2) =
      (fun x y a b => p x a * q y b) := by
    funext x y a b
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, w,
      deterministicTable, Fintype.sum_prod_type]
    have hind (u : IA) (v : IB) :
        (if a=u x ∧ b=v y then (1:ℝ) else 0) =
          (if a=u x then (1:ℝ) else 0) * (if b=v y then 1 else 0) := by
      split_ifs <;> simp_all
    simp_rw [hind]
    calc
      _ = (∑ u : IA, ClassicalProduct.mass p u * (if a=u x then 1 else 0)) *
          (∑ v : IB, ClassicalProduct.mass q v * (if b=v y then 1 else 0)) := by
        rw [Finset.sum_mul]
        apply Finset.sum_congr rfl
        intro u _
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro v _
        ring
      _ = _ := by rw [ClassicalProduct.marginal p hnp, ClassicalProduct.marginal q hnq]
  rw [heq] at hm
  exact hm

/-- A local trace is real for two Hermitian factors. -/
theorem trace_product_im_zero {A B : Operator} (hA : A.IsHermitian) (hB : B.IsHermitian) :
    (Matrix.trace (A*B)).im = 0 := by
  rw [← QubitGeometry.pauli_coordinates hA, ← QubitGeometry.pauli_coordinates hB,
    QubitGeometry.pauli_trace_product]
  simp

theorem Assemblage.right_complement_positive {A : Architecture} (s : Assemblage A)
    (y : Fin A.bobInputs) (b : Fin (A.bobOutputs y)) :
    (s.reduced-s.steered y b).PosSemidef := by
  classical
  have he : s.steered y b + (∑ c : {c // c ≠ b}, s.steered y c) = s.reduced := by
    rw [← Fintype.sum_eq_add_sum_subtype_ne, s.commonSum y]
  rw [← show (∑ c : {c // c ≠ b}, s.steered y c) = s.reduced-s.steered y b from
    eq_sub_of_add_eq' he]
  exact positive_sum _ fun c => s.positive y c

theorem Assemblage.singular_mem_convexPVM {A : Architecture} (s : Assemblage A)
    (hd : s.reduced.det = 0) : s.behavior ∈ convexPVM A := by
  have hrn : s.reduced ≠ 0 := by
    intro hz
    have h := s.reducedNormalized
    simp [hz] at h
  have htr : (Matrix.trace s.reduced).re = 1 := by rw [s.reducedNormalized]; rfl
  have hray : ∀ y b, s.steered y b = (Matrix.trace (s.steered y b)).re • s.reduced := by
    intro y b
    simpa [htr] using positive_below_rank_one s.reducedPositive hrn hd
      (s.positive y b) (s.right_complement_positive y b)
  let p := fun x a => localTrace ((s.alice x).effect a) s.reduced
  let q := fun y b => (Matrix.trace (s.steered y b)).re
  have hp : ∀ x a, 0 ≤ p x a := fun x a =>
    localTrace_nonnegative ((s.alice x).positive a) s.reducedPositive
  have hq : ∀ y b, 0 ≤ q y b := fun y b => positive_trace_nonneg (s.positive y b)
  have hnp : ∀ x, ∑ a, p x a = 1 := by
    intro x
    simp_rw [p, localTrace_comm _ s.reduced]
    rw [← map_sum, (s.alice x).normalized]
    simp [localTrace, s.reducedNormalized]
  have hnq : ∀ y, ∑ b, q y b = 1 := by
    intro y
    simpa [q, Matrix.trace_sum,s.reducedNormalized] using
      congrArg (fun R : Operator => (Matrix.trace R).re) (s.commonSum y)
  have heq : s.behavior = fun x y a b => p x a*q y b := by
    funext x y a b
    unfold Assemblage.behavior
    rw [hray, map_smul]
    simp only [smul_eq_mul, p, q]
    ring
  rw [heq]
  exact product_behavior_mem_convexPVM A p q hp hq hnp hnq

/-- A singular common reduced state needs no inverse in the realization theorem:
its product behavior is already PVM-simulable. -/
theorem Assemblage.mem_convexPOVM {A : Architecture} (s : Assemblage A) :
    s.behavior ∈ convexPOVM A := by
  by_cases hd : s.reduced.det = 0
  · exact convexPVM_subset_convexPOVM A (s.singular_mem_convexPVM hd)
  · exact subset_convexHull ℝ (rawPOVM A) (s.mem_rawPOVM (isUnit_iff_ne_zero.mpr hd))

end Bell
