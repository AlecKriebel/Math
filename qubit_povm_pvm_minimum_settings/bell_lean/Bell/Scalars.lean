import Mathlib

/-!
# Exact scalar analysis of the separator (paper §3 and Appendices A/B)

The quantum-to-scalar upper-bound reduction is NOT assumed as an axiom here.
`global_upper_from_deficits` states its scalar hypotheses explicitly.
-/

noncomputable section
namespace Bell

abbrev sqrtTwo : ℝ := Real.sqrt 2

def lower : ℝ := 20 * sqrtTwo + 16 / 25

def upper : ℝ := 20 * sqrtTwo + 3 / 5 + (4 + 3 * sqrtTwo) / 250

def strengthenedLower : ℝ := (16 + 8 * Real.sqrt 7813) / 25

theorem sqrtTwo_sq : sqrtTwo ^ 2 = 2 := Real.sq_sqrt (by norm_num)

theorem sqrtTwo_pos : 0 < sqrtTwo := Real.sqrt_pos.2 (by norm_num)

theorem sqrtTwo_lt_two : sqrtTwo < 2 := by
  have hs := sqrtTwo_sq
  have hp := sqrtTwo_pos
  nlinarith

theorem gap_identity : lower - upper = 3 * (2 - sqrtTwo) / 250 := by
  unfold lower upper
  ring

theorem strict_gap : upper < lower := by
  have h : 0 < 2 - sqrtTwo := sub_pos.mpr sqrtTwo_lt_two
  rw [← sub_pos]
  rw [gap_identity]
  positivity

/-- Elementary ordered-field helper, avoiding an opaque square-root comparison. -/
theorem le_of_square_le (a b : ℝ) (hb : 0 ≤ b) (hs : a ^ 2 ≤ b ^ 2) : a ≤ b := by
  by_contra h
  have hlt : b < a := lt_of_not_ge h
  have hp : 0 < (a - b) * (a + b) :=
    mul_pos (by linarith) (by linarith)
  nlinarith

theorem sqrt_deficit_one_identity (u : ℝ) :
    (1 - u ^ 2 / 2) ^ 2 - (1 - u ^ 2) = u ^ 4 / 4 := by ring

theorem sqrt_deficit_four_identity (u : ℝ) :
    (2 - u ^ 2 / 4) ^ 2 - (4 - u ^ 2) = u ^ 4 / 16 := by ring

theorem sqrt_deficit_one (u : ℝ) (hu0 : 0 ≤ u) (hu1 : u ≤ 1) :
    Real.sqrt (1 - u ^ 2) ≤ 1 - u ^ 2 / 2 := by
  have hu2 : u ^ 2 ≤ 1 := by
    nlinarith [mul_nonneg hu0 (sub_nonneg.mpr hu1)]
  have harg : 0 ≤ 1 - u ^ 2 := by linarith
  apply le_of_square_le
  · linarith
  · rw [Real.sq_sqrt harg]
    have h := sqrt_deficit_one_identity u
    nlinarith [sq_nonneg (u ^ 2)]

theorem sqrt_deficit_four (u : ℝ) (hu0 : 0 ≤ u) (hu1 : u ≤ 1) :
    Real.sqrt (4 - u ^ 2) ≤ 2 - u ^ 2 / 4 := by
  have hu2 : u ^ 2 ≤ 1 := by
    nlinarith [mul_nonneg hu0 (sub_nonneg.mpr hu1)]
  have harg : 0 ≤ 4 - u ^ 2 := by linarith
  apply le_of_square_le
  · linarith
  · rw [Real.sq_sqrt harg]
    have h := sqrt_deficit_four_identity u
    nlinarith [sq_nonneg (u ^ 2)]

def discriminant (η x y r : ℝ) : ℝ :=
  (-1 + η * (3 * x - 4 * y)) ^ 2 + 24 * (1 - η ^ 2) * (1 - r)

def robustH (x y : ℝ) : ℝ := 8 - 3 * x - 4 * y

def robustCertificate (η x y r q : ℝ) : ℝ :=
  2 * η * (η * (8 * (1 - y) * (4 - 3 * x) + 12 * (1 - r)) +
    (q - 1) * robustH x y + 8 * (1 - y))

/-- An identity for arbitrary real inputs, not a sampled instance. -/
theorem robust_square_identity (η x y r q : ℝ) :
    (q + η * robustH x y) ^ 2 - discriminant η x y r =
      (q ^ 2 - (25 - 24 * r)) + robustCertificate η x y r q := by
  unfold robustH discriminant robustCertificate
  ring

theorem robust_certificate_nonnegative (η x y r q : ℝ)
    (hη : 0 ≤ η) (hx : x ≤ 1) (hy : y ≤ 1) (hr : r ≤ 1) (hq : 1 ≤ q) :
    0 ≤ robustCertificate η x y r q := by
  have h1 : 0 ≤ 1 - y := by linarith
  have h2 : 0 ≤ 4 - 3 * x := by linarith
  have h3 : 0 ≤ 1 - r := by linarith
  have h4 : 0 ≤ q - 1 := by linarith
  have hH : 0 ≤ robustH x y := by unfold robustH; linarith
  unfold robustCertificate
  positivity

def pairScore (η x y r : ℝ) : ℝ :=
  (7 + η * (3 * x + 4 * y) + Real.sqrt (discriminant η x y r)) / 20

/-- Appendix A's robust pair bound holds on the whole larger box. -/
theorem robust_pair_bound (η x y r u : ℝ)
    (hη0 : 0 ≤ η) (hη1 : η ≤ 1)
    (hx : x ≤ 1) (hy : y ≤ 1) (hr1 : r ≤ 1)
    (hu : 0 ≤ u) (hru : -u ≤ r) :
    pairScore η x y r ≤ 3 / 5 + 2 / 5 * (η + u) := by
  let q : ℝ := Real.sqrt (25 - 24 * r)
  have hrad : 0 ≤ 25 - 24 * r := by linarith
  have hq0 : 0 ≤ q := Real.sqrt_nonneg _
  have hq2 : q ^ 2 = 25 - 24 * r := Real.sq_sqrt hrad
  have hq1 : 1 ≤ q := by nlinarith
  have hη2 : 0 ≤ 1 - η ^ 2 := by
    nlinarith [mul_nonneg hη0 (sub_nonneg.mpr hη1)]
  have hr : 0 ≤ 1 - r := by linarith
  have hd : 0 ≤ discriminant η x y r := by unfold discriminant; positivity
  have hH : 1 ≤ robustH x y := by unfold robustH; linarith
  have hH0 : 0 ≤ robustH x y := le_trans (by norm_num) hH
  have hright : 0 ≤ q + η * robustH x y :=
    add_nonneg hq0 (mul_nonneg hη0 hH0)
  have hcert := robust_certificate_nonnegative η x y r q hη0 hx hy hr1 hq1
  have hid := robust_square_identity η x y r q
  have hsquare : (Real.sqrt (discriminant η x y r)) ^ 2 ≤
      (q + η * robustH x y) ^ 2 := by
    rw [Real.sq_sqrt hd]
    nlinarith [hid, hq2, hcert]
  have hs := le_of_square_le _ _ hright hsquare
  have huaux : 0 ≤ 8 * u * (7 + 8 * u) := by positivity
  have hqbound : q ≤ 5 + 8 * u := by
    apply le_of_square_le
    · positivity
    · nlinarith [hq2, huaux]
  unfold pairScore
  unfold robustH at hs
  nlinarith [hs, hqbound]

/-- The completion of the square used in §3.2. -/
theorem complete_square (κ t : ℝ) : κ * t - 10 * t ^ 2 ≤ κ ^ 2 / 40 := by
  nlinarith [sq_nonneg (κ - 20 * t)]

/-- All hypotheses are scalar. The end-to-end PVM-bound source uses the separate
exact operator SOS certificate; it does not assume every physical PVM strategy
supplies these scalar deficits. This estimate is retained as auxiliary algebra. -/
theorem global_upper_from_deficits (S T η u δ : ℝ)
    (hδ : 0 ≤ δ) (hS : S = 2 * sqrtTwo - δ)
    (hη : η ^ 2 ≤ sqrtTwo * δ) (hu : u ^ 2 ≤ 2 * sqrtTwo * δ)
    (hT : T ≤ 3 / 5 + 2 / 5 * (η + u)) :
    10 * S + T ≤ upper := by
  let a : ℝ := Real.sqrt sqrtTwo
  let t : ℝ := Real.sqrt δ
  let κ : ℝ := 2 / 5 * (1 + sqrtTwo) * a
  have hr0 : 0 ≤ sqrtTwo := le_of_lt sqrtTwo_pos
  have hr2 := sqrtTwo_sq
  have ha0 : 0 ≤ a := Real.sqrt_nonneg _
  have ha2 : a ^ 2 = sqrtTwo := Real.sq_sqrt hr0
  have ht0 : 0 ≤ t := Real.sqrt_nonneg _
  have ht2 : t ^ 2 = δ := Real.sq_sqrt hδ
  have hηbound : η ≤ a * t := by
    apply le_of_square_le _ _ (mul_nonneg ha0 ht0)
    calc
      η ^ 2 ≤ sqrtTwo * δ := hη
      _ = (a * t) ^ 2 := by rw [mul_pow, ha2, ht2]
  have hubound : u ≤ sqrtTwo * a * t := by
    apply le_of_square_le _ _ (mul_nonneg (mul_nonneg hr0 ha0) ht0)
    calc
      u ^ 2 ≤ 2 * sqrtTwo * δ := hu
      _ = (sqrtTwo * a * t) ^ 2 := by rw [mul_pow, mul_pow, hr2, ha2, ht2]
  have hTbound : T ≤ 3 / 5 + κ * t := by
    dsimp [κ]
    nlinarith [hT, hηbound, hubound]
  have hk2 : κ ^ 2 = (16 + 12 * sqrtTwo) / 25 := by
    dsimp [κ]
    calc
      (2 / 5 * (1 + sqrtTwo) * a) ^ 2 =
        (4 / 25) * (1 + 2 * sqrtTwo + sqrtTwo ^ 2) * a ^ 2 := by ring
      _ = (16 + 12 * sqrtTwo) / 25 := by rw [ha2, hr2]; nlinarith [hr2]
  have hsq := complete_square κ t
  unfold upper
  rw [hS]
  nlinarith [hsq, hTbound, ht2, hk2]

/-- The strengthened radical is strictly larger even than the simple lower bound. -/
theorem strengthened_gt_lower : lower < strengthenedLower := by
  let q : ℝ := Real.sqrt 7813
  have hq0 : 0 ≤ q := Real.sqrt_nonneg _
  have hq2 : q ^ 2 = 7813 := Real.sq_sqrt (by norm_num)
  have hr0 : 0 ≤ sqrtTwo := le_of_lt sqrtTwo_pos
  have hr2 := sqrtTwo_sq
  have h : 500 * sqrtTwo < 8 * q := by
    by_contra hnot
    have hle : 8 * q ≤ 500 * sqrtTwo := le_of_not_gt hnot
    have hp : 0 ≤ (500 * sqrtTwo - 8 * q) * (500 * sqrtTwo + 8 * q) :=
      mul_nonneg (by linarith) (by positivity)
    nlinarith [hp, hq2, hr2]
  unfold lower strengthenedLower
  dsimp [q] at h
  linarith

theorem strengthened_gt_upper : upper < strengthenedLower :=
  lt_trans strict_gap strengthened_gt_lower

/-- Appendix B's one-parameter family upper bound, by a square certificate,
not by trusting a differentiation or numerical optimization routine. -/
theorem strengthened_family_bound (η : ℝ) (hη0 : 0 ≤ η) (hη1 : η ≤ 1) :
    20 * Real.sqrt (2 - η ^ 2) + (16 + 4 * η) / 25 ≤ strengthenedLower := by
  let t : ℝ := Real.sqrt (2 - η ^ 2)
  let q : ℝ := Real.sqrt 7813
  have ht0 : 0 ≤ t := Real.sqrt_nonneg _
  have harg : 0 ≤ 2 - η ^ 2 := by
    nlinarith [mul_nonneg hη0 (sub_nonneg.mpr hη1)]
  have ht2 : t ^ 2 = 2 - η ^ 2 := Real.sq_sqrt harg
  have hq0 : 0 ≤ q := Real.sqrt_nonneg _
  have hq2 : q ^ 2 = 7813 := Real.sq_sqrt (by norm_num)
  have hsq : (500 * t + 4 * η) ^ 2 ≤ (8 * q) ^ 2 := by
    nlinarith [sq_nonneg (4 * t - 500 * η), ht2, hq2]
  have h := le_of_square_le _ _ (mul_nonneg (by norm_num) hq0) hsq
  unfold strengthenedLower
  dsimp [t, q] at h
  linarith

end Bell
