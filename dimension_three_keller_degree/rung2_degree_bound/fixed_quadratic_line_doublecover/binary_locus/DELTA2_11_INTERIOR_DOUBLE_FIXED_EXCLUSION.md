# Provisional exclusion of the squarefree-interior doubled-fixed-root
\(\delta=2,\{1,1\}\) row

**Status:** exact SymPy and independent PARI/GP replays pass; hostile
mathematical audit is pending.

**First recorded release (UTC):** 2026-07-25T14:28:58Z.

This work is not peer reviewed.  Exact checks are evidence about the
encoded algebra, not peer review.

## Theorem

Put
\[
L=p-wq,\qquad M=wp-q,\qquad h=LM,
\]
and assume
\[
w\ne0,\qquad w^2\ne1.                              \tag{1}
\]
No Keller counterexample in the binary fixed-quadratic
line-double-cover row lies on
\[
R=L^2(Ap+Bq)                                      \tag{2}
\]
on the exact open
\[
\begin{aligned}
E&=A+Bw\ne0,\\
C_p&=5Aw^2-3A-4Bw\ne0,\\
C_q&=4Aw+3Bw^2-5B\ne0.                            \tag{3}
\end{aligned}
\]

The conditions have their literal incidence meanings.  Direct gcd
recomputation gives
\[
\begin{array}{c|c}
E=0&L^2M\\
C_p=0&qL^2\\
C_q=0&pL^2.
\end{array}                                       \tag{4}
\]
Thus these three divisors have \(\delta\ge3\) and are routed rather
than divided away.  The values \(w=0,w^2=1\) leave the squarefree
interior fixed-divisor orbit.  They belong to already separated
boundary fixed-divisor charts.

## The generic tangent chart

Set
\[
D=Aw+B.                                           \tag{5}
\]
First assume \(D\ne0\).  A complete polynomial basis for the two
\(E_7\) tangents is \(N_1=(U_1,V_1,T_1)\),
\(N_2=(U_2,V_2,T_2)\), where
\[
\begin{aligned}
U_1={}&p(4Apw+27Bpw^2-5Bp-18Bqw),\\
V_1={}&-q(8Apw^2-12Aqw-10Bpw-9Bqw^2+15Bq),\\
T_1={}&5pD^2,\\
U_2={}&-p(15Apw^2-9Ap-10Aqw-12Bpw+8Bq),\\
V_2={}&-q(18Apw+5Aqw^2-27Aq-4Bqw),\\
T_2={}&5qD^2.
\end{aligned}                                     \tag{6}
\]
The decisive \(E_7\) rank minor is
\[
360E^2(w-1)^2(w+1)^2D^2C_qC_p,                   \tag{7}
\]
so (6) is complete on this chart.

Lift \([r]E_6\) to the linear coefficient map in
\[
(X,Y,Z,x_5,y_5)=(s^2,st,t^2,x_5,y_5).
\]
Four of its maximal minors have the form
\[
\begin{aligned}
\Delta_1&=\mathcal B w^2Q_1,&
\Delta_2&=-\mathcal B w^2Q_2,\\
\Delta_3&=-\mathcal B w^2Q_3,&
\Delta_4&=\mathcal B wQ_4,
\end{aligned}                                     \tag{8}
\]
where
\[
\mathcal B=1920000(w-1)^3(w+1)^3D^6C_qC_p.        \tag{9}
\]

It remains to prove that the residual \(Q_i\) cannot vanish
simultaneously.  This is a genuinely multivariate issue: a gcd of the
maximal minors would not suffice.

### The \(B\ne0\) projective chart

Normalize \(B=1\) and write \(a=A/B\).  The residual cubics in \(a\)
are
\[
\begin{aligned}
Q_1={}&a^3(108w^5-266w^3)
 +a^2(216w^6-855w^4+165w^2)\\
&+a(108w^7-972w^5+450w^3-60w)
 -378w^6+270w^4-45w^2-5,\\
Q_2={}&a^3(127w^4-285w^2)
 +a^2(294w^5-954w^3+186w)\\
&+a(162w^6-978w^4+357w^2-15)
 -324w^5+186w^3-20w,\\
Q_3={}&a^3(20w^5-186w^3+324w)
 +a^2(15w^6-357w^4+978w^2-162)\\
&+a(-186w^5+954w^3-294w)+285w^4-127w^2,\\
Q_4={}&a^3(5w^7+45w^5-270w^3+378w)
 +a^2(60w^6-450w^4+972w^2-108)\\
&+a(-165w^5+855w^3-216w)+266w^4-108w^2.
\end{aligned}                                     \tag{10}
\]
Exact elimination in \(a\) gives
\[
\begin{aligned}
\operatorname{Res}(Q_1,Q_2)
={}&637729200w^6(w^2-1)^{12}
 (12w^4+28w^2-57),\\
\operatorname{Res}(Q_1,Q_3)
={}&-318864600w^3(w^2-1)^{12}(w^2+3)^2\\
&\hspace{60pt}\cdot(18w^4-27w^2-8),\\
\operatorname{Res}(Q_1,Q_4)
={}&1434890700w^3(w^2-1)^{12}\\
&\hspace{20pt}\cdot(14w^{12}+28w^{10}+77w^8-34w^6\\
&\hspace{120pt}+77w^4+28w^2+14),\\
\operatorname{Res}(Q_2,Q_3)
={}&-159432300w^4(w^2-1)^{12}
 (23w^4-114w^2+23).
\end{aligned}                                     \tag{11}
\]
The monic gcd of the four resultants is exactly
\[
w^3(w^2-1)^{12}.                                  \tag{12}
\]
Conditions (1) therefore rule out a common zero of all four residual
minors.

### The \(B=0\) endpoint

Normalize \(A=1\).  The first two residuals have univariate gcd
\[
\gcd(Q_1,Q_2)=w^2
\quad\hbox{up to a nonzero scalar}.                \tag{13}
\]
Again (1) rules out simultaneous vanishing.  Equations (8)--(13)
therefore prove that the lifted contact map is injective throughout
the \(D\ne0\) part of the exact open.

## Fresh triple-fixed-root pivot

The divisor \(D=0\) remains inside exact \(\delta=2\).  Normalize
\((A,B)=(1,-w)\); then \(R=L^3\).  Conditions (3) become
\[
w^2\ne\frac13,\qquad w^2\ne3.                    \tag{14}
\]
A fresh complete tangent basis is
\[
\begin{aligned}
N'_1={}&\bigl(9pw(3pw^2-p-2qw),\,
 9qw(2pw+qw^2-3q),\,0\bigr),\\
N'_2={}&\bigl(8p(4pw-3q),\,8pqw^2,\,
 -9L(w^2-3)\bigr).
\end{aligned}                                     \tag{15}
\]
The fresh lifted contact determinant is
\[
48977602560w^5(w-1)^6(w+1)^6
\,(w^2-3)^4(3w^2-1),                              \tag{16}
\]
which is nonzero by (1) and (14).

Thus every tangent and quadratic-\(r\) variable vanishes on the entire
exact open.  The remaining constant \(E_6\) block has decisive
determinant
\[
-216E^2(w-1)^2(w+1)^2C_qC_p,                     \tag{17}
\]
also nonzero there.  Every nonlinear term is therefore binary.  The
established degree-four plane-field theorem, generic-degree descent,
and birational Keller theorem make the map a polynomial automorphism.
No form of the full plane Jacobian Conjecture is used.

This proves the theorem.

## Verification

Run

```text
./verify_delta2_11_interior_double_fixed_strict.sh
```

The strict wrapper requires exact whitelisted SymPy and PARI/GP
transcripts.  Both reconstruct (4), four literal maximal-minor
identities, all four resultants and their gcd, the projective endpoint,
the fresh pivot chart, and the constant \(E_6\) block.  The all-binary
exit is recorded in `../../WORKING_FIXED_CUBIC_LINE_ROW.md`,
Section 4.

This proof was developed with AI assistance.
