# Adversarial audit of the closure proof

## Audit conclusion

No unresolved mathematical dependency remains inside the residual \((2,3)\)-by-\((2,3)\) architecture, conditional only on the frozen architecture reduction. The earlier numerical “always \((7,7)\)” claim was found to be false and was removed; the proof now uses a weaker exact inertia statement that is sufficient on every rank stratum.

## 1. Convex separation

**Possible failure:** excluding only exposed smooth points might miss singular or nonexposed points.

**Resolution:** the proof starts from a nearest-point strict separating functional. Its maximum over the compact residual set is attained. The rank analysis is performed on the smooth incidence lift, not merely on the projected behavior image, and covers metric differential ranks \(0,1,2,3,4\).

## 2. Algebraic incidence versus physical strategies

**Possible failure:** an uphill direction in the null-equation variety might not correspond to physical POVMs.

**Resolution:** Lemma 6.1 reconstructs Alice's effects, the steered Bob rank-one operators, the reduced state, Bob's POVMs, and the pure state from every nearby strict incidence point. The incidence model is locally physically complete.


## 2A. Global versus merely residual maximization

**Possible failure:** local POVM duality would be unjustified if the selected point maximized only over the residual parametrization rather than over all fixed-qubit POVM strategies.

**Resolution:** the nearest-point functional is first maximized over the full compact POVM set. Linearity removes shared randomness, and frozen dependency D3 supplies a residual component attaining that same full optimum. Therefore every local measurement is globally optimal with the other variables fixed, exactly as required for the dual-slack argument.

## 2B. Zero joint probabilities

**Possible failure:** an incidence tangent could leave the physical probability cone at a point where a joint probability vanishes.

**Resolution:** local reconstruction does not assume entrywise positivity. The null equations and positive marginals reconstruct future-null positive operators \(E_i,S_j\), and
\[
p_{ij}=\operatorname{Tr}(E_iS_j)\ge0.
\]
Hence every sufficiently small incidence curve is a genuine quantum curve even when some original joint probabilities are zero.

## 3. Smoothness at projected singularities

**Possible failure:** rank loss of the behavior Jacobian might invalidate multiplier or second-order arguments.

**Resolution:** the five null constraints have independent derivatives with respect to \(P\) because the matrices \(r_jr_j^T\) are linearly independent. The incidence space is smooth even when its projection to behavior space is singular. Every incidence tangent integrates to a physical curve.

## 4. Sign of determinant multipliers

**Possible failure:** equality constraints normally have unsigned multipliers.

**Resolution:** the signs come from the independent positive-semidefinite POVM dual slacks, not from an arbitrary equality-constraint convention. At a Bell maximum, \(\Gamma-K_j\ge0\) and annihilates the rank-one effect, so it is a nonnegative multiple of the adjugate. Under invertible steering this is exactly the determinant multiplier. A zero multiple gives a deterministic measurement with the same score, followed by a local/PVM realization; therefore a strict separator has all multipliers positive.

## 5. Hessian sign

**Possible failure:** the sign of the square-completion term was reversed in early scratch work.

**Resolution:** the frozen convention is

\[
c-\alpha uu^T=-\sum_j\lambda_j\nabla F_j,
\quad \lambda_j>0.
\]

Along a feasible curve,

\[
L_c''=\sum_j\lambda_jD^2F_j=2q(W).
\]

A local maximum therefore requires \(q\le0\). The proof finds \(q>0\) for rank at least two. The exact verifier checks the square-completion identity and its sign/order.

## 6. Normalization direction

**Possible failure:** the only positive direction might be radial and disappear after imposing \(u^TPu=1\).

**Resolution:** the radial matrix \(I\) is null and orthogonal to the entire compatible \(W\)-space. Adding a multiple of \(I\) changes normalization but leaves \(q\) and tangent compatibility unchanged. Every positive direction can therefore be normalized without losing positivity.

## 7. Generic-signature overclaim

**Earlier false conjecture:** the intrinsic constrained Hessian always has signature \((7,7)\).

**Countercheck:** exact/numerical Lorentz analysis showed signatures vary with the multiplier inertia before the strict KKT sign is imposed.

**Replacement theorem:** with \(\Lambda>0\), the ambient matrix form has exact inertia \((4,12)\). If `rank(D) >= 2`, the compatible subspace has dimension at least thirteen, too large to be nonpositive. This is both weaker and fully sufficient.

## 8. Rank-one singularities

**Possible failure:** a one-dimensional row span could admit mixed-sign rows and a positive dependence.

**Resolution:** the projective null-ray map is injective away from its five base rays. Thus all nonzero rows in a rank-one configuration would come from the same nonbase null ray. Since the five transformed outcome rays are distinct, only one row can be nonzero. Its kernel forces the corresponding multiplier coordinate to vanish.

All generic and exceptional fibers are covered: `x2=0`, `x3=0`, `x0=x1`, and `x2=x3`. Exact resultants are independently checked.

## 9. Rank-zero singularities

**Possible failure:** rank zero can have a semidefinite second form and might hide a separator.

**Resolution:** rank zero maps the transformed outcome pentad bijectively onto the five base rays. The unique signed circuit forces a partition-preserving permutation and equal scale. The behavior is a Lorentz Gram table. A bounded antisymmetric-flow construction gives an explicit deterministic local decomposition for every such table.

## 10. Boundary effects and repeated rays

**Possible failure:** the strict metric inequalities used in the fiber proof fail on the boundary.

**Resolution:** repeated rays, zero effects, ternary-to-binary degeneration, product states, and common operator spans are excluded from a strict residual separator by frozen dependency D3 and the one-binary-party theorem. They belong to the already simulated boundary. The closure argument uses strict inequalities only after entering the genuine residual stratum.

## 11. Shared randomness and stochastic postprocessing

**Possible failure:** the proof treats only one pure strategy.

**Resolution:** a linear Bell functional attains its maximum on one component of any shared-randomness mixture. Deterministic postprocessings remain PVMs after merging orthogonal projectors and inserting zeros; stochastic postprocessing is their convex hull. The final equality is between the stated convex hulls.

## 12. Arbitrary finite outputs

**Possible failure:** the proof directly treats only declared \((2,3)\)-by-\((2,3)\) outputs.

**Resolution:** D3 is precisely the frozen reduction from any arbitrary finite-output separator to this residual architecture. The closure theorem eliminates that final architecture.

## 13. Independent verifier boundary

The verifier does not “prove by testing.” It checks the nontrivial symbolic identities on which the human proof depends. The universal dimension and convexity steps are proved in text and do not reduce to finite samples.
