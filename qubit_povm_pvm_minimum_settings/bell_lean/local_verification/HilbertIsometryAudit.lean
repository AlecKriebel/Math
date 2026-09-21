import Bell.HilbertIsometry
noncomputable section
open scoped InnerProductSpace
open Bell.Hilbert

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    {d : ℕ} (b : OrthonormalBasis (Fin d) ℂ E) (hd : d ≤ 2) :
    E →ₗᵢ[ℂ] EuclideanSpace ℂ (Fin 2) := linearIsometry b hd

#print axioms Bell.Hilbert.linearIsometry
#print axioms Bell.Hilbert.linearIsometry_apply
#print axioms Bell.Hilbert.linearIsometry_inner
#print axioms Bell.Hilbert.linearIsometry_injective
