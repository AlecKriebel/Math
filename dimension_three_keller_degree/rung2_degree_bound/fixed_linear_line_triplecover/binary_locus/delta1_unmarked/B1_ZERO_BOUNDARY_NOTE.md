# The \(b_1=0\) unmarked boundary has no exact-\(\delta=1\) contact

**Exact candidate checkpoint:** 2026-07-25T14:04:18Z  
**Status:** complete primary proof; pending independent hostile audit; not
peer reviewed.

## 1. Normalized boundary

On the unmarked chart, assume \(a_2c_0\ne0\) but \(b_1=0\).
The source and target stabilizers normalize
\[
a_2=c_0=1,\qquad b_2=0.
\]
Writing \(a=a_3,b=b_3,c=c_2,d=c_3\), the leading forms are
\[
\begin{aligned}
P&=p(pq^2+aq^3),\\
Q&=p(p^3+bq^3),\\
R&=p^3+cpq^2+dq^3.                              \tag{1}
\end{aligned}
\]
The marked factor of \(P,Q\) is \(p\), while the proposed unmarked
Hilbert--Burch divisor is \(q\).

**Candidate theorem.**  Every Keller map on the exact-\(\delta=1\)
part of this boundary is an automorphism.

## 2. Contact equations

Let
\[
\alpha=J(Q,R),\qquad\beta=-J(P,R),\qquad
\gamma=J(P,Q),
\]
and use the divided directional-gradient tangent
\[
N=q^{-1}\partial_q(P,Q,R).
\]
The first contact coefficient gives
\[
d=ac+\frac34b.                                   \tag{2}
\]
After (2), three subsequent coefficients include
\[
\begin{aligned}
4c\lambda+3\mu&=0,                               \tag{3}\\
4ac\lambda+3a\mu-2bc&=0,                         \tag{4}\\
12abc+9b^2+4c\mu&=0.                             \tag{5}
\end{aligned}
\]
Subtracting \(a\) times (3) from (4) gives \(bc=0\).
If \(c=0\), equation (5) gives \(b=0\).  If \(c\ne0\), then \(bc=0\)
again gives \(b=0\).  Thus every contact point has
\[
b=0,\qquad d=ac.                                 \tag{6}
\]
(When \(c\ne0\), (3) and (5) additionally give
\(\lambda=\mu=0\), but this is not needed.)

## 3. Gcd jump

Substitution of (6) yields the literal factorizations
\[
\begin{aligned}
\alpha&=4cp^3q(2p+3aq),\\
\beta&=q(2p+3aq)(3p^3-cpq^2-acq^3),\\
\gamma&=-4p^4q(2p+3aq).                          \tag{7}
\end{aligned}
\]
Therefore every contact point has the common divisor
\[
q(2p+3aq),
\]
of degree two.  The second factor cannot vanish as a polynomial because
its \(p\)-coefficient is \(2\).  Hence no contact point of this boundary
lies in exact \(\delta=1\).

For a Keller map in exact \(\delta=1\), the tangent parameter must
therefore be zero.  The injective zero-tangent lower block from the
binary fixed-linear lemma makes all nonlinear terms binary.  The
plane-plus-shear exit, together with the unconditional plane
degree bound, then gives an automorphism.

## 4. Verification and disclosure

`verify_b1_zero_sympy.py` and `verify_b1_zero_pari.gp` independently
reconstruct the contact coefficients and (7); the strict wrapper
requires both.

The exact checks certify the encoded algebra, not the normal-form
exhaustion or the inherited zero-tangent lemma.  This result is pending
hostile review, has not been peer reviewed, and is not a scholarly
priority claim.  AI systems materially assisted the discovery,
verification, and exposition.
