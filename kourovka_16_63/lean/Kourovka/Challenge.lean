/-
UNCOMPILED independently readable challenge, not a proof or an axiom.
No custom automorphism type is used. No BCH group instance is postulated.
-/
import Kourovka.Parameters
import Mathlib.Algebra.Group.End
import Mathlib.SetTheory.Cardinal.Finite
import Mathlib.Algebra.Ring.Parity

namespace Kourovka.Challenge

def ExactOrders (G : Type*) [Group G] : Prop :=
  Finite G ∧ Nat.card G = 1009 ^ 52359 ∧
    Nat.card (MulAut G) = 1009 ^ 52359

def NotebookAffirmative : Prop :=
  ∃ p n : Nat, Nat.Prime p ∧ Odd p ∧ 0 < n ∧
    ∃ G : Type, ∃ g : Group G,
      letI := g
      Finite G ∧ Nontrivial G ∧ Nat.card G = p ^ n ∧
        Nat.card (MulAut G) = Nat.card G

end Kourovka.Challenge
