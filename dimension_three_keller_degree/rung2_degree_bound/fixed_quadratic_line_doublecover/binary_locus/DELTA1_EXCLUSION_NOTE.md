# Exact \(\delta=1\) exclusion in the binary fixed-quadratic row

**First exact release:** 2026-07-25T11:20:20Z  
**Status:** research note; not peer reviewed.

## 1. Scope and theorem

Let \(p,q,r\) be source coordinates and write a degree-four map as
\[
F=L(p,q,r)^T+H_2+H_3+H_4,
\]
where \(L\in\operatorname{GL}_3(\mathbb C)\) and \(H_i\) is homogeneous
of degree \(i\).  This note treats only the binary fixed-quadratic
line-double-cover row
\[
H_4=(P,Q,0)=h(p,q)(p^2,q^2,0),\qquad \deg h=2.
\]
Put \(R=(H_3)_3\), which the top Keller identity makes binary, and
\[
\alpha=J(Q,R),\qquad\beta=-J(P,R),\qquad
\gamma=J(P,Q),\qquad
\delta=\deg\gcd(\alpha,\beta,\gamma).
\]

**Theorem.**  Every Keller map in this row on the exact \(\delta=1\)
stratum is a polynomial automorphism.  Equivalently, no Keller
counterexample lies on that stratum.

This is a row theorem, not a degree-four lower bound by itself.  The
\(\delta\ge2\) strata and the constant-dependent power fibre remain
separate frontiers.

## 2. Input: the complete \(E_6\)-contact classification

Write
\[
\det(L+zJH_2+z^2JH_3+z^3JH_4)=\sum_{i=0}^8E_i z^i.
\]
Thus \(U,V,R\) below are homogeneous cubics, \(A,B,T\) are homogeneous
quadratics, and the three \(E_7\) multiplier blocks at
\(r^2,r^1,r^0\) have coefficient degrees
\[
(0,0,-1),\qquad(1,1,0),\qquad(2,2,1),
\]
respectively.  These are weighted-matrix degrees, not component degrees.
On \(\delta=1\), Hilbert--Burch gives one degree-one tangent
\(N=(u,v,t)\), and the full \(E_7\) solution has
\[
(U_r,V_r,T_r)=\kappa N,                              \tag{1}
\]
where \(U=(H_3)_1,V=(H_3)_2,T=(H_2)_3\).
The \(r\)-coefficient of \(E_6\) requires the contact curvature
\(K_N\) to lie in \(\langle\alpha,\beta\rangle_{\mathbb C}\).

The exact contact calculation leaves, up to the full stabilizer and the
swap \(p\leftrightarrow q\), only
\[
\begin{array}{ll}
\text{B:}&h=p^2,\quad R=bp^2q+dq^3,\quad bd\ne0,\\[2mm]
\text{I:}&h=p^2+q^2,\quad R=ap^3+cpq^2,\quad
              c(a-c)\ne0.
\end{array}                                          \tag{2}
\]
The normalized tangent columns are
\[
N_{\mathrm B}=(2p^2,q^2,bq),\qquad
N_{\mathrm I}=(p^2,p^2+2q^2,cp).                    \tag{3}
\]

For completeness, the exact certificates removing every other
component are:

\[
\begin{array}{c|c|c}
h&\text{rank-drop component}&\text{contact certificate}\\ \hline
pq&a=0&70b^3,\quad6c(54bd+5c^2)\\
p(p+q)&d=0&-14c^2(3a-4b),\ 30b^3,\ 486a^3\\
p(p+q)&3a=4b&1944d^3\\
p(p+q)&a-b+c-d=0&486d^3\\
p^2&\text{generic}&
15552cd^4,\ -576d^2(27ad^2-10c^3).
\end{array}                                          \tag{4}
\]
On the interior ramification component
\(3a\eta=4b\), for
\[
h=p^2+\eta pq+q^2,
\]
the first contact coefficient is
\[
7a\eta^3-48a\eta+48c\eta-64d.                       \tag{5}
\]
After (5), three literal wedges in the chart \(a=1,c=t\) have two
resultants whose gcd is exactly \(\eta^2\).  In the \(a=0,c=1\) chart,
two wedges are
\[
192\eta(7\eta^2-48),\qquad
48\eta^2(13\eta^2-120).                              \tag{6}
\]
Thus contact forces \(\eta=0,b=d=0\), giving row I.  On the
common-root component, write
\[
h=(p-sq)(sp-q),\qquad R=(p-sq)(Ap^2+Bpq+Cq^2).
\]
Endpoint evaluations determine both contact multipliers as \(-2s\);
evaluation at \(p=sq\) then gives
\[
14s(s^2-1)^2(As^2+Bs+C)=0,                          \tag{7}
\]
which is a deeper intersection.  Finally, for \(h=(p+q)^2\),
\[
K_N\bmod(p+q)=-324q^5(a-b+c-d)^3,                   \tag{8}
\]
again routing contact to a deeper intersection.  Equations (4)--(8)
prove (2).

The abstract height-two Hilbert--Burch step and the simultaneous scalar
normalization of its power-fibre exception are independently reconstructed
in `audit_abstract_hb_e6_hostile/REPORT.md`; this note uses that audited
lemma and does not duplicate its derivation.

## 3. Branch-square survivor with every lower coefficient retained

Use the coefficient conventions
\[
\begin{aligned}
U_0&=\sum_{i=0}^3u_i p^{3-i}q^i,&
V_0&=\sum_{i=0}^3v_i p^{3-i}q^i,\\
T_0&=t_0p^2+t_1pq+t_2q^2,&
A_0&=x_0p^2+x_1pq+x_2q^2,\\
B_0&=y_0p^2+y_1pq+y_2q^2.
\end{aligned}
\]
Before imposing \(E_6\), the full family in row B is
\[
\begin{aligned}
H_3={}&(U_0+2\kappa rp^2,\,
        V_0+\kappa rq^2,\,
        bp^2q+dq^3),\\
H_2={}&(A_0+r(x_3p+x_4q)+x_5r^2,\\
&\quad B_0+r(y_3p+y_4q)+y_5r^2,\,
        T_0+\kappa bqr),
\end{aligned}                                        \tag{9}
\]
and all nine entries \(\ell_{ij}\) of \(L\) are free.

For \(bd\kappa\ne0\), exact coefficient comparison in \(E_6=0\)
gives
\[
\begin{gathered}
x_5=\kappa^2,\quad y_5=0,\quad
u_2=0,\quad t_1=bv_2,\\
y_3=\tfrac32\kappa v_0,\quad y_4=\kappa v_1,\\
x_3=\kappa(\tfrac32u_0-v_2),\quad x_4=\kappa u_1,
\quad \ell_{33}=\kappa t_0.                          \tag{10}
\end{gathered}
\]
No binary coefficient has been gauged away.  The \(r\)-coefficient of
\(E_5\) is
\[
\begin{aligned}
\frac32\kappa^2\{&
2bp^4v_0+bp^2q^2u_0-2bp^2q^2v_2
+6dp^2q^2v_0\\
&-3dq^4u_0+6dq^4v_2\},
\end{aligned}
\]
so
\[
v_0=0,\qquad u_0=2v_2.                              \tag{11}
\]
The remaining coefficient of \(E_5\) gives
\[
\begin{gathered}
x_1=u_1v_2,\qquad y_1=v_1v_2,\\
\ell_{13}=\kappa(x_0-v_2^2),\qquad
\ell_{23}=\kappa y_0,\qquad
\ell_{31}=t_0v_2.                                   \tag{12}
\end{gathered}
\]
Every coefficient not displayed in (10)--(12) remains free.

Set
\[
M_0=\kappa\ell_{11}-v_2\ell_{13},\qquad
M_3=\kappa\ell_{21}-v_2\ell_{23}.                   \tag{13}
\]
After the *full* \(E_6,E_5\) solution, with no sparse specialization,
\[
E_4=
2bM_3p^4+(bM_0+6dM_3)p^2q^2-3dM_0q^4.             \tag{14}
\]
Because \(b,d\ne0\), equation \(E_4=0\) forces \(M_0=M_3=0\).
But (10), (12), and (13) give
\[
L\begin{pmatrix}\kappa\\0\\-v_2\end{pmatrix}
=\begin{pmatrix}M_0\\M_3\\
\kappa\ell_{31}-v_2\ell_{33}\end{pmatrix}=0.         \tag{15}
\]
The vector in (15) is nonzero because \(\kappa\ne0\), contradicting
\(L\in\operatorname{GL}_3\).

## 4. Interior survivor with every lower coefficient retained

Use the same coefficient conventions.  The full family in row I is
\[
\begin{aligned}
H_3={}&(U_0+\kappa rp^2,\,
        V_0+\kappa r(p^2+2q^2),\,
        ap^3+cpq^2),\\
H_2={}&(A_0+r(x_3p+x_4q)+x_5r^2,\\
&\quad B_0+r(y_3p+y_4q)+y_5r^2,\,
        T_0+\kappa cpr).
\end{aligned}                                        \tag{16}
\]
For \(c(a-c)\kappa\ne0\), \(E_6=0\) gives
\[
\begin{gathered}
x_5=0,\quad y_5=\kappa^2,\quad
v_1=u_1,\quad t_1=cu_1,\\
x_3=\kappa u_2,\quad x_4=\tfrac32\kappa u_3,\\
y_3=\kappa v_2,\quad
y_4=\kappa(\tfrac32v_3-u_1),\quad
\ell_{33}=\kappa t_2.                               \tag{17}
\end{gathered}
\]
The \(r\)-coefficient of \(E_5\) forces
\[
u_3=0,\qquad v_3=2u_1.                              \tag{18}
\]
The remaining coefficient gives
\[
\begin{gathered}
x_1=u_1u_2,\qquad y_1=u_1v_2,\\
\ell_{13}=\kappa x_2,\qquad
\ell_{23}=\kappa(y_2-u_1^2),\qquad
\ell_{32}=t_2u_1.                                   \tag{19}
\end{gathered}
\]
Again, every coefficient not displayed remains free.

Put
\[
M_1=\kappa\ell_{12}-u_1\ell_{13},\qquad
M_4=\kappa\ell_{22}-u_1\ell_{23}.                   \tag{20}
\]
The complete \(E_4\) coefficient reduces to
\[
\begin{aligned}
E_4={}&[3aM_1+(-3a+4c)M_4]p^4\\
&+[(6a-c)M_1+cM_4]p^2q^2+2cM_1q^4.                \tag{21}
\end{aligned}
\]
Since \(c\ne0\), equation (21) first gives \(M_1=0\) and then
\(M_4=0\).  Equations (17), (19), and (20) now give the nonzero kernel
vector
\[
L\begin{pmatrix}0\\\kappa\\-u_1\end{pmatrix}
=\begin{pmatrix}M_1\\M_4\\
\kappa\ell_{32}-u_1\ell_{33}\end{pmatrix}=0,         \tag{22}
\]
again contradicting \(\det L\ne0\).

## 5. Gauge and divisor audit

The affine-linear stabilizer of the normalized top row is generated by:

- the diagonal torus in \(p,q\), together with \(p\leftrightarrow q\);
- \(r\mapsto\rho r+\lambda p+\mu q\);
- the corresponding target scalings; and
- the target row shears
  \(F_1\mapsto F_1+sF_3,\ F_2\mapsto F_2+tF_3\).

Source and target translations only move lower coefficients already
retained in (9) and (16).  Instead of choosing a gauge slice, which has
exceptional stabilizers on boundary divisors, the proof keeps every
coefficient and uses the covariants \(M_0,M_3\) and \(M_1,M_4\).
Thus (15) and (22) descend to the full quotient automatically.  In
particular, the kernel vectors are precisely the covariant forms of the
source \(r\)-shear direction; no legal gauge can turn a singular \(L\)
into an invertible one.

The exact \(E_7\) block-rank mutations are
\[
\begin{array}{c|c|c}
\text{family}&\text{parameters}&(\operatorname{rk}M_2,
\operatorname{rk}M_1,\operatorname{rk}M_0)\\ \hline
\mathrm B&b=d=1&(2,5,7)\\
\mathrm B&b=0,d=1&(2,5,6)\\
\mathrm B&b=1,d=0&(2,4,5)\\
\mathrm I&a=2,c=1&(2,5,7)\\
\mathrm I&a=1,c=0&(2,5,6)\\
\mathrm I&a=c=1&(2,4,5).
\end{array}                                          \tag{23}
\]
Thus the divisors \(b=0,d=0,c=0,a-c=0\) really leave the exact
\(\delta=1\) open and are not silently divided out.  If \(\kappa=0\),
(1) has no contact term; \(E_6\) then makes all nonlinear pieces binary
and the plane low-degree exit gives an automorphism.  Therefore every
counterexample candidate in exact \(\delta=1\) has \(\kappa\ne0\), as
used in (15) and (22).

## 6. Exact verification

Run

```text
./verify_delta1_lower_exclusion_strict.sh
```

The strict wrapper requires both:

1. a SymPy derivation from the completely general families (9), (16),
   including literal mutation guards for \(b,d,c,a-c,\kappa\) and both
   final kernel vectors; and
2. a structurally independent PARI/GP replay of the two completed
   families, the \(E_4\) collapses, kernel identities, wrong-sign kernel
   mutations, and divisor-rank table (23).

The checks certify the algebra encoded in the scripts.  They are
evidence, not peer review.

## AI-assistance disclosure

This note and its verification code were developed with substantial
AI assistance.  Every displayed identity is checked by exact symbolic
arithmetic in two independent systems, but neither those checks nor this
disclosure substitute for expert review.
