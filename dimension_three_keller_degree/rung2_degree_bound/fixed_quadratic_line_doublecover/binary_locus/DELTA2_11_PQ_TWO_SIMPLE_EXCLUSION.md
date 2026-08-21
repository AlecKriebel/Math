# Provisional exclusion of the \(h=pq\), two-simple-contribution
\(\delta=2,\{1,1\}\) row

**Status:** exact SymPy and independent PARI/GP replays pass; hostile
mathematical audit is pending.

**First recorded release (UTC):** 2026-07-25T13:20:14Z.

This work is not peer reviewed.  Exact checks are evidence about the
encoded algebra, not peer review.

## Theorem

No Keller counterexample in the binary fixed-quadratic
line-double-cover row lies on
\[
h=pq,\qquad R=pq(Ap+Bq),\qquad AB\ne0.             \tag{1}
\]

For \(P=p^3q,Q=pq^3\), the gcd of the \(E_7\) row is \(pq\).
At \(A=0\) and \(B=0\), the gcds become \(pq^2\) and \(p^2q\);
these are \(\delta=3\) mutations and are routed rather than divided
away.

## Contact kernel and Veronese obstruction

A polynomial basis of the two degree-\((2,2,1)\) \(E_7\) tangents is
\[
N_1=(5p^2,-q^2,3Ap),\qquad
N_2=(-p^2,5q^2,3Bq).                               \tag{2}
\]
Lift \([r]E_6\) to the linear coefficient map in
\[
(X,Y,Z,x_5,y_5)=(s^2,st,t^2,x_5,y_5).
\]
Its rank is four on (1).  A decisive \(4\times4\) minor is
\[
5760A^2B^2,                                        \tag{3}
\]
and its complete kernel is spanned by
\[
K=(1,7/5,1,0,0).                                   \tag{4}
\]
An actual tangent must satisfy the Veronese equation \(Y^2=XZ\), but
\[
K_Y^2-K_XK_Z=\frac{24}{25}\ne0.                   \tag{5}
\]
Thus no nonzero tangent lies in the lifted kernel, and
\[
s=t=x_5=y_5=0.                                    \tag{6}
\]

After (6), the constant \(E_6\) block in the two linear-in-\(r\)
coefficients of \(H_{2,1},H_{2,2}\) and \(\ell_{33}\) has a decisive
minor
\[
8A^2B^2.                                           \tag{7}
\]
It is full rank, so every nonlinear term is binary.  The established
degree-four plane-field theorem, generic-degree descent, and the
birational Keller theorem make the map a polynomial automorphism.
No form of the full plane Jacobian Conjecture is used.

This proves the theorem.  Together with the doubled-contribution
companion note, it provisionally eliminates every exact-\(\delta=2\),
\(\{1,1\}\) leaf on the \(h=pq\) fixed-divisor orbit.

## Verification

Run

```text
./verify_delta2_11_pq_two_simple_strict.sh
```

The strict wrapper requires exact whitelisted SymPy and PARI/GP
transcripts.  Both reconstruct the gcd mutations, tangent basis,
rank-four kernel, Veronese obstruction, and constant \(E_6\) minor.
The field/descent theorem is recorded in
`../../WORKING_FIXED_CUBIC_LINE_ROW.md`, Section 4.

This proof was developed with AI assistance.
