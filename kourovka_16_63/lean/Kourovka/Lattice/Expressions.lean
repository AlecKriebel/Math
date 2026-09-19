/- Uncompiled source. Integral expressions and exact error-tolerant generation. -/
import Kourovka.Linear.BilinearOps

namespace Kourovka.Lattice

inductive Expr where
  | x
  | y
  | add (a b : Expr)
  | scale (c : Int) (a : Expr)
  | bracket (a b : Expr)

namespace Expr
variable {M : Type*} [AddCommGroup M]

def eval (br : M → M → M) (x y : M) : Expr → M
  | .x => x
  | .y => y
  | .add a b => eval br x y a + eval br x y b
  | .scale c a => c • eval br x y a
  | .bracket a b => br (eval br x y a) (eval br x y b)

variable {N : Type*} [AddCommGroup N]

theorem map_eval (f : M →+ N) (b : M → M → M) (c : N → N → N)
    (hf : ∀ u v, f (b u v) = c (f u) (f v)) (x y : M) (e : Expr) :
    f (eval b x y e) = eval c (f x) (f y) e := by
  induction e with
  | x => rfl
  | y => rfl
  | add a b ha hb => simp only [eval,map_add,ha,hb]
  | scale c a ha => simp only [eval,map_zsmul,ha]
  | bracket a b ha hb => simp only [eval,hf,ha,hb]

variable {R : Type*} [CommRing R] [Module R M]

theorem eval_mem (S : Submodule R M) (br : M → M → M)
    (hbr : ∀ a, a ∈ S → ∀ b, b ∈ S → br a b ∈ S)
    (x y : M) (hx : x ∈ S) (hy : y ∈ S) (e : Expr) : eval br x y e ∈ S := by
  induction e with
  | x => exact hx
  | y => exact hy
  | add a b ha hb => exact S.add_mem ha hb
  | scale c a ha =>
      exact (c • (⟨eval br x y a,ha⟩ : S)).property
  | bracket a b ha hb => exact hbr _ ha _ hb

/-- Approximate bracket preservation suffices for integrality on generated expressions. -/
theorem approximate_map_mem (S : Submodule R M) (br : M → M → M)
    (hbr : ∀ a, a ∈ S → ∀ b, b ∈ S → br a b ∈ S)
    (Q : M →ₗ[R] M) (x y : M) (hx : x ∈ S) (hy : y ∈ S)
    (hQx : Q x ∈ S) (hQy : Q y ∈ S)
    (herror : ∀ a, a ∈ S → ∀ b, b ∈ S → Q (br a b) - br (Q a) (Q b) ∈ S)
    (e : Expr) : Q (eval br x y e) ∈ S := by
  induction e with
  | x => exact hQx
  | y => exact hQy
  | add a b ha hb => simpa only [eval,map_add] using S.add_mem ha hb
  | scale c a ha =>
      simpa only [eval,map_zsmul] using
        (c • (⟨Q (eval br x y a),ha⟩ : S)).property
  | bracket a b ha hb =>
      have hE := herror _ (eval_mem S br hbr x y hx hy a)
        _ (eval_mem S br hbr x y hx hy b)
      have hB := hbr _ ha _ hb
      simpa only [eval,sub_add_cancel] using S.add_mem hE hB

/-- The analogous lemma for an approximate derivation, again on all generated expressions. -/
theorem approximate_derivation_mem (S : Submodule R M) (br : M → M → M)
    (hbr : ∀ a, a ∈ S → ∀ b, b ∈ S → br a b ∈ S)
    (D : M →ₗ[R] M) (x y : M) (hx : x ∈ S) (hy : y ∈ S)
    (hDx : D x ∈ S) (hDy : D y ∈ S)
    (herror : ∀ a, a ∈ S → ∀ b, b ∈ S →
      D (br a b) - br (D a) b - br a (D b) ∈ S)
    (e : Expr) : D (eval br x y e) ∈ S := by
  induction e with
  | x => exact hDx
  | y => exact hDy
  | add a b ha hb => simpa only [eval,map_add] using S.add_mem ha hb
  | scale c a ha =>
      simpa only [eval,map_zsmul] using
        (c • (⟨D (eval br x y a),ha⟩ : S)).property
  | bracket a b ha hb =>
      have ha' := eval_mem S br hbr x y hx hy a
      have hb' := eval_mem S br hbr x y hx hy b
      have hE := herror _ ha' _ hb'
      have hh := S.add_mem (S.add_mem hE (hbr _ ha _ hb')) (hbr _ ha' _ hb)
      have heq : D (br (eval br x y a) (eval br x y b)) =
        (D (br (eval br x y a) (eval br x y b)) -
          br (D (eval br x y a)) (eval br x y b) -
          br (eval br x y a) (D (eval br x y b)) +
          br (D (eval br x y a)) (eval br x y b)) +
          br (eval br x y a) (D (eval br x y b)) := by abel
      rw [eval,heq]
      exact hh

end Expr
end Kourovka.Lattice
