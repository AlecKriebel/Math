# Provisional exclusion of the \(h=pq\), doubled-contribution
\(\delta=2,\{1,1\}\) row

**Status:** exact SymPy and independent PARI/GP replays pass; hostile
mathematical audit is pending.

**First recorded release (UTC):** 2026-07-25T13:17:07Z.

This work is not peer reviewed.  Exact checks are evidence about the
encoded algebra, not peer review.

## Theorem

No Keller counterexample in the binary fixed-quadratic
line-double-cover row lies on
\[
h=pq,\qquad R=p^2(Ap+Bq),\qquad AB\ne0,            \tag{1}
\]
up to the swap \(p\leftrightarrow q\).

For
\[
P=p^3q,\qquad Q=pq^3,
\]
the exact gcd is \(p^2\), so (1) has
\(\delta=2\).  At \(A=0\) and \(B=0\) the gcds become \(p^2q\) and
\(p^3\), respectively; both mutations are routed to \(\delta\ge3\).
There is no internal pivot divisor on the exact open.

## Complete \(E_6\) contact obstruction

A polynomial basis of the two \(E_7\) tangents is
\[
\begin{aligned}
N_1&=(5Bp^2,15Bq^2,5B^2p),\\
N_2&=(-p(9Ap-8Bq),-27Aq^2,5B^2q).                \tag{2}
\end{aligned}
\]
For \(N=sN_1+tN_2\), lift \([r]E_6\) to the linear coefficient map in
\[
(X,Y,Z,x_5,y_5)=(s^2,st,t^2,x_5,y_5).
\]
The determinant of its first five coefficient rows is
\[
-2332800000A^3B^8.                                \tag{3}
\]
It is nonzero throughout (1).  Therefore
\[
s=t=x_5=y_5=0.                                    \tag{4}
\]

After (4), \(U,V,T\) are binary and the constant part of \(E_6\) is
\[
\alpha(a_0p+a_1q)+\beta(b_0p+b_1q)+\gamma\ell_{33},
\]
where
\[
\alpha=J(Q,R),\quad\beta=-J(P,R),\quad
\gamma=J(P,Q).
\]
The first five coefficient rows of this \(7\times5\) system have
determinant
\[
-3240A^3B.                                        \tag{5}
\]
Thus the two linear-in-\(r\) coefficients of each of \(H_{2,1}\) and
\(H_{2,2}\), together with \(\ell_{33}\), also vanish.  Every nonlinear
term is now binary.

Choose a target component with nonzero \(r\)-coefficient in the
invertible linear part, triangularize it to the third coordinate, and
view the first two components over the resulting function field.  They
form a plane Keller map of degree at most four.  The unconditional
plane low-degree theorem, generic-degree descent, and the birational
Keller theorem give a polynomial automorphism.  This is the established
all-binary exit; it uses no form of the full plane Jacobian Conjecture.

Hence (1) contains no Keller counterexample.

## Verification

Run

```text
./verify_delta2_11_pq_double_strict.sh
```

The strict wrapper requires exact whitelisted SymPy and PARI/GP
transcripts.  Both systems reconstruct the gcd mutations, tangent
syzygies, contact determinant (3), and constant determinant (5).
The field/descent input is recorded in
`../../WORKING_FIXED_CUBIC_LINE_ROW.md`, Section 4.

This proof was developed with AI assistance.
