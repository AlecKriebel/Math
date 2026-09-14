import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic

/-! The physical two-channel system from Appendix A. All rank indices are one-based:
  a: 1 ≤ k < N; b: 2 ≤ k < N. No state at rank N occurs in this system.
  K acts on coefficient columns and equals the transpose of the printed H.
-/
namespace SymmetricSector

abbrev Channel (N : ℕ) := Fin (N - 1) ⊕ Fin (N - 2)

def c₀ (N : ℕ) : ℚ := (2 ^ N - 1) / (N * 2 ^ (N - 1))

/-- A.3 with d₀=d_N=0; natural subtraction is used only in index arithmetic. -/
def gradient (N : ℕ) : ℕ → ℚ
  | 0 => 0
  | k + 1 => if k + 1 < N then
      (k * gradient N k + 2 * N * (1 / (k + 1 : ℚ) - c₀ N)) /
        ((N : ℚ) - (k + 1)) else 0

/-- A.12–A.14, transposed to act on coefficient columns. -/
def coefficientK (N : ℕ) : Matrix (Channel N) (Channel N) ℚ
  | .inl i, .inl j =>
    let k : ℚ := i.val + 1
    if i.val = j.val then k / (2 * N)
    else if j.val = i.val + 1 then ((N : ℚ) - k - 1) / (2 * N) else 0
  | .inl i, .inr j =>
    if j.val = i.val then -1 / (N : ℚ) else 0
  | .inr i, .inl j =>
    let k : ℚ := i.val + 2
    if j.val = i.val then (k - 1) / (2 * k * N)
    else if j.val = i.val + 1 then ((N : ℚ) - k) / (2 * k * N) else 0
  | .inr i, .inr j =>
    let k : ℚ := i.val + 2
    if i.val = j.val then (N * (k - 2) + k) / (2 * k * N)
    else if i.val = j.val + 1 then (k - 1) * (k - 2) / (2 * k * N)
    else if j.val = i.val + 1 then ((N : ℚ) - k - 2) / (2 * N) else 0

/-- A.15, with the bottom b rank equal to two. -/
def source (N : ℕ) : Channel N → ℚ
  | .inl i => gradient N (i.val + 1) / 2
  | .inr i => gradient N (i.val + 1) / (2 * (i.val + 2))

/-- A.16: the b reward is negative. -/
def reward (N : ℕ) : Channel N → ℚ
  | .inl i => (Nat.choose (N - 2) i.val : ℚ) / (2 ^ (N - 1) * (N + 1))
  | .inr i => -(Nat.choose (N - 3) i.val : ℚ) / (2 ^ (N - 2) * (N + 1))

/-- The actual reduced scalar in A.17. Invertibility is a separate proof obligation. -/
noncomputable def reducedScalar (N : ℕ) : ℚ :=
  dotProduct (reward N) (((1 - coefficientK N)⁻¹).mulVec (source N))

end SymmetricSector
