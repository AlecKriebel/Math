# Provisional exclusion of the \(h=p(p+q)\), fixed-\(p\) plus
ramification-contact \(\delta=2,\{1,1\}\) row

**Status:** exact SymPy and independent PARI/GP replays pass; hostile
mathematical audit is pending.

**First recorded release (UTC):** 2026-07-25T13:47:46Z.

This work is not peer reviewed.  Exact checks are evidence about the
encoded algebra, not peer review.

## Theorem

No Keller counterexample in the binary fixed-quadratic
line-double-cover row lies on
\[
\begin{aligned}
h&=p(p+q),\\
R&=p(4Tp^2+3Tpq+Cq^2),
\end{aligned}                                     \tag{1}
\]
on the exact open
\[
C(C+T)\ne0.                                       \tag{2}
\]

For \(P=p^3(p+q)\) and \(Q=p(p+q)q^2\), the gcd of the
\(E_7\) row is \(pq\).  The two excluded coefficient boundaries were
recomputed directly:
\[
C=0:\ p^2q,\qquad C=-T:\ pq(p+q).                 \tag{3}
\]
Both have gcd degree three and fresh \(E_7\)-matrix rank five.  They
are routed to the future \(\delta\ge3\) analysis, and no determinant
valid only on (2) is used there.

## The generic contact chart

Away from \(16C-9T=0\), a polynomial basis of the two \(E_7\)
tangents is
\[
\begin{aligned}
N_1={}&\bigl(-5Cp^2,\,
 C(16p^2+22pq+q^2),\,Cp(16C-9T)\bigr),\\
N_2={}&\bigl((8C+3T)p^2,\,
 16Cpq+24Cq^2-24Tp^2-42Tpq-15Tq^2,\\
&\hspace{126pt}Cq(16C-9T)\bigr).
\end{aligned}                                     \tag{4}
\]
Writing the tangent as \(sN_1+tN_2\), lift \([r]E_6\) to the linear
map in
\[
(X,Y,Z,x_5,y_5)=(s^2,st,t^2,x_5,y_5).
\]
Its decisive determinant is
\[
27648C^5(C+T)^2(12C+7T)(16C-9T)^3.               \tag{5}
\]
Thus the contact map is injective away from the two internal divisors
\(16C-9T=0\) and \(12C+7T=0\).

## Fresh internal charts

The factor \(16C-9T\) in (5) comes from the tangent-basis pivot.
Normalize its projective parameter to \((C,T)=(9,16)\).  A fresh
complete tangent basis is
\[
\begin{aligned}
N'_1&=(-5p^2,16p^2+22pq+q^2,0),\\
N'_2&=\left(\frac89p^2,-\frac89p(3p+4q),
             \frac{8p+3q}{3}\right).
\end{aligned}                                     \tag{6}
\]
A fresh \(E_7\) rank minor is \(32805000\), and the lifted contact
determinant is
\[
422400000\ne0.                                    \tag{7}
\]
Hence the pivot divisor has full contact rank.

On the other divisor, normalize \((C,T)=(7,-12)\).  A fresh complete
tangent basis is
\[
\begin{aligned}
M_1&=\left(-\frac{p^2}{44},
 \frac{16p^2+22pq+q^2}{220},p\right),\\
M_2&=\left(\frac{p^2}{77},
 \frac{72p^2+154pq+87q^2}{385},q\right).
\end{aligned}                                     \tag{8}
\]
The lifted contact matrix has rank four, with decisive minor
\(-864/9317\), and its kernel is spanned by
\[
K=\left(-\frac{2354}{3},\frac{3773}{24},
        -\frac{539}{48},0,1\right).               \tag{9}
\]
This is not an actual tangent because
\[
K_Y^2-K_XK_Z=\frac{3053435}{192}\ne0.            \tag{10}
\]
Thus the genuine rank drop still misses the Veronese cone.

The three contact charts cover the whole exact open (2), and in every
chart
\[
s=t=x_5=y_5=0.                                   \tag{11}
\]
After (11), the remaining constant \(E_6\) block has decisive
determinant
\[
72C^2(C+T)^2,                                     \tag{12}
\]
nonzero on (2).  Hence every nonlinear term is binary.  The established
degree-four plane-field theorem, generic-degree descent, and birational
Keller theorem make the map a polynomial automorphism.  No form of the
full plane Jacobian Conjecture is used.

This proves the theorem.

## Verification

Run

```text
./verify_delta2_11_pell_p_contact_strict.sh
```

The strict wrapper requires exact whitelisted SymPy and PARI/GP
transcripts.  Both independently reconstruct the two \(\delta=3\)
boundary reruns, the generic contact determinant, both fresh internal
charts, the Veronese obstruction, and the constant \(E_6\) block.
The field/descent theorem is recorded in
`../../WORKING_FIXED_CUBIC_LINE_ROW.md`, Section 4.

This proof was developed with AI assistance.
