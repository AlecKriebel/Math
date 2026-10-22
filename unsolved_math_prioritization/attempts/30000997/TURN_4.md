# Author turn 4 — a finite exact witness and a product obstruction

2026-10-03 06:42 UTC. Partial result. The full manifold implication remains unresolved; completion estimate stays 10%.

## No asymptotic or numerical sign is needed

Specialize the compact sphere of turn 2 to a=1/10, choose equatorial source p=(0,0), and target q=(0,π/2). The pair is uniquely minimizing and nonconjugate by the metric-comparison argument of turn 3. Set e1=∂x, e2=∂y at p and v=(π/2)e2.

The exact integrals at r=π/2 are h=0, I0=1/2, I1=1/8. With κ=−12/5, the full tensor on u=w=e1 is

S(v;e1,e1)=7/10−8/π²<0.

The inequality is elementary: π²<10 gives 8/π²>4/5>7/10. The original endpoint tangent is Dexp_p(v)e1=(2/π)∂x at q, not ∂x itself; this normalization is part of the stated witness.

For every normalized orthogonal pair u=(cosθ,sinθ), w=(−sinθ,cosθ), the same tensor is

2cos⁴θ+(8/π²)sin⁴θ+(47/10−24/π²)cos²θ sin²θ.

All coefficients are positive: π²>9 implies 47/10−24/π²>47/10−8/3>0. Thus the null-pair positivity and the full-pair negativity at this one non-diagonal squared-distance point are completely explicit. Smoothness and compactness of the normalized null-pair set imply a product neighborhood of (p,q) with strict A3w and negative full curvature somewhere. This strengthens the local interpretation result without claiming global A3w.

## A product does not repair the missing antecedent

For a product M×R with squared-distance cost, the cost is the sum of factor costs and the MTW tensor is additive. In the tangent representation its null condition is

g_M(u,w)+αβ=0.

If the M tensor has any negative full pair (u,w), take α=1 and β=−g_M(u,w). This produces a null pair in M×R with the same negative MTW value. Conversely, if M is NNCC, then its product with the flat line is NNCC and hence A3w. Therefore

M×R is A3w iff M is NNCC.

The forward direction is a local algebraic argument on the whole off-cut product; the reverse follows by additivity. This product principle is prior art: see Kim–McCann, *Towards the smoothness of optimal maps on Riemannian submersions and Riemannian products*, Theorem 1.2 (especially the failure of A3w if a factor is not nonnegatively cross-curved). It is recorded here as a diagnostic, not a novel result.

For the exact sphere witness, lift e1 to (e1,1) and (e1,−1) at source tangent v=(π/2)e2 with zero line displacement. Their dot product is zero; the product tensor is still 7/10−8/π². Replacing R by a flat circle and using a sufficiently small circle displacement gives a compact product witness as well. Thus a flat-factor construction cannot turn the candidate sphere into an A3w counterexample; it automatically destroys A3w.

The universal conjecture can equivalently be viewed as asking whether A3w is preserved when any global-A3w manifold is multiplied by a flat line. Invoking such stability without proof would assume the requested conclusion.

## Numerical negatives rejected as evidence

The refinement file records a coarse negative value at source latitude 0.5 becoming positive as the difference step decreases. For each of the two most negative latitude-0.25 examples, a separate geodesic shooting experiment found a numerically shorter competing geodesic to the same endpoint (length about 2.99967 or 2.99969 versus 3). These computations are not validated interval certificates. They nevertheless invalidate treating the original coarse negatives as certified pre-cut violations and identify the exact missing condition: a Jacobi denominator is not a minimization certificate.

No numerical sign, shorter-path claim, or cut-locus location is promoted to a theorem. The exact finite witness and equatorial positivity above do not rely on these computations.
