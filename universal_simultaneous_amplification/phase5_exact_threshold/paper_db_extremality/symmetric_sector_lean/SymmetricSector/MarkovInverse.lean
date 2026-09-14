import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-! Finite Markov-chain uniqueness from its actual transition matrix.
No irreducibility or inverse is assumed by the edge theorem: stationarity
with strictly positive weights and stochasticity suffice. -/
namespace SymmetricSector.Markov
open Matrix
open scoped BigOperators

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

omit [DecidableEq ι] in
/-- Expanding the stationary Dirichlet sum of a harmonic function gives zero. -/
theorem harmonic_energy_zero (K : Matrix ι ι ℝ) (ν f : ι → ℝ)
    (hrow : ∀ i, ∑ j, K i j = 1)
    (hstat : ∀ j, ∑ i, ν i * K i j = ν j)
    (hf : K *ᵥ f = f) :
    (∑ i, ∑ j, ν i * K i j * (f i - f j) ^ 2) = 0 := by
  have hinner : ∀ i, (∑ j, ν i * K i j * (f i - f j) ^ 2) =
      ν i * (f i) ^ 2 * (∑ j, K i j) +
      (∑ j, ν i * K i j * (f j) ^ 2) -
      2 * ν i * f i * (∑ j, K i j * f j) := by
    intro i
    calc
      _ = ∑ j, (ν i * (f i) ^ 2 * K i j + ν i * K i j * (f j) ^ 2 -
          2 * ν i * f i * (K i j * f j)) := by
        apply Finset.sum_congr rfl
        intro j _
        ring
      _ = _ := by
        simp only [Finset.sum_sub_distrib, Finset.sum_add_distrib, Finset.mul_sum]
  have hsecond : (∑ i, ∑ j, ν i * K i j * (f j) ^ 2) =
      ∑ j, ν j * (f j) ^ 2 := by
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro j _
    rw [← Finset.sum_mul, hstat j]
  have hfj : ∀ i, (∑ j, K i j * f j) = f i := by
    intro i
    exact congrFun hf i
  simp_rw [hinner, hrow, hfj, mul_one]
  rw [Finset.sum_sub_distrib, Finset.sum_add_distrib, hsecond]
  have hc : (∑ i, 2 * ν i * f i * f i) = 2 * ∑ i, ν i * (f i) ^ 2 := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    ring
  rw [hc]
  ring

omit [DecidableEq ι] in
/-- A real harmonic function is constant along each positive transition when
the chain has a strictly positive stationary distribution. -/
theorem harmonic_edge_eq (K : Matrix ι ι ℝ) (ν f : ι → ℝ)
    (hK : ∀ i j, 0 ≤ K i j) (hν : ∀ i, 0 < ν i)
    (hrow : ∀ i, ∑ j, K i j = 1)
    (hstat : ∀ j, ∑ i, ν i * K i j = ν j)
    (hf : K *ᵥ f = f) {i j : ι} (hij : 0 < K i j) : f i = f j := by
  have hn : ∀ i j, 0 ≤ ν i * K i j * (f i - f j) ^ 2 := by
    intro a b
    exact mul_nonneg (mul_nonneg (hν a).le (hK a b)) (sq_nonneg _)
  have hz := harmonic_energy_zero K ν f hrow hstat hf
  have hrowz : (∑ b, ν i * K i b * (f i - f b) ^ 2) = 0 :=
    (Finset.sum_eq_zero_iff_of_nonneg
      (fun a _ => Finset.sum_nonneg (fun b _ => hn a b))).mp hz i (Finset.mem_univ i)
  have hterm : ν i * K i j * (f i - f j) ^ 2 = 0 :=
    (Finset.sum_eq_zero_iff_of_nonneg (fun b _ => hn i b)).mp hrowz j (Finset.mem_univ j)
  have hw : ν i * K i j ≠ 0 := ne_of_gt (mul_pos (hν i) hij)
  have hs : (f i - f j) ^ 2 = 0 := (mul_eq_zero.mp hterm).resolve_left hw
  nlinarith [sq_nonneg (f i - f j)]

/-- The rank-one correction to the Markov Poisson matrix. -/
def centered (K : Matrix ι ι ℝ) (ν : ι → ℝ) : Matrix ι ι ℝ :=
  1 - K + Matrix.of (fun (_ : ι) (j : ι) => ν j)

theorem centered_mulVec (K : Matrix ι ι ℝ) (ν f : ι → ℝ) :
    centered K ν *ᵥ f = f - K *ᵥ f + fun _ => dotProduct ν f := by
  rw [centered, Matrix.add_mulVec, Matrix.sub_mulVec, Matrix.one_mulVec]
  rfl

omit [DecidableEq ι] in
/-- Stationarity preserves the weighted pairing with a transition average. -/
theorem stationary_pairing (K : Matrix ι ι ℝ) (ν f : ι → ℝ)
    (hstat : ∀ j, ∑ i, ν i * K i j = ν j) :
    dotProduct ν (K *ᵥ f) = dotProduct ν f := by
  rw [Matrix.dotProduct_mulVec]
  congr 1
  exact funext hstat

theorem centered_pairing (K : Matrix ι ι ℝ) (ν f : ι → ℝ)
    (hstat : ∀ j, ∑ i, ν i * K i j = ν j)
    (hnorm : ∑ i, ν i = 1) :
    dotProduct ν (centered K ν *ᵥ f) = dotProduct ν f := by
  rw [centered_mulVec, dotProduct_add, dotProduct_sub,
    stationary_pairing K ν f hstat, sub_self, zero_add]
  simp only [dotProduct, ← Finset.sum_mul, hnorm, one_mul]

/-- Triviality of the corrected Poisson kernel needs only stationarity,
normalization, and the explicitly stated harmonic-constant property. -/
theorem centered_kernel_eq_zero (K : Matrix ι ι ℝ) (ν f : ι → ℝ)
    (hstat : ∀ j, ∑ i, ν i * K i j = ν j)
    (hnorm : ∑ i, ν i = 1)
    (hconstant : ∀ g : ι → ℝ, K *ᵥ g = g → ∀ i j, g i = g j)
    (hf : centered K ν *ᵥ f = 0) : f = 0 := by
  have hmean : dotProduct ν f = 0 := by
    have hp := centered_pairing K ν f hstat hnorm
    rw [hf, dotProduct_zero] at hp
    exact hp.symm
  have hharm : K *ᵥ f = f := by
    rw [centered_mulVec] at hf
    ext i
    have hi := congrFun hf i
    simp only [Pi.add_apply, Pi.sub_apply, Pi.zero_apply, hmean, add_zero] at hi
    linarith
  ext i
  have hpair : dotProduct ν f = f i := by
    calc
      _ = ∑ j, ν j * f i := by
        apply Finset.sum_congr rfl
        intro j _
        rw [hconstant f hharm j i]
      _ = f i := by rw [← Finset.sum_mul, hnorm, one_mul]
  simpa only [Pi.zero_apply] using hpair.symm.trans hmean

/-- A normalized stationary finite chain whose only harmonic functions are
constant has an invertible corrected Poisson matrix. -/
theorem centered_isUnit (K : Matrix ι ι ℝ) (ν : ι → ℝ)
    (hstat : ∀ j, ∑ i, ν i * K i j = ν j)
    (hnorm : ∑ i, ν i = 1)
    (hconstant : ∀ g : ι → ℝ, K *ᵥ g = g → ∀ i j, g i = g j) :
    IsUnit (centered K ν) := by
  apply Matrix.mulVec_injective_iff_isUnit.mp
  intro f g hfg
  have hz : centered K ν *ᵥ (f - g) = 0 := by
    rw [Matrix.mulVec_sub, hfg, sub_self]
  exact sub_eq_zero.mp (centered_kernel_eq_zero K ν (f-g) hstat hnorm hconstant hz)

theorem centered_det_isUnit (K : Matrix ι ι ℝ) (ν : ι → ℝ)
    (hstat : ∀ j, ∑ i, ν i * K i j = ν j)
    (hnorm : ∑ i, ν i = 1)
    (hconstant : ∀ g : ι → ℝ, K *ᵥ g = g → ∀ i j, g i = g j) :
    IsUnit (centered K ν).det :=
  (Matrix.isUnit_iff_isUnit_det _).mp (centered_isUnit K ν hstat hnorm hconstant)

end SymmetricSector.Markov
