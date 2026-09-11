import Bell.Quantum

/-! Explicit entrywise norms for finite matrices. We do not install a global
matrix norm; opening Bell.Entrywise selects the Pi norm only where calculus
needs a concrete norm. All matrix products are treated as finite polynomials. -/
noncomputable section
namespace Bell.Entrywise
scoped instance matrixNormedAddCommGroup {m n : Type*} [Fintype m] [Fintype n]
    {𝕜 : Type*} [NormedAddCommGroup 𝕜] : NormedAddCommGroup (Matrix m n 𝕜) :=
  inferInstanceAs (NormedAddCommGroup (m → n → 𝕜))
scoped instance matrixNormedSpace {m n : Type*} [Fintype m] [Fintype n]
    {𝕜 : Type*} [NormedAddCommGroup 𝕜] [NormedSpace ℝ 𝕜] : NormedSpace ℝ (Matrix m n 𝕜) :=
  inferInstanceAs (NormedSpace ℝ (m → n → 𝕜))
end Bell.Entrywise
