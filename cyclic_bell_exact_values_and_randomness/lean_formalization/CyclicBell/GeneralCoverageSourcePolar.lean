import CyclicBell.GeneralSourceFourier
import CyclicBell.GeneralPolarPhases
import CyclicBell.GeneralFiniteSpectrum

/-!
Additional source-convention identities for manuscript `app:attainment`.
This module uses the source positive clock and forward shift, not a renamed
permutation witness. Completion of the literal source-polar coefficient bridge
is tracked separately from these foundational identities.
-/

noncomputable section
open scoped BigOperators Matrix ComplexOrder

namespace CyclicBell.General

variable {d : ℕ} [NeZero d]

/-- Literal W_y from manuscript app:attainment. -/
def sourceRelative (y : Ix d) : Mat (Ix d) :=
  chi y • ((sourceClock d)ᴴ * cyclicShift d)

theorem source_clock_unitary : UnitaryRel (sourceClock d) := by
  constructor
  · ext i j
    simp only [sourceClock, Matrix.diagonal_conjTranspose, Matrix.diagonal_mul_diagonal,
      Matrix.diagonal_apply, Matrix.one_apply]
    by_cases hij : i=j
    · subst j
      simpa only [if_pos rfl,Pi.star_apply] using chi_star_mul i
    · simp [hij]
  · ext i j
    simp only [sourceClock, Matrix.diagonal_conjTranspose, Matrix.diagonal_mul_diagonal,
      Matrix.diagonal_apply, Matrix.one_apply]
    by_cases hij : i=j
    · subst j
      simpa only [if_pos rfl,Pi.star_apply,mul_comm] using chi_star_mul i
    · simp [hij]

theorem source_shift_unitary : UnitaryRel (cyclicShift d) := by
  exact weighted_unitary (fun _ => 1) (by intro j; simp) (by simp)

theorem source_relative_unitary (y : Ix d) : UnitaryRel (sourceRelative y) :=
  (source_clock_unitary.adjoint.mul source_shift_unitary).scalar (chi_star_mul y)

/-- The sign is fixed by X|j> = |j+1> and Z|j> = chi(j)|j>. -/
theorem source_clock_shift :
    sourceClock d * cyclicShift d = chi (1 : Ix d) • (cyclicShift d * sourceClock d) := by
  ext i j
  simp only [sourceClock, Matrix.diagonal_mul, Matrix.mul_diagonal, Matrix.smul_apply,
    smul_eq_mul, cyclicShift, weightedCycle]
  by_cases hij : i=j+1
  · subst i
    simp [chi_add, mul_comm]
  · simp [hij]

theorem source_relative_weights (y : Ix d) :
    sourceRelative y = weightedCycle (fun j => chi (y-j-1)) := by
  ext i j
  simp only [sourceRelative, sourceClock, Matrix.diagonal_conjTranspose,
    Matrix.diagonal_mul, Matrix.smul_apply, smul_eq_mul, cyclicShift, weightedCycle]
  by_cases hij : i=j+1
  · subst i
    simp only [if_pos rfl,ite_true,mul_one,Pi.star_apply,chi_star,← chi_add]
    congr 1
    ring
  · simp [hij]

theorem source_equalityBase_power (hd : 2≤d) :
    equalityBase d ^ d = (-1 : ℂ)^(d-1) := by
  simpa only [equalityRoot,chi_zero,mul_one] using equalityRoot_power hd (0 : Ix d)

theorem source_clock_root_product (hd : 2≤d) :
    (∏ j : Ix d,chi j) = (-1 : ℂ)^(d-1) := by
  have he : equalityBase d^d * (∏ j : Ix d,chi j)=1 := by
    simpa only [equalityRoot,Finset.prod_mul_distrib,Finset.prod_const,
      Finset.card_univ,ZMod.card] using equalityRoot_product hd
  rw [source_equalityBase_power hd] at he
  apply mul_left_cancel₀ (pow_ne_zero (d-1) (by norm_num : (-1 : ℂ)≠0))
  rw [he,← mul_pow]
  norm_num

theorem source_character_product_reindex (y : Ix d) :
    (∏ j : Ix d, chi ((y-1)-j)) = ∏ j : Ix d, chi j := by
  exact Fintype.prod_equiv (Equiv.subLeft (y-1))
    (fun j : Ix d => chi ((y-1)-j)) (fun j : Ix d => chi j) (by intro j; rfl)

theorem source_relative_weight_product (hd : 2≤d) (y : Ix d) :
    (∏ j : Ix d,chi (y-j-1)) = (-1 : ℂ)^(d-1) := by
  have he : (∏ j : Ix d,chi (y-j-1)) = ∏ j : Ix d,chi ((y-1)-j) := by
    apply Finset.prod_congr rfl
    intro j _
    congr 1
    ring
  exact he.trans ((source_character_product_reindex y).trans (source_clock_root_product hd))

theorem source_relative_power (hd : 2≤d) (y : Ix d) :
    sourceRelative y ^ d = (-1 : ℂ)^(d-1) • (1 : Mat (Ix d)) := by
  rw [source_relative_weights,weighted_full_power,source_relative_weight_product hd]

theorem source_relative_spectral_power (hd : 2≤d) (y : Ix d)
    (z : MatrixSpectrum (sourceRelative y)) :
    (z : ℂ)^d = (-1 : ℂ)^(d-1) := by
  have hp : (toCMatrix (sourceRelative y))^d =
      algebraMap ℂ (CMat (Ix d)) ((-1 : ℂ)^(d-1)) := by
    change toCMatrix ((sourceRelative y)^d) = _
    rw [source_relative_power hd,Algebra.algebraMap_eq_smul_one]
    rfl
  have hz : (z : ℂ)^d ∈ spectrum ℂ ((toCMatrix (sourceRelative y))^d) := by
    rw [spectrum.map_pow]
    exact ⟨z,z.property,rfl⟩
  rw [hp,spectrum.scalar_eq] at hz
  exact hz

end CyclicBell.General
