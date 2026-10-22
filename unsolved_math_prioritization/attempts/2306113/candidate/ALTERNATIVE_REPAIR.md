# The same witness also handles an inner-absolute-value repair

This supplement does not assert what the source intended. It proves that the exact F, L, g and positive rho in PROOF.md also violate the inclusion for the following separately specified neighborhood condition:

    |H'(z)-H(z)/z| + |H'(z)+|H(z)|/z| < 2 delta,
    H=g-f,  0<|z|<1.

At zero the expression extends continuously by zero for normalized differences. The proposed alternative replaces the second occurrence of h/z in the symmetric formula by |h|/z. Because the original printed formula has unmatched delimiters, the supplement rules out this particular alternative repair without claiming that it exhausts all conceivable readings.

Let H=-h/L and q(z)=H(z)/z, with the exact h,L of PROOF.md. Write H=sum_{n=2}^{10} d_n z^n, where all d_n are Gaussian rational. At z=r exp(i theta), define

    T(r,theta)=1/2 (|H'(z)-q(z)|
                  + |H'(z)+exp(-i theta)|q(z)||).

The identity |H(z)|/z=exp(-i theta)|q(z)| holds for r>0. Thus T is the required half-sum, continuously extended at r=0. It is not assumed to be subharmonic. A boundary-only maximum argument would not be justified here.

## Exact disk-covering method

For any R in [0,1], changes in r on [0,R] give a Lipschitz constant at most

    B_r(R)=sum_{n=2}^{10} n(n-1)(|Re d_n|+|Im d_n|) R^(n-2).

Changes in theta, at fixed r<=R, give a Lipschitz constant at most

    B_theta(R)=sum_{n=2}^{10}(n^2-n+1/2)
                               (|Re d_n|+|Im d_n|) R^(n-1).

These follow by applying the reverse triangle inequality separately to the two summands. For the second summand, the angular change of exp(-i theta)|q| is bounded by |q|+|q_theta|, and the radial change by |q_r|. For the first summand, the coefficient of H'-q is (n-1)d_n. Combining these estimates yields precisely the displayed constants. The formulas also give Lipschitz bounds across any zeros of q or either outer-modulus argument; differentiability of their absolute values at zero is not required.

Parameterize the circle by

    v(t)=((1-t^2)+2it)/(1+t^2),  -1<=t<=1,

and its negative. Together these parameterize the entire circle. Since |d theta/dt|<=2, the Lipschitz constant in t is bounded by

    B_t(R)=2 B_theta(R).

Start with the two closed rectangles [0,1] x [-1,1], one for each sign of v. For a rectangle [r0,r1] x [t0,t1], evaluate T at the exact rational midpoint. Add

    B_r(r1)(r1-r0)/2 + B_t(r1)(t1-t0)/2.                (A)

This is a rigorous upper bound for T everywhere in that rectangle, by first changing r and then t. The bound is valid on the closed rectangle, so overlapping edges or the multiply represented origin cause no coverage gap.

If the upper bound is below gamma=1000000/1002001, accept that rectangle. Otherwise bisect the coordinate contributing the larger term of (A), and inspect both children. This partitions each original rectangle. Acceptance occurs only after every leaf is certified; a node/depth budget is a rejection condition, never an acceptance condition.

## Exact modulus enclosure at a midpoint

At the midpoint, v,z,H',q are Gaussian rational. Choose Q to be an upward rational enclosure of |q| at denominator 10^10, using the same integer-square-root construction as in PROOF.md. Then

    0 <= Q-|q| < 10^(-10),

with a non-strict upper inequality sufficient as well. Replacing |q| by Q in the second outer-modulus argument changes that modulus by at most 10^(-10). Both remaining outer moduli are enclosed upward by exact integer-square-root calculations. Half their sum plus half this replacement error is consequently a valid upper bound for T at the midpoint. No floating-point quantity enters a decision.

## Verified result

The exact adaptive traversal in verify_alternative.py terminates after 4050 inspected rectangles, with 2026 accepted leaves and maximum depth 21. Every leaf's rational bound is strictly below gamma. ALTERNATIVE_RESULT.json records the exact smallest positive margin. Therefore T(r,theta)<gamma throughout the closed unit disk.

The same g consequently belongs to this alternative neighborhood at center z. F is still in S, and (g*F)(999/1000)=0 by the exact algebra in PROOF.md. Thus the inclusion fails under this repair too.

The supplement removes the distinction between these two explicit repairs as a possible escape for this witness. It does not supply a missing primary source or convert an inferred source correction into a verified historical definition.
