/- Uncompiled source. Bracket monomials of arbitrary shape, not just repeated adjoints. -/
import Kourovka.Linear.BilinearOps

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
