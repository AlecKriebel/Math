import Bell.Witness
import Bell.Transportation

/-!
# Physical realization of the bounded-transport simulator (paper §9.3 / H)

Every deterministic branch is an actual qubit PVM strategy (identity and zero
projectors, on the explicit Bell state). The final membership is in Mathlib's
convex hull of the physical PVM strategy image. It is not membership in a newly
invented "local" set standing in for that image.

The geometric reduction of arbitrary rank-zero incidence points to this table
is NOT proved here.
-/

noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace Bell

/-- Deterministic output labels are valid projective measurements, with all
unused labels represented by the zero projector. -/
def deterministicPVM (n : ℕ) (label : Fin n) : PVM n where
  effect := fun a => if a=label then 1 else 0
  positive := by
    intro a
    by_cases h : a=label
    · simpa [h] using (Matrix.PosSemidef.one : (1 : Operator).PosSemidef)
    · simpa [h] using (Matrix.PosSemidef.zero : (0 : Operator).PosSemidef)
  normalized := by simp
  idempotent := by
    intro a
    by_cases h : a=label <;> simp [h]
  orthogonal := by
    intro a b hab
    by_cases ha : a=label
    · have hb : b≠label := by
        intro hb
        exact hab (ha.trans hb.symm)
      simp [ha,hb]
    · simp [ha]

def deterministicStrategy (A : Architecture)
    (α : (x : Fin A.aliceInputs) → Fin (A.aliceOutputs x))
    (β : (y : Fin A.bobInputs) → Fin (A.bobOutputs y)) : ProjectiveStrategy A where
  state := phiState
  alice := fun x => deterministicPVM _ (α x)
  bob := fun y => deterministicPVM _ (β y)

def deterministicTable (A : Architecture)
    (α : (x : Fin A.aliceInputs) → Fin (A.aliceOutputs x))
    (β : (y : Fin A.bobInputs) → Fin (A.bobOutputs y)) : Behavior A :=
  fun x y a b => if a=α x ∧ b=β y then 1 else 0

theorem deterministic_behavior (A : Architecture)
    (α : (x : Fin A.aliceInputs) → Fin (A.aliceOutputs x))
    (β : (y : Fin A.bobInputs) → Fin (A.bobOutputs y)) :
    (deterministicStrategy A α β).toStrategy.behavior=deterministicTable A α β := by
  funext x y a b
  by_cases ha : a=α x <;> by_cases hb : b=β y <;>
    norm_num [deterministicStrategy,deterministicPVM,ProjectiveStrategy.toStrategy,
      Strategy.behavior,deterministicTable,phiState,born,phi_trace_tensor,
      Matrix.one_apply,ha,hb]

theorem deterministic_mem_rawPVM (A : Architecture)
    (α : (x : Fin A.aliceInputs) → Fin (A.aliceOutputs x))
    (β : (y : Fin A.bobInputs) → Fin (A.bobOutputs y)) :
    deterministicTable A α β ∈ rawPVM A :=
  ⟨deterministicStrategy A α β,deterministic_behavior A α β⟩

/-- Every finite local common-randomness table has a fixed-qubit PVM realization
with the same declared input/output alphabets. -/
theorem finite_local_mixture_mem_convexPVM (A : Architecture)
    {ι : Type*} [Fintype ι] (weight : ι → ℝ)
    (α : ι → (x : Fin A.aliceInputs) → Fin (A.aliceOutputs x))
    (β : ι → (y : Fin A.bobInputs) → Fin (A.bobOutputs y))
    (hw : ∀ i, 0≤weight i) (hsum : ∑ i, weight i=1) :
    (∑ i, weight i • deterministicTable A (α i) (β i)) ∈ convexPVM A := by
  change (∑ i, weight i • deterministicTable A (α i) (β i)) ∈
    convexHull ℝ (rawPVM A)
  apply (convex_convexHull ℝ (rawPVM A)).sum_mem
  · intro i _
    exact hw i
  · exact hsum
  · intro i _
    exact subset_convexHull ℝ (rawPVM A) (deterministic_mem_rawPVM A (α i) (β i))

/-- A common-label encoding: input 0 is binary with a zero label 2; input 1
is ternary. Both parties have the same two declared inputs. -/
abbrev binaryTernaryArchitecture : Architecture where
  aliceInputs := 2
  bobInputs := 2
  aliceOutputs := fun _ => 3
  bobOutputs := fun _ => 3

abbrev TransportBranch := Fin 2 × (Fin 3 × Fin 3)

def branchAlice (k : TransportBranch) : Fin 2 → Fin 3 :=
  if k.1=0 then ![0,k.2.1] else ![1,k.2.1]

def branchBob (k : TransportBranch) : Fin 2 → Fin 3 :=
  if k.1=0 then ![1,k.2.2] else ![0,k.2.2]

def branchWeight {a b : Transport.Vec} {C : Transport.Mat}
    (q : Transport.Certificate a b C) (k : TransportBranch) : ℝ :=
  if k.1=0 then q.flow k.2.1 k.2.2 else C k.2.1 k.2.2-q.flow k.2.1 k.2.2

def transportMixture {a b : Transport.Vec} {C : Transport.Mat}
    (q : Transport.Certificate a b C) : Behavior binaryTernaryArchitecture :=
  ∑ k : TransportBranch, branchWeight q k •
    deterministicTable binaryTernaryArchitecture (branchAlice k) (branchBob k)

/-- The four input blocks after rank-zero normalization P=g. -/
def rankZeroTable (a b : Transport.Vec) (C : Transport.Mat) :
    Behavior binaryTernaryArchitecture :=
  fun x y i j =>
    if x=0 then
      if y=0 then
        if (i=0 ∧ j=1) ∨ (i=1 ∧ j=0) then 1/2 else 0
      else if i=0 then a j else if i=1 then b j else 0
    else if y=0 then
      if j=0 then a i else if j=1 then b i else 0
    else C i j

theorem transportMixture_mem {a b : Transport.Vec} {C : Transport.Mat}
    (q : Transport.Certificate a b C)
    (hrows : ∀ i, ∑ j, C i j=a i+b i)
    (hsa : ∑ i, a i=1/2) (hsb : ∑ i, b i=1/2) :
    transportMixture q ∈ convexPVM binaryTernaryArchitecture := by
  apply finite_local_mixture_mem_convexPVM
  · intro k
    by_cases hk : k.1=0
    · simpa [branchWeight,hk] using q.nonnegative k.2.1 k.2.2
    · simpa [branchWeight,hk] using q.complement_nonnegative k.2.1 k.2.2
  · simpa [branchWeight,Fintype.sum_prod_type,Fin.sum_univ_two] using
      q.total_branch_mass hrows hsa hsb

set_option maxHeartbeats 2000000 in
/-- All 36 declared probabilities, including the zero binary label, are covered
by the same branch distribution. -/
theorem transportMixture_eq {a b : Transport.Vec} {C : Transport.Mat}
    (q : Transport.Certificate a b C)
    (hrows : ∀ i, ∑ j, C i j=a i+b i)
    (hcols : ∀ j, ∑ i, C i j=a j+b j)
    (hsa : ∑ i, a i=1/2) (hsb : ∑ i, b i=1/2) :
    transportMixture q=rankZeroTable a b C := by
  have htwo (h : 2 < 3) : (⟨2,h⟩ : Fin 3) = 2 := rfl
  have qr0 := q.row_sum 0
  have qr1 := q.row_sum 1
  have qr2 := q.row_sum 2
  have qc0 := q.column_sum 0
  have qc1 := q.column_sum 1
  have qc2 := q.column_sum 2
  have cr0 := q.complement_row hrows 0
  have cr1 := q.complement_row hrows 1
  have cr2 := q.complement_row hrows 2
  have cc0 := q.complement_column hcols 0
  have cc1 := q.complement_column hcols 1
  have cc2 := q.complement_column hcols 2
  have mass0 := q.mass_first hsb
  have mass1 := q.mass_second hrows hsa
  norm_num [Fin.sum_univ_succ] at qr0 qr1 qr2 qc0 qc1 qc2 cr0 cr1 cr2 cc0 cc1 cc2 mass0 mass1
  funext x y i j
  fin_cases x <;> fin_cases y <;> fin_cases i <;> fin_cases j <;>
    norm_num [transportMixture,rankZeroTable,branchWeight,branchAlice,branchBob,
      deterministicTable,Fintype.sum_prod_type,Fin.sum_univ_succ,
      Pi.smul_apply,smul_eq_mul] <;>
      norm_num only [Fin.ext_iff, Fin.coe_ofNat_eq_mod] <;>
      (try simp [htwo]) <;> linarith

/-- Physical PVM simulation from an arbitrary bounded-transport certificate. -/
theorem rankZeroTable_mem_of_transport {a b : Transport.Vec} {C : Transport.Mat}
    (q : Transport.Certificate a b C)
    (hrows : ∀ i, ∑ j, C i j=a i+b i)
    (hcols : ∀ j, ∑ i, C i j=a j+b j)
    (hsa : ∑ i, a i=1/2) (hsb : ∑ i, b i=1/2) :
    rankZeroTable a b C ∈ convexPVM binaryTernaryArchitecture := by
  rw [← transportMixture_eq q hrows hcols hsa hsb]
  exact transportMixture_mem q hrows hsa hsb

/-- The unconditional simulation theorem for every table satisfying Appendix H's
nonnegative symmetric-capacity hypotheses, including boundary capacities. -/
theorem rankZeroTable_mem (a b : Transport.Vec) (C : Transport.Mat)
    (ha : ∀ i, 0≤a i) (hb : ∀ i, 0≤b i)
    (hC : ∀ i j, 0≤C i j)
    (hsym : ∀ i j, C i j=C j i) (hdiag : ∀ i, C i i=0)
    (hbalance : ∀ i, ∑ j, C i j=a i+b i)
    (hsa : ∑ i, a i=1/2) (hsb : ∑ i, b i=1/2) :
    rankZeroTable a b C ∈ convexPVM binaryTernaryArchitecture := by
  obtain ⟨q⟩ := Transport.exists_transport a b C ha hb hC hsym hdiag hbalance hsa hsb
  have hcols : ∀ j, ∑ i, C i j=a j+b j := by
    intro j
    calc
      ∑ i, C i j = ∑ i, C j i := Finset.sum_congr rfl (fun i _ => hsym i j)
      _ = a j+b j := hbalance j
  exact rankZeroTable_mem_of_transport q hbalance hcols hsa hsb

end Bell
