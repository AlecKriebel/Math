# Exact marked-divisor exclusion in the fixed-linear \(\delta=1\) row

**Exact candidate checkpoint:** 2026-07-25T13:08:54Z  
**Status:** complete primary proof; pending independent hostile audit; not peer
reviewed.

## 1. Scope and statement

Let
\[
H_4=(P,Q,0)=(pA_3(p,q),pB_3(p,q),0),
\qquad \gcd(A_3,B_3)=1,
\]
and put \(R=(H_3)_3\in\mathbb C[p,q]_3\).  As usual,
\[
\alpha=J(Q,R),\qquad \beta=-J(P,R),\qquad
\gamma=J(P,Q),\qquad
\delta=\deg\gcd(\alpha,\beta,\gamma).
\]
This note treats only the marked exact-\(\delta=1\) component: the common
linear divisor is the fixed divisor \(p\).

**Candidate theorem.**  Every Keller map in this marked
exact-\(\delta=1\) component is a polynomial automorphism.  Equivalently,
no Keller counterexample lies on it.

The unmarked critical-point component of \(\delta=1\), and all
\(\delta\ge2\) components, remain separate.

## 2. The divided-gradient tangent

The condition \(p\mid\alpha,\beta\) is equivalent here to
\[
R=pS_2(p,q).
\]
After a target change in the first two components, normalize the
\(q^3\)-coefficients of \((A_3,B_3)\) to \((0,1)\):
\[
\begin{aligned}
A_3&=a_0p^3+a_1p^2q+a_2pq^2,\\
B_3&=b_0p^3+b_1p^2q+b_2pq^2+q^3.                 \tag{1}
\end{aligned}
\]
Exactness of \(\delta=1\) forces the \(q^2\)-coefficient of \(S_2\) to
be nonzero.  Indeed, in this normalization the value of \(\alpha/p\) at
\(p=0\) is a nonzero scalar multiple of that coefficient, while
\(\beta/p\) and \(\gamma/p\) already vanish there.

Scale and shear \(q\) while preserving \(p\).  The two possible quadratic
orbits are therefore
\[
S_2=q^2,\qquad S_2=p^2+q^2.                       \tag{2}
\]
The unique degree-one Hilbert--Burch tangent is the divided
\(q\)-gradient
\[
N=(A_{3,q},B_{3,q},S_{2,q}).                       \tag{3}
\]
It is a syzygy because it is \(p^{-1}(P_q,Q_q,R_q)\).

Write the \(r\)-dependent part allowed by \(E_7=0\) as \(\kappa rN\).
If \(\kappa=0\), then \(U,V,T\) are binary.  The \(r\)-coefficient of
\(E_6\) first kills the \(r^2\)-coefficients of \((H_2)_1,(H_2)_2\)
because \(\alpha,\beta\) are constant-linearly independent.  The
degree-\((1,1,0)\) syzygy block has nullity zero on exact \(\delta=1\);
it therefore kills the remaining \(r\)-derivatives and \(\ell_{33}\).
Every nonlinear term is binary, so the unconditional plane low-degree
exit gives an automorphism.  Hence a counterexample would require
\(\kappa\ne0\).
The coefficient of \(r\) in \(E_6\) then requires the contact curvature
\(K_N\) to satisfy
\[
K_N=\lambda\alpha+\mu\beta                         \tag{4}
\]
for constants \(\lambda,\mu\).

## 3. The double-root orbit

Take \(S_2=q^2\).  Dividing (4) by the common \(p\), its \(p^4\)
coefficient is
\[
-8(a_0b_1-a_1b_0)=0.                              \tag{5}
\]
But \(\alpha/p\) and \(\beta/p\) are both divisible by \(q\), while
\[
\left.\frac{\gamma}{p}\right|_{q=0}
 =4(a_0b_1-a_1b_0)p^5.                            \tag{6}
\]
Equations (5)--(6) make \(q\) a second common divisor.  Thus contact lies
in \(\delta\ge2\), contradicting exact \(\delta=1\).

## 4. The squarefree orbit

Take \(S_2=p^2+q^2\).  If \(a_2=0\), the coefficients of
\(q^4,pq^3,p^3q,p^2q^2\) in (4), successively, give
\[
\lambda=0,\qquad a_1=0,\qquad \mu=0,\qquad 24a_0=0,
\]
contradicting \(A_3\ne0\).

Assume \(a_2\ne0\).  A target scaling makes \(a_2=1\), and the target
shear \(B_3\mapsto B_3+cA_3\) makes \(b_2=0\), without changing either
leading \(q^3\)-coefficient in (1).  The five coefficients of (4) now
give
\[
\begin{aligned}
\lambda&=-6,&\mu&=-7a_1,\\
b_0&=\frac{(7a_0-3)a_1}{6},&
b_1&=\frac{72-24a_0+35a_1^2}{28},                 \tag{7}\\
0&=(a_0-3)(72a_0-7a_1^2+108).                     \tag{8}
\end{aligned}
\]
Put \(t=a_1\).  On the first factor \(a_0=3\), all three multipliers
share
\[
pG_1,\qquad
G_1=3tp^3-18p^2q-5tpq^2-2q^3.                    \tag{9}
\]
This has degree four.  On the second factor,
\[
a_0=\frac{7t^2}{72}-\frac32,
\]
and (7) gives
\[
b_0=\frac{t(49t^2-972)}{432},\qquad
b_1=\frac{49t^2+162}{42}.                         \tag{10}
\]
Now all three multipliers share
\[
pG_2,\qquad G_2=27p^2-7tpq-3q^2,                 \tag{11}
\]
of degree three.  Neither \(G_1\) nor \(G_2\) is the zero polynomial for
any \(t\).  Both contact families therefore lie strictly outside exact
\(\delta=1\).

Thus \(\kappa\ne0\) is impossible on the marked exact stratum.
The \(\kappa=0\) all-binary exit proves the candidate theorem.

## 5. Verification and disclosure

`verify_marked_delta1_sympy.py` reconstructs the Jacobians, the divided
gradient tangent, the contact curvature, all coefficient equations
(5)--(8), and the literal common factors (9)--(11).  The strict suite
also requires an independent PARI/GP determinant replay.

The exact scripts certify the encoded algebra.  They do not replace the
abstract Hilbert--Burch theorem, the plane low-degree theorem, the pending
hostile normalization audit, or peer review.  AI systems materially
assisted the discovery, verification, and exposition.
