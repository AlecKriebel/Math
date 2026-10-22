# Necessary conditions and exact exclusions for irrational maxima

Alec Kriebel · ORCID https://orcid.org/0009-0001-9320-500X

Problem 30002497 / OWR-12866-004. Status: **unsolved**.

Let

\[
 A(x)=\int_0^\infty\{t\}\{xt\}\,\frac{dt}{t^2},\qquad x>0.
\]

The target is the existence of an irrational \(x>0\) and \(\epsilon>0\)
such that \(A(y)<A(x)\) whenever \(0<|y-x|<\epsilon\), \(y>0\).
The results below give necessary conditions and excluded families. They do
not supply such a point or prove that none exists. No novelty claim is made
for these deductions from the cited literature.

## 1. Direct truncation: finite convexity does not survive the needed limit

For an integer \(T\ge1\), put
\[
 A_T(x)=\int_0^T\{t\}\{xt\}\,dt/t^2.
\]
Then, uniformly for every \(x>0\),
\[
 0\le A(x)-A_T(x)\le 1/T.                                      \tag{1}
\]
For \(x\) away from the finitely many breakpoints in a fixed compact
interval, differentiation of the finitely many moving jumps gives
\[
 A_T'(x)=C_T-\sum_{1\le m\le xT}\frac{\{m/x\}}m,
 \qquad C_T=\int_0^T\frac{\{t\}}t\,dt.                         \tag{2}
\]
Indeed the derivative of the linear part of \(\{xt\}\) contributes
\(C_T\); the jump crossing \(t=m/x\) contributes \(-\{m/x\}/m\).
Between breakpoints both \(M=\lfloor xT\rfloor\) and all
\(\lfloor m/x\rfloor\) are constant, so
\[
 A_T''(x)=M/x^2\ge0.                                           \tag{3}
\]
The breakpoints are rational: \(m/T\) and \(m/n\) with integer
\(1\le n\le T\). For \(x<1/T\), (2) instead gives the positive
constant slope \(C_T\). Consequently every strict local maximum of
\(A_T\) is rational.

This does **not** prove the target negative. Uniform limits can acquire a
strict irrational maximum: if rational \(r_n\to\alpha\notin\mathbb Q\),
then \(-|x-r_n|\) converges uniformly to \(-|x-\alpha|\).
Equation (1) controls values, not signs of arbitrarily small increments.
Thus the finite-convexity route is blocked at a genuine limit issue.

For numerical evaluation, on a cell where \(n=\lfloor t\rfloor\) and
\(m=\lfloor xt\rfloor\) are fixed, an antiderivative is
\[
 xt-(m+nx)\log t-nm/t.                                         \tag{4}
\]
The accompanying verifier uses (4), certified ordering of the endpoints
\(n\) and \(m/x\), interval arithmetic, and the tail enclosure (1).

## 2. Hilbert-space geometry and reciprocity

Substitution gives
\[
 A(x)=xA(1/x).                                                 \tag{5}
\]
In \(H=L^2((0,\infty),t^{-2}dt)\), set \(f(t)=\{t\}\) and
\(K_xf(t)=x^{-1/2}f(xt)\). The operator \(K_x\) is unitary, and
\[
 A(x)/\sqrt{x}=\langle f,K_xf\rangle\le A(1),
 \qquad A(1)=\log(2\pi)-\gamma.                               \tag{6}
\]
Equality implies \(K_xf=f\) almost everywhere, since both have the same
norm and their inner product equals that norm squared. On a sufficiently
small positive interval, \(K_xf(t)=\sqrt{x}\,t\) and \(f(t)=t\),
so equality forces \(x=1\).

Thus the *normalized* autocorrelation has its unique global maximum at 1.
Multiplication by \(\sqrt{x}\) changes extrema; (6) does not settle
local extrema of \(A\). At differentiability points, (5) yields
\[
 xA'(x)+A'(1/x)=A(x).                                         \tag{7}
\]
In particular, a stationary irrational \(x\) has
\(A'(1/x)=A(x)>0\). Passing to reciprocals cannot preserve a
stationary local maximum of the unnormalized function.

## 3. Irrational local maxima must be stationary Wilton points

We use precise results from Balazard–Martin [BM], not merely the slogan
that almost every point is differentiable. On \((0,1)\), let
\(\alpha_0(x)=x\), \(\alpha_{k+1}(x)=\{1/\alpha_k(x)\}\),
\(\beta_{-1}=1\), \(\beta_k=\prod_{j=0}^k\alpha_j\), and
\[
 \gamma_k(x)=\beta_{k-1}(x)\log(1/\alpha_k(x))>0,
 \quad S_K(x)=\sum_{k=0}^K(-1)^k\gamma_k(x).
\]
Write \(W=\sum(-1)^k\gamma_k\) where it converges and
\(\Upsilon(x)=\int_0^x W(t)\,dt\), using the almost-everywhere
integrable version. A Wilton point is an irrational where this series
converges. [BM, Proposition 7 and Theorem 1] identify these with the
irrational differentiability points of \(A\).

Two specific inputs are needed:

- [BM, Proposition 1]: \(A(x)=\rho(x)-\Upsilon(x)/(2x)\), where
  \(\rho\) is differentiable at every irrational in \((0,1)\).
- [BM, proof of Proposition 11, equation (37), pp. 17–19]: for each fixed
  irrational \(x\), there are \(h_K\to0\), positive for odd \(K\)
  and negative for even \(K\), for which
  \[
    \frac{\Upsilon(x+h_K)-\Upsilon(x)}{h_K}
      =S_K(x)+O(1/q_K).                                      \tag{8}
  \]
  The estimates constructing (8) do not assume divergence of \(S_K\).
  Divergence is invoked only at the last step of the cited proof to deduce
  non-differentiability. Hence (8) is available at every irrational.

**Parity squeeze lemma.** Suppose \(r,c\) are differentiable at an
irrational \(x\in(0,1)\), \(c(x)>0\), and
\(F(t)=r(t)-c(t)\Upsilon(t)\) locally. If \(F\) has a local maximum
at \(x\), then \(x\) is a Wilton point.

**Proof.** Exact rearrangement, before taking limits, gives
\[
 \frac{F(x+h)-F(x)}h
 =\frac{r(x+h)-r(x)}h-
   \frac{c(x+h)-c(x)}h\Upsilon(x)
   -c(x+h)\frac{\Upsilon(x+h)-\Upsilon(x)}h.
\]
For positive \(h\), maximality makes the left side nonpositive, so the
last secant quotient is bounded below by a quantity tending to
\(D=(r'(x)-c'(x)\Upsilon(x))/c(x)\). For negative \(h\), the
inequality is reversed. Using (8) and \(q_K\to\infty\),
\[
 \liminf_{k\to\infty}S_{2k+1}\ge D,
 \qquad \limsup_{k\to\infty}S_{2k}\le D.                      \tag{9}
\]
Positivity of the \(\gamma_j\) implies
\(S_{2k+1}\le S_{2k}\) and \(S_{2k-1}\le S_{2k}\).
The first inequality and (9) squeeze the odd subsequence to \(D\);
the second and (9) squeeze the even subsequence to \(D\). Thus the
whole series converges. This argument never assumes bounded secants before
establishing the squeeze. ∎

**Theorem.** Every irrational local maximum of \(A\), even a non-strict
one, is a differentiability point of \(A\), and \(A'(x)=0\).

For \(0<x<1\), apply the lemma with \(r=\rho\), \(c(t)=1/(2t)\).
For \(x>1\), put \(y=1/x\). The function
\(F(t)=A(1/t)=A(t)/t=\rho(t)/t-\Upsilon(t)/(2t^2)\) has a local
maximum at \(y\). The lemma makes \(y\) Wilton, so \(A\) is
differentiable there. Reciprocity then implies differentiability at \(x\).
Fermat's theorem supplies \(A'(x)=0\) in either case. ∎

This excludes all non-Wilton irrationals. It leaves the stationary Wilton
points, and is not a full solution to the existence question.

## 4. The stationary residual and the rational-cusp obstruction

Let \(\phi_1(t)=\sum_{n\ge1}B_1(nt)/n\), with
\(B_1(u)=\{u\}-1/2+[u\in\mathbb Z]/2\). At a positive Wilton
point \(x\), [BM, Theorem 2 and Proposition 26] justify convergence
and the needed Lebesgue-point differentiation. The integral identity
[BM, equation (6)] gives
\[
 A'(x)=\frac{A(x)-\tfrac12\log x-\tfrac12 A(1)+\phi_1(x)}x.    \tag{10}
\]
If this vanishes, subtraction of the same integral identity at \(x+h\)
and \(x\) gives the **exact** formula
\[
 A(x+h)-A(x)=\frac12\left(\log(1+h/x)-h/x\right)
  +(x+h)\int_x^{x+h}\frac{\phi_1(t)-\phi_1(x)}{t^2}\,dt.       \tag{11}
\]
Oriented integrals make (11) valid for both signs of \(h\), with
\(x+h>0\). The explicit term is negative, of size
\(-h^2/(4x^2)+O(h^3)\). But the Lebesgue-point theorem only makes
the integral term \(o(|h|)\), which may be much larger than \(h^2\).
It does not give the required two-sided upper bound. A sufficient condition
would be that this integral is \(o(h^2)\); no such condition has been
established at a stationary point here.

The fixed-rational asymptotic in [BDBLS, Proposition 98] has leading term
\[
 A(p/q+h)-A(p/q)=\frac{|h|\log|h|}{2p}+O_{p,q}(|h|),           \tag{12}
\]
for coprime positive integers \(p,q\). It proves strict local maxima at
rational points. Applying (12) along convergents to an irrational without
controlling its denominator-dependent linear term and neighborhood is
invalid. The corresponding uniform formula contains an explicit
\(D^\pm(p,q)h\) and an \(O(q^4p^{-1}h^3)\) remainder. Their
comparison with the cusp along a general convergent sequence has no
settled sign. This is the exact obstruction to the rational-approximation
route tried here.

## 5. A periodic continued-fraction family can be excluded

[BDBLS, Proposition 88] and the convergence theorem give, at Wilton points,
\[
 A(x)=\frac{1-x}{2}\log x+\frac{1+x}{2}A(1)
      -\phi_1(x)-x\phi_1(1/x).                               \tag{13}
\]
If \(1/x-x\in\mathbb Z\), periodicity makes the two \(\phi_1\)
values equal. Substituting (13) into (10) and simplifying proves
\[
             A'(x)=\frac{A(x)-\log x}{1+x}.                  \tag{14}
\]
These \(x\) are quadratic irrationals (apart from \(x=1\), which is
excluded): their continued fractions are eventually periodic with bounded
partial quotients, so the Wilton series converges absolutely. For clarity,
\(x=1\) is **not** covered by (14), since \(A\) is not differentiable
there.

For every integer \(m\ge1\), let
\[
 r_m=\frac{\sqrt{m^2+4}-m}{2},\qquad y_m=1/r_m=m+r_m.
\]
Since \(0<r_m<1\), positivity of \(A\) and negativity of \(\log r_m\)
show \(A'(r_m)>0\). Therefore none of these infinitely many
irrationals is a local maximum.

For the reciprocal family, let \(M=\pi^2/36\) and
\(C=(1+A(1))/2\). The Bernoulli-series function
\(\phi_2(t)=\sum_{n\ge1}B_2(nt)/n^2\) obeys \(|\phi_2(t)|\le M\).
The representation [BM, Proposition 28] therefore gives
\[
 A(y)\le\tfrac12\log y+C+M/y.                                \tag{15}
\]
The function \(C+M/y-\tfrac12\log y\) decreases for \(y>0\),
and it is less than \(-0.04369\) at 11 (checked with interval constants).
Thus \(A'(y_m)<0\) whenever \(m\ge11\).

For \(m=1,\ldots,10\), the reproducible interval computation using
(1) and (4) proves the following signs, conditional only on the correctness
of the standard mpmath interval implementation used by the verifier:

- \(A'(y_m)>0\) for \(1\le m\le9\);
- \(A'(y_{10})<0\).

The program also checks \(m=11\), agreeing with the independent analytic
bound. At \(m=9\) the derivative enclosure is contained in
\([0.0028377,0.0028861]\); at \(m=10\) it is contained in
\([-0.0020362,-0.0019921]\). Both are safely separated from zero.
The full intervals are in `control_results.json`. Reciprocal integral
checks and the exact \(A(1)\) control are included.

Consequently the entire family \(\{r_m,y_m:m\ge1\}\) is excluded,
with the finite reciprocal cases checked by validated numerics. The change
of sign between \(y_9\) and \(y_{10}\) does not force a stationary
irrational: rational nondifferentiability points lie between them, so no
Darboux or continuous-derivative argument applies across the interval.

## Remaining gap

The existence or impossibility of a stationary Wilton point satisfying the
strict two-sided increment inequality (11) remains unproved. Five distinct
routes were pursued; no additional search is hidden as verification.

References and exact source locations are recorded in `SOURCES.md`.
