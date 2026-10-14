# Proof 22  A dominant constant region on the cubic support

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

Let q = p/2 lie in (2,3), let a,b,c >= 0, and put

D_q(a,b,c) = integral_T |a+bz+cz^3|^(2q) - integral_T |a+bz-cz^3|^(2q).

## Lemma

If a >= b+c, then

D_q(a,b,c) >= 4 q binom(q,3) a^(2q-4) b^3 c
  [1 - ((q-1)(3-q)/4) (b^2+2c^2)/a^2] >= 0.

If a,b,c are positive, the first displayed right-hand side is positive.

## Proof

The case a=0 is trivial. Expand

(a+bz+cz^3)^q = sum_(j>=0) binom(q,j) a^(q-j) (bz+cz^3)^j.

For a >= b+c, this converges absolutely and uniformly on the unit circle; the boundary case is allowed because sum_j |binom(q,j)| is finite. Multiplying by the conjugate expansion and integrating is therefore legitimate, including at boundary zeros.

In the j-th and l-th blocks, a resonance has the form

j+2k = l+2h,

where k and h count occurrences of c. Consequently j and l have the same parity. Passing from c to -c changes the resonant contribution exactly when k+h is odd.

For q in (2,3), binom(q,j) is positive for every odd j; it is positive for j=0,2, and negative for every even j>=4. Thus a negative sign-changing resonant contribution can only pair j=2 with an even l>=4 (or vice versa). Since the j=2 block has degree at most 6, necessarily l=4 or l=6. The l=6 resonance has k=2,h=0, so k+h is even and does not contribute to D_q. With l=4 the only sign-changing resonances are

- 2bc z^4 paired with b^4 z^4;
- c^2 z^6 paired with 4b^3 c z^6.

Their combined contribution to D_q is

4 binom(q,2) binom(q,4) a^(2q-6) (2 b^5 c + 4 b^3 c^3).

All remaining sign-changing resonant contributions are nonnegative. In particular, j=1 paired with l=3 includes c z^3 paired with b^3 z^3 and contributes

4 q binom(q,3) a^(2q-4) b^3 c.

Keeping this positive term and the complete list of negative terms gives the claimed first inequality, since binom(q,4)/binom(q,3)=(q-3)/4 and binom(q,2)=q(q-1)/2.

Finally, (q-1)(3-q)<1 for q in (2,3), while b^2+2c^2 <= 2(b+c)^2 <= 2a^2. The bracket is therefore strictly greater than 1/2. This proves the lemma.

## Scope and unresolved obstruction

For real coefficients on this support, the sign of a can be removed by combining z -> -z with multiplication by -1. Simultaneously flipping b and c is also norm-preserving, so the displayed D_q is the only nontrivial fixed-magnitude sign comparison.

The proof above covers only a >= b+c. The other two dominant cones are proved in [Proof 26](26_cubic_high_cone.md) and [Proof 34](34_cubic_middle_cone.md). The general strict-triangle region remains unresolved, with symmetric and nearby boxes covered by [Proof 38](38_cubic_symmetric_slice.md). Expanding around c changes the support to {0,2,3}; the formerly finite list of negative terms becomes an infinite tail. Expanding around b also produces an infinite negative family. No valid analytic-continuation argument transfers the positive termwise conclusion past a=b+c.
