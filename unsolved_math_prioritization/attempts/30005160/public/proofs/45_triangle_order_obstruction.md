# Proof 45  A strict triangle obstruction to a stronger convex order

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

This is an auxiliary convex-order obstruction, not a counterexample to the cubic power-majorant comparison for 4<p<6.

Take a=1/2, b=3/4, c=1. These amplitudes satisfy all three strict triangle inequalities. With x=cos(theta), put U=|a+bz+cz^3|^2 and V=|a+bz-cz^3|^2. Direct factorization gives

U=(x-1/4)^2(4x+5),
V=1/16+(1-x)(16x^2+28x+13)/4.

The quadratic in V is everywhere positive because its leading coefficient is positive and its discriminant is -48. Thus V>=1/16 on the circle, whereas U vanishes at x=1/4.

The first two moments of U and V coincide. Indeed E U=E V=a^2+b^2+c^2, and E U^2=E V^2=(a^2+b^2+c^2)^2+2(a^2b^2+a^2c^2+b^2c^2), since the nonzero Fourier frequencies 1,2,3 are distinct.

Set t=1/32. Since V>t everywhere,

E(U-t)_+^2 - E(V-t)_+^2
 = E(U-t)^2 - E(V-t)^2 - E(t-U)_+^2
 = -E(t-U)_+^2 < 0.

Strictness follows because U is continuous and zero at a point, so U<t on a nonempty open arc of positive circle measure. Therefore third-order convex ordering fails even in the strict triangle region. Any proof using this stronger order needs a different, weaker integrated comparison. This obstruction does not determine the sign of D_q for 2<q<3.
