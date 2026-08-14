# Unsent specialist inquiries

These drafts are prepared for manual sending. No message was sent automatically.

## Reaction-network / Turing specialist

**Subject:** Priority and scope check: exact classical mass-action stationary-Turing decision theorem

We study an indexed classical mass-action network with source matrix `Y` and stoichiometric matrix `Gamma`. We claim that weak all-mobile stationary diffusion-driven instability exists exactly when there are `v>0`, `Gamma v=0`, and `h>0` such that `Gamma diag(v) Y^T diag(h)` is Hurwitz on `im Gamma` and has a negative signed principal minor. Routh-Hurwitz plus a Boolean principal-set selector gives an exact existential-real formula. We explicitly mean a positive real nonzero-mode eigenvalue, not first crossing, wave exclusion, or nonlinear pattern formation.

Have you seen an earlier arbitrary-network classical-mass-action iff theorem with these existential quantifiers? In particular, does any unstable-core, child-selection, or graph-theoretic Turing result already imply this exact network-wide formulation or its fixed-species algorithm?

The proof point on which I would especially value scrutiny is the conservation treatment: homogeneous stability is on `im Gamma`, but a nonzero Neumann amplitude is unrestricted because its spatial mean is zero, so the diffusive matrix is tested on the full species space.

## Matrix-stability specialist

**Subject:** Check of a diagonal-damping lemma and a reduction-specific scaling elimination

For a real square matrix `J`, we prove that some positive diagonal `D` makes `J-D` have a positive real eigenvalue iff `(-1)^|I| det J[I,I] < 0` for some principal set. The sufficiency proof isolates the corresponding coefficient in `det(D-J)` by assigning `d_i=t^{-1}` on `I` and `d_i=t` off `I`, then uses negativity of the characteristic polynomial at zero.

Separately, our NP-hardness proof does not solve general positive diagonal stabilizability. For a particular row-split lift `L(q)` of the Blondel-Tsitsiklis `PARTITION` family, we prove `exists q,D>0: L(q)D Hurwitz` iff the partition instance is YES. The key is the one-positive-eigenvalue inertia of `L(0)D`, determinant continuity, and transfer of an interior singularity back to the original interval matrix.

Are either statement or this exact scaling-elimination argument already standard under another name? Do you see a gap in the inertia-to-interior-singularity step for arbitrary relative diagonal magnitudes?

## Real-algebraic geometry / complexity specialist

**Subject:** Complexity audit: fixed-species projection and exact certificates for a mass-action decision problem

The arbitrary-network formula is in the existential theory of the reals using polynomial-size determinant/Hurwitz circuits and Boolean selector variables. NP-hardness is only from `PARTITION`.

For fixed species count `n`, we project `K={v>=0: Gamma v=0}` under `Phi(v)=Gamma diag(v)Y^T`. Extreme rays of `K` have support at most `rank Gamma+1<=n+1`, so they can be enumerated in polynomial time; their images give a cone in fixed dimension `n^2`. A fixed-dimensional relative-facet description and then fixed-variable real-algebraic decision yield polynomial bit complexity.

For certificates, strict inequalities are equationized and we use algebraic sample points for YES and Real Nullstellensatz identities for NO. We claim finite exact existence and exhaustive computability, but no polynomial size and no practical general generator.

Does the fixed-dimensional generator-to-relative-facet and Renegar/Basu-Pollack-Roy step support the stated polynomial bit complexity with the number of reactions variable? Is the certificate wording appropriately limited?
