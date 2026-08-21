# Provisional exclusion of the \(h=p(p+q)\), fixed-\((p+q)\) plus
ramification-contact \(\delta=2,\{1,1\}\) row

**Status:** exact SymPy and independent PARI/GP replays pass; hostile
mathematical audit is pending.

**First recorded release (UTC):** 2026-07-25T13:54:16Z.

This work is not peer reviewed.  Exact checks are evidence about the
encoded algebra, not peer review.

## Theorem

No Keller counterexample in the binary fixed-quadratic
line-double-cover row lies on
\[
\begin{aligned}
h&=p(p+q),\\
R&=(p+q)(-4Bp^2+Bpq+Cq^2),
\end{aligned}                                     \tag{1}
\]
on the exact open
\[
C(5B-C)\ne0.                                      \tag{2}
\]

For \(P=p^3(p+q)\) and \(Q=p(p+q)q^2\), the gcd of the
\(E_7\) row is \(q(p+q)\).  The excluded coefficient boundaries were
recomputed directly:
\[
C=0:\ pq(p+q),\qquad C=5B:\ q(p+q)^2.             \tag{3}
\]
Both have gcd degree three and fresh \(E_7\)-matrix rank five.  They
are routed to the future \(\delta\ge3\) analysis; no open-chart
determinant is evaluated there.

## The generic contact chart

Away from \(B+16C=0\), a polynomial basis of the complete two-tangent
\(E_7\) kernel is
\[
\begin{aligned}
N_1={}&\bigl(-27Cp^2,\,
 8Bp^2+8Bpq-16Cp^2+2Cpq-9Cq^2,\\
&\hspace{118pt}p(B+16C)(5B-C)\bigr),\\
N_2={}&\bigl(3p^2(5B+8C),\,
 72Bp^2+62Bpq+5Bq^2-16Cpq+8Cq^2,\\
&\hspace{118pt}q(B+16C)(5B-C)\bigr).
\end{aligned}                                     \tag{4}
\]
Lifting \([r]E_6\) to the coefficient map in
\((s^2,st,t^2,x_5,y_5)\) gives the decisive determinant
\[
-746496C^3(B+16C)^3(5B-4C)(5B-C)^4.              \tag{5}
\]
It is injective away from the two internal divisors
\(B+16C=0\) and \(5B-4C=0\).

## Fresh internal charts

The first internal factor is a tangent-basis pivot.  Normalize it to
\((B,C)=(-16,1)\).  A fresh complete basis is
\[
\begin{aligned}
N'_1&=(3p^2,16p^2+14pq+q^2,0),\\
N'_2&=\left(0,\frac89p(p+q),-8p+q\right).
\end{aligned}                                     \tag{6}
\]
A fresh \(E_7\) rank minor is \(-157464\), while the contact
determinant is
\[
6967296\ne0.                                      \tag{7}
\]

On the genuine contact-rank divisor, normalize to \((B,C)=(4,5)\).
A fresh complete basis is
\[
\begin{aligned}
M_1&=\left(-\frac{3p^2}{28},
 -\frac{16p^2-14pq+15q^2}{420},p\right),\\
M_2&=\left(\frac{p^2}{7},
 \frac{24p^2+14pq+5q^2}{105},q\right).
\end{aligned}                                     \tag{8}
\]
The lifted contact map has rank four, with decisive minor \(120/343\)
and kernel
\[
K=\left(-840,-\frac{945}{2},-\frac{945}{4},0,1\right).
                                                               \tag{9}
\]
Its Veronese obstruction is
\[
K_Y^2-K_XK_Z=\frac{99225}{4}\ne0.                \tag{10}
\]
Thus no actual nonzero tangent survives on this divisor.

The three charts cover (2), so all tangent and quadratic-\(r\)
variables vanish.  The remaining constant \(E_6\) block has decisive
determinant
\[
-648C^3(5B-C),                                    \tag{11}
\]
nonzero on (2).  Hence every nonlinear term is binary.  The established
degree-four plane-field theorem, generic-degree descent, and birational
Keller theorem make the map a polynomial automorphism.  No form of the
full plane Jacobian Conjecture is used.

This proves the theorem.

## Verification

Run

```text
./verify_delta2_11_pell_l_contact_strict.sh
```

The strict wrapper requires exact whitelisted SymPy and PARI/GP
transcripts.  Both independently reconstruct the two boundary reruns,
the generic determinant, both fresh internal charts, the Veronese
obstruction, and the constant \(E_6\) block.  The field/descent theorem
is recorded in `../../WORKING_FIXED_CUBIC_LINE_ROW.md`, Section 4.

This proof was developed with AI assistance.
