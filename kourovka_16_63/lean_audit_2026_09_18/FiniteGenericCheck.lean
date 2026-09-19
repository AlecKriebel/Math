/- Uncompiled source. Bracket monomials of arbitrary shape, not just repeated adjoints. -/
import Mathlib.Algebra.Lie.Nilpotent
import Mathlib.Tactic
namespace Kourovka.Linear
abbrev Bilinear (R V : Type*) [CommRing R] [AddCommGroup V] [Module R V] := V →ₗ[R] V →ₗ[R] V
end Kourovka.Linear

namespace Kourovka.Finite

inductive BracketTree (V : Type*) where
  | leaf (value : V)
  | node (left right : BracketTree V)

namespace BracketTree
variable {R : Type*} [CommRing R]
variable {V : Type*} [AddCommGroup V] [Module R V]

/-- Number of input leaves, i.e. bracket length. -/
def length : BracketTree V → Nat
  | .leaf _ => 1
  | .node a b => a.length + b.length

def eval (b : Kourovka.Linear.Bilinear R V) : BracketTree V → V
  | .leaf a => a
  | .node a c => b (eval b a) (eval b c)

def map {W : Type*} (f : V → W) : BracketTree V → BracketTree W
  | .leaf a => .leaf (f a)
  | .node a b => .node (map f a) (map f b)

@[simp] theorem length_map {W : Type*} (f : V → W) (t : BracketTree V) :
    (t.map f).length = t.length := by
  induction t with
  | leaf a => rfl
  | node a b ha hb => simp only [map,length,ha,hb]

theorem length_pos (t : BracketTree V) : 0 < t.length := by
  induction t with
  | leaf a => exact Nat.zero_lt_one
  | node a b ha hb => dsimp [length]; omega

variable {S : Type*} [CommRing S]
variable {W : Type*} [AddCommGroup W] [Module S W]

/-- Naturality needs only an actual bracket-preserving function. -/
theorem eval_map (b : Kourovka.Linear.Bilinear R V) (c : Kourovka.Linear.Bilinear S W)
    (f : V → W) (hf : ∀ a d, f (b a d) = c (f a) (f d)) (t : BracketTree V) :
    f (t.eval b) = (t.map f).eval c := by
  induction t with
  | leaf a => rfl
  | node a d ha hd => simp only [eval,map,hf,ha,hd]

@[simp] theorem map_map {W X : Type*} (f : V → W) (g : W → X) (t : BracketTree V) :
    (t.map f).map g = t.map (g ∘ f) := by
  induction t with
  | leaf a => rfl
  | node a b ha hb => simp only [map,ha,hb]

@[simp] theorem map_id (t : BracketTree V) : t.map id = t := by
  induction t with
  | leaf a => rfl
  | node a b ha hb => simp only [map,ha,hb]

end BracketTree
end Kourovka.Finite

namespace Kourovka.Finite
open Kourovka.Linear
section LowerCentral
variable {R : Type*} [CommRing R]
variable {M : Type*} [LieRing M] [LieAlgebra R M]

def standardB : Bilinear R M where
  toFun a :=
    { toFun := fun b => ⁅a,b⁆
      map_add' := lie_add a
      map_smul' := by intro c v; exact lie_smul c a v }
  map_add' := by intro a b; ext c; exact add_lie a b c
  map_smul' := by intro c a; ext b; exact smul_lie c a b

/-- All shapes of bracket monomials, closed under linear combinations. -/
def wordSpan (n : Nat) : Submodule R M :=
  Submodule.span R {a | ∃ t : BracketTree M, n ≤ t.length ∧ t.eval (standardB (R := R)) = a}

theorem bracket_mem_wordSpan (n : Nat) (a b : M) (hb : b ∈ wordSpan (R := R) n) :
    ⁅a,b⁆ ∈ wordSpan (R := R) (n+1) := by
  induction hb using Submodule.span_induction with
  | mem b hb =>
      obtain ⟨t,ht,rfl⟩ := hb
      apply Submodule.subset_span
      exact ⟨BracketTree.node (BracketTree.leaf a) t, by simp only [BracketTree.length]; omega, rfl⟩
  | zero => simpa only [lie_zero] using (wordSpan (R := R) (n+1)).zero_mem
  | add b c hb hc ihb ihc =>
      rw [lie_add]
      exact Submodule.add_mem _ ihb ihc
  | smul c b hb ih =>
      rw [lie_smul]
      exact Submodule.smul_mem _ _ ih

/-- Lower-central term n is spanned by words with at least n+1 leaves. -/
theorem lowerCentral_le_wordSpan (n : Nat) :
    (LieModule.lowerCentralSeries R M M n).toSubmodule ≤ wordSpan (R := R) (n+1) := by
  induction n with
  | zero =>
      intro a ha
      apply Submodule.subset_span
      exact ⟨BracketTree.leaf a,by exact Nat.le_refl 1,rfl⟩
  | succ n ih =>
      rw [LieModule.lowerCentralSeries_succ,LieSubmodule.lieIdeal_oper_eq_linear_span']
      apply Submodule.span_le.mpr
      rintro a ⟨b,hb,c,hc,rfl⟩
      exact bracket_mem_wordSpan (n+1) b c (ih hc)

theorem lowerCentral_eq_bot_of_words (n : Nat)
    (h : ∀ t : BracketTree M, n+1 ≤ t.length → t.eval (standardB (R := R)) = 0) :
    LieModule.lowerCentralSeries R M M n = ⊥ := by
  apply (LieSubmodule.eq_bot_iff _).mpr
  intro a ha
  have hspan : wordSpan (R := R) (n+1) ≤ (⊥ : Submodule R M) := by
    apply Submodule.span_le.mpr
    rintro a ⟨t,ht,rfl⟩
    simpa only [Submodule.mem_bot] using h t ht
  have hh := hspan (lowerCentral_le_wordSpan n ha)
  simpa only [Submodule.mem_bot] using hh
end LowerCentral


end Kourovka.Finite
