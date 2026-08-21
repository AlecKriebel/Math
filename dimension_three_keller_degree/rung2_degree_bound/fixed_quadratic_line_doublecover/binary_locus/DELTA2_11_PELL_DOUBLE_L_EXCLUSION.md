# Provisional exclusion of the \(h=p(p+q)\), doubled-\((p+q)\)
\(\delta=2,\{1,1\}\) row

**Status:** exact SymPy and independent PARI/GP replays pass; hostile
mathematical audit is pending.

**First recorded release (UTC):** 2026-07-25T13:31:29Z.

This work is not peer reviewed.  Exact checks are evidence about the
encoded algebra, not peer review.

## Theorem

No Keller counterexample in the binary fixed-quadratic
line-double-cover row lies on
\[
h=p(p+q),\qquad R=(p+q)^2(Ap+Bq),                 \tag{1}
\]
on the exact open
\[
B(5A+4B)\ne0.                                     \tag{2}
\]

This leaf is treated independently.  The proof does not assume that a
formal interchange of \(p\) and \(p+q\) preserves every marking of the
fixed row.

For \(P=hp^2,Q=hq^2\), the \(E_7\)-row gcd is \((p+q)^2\).
The two boundary divisors have gcds
\[
B=0:\ p(p+q)^2,\qquad
5A+4B=0:\ q(p+q)^2,                               \tag{3}
\]
and are routed to \(\delta=3\).  The internal pivot \(A=B\) remains
exact \(\delta=2\).

## Contact cover away from \(A=B\)

On \(A\ne B\), a polynomial \(E_7\)-tangent basis is
\[
\begin{aligned}
N_1={}&(-27Bp^2,\ q(8Ap+10Bp-9Bq),\
         5p(A-B)^2),\\
N_2={}&(3p^2(5A+4B),\
        -q(18Ap-5Aq-4Bq),\
        5q(A-B)^2).                                \tag{4}
\end{aligned}
\]
Lift \([r]E_6\) to the linear map in
\((s^2,st,t^2,x_5,y_5)\).  A single chosen maximal minor contains an
extraneous quartic factor, so it is not used alone.  Two maximal minors
are
\[
\begin{aligned}
M_0={}&-466560000B^3(A-B)^6
       (5A^2+26AB+23B^2),\\
M_1={}&-311040000B^3(A-B)^6
       (2A+7B)(5A+4B).                             \tag{5}
\end{aligned}
\]
On (2), simultaneous vanishing of (5) would require
\(2A+7B=0\) and
\[
5A^2+26AB+23B^2=-\frac{27}{4}B^2\ne0,
\]
a contradiction.  Thus the contact map is injective throughout the
\(A\ne B\) part of the exact open.

## Fresh \(A=B\) chart

At \(A=B\ne0\), rescale \(R\) to
\[
R=(p+q)^3.
\]
A fresh tangent basis is
\[
(3p^2,-q(2p-q),0),\qquad
\left(0,\frac89pq,p+q\right).                     \tag{6}
\]
The lifted contact determinant in this basis is
\[
276480\ne0.                                       \tag{7}
\]
Hence no tangent is lost through division by \(A-B\).

After the contact variables vanish, the constant \(E_6\) system has
the decisive determinant
\[
-648B^3(5A+4B),                                   \tag{8}
\]
nonzero on (2).  Therefore every nonlinear term is binary, and the
established degree-four plane-field, generic-degree descent, and
birational Keller exit proves automorphy.

This proves the theorem.

## Verification

Run

```text
./verify_delta2_11_pell_double_l_strict.sh
```

The strict wrapper requires exact whitelisted SymPy and PARI/GP
transcripts.  Both systems reconstruct the gcd boundaries, the
two-minor cover, the fresh \(A=B\) chart, and the constant \(E_6\)
determinant.  The all-binary input is recorded in
`../../WORKING_FIXED_CUBIC_LINE_ROW.md`, Section 4.

This proof was developed with AI assistance.
