# Checkpoint 1 Adversarial Review — Mathematical Scope

**Reviewer role:** proof auditor  
**Verdict:** CONDITIONAL GO

## Accepted scope

The reviewer accepted the following as a useful NCS application:

> A gold-standard-free commutator audit that can refute a uniform
> retrain-equivalence tolerance without computing a retrained reference.

The reviewer rejected presenting it as a successful-unlearning certificate or
as a strong standalone theorem paper without broader validation.

## Verified mathematical core

For path outputs \(Y=\{y_\pi\}\) and every common target \(t\),

\[
\max_\pi d(y_\pi,t)
\ge \inf_z\max_\pi d(y_\pi,z)
\ge \frac12\operatorname{diam}(Y).
\]

For two normed-space outputs \(y_{ij},y_{ji}\), the exact radius is half their
distance and is attained at the midpoint. The reviewer also verified the
Hilbert-space identity

\[
\frac{\|y_{ij}-t\|^2+\|y_{ji}-t\|^2}{2}
=
\left\|\frac{y_{ij}+y_{ji}}2-t\right\|^2
+\frac{\|y_{ij}-y_{ji}\|^2}{4}.
\]

For affine deletion maps, the square defect is affine, so its values on an
affine basis reconstruct it exactly. The reviewer stressed that this is
elementary affine algebra and may require off-manifold queries.

For the fixed-preconditioner relinearized ridge map

\[
U_i(\theta)=\theta+P x_i(x_i^\top\theta-y_i),
\]

the reviewer independently derived

\[
\Omega_{ij}(\theta)
=(x_j^\top P x_i)
\left[
P x_j(x_i^\top\theta-y_i)
-P x_i(x_j^\top\theta-y_j)
\right].
\]

For nonzero features and positive-definite \(P\), this vanishes globally iff
the features are \(P\)-orthogonal or the labeled examples are proportional.

## Required distinctions

- A frozen-vector influence update is a translation and commutes.
- A fixed-preconditioner update that re-evaluates the deleted example's
  residual at the current state generally does not commute.
- Exact retained-Hessian quadratic deletion is a reset to the retained-data
  minimizer and commutes.
- Midpoint averaging removes the antisymmetric order component but need not
  improve fidelity to retraining.
- Zero defect can coexist with arbitrarily large retraining error.

## Novelty boundary

The lower bound, Chebyshev center, affine interpolation, influence algebra, and
kernel distances are individually standard. The possible contribution is their
specific organization as a deletion-order, target-free rejection audit.

