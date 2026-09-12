import Bell

/- Independent referee contract: the set equality is restated with explicit
complex matrices, positivity, normalization, orthogonality, and the tensor
entries. The independent set definitions do not mention Bell's strategy or
behavior-image definitions. -/
noncomputable section
open scoped BigOperators Matrix ComplexOrder
namespace RefereeMatrixModel

abbrev Table (AO BO : Fin 2 → ℕ) :=
  (x y : Fin 2) → Fin (AO x) → Fin (BO y) → ℝ
abbrev LocalMatrices (O : Fin 2 → ℕ) :=
  (x : Fin 2) → Fin (O x) → Matrix (Fin 2) (Fin 2) ℂ

def MatrixPOVMBehaviors (AO BO : Fin 2 → ℕ) : Set (Table AO BO) :=
  {p | ∃ (ρ : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ)
    (M : LocalMatrices AO) (N : LocalMatrices BO),
    ρ.PosSemidef ∧ Matrix.trace ρ = 1 ∧
    (∀ x a, (M x a).PosSemidef) ∧ (∀ x, ∑ a, M x a = 1) ∧
    (∀ y b, (N y b).PosSemidef) ∧ (∀ y, ∑ b, N y b = 1) ∧
    p = fun x y a b => (Matrix.trace (ρ *
      Matrix.of (fun i j : Fin 2 × Fin 2 => M x a i.1 j.1 * N y b i.2 j.2))).re}

def MatrixPVMBehaviors (AO BO : Fin 2 → ℕ) : Set (Table AO BO) :=
  {p | ∃ (ρ : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ)
    (M : LocalMatrices AO) (N : LocalMatrices BO),
    ρ.PosSemidef ∧ Matrix.trace ρ = 1 ∧
    (∀ x a, (M x a).PosSemidef) ∧ (∀ x, ∑ a, M x a = 1) ∧
    (∀ y b, (N y b).PosSemidef) ∧ (∀ y, ∑ b, N y b = 1) ∧
    (∀ x a, M x a * M x a = M x a) ∧
    (∀ x a a', a ≠ a' → M x a * M x a' = 0) ∧
    (∀ y b, N y b * N y b = N y b) ∧
    (∀ y b b', b ≠ b' → N y b * N y b' = 0) ∧
    p = fun x y a b => (Matrix.trace (ρ *
      Matrix.of (fun i j : Fin 2 × Fin 2 => M x a i.1 j.1 * N y b i.2 j.2))).re}

theorem matrix_povm_matches (AO BO : Fin 2 → ℕ) :
    MatrixPOVMBehaviors AO BO = Bell.rawPOVM ⟨2, 2, AO, BO⟩ := by
  ext p
  constructor
  · rintro ⟨ρ, M, N, hρ, ht, hM, hMn, hN, hNn, rfl⟩
    let s : Bell.Strategy ⟨2, 2, AO, BO⟩ :=
      { state := ⟨ρ, hρ, ht⟩
        alice := fun x => ⟨M x, hM x, hMn x⟩
        bob := fun y => ⟨N y, hN y, hNn y⟩ }
    exact ⟨s, rfl⟩
  · rintro ⟨s, rfl⟩
    exact ⟨s.state.density, fun x => (s.alice x).effect, fun y => (s.bob y).effect,
      s.state.positive, s.state.normalized, fun x => (s.alice x).positive,
      fun x => (s.alice x).normalized, fun y => (s.bob y).positive,
      fun y => (s.bob y).normalized, rfl⟩

theorem matrix_pvm_matches (AO BO : Fin 2 → ℕ) :
    MatrixPVMBehaviors AO BO = Bell.rawPVM ⟨2, 2, AO, BO⟩ := by
  ext p
  constructor
  · rintro ⟨ρ, M, N, hρ, ht, hM, hMn, hN, hNn, hMi, hMo, hNi, hNo, rfl⟩
    let s : Bell.ProjectiveStrategy ⟨2, 2, AO, BO⟩ :=
      { state := ⟨ρ, hρ, ht⟩
        alice := fun x => ⟨⟨M x, hM x, hMn x⟩, hMi x, hMo x⟩
        bob := fun y => ⟨⟨N y, hN y, hNn y⟩, hNi y, hNo y⟩ }
    exact ⟨s, rfl⟩
  · rintro ⟨s, rfl⟩
    exact ⟨s.state.density, fun x => (s.alice x).effect, fun y => (s.bob y).effect,
      s.state.positive, s.state.normalized, fun x => (s.alice x).positive,
      fun x => (s.alice x).normalized, fun y => (s.bob y).positive,
      fun y => (s.bob y).normalized, fun x => (s.alice x).idempotent,
      fun x => (s.alice x).orthogonal, fun y => (s.bob y).idempotent,
      fun y => (s.bob y).orthogonal, rfl⟩

/-- Arbitrary finite input-dependent outcome counts, with no positivity
hypothesis on the counts and no physical or geometric theorem assumed. -/
theorem explicit_complex_matrix_convex_equality (AO BO : Fin 2 → ℕ) :
    convexHull ℝ (MatrixPOVMBehaviors AO BO) =
      convexHull ℝ (MatrixPVMBehaviors AO BO) := by
  rw [matrix_povm_matches, matrix_pvm_matches]
  exact Bell.two_input_convex_equality AO BO

#print axioms explicit_complex_matrix_convex_equality
end RefereeMatrixModel
