# Characteristic growth under differentiation: partial results for Problem 2.69

**ID:** 2302069 / AMR-022-2069. **Date:** 2026-10-04.

**Verdict: partial; the original existence question is not resolved.**
No novelty or priority is claimed for the auxiliary results below.

## 1. Target and conventions

For an entire function, write

\[
 T(r,f)=\frac1{2\pi}\int_0^{2\pi}\log^+|f(re^{i\theta})|\,d\theta,
 \qquad M(r,f)=\max_{|z|=r}|f(z)|.
\]

The order and lower order are respectively
\(\rho(f)=\limsup \log T(r,f)/\log r\) and
\(\lambda(f)=\liminf \log T(r,f)/\log r\).
The target asks whether there exists a single \(d>0\) such that every
transcendental entire \(f\) with \(\rho(f)<d\) satisfies

\[
 L(f):=\liminf_{r\to\infty}\frac{T(r,f)}{T(r,f')}\le1. \tag{Q}
\]

The full statement and update are in Hayman–Lingham [HL], printed pp. 48–49.
The update cites Langley's counterexamples for every order above \(1/2\).
Consequently any admissible \(d\) is at most \(1/2\): otherwise choose an order
strictly between \(1/2\) and \(d\) and apply [L, Theorem 2]. This is prior work,
not a result of this investigation. The issue at order exactly \(1/2\) is not
required for choosing \(d=1/2\), since (Q) uses a strict order inequality.

All circle integrals below ignore finitely many zeros on a given circle;
the logarithmic and fractional-power singularities used here are integrable.
The notation \(x^+\) means \(\max(x,0)\).

## 2. A self-contained comparison bound approaching 1 at lower order zero

### Lemma 1: growth and fixed dilations

For any transcendental entire \(F\),

\[
 \frac{T(r,F)}{\log r}\longrightarrow\infty. \tag{1}
\]

Also \(\rho(F')=\rho(F)\) and \(\lambda(F')=\lambda(F)\).

**Proof.** The Poisson majorant for the subharmonic function
\(\log^+|F|\) on a disk gives, for \(R>r\),

\[
 \log^+M(r,F)\le\frac{R+r}{R-r}T(R,F). \tag{2}
\]

Indeed the Poisson kernel on \(|z|=r\) is at most \((R+r)/(R-r)\).
If \(a_n\ne0\) is a Taylor coefficient, Cauchy's coefficient inequality and
(2) give
\(n\log r+\log|a_n|\le\log M(r,F)\le3T(2r,F)\).
A transcendental entire function has nonzero coefficients of arbitrarily
large index. Replacing \(2r\) by \(s\) and then taking arbitrarily large
indices proves (1).

Cauchy's derivative estimate, applied on radius \(r\) disks centered at
points of \(|z|=r\), gives
\(M(r,F')\le M(2r,F)/r\). For \(r\ge1\), therefore,

\[
 T(r,F')\le3T(4r,F).
\]

Radial integration gives
\(M(r,F)\le |F(0)|+rM(r,F')\), hence

\[
 T(r,F)\le3T(2r,F')+\log r+C_F. \tag{3}
\]

The derivative is also transcendental. By (1), the additive term in (3)
can be absorbed into a fixed multiple of \(T(2r,F')\) for large \(r\).
These two comparisons, with fixed dilations of \(r\), prove equality of
both upper and lower orders. ∎

### Lemma 2: good dilation radii

If \(U(r)>0\) is nondecreasing and has finite lower order \(\lambda\), then
for every \(k>1\) and \(\sigma>\lambda\) there are arbitrarily large \(r\) with
\(U(kr)\le k^\sigma U(r)\).

**Proof.** Otherwise \(U(kr)>k^\sigma U(r)\) eventually. Iteration at
\(r=k^nR\), and monotonicity between these radii, imply
\(\liminf\log U(r)/\log r\ge\sigma\), a contradiction. ∎

### Proposition 3: elementary universal bound

If \(f\) is transcendental entire of finite lower order \(\lambda\), then

\[
 L(f)\le C(\lambda):=\inf_{k>1}k^\lambda\frac{k+1}{k-1}. \tag{4}
\]

In particular \(C(0)=1\), recovering the lower-order-zero conclusion.
For every \(\lambda>0\), however, \(C(\lambda)>1\).

**Proof.** Radial integration followed by (2), this time for \(f'\), yields

\[
 T(r,f)\le\log r+C_f+\frac{k+1}{k-1}T(kr,f').
\]

Apply Lemma 2 to \(U=T(\cdot,f')\), whose lower order is \(\lambda\) by
Lemma 1. Divide by \(T(r,f')\) at its good radii. The additive term vanishes
by (1). Thus \(L(f)\le k^\sigma(k+1)/(k-1)\). Let \(\sigma\downarrow\lambda\)
and take the infimum over \(k\).

When \(\lambda=0\), send \(k\to\infty\). When \(\lambda>0\), the expression
diverges at both endpoints \(k\downarrow1\) and \(k\to\infty\). Its unique
minimizer is

\[
 k_\lambda=\frac{1+\sqrt{1+\lambda^2}}{\lambda}>1,
\]

as follows by differentiating its logarithm:
\(\lambda/k-2/(k^2-1)=0\). Its minimum is strictly above 1. On the other
hand \(C(\lambda)\to1\) as \(\lambda\downarrow0\), for example by inserting
\(k=\lambda^{-1/2}\) for small positive \(\lambda\). ∎

**Gap in this approach.** Arbitrarily small excess over 1 does not establish
(Q) on any fixed positive interval of orders. The dilation factor cannot be
sent to infinity while keeping \(k^\lambda\) close to 1 for a fixed positive
\(\lambda\). We do not assert that (4) is the best known comparison bound.

## 3. Forward logarithmic derivatives and the exact loss term

The following calculation applies to canonical products without a
nonconstant exponential factor. The standard genus-zero case of Hadamard
factorization says that every nonzero entire function of order \(\rho<1\)
has the representation used below and that
\(\sum_n|a_n|^{-p}<\infty\) whenever \(\rho<p<1\).
We use this classical factorization theorem; we do not claim to reprove it.

### Proposition 4: a vanishing forward proximity term

Suppose

\[
 f(z)=c z^m\prod_n(1-z/a_n),\qquad c\ne0,
 \quad a_n\ne0,\quad\sum_n|a_n|^{-p}<\infty
 \quad\text{for some }0<p<1. \tag{5}
\]

Repeated zeros are repeated in the list; a finite list is permitted.
Then, with \(h=f'/f\),

\[
 m(r,h):=\frac1{2\pi}\int\log^+|h(re^{i\theta})|\,d\theta\longrightarrow0.
 \tag{6}
\]

**Proof.** Normal convergence of the logarithmic derivative series away
from the zeros gives

\[
 h(z)=\frac mz+\sum_n\frac1{z-a_n}. \tag{7}
\]

Here \(\sum|a_n|^{-1}<\infty\) follows from the assumption in (5).
There is a finite constant \(A_p\) such that

\[
 \sup_{s\ge0}\frac1{2\pi}\int_0^{2\pi}|se^{i\theta}-1|^{-p}d\theta\le A_p.
 \tag{8}
\]

For \(s\le1/2\) the integrand is at most \(2^p\); for \(s\ge2\) it is at
most 1. For \(1/2\le s\le2\), use
\(|se^{i\theta}-1|^2=(s-1)^2+4s\sin^2(\theta/2)\ge2\sin^2(\theta/2)\).
The resulting bound is integrable because \(p<1\).

By rotation and scaling, the mean of \(|re^{i\theta}-a|^{-p}\) is at most
\(A_p|a|^{-p}\), uniformly in \(r\), and tends to zero as \(r\to\infty\)
for each fixed \(a\). The inequality
\(|\sum b_j|^p\le\sum|b_j|^p\), first for finite sums and then by passage to
the convergent series, gives

\[
 \frac1{2\pi}\int|h(re^{i\theta})|^p d\theta
 \le\frac{m^p}{r^p}+\sum_n\frac1{2\pi}\int|re^{i\theta}-a_n|^{-p}d\theta
 \longrightarrow0.
\]

The last limit follows from the summable majorant in (8). Finally
\(\log^+x\le x^p/p\) for \(x\ge0\), proving (6). ∎

### Proposition 5: exact formulation of the missing estimate

Let \(f\) be transcendental entire of order \(\rho<1\). Set

\[
 A_r(\theta)=\log^+|f(re^{i\theta})|,
 \quad D_r(\theta)=\log^+|f'(re^{i\theta})|,
\]
\[
 B_f(r)=\frac1{2\pi}\int(A_r-D_r)^+d\theta,
 \quad E_f(r)=\frac1{2\pi}\int(D_r-A_r)^+d\theta.
\]

Then

\[
 T(r,f)-T(r,f')=B_f(r)-E_f(r),\qquad 0\le E_f(r)\le m(r,f'/f)=o(1). \tag{9}
\]

Consequently \(L(f)\ge1\), and

\[
 L(f)=1\quad\Longleftrightarrow\quad
 \liminf_{r\to\infty}\frac{B_f(r)}{T(r,f)}=0. \tag{10}
\]

**Proof.** The equality in (9) is the identity \(a-b=(a-b)^+-(b-a)^+\).
For positive \(u,v\),
\((\log^+v-\log^+u)^+\le\log^+(v/u)\).
Apply this with \(u=|f|,v=|f'|\) and use Proposition 4. Zeros do not affect
the integrals. Divide (9) by \(T(r,f)\), which tends to infinity:

\[
 \frac{T(r,f')}{T(r,f)}=1-\frac{B_f(r)}{T(r,f)}+o(1).
\]

The right side is positive and at most \(1+o(1)\). Since
\(0\le B_f(r)/T(r,f)\le1\), reciprocal ratios give (10), including the
possibility that the limsup of the derivative ratio is zero. ∎

**Gap in this approach.** The forward proximity term is already negligible
throughout \(\rho<1\), a range containing known counterexamples. What is
needed is a subsequence on which the *loss* \(B_f/T\) tends to zero. Its
integrand measures exactly where the characteristic contribution of \(f\)
is larger than that of \(f'\). A mere small upper bound on \(f'/f\) gives
no such conclusion.

## 4. Complete positive result for a restricted zero geometry

### Proposition 6: real zeros

If \(f\) is transcendental entire of order less than 1 and every zero is
real, then

\[
 \lim_{r\to\infty}\frac{T(r,f)}{T(r,f')}=1. \tag{11}
\]

The same holds if the zero set is contained in a line through the origin,
by rotation. This is a subclass result, not an arbitrary-zero theorem.

**Proof.** Factorize as in (5) and take \(\rho<p<1\). The function has a
zero: otherwise its genus-zero factorization would be constant. Fix one
zero \(a\), which may equal 0. For \(z=x+iy\) with \(y\ne0\), (7) gives

\[
 \operatorname{Im}h(z)
 =-y\left(\frac m{|z|^2}+\sum_n\frac1{|z-a_n|^2}\right).
\]

All summands have the same sign after multiplication by \(-y\), and the
chosen zero therefore gives, on \(|z|=r\),

\[
 |h(re^{i\theta})|\ge\frac{r|\sin\theta|}{(r+|a|)^2}.
\]

For \(r\ge1\), \((r+|a|)^2/r\ge1\). Integrating the resulting reciprocal
bound, and using the elementary integral
\((2\pi)^{-1}\int_0^{2\pi}\log(1/|\sin\theta|)d\theta=\log2\), gives

\[
 m(r,1/h)\le\log r+2\log(1+|a|/r)+\log2. \tag{12}
\]

The two real-axis points on each circle have measure zero. The displayed
integral is finite; its value follows from the substitutions
\(\theta\mapsto\pi/2-\theta\) and \(\sin2\theta=2\sin\theta\cos\theta\)
in \(\int_0^{\pi/2}\log\sin\theta\,d\theta\).
Since \(f=f'/h\),
\(T(r,f)\le T(r,f')+m(r,1/h)\).
On the other hand Proposition 4 gives
\(T(r,f')\le T(r,f)+m(r,h)=T(r,f)+o(1)\).
Divide these two inequalities by the characteristics and use (1).
This proves (11), including arbitrary zero multiplicities. ∎

**Gap in this approach.** For zeros with different imaginary parts the
summands in \(\operatorname{Im}h\) need not have a common sign. The estimate
(12) has not been extended here to arbitrary complex zero sets at any
uniform positive upper-order threshold.

## 5. A normalized obstruction to a same-radius minimum-modulus argument

Large minimum modulus, even together with \(f(0)=0\), does not on its own
force the desired comparison on that circle. The following exact example
is useful for detecting that invalid inference.

### Proposition 7: varying-polynomial obstruction

Fix \(c>0\). For positive integers \(N\equiv3\pmod6\), put

\[
 F_N(z)=e^{cN}\big((1-z)^N-1\big).
\]

Then \(F_N(0)=0\),

\[
 \min_{|z|=1}|F_N(z)|\ge\tfrac14 e^{cN}, \tag{13}
\]

but \(T(1,F_N)/T(1,F_N')\) tends to a constant strictly greater than 1 as
\(N\to\infty\) through these integers.

**Proof of (13).** Write \(w=1-z=2\cos t\,e^{it}\) on \(|z|=1\), where
\(-\pi/2\le t\le\pi/2\). The point \(w=0\) gives \(|w^N-1|=1\).
If \(|w^N-1|<1/4\), then

\[
 |\log|w||\le\frac{\log(4/3)}N,
 \qquad |w|<(5/4)^{1/N}\le5/4<\sqrt2.
\]

Thus \(|t|>\pi/4\). On the interval between \(|t|\) and \(\pi/3\),
\(|d\log(2\cos t)/dt|=|\tan t|\ge1\). The mean value theorem yields

\[
 |N|t|-N\pi/3|\le\log(4/3)<\pi/2.
\]

But \(N\pi/3\) is an odd multiple of \(\pi\), so \(\operatorname{Re}w^N<0\).
This contradicts \(\operatorname{Re}w^N>3/4\), proving (13).

For the characteristic limit, put
\(u(\theta)=\log|1-e^{i\theta}|\) and
\(C_0=(2\pi)^{-1}\int u^+d\theta>0\). Except at a set of measure zero,

\[
 \frac1N\log^+|F_N(e^{i\theta})|\longrightarrow c+u(\theta)^+.
\]

The lower bound (13) and upper bound
\(|w^N-1|\le2\max(1,|w|^N)\) provide a uniform integrable bound after
normalization. Likewise, from
\(F_N'(z)=-Ne^{cN}(1-z)^{N-1}\),

\[
 \frac1N\log^+|F_N'(e^{i\theta})|\longrightarrow(c+u(\theta))^+,
\]

with a uniform upper bound because \(u\le\log2\). Dominated convergence
therefore gives

\[
 \frac{T(1,F_N)}N\to c+C_0,
 \quad\frac{T(1,F_N')}N\to I(c):=\frac1{2\pi}\int(c+u)^+d\theta>0.
\]

The difference of the limits is

\[
 c+C_0-I(c)=\frac1{2\pi}\int_{u<0}\min(c,-u)\,d\theta>0,
\]

because \(u<0\) on a set of positive measure. ∎

**Scope warning.** These are different polynomials at the fixed radius 1.
The target concerns one fixed transcendental function as \(r\to\infty\).
Thus Proposition 7 is not a counterexample to (Q). It rules out only a local
inference using large minimum modulus and normalization. Any successful
minimum-modulus proof must also exploit the global fixed-function growth
restriction. We have not supplied that missing step.

## 6. Ramification preserves the ratio but raises the order

### Proposition 8: polynomial pullback

For a transcendental entire \(f\), an integer \(q\ge1\), and
\(g(z)=f(z^q)\),

\[
 T(r,g)=T(r^q,f),\quad
 T(r^q,f')\le T(r,g')\le T(r^q,f')+\log q+(q-1)\log r\quad(r\ge1). \tag{14}
\]

Consequently \(L(g)=L(f)\), \(\rho(g)=q\rho(f)\), and
\(\lambda(g)=q\lambda(f)\).

**Proof.** The first equality follows by the substitution
\(\phi=q\theta\) in the circle integral. For the derivative,
\(g'(z)=qz^{q-1}f'(z^q)\), and the multiplier has modulus
\(qr^{q-1}\ge1\). The scalar inequalities
\(\log^+x\le\log^+(ax)\le\log^+x+\log a\), for \(a\ge1\), prove (14).
By (1), its additive error is negligible relative to \(T(r^q,f')\),
so it preserves the liminf ratio. The assertions about orders follow
directly from the first equality. ∎

Trying \(f(z^{1/q})\) in reverse does not define an entire function in
general. An entire \(g\) admits a representation \(g(z)=F(z^q)\) precisely
when it is invariant under multiplication by every \(q\)-th root of unity:
the Taylor coefficients in nonmultiple degrees must vanish. In that case
\(F\) is entire, as its power series converges on every disk by the entire
convergence of \(g\). No such invariance has been established for a
counterexample here. Averaging over rotations enforces it but supplies no
lower bound on the characteristic or on the loss term; an odd entire
function, for example, averages to zero under \(z\mapsto-z\).

**Gap in this approach.** The available pullback increases order. There is
no verified order-lowering construction preserving \(L>1\). The approximation
angle used in [L, Lemma B] also has positive width only above order \(1/2\);
its collapse is an obstruction to that particular construction, not a proof
that counterexamples cannot exist below it.

## 7. Final boundary

This note proves a lower-order-dependent comparison, a vanishing forward
logarithmic-derivative proximity for order below 1, a complete real-zero
subclass theorem, a finite-radius minimum-modulus obstruction, and the exact
ramification identities. None supplies a universal positive \(d\) in (Q),
or counterexamples of arbitrarily small positive order.

For order below 1 the precise remaining analytic estimate in this note is:
find \(d>0\) such that every transcendental entire \(f\) of order below \(d\)
has a sequence \(r_j\to\infty\) with
\(B_f(r_j)=o(T(r_j,f))\); alternatively construct violations at arbitrarily
small positive orders. Equation (10) is a reformulation, not progress by
itself. No full-resolution or present-day exhaustive literature claim is made.

## References

[HL] W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory*,
arXiv:1809.07200v2 (2018), Problem and Update 2.69, pp. 48–49.
https://arxiv.org/abs/1809.07200v2

[L] J. K. Langley, “On the deficiencies of composite entire functions,”
*Proceedings of the Edinburgh Mathematical Society* 36 (1993), 151–164,
Theorem 2 and §§2–4. The PDF masthead says 1992; the publisher's volume/issue
metadata says February 1993.
https://doi.org/10.1017/S0013091500005964

[T] S. Toppila, “On Nevanlinna's characteristic functions of entire functions
and their derivatives,” *Ann. Acad. Sci. Fenn. Ser. A I Math.* 3 (1977),
131–134. https://doi.org/10.5186/aasfm.1977.0326
