/- Uncompiled source. Sound derivation-matrix construction from the actual bracket. -/
import Kourovka.Linear.EndomorphismCoordinates
import Kourovka.Lattice.ScaledData
import Mathlib.LinearAlgebra.Matrix.ToLin

namespace Kourovka.Certificates
open Kourovka.Linear Kourovka.Ambient
open scoped BigOperators
set_option maxRecDepth 20000
set_option maxHeartbeats 2000000

abbrev Pair := {p : I × I // p.1 < p.2}
abbrev Row := Pair × I
abbrev Col := I × I

theorem num_pairs : Fintype.card Pair = 465 := by decide +kernel
theorem num_rows : Fintype.card Row = 14415 := by
  simp [Row, Fintype.card_prod, num_pairs, I]
theorem num_cols : Fintype.card Col = 961 := by
  simp [Col, Fintype.card_prod, I]

variable {R : Type*} [CommRing R]

/-- The matrix is DEFINED by the derivation operator on matrix units. -/
def derivationMatrix (b : Bilinear R (V R)) : Matrix Row Col R :=
  fun row col => delta b (elementary col.1 col.2)
    (unitVec row.1.val.1) (unitVec row.1.val.2) row.2

def coefficient (b : Bilinear R (V R)) (i j k : I) : R := b (unitVec i) (unitVec j) k

/-- The standard three-term formula is a theorem, not a separately assumed input table. -/
theorem matrix_entry (b : Bilinear R (V R)) (row : Row) (col : Col) :
    derivationMatrix b row col =
      (if row.2 = col.1 then coefficient b row.1.val.1 row.1.val.2 col.2 else 0) -
      (if row.1.val.1 = col.2 then coefficient b col.1 row.1.val.2 row.2 else 0) -
      (if row.1.val.2 = col.2 then coefficient b row.1.val.1 col.1 row.2 else 0) := by
  rcases row with ⟨⟨⟨i,j⟩,hij⟩,k⟩
  rcases col with ⟨a,c⟩
  by_cases hka : k = a <;> by_cases hic : i = c <;> by_cases hjc : j = c <;>
    simp [derivationMatrix,coefficient,delta_apply,elementary,unitVec,
      hka,hic,hjc,eq_comm,LinearMap.smul_apply,smul_eq_mul]

def matrixLinear (b : Bilinear R (V R)) : (Col → R) →ₗ[R] (Row → R) where
  toFun d := fun row => ∑ col, derivationMatrix b row col * d col
  map_add' := by intro d e; funext row; simp [mul_add,Finset.sum_add_distrib]
  map_smul' := by
    intro c d
    funext row
    simp only [Pi.smul_apply,smul_eq_mul,Finset.mul_sum,RingHom.id_apply]
    apply Finset.sum_congr rfl
    intro col hcol
    ring

/-- The linearized equations on every ordered pair are precisely K times the entry vector. -/
theorem matrix_apply (b : Bilinear R (V R)) (d : Col → R) (row : Row) :
    matrixLinear b d row =
      delta b (fromEntries d) (unitVec row.1.val.1) (unitVec row.1.val.2) row.2 := by
  change (∑ col, derivationMatrix b row col * d col) = _
  have hh : delta b (fromEntries d) =
      ∑ col : Col, d col • delta b (elementary col.1 col.2) := by
    have hexpand : fromEntries d = ∑ col : Col, d col • elementary col.1 col.2 := rfl
    rw [hexpand]
    simp only [map_sum,map_smul]
  rw [hh]
  simp only [LinearMap.sum_apply,LinearMap.smul_apply,Finset.sum_apply,
    Pi.smul_apply,smul_eq_mul,derivationMatrix]
  apply Finset.sum_congr rfl
  intro col hcol
  ring

theorem bracket_skew (b : Bilinear R (V R)) (halt : ∀ u, b u u = 0) (u v : V R) :
    b u v = -b v u := by
  have hh := halt (u+v)
  simp only [map_add,LinearMap.add_apply,halt,zero_add,add_zero] at hh
  exact eq_neg_iff_add_eq_zero.mpr (by simpa only [add_comm] using hh)

theorem delta_alternating (b : Bilinear R (V R)) (halt : ∀ u, b u u = 0)
    (D : V R →ₗ[R] V R) (u : V R) : delta b D u u = 0 := by
  rw [delta_apply,halt,map_zero,bracket_skew b halt (D u) u]
  abel

theorem delta_skew (b : Bilinear R (V R)) (halt : ∀ u, b u u = 0)
    (D : V R →ₗ[R] V R) (u v : V R) : delta b D u v = -delta b D v u := by
  simp only [delta_apply]
  rw [bracket_skew b halt v u,bracket_skew b halt (D v) u,
    bracket_skew b halt v (D u),map_neg]
  abel

/-- Ordered-pair rows suffice because alternation is proved, including the diagonal cases. -/
theorem zero_of_ordered_basis (b : Bilinear R (V R)) (halt : ∀ u, b u u = 0)
    (D : V R →ₗ[R] V R)
    (h : ∀ row : Row, delta b D (unitVec row.1.val.1) (unitVec row.1.val.2) row.2 = 0) :
    delta b D = 0 := by
  apply ext_bilinear
  intro i j
  rcases lt_trichotomy i j with hij | hij | hji
  · funext k
    exact h (⟨(i,j),hij⟩,k)
  · subst j
    exact delta_alternating b halt D (unitVec i)
  · rw [delta_skew b halt D]
    have hh : delta b D (unitVec j) (unitVec i) = 0 := by
      funext k
      exact h (⟨(j,i),hji⟩,k)
    simp only [hh,neg_zero,LinearMap.zero_apply]

def DerivationCondition (b : Bilinear R (V R)) (D : V R →ₗ[R] V R) : Prop :=
  ∀ u v, D (b u v) = b (D u) v + b u (D v)

theorem derivation_iff_delta_zero (b : Bilinear R (V R)) (D : V R →ₗ[R] V R) :
    DerivationCondition b D ↔ delta b D = 0 := by
  constructor
  · intro h
    apply LinearMap.ext
    intro u
    apply LinearMap.ext
    intro v
    change delta b D u v = 0
    rw [delta_apply,h]
    abel
  · intro h u v
    have hh : delta b D u v = 0 := by rw [h]; rfl
    rw [delta_apply] at hh
    calc
      D (b u v) = (D (b u v)-b (D u) v-b u (D v)) + (b (D u) v+b u (D v)) := by abel
      _ = b (D u) v+b u (D v) := by rw [hh,zero_add]

theorem kernel_iff_derivation (b : Bilinear R (V R)) (halt : ∀ u, b u u = 0)
    (d : Col → R) : matrixLinear b d = 0 ↔ DerivationCondition b (fromEntries d) := by
  rw [derivation_iff_delta_zero]
  constructor
  · intro h
    apply zero_of_ordered_basis b halt
    intro row
    rw [← matrix_apply]
    exact congrFun h row
  · intro h
    funext row
    rw [matrix_apply,h]
    rfl

/-- A set equivalence with the COMPLETE derivation kernel. -/
def derivationsEquivKernel (b : Bilinear R (V R)) (halt : ∀ u, b u u = 0) :
    {D : V R →ₗ[R] V R // DerivationCondition b D} ≃
      {d : Col → R // matrixLinear b d = 0} where
  toFun D := ⟨toEntries D.val, (kernel_iff_derivation b halt _).mpr
    (by simpa only [fromEntries_entries] using D.property)⟩
  invFun d := ⟨fromEntries d.val,(kernel_iff_derivation b halt _).mp d.property⟩
  left_inv := by intro D; apply Subtype.ext; exact fromEntries_entries D.val
  right_inv := by intro d; apply Subtype.ext; exact entries_fromEntries d.val

/-- The actual matrix in the paper, with integer coefficients and no guessed rank. -/
def K : Matrix Row Col Int := derivationMatrix Lattice.LB

def Kmod (n : Nat) : Matrix Row Col (ZMod n) := derivationMatrix Lattice.LB

end Kourovka.Certificates
