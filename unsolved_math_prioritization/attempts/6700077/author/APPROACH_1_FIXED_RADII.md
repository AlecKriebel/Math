# Approach 1: direct comparison at fixed radii

## Statement

Let g_j and g be continuous positive-definite metrics on a fixed n-manifold, n >= 2, with g_j -> g locally uniformly. Fix kappa > 0. Suppose that, on each sufficiently small relatively compact neighborhood U, for every lambda in (0,kappa), there is R_lambda > 0, independent of j, such that for centers x in a smaller neighborhood and 0 < r < R_lambda,

vol_gj(B_gj(x,r)) <= M_lambda(r).

All relevant balls must lie in U; shrinking R_lambda ensures this. Then g has the intended volumic lower bound kappa on the smaller neighborhood. Only per-lambda uniformity is needed, not a radius uniform over lambda. The analogous conclusion for the stronger zero condition holds if every model is omega_n r^n and there is one common positive radius.

## Proof

On a fixed compact neighborhood, for j sufficiently large,

(1-e_j)g <= g_j <= (1+e_j)g, with e_j -> 0 and 0 < e_j < 1.

Integration of path lengths gives the corresponding square-root distance bounds for paths in that neighborhood. For the small balls under discussion, paths leaving a fixed larger neighborhood cost more than the radius: continuous positive-definite metrics have a uniform local ellipticity constant, so a positive coordinate separation gives a positive length bound. Thus the same ball inclusions hold for the intrinsic distances relevant here:

B_g(x,r) is contained in B_gj(x,sqrt(1+e_j)r).

The eigenvalues of g_j relative to g lie in [1-e_j,1+e_j], so their volume densities satisfy

(1-e_j)^(n/2) dvol_g <= dvol_gj <= (1+e_j)^(n/2) dvol_g.

For fixed r < R_lambda, eventually sqrt(1+e_j)r < R_lambda. Therefore

vol_g(B_g(x,r)) <= (1-e_j)^(-n/2) M_lambda(sqrt(1+e_j)r).

Letting j tend to infinity gives the non-strict inequality with M_lambda(r). This argument does not need spheres to have zero volume or any interchange of moving-set limits.

For a requested strict comparison at lambda < kappa, choose lambda' in (lambda,kappa), apply the preceding conclusion to lambda', and restrict r further. The model expansions give

M_lambda(r)-M_lambda'(r)
 = omega_n (lambda'-lambda) r^(n+2)/(6(n+2)) + O(r^(n+4)) > 0.

Consequently vol_g(B_g(x,r)) <= M_lambda'(r) < M_lambda(r) for all sufficiently small r. The radius is uniform on the smaller neighborhood because both the original common witness and the model comparison are uniform there. Local positive witnesses can be reduced to a continuous positive radius function by a locally finite cover and a partition of unity subordinate to neighborhoods with valid smaller radii. Specifically, choose positive constants valid on each cover element and use a partition-weighted average of those constants; at every point each active constant is valid, hence their average is no greater than the maximum active valid constant. If desired first reduce each constant so validity also holds throughout its cover element. This supplies the requested local convention.

For the zero-model statement the same limit argument directly gives vol_g(B_g(x,r)) <= omega_n r^n. No strict inequality at zero follows merely by taking a limit. QED.

## Automatic n-dimensional normalization

Every continuous Riemannian metric satisfies vol_g(B_g(x,r))/(omega_n r^n) -> 1. To see this, use coordinates in which g(x)=I. On a sufficiently small neighborhood (1-e)I <= g <= (1+e)I and the determinant density lies between (1-e)^(n/2) and (1+e)^(n/2). Euclidean ball inclusions then sandwich the normalized ratio between ((1-e)/(1+e))^(n/2) and its reciprocal. First let r decrease within that neighborhood, then let e decrease to zero.

## Relation to known work and residual obstruction

This is the fixed-manifold elementary mechanism behind Deng's common-SC-radius theorem. It is not a removal of that assumption. The conjecture gives, for each j, some positive R_j,lambda; it does not give a positive infimum over j. If R_j,lambda tends to zero, the fixed r used above eventually lies outside the range in which the hypothesis can be applied. Compactness in the center for an individual metric does not make the radius uniform across j.
