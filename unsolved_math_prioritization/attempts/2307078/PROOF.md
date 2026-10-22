# Rubel planar equilibrium problem and its established resolution

## Result and attribution

The answer to the existence question in Problem 7.78 of *Research Problems in Function Theory* is negative in the complex plane. Every sequence in the question produces infinitely many equilibrium points away from the charges.

This is an established result, explicitly stated for distinct points with unit charges by J. Clunie, A. Eremenko and J. Rossi in *On equilibrium points of logarithmic and Newtonian potentials*, Journal of the London Mathematical Society (2) 47 (1993), 309-320, printed p. 310, in the paragraph immediately preceding Theorem 2.1. The present proof supplies the elementary details of that particular case. It makes no novelty claim and does not reproduce the paper's more general theorems.

Primary source: [Clunie, Eremenko and Rossi, author-hosted paper](https://www.math.purdue.edu/~eremenko/dvi/cer.pdf). Bibliographic DOI: [10.1112/jlms/s2-47.2.309](https://doi.org/10.1112/jlms/s2-47.2.309).

The original statement appears on printed pp. 185-186 of Walter K. Hayman and Eleanor F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2 (2018). Update 7.78 on printed p. 186 already credits the planar resolution to those authors. See [the versioned source](https://arxiv.org/abs/1809.07200v2).

## Exact theorem

Let \((z_n)_{n\geq1}\) be an infinite sequence of pairwise distinct nonzero complex numbers satisfying

\[
\sum_{n=1}^{\infty}\frac{1}{|z_n|}<\infty.
\]

Then

\[
S(z)=\sum_{n=1}^{\infty}\frac{1}{z-z_n}
\]

defines a meromorphic function on \(\mathbb C\), with simple poles of residue one precisely at the points \(z_n\), and has infinitely many distinct zeros in \(\mathbb C\setminus\{z_n:n\geq1\}\).

The original reciprocal-modulus condition already excludes zero among the \(z_n\). Its nonvanishing condition is understood on the complement of the poles, equivalently as zero-freeness of the resulting meromorphic function.

## Convergence and the product

The summability condition implies \(|z_n|\to\infty\): otherwise infinitely many terms of the positive series would be bounded below by a fixed positive number. In particular the set of charge locations has no finite accumulation point.

Fix \(R>0\). If \(|z_n|>2R\) and \(|z|\leq R\), then

\[
\left|\frac{1}{z-z_n}\right|\leq \frac{2}{|z_n|}.
\]

The tail of the series for \(S\) therefore converges absolutely and uniformly on this disk. Including the finitely many remaining terms gives local uniform convergence off the poles. In a small disk about any \(z_k\), all terms except the \(k\)-th have a holomorphic sum; thus \(S(z)-(z-z_k)^{-1}\) is holomorphic there. This proves the claimed poles and residues.

Consider the genus-zero product

\[
F(z)=\prod_{n=1}^{\infty}\left(1-\frac{z}{z_n}\right).
\]

For the same tail, use the analytic power-series branch

\[
\ell_n(z)=\log(1-z/z_n)
          =-\sum_{j\geq1}\frac{(z/z_n)^j}{j}.
\]

For \(|z|\leq R\) and \(|z_n|>2R\),

\[
|\ell_n(z)|\leq\frac{|z|/|z_n|}{1-|z|/|z_n|}
\leq\frac{2R}{|z_n|}.
\]

The logarithmic tail is locally uniformly convergent and analytic, so its exponential is a holomorphic, nonzero tail product. The finite head then shows that \(F\) is entire, that \(F(0)=1\), and that its zeros are exactly the \(z_n\). Each zero is simple: near \(z_k\), write \(F(z)=(1-z/z_k)Q_k(z)\), where \(Q_k\) is holomorphic and nonzero at \(z_k\). Hence \(F'(z_k)=-Q_k(z_k)/z_k\ne0\). The infinite set of zeros ensures that \(F\) is not a polynomial.

Differentiation of the normally convergent analytic logarithmic tail is legitimate on every smaller compact disk. Its derivative terms are \(1/(z-z_n)\), which also satisfy the uniform summable bound above. The logarithmic derivative of the finite head contributes the remaining terms. Consequently

\[
\frac{F'(z)}{F(z)}=S(z)
\qquad(z\notin\{z_n:n\geq1\}).
\]

This argument uses local logarithms only where needed and does not assume a global logarithm of the function \(F\), which has zeros.

## Sublinear logarithmic growth of the product and derivative

Write \(M_G(r)=\max_{|z|\leq r}|G(z)|\) for an entire function \(G\). For \(r>0\),

\[
\log M_F(r)\leq L(r):=\sum_{n\geq1}\log(1+r/|z_n|).
\]

The sum on the right is finite because \(\log(1+t)\leq t\). For every fixed \(n\),

\[
\frac{\log(1+r/|z_n|)}{r}\longrightarrow0,
\qquad
0\leq\frac{\log(1+r/|z_n|)}{r}\leq\frac1{|z_n|}.
\]

For an explicit limit argument, choose a finite head so that the sum of \(1/|z_n|\) in the tail is less than \(\varepsilon\). That tail contributes at most \(\varepsilon\) to \(L(r)/r\); the finite head tends to zero after division by \(r\). Since \(\varepsilon\) is arbitrary, \(L(r)/r\to0\). Also \(M_F(r)\geq|F(0)|=1\), so \(\log M_F(r)/r\to0\).

Cauchy's formula on the circle of radius one centered at any \(z\) gives

\[
|F'(z)|\leq\max_{|w-z|=1}|F(w)|.
\]

Therefore

\[
\log M_{F'}(r)\leq L(r+1)=o(r).
\]

The function \(F'\) is not identically zero, since \(F\) is nonconstant. A fixed nonzero value of \(F'\) bounds its maximum modulus below for all sufficiently large radii. Thus its logarithmic maximum modulus divided by \(r\) also tends to zero. The upper bound alone is sufficient below.

## An elementary finite-zero lemma

**Lemma.** If \(G\not\equiv0\) is entire, has only finitely many distinct zeros, and

\[
\limsup_{r\to\infty}\frac{\log M_G(r)}r\leq0,
\]

then \(G\) is a polynomial.

**Proof.** Nonzero analytic functions have finite multiplicity at each zero. Let \(P\) be the monic polynomial having exactly the zeros of \(G\), with those multiplicities; take \(P=1\) when there are no zeros. Then \(H=G/P\), with its removable singularities filled in, is entire and nowhere zero.

Let \(m=\deg P\). For sufficiently large \(r\), each zero \(a_j\) of \(P\), repeated according to multiplicity, satisfies \(|a_j|\leq r/2\). On \(|z|=r\),

\[
|P(z)|=\prod_{j=1}^{m}|z-a_j|\geq(r/2)^m.
\]

The maximum modulus principle for \(H\) consequently gives

\[
\log M_H(r)\leq\log M_G(r)-m\log r+m\log2,
\]

for all sufficiently large \(r\). Thus \(\limsup \log M_H(r)/r\leq0\). Since \(H(0)\ne0\), the lower bound \(M_H(r)\geq|H(0)|\) shows that the limit is in fact zero.

The quotient \(H'/H\) is entire and has an entire primitive on the simply connected plane. Choosing an additive constant in that primitive yields an entire function \(h\) with \(H=e^h\). This follows directly because the derivative of \(He^{-h}\) is zero; a logarithm of its nonzero constant value fixes the additive constant. No entire-function factorization theorem is used.

Fix \(a\in\mathbb C\) and let

\[
A_R=\max_{|z-a|\leq R}\operatorname{Re}h(z).
\]

Since \(\operatorname{Re}h=\log|H|\),

\[
\operatorname{Re}h(a)\leq A_R\leq \log M_H(R+|a|),
\qquad A_R/R\longrightarrow0.
\]

On the disk centered at \(a\) with radius \(R\), the harmonic function \(u=A_R-\operatorname{Re}h\) is nonnegative. Taylor expansion on its boundary gives the first Fourier coefficient identity

\[
\frac1{2\pi}\int_0^{2\pi}
  \operatorname{Re}h(a+Re^{it})e^{-it}\,dt
  =\frac{R h'(a)}2.
\]

The constant \(A_R\) contributes zero to this coefficient, so the triangle inequality and the harmonic mean-value identity imply

\[
\frac{R|h'(a)|}{2}
\leq\frac1{2\pi}\int_0^{2\pi}u(a+Re^{it})\,dt
=u(a)=A_R-\operatorname{Re}h(a).
\]

Divide by \(R\) and let \(R\to\infty\). The right-hand side divided by \(R\) tends to zero; hence \(h'(a)=0\). The point \(a\) was arbitrary. Thus \(h\), and therefore \(H\), is constant. It follows that \(G=PH\) is a polynomial. This proves the lemma.

## Infinitely many zeros away from the poles

Suppose \(F'\) had only finitely many distinct zeros. The growth estimate and the lemma would make \(F'\) a polynomial. Taking a polynomial antiderivative would then make \(F\) a polynomial plus a constant, contradicting its infinitely many zeros. Therefore \(F'\) has infinitely many distinct zeros.

Every \(z_n\) is a simple zero of \(F\), so \(F'(z_n)\ne0\). None of the zeros just obtained is a pole of \(S\). At each such zero, the identity \(S=F'/F\) gives \(S=0\). This completes the theorem.

## Potential interpretation and scope

The well-defined normalized potential away from the charges is

\[
U(z)=\sum_{n\geq1}\log|1-z/z_n|=\log|F(z)|.
\]

The analytic logarithmic tail used above gives local convergence and justifies taking derivatives. With \(z=x+iy\), the exact convention is

\[
U_x-iU_y=S(z),\qquad U_x+iU_y=\overline{S(z)}.
\]

Thus equilibria of the real planar gradient are exactly the zeros of \(S\). Subtracting \(\log|z_n|\) from each individual unnormalized potential term changes no individual gradient; the normalized series is the convergent definition, rather than a subtraction of two asserted convergent infinite sums.

Distinctness is essential to this particular elementary separation argument: it makes \(F\) and \(F'\) have no common zeros. The proof here establishes precisely the infinite, distinct, unit-charge planar case. It makes no claim to settle arbitrary positive real charges or higher-dimensional Newtonian analogues, nor to determine the current status of those extensions. No numerical experiment, source-author code, or formal proof assistant is used.
