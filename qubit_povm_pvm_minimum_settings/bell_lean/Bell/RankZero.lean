import Bell.RankOne
import Bell.LocalSimulation
import Bell.Relabeling

/-!
# Rank-zero ray rigidity and its normalized metric table

This module proves the five-ray permutation/common-scale reduction algebraically,
and identifies the normalized metric table with the bounded-transport simulator.
Its hypotheses are explicit null, future-orientation, invertibility, and
normalization conditions. The differential-geometric construction of these data
from an arbitrary physical maximizing strategy is a separate obligation.

STATUS: uncompiled proof source.
-/
noncomputable section
open scoped BigOperators Matrix
namespace Bell.Lorentz

/-- The sign vector of the unique binary-versus-ternary circuit. -/
def circuitSign (i : Fin 5) : ℝ := if i.val < 2 then 1 else -1

theorem circuitSign_ne_zero (i : Fin 5) : circuitSign i ≠ 0 := by
  fin_cases i <;> simp [Matrix.cons_val, circuitSign]

theorem circuitSign_squared (i : Fin 5) : circuitSign i * circuitSign i = 1 := by
  fin_cases i <;> simp [Matrix.cons_val, circuitSign]

theorem signed_circuit : (∑ j, circuitSign j • ray j) = 0 := by
  funext i
  fin_cases i <;> simp [Matrix.cons_val, circuitSign, ray, Fin.sum_univ_succ]

theorem circuit_kernel_sign (μ : Fin 5 → ℝ) (h : ∑ j, μ j • ray j = 0) :
    ∃ t : ℝ, ∀ j, μ j = t * circuitSign j := by
  obtain ⟨t,ht⟩ := (circuit_kernel μ).mp h
  refine ⟨t, ?_⟩
  intro j
  rw [ht]
  fin_cases j <;> simp [Matrix.cons_val, circuitSign]

/-- The scalar coordinate of a base-line vector is retained; the zero vector
is allowed here and is excluded later by strict future orientation. -/
theorem baseLines_ray_multiple (x : V) (hx : BaseLines x) :
    ∃ j : Fin 5, ∃ t : ℝ, x = t • ray j := by
  rcases hx with h | h | h | h | h
  · refine ⟨0,x 0,?_⟩
    rcases h with ⟨h1,h2,h3⟩
    funext i
    fin_cases i <;> simp [ray,h1,h2,h3]
  · refine ⟨1,x 1,?_⟩
    rcases h with ⟨h0,h2,h3⟩
    funext i
    fin_cases i <;> simp [ray,h0,h2,h3]
  · refine ⟨2,x 2,?_⟩
    rcases h with ⟨h0,h1,h3⟩
    funext i
    fin_cases i <;> simp [ray,h0,h1,h3]
  · refine ⟨3,x 3,?_⟩
    rcases h with ⟨h0,h1,h2⟩
    funext i
    fin_cases i <;> simp [ray,h0,h1,h2]
  · refine ⟨4,x 0,?_⟩
    rcases h with ⟨h01,h2,h3⟩
    funext i
    fin_cases i <;> simp [ray,h01,h2,h3]

/-- `uᵀ g x`, the physically relevant future-orientation functional. -/
def timeFunctional (g : StrictParameters) : V →ₗ[ℝ] ℝ where
  toFun := fun x => (x 0 + x 1)/2 + (g.a+g.c)*x 2 + (g.b+g.d)*x 3
  map_add' := by intros; simp only [Pi.add_apply]; ring
  map_smul' := by intros; simp only [Pi.smul_apply,smul_eq_mul,RingHom.id_apply]; ring

theorem timeFunctional_unit (g : StrictParameters) : timeFunctional g unitVector = 1 := by
  simp [Matrix.cons_val, timeFunctional,unitVector]

theorem timeFunctional_ray_positive (g : StrictParameters) (j : Fin 5) :
    0 < timeFunctional g (ray j) := by
  have ha := g.a_pos; have hb := g.b_pos
  have hc := g.c_pos; have hd := g.d_pos
  have hac := g.ac_lt; have hbd := g.bd_lt
  fin_cases j <;> simp [Matrix.cons_val, timeFunctional,ray] <;> linarith

theorem null_base_future_multiple (g : StrictParameters) (x : V)
    (hnull : nullPolynomial g.a g.b g.c g.d x = 0)
    (hbase : phi x = 0) (hfuture : 0 < timeFunctional g x) :
    ∃ j : Fin 5, ∃ t : ℝ, 0 < t ∧ x = t • ray j := by
  obtain ⟨j,t,ht⟩ := baseLines_ray_multiple x
    (phi_zero_null_base g.a g.b g.c g.d x hbase hnull)
  refine ⟨j,t,?_,ht⟩
  rw [ht,map_smul,smul_eq_mul] at hfuture
  have hj := timeFunctional_ray_positive g j
  exact (mul_pos_iff_of_pos_right hj).mp hfuture

/-- An injective linear transformation cannot merge two coefficient rays. -/
theorem ray_assignment_injective (T : V ≃ₗ[ℝ] V)
    (σ : Fin 5 → Fin 5) (t : Fin 5 → ℝ)
    (ht : ∀ j, t j ≠ 0) (hT : ∀ j, T (ray j) = t j • ray (σ j)) :
    Function.Injective σ := by
  intro i j hij
  apply transformed_rays_projectively_distinct T i j
  refine ⟨t i / t j, div_ne_zero (ht i) (ht j), ?_⟩
  rw [hT i,hT j,hij,smul_smul,div_mul_cancel₀ _ (ht j)]

/-- Reindexing the transported signed circuit exposes its unique coefficient
relation. No equality of positive and negative support sizes is assumed. -/
theorem permuted_circuit_coefficients (T : V ≃ₗ[ℝ] V)
    (π : Equiv.Perm (Fin 5)) (t : Fin 5 → ℝ)
    (hT : ∀ j, T (ray j) = t j • ray (π j)) :
    ∃ c : ℝ, ∀ j, circuitSign j * t j = c * circuitSign (π j) := by
  have hc : (∑ j, (circuitSign j * t j) • ray (π j)) = 0 := by
    have h := congrArg T signed_circuit
    simpa only [map_sum,map_smul,map_zero,hT,smul_smul] using h
  let μ : Fin 5 → ℝ := fun i => circuitSign (π.symm i) * t (π.symm i)
  have hμ : (∑ i, μ i • ray i) = 0 := by
    calc
      (∑ i, μ i • ray i) = ∑ j, μ (π j) • ray (π j) :=
        (Equiv.sum_comp π (fun i => μ i • ray i)).symm
      _ = ∑ j, (circuitSign j * t j) • ray (π j) := by
        simp only [μ,Equiv.symm_apply_apply]
      _ = 0 := hc
  obtain ⟨c,hc⟩ := circuit_kernel_sign μ hμ
  refine ⟨c,?_⟩
  intro j
  simpa only [μ,Equiv.symm_apply_apply] using hc (π j)

/-- Three distinct indices cannot all be mapped to the binary pair. -/
theorem not_three_in_binary_pair (π : Equiv.Perm (Fin 5)) :
    ¬ ((π 2).val < 2 ∧ (π 3).val < 2 ∧ (π 4).val < 2) := by
  rintro ⟨h2,h3,h4⟩
  have h23 : (π 2).val ≠ (π 3).val := by
    intro h
    have hi := π.injective (Fin.ext h)
    exact (by decide : (2 : Fin 5) ≠ 3) hi
  have h24 : (π 2).val ≠ (π 4).val := by
    intro h
    have hi := π.injective (Fin.ext h)
    exact (by decide : (2 : Fin 5) ≠ 4) hi
  have h34 : (π 3).val ≠ (π 4).val := by
    intro h
    have hi := π.injective (Fin.ext h)
    exact (by decide : (3 : Fin 5) ≠ 4) hi
  omega

/-- Positive scales and the 2-versus-3 circuit rule out sign reversal. -/
theorem circuit_scale_positive (π : Equiv.Perm (Fin 5)) (t : Fin 5 → ℝ)
    (ht : ∀ j, 0 < t j) (c : ℝ)
    (hc : ∀ j, circuitSign j * t j = c * circuitSign (π j)) : 0 < c := by
  have hc0 : c ≠ 0 := by
    intro hz
    have h := hc 0
    simp [Matrix.cons_val, circuitSign,hz] at h
    exact (ne_of_gt (ht 0)) h
  by_contra hn
  have hneg : c < 0 := lt_of_le_of_ne (le_of_not_gt hn) hc0
  have hmap : ∀ j : Fin 5, 2 ≤ j.val → (π j).val < 2 := by
    intro j hj
    by_contra hpj
    have h := hc j
    have htn := ht j
    simp [circuitSign,not_lt.mpr hj,hpj] at h
    linarith
  exact not_three_in_binary_pair π
    ⟨hmap 2 (by decide),hmap 3 (by decide),hmap 4 (by decide)⟩

theorem circuit_partition_and_scale (π : Equiv.Perm (Fin 5)) (t : Fin 5 → ℝ)
    (ht : ∀ j, 0 < t j) (c : ℝ) (hcpos : 0 < c)
    (hc : ∀ j, circuitSign j * t j = c * circuitSign (π j)) :
    (∀ j, (π j).val < 2 ↔ j.val < 2) ∧ (∀ j, t j = c) := by
  have hall : ∀ j, ((π j).val < 2 ↔ j.val < 2) ∧ t j = c := by
    intro j
    have h := hc j
    have htp := ht j
    by_cases hj : j.val < 2 <;> by_cases hpj : (π j).val < 2
    all_goals simp [circuitSign,hj,hpj] at h ⊢
    all_goals linarith
  exact ⟨fun j => (hall j).1,fun j => (hall j).2⟩

/-- A partition-preserving ray permutation sends the binary sum to itself. -/
theorem binary_sum_preserved (π : Equiv.Perm (Fin 5))
    (hπ : ∀ j, (π j).val < 2 ↔ j.val < 2) :
    ray (π 0) + ray (π 1) = unitVector := by
  have h0 : (π 0).val < 2 := (hπ 0).mpr (by decide)
  have h1 : (π 1).val < 2 := (hπ 1).mpr (by decide)
  have hne : (π 0).val ≠ (π 1).val := by
    intro h
    have he := π.injective (Fin.ext h)
    norm_num at he
  have alternatives :
      (π 0 = 0 ∧ π 1 = 1) ∨ (π 0 = 1 ∧ π 1 = 0) := by
    have ha : (π 0).val = 0 ∨ (π 0).val = 1 := by omega
    rcases ha with ha | ha
    · exact Or.inl ⟨Fin.ext ha,Fin.ext (by omega)⟩
    · exact Or.inr ⟨Fin.ext ha,Fin.ext (by omega)⟩
  rcases alternatives with ⟨ha,hb⟩ | ⟨ha,hb⟩
  · simpa [ha,hb] using binary_circuit
  · simpa [ha,hb,add_comm] using binary_circuit

/-- All positive scales are equal, and normalization fixes that scale to one.
This is the complete algebraic rank-zero ray reduction, with the permutation
retained rather than silently identifying differently labelled tables. -/
theorem rank_zero_normalized_rigidity (g : StrictParameters) (T : V ≃ₗ[ℝ] V)
    (hnull : ∀ j, nullPolynomial g.a g.b g.c g.d (T (ray j)) = 0)
    (hbase : ∀ j, phi (T (ray j)) = 0)
    (hfuture : ∀ j, 0 < timeFunctional g (T (ray j)))
    (hnormal : timeFunctional g (T unitVector) = 1) :
    ∃ π : Equiv.Perm (Fin 5),
      (∀ j, (π j).val < 2 ↔ j.val < 2) ∧ (∀ j, T (ray j) = ray (π j)) := by
  classical
  have hex : ∀ j : Fin 5, ∃ i : Fin 5, ∃ t : ℝ,
      0 < t ∧ T (ray j) = t • ray i := by
    intro j
    exact null_base_future_multiple g (T (ray j)) (hnull j) (hbase j) (hfuture j)
  choose σ t ht hT using hex
  have hinj := ray_assignment_injective T σ t (fun j => ne_of_gt (ht j)) hT
  let π : Equiv.Perm (Fin 5) := Equiv.ofBijective σ
    ⟨hinj,Finite.surjective_of_injective hinj⟩
  have hTπ : ∀ j, T (ray j) = t j • ray (π j) := hT
  obtain ⟨c,hc⟩ := permuted_circuit_coefficients T π t hTπ
  have hcpos := circuit_scale_positive π t ht c hc
  obtain ⟨hpartition,hscale⟩ := circuit_partition_and_scale π t ht c hcpos hc
  have hunit : T unitVector = c • unitVector := by
    conv_lhs => rw [← binary_circuit]
    rw [map_add,hTπ 0,hTπ 1,hscale 0,hscale 1,← smul_add,
      binary_sum_preserved π hpartition]
  have hc1 : c = 1 := by
    rw [hunit,map_smul,smul_eq_mul,timeFunctional_unit,mul_one] at hnormal
    exact hnormal
  refine ⟨π,hpartition,?_⟩
  intro j
  simpa only [hscale j,hc1,one_smul] using hTπ j

/-! ## Exact metric-table identification with the transport construction -/

def mixedA (g : StrictParameters) : Transport.Vec := ![g.a,g.b,1/2-g.a-g.b]
def mixedB (g : StrictParameters) : Transport.Vec := ![g.c,g.d,1/2-g.c-g.d]
def capacity (g : StrictParameters) : Transport.Mat :=
  !![0,g.a+g.b+g.c+g.d-1/2,1/2-g.b-g.d;
     g.a+g.b+g.c+g.d-1/2,0,1/2-g.a-g.c;
     1/2-g.b-g.d,1/2-g.a-g.c,0]

def effectRay (x : Fin 2) (a : Fin 3) : V :=
  if x = 0 then ![ray 0,ray 1,0] a else ![ray 2,ray 3,ray 4] a

def metricTable (g : StrictParameters) : Behavior binaryTernaryArchitecture :=
  fun x y a b => dotProduct (effectRay x a)
    (metric g.a g.b g.c g.d *ᵥ effectRay y b)

theorem metricTable_eq_rankZeroTable (g : StrictParameters) :
    metricTable g = rankZeroTable (mixedA g) (mixedB g) (capacity g) := by
  funext x y a b
  fin_cases x <;> fin_cases y <;> fin_cases a <;> fin_cases b <;>
    simp [Matrix.cons_val, metricTable,rankZeroTable,effectRay,mixedA,mixedB,capacity,
      metric,ray,dotProduct,Matrix.mulVec,Fin.sum_univ_succ] <;> ring

theorem metricTable_mem_convexPVM (g : StrictParameters) :
    metricTable g ∈ convexPVM binaryTernaryArchitecture := by
  rw [metricTable_eq_rankZeroTable]
  apply rankZeroTable_mem
  · intro i
    have ha := g.a_pos; have hb := g.b_pos; have hab := g.ab_lt
    fin_cases i <;> simp [Matrix.cons_val, mixedA] <;> linarith
  · intro i
    have hc := g.c_pos; have hd := g.d_pos; have hcd := g.cd_lt
    fin_cases i <;> simp [Matrix.cons_val, mixedB] <;> linarith
  · intro i j
    have he := g.e_pos; have hac := g.ac_lt; have hbd := g.bd_lt
    fin_cases i <;> fin_cases j <;> simp [Matrix.cons_val, capacity] <;> linarith
  · intro i j
    fin_cases i <;> fin_cases j <;> rfl
  · intro i
    fin_cases i <;> rfl
  · intro i
    fin_cases i <;> simp [Matrix.cons_val, capacity,mixedA,mixedB,Fin.sum_univ_succ] <;> ring
  · simp [Matrix.cons_val, mixedA,Fin.sum_univ_succ]
  · simp [Matrix.cons_val, mixedB,Fin.sum_univ_succ]

end Bell.Lorentz
