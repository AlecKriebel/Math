/-
UNCOMPILED research source: the original integer coefficient formula.
No LieRing instance is declared. Alternation, Jacobi, the change of basis,
and the correspondence to the exported data remain named obligations.
-/
import Mathlib.Data.Int.Basic
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Algebra.BigOperators.Ring.Finset

namespace Kourovka.Raw

/-- Falling factorial; for r>a the product includes zero. -/
def falling (a r : Nat) : Int :=
  ((List.range r).map fun j => (a : Int) - (j : Int)).prod

/-- Raw (not factorial-normalized) transvectant coefficient. -/
def transvectant (m n r i j : Nat) : Int :=
  ((List.range (r + 1)).map fun q =>
    (-1 : Int) ^ q * (Nat.choose r q : Int) *
      falling (m - i) (r - q) * falling i q *
      falling (n - j) q * falling j (r - q)).sum

structure Summand where
  degree : Nat
  start : Nat
  deriving DecidableEq, Repr

def summands : List Summand :=
  [⟨6, 3⟩, ⟨4, 10⟩, ⟨6, 15⟩, ⟨2, 22⟩, ⟨4, 25⟩, ⟨0, 30⟩]

/-- The sl2 action on one indicated homogeneous-binary-form summand. -/
def moduleCoefficient (s : Summand) (i j k : Nat) : Int :=
  if s.start ≤ j ∧ j ≤ s.start + s.degree then
    if i = 0 ∧ k = j then (s.degree : Int) - 2 * ((j - s.start : Nat) : Int)
    else if i = 1 ∧ s.start < j ∧ k + 1 = j then ((j - s.start : Nat) : Int)
    else if i = 2 ∧ j < s.start + s.degree ∧ k = j + 1 then
      ((s.degree - (j - s.start) : Nat) : Int)
    else 0
  else 0

structure Product where
  leftDegree : Nat
  leftStart : Nat
  rightDegree : Nat
  rightStart : Nat
  outputStart : Nat
  contraction : Nat
  deriving DecidableEq, Repr

def products : List Product :=
  [⟨6, 3, 6, 3, 15, 3⟩,
   ⟨6, 3, 4, 10, 22, 4⟩,
   ⟨6, 3, 6, 15, 22, 5⟩,
   ⟨6, 3, 4, 25, 22, 4⟩,
   ⟨4, 10, 4, 10, 22, 3⟩,
   ⟨4, 10, 4, 25, 30, 4⟩,
   ⟨4, 25, 4, 25, 22, 3⟩]

def productCoefficient (s : Product) (i j k : Nat) : Int :=
  if s.leftStart ≤ i ∧ i ≤ s.leftStart + s.leftDegree ∧
      s.rightStart ≤ j ∧ j ≤ s.rightStart + s.rightDegree then
    let a := i - s.leftStart
    let b := j - s.rightStart
    if s.contraction ≤ a + b ∧
        a + b - s.contraction ≤ s.leftDegree + s.rightDegree - 2 * s.contraction ∧
        k = s.outputStart + a + b - s.contraction then
      transvectant s.leftDegree s.rightDegree s.contraction a b
    else 0
  else 0

def orderedCoefficient (i j k : Nat) : Int :=
  (if i = 0 ∧ j = 1 ∧ k = 1 then 2
   else if i = 0 ∧ j = 2 ∧ k = 2 then -2
   else if i = 1 ∧ j = 2 ∧ k = 0 then 1 else 0) +
  (summands.map fun s => moduleCoefficient s i j k).sum +
  (products.map fun s => productCoefficient s i j k).sum

/-- Valid basis indices are Fin 31. This extension to Nat makes certificate generation simple. -/
def coefficient (i j k : Nat) : Int :=
  if i < j then orderedCoefficient i j k
  else if j < i then -orderedCoefficient j i k
  else 0

/-- All nonzero skew-half entries, in lexicographic (i,j,k) order. -/
def reconstructedTerms : List (Nat × Nat × Nat × Int) :=
  (List.range 31).flatMap fun i =>
    (List.range 31).flatMap fun j =>
      if i < j then
        (List.range 31).flatMap fun k =>
          let c := coefficient i j k
          if c = 0 then [] else [(i, j, k, c)]
      else []

end Kourovka.Raw
