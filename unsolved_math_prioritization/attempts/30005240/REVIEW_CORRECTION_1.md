# Review correction 1: rank of the finite clock operator

This additive correction supersedes one rank statement in the historical TURN_5.md, Section 5, and its identical description of the model as rank L+1. The frozen proof file and FINAL_AUTHOR_MANIFEST.json are preserved unchanged for provenance.

For L≥1, the displayed operator has **rank exactly L**, rather than L+1. Its output coordinates L−1 and L both equal sigma f(L); only the L input coordinates 1,...,L are used. Conversely, restricting to output coordinates 0,...,L−1 and input coordinates 1,...,L gives sigma times the L-dimensional identity matrix. These two observations prove the upper and lower rank bounds.

It still acts on the indicated L+1 coordinate subspace and is zero on all later output coordinates. Its finite-dimensional active matrix still has eigenvalue sigma algebraically simple and eigenvalue zero with algebraic multiplicity L. Therefore finite rank/compactness, positivity, operator norm sigma, the exact iterate formula, uniform summability and the logarithmic-window obstruction are unchanged. No source-specific conclusion is strengthened.

This is a localized proof-review correction after five completed author turns, not an additional author search. The original target remains unresolved 5/5. The supplementary exact checker verifies the rank certificate for L=1,...,100 using rational matrix entries; the general proof is the preceding coordinate argument.

Historical TURN_5.md SHA-256: c41297a9c2ed46e8337fe9188e4ef520251323890dd15a7b28d9f8ff742c2eb4
Original FINAL_AUTHOR_MANIFEST.json SHA-256: 2791a4f342f256ce032c6b8b16c6577267f19453074608e5fca77322add10c9e
