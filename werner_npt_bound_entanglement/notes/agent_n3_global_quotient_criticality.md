# Global quotient criticality and the pair-centered Haar obstruction

## Status

This note derives the complete first-order system for a hypothetical
global minimizer of the strengthened-face quotient
\[
 \frac{k}{\sigma}
 =
 \frac{\langle z,K(V)z\rangle}
      {\langle z,S_Vz\rangle}.
 \tag{1}
\]
It also gives a new criticality-specific nonlinear realizability
condition.

The quotient (1) is a strictly increasing fractional-linear function
of
\[
 \lambda=\frac{Q_3(C)}{\|\Pi _2C\|_2^2}.
 \tag{2}
\]
Thus a hypothetical negative global minimizer can be studied directly
on the smooth rank-two determinantal variety.  If
\[
 {\cal A}=L^{\otimes3},\qquad {\cal P}=\Pi _2,\qquad
 D={\cal P}C,\qquad c=\|D\|_2^2,
 \tag{3}
\]
then its shifted gradient
\[
 R=({\cal A}-\lambda{\cal P})C
 \tag{4}
\]
is supported entirely between the orthogonal complements of the two
singular planes:
\[
 \boxed{
 U^\dagger R=0,\qquad RV=0
 }
 \tag{5}
\]
for \(C=U\Sigma V^\dagger\).  These are exactly the missing
\(V,z\) Euler--Lagrange equations in intrinsic form.

For every site and on both the left and the right, define a
pair-centered \(3\times3\) matrix
\[
\begin{aligned}
 M_i^L&=\frac1c\operatorname{Tr}_{\widehat i}(CD^\dagger),\\
 M_i^R&=\frac1c\operatorname{Tr}_{\widehat i}(D^\dagger C),
 \qquad
 H_i^{L,R}=\frac12(M_i^{L,R}+M_i^{L,R\dagger}).
\end{aligned}
\tag{6}
\]
Both Hermitian matrices have trace one, but need not be positive.
Let their ordered eigenvalues be
\[
 \nu_1\geq\nu_2\geq\nu_3,\qquad
 \nu_1+\nu_2+\nu_3=1,
\tag{7}
\]
and put
\[
 {\cal R}(H)=
 \sum_{\nu_r>1/2}
 \frac{(\nu_r-\frac12)^3}
 {\displaystyle\prod_{s\ne r}(\nu_r-\nu_s)}.
\tag{8}
\]
At repeated eigenvalues, (8) means its continuous divided-difference
extension.  Equivalently, it is the second divided difference of the
convex function \(t\mapsto(t-\frac12)_+^3\), so
\({\cal R}(H)\geq0\).  If only \(\nu_1\) exceeds \(1/2\), (8) reduces
to the single fraction displayed in the first version of this
reduction.
Then every negative global minimizer obeys the six exact inequalities
\[
\boxed{
 g_i(C)\geq
 \frac{16(-Q_3(C))}{15}\,
 {\cal R}(H_i^L),
 \qquad
 g_i(C)\geq
 \frac{16(-Q_3(C))}{15}\,
 {\cal R}(H_i^R).
}
\tag{9}
\]

This is not a generic negative-depth estimate.  It uses the full
Euler equation (5), with the normalization supplied by the pair
sector rather than by the Hilbert--Schmidt norm.  In terms of the
triple-Hodge fusion variables
\[
 G=\sum_i g_i,\qquad
 a=\|\Pi _1C\|_2^2,\qquad
 \Xi=\|C\|_2^2+6{\cal J}_3(C),
\tag{10}
\]
put
\[
 {\cal D}=108c-204G-45a-16\Xi=-640Q_3(C)>0.
\tag{11}
\]
Equation (9) becomes
\[
\boxed{
 g_i\geq\frac{{\cal D}}{600}
 \max\{{\cal R}(H_i^L),{\cal R}(H_i^R)\}.
}
\tag{12}
\]
Consequently
\[
\boxed{
 600G\geq{\cal D}\sum_i
 \max\{{\cal R}(H_i^L),{\cal R}(H_i^R)\}.
}
\tag{13}
\]

Thus a negative critical sequence for which the fusion deficit
\({\cal D}\) dominates \(G\) is forced quantitatively into the
balanced locus
\[
 H_i^L,H_i^R\preceq\frac12I_3
 \quad(i=1,2,3).
\tag{14}
\]
The remaining theorem is therefore no longer an arbitrary rank-two
inequality: it is the exclusion of a global normal-space solution
(5) in the balanced pair-centered locus (14), together with the
quantitative transition region controlled by (12).

This note does **not** exclude that final locus and therefore does not
complete unrestricted three-copy positivity.

The dependency-free checker is
`verification/verify_n3_global_quotient_criticality.py`.

## 1. The two quotients are the same optimization

For the transition \(C=C_z\), retain the exact identities
\[
\begin{aligned}
 q&=Q_3(C),&
 c&=\|\Pi _2C\|_2^2,\\
 \sigma&=\langle z,S_Vz\rangle=2q+3c,&
 k&=\langle z,K(V)z\rangle=\frac12\sigma+5q.
\end{aligned}
\tag{15}
\]
The Schur operator satisfies \(S_V\succ0\), so \(\sigma>0\) for a
nonzero transition.  If \(q<0\), (15) implies \(c>0\).  Set
\[
 \mu=\frac{k}{\sigma},\qquad \lambda=\frac qc.
\tag{16}
\]
Then
\[
\boxed{
 \mu=\frac{6\lambda+\frac32}{2\lambda+3},
 \qquad
 \lambda=\frac{3\mu-\frac32}{6-2\mu}
 =\frac{3(2\mu-1)}{4(3-\mu)}.
}
\tag{17}
\]
On the physical range the denominator is positive, and
\[
 \frac{d\mu}{d\lambda}
 =\frac{15}{(2\lambda+3)^2}>0.
\tag{18}
\]
Therefore the global minimizers of the two quotients agree.
Moreover,
\[
\boxed{
 k-\mu\sigma
 =2(3-\mu)(q-\lambda c).
}
\tag{19}
\]
Thus the fixed-\(V\) generalized eigen-equation
\[
 (K(V)-\mu S_V)z=0
\tag{20}
\]
is precisely the fixed-right-plane part of the Euler equation for
\(q-\lambda c\).

## 2. Complete \(V,z\) Euler equations

Let \(C\) be a rank-two global minimizer with \(q<0\), and write
\[
 C=U\Sigma V^\dagger,\qquad
 U^\dagger U=V^\dagger V=I_2,\qquad \Sigma>0.
\tag{21}
\]
Consider
\[
 {\cal W}_\lambda={\cal A}-\lambda{\cal P}.
\tag{22}
\]
For every rank-at-most-two \(X\) with \(\|{\cal P}X\|>0\),
global minimality gives
\[
 \langle X,{\cal W}_\lambda X\rangle
 =Q_3(X)-\lambda\|\Pi _2X\|_2^2\geq0.
\tag{23}
\]
At \(C\), equality holds.

The tangent space of the smooth rank-two stratum is
\[
 T_C=
 \{Z:(I-UU^\dagger)Z(I-VV^\dagger)=0\}.
\tag{24}
\]
The first variation of (23) at \(C\) is
\[
 2\operatorname{Re}
 \langle Z,{\cal W}_\lambda C\rangle.
\tag{25}
\]
It vanishes for every complex tangent \(Z\).  Hence
\[
 R={\cal W}_\lambda C\in T_C^\perp
 =(I-UU^\dagger)M_{27}(I-VV^\dagger),
\tag{26}
\]
which proves (5).  Equivalently,
\[
\boxed{
\begin{aligned}
 {\cal A}(C)V&=\lambda D V,\\
 {\cal A}(C)^\dagger U&=\lambda D^\dagger U.
\end{aligned}}
\tag{27}
\]
There are also the useful full matrix identities
\[
\boxed{
 RC^\dagger=0,\qquad C^\dagger R=0.
}
\tag{28}
\]

To see directly how the two equations split between the original
variables, write \(C=ZV^\dagger\).  Arbitrary variations of \(z\), or
equivalently of \(Z\), give \(RV=0\), which is (20) after (19).
Stiefel variations of \(V\), including leakage out of its
two-plane, give \(R^\dagger Z=0\).  Since \(Z\) has range \(U\), this
is \(U^\dagger R=0\).  Thus no part of the determinantal Euler system
is lost in the Schur parametrization.

Every rank-preserving left or right local filter is a tangent
variation.  Therefore, for every \(A\in M_3\),
\[
\boxed{
\begin{aligned}
 \langle A^{(i)}C,R\rangle&=0,\\
 \langle CA^{(i)},R\rangle&=0.
\end{aligned}}
\tag{29}
\]
These scalar filter equations are consequences of the stronger
normal-block equations (5).

## 3. The pair-centered local functional

At a fixed site define the left endpoint and pair forms
\[
\begin{aligned}
 h_i^L(A,B)
 &=\langle A^{(i)}C,{\cal A}(B^{(i)}C)\rangle,\\
 p_i^L(A,B)
 &=\langle{\cal P}(A^{(i)}C),
             {\cal P}(B^{(i)}C)\rangle.
\end{aligned}
\tag{30}
\]
The right forms are defined by replacing \(A^{(i)}C\) by
\(CA^{(i)}\).  Equation (29) says
\[
\boxed{
 h_i^{L,R}(I,A)=\lambda p_i^{L,R}(I,A)
 \qquad(A\in M_3).
}
\tag{31}
\]

Because \(D={\cal P}C\),
\[
\begin{aligned}
 p_i^L(I,A)
 &=\langle D,A^{(i)}C\rangle
 =c\,\operatorname{Tr}(A M_i^L),\\
 p_i^R(I,A)
 &=\langle D,CA^{(i)}\rangle
 =c\,\operatorname{Tr}(A M_i^R),
\end{aligned}
\tag{32}
\]
with the matrices in (6).  In particular
\[
 \operatorname{Tr}M_i^L
 =\operatorname{Tr}M_i^R=1.
\tag{33}
\]

We prove (9) on the left; the right proof is identical.  Define the
linear functional
\[
 \ell(A)=\frac1c p_i^L(I,A)=\operatorname{Tr}(AM_i^L).
\tag{34}
\]
Then \(\ell(I)=1\).  Decompose
\[
 A=tI+B,\qquad t=\ell(A),\qquad\ell(B)=0.
\tag{35}
\]
Equation (31) and \(q=\lambda c\) remove the cross term:
\[
 h_i^L(A,A)=q|t|^2+h_i^L(B,B).
\tag{36}
\]

For every eigenvalue \(\zeta\) of \(B\), the matrix
\(B-\zeta I\) has rank at most two.  The established local-support
boundary theorem gives
\[
 h_i^L(B-\zeta I,B-\zeta I)
 =Q_3((B-\zeta I)^{(i)}C)\geq0.
\tag{37}
\]
Using (36) and \(q<0\),
\[
\boxed{
 h_i^L(B,B)\geq(-q)\,r(B)^2,
}
\tag{38}
\]
where \(r(B)\) is the spectral radius.

For a unit vector \(z\), put
\[
 R_z=|z\rangle\langle z|,\qquad P_z=I-R_z,\qquad
 m_z=\ell(R_z)=\langle z,M_i^Lz\rangle.
\tag{39}
\]
The centered part of \(P_z\) is
\[
 B_z=P_z-(1-m_z)I=m_zI-R_z,
\tag{40}
\]
whose eigenvalues are
\[
 m_z-1,\quad m_z,\quad m_z.
\tag{41}
\]
Equations (36), (38), and (41) imply
\[
\boxed{
 Q_3(P_z^{(i)}C)
 \geq(-q)(2\operatorname{Re}m_z-1)_+.
}
\tag{42}
\]
Now
\[
 \operatorname{Re}m_z=\langle z,H_i^Lz\rangle.
\tag{43}
\]
The exact one-site Haar twirl has endpoint eigenvalue zero on the
local scalar sector and \(5/8\) on the local traceless sector.
Therefore
\[
 {\mathbb E}_zQ_3(P_z^{(i)}C)=\frac58g_i(C).
\tag{44}
\]
Combining (42)--(44),
\[
\boxed{
 \frac58g_i(C)\geq
 (-q)\,{\mathbb E}_z
 (2\langle z,H_i^Lz\rangle-1)_+.
}
\tag{45}
\]

## 4. Exact qutrit Haar integral

Diagonalize \(H=H^\dagger\), with eigenvalues as in (7).  For a Haar
unit vector in \(\mathbb C^3\), the squared coordinate moduli
\((p_1,p_2,p_3)\) are uniform on the probability simplex, with
density two.

The simplex integral is the standard elementary divided-difference
formula
\[
\boxed{
 {\mathbb E}_z(2\langle z,Hz\rangle-1)_+
 =
 \frac23\sum_{\nu_r>1/2}
 \frac{(\nu_r-\frac12)^3}
 {\displaystyle\prod_{s\ne r}(\nu_r-\nu_s)}
 =\frac23{\cal R}(H).
}
\tag{46}
\]
For distinct eigenvalues, this follows by cutting the simplex by the
line \(\sum_r\nu_rp_r=1/2\) and integrating the affine height on the
resulting triangle or trapezoid.  Equivalently, integrate first along
one simplex coordinate and interpolate the resulting quadratic
truncated power at the three nodes \(\nu_r\).  Repeated eigenvalues
follow by continuity.  In the one-eigenvalue regime, put
\(\alpha=\nu_1-\frac12\), \(b=\frac12-\nu_2\), and
\(d=\frac12-\nu_3\).  The positive region is a triangle and its
area-times-average-height calculation gives the corresponding term
\[
 \frac23\frac{\alpha^3}{(\alpha+b)(\alpha+d)}
 \]
directly.

Equations (45) and (46) prove the left inequality in (9).  The right
one follows from the same argument applied to right local filters.
In particular, compactness on any fixed operator-norm ball shows
that (9) forces every pair-centered largest eigenvalue toward the
closed half-space \(\nu_1\leq1/2\) whenever \(G/(-q)\) tends to
zero.  No positivity of \(H\)
has been assumed; two eigenvalues may exceed \(1/2\), which is why
the full divided difference in (46) is retained.

## 5. Conversion to \(G,a,\Xi\)

Let \(x,a,c,d\) denote the masses in degrees \(0,1,2,3\).  Then
\[
\begin{aligned}
 q&=-\frac18x+\frac14a-\frac12c+d,\\
 G&=\frac14a-c+3d,\\
 \Xi&=-5x+4a-\frac12c+\frac74d.
\end{aligned}
\tag{47}
\]
Eliminating \(x,d\) gives the exact fusion arithmetic
\[
\boxed{
 640q=204G+45a+16\Xi-108c.
}
\tag{48}
\]
For a negative minimizer, (11) follows.
Substitution of \(-q={\cal D}/640\) into (9) gives (12), and summing
over the three sites gives (13).

For completeness, the ordinary Hilbert--Schmidt traces of the local
critical forms also have exact common-invariant expressions.  Sum
over a matrix-unit basis of \(M_3\).  The endpoint forms give
\[
 \sum_i\operatorname{Tr}_{\rm HS}h_i^L
 =-15q+\frac{15}{2}G.
\tag{49}
\]
The pair forms give
\[
\begin{aligned}
 \sum_i\operatorname{Tr}_{\rm HS}p_i^L
 &=\frac{16}{3}a+\frac{17}{3}c+d\\
 &=\frac13G+\frac{21}{4}a+6c.
\end{aligned}
\tag{50}
\]
The same identities hold on the right.  Hence for the shifted
positive local form \(h_i-\lambda p_i\),
\[
\boxed{
 \sum_i\operatorname{Tr}_{\rm HS}(h_i^L-\lambda p_i^L)
 =
 \left(\frac{15}{2}-\frac{\lambda}{3}\right)G
 -\frac{21\lambda}{4}a-21\lambda c.
}
\tag{51}
\]
Equations (5), (9), (52), and (55) are the complete scalar and
matrix-valued first-order data in the requested variables.  The
unresolved step is to couple the six matrices (6), which all arise
from the same pair \((C,\Pi _2C)\), strongly enough to rule out
\({\cal D}>0\) in the balanced locus.
