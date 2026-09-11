import Bell.Assembly

/-!
# Appendix B: exact attained strengthened lower bound

Bob uses X and Z. The state coefficient is diag(a,b), and k = 3 b / (5 a).
This is the appendix's square-root expression, written as a quotient to avoid
unnecessary nested-radical identities. All positivity and normalization
hypotheses are proved for the explicit parameters below.
-/
noncomputable section
open scoped Bell.Entrywise BigOperators Matrix ComplexOrder
namespace Bell.Strengthened

abbrev q : ℝ := Real.sqrt 7813
abbrev a : ℝ := Real.sqrt ((q+1)/(2*q))
abbrev b : ℝ := Real.sqrt ((q-1)/(2*q))
abbrev k : ℝ := 3*b/(5*a)
abbrev z : ℝ := q/125
abbrev x : ℝ := 2*q*a*b/125

theorem q_sq : q^2=7813 := Real.sq_sqrt (by norm_num)
theorem q_pos : 0<q := Real.sqrt_pos.mpr (by norm_num)
theorem q_gt_one : 1<q := by nlinarith [q_sq,q_pos]
theorem a_pos : 0<a := Real.sqrt_pos.mpr (div_pos (by linarith [q_pos]) (by positivity))
theorem b_pos : 0<b := Real.sqrt_pos.mpr (div_pos (by linarith [q_gt_one]) (by positivity))
theorem a_sq : a^2=(q+1)/(2*q) := Real.sq_sqrt (by positivity)
theorem b_sq : b^2=(q-1)/(2*q) :=
  Real.sq_sqrt (div_nonneg (sub_nonneg.mpr q_gt_one.le) (by positivity))

theorem scaled_a_sq : 2*q*a^2=q+1 := by
  rw [a_sq]
  field_simp [q_pos.ne']
theorem scaled_b_sq : 2*q*b^2=q-1 := by
  rw [b_sq]
  field_simp [q_pos.ne']

theorem state_norm : a^2+b^2=1 := by
  rw [a_sq,b_sq]
  field_simp [q_pos.ne']
  <;> ring

theorem k_a : k*a=3*b/5 := by
  dsimp [k]
  field_simp [a_pos.ne']
  <;> ring

theorem k_sq_lt_one : k^2<1 := by
  have hab : b<a := by
    have hs : a^2-b^2=1/q := by
      rw [a_sq,b_sq]
      field_simp [q_pos.ne']
      <;> ring
    have hp : 0<1/q := by positivity
    nlinarith [sq_nonneg (a-b),a_pos,b_pos]
  have hk : 0≤k := by dsimp [k]; positivity
  have hlt : k<1 := by
    dsimp [k]
    apply (div_lt_one (by positivity : (0 : ℝ)<5*a)).mpr
    nlinarith [a_pos,b_pos]
  nlinarith

theorem q_product_sq : q^2*(a*b)^2=1953 := by
  calc
    _ = ((2*q*a^2)*(2*q*b^2))/4 := by ring
    _ = ((q+1)*(q-1))/4 := by rw [scaled_a_sq,scaled_b_sq]
    _ = 1953 := by nlinarith [q_sq]

theorem observable_norm : z^2+x^2=1 := by
  have hp := q_product_sq
  dsimp [x,z]
  nlinarith [q_sq,hp]

def coefficient (a b : ℝ) : Operator := !![(a : ℂ),0;0,(b : ℂ)]

def auxiliary (k : ℝ) : Fin 3 → Operator :=
  ![ !![((k^2/2 : ℝ) : ℂ),((k/2 : ℝ) : ℂ);((k/2 : ℝ) : ℂ),(1/2 : ℂ)],
     !![((k^2/2 : ℝ) : ℂ),((-k/2 : ℝ) : ℂ);((-k/2 : ℝ) : ℂ),(1/2 : ℂ)],
     !![((1-k^2 : ℝ) : ℂ),0;0,0] ]

def aliceEffect (z x k : ℝ) : Fin 3 → Fin 3 → Operator :=
  ![ ![polarEffect z x,polarEffect (-z) (-x),0],
     ![polarEffect (-z) x,polarEffect z (-x),0],auxiliary k ]

def bobEffect : Fin 2 → Fin 2 → Operator :=
  ![ ![polarEffect 0 1,polarEffect 0 (-1)],
     ![polarEffect 1 0,polarEffect (-1) 0] ]

theorem auxiliary_positive (k : ℝ) (hk : k^2≤1) (j : Fin 3) :
    (auxiliary k j).PosSemidef := by
  fin_cases j
  · let G : Operator := !![((k/2 : ℝ) : ℂ),1/2;((k/2 : ℝ) : ℂ),1/2]
    have he : G.conjTranspose*G=auxiliary k 0 := by
      ext i j
      fin_cases i <;> fin_cases j <;> apply Complex.ext <;>
        norm_num [G,auxiliary,Matrix.conjTranspose_apply,Matrix.mul_apply,Fin.sum_univ_succ] <;> ring
    rw [← he]
    exact gram_positive G
  · let G : Operator := !![((k/2 : ℝ) : ℂ),-1/2;((k/2 : ℝ) : ℂ),-1/2]
    have he : G.conjTranspose*G=auxiliary k 1 := by
      ext i j
      fin_cases i <;> fin_cases j <;> apply Complex.ext <;>
        norm_num [G,auxiliary,Matrix.conjTranspose_apply,Matrix.mul_apply,Fin.sum_univ_succ] <;> ring
    rw [← he]
    exact gram_positive G
  · have hp := posSemidef_real_smul (polarEffect_positive 1 0 (by norm_num))
        (sub_nonneg.mpr hk)
    convert hp using 1
    ext i j
    fin_cases i <;> fin_cases j <;> apply Complex.ext <;>
      norm_num [auxiliary,polarEffect] <;> ring

theorem alice_positive (z x k : ℝ) (ho : z^2+x^2=1) (hk : k^2≤1)
    (i j : Fin 3) : (aliceEffect z x k i j).PosSemidef := by
  fin_cases i <;> fin_cases j
  · exact polarEffect_positive _ _ ho
  · apply polarEffect_positive; nlinarith [ho]
  · exact Matrix.PosSemidef.zero
  · apply polarEffect_positive; nlinarith [ho]
  · apply polarEffect_positive; nlinarith [ho]
  · exact Matrix.PosSemidef.zero
  · exact auxiliary_positive _ hk 0
  · exact auxiliary_positive _ hk 1
  · exact auxiliary_positive _ hk 2

theorem alice_normalized (z x k : ℝ) (i : Fin 3) : ∑ j, aliceEffect z x k i j=1 := by
  fin_cases i <;> ext j l <;> fin_cases j <;> fin_cases l <;>
    apply Complex.ext <;> norm_num [aliceEffect,auxiliary,polarEffect,Fin.sum_univ_succ] <;> ring

theorem bob_positive (i j : Fin 2) : (bobEffect i j).PosSemidef := by
  fin_cases i <;> fin_cases j <;> apply polarEffect_positive <;> norm_num

theorem bob_normalized (i : Fin 2) : ∑ j, bobEffect i j=1 := by
  fin_cases i <;> ext j l <;> fin_cases j <;> fin_cases l <;>
    norm_num [bobEffect,polarEffect,Fin.sum_univ_succ]

theorem coefficient_normalized :
    Matrix.trace (coefficient a b * (coefficient a b).conjTranspose)=1 := by
  apply Complex.ext
  · simpa [coefficient,Matrix.conjTranspose_apply,Matrix.trace,Matrix.mul_apply,
      Fin.sum_univ_succ,pow_two] using state_norm
  · norm_num [coefficient,Matrix.conjTranspose_apply,Matrix.trace,Matrix.mul_apply,Fin.sum_univ_succ]

def strategy : Strategy separatorArchitecture where
  state := pureState (coefficient a b) coefficient_normalized
  alice i := ⟨aliceEffect z x k i,alice_positive z x k observable_norm k_sq_lt_one.le i,
    alice_normalized z x k i⟩
  bob i := ⟨bobEffect i,bob_positive i,bob_normalized i⟩

/-- Polynomial expansion valid before imposing any parameter relations. -/
set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
theorem parameter_score (a b z x k : ℝ) :
    bellScore (fun i j u v => born (pureDensity (coefficient a b))
      (aliceEffect z x k i u) (bobEffect j v)) =
      40*x*a*b+20*z*(a^2+b^2)+(3/10)*(k*a+b)^2+(4/5)*(1-k^2)*a^2 := by
  unfold bellScore correlation
  norm_num [aliceSign,bobSign,aliceEffect,bobEffect,auxiliary,polarEffect,
    pureDensity_born,localTrace_apply,coefficient,Matrix.trace,Matrix.mul_apply,
    Matrix.transpose_apply,Matrix.conjTranspose_apply,Fin.sum_univ_succ]
  <;> ring

theorem auxiliary_value :
    (3/10)*(k*a+b)^2+(4/5)*(1-k^2)*a^2=(16+4/q)/25 := by
  have hk : k^2*a^2=(3*b/5)^2 := by nlinarith [congrArg (fun t : ℝ => t^2) k_a]
  rw [k_a]
  have he : (3/10)*(3*b/5+b)^2+(4/5)*(1-k^2)*a^2=
      (4/5)*a^2+(12/25)*b^2 := by nlinarith [hk]
  rw [he,a_sq,b_sq]
  field_simp [q_pos.ne']
  <;> ring

theorem locking_value : 40*x*a*b+20*z*(a^2+b^2)=2500/q := by
  rw [state_norm]
  have hp := q_product_sq
  have hq := q_sq
  apply (eq_div_iff q_pos.ne').mpr
  dsimp [x,z]
  nlinarith [hp,hq]

/-- Appendix B's exact radical is attained by actual qubit measurements. -/
theorem value : bellScore strategy.behavior=strengthenedLower := by
  change bellScore (fun i j u v => born (pureDensity (coefficient a b))
    (aliceEffect z x k i u) (bobEffect j v)) = _
  rw [parameter_score,show 40*x*a*b+20*z*(a^2+b^2)+(3/10)*(k*a+b)^2+
      (4/5)*(1-k^2)*a^2=
      (40*x*a*b+20*z*(a^2+b^2))+((3/10)*(k*a+b)^2+(4/5)*(1-k^2)*a^2) by ring,
    locking_value,auxiliary_value]
  change 2500/q+(16+4/q)/25=(16+8*q)/25
  field_simp [q_pos.ne']
  <;> nlinarith [q_sq]

end Bell.Strengthened

namespace Bell

theorem strengthened_attainment : StrengthenedAttainment :=
  ⟨Strengthened.strategy.behavior,⟨Strengthened.strategy,rfl⟩,Strengthened.value⟩

/-- The main theorem and the separate strengthened physical-attainment claim. -/
theorem main_claims_with_strengthening : MainClaims ∧ StrengthenedAttainment :=
  ⟨main_claims,strengthened_attainment⟩

end Bell
