import Mathlib

/-!
# Bounded transportation on three labels (paper Appendix H)

This is a general real-parameter construction, including zero capacities.  It
is not a proof by enumerating examples. The larger geometric assertion that a
rank-zero quantum incidence point has these hypotheses remains separate.
-/

noncomputable section
open scoped BigOperators Matrix
namespace Bell.Transport

abbrev Vec := Fin 3 → ℝ
abbrev Mat := Matrix (Fin 3) (Fin 3) ℝ

def capacity (c01 c02 c12 : ℝ) : Mat :=
  !![0,c01,c02; c01,0,c12; c02,c12,0]

def candidate (c01 c02 c12 d0 d1 t : ℝ) : Mat :=
  !![0, c01/2+t, c02/2+d0-t;
     c01/2-t, 0, c12/2+d1+t;
     c02/2-d0+t, c12/2-d1-t, 0]

structure Certificate (a b : Vec) (C : Mat) where
  flow : Mat
  nonnegative : ∀ i j, 0 ≤ flow i j
  bounded : ∀ i j, flow i j ≤ C i j
  row_sum : ∀ i, ∑ j, flow i j = b i
  column_sum : ∀ j, ∑ i, flow i j = a j

/-- Finite interval Helly property, with an explicit max-of-lower-endpoints
choice. There is no compactness or choice-of-a-numerical-sample assumption. -/
theorem three_intervals (l0 l1 l2 u0 u1 u2 : ℝ)
    (h00 : l0≤u0) (h01 : l0≤u1) (h02 : l0≤u2)
    (h10 : l1≤u0) (h11 : l1≤u1) (h12 : l1≤u2)
    (h20 : l2≤u0) (h21 : l2≤u1) (h22 : l2≤u2) :
    ∃ t : ℝ, l0≤t ∧ t≤u0 ∧ l1≤t ∧ t≤u1 ∧ l2≤t ∧ t≤u2 := by
  refine ⟨max l0 (max l1 l2), le_max_left _ _, ?_, ?_, ?_, ?_, ?_⟩
  · exact max_le h00 (max_le h10 h20)
  · exact le_trans (le_max_left l1 l2) (le_max_right l0 (max l1 l2))
  · exact max_le h01 (max_le h11 h21)
  · exact le_trans (le_max_right l1 l2) (le_max_right l0 (max l1 l2))
  · exact max_le h02 (max_le h12 h22)

/-- Appendix H's construction for all three edge capacities. -/
theorem exists_capacity_transport (a b : Vec) (c01 c02 c12 : ℝ)
    (ha : ∀ i, 0≤a i) (hb : ∀ i, 0≤b i)
    (hc01 : 0≤c01) (hc02 : 0≤c02) (hc12 : 0≤c12)
    (h0 : c01+c02=a 0+b 0)
    (h1 : c01+c12=a 1+b 1)
    (h2 : c02+c12=a 2+b 2)
    (hsa : ∑ i, a i=1/2) (hsb : ∑ i, b i=1/2) :
    Nonempty (Certificate a b (capacity c01 c02 c12)) := by
  let d0 : ℝ := (b 0-a 0)/2
  let d1 : ℝ := (b 1-a 1)/2
  have ha0 := ha 0
  have ha1 := ha 1
  have ha2 := ha 2
  have hb0 := hb 0
  have hb1 := hb 1
  have hb2 := hb 2
  have hsa' : a 0+a 1+a 2=1/2 := by
    simpa [Fin.sum_univ_succ, add_assoc] using hsa
  have hsb' : b 0+b 1+b 2=1/2 := by
    simpa [Fin.sum_univ_succ, add_assoc] using hsb
  have hh : ∃ t : ℝ,
      -c01/2≤t ∧ t≤c01/2 ∧
      d0-c02/2≤t ∧ t≤d0+c02/2 ∧
      -d1-c12/2≤t ∧ t≤ -d1+c12/2 := by
    apply three_intervals
    all_goals dsimp [d0,d1] <;> linarith
  rcases hh with ⟨t,ht0,ht1,ht2,ht3,ht4,ht5⟩
  refine ⟨{
    flow := candidate c01 c02 c12 d0 d1 t
    nonnegative := ?_
    bounded := ?_
    row_sum := ?_
    column_sum := ?_ }⟩
  · intro i j
    fin_cases i <;> fin_cases j <;> norm_num [candidate] <;> linarith
  · intro i j
    fin_cases i <;> fin_cases j <;>
      norm_num [candidate,capacity] <;> linarith
  · intro i
    fin_cases i <;> norm_num [candidate,Fin.sum_univ_succ] <;>
      dsimp [d0,d1] <;> linarith
  · intro j
    fin_cases j <;> norm_num [candidate,Fin.sum_univ_succ] <;>
      dsimp [d0,d1] <;> linarith

/-- Every symmetric, zero-diagonal 3-by-3 capacity matrix has the displayed
three-edge form. -/
theorem capacity_representation (C : Mat)
    (hsym : ∀ i j, C i j=C j i) (hdiag : ∀ i, C i i=0) :
    C=capacity (C 0 1) (C 0 2) (C 1 2) := by
  funext i j
  fin_cases i <;> fin_cases j
  · exact hdiag 0
  · rfl
  · rfl
  · exact hsym 1 0
  · exact hdiag 1
  · rfl
  · exact hsym 2 0
  · exact hsym 2 1
  · exact hdiag 2

/-- General bounded-transport existence theorem with the paper's hypotheses. -/
theorem exists_transport (a b : Vec) (C : Mat)
    (ha : ∀ i, 0≤a i) (hb : ∀ i, 0≤b i)
    (hC : ∀ i j, 0≤C i j)
    (hsym : ∀ i j, C i j=C j i) (hdiag : ∀ i, C i i=0)
    (hbalance : ∀ i, ∑ j, C i j=a i+b i)
    (hsa : ∑ i, a i=1/2) (hsb : ∑ i, b i=1/2) :
    Nonempty (Certificate a b C) := by
  have heq := capacity_representation C hsym hdiag
  have h0 := hbalance 0
  have h1 := hbalance 1
  have h2 := hbalance 2
  rw [heq] at h0 h1 h2
  norm_num [capacity,Fin.sum_univ_succ] at h0 h1 h2
  rw [heq]
  exact exists_capacity_transport a b (C 0 1) (C 0 2) (C 1 2)
    ha hb (hC 0 1) (hC 0 2) (hC 1 2) h0 h1 h2 hsa hsb

namespace Certificate

variable {a b : Vec} {C : Mat}

/-- The weight of the complementary deterministic branch is nonnegative. -/
theorem complement_nonnegative (q : Certificate a b C) (i j : Fin 3) :
    0≤C i j-q.flow i j := sub_nonneg.mpr (q.bounded i j)

theorem diagonal_zero (q : Certificate a b C) (hdiag : ∀ i, C i i=0) (i : Fin 3) :
    q.flow i i=0 := by
  have hl := q.nonnegative i i
  have hu := q.bounded i i
  rw [hdiag i] at hu
  linarith

theorem complement_row (q : Certificate a b C)
    (hbalance : ∀ i, ∑ j, C i j=a i+b i) (i : Fin 3) :
    ∑ j, (C i j-q.flow i j)=a i := by
  rw [Finset.sum_sub_distrib,hbalance i,q.row_sum i]
  ring

theorem complement_column (q : Certificate a b C)
    (hbalance : ∀ j, ∑ i, C i j=a j+b j) (j : Fin 3) :
    ∑ i, (C i j-q.flow i j)=b j := by
  rw [Finset.sum_sub_distrib,hbalance j,q.column_sum j]
  ring

theorem mass_first (q : Certificate a b C) (hsb : ∑ i, b i=1/2) :
    ∑ i, ∑ j, q.flow i j=1/2 := by
  simp_rw [q.row_sum]
  exact hsb

theorem mass_second (q : Certificate a b C)
    (hbalance : ∀ i, ∑ j, C i j=a i+b i) (hsa : ∑ i, a i=1/2) :
    ∑ i, ∑ j, (C i j-q.flow i j)=1/2 := by
  simp_rw [q.complement_row hbalance]
  exact hsa

/-- Both families of deterministic branches together have total probability 1. -/
theorem total_branch_mass (q : Certificate a b C)
    (hbalance : ∀ i, ∑ j, C i j=a i+b i)
    (hsa : ∑ i, a i=1/2) (hsb : ∑ i, b i=1/2) :
    (∑ i, ∑ j, q.flow i j) + (∑ i, ∑ j, (C i j-q.flow i j))=1 := by
  rw [q.mass_first hsb,q.mass_second hbalance hsa]
  norm_num

/-- The ternary–ternary block is reproduced for every pair, not just its sums. -/
theorem ternary_block (q : Certificate a b C) (i j : Fin 3) :
    q.flow i j+(C i j-q.flow i j)=C i j := by ring

/-- The four mixed marginals used by the deterministic branch construction. -/
theorem mixed_blocks (q : Certificate a b C)
    (hrows : ∀ i, ∑ j, C i j=a i+b i)
    (hcols : ∀ j, ∑ i, C i j=a j+b j) :
    (∀ i, ∑ j, q.flow i j=b i) ∧
    (∀ i, ∑ j, (C i j-q.flow i j)=a i) ∧
    (∀ j, ∑ i, q.flow i j=a j) ∧
    (∀ j, ∑ i, (C i j-q.flow i j)=b j) := by
  exact ⟨q.row_sum,q.complement_row hrows,q.column_sum,q.complement_column hcols⟩

end Certificate
end Bell.Transport
