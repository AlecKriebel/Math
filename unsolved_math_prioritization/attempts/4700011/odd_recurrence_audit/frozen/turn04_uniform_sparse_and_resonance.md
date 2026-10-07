# Turn 4: uniform sparse-support classification and all-order obstructions

Problem 4700011, Gasull Problem 11. Authored 2026-10-07.

## Result and scope

This turn proves a classification in **every order** for candidates with at most two active variable terms in the reduced numerator. It also proves a parity-weight obstruction for rational-ratio coefficients, an algebraic-unit constraint from the second fixed point, and a cubic resonance obstruction valid in arbitrary order.

These are structural restrictions, not a sweep over additional finite orders. They do not classify arbitrary larger supports, so the original problem is not solved. No literature-novelty claim is made. Turns 1–3 are unchanged.

## 1. Normalization and spectral arithmetic

By Turn 1, every candidate other than an identity dilation has the form

\[
\tag{1}x_{n+k}=\frac{a_0+\sum_{j=1}^{k-1}a_jx_{n+j}}{x_n},
\qquad a_j\geq0,\quad a_j=a_{k-j}.
\]

Let \(q>0\) be its diagonal fixed point. Rescale by \(x_n=q y_n\) and put

\[
c_0=a_0/q^2,\qquad c_j=a_j/q,\qquad
s=\sum_{j=1}^{k-1}c_j=1-c_0\leq1.
\]

The normalized fixed point is \((1,\ldots,1)\), and its derivative has characteristic polynomial

\[
\tag{2}P(z)=z^k-\sum_{j=1}^{k-1}c_jz^j+1.
\]

If the map has finite order, its companion derivative has finite order. Therefore all roots of \(P\) are roots of unity, and they are simple: the minimal polynomial of a companion matrix is its characteristic polynomial, whereas a finite-order matrix in characteristic zero has squarefree minimal polynomial.

Each \(c_j\) is an algebraic integer, as an elementary symmetric function of roots of unity. The coefficients are real and lie in a cyclotomic field, hence are totally real. Under every embedding of their coefficient field, the conjugate polynomial still has roots of unity.

## 2. A small algebraic-integer lemma

**Lemma 1.** If a totally real algebraic integer \(u\) has every conjugate in \([-2,2]\), then

\[
u=\zeta+\zeta^{-1}
\]

for a root of unity \(\zeta\).

*Proof.* A root \(w\) of \(w^2-u w+1=0\) is an algebraic integer. Every conjugate of \(w\) solves the corresponding quadratic for a real conjugate of \(u\) in \([-2,2]\), so every conjugate of \(w\) has modulus one.

Here is the needed elementary form of Kronecker's argument. If the conjugates of \(w\) are \(w_1,\ldots,w_d\), the polynomials

\[
Q_n(X)=\prod_{i=1}^d(X-w_i^n),\qquad n\geq1,
\]

have integer coefficients: their coefficients are algebraic integers fixed by every automorphism of a normal closure. Their coefficient magnitudes are bounded by the corresponding binomial coefficients because \(|w_i|=1\). Only finitely many such integer polynomials exist. Consequently the values \(w^n\) lie in the finite union of their root sets. Two positive powers agree, so \(w\) is a root of unity. Taking \(\zeta=w\) proves the claim. \(\square\)

## 3. A uniform parity-weight obstruction

Assume the positive variable coefficients have rational ratios. Then there are relatively prime nonnegative integers \(m_j\), not all zero, and \(\tau>0\) such that

\[
c_j=m_j\tau.
\]

Set

\[
N=\sum_jm_j,\qquad
O=\sum_{j\text{ odd}}m_j,\qquad
E=\sum_{j\text{ even}}m_j,\qquad D=O-E.
\]

Here \(N\tau=s\leq1\). Since the positive \(m_j\) have greatest common divisor 1, Bézout's identity expresses \(\tau\) as an integer linear combination of the algebraic integers \(c_j\). Thus \(\tau\) is a totally real algebraic integer.

**Theorem 2.** In even order, if \(N\geq2\), global periodicity forces

\[
\tag{3}O\leq E.
\]

Equivalently, for a rational-ratio numerator with at least two active variable terms, the total weight on odd lags cannot exceed the total weight on even lags.

*Proof.* Let \(\sigma\) be any embedding of the coefficient field. The monic even-degree polynomial

\[
P_\sigma(z)=z^k-\sigma(\tau)\sum_jm_jz^j+1
\]

has all roots on the unit circle. Neither \(+1\) nor \(-1\) can be a root: before conjugation, both values of \(P\) are at least \(2-s\geq1\), and an embedding cannot map a nonzero algebraic number to zero. Pairing the nonreal conjugate roots gives

\[
P_\sigma(1)>0,\qquad P_\sigma(-1)>0.
\]

Hence

\[
2-N\sigma(\tau)>0,\qquad
2+D\sigma(\tau)>0.
\]

Suppose \(D>0\). Because \(D\) is an integer, \(D\geq1\), and every conjugate satisfies

\[
\tag{4}-2\leq-\frac2D<\sigma(\tau)<\frac2N\leq1.
\]

Lemma 1 gives \(\tau=\zeta+\zeta^{-1}\). Let \(n\) be the order of \(\zeta\). If \(n\geq7\), one algebraic conjugate of \(\tau\) is \(2\cos(2\pi/n)>1\), contradicting (4). For \(n\leq6\), the only positive possibilities are \(2\), \(1\), and \((\sqrt5-1)/2\); each is greater than \(1/2\). But \(0<\tau\leq1/N\leq1/2\). The remaining possibilities are zero or negative. This contradiction proves \(D\leq0\). \(\square\)

**Corollary 3.** In even order, a rational-ratio candidate whose active variable lags are all odd has only one active variable term. By symmetry, that term is at the midpoint.

*Proof.* With all lags odd, \(D=N>0\), so Theorem 2 excludes \(N\geq2\). Therefore \(N=1\), which gives exactly one active coefficient. Symmetry forces its lag to equal \(k/2\). \(\square\)

These statements can also be applied after removing any common index dilation. Thus a potential new rational-ratio example of primitive even order, with multiple active terms, must involve both odd and even lags, with even total weight at least odd total weight.

## 4. Complete classification with at most two active variable terms

**Theorem 4.** In arbitrary order, every globally periodic recurrence in the original family whose reduced form (1) has at most two active variable terms belongs to the five classical rescaling/index-dilation families.

*Proof.* An empty variable support gives \(x_{n+k}=a_0/x_n\), the reciprocal dilation. The increasing branch was already proved to be an identity dilation in Turn 1.

With one active lag, symmetry forces \(k=2\ell\) and lag \(\ell\). Writing its coefficient as \(b>0\), the recurrence is

\[
x_{n+2\ell}=\frac{a_0+b x_{n+\ell}}{x_n}.
\]

The residue classes modulo \(\ell\) are independent order-two recurrences. Turn 2's boundary-return proof forces \(a_0=0\) or \(a_0=b^2\), yielding the six- or five-period classical base map.

Now suppose exactly two lags are active. They are a reflected pair \(j,k-j\), with equal coefficient \(b>0\), and \(j\ne k/2\). Let

\[
g=\gcd(k,j),\qquad K=k/g,\qquad r=j/g.
\]

The recurrence splits into \(g\) independent recurrences of order \(K\), with active lags \(r,K-r\); \(\gcd(K,r)=1\). Global periodicity of the original map forces that of this lower-order map, since a suitable power of the original shift acts independently on the residue classes and their initial data can be varied freely.

If \(K\) is even, both \(r\) and \(K-r\) are odd. Their coefficient ratio is 1, so Corollary 3 excludes the two-term support.

If \(K\) is odd, Turn 1's proved rational-ratio classification applies. It forces lags \(K/3,2K/3\) and constant coefficient \(b^2\). Coprimality then forces \(K=3\), so the original lags are \(k/3,2k/3\). This is exactly the third-order eight-period Lyness dilation. \(\square\)

Consequently any genuinely new example must have at least three active variable terms. In odd order symmetry makes the number of active terms even, so a new odd-order example would require at least four, together with irrational coefficient ratios by Turn 1.

**Corollary 5 (equal full numerator).** For \(b>0\), the full-support recurrence

\[
x_{n+k}=\frac{a_0+b\sum_{j=1}^{k-1}x_{n+j}}{x_n}
\]

is not globally periodic for any \(k\geq4\).

*Proof.* For even \(k\geq4\), primitive weights are all 1, so \(N=k-1\geq3\) and \(O-E=1\), contradicting Theorem 2. For odd \(k\geq5\), Turn 1's rational-ratio classification permits only a reflected pair at one-third/two-thirds, not the full support of at least four terms. \(\square\)

This is an independently proved subfamily result, not a novelty assertion about the generalized Lyness literature.

## 5. The negative fixed point gives an algebraic-unit constraint

**Theorem 6.** If \(c_0>0\), global periodicity forces the normalized constant coefficient \(c_0\) to be an algebraic unit. Moreover, both \(c_j\) and \(c_j/c_0\) are totally real algebraic integers.

*Proof.* The normalized recurrence has a second diagonal fixed point \((-c_0,\ldots,-c_0)\): its scalar fixed-point equation is

\[
r^2-sr-c_0=(r-1)(r+c_0)=0.
\]

Although this fixed point is outside the positive orthant, it is legitimate to use it. A rational identity \(F^p=\mathrm{id}\) holding on the positive open set is an identity of rational functions. The map and all iterates are defined at this fixed point because \(c_0>0\) and it remains fixed. Thus its derivative also has finite order.

The characteristic polynomial there is

\[
z^k+\sum_{j=1}^{k-1}\frac{c_j}{c_0}z^j+1.
\]

Its roots are roots of unity, so each \(c_j/c_0\) is a totally real algebraic integer. The same was already proved for \(c_j\) at the positive fixed point. Consequently

\[
c_0=1-\sum_jc_j
\]

is an algebraic integer, and so is

\[
\frac1{c_0}=1+\sum_j\frac{c_j}{c_0}.
\]

This is exactly the assertion that \(c_0\) is an algebraic unit. \(\square\)

In particular, a nonconstant inhomogeneous globally periodic map cannot have all of its fixed-point-normalized coefficients rational: a rational algebraic integer \(c_0\) cannot lie strictly between 0 and 1. This statement concerns normalized coefficients; it does not exclude the usual examples with rational coefficients before rescaling.

## 6. There are no quadratic spectral resonances

**Lemma 7.** Suppose (2) has all its roots on the unit circle, with \(c_j\geq0\) and \(s\leq1\). No product of two roots of \(P\) is another root of \(P\).

*Proof.* For a root \(\zeta\), put \(t=\zeta^k\). Then

\[
|1+t|=\left|\sum_jc_j\zeta^j\right|\leq s\leq1.
\]

Hence the argument of \(t\) lies in the closed arc \([2\pi/3,4\pi/3]\). If roots \(\zeta,\eta,\xi\) satisfied \(\xi=\zeta\eta\), their \(k\)-th powers \(t,u,tu\) would all lie in that arc. Adding the two arc arguments shows that this is possible only at its endpoints:

\[
t=u=\omega,\quad tu=\omega^2,
\]

or the complex conjugate case, where \(\omega=e^{2\pi i/3}\).

Equality in the preceding triangle inequality then forces \(s=1\) and, for every active lag \(j\),

\[
\zeta^j=\eta^j=1+\omega.
\]

Therefore \(\xi^j=(1+\omega)^2=\omega\), so \(\sum_jc_j\xi^j=\omega\). But the root equation for \(\xi\) requires that sum to be \(1+\omega^2=-\omega\), a contradiction. \(\square\)

In particular, \(P(1)>0\) and \(P(\zeta^2)\ne0\) for every root \(\zeta\). The nonresonance is a consequence of the positive-coefficient spectral geometry; it is not an extra assumption.

## 7. An all-order cubic divisibility obstruction

Define

\[
\tag{5}
G(z)=(2-s)z^k(z^{3k}+1)
+P(z^2)(z^{2k}+1)(z^k+1).
\]

**Theorem 8.** Every globally periodic candidate in the normalized decreasing family satisfies

\[
\tag{6}P(z)\mid G(z).
\]

*Proof.* Near the positive fixed point, write \(y_n=1+u_n\). The recurrence becomes exactly

\[
\tag{7}
u_{n+k}+u_n-\sum_jc_j u_{n+j}=-u_nu_{n+k}.
\]

A finite-order analytic map is locally analytically conjugate to its derivative. One can verify this directly by averaging: if \(F^p=\mathrm{id}\) and \(D=DF(0)\), then

\[
h(x)=p^{-1}\sum_{j=0}^{p-1}D^{-j}F^j(x)
\]

has derivative \(I\) at zero and satisfies \(h\circ F=D\circ h\). Complexifying the local analytic identities is legitimate because the rational denominator is nonzero at the fixed point.

Take a nonreal eigenvalue \(\zeta\), together with its inverse \(\zeta^{-1}\). In linearizing coordinates, choose amplitudes \(a,b\) so that the first-order scalar terms are \(a\zeta^n+b\zeta^{-n}\). Since the companion matrix has simple eigenvalues, its eigenvectors can be normalized to have first coordinate 1. Lemma 7 ensures all quadratic denominators below are nonzero.

The degree-two part forced by (7) has the form

\[
U a^2\zeta^{2n}+Vab+Wb^2\zeta^{-2n},
\]

where

\[
\tag{8}
U=-\frac{\zeta^k}{P(\zeta^2)},\qquad
V=-\frac{\zeta^k+\zeta^{-k}}{P(1)}.
\]

At degree three, the monomial \(a^2b\) has frequency \(\zeta\), so its linear left side in (7) vanishes. Its right-side coefficient must consequently satisfy

\[
\tag{9}
U(\zeta^{2k}+\zeta^{-k})+V(1+\zeta^k)=0.
\]

Insert (8), multiply by the nonzero denominators and by \(\zeta^k\), and use \(P(1)=2-s\). The resulting equation is exactly \(G(\zeta)=0\).

The root \(+1\) never occurs. The only possible real root is \(-1\), occurring only in odd order; then \(\zeta^k=-1\), and (5) gives \(G(-1)=0\) directly. Thus \(G\) vanishes at every root of \(P\). The roots are simple, so \(P\) divides \(G\). \(\square\)

This criterion does not require guessing the global period, and it applies in both even and odd orders. Its coefficients are explicit polynomial expressions in the normalized parameters.

### A nonnegative variance consequence

Let \(\zeta=e^{i\theta}\) be a root with \(\zeta^k\ne-1\), and assume \(s>0\). Put

\[
v=\cos(k\theta),\qquad
X_j=\cos((j-k/2)\theta).
\]

The root equation and coefficient symmetry give

\[
\sum_jc_jX_j=2\cos(k\theta/2),\qquad -1<v\leq-1/2.
\]

Dividing the cubic identity by its nonzero factor \(\zeta^k+1\), and taking its real form, gives

\[
\sum_jc_jX_j^2=v+1-\frac{2-s}{4v}.
\]

Therefore the weighted variance is exactly

\[
\tag{10}
\sum_jc_j\left(X_j-\frac{2\cos(k\theta/2)}s\right)^2
=\frac{2-s}{-4sv}\big(s+4v(v+1)\big).
\]

Its nonnegativity yields the necessary inequality

\[
\tag{11}s\geq-4v(v+1).
\]

The identity is potentially useful for larger supports because the left side records the dispersion of the active lag phases. No argument making it vanish for arbitrary supports has been established here.

## 8. Exact checks and a failed sufficiency route

The verifier symbolically derives the cubic coefficient, checks (10), and tests all four decreasing classical families through several index dilations. These are consistency checks; Theorems 2, 4, 6, and 8 are proved above without extrapolating from a finite search.

For order two, with \(P(z)=z^2-cz+1\), the greatest common divisor of **all** remainder coefficients of \(G\) modulo \(P\) is

\[
c(c-2)(c-1)(c^2+c-1).
\]

On \(0\leq c\leq1\), the surviving values are exactly \(0\), \(1\), and \((\sqrt5-1)/2\), matching the reciprocal, six-period, and five-period families.

However, the cubic test does not by itself classify all orders. In order three, with equal coefficients \(c\), the corresponding gcd is

\[
c(c-1)(c^2+2c-1)(c^3+4c^2+2c-2).
\]

The last factor has a root \(\rho\in(12/25,49/100)\), so it produces positive normalized coefficients with \(2\rho<1\). Its polynomial

\[
P(z)=(z+1)(z^2-(\rho+1)z+1)
\]

has all roots on the unit circle and passes the cubic divisibility test. Nevertheless it is not a finite-order spectrum: the irreducible polynomial of \(\rho\) also has a conjugate in \((-4,-3)\), and the corresponding quadratic factor then has roots off the unit circle. Roots of unity cannot acquire such conjugates. This exact control prevents treating circle-valued eigenvalues plus one resonant identity as sufficient.

An attempted route to full classification through the nonnegative variance (10) likewise stops at a real gap: nonnegativity proves (11), but does not force equality for an arbitrary larger support. Assuming that all active lag phases coincide would be unjustified.

## 9. Remaining possibilities after four author turns

Every genuinely new example would now have to evade all of the following proved restrictions:

- The surjectivity reduction and palindromic coefficients from Turn 1.
- At least three active variable terms; at least four in odd order.
- Irrational variable-coefficient ratios in odd order, and the finite cyclotomic factor list of Turn 3.
- For a multiple-term rational-ratio candidate of primitive even order, both lag parities must occur and the even total weight must be at least the odd total weight.
- If inhomogeneous, a positive algebraic-unit normalized constant coefficient and finite-order spectra at both diagonal fixed points.
- The all-order cubic divisibility identity (6), as well as the full nonlinear periodicity identity.

These restrictions are substantial but do not eliminate every larger support. The original arbitrary-order problem remains unresolved in this work. A fifth substantive attempt should target the surviving mixed-parity even supports or seek a uniform arithmetic elimination of the odd spectral factors; it should not replace that gap with a finite-order guess.

## Source context

The original problem is Gasull's Problem 11 in *Some open problems in low dimensional dynamical systems*, Section 2.8: https://arxiv.org/abs/2012.02524 . The proofs here are independently authored, with no claim that their subfamily conclusions are absent from earlier literature.
