import CyclicBell.MatrixAlgebra
import CyclicBell.Phases

/-! Rank-one four-outcome PVMs for arbitrary unimodular weighted four-cycles.
The product-one condition is a physical finite-order condition, not a Bell
maximality assumption. All witness instances discharge it explicitly.
UNCOMPILED SOURCE CANDIDATE. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace CyclicBell.D4
attribute [local simp] Matrix.cons_val_two Matrix.cons_val_three
set_option maxRecDepth 20000
set_option maxHeartbeats 12000000

/-- Weighted shift with column j weight w_j. -/
def weighted (w : Fin 4 → ℂ) : Op 4 := shift * Matrix.diagonal w

def entryConj (T : Op 4) : Op 4 := fun i j => star (T i j)

theorem entryConj_involutive (T : Op 4) : entryConj (entryConj T) = T := by
  ext i j
  simp [entryConj]

def phasedVector (r : Fin 4 → ℂ) (a : Fin 4) : Vec 4 := fun j => r j * u a j

theorem phase_mul_unit {z w : ℂ} (hz : star z * z = 1) (hw : star w * w = 1) :
    star (z * w) * (z * w) = 1 := by
  calc
    star (z * w) * (z * w) = (star z * z) * (star w * w) := by rw [star_mul]; ring
    _ = 1 := by rw [hz, hw]; norm_num

theorem phased_orthonormal (r : Fin 4 → ℂ) (hr : ∀ j, star (r j) * r j = 1)
    (a b : Fin 4) : ip (phasedVector r a) (phasedVector r b) = if a = b then 1 else 0 := by
  calc
    ip (phasedVector r a) (phasedVector r b) = ip (u a) (u b) := by
      unfold ip phasedVector
      apply Finset.sum_congr rfl
      intro j _
      calc
        star (r j * u a j) * (r j * u b j) =
            (star (r j) * r j) * (star (u a j) * u b j) := by rw [star_mul]; ring
        _ = _ := by rw [hr]; simp
    _ = _ := u_orthonormal a b

theorem phased_complete (r : Fin 4 → ℂ) (hr : ∀ j, star (r j) * r j = 1) :
    (∑ a : Fin 4, projector (phasedVector r a)) = 1 := by
  apply Matrix.ext
  intro i j
  have hu := congrFun (congrFun u_complete i) j
  change (∑ a : Fin 4, projector (u a) i j) = (1 : Op 4) i j at hu
  have he : (∑ a : Fin 4, projector (phasedVector r a) i j) =
      r i * star (r j) * (∑ a : Fin 4, projector (u a) i j) := by
    simp only [projector, phasedVector, star_mul, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro a _
    ring
  change (∑ a : Fin 4, projector (phasedVector r a) i j) = _
  rw [he, hu]
  by_cases hij : i = j
  · subst j
    simpa [Matrix.one_apply, mul_comm] using hr i
  · simp [Matrix.one_apply, hij]

def phasedPVM (r : Fin 4 → ℂ) (hr : ∀ j, star (r j) * r j = 1) : PVM 4 :=
  pvmOfBasis (phasedVector r) (phased_orthonormal r hr) (phased_complete r hr)

theorem phased_encoding (r : Fin 4 → ℂ) (hr : ∀ j, star (r j) * r j = 1) :
    observable (phasedPVM r hr) =
      Matrix.diagonal r * shift * (Matrix.diagonal r).conjTranspose := by
  apply Matrix.ext
  intro i j
  have hu := congrFun (congrFun bob_encoding i) j
  have hf : (observable (phasedPVM r hr)) i j =
      r i * star (r j) * (observable bobTargetPVM) i j := by
    simp only [observable, phasedPVM, pvmOfBasis, bobTargetPVM, projector,
      phasedVector, Matrix.sum_apply, Matrix.smul_apply, smul_eq_mul, star_mul,
      Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro a _
    ring
  rw [hf, hu]
  simp only [Matrix.diagonal_conjTranspose, Matrix.mul_diagonal, Matrix.diagonal_mul]
  simp only [Pi.star_apply]
  ring

/-- Prefixes of the cycle's edge weights; q_0 is fixed to 1. -/
def cyclePrefix (w : Fin 4 → ℂ) : Fin 4 → ℂ :=
  ![1, w 0, w 0 * w 1, w 0 * w 1 * w 2]

theorem cyclePrefix_unit (w : Fin 4 → ℂ) (hw : ∀ j, star (w j) * w j = 1)
    (j : Fin 4) : star (cyclePrefix w j) * cyclePrefix w j = 1 := by
  fin_cases j
  · norm_num [cyclePrefix]
  · simpa [cyclePrefix] using hw 0
  · simpa [cyclePrefix] using phase_mul_unit (hw 0) (hw 1)
  · simpa [cyclePrefix] using phase_mul_unit (phase_mul_unit (hw 0) (hw 1)) (hw 2)

theorem cyclePrefix_recurrence (w : Fin 4 → ℂ)
    (hprod : w 0 * w 1 * w 2 * w 3 = 1) (j : Fin 4) :
    cyclePrefix w (j + 1) = w j * cyclePrefix w j := by
  fin_cases j
  · change w 0 = w 0 * 1
    ring
  · change w 0 * w 1 = w 1 * w 0
    ring
  · change w 0 * w 1 * w 2 = w 2 * (w 0 * w 1)
    ring
  · change 1 = w 3 * (w 0 * w 1 * w 2)
    calc
      1 = w 0 * w 1 * w 2 * w 3 := hprod.symm
      _ = _ := by ring

/-- Entry-wise statement fixes the cyclic-shift orientation. -/
theorem shift_entry (i j : Fin 4) : shift i j = if i = j + 1 then 1 else 0 := by
  fin_cases i <;> fin_cases j <;> norm_num [shift, Fin.add_def, Fin.ext_iff]

theorem cycle_diagonalization (w : Fin 4 → ℂ)
    (hw : ∀ j, star (w j) * w j = 1) (hprod : w 0 * w 1 * w 2 * w 3 = 1) :
    Matrix.diagonal (cyclePrefix w) * shift * (Matrix.diagonal (cyclePrefix w)).conjTranspose =
      weighted w := by
  apply Matrix.ext
  intro i j
  simp only [weighted, Matrix.diagonal_conjTranspose, Matrix.mul_diagonal,
    Matrix.diagonal_mul, Pi.star_apply, shift_entry]
  by_cases hij : i = j + 1
  · subst i
    simp only [if_pos, mul_one, one_mul]
    rw [cyclePrefix_recurrence w hprod]
    calc
      w j * cyclePrefix w j * star (cyclePrefix w j) =
          w j * (star (cyclePrefix w j) * cyclePrefix w j) := by ring
      _ = w j := by rw [cyclePrefix_unit w hw]; ring
  · simp [hij]

def cyclePVM (w : Fin 4 → ℂ) (hw : ∀ j, star (w j) * w j = 1)
    (_hprod : w 0 * w 1 * w 2 * w 3 = 1) : PVM 4 :=
  phasedPVM (cyclePrefix w) (cyclePrefix_unit w hw)

theorem cyclePVM_encoding (w : Fin 4 → ℂ) (hw : ∀ j, star (w j) * w j = 1)
    (hprod : w 0 * w 1 * w 2 * w 3 = 1) :
    observable (cyclePVM w hw hprod) = weighted w := by
  rw [cyclePVM, phased_encoding, cycle_diagonalization w hw hprod]

theorem weighted_unitary (w : Fin 4 → ℂ) (hw : ∀ j, star (w j) * w j = 1)
    (hprod : w 0 * w 1 * w 2 * w 3 = 1) : UnitaryRel (weighted w) := by
  rw [← cyclePVM_encoding w hw hprod]
  exact observable_unitary _

theorem weighted_fourth_power (w : Fin 4 → ℂ) (hw : ∀ j, star (w j) * w j = 1)
    (hprod : w 0 * w 1 * w 2 * w 3 = 1) : weighted w ^ 4 = 1 := by
  rw [← cyclePVM_encoding w hw hprod]
  exact observable_fourth_power _

theorem weighted_entry (w : Fin 4 → ℂ) (i j : Fin 4) :
    weighted w i j = shift i j * w j := by simp [weighted, Matrix.mul_apply, Matrix.diagonal]

theorem weighted_linear (z : ℂ) (w v : Fin 4 → ℂ) :
    weighted (fun j => w j + z * v j) = weighted w + z • weighted v := by
  ext i j
  simp only [weighted_entry, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
  ring

theorem weighted_conjugate (w : Fin 4 → ℂ) :
    entryConj (weighted w) = weighted (fun j => star (w j)) := by
  ext i j
  simp only [entryConj, weighted_entry, shift_entry]
  split <;> simp_all

theorem phi_trace (A B : Op 4) :
    expectation phi (tensor A B) = Matrix.trace (A * B.transpose) / 4 := by
  simp only [expectation, ip, applyOp, tensor, phi, Fintype.sum_prod_type]
  simp only [apply_ite, star_zero, star_div₀, star_one, star_ofNat,
    ite_mul, zero_mul, mul_ite, mul_zero, Finset.sum_ite_eq', Finset.sum_ite_eq,
    Finset.mem_univ, if_true]
  simp only [Matrix.trace, Matrix.diag_apply, Matrix.mul_apply, Matrix.transpose_apply,
    Finset.sum_div]
  apply Finset.sum_congr rfl
  intro i _
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem phi_weighted (w v : Fin 4 → ℂ) :
    expectation phi (tensor (weighted w) (weighted v)) =
      (∑ j : Fin 4, w j * v j) / 4 := by
  rw [phi_trace]
  congr 1
  simp only [Matrix.trace, Matrix.diag_apply, Matrix.mul_apply, Matrix.transpose_apply,
    weighted_entry, shift_entry]
  simp only [mul_ite, ite_mul, zero_mul, mul_zero, one_mul, mul_one,
    Finset.sum_ite_eq, Finset.sum_ite_eq', Finset.mem_univ, if_true]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _
  simp

/-- General tensor-unitary invariance for the displayed maximally entangled state.
This is conjugation, not adjoint, on the second local observable. -/
theorem phi_unitary_pair (A : Op 4) (hA : UnitaryRel A) :
    expectation phi (tensor A (entryConj A)) = 1 := by
  rw [phi_trace]
  have ht : (entryConj A).transpose = A.conjTranspose := by
    ext i j; rfl
  rw [ht, hA.2]
  norm_num [Matrix.trace, Matrix.diag_apply, Fin.sum_univ_succ]

end CyclicBell.D4
