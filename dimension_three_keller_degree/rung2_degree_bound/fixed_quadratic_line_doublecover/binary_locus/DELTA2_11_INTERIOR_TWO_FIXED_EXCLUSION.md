# Provisional exclusion of the squarefree-interior two-fixed-root
\(\delta=2,\{1,1\}\) row

**Status:** exact SymPy and independent PARI/GP replays pass; hostile
mathematical audit is pending.

**First recorded release (UTC):** 2026-07-25T14:42:02Z.

This work is not peer reviewed.  Exact checks are evidence about the
encoded algebra, not peer review.

## Theorem

Put
\[
L=p-wq,\qquad M=wp-q,\qquad h=LM,
\]
with \(w\ne0,w^2\ne1\).  No Keller counterexample in the binary
fixed-quadratic line-double-cover row lies on
\[
R=LM(Ap+Bq)                                       \tag{1}
\]
on the exact open
\[
\begin{aligned}
E_M&=A+Bw\ne0,& E_L&=Aw+B\ne0,\\
C_p&=Aw^2+A-4Bw\ne0,&
C_q&=-4Aw+Bw^2+B\ne0.                            \tag{2}
\end{aligned}
\]

All four excluded divisors were recomputed directly:
\[
\begin{array}{c|c}
E_M=0&LM^2\\
E_L=0&L^2M\\
C_p=0&qLM\\
C_q=0&pLM.
\end{array}                                       \tag{3}
\]
They have \(\delta\ge3\) and are routed.  The values \(w=0,w^2=1\)
leave the squarefree interior fixed-divisor orbit.

## Complete \(E_7\) tangent basis

A polynomial basis for the two \(E_7\) tangents is
\[
\begin{aligned}
N_1={}&\bigl(
p(4Apw+5Bpw^2+5Bp-6Bqw),\\
&\qquad q(4Aqw+6Bpw-Bqw^2-Bq),\,
3pE_ME_L\bigr),\\
N_2={}&\bigl(
-p(Apw^2+Ap-6Aqw-4Bpw),\\
&\qquad -q(6Apw-5Aqw^2-5Aq-4Bqw),\,
3qE_ME_L\bigr).
\end{aligned}                                     \tag{4}
\]
The full \(E_7\) coefficient matrix has the decisive rank-six minor
\[
24w^6E_M^2(w-1)^2(w+1)^2E_L^2C_qC_p,             \tag{5}
\]
nonzero on (2).

## Rank-four contact kernel

Lift \([r]E_6\) to the linear coefficient map in
\[
(X,Y,Z,x_5,y_5)=(s^2,st,t^2,x_5,y_5).
\]
Its rank is four, with decisive minor
\[
-41472w^5E_M^4E_L^4C_qC_p.                       \tag{6}
\]
The complete kernel is spanned by
\[
K=(K_X,K_Y,K_Z,K_4,K_5),                         \tag{7}
\]
where
\[
\begin{aligned}
K_X={}&5A^2w^4-14A^2w^2+5A^2
 -4ABw^3-4ABw-4B^2w^2,\\
K_Y={}&2A^2w^3+2A^2w
 +7ABw^4-6ABw^2+7AB\\
&\qquad+2B^2w^3+2B^2w,\\
K_Z={}&-4A^2w^2-4ABw^3-4ABw
 +5B^2w^4-14B^2w^2+5B^2,\\
K_4={}&K_5=-36wE_M^2E_L^2.
\end{aligned}                                     \tag{8}
\]
An actual tangent must satisfy \(Y^2=XZ\), but the exact obstruction is
\[
K_Y^2-K_XK_Z
=24E_M^2(w-1)^2(w+1)^2E_L^2\ne0.                 \tag{9}
\]
Hence the lifted kernel contains no nonzero actual tangent, and all
tangent and quadratic-\(r\) variables vanish.

The remaining constant \(E_6\) block has decisive determinant
\[
-8w^5E_M(w-1)^2(w+1)^2E_LC_qC_p,                 \tag{10}
\]
also nonzero on the exact open.  Every nonlinear term is therefore
binary.  The established degree-four plane-field theorem,
generic-degree descent, and birational Keller theorem make the map a
polynomial automorphism.  No form of the full plane Jacobian
Conjecture is used.

This proves the theorem.

## Verification

Run

```text
./verify_delta2_11_interior_two_fixed_strict.sh
```

The strict wrapper requires exact whitelisted SymPy and PARI/GP
transcripts.  Both independently reconstruct the four boundary gcds,
the complete tangent basis, the rank-four minor, the full kernel and
Veronese obstruction, and the constant \(E_6\) block.  The all-binary
exit is recorded in `../../WORKING_FIXED_CUBIC_LINE_ROW.md`,
Section 4.

This proof was developed with AI assistance.
