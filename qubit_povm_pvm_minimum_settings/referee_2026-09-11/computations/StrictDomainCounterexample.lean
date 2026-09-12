import Mathlib.Data.Matrix.Notation
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/- Exact counterexample to interpreting the manuscript's pairwise positivity
as a sufficient condition for Lorentz signature. This imports Mathlib only. -/
noncomputable section
namespace StrictDomainCounterexample
open scoped BigOperators Matrix
abbrev V := Fin 4 → ℝ
abbrev M := Matrix (Fin 4) (Fin 4) ℝ

def g : M := !![0,1/2,6/25,3/100;
                 1/2,0,3/100,6/25;
                 6/25,3/100,0,1/25;
                 3/100,6/25,1/25,0]
def ray : Fin 5 → V :=
  ![![1,0,0,0],![0,1,0,0],![0,0,1,0],![0,0,0,1],![1,1,-1,-1]]
def pair (x y : V) : ℝ := dotProduct x (g *ᵥ y)
def u : V := ![1,1,0,0]
def v : V := ![2,-2,5,-5]

theorem strict_scalar_inequalities :
    (0:ℝ)<6/25 ∧ (0:ℝ)<3/100 ∧
    (0:ℝ)<6/25+3/100+3/100+6/25-1/2 ∧
    (6/25:ℝ)+3/100<1/2 ∧ (3/100:ℝ)+6/25<1/2 := by norm_num

theorem circuit : ray 0 + ray 1 = ray 2 + ray 3 + ray 4 := by
  change (![1,0,0,0] : V) + ![0,1,0,0] =
    ![0,0,1,0] + ![0,0,0,1] + ![1,1,-1,-1]
  funext i
  fin_cases i <;> norm_num

theorem five_null_rays (i : Fin 5) : pair (ray i) (ray i) = 0 := by
  fin_cases i <;> norm_num [pair,g,ray,Matrix.mulVec,dotProduct,Fin.sum_univ_succ]

theorem all_distinct_pairings_positive (i j : Fin 5) (hij : i ≠ j) :
    0 < pair (ray i) (ray j) := by
  fin_cases i <;> fin_cases j <;>
    norm_num [pair,g,ray,Matrix.mulVec,dotProduct,Fin.sum_univ_succ] at hij ⊢

theorem unit_norm : pair u u = 1 := by
  norm_num [pair,g,u,Matrix.mulVec,dotProduct,Fin.sum_univ_succ]

theorem orthogonal : pair u v = 0 := by
  norm_num [pair,g,u,v,Matrix.mulVec,dotProduct,Fin.sum_univ_succ]

theorem second_positive_direction : pair v v = 12/5 := by
  norm_num [pair,g,v,Matrix.mulVec,dotProduct,Fin.sum_univ_succ]

theorem plane_identity (s t : ℝ) :
    pair (s • u + t • v) (s • u + t • v) = s^2 + (12/5)*t^2 := by
  norm_num [pair,g,u,v,Matrix.mulVec,dotProduct,Fin.sum_univ_succ]
  ring

theorem positive_plane (s t : ℝ) (h : s ≠ 0 ∨ t ≠ 0) :
    0 < pair (s • u + t • v) (s • u + t • v) := by
  rw [plane_identity]
  rcases h with hs | ht
  · exact add_pos_of_pos_of_nonneg (sq_pos_of_ne_zero hs)
      (mul_nonneg (by norm_num) (sq_nonneg t))
  · exact add_pos_of_nonneg_of_pos (sq_nonneg s)
      (mul_pos (by norm_num) (sq_pos_of_ne_zero ht))

#print axioms strict_scalar_inequalities
#print axioms all_distinct_pairings_positive
#print axioms five_null_rays
#print axioms plane_identity
#print axioms positive_plane
end StrictDomainCounterexample
