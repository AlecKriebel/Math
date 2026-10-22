# Auxiliary local expansion at the orthant

This independently derived check is not needed for the complete classical deduction in `PROOF.md`. Its historical novelty has not been established.

Let `H` be symmetric with zero diagonal and let `G=I+H` be positive definite. In a fixed dimension, as `H→0`,

\[
 4^nq(G)q(G^{-1})
 =1-\frac{(2\pi-4)\sum_{i<j}h_{ij}^2+(4-\pi)\|H\mathbf1\|^2}{\pi^2}
 +O_n(\|H\|_F^3). \tag{1}
\]

Consequently, in the normalized generator-Gram chart, the orthant has strictly negative Hessian in every nonzero shape direction. The zero diagonal is the normalization of generator lengths; those lengths are not genuine cone deformations.

## Derivation

Write `a=2/π`, `S=Σ_{i<j}h_ij`, `E=Σ_{i<j}h_ij²`. Let `U` sum `h_ij h_ik` over all unordered pairs of distinct edges sharing a vertex, and let `V` sum products over all unordered pairs of disjoint edges. Then

\[
 S^2=E+2U+2V,\qquad
 \|H\mathbf1\|^2=2E+2U. \tag{2}
\]

If `X_i` are independent standard half-normal variables, then `E X_i=√(2/π)` and `E X_i²=1`. Expanding the Gaussian density with covariance `I+tH` around `t=0` yields

\[
 2^nq(I+tH)=1+atS+a^2t^2V+O(t^3). \tag{3}
\]

Here are the density details, to make the second-order cancellation explicit:

\[
 \det(I+tH)^{-1/2}=1+\tfrac14t^2\operatorname{tr}H^2+O(t^3),
\]
\[
 (I+tH)^{-1}=I-tH+t^2H^2+O(t^3),
\]
\[
 \mathbb E(X^THX)^2=4(E+2aU+2a^2V),\quad
 \mathbb E X^TH^2X=2E+2aU,\quad
 \operatorname{tr}H^2=2E.
\]

In the density expansion the quadratic coefficient is

\[
 \tfrac18\mathbb E(X^THX)^2
 -\tfrac12\mathbb E X^TH^2X
 +\tfrac14\operatorname{tr}H^2=a^2V,
\]

which proves (3). At the identity the first differential in a covariance perturbation `K` is `a Σ_{i<j}k_ij`; diagonal perturbations contribute zero because independent coordinate rescalings preserve the orthant event. Therefore

\[
 2^nq((I+tH)^{-1})
 =1-atS+t^2(aU+a^2V)+O(t^3), \tag{4}
\]

because `Σ_{i<j}(H²)_ij=U`. Multiplying (3) and (4), and using (2), gives

\[
 aU+2a^2V-a^2S^2
 =-a^2E+(a-2a^2)U
 =-(a-a^2)E-(a^2-a/2)\|H\mathbf1\|^2,
\]

which is exactly (1). The coefficients `2π−4` and `4−π` are positive.

The Taylor estimates are valid uniformly in a fixed-dimensional neighborhood of the identity: there the covariance and inverse covariance remain positive definite with eigenvalues bounded away from zero, and derivatives through order three are bounded by integrable polynomial multiples of a fixed Gaussian density. This also turns (1) into a genuine local quadratic stability inequality, not merely a directional formal expansion. For example, for sufficiently small `||H||F` depending on `n`,

\[
 4^nq(I+H)q((I+H)^{-1})
 \leq 1-\frac{\pi-2}{2\pi^2}\|H\|_F^2.
\]

For a single nonzero off-diagonal pair, (1) gives deficit `4t²/π²`, in agreement with the exact planar formula `1−4(arcsin t)²/π²`.
