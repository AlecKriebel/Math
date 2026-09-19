/- A Dynkin--Specht--Wever reconstruction ingredient, proved by word induction.
It is not a proof of BCH associativity or the finite Lazard correspondence. -/
import Mathlib.Algebra.Lie.Basic
import Mathlib.Tactic

namespace Kourovka.BCH

inductive LieWord (α:Type*) where
  | atom : α → LieWord α
  | comm : LieWord α → LieWord α → LieWord α

namespace LieWord

def degree {α:Type*} : LieWord α → Nat
  | .atom _ => 1
  | .comm a b => degree a+degree b

def eval {α L:Type*} [LieRing L] (s:α→L) : LieWord α → L
  | .atom a => s a
  | .comm a b => ⁅eval s a,eval s b⁆

theorem degree_pos {α:Type*} (t:LieWord α) : 0<degree t := by
  induction t with
  | atom a => exact Nat.zero_lt_one
  | comm a b ha hb => change 0<degree a+degree b; omega

end LieWord

/-- Signed noncommutative word lists. Repeated words are deliberately not silently canceled. -/
abbrev Poly (α:Type*) := List (Int × List α)

namespace Poly
variable {α:Type*}

def neg (P:Poly α) : Poly α := P.map (fun z => (-z.1,z.2))
def shift (c:Int) (w:List α) (P:Poly α) : Poly α := P.map (fun z => (c*z.1,w++z.2))
def mul (P Q:Poly α) : Poly α := P.flatMap (fun z => shift z.1 z.2 Q)
def comm (P Q:Poly α) : Poly α := mul P Q ++ neg (mul Q P)

def sumEval {M:Type*} [AddCommGroup M] (f:List α→M) : Poly α → M
  | [] => 0
  | (c,w)::P => c • f w + sumEval f P

@[simp] theorem sumEval_append {M:Type*} [AddCommGroup M] (f:List α→M) (P Q:Poly α) :
    sumEval f (P++Q)=sumEval f P+sumEval f Q := by
  induction P with
  | nil => simp [sumEval]
  | cons z P ih => rcases z with ⟨c,w⟩; simp only [List.cons_append,sumEval,ih]; abel

@[simp] theorem sumEval_neg {M:Type*} [AddCommGroup M] (f:List α→M) (P:Poly α) :
    sumEval f (neg P) = -sumEval f P := by
  induction P with
  | nil => simp [neg,sumEval]
  | cons z P ih =>
    rcases z with ⟨c,w⟩
    change (-c) • f w+sumEval f (neg P) = -(c • f w+sumEval f P)
    rw [ih,neg_smul]
    abel

def NonemptyWords (P:Poly α) : Prop := ∀ z∈P,z.2≠[]

theorem nonempty_neg (P:Poly α) (h:NonemptyWords P) : NonemptyWords (neg P) := by
  intro z hz
  obtain ⟨w,hw,rfl⟩ := List.mem_map.mp hz
  exact h w hw

theorem nonempty_mul (P Q:Poly α) (h:NonemptyWords Q) : NonemptyWords (mul P Q) := by
  intro z hz
  obtain ⟨a,ha,hz⟩ := List.mem_flatMap.mp hz
  obtain ⟨b,hb,rfl⟩ := List.mem_map.mp hz
  intro hn
  have hb0 : b.2=[] := (List.append_eq_nil_iff.mp hn).2
  exact h b hb hb0

theorem nonempty_comm (P Q:Poly α) (hP:NonemptyWords P) (hQ:NonemptyWords Q) :
    NonemptyWords (comm P Q) := by
  intro z hz
  rcases List.mem_append.mp hz with h | h
  · exact nonempty_mul P Q hQ z h
  · exact nonempty_neg _ (nonempty_mul Q P hP) z h

end Poly

namespace LieWord

def expand {α:Type*} : LieWord α → Poly α
  | .atom a => [(1,[a])]
  | .comm a b => Poly.comm (expand a) (expand b)

theorem expansion_nonempty {α:Type*} (t:LieWord α) : Poly.NonemptyWords (expand t) := by
  induction t with
  | atom a => intro z hz; simp only [expand,List.mem_singleton] at hz; subst z; simp
  | comm a b ha hb => exact Poly.nonempty_comm _ _ ha hb

end LieWord

section Lie
variable {α L:Type*} [LieRing L] (s:α→L)

/-- The associative adjoint-word action; the empty word is the identity operator. -/
def wordAction : List α → L → L
  | [],z => z
  | a::w,z => ⁅s a,wordAction w z⁆

theorem wordAction_zero (w:List α) : wordAction s w 0=0 := by
  induction w with
  | nil => rfl
  | cons a w ih => simp only [wordAction,ih,lie_zero]

theorem wordAction_add (w:List α) (u v:L) :
    wordAction s w (u+v)=wordAction s w u+wordAction s w v := by
  induction w with
  | nil => rfl
  | cons a w ih => simp only [wordAction,ih,lie_add]

theorem wordAction_zsmul (w:List α) (c:Int) (u:L) :
    wordAction s w (c • u)=c • wordAction s w u := by
  induction w with
  | nil => rfl
  | cons a w ih => simp only [wordAction,ih,lie_zsmul]

theorem wordAction_append (w v:List α) (z:L) :
    wordAction s (w++v) z=wordAction s w (wordAction s v z) := by
  induction w with
  | nil => rfl
  | cons a w ih => simp only [List.cons_append,wordAction,ih]

/-- Right-normed Dynkin word, with zero assigned to the empty word. -/
def dynkinWord : List α → L
  | [] => 0
  | [a] => s a
  | a::b::w => ⁅s a,dynkinWord (b::w)⁆

theorem dynkinWord_append (w v:List α) (hv:v≠[]) :
    dynkinWord s (w++v)=wordAction s w (dynkinWord s v) := by
  induction w with
  | nil => rfl
  | cons a w ih =>
    have hne : w++v≠[] := by intro h; exact hv (List.append_eq_nil_iff.mp h).2
    cases hrest:w++v with
    | nil => exact (hne hrest).elim
    | cons b rest =>
      simp only [List.cons_append, hrest, dynkinWord, wordAction]
      exact congrArg (fun z:L => ⁅s a,z⁆) (hrest ▸ ih)

def polyAction (P:Poly α) (z:L) : L := Poly.sumEval (fun w => wordAction s w z) P
def dynkin (P:Poly α) : L := Poly.sumEval (dynkinWord s) P

theorem polyAction_zero (P:Poly α) : polyAction s P 0=0 := by
  induction P with
  | nil => rfl
  | cons a P ih =>
    rcases a with ⟨c,w⟩
    change c • wordAction s w 0 + polyAction s P 0 = 0
    rw [wordAction_zero, smul_zero, ih, add_zero]

theorem polyAction_add (P:Poly α) (u v:L) :
    polyAction s P (u+v)=polyAction s P u+polyAction s P v := by
  induction P with
  | nil => simp [polyAction,Poly.sumEval]
  | cons a P ih =>
    rcases a with ⟨c,w⟩
    change c • wordAction s w (u+v)+polyAction s P (u+v) = _
    rw [wordAction_add,smul_add,ih]
    change _=(c • wordAction s w u+polyAction s P u)+(c • wordAction s w v+polyAction s P v)
    abel

theorem polyAction_zsmul (P:Poly α) (c:Int) (u:L) :
    polyAction s P (c • u)=c • polyAction s P u := by
  induction P with
  | nil => simp [polyAction,Poly.sumEval]
  | cons a P ih =>
    rcases a with ⟨d,w⟩
    change d • wordAction s w (c • u)+polyAction s P (c • u) =
      c • (d • wordAction s w u+polyAction s P u)
    rw [wordAction_zsmul,ih,smul_add,smul_smul,smul_smul,mul_comm d c]

theorem action_shift (c:Int) (w:List α) (P:Poly α) (z:L) :
    polyAction s (Poly.shift c w P) z=c • wordAction s w (polyAction s P z) := by
  induction P with
  | nil => simp [Poly.shift,polyAction,Poly.sumEval,wordAction_zero]
  | cons a P ih =>
    rcases a with ⟨d,v⟩
    change (c*d) • wordAction s (w++v) z+polyAction s (Poly.shift c w P) z =
      c • wordAction s w (d • wordAction s v z+polyAction s P z)
    rw [wordAction_append,ih,wordAction_add,wordAction_zsmul,smul_add,smul_smul]

theorem action_mul (P Q:Poly α) (z:L) :
    polyAction s (Poly.mul P Q) z=polyAction s P (polyAction s Q z) := by
  induction P with
  | nil => rfl
  | cons a P ih =>
    rcases a with ⟨c,w⟩
    change polyAction s (Poly.shift c w Q++Poly.mul P Q) z = _
    rw [polyAction,Poly.sumEval_append]
    change polyAction s (Poly.shift c w Q) z+polyAction s (Poly.mul P Q) z = _
    rw [action_shift,ih]
    rfl

theorem dynkin_shift (c:Int) (w:List α) (P:Poly α) (hP:Poly.NonemptyWords P) :
    dynkin s (Poly.shift c w P)=c • wordAction s w (dynkin s P) := by
  induction P with
  | nil => simp [dynkin,Poly.shift,Poly.sumEval,wordAction_zero]
  | cons a P ih =>
    rcases a with ⟨d,v⟩
    have hv : v≠[] := hP (d,v) (List.mem_cons_self ..)
    have ht : Poly.NonemptyWords P := fun z hz => hP z (List.mem_cons_of_mem _ hz)
    change (c*d) • dynkinWord s (w++v)+dynkin s (Poly.shift c w P) =
      c • wordAction s w (d • dynkinWord s v+dynkin s P)
    rw [dynkinWord_append s w v hv,ih ht,wordAction_add,wordAction_zsmul,smul_add,smul_smul]

theorem dynkin_mul (P Q:Poly α) (hQ:Poly.NonemptyWords Q) :
    dynkin s (Poly.mul P Q)=polyAction s P (dynkin s Q) := by
  induction P with
  | nil => rfl
  | cons a P ih =>
    rcases a with ⟨c,w⟩
    change dynkin s (Poly.shift c w Q++Poly.mul P Q) = _
    rw [dynkin,Poly.sumEval_append]
    change dynkin s (Poly.shift c w Q)+dynkin s (Poly.mul P Q)=_
    rw [dynkin_shift s c w Q hQ,ih]
    rfl

/-- Expansion into associative words acts by exactly the corresponding iterated inner derivation. -/
theorem action_expand (t:LieWord α) (z:L) :
    polyAction s (LieWord.expand t) z=⁅LieWord.eval s t,z⁆ := by
  induction t generalizing z with
  | atom a => simp [polyAction,LieWord.expand,Poly.sumEval,wordAction,LieWord.eval]
  | comm a b ha hb =>
    change Poly.sumEval (fun w => wordAction s w z)
      (Poly.mul (LieWord.expand a) (LieWord.expand b) ++
       Poly.neg (Poly.mul (LieWord.expand b) (LieWord.expand a))) = _
    rw [Poly.sumEval_append,Poly.sumEval_neg, ← sub_eq_add_neg]
    change polyAction s (Poly.mul (LieWord.expand a) (LieWord.expand b)) z-
      polyAction s (Poly.mul (LieWord.expand b) (LieWord.expand a)) z = _
    rw [action_mul,action_mul,ha,hb,ha,hb]
    exact (lie_lie (LieWord.eval s a) (LieWord.eval s b) z).symm

/-- Dynkin--Specht--Wever on individual homogeneous Lie words, over ANY Lie ring. -/
theorem dynkin_expand (t:LieWord α) :
    dynkin s (LieWord.expand t)=LieWord.degree t • LieWord.eval s t := by
  induction t with
  | atom a => simp [dynkin,LieWord.expand,Poly.sumEval,dynkinWord,LieWord.degree,LieWord.eval]
  | comm a b ha hb =>
    change Poly.sumEval (dynkinWord s)
      (Poly.mul (LieWord.expand a) (LieWord.expand b) ++
       Poly.neg (Poly.mul (LieWord.expand b) (LieWord.expand a))) = _
    rw [Poly.sumEval_append,Poly.sumEval_neg, ← sub_eq_add_neg]
    change dynkin s (Poly.mul (LieWord.expand a) (LieWord.expand b))-
      dynkin s (Poly.mul (LieWord.expand b) (LieWord.expand a)) = _
    rw [dynkin_mul s _ _ (LieWord.expansion_nonempty b),
      dynkin_mul s _ _ (LieWord.expansion_nonempty a),ha,hb,action_expand,action_expand]
    simp only [lie_nsmul,LieWord.degree,LieWord.eval,add_nsmul]
    have hsk : ⁅LieWord.eval s b,LieWord.eval s a⁆ = -⁅LieWord.eval s a,LieWord.eval s b⁆ := by
      exact (lie_skew (LieWord.eval s b) (LieWord.eval s a)).symm
    rw [hsk,smul_neg,sub_neg_eq_add,add_comm]

/-- Once multiplication by the homogeneous degree is injective, reconstruction detects equal evaluations.
The downstream BCH proof must still connect normalized associative coefficients and the primitive log. -/
theorem eval_eq_of_dynkin_eq (a b:LieWord α) (hdegree:LieWord.degree a=LieWord.degree b)
    (hinj:Function.Injective (fun z:L => LieWord.degree a • z))
    (h:dynkin s (LieWord.expand a)=dynkin s (LieWord.expand b)) :
    LieWord.eval s a=LieWord.eval s b := by
  apply hinj
  simpa only [dynkin_expand,← hdegree] using h

end Lie
end Kourovka.BCH
