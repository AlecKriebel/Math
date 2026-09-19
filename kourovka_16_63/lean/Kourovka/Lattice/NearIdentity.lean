/- Uncompiled source. The precise TWO-LATTICE power estimate and finite invertibility.
An endomorphism small in the ambient B basis need not be p times an endomorphism
in the ell basis. The loss of two powers is proved from the actual embedding. -/
import Kourovka.Finite.Coordinates
import Kourovka.Lattice.AdaptedBasis
import Kourovka.Analytic.NilpotentUnit

namespace Kourovka.Lattice.NearIdentity
open Kourovka.Ambient Kourovka.Finite

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

/-- Ambient smallness means embed(Ea)=p*C(embed(a)), with C integral on B. -/
theorem ambient_power_divisible (E C : Module.End Int (V Int))
    (h : ∀ a, embed (E a)=(1009:Int) • C (embed a)) (n:Nat) (a:V Int) :
    ∃ b:V Int, embed ((E^n) a)=(1009:Int)^(n+2) • b := by
  induction n with
  | zero => simpa only [pow_zero,Module.End.one_apply,zero_add] using embed_divisible_two a
  | succ n ih =>
    obtain ⟨b,hb⟩ := ih
    refine ⟨C b,?_⟩
    rw [pow_succ',Module.End.mul_apply,h,hb,map_smul,smul_smul]
    have hn : n+1+2=(n+2)+1 := by omega
    rw [hn, pow_succ' (1009 : Int) (n+2)]

/-- In ell coordinates the gain is n-2, not n. This is where the distinct lattices matter. -/
theorem ell_power_divisible (E C : Module.End Int (V Int))
    (h : ∀ a, embed (E a)=(1009:Int) • C (embed a)) (n:Nat) (hn:2≤n) (a:V Int) :
    ∃ b:V Int, (E^n) a=(1009:Int)^(n-2) • b := by
  obtain ⟨b,hb⟩ := ambient_power_divisible E C h n a
  have hh := embed_divisible_reflect (n+2) (by omega) ((E^n) a) b hb
  have he : n+2-4=n-2 := by omega
  simpa only [he] using hh

theorem reduce_scalar_modulus (i:Nat) (a:V Int) :
    reduce i ((1009:Int)^i • a)=0 := by
  apply (reduce_eq_zero_iff i _).mpr
  intro j
  exact ⟨a j,rfl⟩

/-- The reduced small endomorphism is nilpotent even if its reduction modulo p
in the ell basis is nonzero. Every residue vector is covered using surjectivity. -/
theorem finite_power_zero (i:Nat) (E C : Module.End Int (V Int))
    (h : ∀ a, embed (E a)=(1009:Int) • C (embed a))
    (F : Module.End (RAt i) (LAt i))
    (hred : ∀ a, reduce i (E a)=F (reduce i a)) : F^(i+2)=0 := by
  apply LinearMap.ext
  intro a
  obtain ⟨z,hz⟩ := reduce_surjective i a
  obtain ⟨b,hb⟩ := ell_power_divisible E C h (i+2) (by omega) z
  have he : i+2-2=i := by omega
  rw [he] at hb
  have hn := powers_natural (reduce i) E F hred (i+2) z
  rw [hb,reduce_scalar_modulus,hz] at hn
  exact hn.symm

/-- A constructive finite geometric inverse, not a claim about exp/log convergence. -/
def finiteOneAddUnit (i:Nat) (E C : Module.End Int (V Int))
    (h : ∀ a, embed (E a)=(1009:Int) • C (embed a))
    (F : Module.End (RAt i) (LAt i))
    (hred : ∀ a, reduce i (E a)=F (reduce i a)) : (Module.End (RAt i) (LAt i))ˣ :=
  Kourovka.Analytic.oneAddUnit F (i+2) (finite_power_zero i E C h F hred)

@[simp] theorem finiteOneAddUnit_value (i:Nat) (E C : Module.End Int (V Int))
    (h : ∀ a, embed (E a)=(1009:Int) • C (embed a))
    (F : Module.End (RAt i) (LAt i))
    (hred : ∀ a, reduce i (E a)=F (reduce i a)) :
    (finiteOneAddUnit i E C h F hred : Module.End (RAt i) (LAt i))=1+F := by
  exact Kourovka.Analytic.oneAddUnit_val F (i+2) (finite_power_zero i E C h F hred)

end Kourovka.Lattice.NearIdentity
