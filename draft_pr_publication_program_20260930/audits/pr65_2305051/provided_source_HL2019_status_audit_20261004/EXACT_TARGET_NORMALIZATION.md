# Exact Holland target from the cited 1999 theorem

This is the status family's independent deduction. It verifies the historical construction's exact target, not the candidate's four-adic proof.

The primary theorem is A. B. Aleksandrov, J. M. Anderson, A. Nicolau, *Inner functions, Bloch spaces and symmetric measures*, Proc. London Math. Soc. (3) 79 (1999), 318-352, Theorem 2 (printed p.320 / PDF p.3), proof printed pp.326-327 / PDF pp.9-10. The inspected author-hosted body is [here](https://mat.uab.cat/~artur/data/innerfunctions,blochspacesand.pdf), SHA-256 `479babf99aeaf1f58e6ee44590d29046bd54b98cfa9603d496812985bae6c7be`. Fresh retrieval matches the retained primary body byte-for-byte.

Fix any constant c>0 and use the gauge phi(t)=ct^2 on (0,1]. The theorem supplies an interpolating Blaschke product A such that

\[
 (1-|w|^2)|A'(w)|\le c(1-|A(w)|^2)^2\quad(w\in\mathbb D).
\]

The proof constructs A as a holomorphic universal covering onto D minus a countable set Lambda contained in D minus {0}, with no interior cluster points. Hence 0 lies in the covered domain, and there is a point a in D with A(a)=0. Let

\[
 \eta_a(z)=\frac{a+z}{1+\overline a z},\qquad B(z)=A(\eta_a(z)).
\]

The map eta_a is a disk automorphism, eta_a(0)=a, and

\[
 (1-|z|^2)|\eta_a'(z)|=1-|\eta_a(z)|^2.
\]

Consequently B(0)=0 and the chain rule gives

\[
 (1-|z|^2)|B'(z)|\le c(1-|B(z)|^2)^2.
\]

Precomposition preserves the covering onto the same domain. The purity argument in the cited proof applies to that covering directly: it is inner; a singular inner factor would produce a radial limit zero somewhere, which a covering of a neighborhood of the unomitted value zero cannot have. For the latter assertion, choose a simply connected neighborhood U of zero compactly contained in the covered domain. If B(r xi) tends to zero, the connected tail of that radial path lies in a single component V of B^{-1}(U). The covering maps V biholomorphically onto U; let g be that inverse. Then r xi=g(B(r xi)) tends to g(0) in D, contradicting r xi tending to the boundary point xi. Thus B is a pure Blaschke product. No good-Frostman-parameter selection is involved. The covering is nonconstant.

For every u in D,

\[
 \frac{1-|u|^2}{|1-u|}
 =\frac{(1-|u|)(1+|u|)}{|1-u|}\le1+|u|\le2.
\]

Since |B|<1, F=(1+B)/(1-B) is holomorphic in D, and therefore

\[
 \begin{aligned}
 (1-|z|^2)|F'(z)|
 &=\frac{2(1-|z|^2)|B'(z)|}{|1-B(z)|^2}\\
 &\le2c\left(\frac{1-|B(z)|^2}{|1-B(z)|}\right)^2
 \le8c.
 \end{aligned}
\]

This checks the exact normalization and Bloch conclusion. It also shows why a mere bound on B's hyperbolic derivative would be insufficient: the quadratic defect in the displayed numerator is what cancels the Cayley denominator.

B must be infinite. A nonconstant finite Blaschke product maps the unit circle onto itself and has nonzero angular phase derivative at any point mapped to 1. Its Cayley transform has a simple boundary pole there, causing (1-|z|^2)|F'(z)| to diverge along that radius. The proved bound excludes that possibility.

The same Cayley calculation for all rotations of the boundary value is already printed in the cited primary paper at pp.328-329 / PDF pp.11-12. The normalization above is recorded as a deduction, not falsely attributed as a separately stated Holland theorem in that paper. This construction reaches the exact requested mathematical object. It does not assert that the primary paper supplies the candidate's finite-algebraic algorithm or its compact convergence modulus.
