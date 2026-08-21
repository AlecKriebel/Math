# Provisional exclusion of the \(h=p(p+q)\), two-fixed-root
\(\delta=2,\{1,1\}\) row

**Status:** exact SymPy and independent PARI/GP replays pass; hostile
mathematical audit is pending.

**First recorded release (UTC):** 2026-07-25T13:39:13Z.

This work is not peer reviewed.  Exact checks are evidence about the
encoded algebra, not peer review.

## Theorem

No Keller counterexample in the binary fixed-quadratic
line-double-cover row lies on
\[
h=p(p+q),\qquad R=p(p+q)(Ap+Bq),                 \tag{1}
\]
on the exact open
\[
B(A-B)(A+4B)\ne0.                                \tag{2}
\]

For
\[
P=p^3(p+q),\qquad Q=p(p+q)q^2,
\]
the gcd of the \(E_7\) row is \(p(p+q)\).  The three boundary
recomputations are
\[
\begin{array}{c|c}
B=0& p^2(p+q)\\
A=B& p(p+q)^2\\
A=-4B&pq(p+q).
\end{array}                                      \tag{3}
\]
Each has gcd degree three and is routed to the future
\(\delta\ge3\) analysis rather than divided away.  A fresh computation
on each boundary also gives \(E_7\)-matrix rank five, whereas the
matrix has rank six on (2).

## Contact kernel and Veronese obstruction

A polynomial basis of the complete two-dimensional \(E_7\) tangent
space on (2) is
\[
\begin{aligned}
N_1={}&\bigl(5Bp^2,-Bq(6p+q),3Bp(A-B)\bigr),\\
N_2={}&\bigl(-(A+4B)p^2,\,
 q(6Ap+5Aq-4Bq),\,3Bq(A-B)\bigr).
\end{aligned}                                    \tag{4}
\]
Indeed, a decisive \(6\times6\) minor of the full \(E_7\) coefficient
matrix is
\[
24B^3(A-B)^2(A+4B).                              \tag{5}
\]

Write a tangent as \(sN_1+tN_2\), and lift \([r]E_6\) to the linear
coefficient map in
\[
(X,Y,Z,x_5,y_5)=(s^2,st,t^2,x_5,y_5).
\]
Its rank is four on (2), as certified by the minor
\[
-41472B^5(A-B)^4(A+4B).                          \tag{6}
\]
The complete kernel is spanned by
\[
\begin{aligned}
K=\bigl(&-(5A^2+4AB-4B^2),\,
         -B(7A-2B),\,-5B^2,\,0,\\
       &36B^2(A-B)^2\bigr).
\end{aligned}                                    \tag{7}
\]
An actual tangent must lie on the Veronese cone \(Y^2=XZ\), but
\[
K_Y^2-K_XK_Z=24B^2(A-B)^2\ne0                  \tag{8}
\]
on (2).  Thus the lifted kernel contains no nonzero actual tangent,
and
\[
s=t=x_5=y_5=0.                                   \tag{9}
\]

After (9), the constant \(E_6\) block in the two linear-in-\(r\)
coefficients of each of the first two components and \(\ell_{33}\)
has decisive determinant
\[
8B^2(A-B)(A+4B).                                 \tag{10}
\]
It is full rank on (2), so every nonlinear term is binary.  The
established degree-four plane-field theorem, generic-degree descent,
and birational Keller theorem make the map a polynomial automorphism.
No form of the full plane Jacobian Conjecture is used.

This proves the theorem.

## Verification

Run

```text
./verify_delta2_11_pell_two_fixed_strict.sh
```

The strict wrapper requires exact whitelisted SymPy and PARI/GP
transcripts.  Both systems independently reconstruct the three
boundary gcds and fresh \(E_7\) ranks, the full tangent basis, the
rank-four kernel, the Veronese obstruction, and the constant
\(E_6\) minor.  The field/descent theorem is recorded in
`../../WORKING_FIXED_CUBIC_LINE_ROW.md`, Section 4.

This proof was developed with AI assistance.
