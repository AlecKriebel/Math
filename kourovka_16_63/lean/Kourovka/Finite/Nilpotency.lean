/- Uncompiled source. The length-847 vanishing theorem is proved from the exact integral embedding. -/
import Kourovka.Finite.Coordinates
import Kourovka.Finite.BracketTrees
import Kourovka.Lattice.AdaptedBasis
import Mathlib.Algebra.Lie.Nilpotent

set_option maxRecDepth 10000
set_option exponentiation.threshold 2000

namespace Kourovka.Finite
open Kourovka.Linear Kourovka.Ambient
open BracketTree

/-- An arbitrary bracket tree of m ell vectors embeds into p^(2m)B. -/
theorem tree_embed_divisible (t : BracketTree (V Int)) :
    ∃ a : V Int, Lattice.embed (t.eval Lattice.LB) =
      (1009 : Int)^(2*t.length) • a := by
  induction t with
  | leaf a => exact Lattice.embed_divisible_two a
  | node t s ht hs =>
      obtain ⟨a,ha⟩ := ht
      obtain ⟨b,hb⟩ := hs
      refine ⟨Ambient.B a b, ?_⟩
      simp only [BracketTree.eval,BracketTree.length,Lattice.embed_bracket,ha,hb,
        map_smul,LinearMap.smul_apply,smul_smul]
      rw [← pow_add]
      congr 2
      omega

/-- The bounded-index reflection recovers divisibility in ell coordinates. -/
theorem integer_tree_divisible (t : BracketTree (V Int)) (ht : 2 ≤ t.length) :
    ∃ a : V Int, t.eval Lattice.LB = (1009 : Int)^(2*t.length-4) • a := by
  obtain ⟨a,ha⟩ := tree_embed_divisible t
  exact Lattice.embed_divisible_reflect (2*t.length) (by omega) _ a ha

/-- Every bracket monomial of length at least 847 vanishes at the target depth. -/
theorem monomial_vanishes (t : BracketTree (LAt 1689)) (ht : 847 ≤ t.length) :
    t.eval Lattice.LB = 0 := by
  let s := t.map (lift 1689)
  have hslen : s.length = t.length := BracketTree.length_map _ _
  obtain ⟨a,ha⟩ := integer_tree_divisible s (by omega)
  have hmap : reduce 1689 (s.eval Lattice.LB) = t.eval Lattice.LB := by
    rw [BracketTree.eval_map _ _ (reduce 1689) (reduce_bracket 1689)]
    have heq : s.map (reduce 1689) = t := by
      dsimp only [s]
      rw [BracketTree.map_map]
      have hf : reduce 1689 ∘ lift 1689 = id := funext (reduce_lift 1689)
      rw [hf,BracketTree.map_id]
    rw [heq]
  rw [← hmap,ha]
  change mapVec (Int.castRingHom (RAt 1689)) ((1009 : Int)^(2*s.length-4) • a) = 0
  rw [mapVec_smul]
  have hpow : ((1009 : Int)^(2*s.length-4) : RAt 1689) = 0 := by
    have hle : 1689 ≤ 2*s.length-4 := by omega
    have hd : (1009 : Int)^1689 ∣ (1009 : Int)^(2*s.length-4) :=
      pow_dvd_pow _ hle
    have hz := (ZMod.intCast_zmod_eq_zero_iff_dvd
      ((1009 : Int)^(2*s.length-4)) (1009^1689)).mpr
      (by simpa only [Nat.cast_pow, Nat.cast_ofNat] using hd)
    simpa only [Int.cast_pow] using hz
  change (((1009 : Int)^(2*s.length-4) : Int) : RAt 1689) •
    mapVec (Int.castRingHom (RAt 1689)) a = 0
  rw [Int.cast_pow, hpow, zero_smul]

/- The following general span argument connects bracket-tree vanishing to
mathlib's lower central series. Its index zero is the whole Lie algebra. -/
section LowerCentral
variable {R : Type*} [CommRing R]
variable {M : Type*} [LieRing M] [LieAlgebra R M]

def standardB : Bilinear R M where
  toFun a :=
    { toFun := fun b => ⁅a,b⁆
      map_add' := lie_add a
      map_smul' := by intro c v; exact lie_smul c a v }
  map_add' := by intro a b; apply LinearMap.ext; intro c; exact add_lie a b c
  map_smul' := by intro c a; apply LinearMap.ext; intro b; exact smul_lie c a b

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

section Target
local instance : LieRing (LAt 1689) := lieRingAt 1689
local instance : LieAlgebra (RAt 1689) (LAt 1689) := lieAlgebraAt 1689

/-- Standard mathlib lower central series: gamma_847=0, class at most 846. -/
theorem target_lowerCentralSeries :
    LieModule.lowerCentralSeries (RAt 1689) (LAt 1689) (LAt 1689) 846 = ⊥ := by
  apply lowerCentral_eq_bot_of_words
  intro t ht
  exact monomial_vanishes t ht
end Target

end Kourovka.Finite
