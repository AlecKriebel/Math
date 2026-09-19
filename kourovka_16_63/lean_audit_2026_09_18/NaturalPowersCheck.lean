import Mathlib.Tactic
namespace Kourovka.Lattice.NearIdentity
/-- Naturality of iterates uses no unjustified exact Lie-automorphism lift. -/
theorem powers_natural {R S A B : Type*} [CommRing R] [CommRing S]
    [AddCommGroup A] [Module R A] [AddCommGroup B] [Module S B]
    (f : A → B) (E : Module.End R A) (F : Module.End S B)
    (h : ∀ x, f (E x)=F (f x)) (n:Nat) (x:A) :
    f ((E^n) x)=(F^n) (f x) := by
  induction n with
  | zero => simp only [pow_zero,Module.End.one_apply]
  | succ n ih =>
    rw [pow_succ',Module.End.mul_apply,h,ih]
    rw [pow_succ',Module.End.mul_apply]


end Kourovka.Lattice.NearIdentity
