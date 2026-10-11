# Precision correction to the older equation (33) audit

This correction supplements the immutable completed equivalent-family report.
The primary K20 equation (33) asserts **norm** equalities. The family's plain
isometric-shift example distinguishes forward/reversed multiplier products,
but their global supremum norms coincide in that example. It alone falsifies
the implicit common-cocycle operator identification, not the printed norm
identity. The narrowed priority certificate remains independent of both.

An allowed broader module example does falsify the printed first norm equality.
Use scalar Linfinity({stable,unstable} x Z), with Stone measure-algebra module,
phi(n)=n-1, and T=M_b U. On the stable component take period-three weights
b=(1/4,1/2,3/4), and Ux(n)=c_n x(n-1), c=(4,1/4,1). On the unstable component
U is plain shift and b=2. U is similar to the plain shift via the bounded
invertible periodic multiplier h=(4,1,1), since c_n=h_n/h_(n-1). Its spectrum
lies on the unit circle, and it is a module d-isomorphism. Coordinate residue
partitions rule out periodic Stone points. The stable T^3 is (3/32) times the
three-step plain shift, so the stable spectrum lies strictly inside one;
the unstable spectrum is the circle of radius two. P1 is the genuine stable
spectral projection for r=1 and commutes with U and the multiplier algebra.

At exponent two, the actual multiplier of (b U^-1)^2 P1 has values
(1/2,3/32,3/16); the asserted b_2 U^-2 P1 has values (3/4,1/32,3/8), where
b_2=b(b o phi). Their operator norms are 1/2 and 3/4, respectively. This is
an exact rational counterexample to the printed norm identity under the
broader theorem's hypotheses, not a counterexample to its spectral conclusion.

The correct operator relation is

`(b U^-1)^n = U^(1-n) (b U)^n U^(-n-1)`.

It follows by shifting the forward product by -(n-1). When P1 commutes with
U, it gives a norm upper bound using both outer U factors. Their growth is
subexponential because sigma(U) lies on the unit circle; hence it can repair
the needed spectral-radius estimate. This audit therefore records a repairable
proof identity issue, **not** a disproved old theorem. The accepted sufficient
mechanism continues to use the directly proved one-direction transfer and
resolvent splitting, with scalar Theorem 2.26 as its only non-elementary input.
