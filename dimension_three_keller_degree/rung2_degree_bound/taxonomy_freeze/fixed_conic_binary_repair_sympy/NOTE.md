# Exact repair of the binary fixed-conic E7/E6 reduction

**Computed:** 2026-07-26T10:09:44Z
**Scope:** only \(h=pq\) and \(h=p^2\), through E7, E6, and the
resulting tangent-orbit reduction.

## Verdict

\[
\boxed{\text{Equations (7), (8), and the tangent list (9) are correct.}}
\]

The fail-closed gap identified in
`audit_bridge_q2_e2_a1_b2_d2_n1_v1/REPORT.md` is repaired for this exact
binary E7/E6 obligation.  The full calculation finds no counterexample to
the legacy tangent list.  It does find and retain E7 compatibility rank
jumps in the coefficients of \(V\) which were not visible in the old
specialized E6 regression.

This note does **not** reaudit the later branch endgames in Sections 3--8
of `WORKING_FIXED_CONIC_ROW.md`, so it is not by itself a certificate for
the final theorem or the global frozen row.

## 1. Full starting system

Let
\[
A=(p^2,pq,q^2)^T,\qquad A_p=\partial_pA,\qquad A_q=\partial_qA
\]
and start with the full degree-eight normal
\[
H_3=V(p,q)+r\bigl((ap+bq)A_p+(cp+dq)A_q\bigr)
       +\frac{r^2}{2}(eA_p+fA_q).                 \tag{R1}
\]
The calculation uses all twelve coefficients \(v_0,\ldots,v_{11}\) of
\(V\).  In each target component their monomial order is
\[
(p^3,p^2q,pq^2,q^3).
\]
It also uses all eighteen coefficients \(w_0,\ldots,w_{17}\) of \(H_2\).
In each component their monomial order is
\[
(p^2,pq,q^2,pr,qr,r^2).
\]
Finally, \(L=(\ell_0,\ldots,\ell_8)\) is an arbitrary row-major
\(3\times3\) linear part.

Put
\[
D(s)=\det\bigl(L+sJH_2+s^2JH_3+s^3JH_4\bigr)
\]
and write \(E_k=[s^k]D(s)\).  Direct determinant multilinearity gives
\[
E_7=\operatorname{tr}\bigl(\operatorname{adj}(JH_4)JH_2\bigr)
  +\operatorname{tr}\bigl(\operatorname{adj}(JH_3)JH_4\bigr). \tag{R2}
\]
For both \(h=pq\) and \(h=p^2\), the coefficient matrix of \(E_7\) in the
eighteen \(w_i\) has constant rational rank \(7\).  Thus every solve below
uses constant pivots; the only denominators are \(2,4,8\).

## 2. Complete E7 solution for \(h=pq\)

The raw system has 22 nonzero coefficient equations and a 15-dimensional
left-null space.  Its compatibility polynomials contain nonzero constant
multiples of
\[
e^2,\quad f^2,
\]
so \(e=f=0\) at every complex solution.  After that substitution they
contain nonzero constant multiples of
\[
b^2,\quad c^2,
\]
so \(b=c=0\).  Substitution into the complete left-null ideal leaves
exactly
\[
\boxed{(3a-d)v_8=0,\qquad (a-3d)v_3=0.}           \tag{R3}
\]

Conditional only on (R3), the complete \(H_2\) fibre is obtained by
leaving
\[
w_0,w_1,w_2,w_6,w_7,w_8,w_{10},
w_{12},w_{13},w_{14},w_{16}                      \tag{R4}
\]
free and setting
\[
\begin{aligned}
w_3={}&\frac{
5av_1-3av_{11}-2av_6+dv_1+9dv_{11}-10dv_6+8w_{10}}4,\\
w_4={}&\frac{av_2+6av_7+5dv_2-18dv_7}{4},&
w_5={}&0,\\
w_9={}&-\frac{
9av_0+av_{10}-10av_5-3dv_0+5dv_{10}-2dv_5-4w_{16}}8,\\
w_{11}={}&-\frac{(a-d)^2}{2},\\
w_{15}={}&-\frac{
18av_4-5av_9-6dv_4-dv_9}{4},&
w_{17}={}&0.                                      \tag{R5}
\end{aligned}
\]
Substitution of (R5) into every E7 coefficient gives precisely the ideal
in (R3).  Rank \(7\) then proves that (R4)--(R5) is the whole affine
\(\mathbb A^{11}\) fibre, not a selected solution.

The compatibility rank in \(V\) is transparent from
\[
\begin{pmatrix}3a-d&0\\0&a-3d\end{pmatrix}
\begin{pmatrix}v_8\\v_3\end{pmatrix}=0.            \tag{R6}
\]
It is two off the resonant lines, one on either nonzero resonant line
\(d=3a\) or \(a=3d\), and zero at \(a=d=0\).

## 3. Universal E6 ideal for \(h=pq\)

Insert the complete fibre (R5), keep every free coefficient in (R4), and
keep all nine entries of \(L\).  Exact expansion gives
\[
\boxed{
[r^2]E_6=12p^2q^2(a-d)^2(a+d).}                  \tag{R7}
\]
The right side contains no \(v_i\), no free \(w_i\), and no \(\ell_i\).
Thus the raw tangent compatibility ideal is
\[
I_{pq}=\bigl\langle (a-d)^2(a+d)\bigr\rangle.      \tag{R8}
\]

This is the full tangent-elimination ideal, not just a contained
necessary ideal.  Indeed, set \(V=0\), all entries in (R4) to zero, and
\(L=0\).  Then
\[
H_2=r^2(0,-(a-d)^2/2,0)^T,
\]
E7 vanishes identically, and
\[
E_6=12r^2p^2q^2(a-d)^2(a+d).
\]
Consequently the specialization map sends the complete E7/E6 coefficient
ideal into \(I_{pq}\) while restricting to the identity on
\(\mathbb Q[a,d]\).  The reverse containment follows from (R7), proving
equality of the elimination ideal.

The reduced ideal is
\[
\sqrt{I_{pq}}=\langle(a-d)(a+d)\rangle.            \tag{R9}
\]
Hence the two components are \(d=a\) and \(d=-a\); the first occurs with
multiplicity two in the raw E6 ideal.  They meet only at \(a=d=0\).

Write the tangent field as \(D_MA\), with
\[
M=\begin{pmatrix}a&0\\0&d\end{pmatrix}.
\]
On \(d=a\ne0\), scaling \(r\) gives \(M=I\), and Euler's identity gives
\(D_MA=2A\).  On \(d=-a\ne0\), scaling \(r\) gives
\(M=\operatorname{diag}(1,-1)\), hence
\(D_MA=pA_p-qA_q\).  Their common boundary is \(M=0\).  The diagonal and
anti-diagonal stabilizer of \(pq\) adds no further orbit.  Thus the split
list is exactly
\[
\boxed{2A,\quad pA_p-qA_q,\quad0.}                 \tag{R10}
\]

On each nonzero E6 component, (R6) has rank two and forces
\(v_3=v_8=0\).  At the zero tangent it has rank zero and both coefficients
are free.  The rank-one resonant E7 strata do not survive E6 away from the
origin.

## 4. Complete E7 solution for \(h=p^2\)

The raw system has 20 nonzero coefficient equations and a 13-dimensional
left-null space.  It again contains nonzero constant multiples of
\(e^2,f^2\), and after \(e=f=0\) it contains a nonzero constant multiple
of \(b^2\).  Thus
\[
e=f=b=0,
\]
while \(c\) remains arbitrary.  The remaining complete compatibility
ideal is
\[
\boxed{
\begin{aligned}
(a-4d)v_2+6(2d-a)v_7-6cv_3&=0,\\
(a-2d)v_3&=0.
\end{aligned}}                                     \tag{R11}
\]

The eleven free coefficients are again exactly (R4).  The seven pivots
are
\[
\begin{aligned}
w_3={}&\frac{
3av_0-av_{10}-2av_5+2cv_1+6cv_{11}-8cv_6
 +4dv_{10}-4dv_5+4w_{10}}2,\\
w_4={}&\frac{
av_1-3av_{11}+2av_6+4cv_2-12cv_7
 +2dv_1+6dv_{11}-8dv_6}{2},\\
w_5={}&(a-d)^2,\\
w_9={}&\frac{
6av_4-av_9-4cv_{10}+4cv_5-2dv_9+2w_{16}}4,\\
w_{11}={}&c(a-d),&
w_{15}={}&\frac{3av_8+2cv_9}{2},&
w_{17}={}&c^2.                                     \tag{R12}
\end{aligned}
\]
Substitution into all E7 coefficients gives exactly (R11), so (R12) is
again the complete \(\mathbb A^{11}\) fibre.

In the variables \((v_2,v_3,v_7)\), the compatibility matrix is
\[
\begin{pmatrix}
a-4d&-6c&6(2d-a)\\
0&a-2d&0
\end{pmatrix}.                                    \tag{R13}
\]
Put \(x=a-2d\).  A \(2\times2\) minor is \(6x^2\).  Thus the rank is two
when \(x\ne0\).  On \(x=0\), (R13) becomes
\[
\begin{pmatrix}-2d&-6c&0\\0&0&0\end{pmatrix},
\]
so the rank is one unless \(c=d=0\), and is zero exactly at
\((a,c,d)=(0,0,0)\).  This records every E7 rank jump without division.

## 5. Universal E6 ideal for \(h=p^2\)

Substitution of the full fibre (R12), with arbitrary free coefficients
and arbitrary \(L\), gives
\[
\boxed{
[r^2]E_6=24dp^2\bigl(cp+(d-a)q\bigr)^2.}          \tag{R14}
\]
Therefore the raw coefficient ideal is
\[
\begin{aligned}
I_{p^2}
 &=\langle dc^2,\ dc(d-a),\ d(d-a)^2\rangle\\
 &=d\langle c,d-a\rangle^2.                       \tag{R15}
\end{aligned}
\]

As in the split case, this is the exact tangent-elimination ideal.  Set
\(V=0\), the eleven free entries to zero, and \(L=0\).  Then
\[
H_2=r^2\bigl((a-d)^2,c(a-d),c^2\bigr)^T,
\]
E7 is zero, and E6 is \(r^2\) times (R14).  This polynomial section gives
the reverse ideal containment.

The reduced ideal is
\[
\begin{aligned}
\sqrt{I_{p^2}}
 &=\langle dc,d(d-a)\rangle\\
 &=\langle d\rangle\cap\langle c,d-a\rangle.       \tag{R16}
\end{aligned}
\]
An exact certificate is
\[
I_{p^2}\subseteq\langle dc,d(d-a)\rangle,\qquad
\langle dc,d(d-a)\rangle^2\subseteq I_{p^2}.
\]
Thus the two reduced components are
\[
d=0,\qquad\text{or}\qquad c=0,\ d=a.              \tag{R17}
\]
The scalar component is doubled in the raw ideal, and the two components
meet only at the zero tangent.

With
\[
M=\begin{pmatrix}a&0\\c&d\end{pmatrix},
\]
the second component of (R17), away from the origin, is \(M=aI\), giving
\(2A\).  On \(d=0\):

* if \(a\ne0\), the lower-triangular stabilizer matrix
  \[
  g=\begin{pmatrix}a&0\\c&1\end{pmatrix},\qquad\det g=a,
  \]
  satisfies
  \[
  Mg=g\operatorname{diag}(a,0).
  \]
  Hence this chart is the semisimple orbit \(pA_p\);
* if \(a=0,c\ne0\), the matrix \(g=\operatorname{diag}(1,c)\), with
  \(\det g=c\), conjugates \(M\) to
  \(\left(\begin{smallmatrix}0&0\\1&0\end{smallmatrix}\right)\).
  This is the nilpotent orbit \(pA_q\);
* if \(a=c=0\), the tangent is zero.

Every division used to normalize an orbit is therefore attached to the
explicit nonvanishing premise \(\det g=a\ne0\) or \(\det g=c\ne0\).
The double-root list is exactly
\[
\boxed{2A,\quad pA_p,\quad pA_q,\quad0.}           \tag{R18}
\]

The E7 compatibility ranks on these four orbits are respectively
\[
2,\quad2,\quad1,\quad0.
\]
More explicitly, the nonzero scalar orbit forces
\(v_3=0,\ v_2=2v_7\); the nonzero semisimple orbit forces
\(v_3=0,\ v_2=6v_7\); the nilpotent orbit forces only \(v_3=0\);
and the zero tangent imposes no condition on \((v_2,v_3,v_7)\).

## 6. Retained verification

Run

```sh
taxonomy_freeze/fixed_conic_binary_repair_sympy/verify_strict.sh
```

from `dimension_three_keller_degree/rung2_degree_bound`.
The checker reconstructs (R1)--(R2) with all \(12+18+9\) lower
coefficients, computes both constant-rank E7 systems, validates the full
affine fibres (R5) and (R12), derives the E6 ideals and their polynomial
sections, and checks the orbit and rank-jump certificates.  Any missing
coefficient, changed rank, parameter-dependent pivot, ideal mismatch, or
failed section terminates nonzero.

## 7. Composition with the legacy branch endgames

The exact interface supplied by this repair is:

1. every solution of the full binary E7 system occurs in (R3)--(R5) or
   (R11)--(R12);
2. every solution which also satisfies E6 has tangent on one of the
   reduced components (R9) or (R16);
3. the displayed stabilizer conjugacies are invertible on their recorded
   nonzero charts, so tangent normalization to one of (R10) or (R18)
   transports the **entire** remaining lower-coefficient fibre; and
4. after that transport, the next calculation must start with the image
   of every compatible \(V\) coefficient and all eleven free \(H_2\)
   coefficients, then solve the \(r^1,r^0\) parts of E6 and the lower
   weighted equations.

This repair proves the first three statements.  It does not prove that
the later displayed families (13)--(16), (23)--(25), or (28)--(36) in the
working note are the complete images of the fibres in the fourth
statement.  The old checker begins several of those endgames from
pre-solved branch-specific families.  Those formulas may be correct, but
their completeness is not established by the present script.

Accordingly,
\[
\boxed{\text{the E7/E6 tangent reduction is repaired, but the later
fibre-to-endgame composition remains fail-closed here.}}
\]

Promotion of the whole binary theorem still requires either a retained
constant-pivot derivation from (R5)/(R12) through each later branch, with
all exceptional specializations, or a separate exact certificate proving
that the legacy branch families span those full solution fibres.
