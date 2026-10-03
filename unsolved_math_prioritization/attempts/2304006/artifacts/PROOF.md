# Hermite tetranomials: verified partial results and exact gap

**Problem 2304006 / AMR-022-4006. Overall verdict: unresolved in this work.**

Let the physicists' Hermite polynomials be defined by
\[
H_k(z)=(-1)^k e^{z^2}\frac{d^k}{dz^k}e^{-z^2},
\qquad P(z)=1+2z+aH_n(z)+bH_m(z),\quad 2\le n<m.
\]
The full question asks for one constant \(C<\infty\) that works for all integers
\(n,m\) and all complex \(a,b\), with at least one zero in
\(|\operatorname{Im}z|\le C\). Nothing below establishes that full statement or
constructs a counterexample to it. No novelty or priority is asserted for these
partial results.

## 1. Every real-coefficient instance has a real zero

Write \(d\gamma(x)=\pi^{-1/2}e^{-x^2}\,dx\). Repeated integration by parts in
Rodrigues' formula gives
\[
\int H_k(x)q(x)\,d\gamma(x)=0\qquad(\deg q<k).
\]
All boundary terms vanish because a polynomial times a Gaussian tends to zero.
Also \(\int x\,d\gamma=0\), \(\int x^2\,d\gamma=1/2\), and odd Gaussian moments
vanish.

Suppose first that \(a,b\in\mathbb R\) and \(n\ge3\). Then
\[
\int P\,d\gamma=1,\qquad
\int xP\,d\gamma=1,\qquad
\int x^2P\,d\gamma=\tfrac12,
\]
so
\[
\int (x-1)^2P(x)\,d\gamma(x)=-\tfrac12.
\]
If \(P\) had no real zero, continuity would give a constant sign; its positive
integral would force \(P>0\). The last displayed integral would then be positive,
a contradiction.

Now let \(n=2\). If \(m\) is odd and \(b\ne0\), \(P\) is a real odd-degree
polynomial and has a real zero. In every remaining case its odd part is \(2x\):
write \(P(x)=E(x)+2x\) with \(E\) even. A zero-free real \(P\) would again be
positive. Positivity of both \(P(x)\) and \(P(-x)\) forces
\(E(x)>2|x|\). But
\[
1=\int E\,d\gamma>2\int|x|\,d\gamma=2/\sqrt\pi>1,
\]
a contradiction. This includes \(a=0\), \(b=0\), and all possible degree drops.

The same argument applies to \(\operatorname{Re}P\) for any complex \(a,b\).
A real zero of \(\operatorname{Re}P\) is not a zero of \(P\), however. The exact
triple-zero construction in `CUBIC_SUBCASE.md` demonstrates the obstruction.

## 2. Two rigorous perturbative regions

These sufficient conditions give actual zeros, but their union has not been
shown to cover the coefficient plane uniformly in the degrees.

For \(r>0\), the derivative identity \(H_k^{(j)}=2^j k!H_{k-j}/(k-j)!\) gives
on \(|z+1/2|=r\)
\[
|H_k(z)|\le M_k(r):=\sum_{j=0}^k\binom{k}{j}(2r)^j|H_{k-j}(-1/2)|.
\]
Consequently
\[
|a|M_n(r)+|b|M_m(r)<2r                                      \tag{2.1}
\]
implies, by Rouché's theorem, that \(P\) has exactly one zero in
\(|z+1/2|<r\), counted with multiplicity. This is an exact symbolic sufficient
condition, not a sampled-circle test.

The standard fact that Hm has m distinct real zeros also follows from the same
orthogonality: if it had fewer than m sign changes on the real line, multiplying
by the product of its sign-changing real factors would give a nonzero integrand
of constant sign and multiplier degree less than m, contradicting orthogonality.
There are therefore m distinct real roots, accounting for the whole degree.

For a complementary dominant-term region, let \(x_1,\ldots,x_m\) be the distinct
real zeros of \(H_m\), fix \(i\), and take
\(0<\rho<\min_{j\ne i}|x_i-x_j|\). Define
\[
L=2^m\rho\prod_{j\ne i}(|x_i-x_j|-\rho)>0,
\quad R=|x_i|+\rho,
\quad B_n(R)=n!\sum_{j=0}^{\lfloor n/2\rfloor}
 \frac{(2R)^{n-2j}}{j!(n-2j)!}.
\]
The Hermite product and coefficient formulas show that on \(|z-x_i|=\rho\),
\(|H_m(z)|\ge L\), \(|H_n(z)|\le B_n(R)\), and \(|1+2z|\le1+2R\).
Thus
\[
|b|L>|a|B_n(R)+1+2R                                      \tag{2.2}
\]
puts exactly one zero of \(P\) in that disk, by Rouché. An analogous criterion
holds after exchanging the two high terms and choosing a zero of \(H_n\).

The classical one-high-term proof uses two regions whose thresholds overlap.
In the two-high-term problem cancellation is a real additional issue: at any
point \(z_0\) with \(H_m(z_0)\ne0\), taking
\(b=-aH_n(z_0)/H_m(z_0)\) makes the high-term sum vanish at \(z_0\), however
large \(|a|\) is. This does not rule out better contours or a solution; it prevents
using an unsupported lower bound on that sum in the one-term proof.

## 3. Hermite differential elimination and its missing implication

Set \(L=D^2-2zD\). The defining differential equation is \(LH_k=-2kH_k\).
Directly applying the commuting operators gives
\[
(L+2n)(L+2m)P=4nm+8(n-1)(m-1)z.                         \tag{3.1}
\]
It is tempting to transfer the real zero of the right side back to a nearby
zero of \(P\). No degree-independent zero-transfer theorem adequate for that
step is proved here. Ordinary Gauss–Lucas supplies no converse: for
\(Q(z)=z^2+T^2\), \(Q'\) has the real zero 0 while both zeros of \(Q\) have
imaginary distance \(T\), with \(T\) arbitrary. This example is not in the target
family and is not a disproof of a special Hermite-operator theorem. It specifies
why derivative-zero information alone does not close (3.1).

## 4. Sharp complex cubic subcase

For \(n=2,m=3\), the exact best half-width is
\[
C_3=\frac{\sqrt3}{2}\sqrt{1+u^2}=0.903669\ldots,
\qquad 4u^3+3u-1=0,\quad u>0.
\]
The full proof, the half-plane coincidence input, and an exact attaining
triple-zero construction are in `CUBIC_SUBCASE.md`. In particular any constant
that answers the full question affirmatively must satisfy \(C\ge C_3\).
A lower bound on a possible constant is not a counterexample to its existence.

## 5. Uniformity for any fixed finite degree range

For each fixed pair \(n,m\) there is a finite radius \(R_{n,m}\) such that every
\(P\) has a zero in \(|z|\le R_{n,m}\), uniformly over complex \(a,b\).

Otherwise choose \((a_j,b_j)\) so that every zero has modulus greater than \(j\).
Divide by \(t_j=\max(1,|a_j|,|b_j|)\). Along a subsequence the bounded vectors
\((1/t_j,a_j/t_j,b_j/t_j)\) converge to \((\lambda,\alpha,\beta)\), with maximum
absolute coordinate 1. The normalized polynomials converge locally uniformly to
\[
Q(z)=\lambda(1+2z)+\alpha H_n(z)+\beta H_m(z).
\]
This limit is nonconstant: if \(\beta\ne0\) it has degree \(m\); if
\(\beta=0,\alpha\ne0\) it has degree \(n\); otherwise \(\lambda\ne0\) and it
has degree 1. Choose a zero \(\zeta\) of \(Q\) and a small circle about it on
which \(Q\) is nonzero. Local uniform convergence and Rouché force a zero of
the normalized \(P_j\) in that fixed disk for all sufficiently large \(j\).
This contradicts the choice of \(P_j\).

Taking the maximum over finitely many pairs proves the same result for any fixed
bound on \(m\). This compactness proof does not bound \(R_{n,m}\) as \(m\to\infty\).
Thus any sequence disproving the strip conjecture must have unbounded highest
index. The reverse assertion, that no such sequence exists, remains unproved.

## Exact remaining gap

Let
\[
C_{n,m}=\sup_{a,b\in\mathbb C}\min_{P(z)=0}|\operatorname{Im}z|.
\]
The work proves \(C_{n,m}<\infty\) for every fixed pair and computes \(C_{2,3}\),
while the real-coefficient supremum is 0. The unanswered question is
\(\sup_{2\le n<m} C_{n,m}<\infty\). Neither a degree-independent upper bound
nor a sequence with \(C_{n,m}\to\infty\) has been obtained. The five attempts
therefore end with status **unsolved**, not with a solution claim.
