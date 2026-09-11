import Bell.Quantum
import Bell.Scalars

/-!
# The explicit complex-qubit strategy (paper §3.1)

All density matrices and effects are concrete complex matrices.  Positivity is
proved through Gram factorizations, not stipulated as a certificate hypothesis.
The upper bound over arbitrary PVM strategies is deliberately NOT claimed here.

STATUS: uncompiled proof source. See reports/status.json.
-/

noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace Bell

/-- A rank-one real-plane qubit effect, represented over the complex numbers. -/
def polarEffect (z x : ℝ) : Operator :=
  !![ (((1 + z) / 2 : ℝ) : ℂ), ((x / 2 : ℝ) : ℂ);
      ((x / 2 : ℝ) : ℂ), (((1 - z) / 2 : ℝ) : ℂ) ]

theorem polarEffect_hermitian (z x : ℝ) :
    (polarEffect z x).conjTranspose = polarEffect z x := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    apply Complex.ext <;> norm_num [polarEffect, Matrix.conjTranspose_apply]

theorem polarEffect_idempotent (z x : ℝ) (h : z ^ 2 + x ^ 2 = 1) :
    polarEffect z x * polarEffect z x = polarEffect z x := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    apply Complex.ext <;>
    norm_num [polarEffect, Matrix.mul_apply, Fin.sum_univ_two] <;> nlinarith [h]

theorem polarEffect_positive (z x : ℝ) (h : z ^ 2 + x ^ 2 = 1) :
    (polarEffect z x).PosSemidef := by
  have hg := gram_positive (polarEffect z x)
  rw [polarEffect_hermitian, polarEffect_idempotent z x h] at hg
  exact hg

theorem polarEffect_complement (z x : ℝ) :
    polarEffect z x + polarEffect (-z) (-x) = 1 := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    apply Complex.ext <;> norm_num [polarEffect, Matrix.one_apply] <;> ring

abbrev halfRoot : ℝ := sqrtTwo / 2

theorem halfRoot_sq : halfRoot ^ 2 = 1 / 2 := by
  dsimp [halfRoot]
  nlinarith [sqrtTwo_sq]

def aux0 : Operator := !![16/25, -4/25; -4/25, 1/25]
def aux1 : Operator := !![1/25, -4/25; -4/25, 16/25]
def aux2 : Operator := !![8/25, 8/25; 8/25, 8/25]

def auxGram0 : Operator := !![4/5, -1/5; 0, 0]
def auxGram1 : Operator := !![1/5, -4/5; 0, 0]
def auxGram2 : Operator := !![2/5, 2/5; 2/5, 2/5]

theorem aux0_gram : auxGram0.conjTranspose * auxGram0 = aux0 := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    apply Complex.ext <;> norm_num [aux0, auxGram0, Matrix.conjTranspose_apply, Matrix.mul_apply,
      Fin.sum_univ_two, map_ofNat]

theorem aux1_gram : auxGram1.conjTranspose * auxGram1 = aux1 := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    apply Complex.ext <;> norm_num [aux1, auxGram1, Matrix.conjTranspose_apply, Matrix.mul_apply,
      Fin.sum_univ_two, map_ofNat]

theorem aux2_gram : auxGram2.conjTranspose * auxGram2 = aux2 := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    apply Complex.ext <;> norm_num [aux2, auxGram2, Matrix.conjTranspose_apply, Matrix.mul_apply,
      Fin.sum_univ_two, map_ofNat]

theorem aux0_positive : aux0.PosSemidef := by
  rw [← aux0_gram]
  exact gram_positive auxGram0

theorem aux1_positive : aux1.PosSemidef := by
  rw [← aux1_gram]
  exact gram_positive auxGram1

theorem aux2_positive : aux2.PosSemidef := by
  rw [← aux2_gram]
  exact gram_positive auxGram2

theorem auxiliary_normalized : aux0 + aux1 + aux2 = 1 := by
  funext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [aux0, aux1, aux2, Matrix.one_apply]

theorem auxiliary_not_projective : aux0 * aux0 ≠ aux0 := by
  intro h
  have he := congrArg (fun M : Operator => (M 0 0).re) h
  norm_num [aux0, Matrix.mul_apply, Fin.sum_univ_two] at he

/-- Density matrix of (|00⟩ + |11⟩)/√2. -/
def phiDensity : JointOperator :=
  fun i j => if i.1 = i.2 ∧ j.1 = j.2 then 1/2 else 0

/-- Two equal rational rows avoid introducing a radical in the Gram factor. -/
def phiGram : Matrix (Fin 2) Joint ℂ :=
  fun _ j => if j.1 = j.2 then 1/2 else 0

theorem phi_gram : phiGram.conjTranspose * phiGram = phiDensity := by
  funext i j
  rcases i with ⟨i₀, i₁⟩
  rcases j with ⟨j₀, j₁⟩
  fin_cases i₀ <;> fin_cases i₁ <;> fin_cases j₀ <;> fin_cases j₁ <;>
    norm_num [phiGram, phiDensity, Matrix.conjTranspose_apply,
      Matrix.mul_apply, Fin.sum_univ_two]

theorem phi_positive : phiDensity.PosSemidef := by
  rw [← phi_gram]
  exact joint_gram_positive phiGram

theorem phi_normalized : Matrix.trace phiDensity = 1 := by
  norm_num [Matrix.trace, phiDensity, Fintype.sum_prod_type, Fin.sum_univ_two]

def phiState : State where
  density := phiDensity
  positive := phi_positive
  normalized := phi_normalized

/-- Bell-state Born identity, for arbitrary complex local operators. -/
theorem phi_trace_tensor (A B : Operator) :
    Matrix.trace (phiDensity * tensor A B) =
      (A 0 0 * B 0 0 + A 0 1 * B 0 1 +
       A 1 0 * B 1 0 + A 1 1 * B 1 1) / 2 := by
  simp [Matrix.trace, Matrix.mul_apply, tensor, phiDensity,
    Fintype.sum_prod_type, Fin.sum_univ_two]
  <;> ring

/-- Three labels are declared on Alice's first two inputs, but label 2 is zero.
This is the paper's common-label presentation of (2,2,3)-by-(2,2). -/
abbrev separatorArchitecture : Architecture where
  aliceInputs := 3
  bobInputs := 2
  aliceOutputs := fun _ => 3
  bobOutputs := fun _ => 2

def aliceEffect : Fin 3 → Fin 3 → Operator :=
  ![ ![polarEffect halfRoot halfRoot, polarEffect (-halfRoot) (-halfRoot), 0],
     ![polarEffect halfRoot (-halfRoot), polarEffect (-halfRoot) halfRoot, 0],
     ![aux0, aux1, aux2] ]

def bobEffect : Fin 2 → Fin 2 → Operator :=
  ![ ![polarEffect 1 0, polarEffect (-1) 0],
     ![polarEffect 0 1, polarEffect 0 (-1)] ]

theorem alice_positive (x a : Fin 3) : (aliceEffect x a).PosSemidef := by
  fin_cases x <;> fin_cases a
  · apply polarEffect_positive; nlinarith [halfRoot_sq]
  · apply polarEffect_positive; nlinarith [halfRoot_sq]
  · exact Matrix.PosSemidef.zero
  · apply polarEffect_positive; nlinarith [halfRoot_sq]
  · apply polarEffect_positive; nlinarith [halfRoot_sq]
  · exact Matrix.PosSemidef.zero
  · exact aux0_positive
  · exact aux1_positive
  · exact aux2_positive

theorem bob_positive (y b : Fin 2) : (bobEffect y b).PosSemidef := by
  fin_cases y <;> fin_cases b <;> apply polarEffect_positive <;> norm_num

theorem alice_normalized (x : Fin 3) : ∑ a, aliceEffect x a = 1 := by
  fin_cases x <;> funext i j <;> fin_cases i <;> fin_cases j <;>
    apply Complex.ext <;>
    norm_num [aliceEffect, polarEffect, aux0, aux1, aux2, Fin.sum_univ_succ,
      Matrix.one_apply] <;> ring

theorem bob_normalized (y : Fin 2) : ∑ b, bobEffect y b = 1 := by
  fin_cases y <;> funext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [bobEffect, polarEffect, Fin.sum_univ_two, Matrix.one_apply]

def witnessStrategy : Strategy separatorArchitecture where
  state := phiState
  alice := fun x => ⟨aliceEffect x, alice_positive x, alice_normalized x⟩
  bob := fun y => ⟨bobEffect y, bob_positive y, bob_normalized y⟩

def witnessBehavior : Behavior separatorArchitecture := witnessStrategy.behavior

def aliceSign (a : Fin 3) : ℝ := if a = 1 then -1 else 1
def bobSign (b : Fin 2) : ℝ := if b = 0 then 1 else -1

def correlation (p : Behavior separatorArchitecture) (x : Fin 3) (y : Fin 2) : ℝ :=
  ∑ a, ∑ b, aliceSign a * bobSign b * p x y a b

def bellScore (p : Behavior separatorArchitecture) : ℝ :=
  10 * (correlation p 0 0 + correlation p 0 1 +
    correlation p 1 0 - correlation p 1 1) +
  (3/5) * p 2 0 0 0 + (3/5) * p 2 0 1 1 + (4/5) * p 2 1 2 0

/-- The witness is a point of the physical raw POVM image, not just a table. -/
theorem witness_mem_raw : witnessBehavior ∈ rawPOVM separatorArchitecture :=
  ⟨witnessStrategy, rfl⟩

theorem witness_mem_convex : witnessBehavior ∈ convexPOVM separatorArchitecture :=
  subset_convexHull ℝ (rawPOVM separatorArchitecture) witness_mem_raw

theorem witness_auxiliary_probabilities :
    witnessBehavior 2 0 0 0 = 8/25 ∧
    witnessBehavior 2 0 1 1 = 8/25 ∧
    witnessBehavior 2 1 2 0 = 8/25 := by
  change born phiDensity aux0 (polarEffect 1 0) = 8/25 ∧
    born phiDensity aux1 (polarEffect (-1) 0) = 8/25 ∧
    born phiDensity aux2 (polarEffect 0 1) = 8/25
  norm_num [born, phi_trace_tensor, polarEffect, aux0, aux1, aux2]

theorem witness_correlations :
    correlation witnessBehavior 0 0 = halfRoot ∧
    correlation witnessBehavior 0 1 = halfRoot ∧
    correlation witnessBehavior 1 0 = halfRoot ∧
    correlation witnessBehavior 1 1 = -halfRoot := by
  unfold correlation
  norm_num [witnessBehavior, witnessStrategy, Strategy.behavior, phiState, born,
    phi_trace_tensor, aliceEffect, bobEffect, polarEffect,
    aliceSign, bobSign, Fin.sum_univ_succ]
  <;> ring_nf <;> simp

theorem witness_value : bellScore witnessBehavior = lower := by
  rcases witness_auxiliary_probabilities with ⟨h₀, h₁, h₂⟩
  rcases witness_correlations with ⟨h₀₀, h₀₁, h₁₀, h₁₁⟩
  unfold bellScore
  rw [h₀₀, h₀₁, h₁₀, h₁₁, h₀, h₁, h₂]
  unfold lower halfRoot
  ring

theorem physical_povm_value_above_numeric_upper :
    ∃ p ∈ rawPOVM separatorArchitecture, upper < bellScore p := by
  refine ⟨witnessBehavior, witness_mem_raw, ?_⟩
  rw [witness_value]
  exact strict_gap

end Bell
