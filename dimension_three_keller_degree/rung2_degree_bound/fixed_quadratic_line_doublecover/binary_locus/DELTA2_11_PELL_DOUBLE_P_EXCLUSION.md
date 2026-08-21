# Provisional exclusion of the \(h=p(p+q)\), doubled-\(p\)
\(\delta=2,\{1,1\}\) row

**Status:** exact SymPy and independent PARI/GP replays pass; hostile
mathematical audit is pending.

**First recorded release (UTC):** 2026-07-25T13:24:34Z.

This work is not peer reviewed.  Exact checks are evidence about the
encoded algebra, not peer review.

## Theorem

No Keller counterexample in the binary fixed-quadratic
line-double-cover row lies on
\[
h=p(p+q),\qquad R=p^2(Ap+Bq),                     \tag{1}
\]
on the exact open
\[
B(A-B)(3A-4B)\ne0.                                \tag{2}
\]

For \(P=hp^2,Q=hq^2\), the \(E_7\)-row gcd is \(p^2\).
The three excluded divisors in (2) have gcds
\[
\begin{array}{c|c}
B=0&p^3\\
A=B&p^2(p+q)\\
3A=4B&p^2q,
\end{array}                                        \tag{3}
\]
so each is genuinely routed to \(\delta=3\).  The endpoint \(A=0\)
remains exact \(\delta=2\) and is retained.

## Complete \(E_6\) obstruction

A polynomial basis of the two \(E_7\) tangents is
\[
\begin{aligned}
N_1={}&(p^2,q(2p+3q),Bp),\\
N_2={}&(-p(9Ap-12Bp-8Bq),\\
       &\qquad-q(18Ap+27Aq-4Bq),5B^2q).
\end{aligned}                                      \tag{4}
\]
Lift \([r]E_6\) to the coefficient map in
\((s^2,st,t^2,x_5,y_5)\).  Its first five rows have determinant
\[
-6220800B^5(A-B)^2(3A-4B),                        \tag{5}
\]
which is nonzero on (2).  Hence both tangent parameters and both
quadratic \(r\)-coefficients vanish.

The remaining constant \(E_6\) system in the two linear-in-\(r\)
coefficients of \(H_{2,1},H_{2,2}\) and \(\ell_{33}\) has determinant
\[
-1080B(A-B)^2(3A-4B).                              \tag{6}
\]
It is also full rank.  Thus every nonlinear term is binary.

The established degree-four plane-field theorem, generic-degree
descent, and birational Keller theorem now make the map a polynomial
automorphism.  This uses no form of the full plane Jacobian
Conjecture, proving the theorem.

## Verification

Run

```text
./verify_delta2_11_pell_double_p_strict.sh
```

The strict wrapper requires exact whitelisted SymPy and PARI/GP
transcripts.  Both systems recompute every divisor in (3), the tangent
basis, and the two decisive determinants.  The all-binary theorem is
recorded in `../../WORKING_FIXED_CUBIC_LINE_ROW.md`, Section 4.

This proof was developed with AI assistance.
