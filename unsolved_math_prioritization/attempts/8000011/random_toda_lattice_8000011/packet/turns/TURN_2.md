# Author turn 2: expectation justified at fixed n

2026-10-03 06:20 UTC. Partial theorem; full original problem unresolved. Completion estimate: 55% toward a fixed-n asymptotic packet, 10% toward full source request.

Retain all definitions and clock from Turn 1. For the declared unscaled GOE, the ordered eigenvalue density is

 p_n(lambda)=Z_n^−1 exp(−sum_j lambda_j²/4) Delta(lambda), lambda_1<...<lambda_n,

where Z_n is the integral over this chamber. The squared first-row eigenvector coordinates w are independent of lambda and have Dirichlet(1/2,...,1/2) law. These are classical GOE spectral-coordinate facts (Dumitriu–Edelman, Matrix Models for Beta Ensembles, 2002, Theorem 2.1 and beta-Hermite spectral law); their paper uses a convention smaller by sqrt(2), and scaling to diagonal variance 2 gives the density above. No new random-matrix distribution theorem is claimed.

## Integrability lemma, including collisions

Let d=min_j(lambda_(j+1)−lambda_j), R=max(1,max_j|lambda_j|), d0=min(1,d), and W=sum_j|log w_j|. For every fixed n>=2,

 E[(1+log(2R)+log(1/d0)+W)/d] < infinity.                 (5)

Proof. Partition the ordered chamber, up to null boundaries, into Omega_j where lambda_(j+1)−lambda_j is the smallest gap. On Omega_j, division of Delta(lambda) by d exactly cancels its factor lambda_(j+1)−lambda_j. The remaining product has polynomial growth in the coordinates. A factor log(2R) therefore remains Gaussian-integrable.

For the logarithmic collision singularity, use coordinates g=lambda_(j+1)−lambda_j, c=(lambda_(j+1)+lambda_j)/2, and the other lambda's. On 0<g<1 the cancelled Vandermonde is bounded in absolute value by a fixed polynomial in |c| and the remaining coordinates (g is bounded), while the Gaussian factor splits into exp(−c²/2−g²/8) times the remaining Gaussian factors. Dropping the ordering constraints bounds the integral by a finite Gaussian-polynomial integral times int_0^1 |log g| dg=1. On d>=1 the logarithm is zero. This argument also includes simultaneous multiple collisions, since other Vandermonde factors vanish instead of creating new singularities. Finally W is independent of lambda and has finite expectation: each w_j has Beta(1/2,(n−1)/2) distribution and the logarithmic endpoint integrals are finite. This proves (5).

The same argument gives finite eigenvalue inverse-gap p-th moments, with logarithmic factors of any fixed finite degree, for 0<p<2. At a single isolated collision the local density is proportional to g dg, so p>=2 is not generally integrable. That observation is not yet a claim about moments of T at a fixed positive tolerance.

## Integrable deterministic error envelope

Define K=W+n(n−1)[log(2R)+log(1/d0)]. Every dominant coefficient satisfies |log A_k|<=K. Indeed its weight factor is at least exp(−W), every nonzero difference is at least d0 and at most 2R, and there are k(k−1)/2 squared differences. Also

 A_k <= tau_k(0) <= binomial(n,k)(2R)^(k(k−1)),

so 0<=log M_k<=n log2+2K. It follows that |log c_k|<=2K, and the H from Turn 1 satisfies

 H<=4K+n log2.

Thus D_n:=E[(4K+n log2)/d] is finite by (5). Taking expectations in the fully deterministic inequality (3) proves, for every fixed n>=2 and 0<epsilon<=1,

 |E[T_all(n,epsilon)]−C_n log(1/epsilon)|<=D_n,
 C_n=E[1/d]
    = Z_n^−1 int_(lambda_1<...<lambda_n) exp(−sum lambda_j²/4) Delta(lambda)/min_j(lambda_(j+1)−lambda_j) d lambda.       (6)

In particular E[T_all]/log(1/epsilon) -> C_n. This is an expectation statement with its rare-gap and norming-constant tails checked, not merely a pointwise extrapolation. C_n is an absolutely convergent, eigenvalue-only finite-dimensional integral; D_n is explicit as another convergent integral under the stated laws. These constants have not been reduced to a closed general-n expression.

## Exact remaining gap

This does not determine E[T_all] at general epsilon, nor establish a simultaneous n→infinity/tolerance limit. The source imposed no such restricted regime, so this is a scoped partial theorem. All later uses must retain 'fixed n' and the declared normalization. Distributional smallest-gap limit laws cannot alone justify an n→infinity asymptotic for C_n.
