import Bell.IsometricCompression
open scoped Matrix ComplexOrder
open Bell.IsometricCompression

-- The carrier edge cases are accepted by the same construction.
example : (canonicalEmbedding (by decide : 0 ≤ 2)).conjTranspose *
    canonicalEmbedding (by decide : 0 ≤ 2) = 1 := canonicalEmbedding_isometry _
example : (canonicalEmbedding (by decide : 1 ≤ 2)).conjTranspose *
    canonicalEmbedding (by decide : 1 ≤ 2) = 1 := canonicalEmbedding_isometry _
example : (canonicalEmbedding (by decide : 2 ≤ 2)).conjTranspose *
    canonicalEmbedding (by decide : 2 ≤ 2) = 1 := canonicalEmbedding_isometry _

-- In full dimension there is no supplementary effect.
example : complement (canonicalEmbedding (by decide : 2 ≤ 2)) = 0 := by
  have h : canonicalEmbedding (by decide : 2 ≤ 2) = 1 := by
    ext i j
    simp [canonicalEmbedding, Matrix.one_apply]
  rw [h]
  simp [complement]

#print axioms Bell.IsometricCompression.complement_positive
#print axioms Bell.IsometricCompression.paddedEffect_orthogonal
#print axioms Bell.IsometricCompression.povm
#print axioms Bell.IsometricCompression.pvm
#print axioms Bell.IsometricCompression.state
#print axioms Bell.IsometricCompression.born_padded
#print axioms Bell.IsometricCompression.canonicalEmbedding_isometry
