/- Soundness of exact associative coefficient cancellation for
homogeneous Lie identities. This supplies a reusable BCH proof ingredient, not the
BCH associativity theorem or the converse automorphism reconstruction. -/
import Kourovka.BCH.Dynkin
import Mathlib.Data.Finset.Defs

namespace Kourovka.BCH
open scoped BigOperators

namespace Poly
variable {α M : Type*} [DecidableEq α] [AddCommGroup M]

/-- Integer coefficients after collecting equal associative words. -/
def coeff (P : Poly α) (w : List α) : Int :=
  match P with
  | [] => 0
  | (c,u)::P => (if u=w then c else 0)+coeff P w

def support (P : Poly α) : Finset (List α) := (P.map Prod.snd).toFinset

@[simp] theorem coeff_nil (w : List α) : coeff ([] : Poly α) w=0 := rfl

@[simp] theorem coeff_cons (c:Int) (u w:List α) (P:Poly α) :
    coeff ((c,u)::P) w=(if u=w then c else 0)+coeff P w := rfl

@[simp] theorem coeff_append (P Q:Poly α) (w:List α) :
    coeff (P++Q) w=coeff P w+coeff Q w := by
  induction P with
  | nil => simp [coeff]
  | cons a P ih => rcases a with ⟨c,u⟩; simp only [List.cons_append,coeff,ih]; omega

@[simp] theorem coeff_neg (P:Poly α) (w:List α) : coeff (neg P) w= -coeff P w := by
  induction P with
  | nil => simp [neg,coeff]
  | cons a P ih =>
    rcases a with ⟨c,u⟩
    change (if u=w then -c else 0)+coeff (neg P) w= -((if u=w then c else 0)+coeff P w)
    rw [ih]
    split <;> omega

@[simp] theorem mem_support (P:Poly α) (w:List α) :
    w∈support P ↔ ∃ c, (c,w)∈P := by
  simp only [support,List.mem_toFinset,List.mem_map]
  constructor
  · rintro ⟨⟨c,u⟩,h,heq⟩
    change u=w at heq
    subst u
    exact ⟨c,h⟩
  · rintro ⟨c,h⟩
    exact ⟨(c,w),h,rfl⟩

/-- Nonlisted words have coefficient zero; no oracle for polynomial equality is used. -/
theorem coeff_eq_zero_of_not_mem (P:Poly α) (w:List α) (h:w∉support P) : coeff P w=0 := by
  induction P with
  | nil => rfl
  | cons a P ih =>
    rcases a with ⟨c,u⟩
    have hu : u≠w := by
      intro hh
      apply h
      exact (mem_support _ _).mpr ⟨c,by simp [hh]⟩
    have hp : w∉support P := by
      intro hw
      apply h
      obtain ⟨b,hb⟩ := (mem_support _ _).mp hw
      exact (mem_support _ _).mpr ⟨b,List.mem_cons_of_mem _ hb⟩
    rw [coeff,if_neg hu,zero_add,ih hp]

/-- Evaluation can be regrouped on any finite set containing the listed words. -/
theorem sumEval_eq_sum (f:List α→M) (P:Poly α) (S:Finset (List α))
    (h : ∀ c w, (c,w)∈P → w∈S) :
    sumEval f P=∑ w∈S, coeff P w • f w := by
  induction P with
  | nil => simp [sumEval,coeff]
  | cons a P ih =>
    rcases a with ⟨c,u⟩
    have hu : u∈S := h c u (by simp)
    have hp : ∀ c w, (c,w)∈P → w∈S := fun c w hw => h c w (List.mem_cons_of_mem _ hw)
    rw [sumEval,ih hp]
    simp only [coeff_cons,add_zsmul,Finset.sum_add_distrib]
    have hone : (∑ w∈S, (if u=w then c else 0) • f w)=c • f u := by
      rw [Finset.sum_eq_single u]
      · simp
      · intro w hw hwu
        simp [Ne.symm hwu]
      · intro hnu
        exact (hnu hu).elim
    rw [hone]

/-- Equal collected coefficients imply equal evaluations into ANY additive commutative group. -/
theorem sumEval_eq_of_coeff_eq (f:List α→M) (P Q:Poly α)
    (h:∀ w,coeff P w=coeff Q w) : sumEval f P=sumEval f Q := by
  let S := support P ∪ support Q
  have hp : ∀ c w,(c,w)∈P → w∈S := by
    intro c w hw
    exact Finset.mem_union_left _ ((mem_support _ _).mpr ⟨c,hw⟩)
  have hq : ∀ c w,(c,w)∈Q → w∈S := by
    intro c w hw
    exact Finset.mem_union_right _ ((mem_support _ _).mpr ⟨c,hw⟩)
  rw [sumEval_eq_sum f P S hp,sumEval_eq_sum f Q S hq]
  exact Finset.sum_congr rfl (fun w _ => by rw [h w])

/-- Finite checking surface; acceptance is a proposition, not an imported certificate axiom. -/
def ZeroCoefficients (P:Poly α) : Prop := ∀ w∈support P,coeff P w=0

instance (P:Poly α) : Decidable (ZeroCoefficients P) := by
  unfold ZeroCoefficients
  infer_instance

theorem zeroCoefficients_sound (f:List α→M) (P:Poly α) (h:ZeroCoefficients P) :
    sumEval f P=0 := by
  have hc : ∀ w,coeff P w=coeff ([] : Poly α) w := by
    intro w
    by_cases hw:w∈support P
    · exact h w hw
    · exact coeff_eq_zero_of_not_mem P w hw
  exact sumEval_eq_of_coeff_eq f P [] hc

end Poly

/-- Finite integer combinations of Lie words. Rational BCH coefficients require a separate
clearing-denominators and unit argument; they are not smuggled into this integer interface. -/
abbrev LiePoly (α:Type*) := List (Int × LieWord α)

namespace LiePoly
variable {α L:Type*} [LieRing L]

def eval (s:α→L) : LiePoly α→L
  | [] => 0
  | (c,t)::P => c • LieWord.eval s t+eval s P

def expand : LiePoly α→Poly α
  | [] => []
  | (c,t)::P => Poly.shift c [] (LieWord.expand t)++expand P

def Homogeneous (n:Nat) (P:LiePoly α) : Prop := ∀ z∈P,LieWord.degree z.2=n

/-- Dynkin reconstruction of a homogeneous INTEGER Lie polynomial. -/
theorem dynkin_expand (s:α→L) (n:Nat) (P:LiePoly α) (h:Homogeneous n P) :
    dynkin s (expand P)=n • eval s P := by
  induction P with
  | nil => simp [expand,dynkin,Poly.sumEval,eval]
  | cons a P ih =>
    rcases a with ⟨c,t⟩
    have ht : LieWord.degree t=n := h (c,t) (by simp)
    have hp : Homogeneous n P := fun z hz => h z (List.mem_cons_of_mem _ hz)
    change dynkin s (Poly.shift c [] (LieWord.expand t)++expand P)=_
    rw [dynkin,Poly.sumEval_append]
    change dynkin s (Poly.shift c [] (LieWord.expand t))+dynkin s (expand P)=_
    rw [dynkin_shift s c [] _ (LieWord.expansion_nonempty t),wordAction,
      Kourovka.BCH.dynkin_expand,ht,ih hp]
    change c • (n • LieWord.eval s t) + n • eval s P =
      n • (c • LieWord.eval s t + eval s P)
    rw [nsmul_add, smul_comm c n]

/-- A proof-producing route from collected associative coefficients to a Lie identity.
The explicit injectivity hypothesis is necessary in torsion; it must be discharged
at every degree to apply this to the paper's finite ring. -/
theorem eval_zero_of_coeff_zero [DecidableEq α] (s:α→L) (n:Nat) (P:LiePoly α)
    (hdegree:Homogeneous n P)
    (hinj:Function.Injective (fun z:L => n • z))
    (hcoeff:Poly.ZeroCoefficients (expand P)) : eval s P=0 := by
  apply hinj
  change n • eval s P = n • (0 : L)
  rw [← dynkin_expand s n P hdegree,nsmul_zero]
  exact Poly.zeroCoefficients_sound (dynkinWord s) (expand P) hcoeff

end LiePoly
end Kourovka.BCH
