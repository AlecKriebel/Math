# Provisional exclusion of the squarefree-interior fixed-root/contact
\(\delta=2,\{1,1\}\) row

**Status:** exact SymPy and independent PARI/GP replays pass; hostile
mathematical audit is pending.

**First recorded release (UTC):** 2026-07-25T15:22:51Z.

This work is not peer reviewed.  Exact checks are evidence about the
encoded algebra, not peer review.

## Theorem

Put
\[
L=p-wq,\qquad M=wp-q,\qquad h=LM,\qquad u=w^2,
\]
and
\[
R=L\{Ap^2+(1-3u)Tpq+4wTq^2\}.                  \tag{1}
\]
There is no Keller counterexample in the binary fixed-quadratic
line-double-cover row on the exact open
\[
w(u-1)(u-3)EFG\ne0,                              \tag{2}
\]
where
\[
\begin{aligned}
E&=A+T(w^3+w),\\
F&=-Aw+3Tu-5T,\\
G&=Au-3A+12Tw^3-4Tw.                            \tag{3}
\end{aligned}
\]

The three incidence boundaries in (3) were recomputed directly:
\[
\begin{array}{c|c}
E=0&pLM\\
F=0&pL^2\\
G=0&pqL.
\end{array}                                      \tag{4}
\]
Their Hilbert--Burch gcd degree is at least three, so they are routed
to the future \(\delta\ge3\) analysis.  The values \(w=0,u=1\) leave
the squarefree-interior fixed-divisor orbit.  The value \(u=3\) is the
exceptional \(\kappa=16/3\), \(\{2,0\}\) row already treated in
`DELTA2_K20_UMBRELLA.md`.

## Generic contact chart

Let \(M_7\) be the coefficient matrix of
\[
\alpha U+\beta V+\gamma W=0,                    \tag{5}
\]
where
\[
\alpha=[Q,R],\qquad \beta=-[P,R],\qquad
\gamma=[P,Q],
\]
\[
P=hp^2,\quad Q=hq^2,\quad
\deg(U,V,W)=(2,2,1),
\]
and \([f,g]=f_pg_q-f_qg_p\).  A direct row reduction gives a
two-dimensional tangent kernel.  A decisive rank-six minor is
\[
-72(u-1)^2E^2F^2DG,                              \tag{6}
\]
with the two internal factors
\[
\begin{aligned}
D&=-16Aw+T(9u^2-6u+1),\\
H&=12Aw^3-4Aw+T(7u^3+9u^2-3u-5).                \tag{7}
\end{aligned}
\]

Write a tangent as \(sN_1+tN_2\), and lift
\([r]E_6\) to the linear coefficient map in
\[
(X,Y,Z,x_5,y_5)=(s^2,st,t^2,x_5,y_5).
\]
The selected maximal minor is
\[
\begin{aligned}
27648\,w^5(u-1)^2(u-3)^2
E^2F^4D^3GH.                                     \tag{8}
\end{aligned}
\]
Thus the contact map has full rank whenever \(DH\ne0\).  Equations
(5)--(8) are literal coefficient calculations over
\(\mathbb Q[w,A,T]\); the complete polynomial tangent bases used for
the minors are recorded verbatim in both verification programs.

## The \(D=0\) chart

Normalize
\[
A=9u^2-6u+1,\qquad T=16w.                        \tag{9}
\]
Then
\[
\begin{aligned}
E&=(5u+1)^2,\\
F&=-9w(u-3)^2,\\
G&=3(3u-1)(u^2+18u+1),\\
H&=4wJ(u),
\end{aligned}
\qquad
J(u)=55u^3+9u^2-3u-21.                           \tag{10}
\]
A fresh \(E_7\) basis, computed without specializing the singular
generic basis, gives contact determinant
\[
\begin{aligned}
41278242816\,w^5(u-1)^2(u-3)^7(u+1)^3
 &(3u-1)(5u-3)^3(5u+1)^4\\
 &\cdot(u^2+18u+1)J(u).                         \tag{11}
\end{aligned}
\]
On the exact open, its only unresolved factors are
\[
u=-1,\qquad u=3/5,\qquad J(u)=0.                 \tag{12}
\]

## The \(H=0\) chart

Normalize
\[
A=-(7u^3+9u^2-3u-5),\qquad T=4w(3u-1).           \tag{13}
\]
Now
\[
\begin{aligned}
E&=(u+1)(5u^2-6u+5),\\
F&=wF_0(u),\\
G&=-G_0(u),\\
D&=4wJ(u),
\end{aligned}                                    \tag{14}
\]
where
\[
\begin{aligned}
F_0(u)&=7u^3+45u^2-75u+15,\\
G_0(u)&=7u^4-156u^3+66u^2-12u+15.
\end{aligned}
\]
The fresh contact map has rank four.  A decisive minor is
\[
\begin{aligned}
294912\,w^8(u-1)^2(u+1)^4(11u-9)
(5u^2-6u+5)^2F_0^4J^3G_0.                       \tag{15}
\end{aligned}
\]
Away from \(u=9/11\) and \(J=0\), its one-dimensional kernel has
Veronese obstruction
\[
\frac{
3V(u)}
{1024w^8(u+1)^2(11u-9)^2F_0(u)^2J(u)^2},        \tag{16}
\]
where
\[
V(u)=515u^4-548u^3+162u^2-324u+243.              \tag{17}
\]
Hence all of this chart is excluded at \(E_6\), except the genuine
quartic survivor \(V(u)=0\) and the two singular-basis values
\[
u=9/11,\qquad J(u)=0.                            \tag{18}
\]

## The genuine quartic survivor dies in \(E_5\)

Both \(V(u)\) and \(V(w^2)\) are primitive and irreducible over
\(\mathbb Q\).  Thus the calculation may be made in the exact field
\[
\mathbb Q[w]/(V(w^2))                            \tag{19}
\]
without selecting a numerical conjugate.  Put
\[
\begin{aligned}
N_X={}&49u^5-987u^4-3126u^3+4650u^2+405u-1215,\\
N_Y={}&343u^5-165u^4+1734u^3+150u^2-2925u+1215.
\end{aligned}                                    \tag{20}
\]
The kernel coordinate \(X\) in (16) is invertible because
\[
\operatorname{Res}(V,N_X)
=46746446734136993390788608\ne0.                 \tag{21}
\]
A denominator-cleared Veronese lift is therefore
\[
c_1=(u+1)N_X,\qquad c_2=2wN_Y.                  \tag{22}
\]
The corresponding \(r^2\)-coefficients in \(H_2\) are
\[
\begin{aligned}
x_5={}&-64w^3N_XF_0^2J(5u-3)
       (12u^3-5u^2+6u-9),\\
y_5={}&-64w^5(u+1)^2N_X(11u-9)F_0^2J.           \tag{23}
\end{aligned}
\]
Substitution into the next weighted identity gives the top-only
coefficient
\[
[r^2p^3]E_5
=-96w^5(u+1)^2F_0^3JG_0N_XC(u),                 \tag{24}
\]
where
\[
\begin{aligned}
C(u)={}&47705u^8-413356u^7+546080u^6+294804u^5\\
       &-623574u^4+87132u^3-152280u^2
         +362556u-142155.
\end{aligned}                                    \tag{25}
\]
The polynomial \(C\) is primitive, and
\[
\begin{aligned}
\gcd(V,C)&=1,\\
\operatorname{Res}(V,C)
&=272095271176488581477730636079615180800\\
&=2^{81}3^{20}5^2\cdot1291\ne0.                 \tag{26}
\end{aligned}
\]
The resultants of \(V\) with every denominator and exact-open factor
in (14)--(23) are also nonzero.  Consequently (24) cannot vanish in
(19), contradicting \(E_5=0\).

No omitted lower jet can alter (24).  The only weight partitions
contributing to \(E_5\) are
\[
(3,2,0),\qquad(3,1,1),\qquad(2,2,1).             \tag{27}
\]
The first has \(r\)-degree at most one.  For \((3,1,1)\), the
\(r\)-leading Jacobian of \(H_2\) contains the omitted \(r\)-linear
jets only in its upper-left \(2\times2\) block.  Since \(JH_4\) is
supported in that same block, the mixed determinant with one
\(JH_4\) and two \(JH_2\)'s is independent of those four entries; it
sees only \(x_5,y_5\) and the fixed tangent \(N_t\).  For
\((2,2,1)\), both required \(r\)'s come from the upper-left
\(2\times2\) block of \(JH_3\), so the mixed determinant sees only
the fixed \((3,3)\) entry \(N_t\) of \(JH_2\).  Binary lower terms
and the linear part have insufficient \(r\)-degree.  Both verification
engines expand these mixed determinants independently.

## The four singular-basis pivots

Fresh row reductions over exact coefficient fields give
\[
\begin{array}{c|c|c|c}
\text{chart}&\text{field relation}&\operatorname{rank}E_7&
\text{contact outcome}\\ \hline
D=0,\ u=-1&w^2+1=0&6&\operatorname{rank}=5\\
D=0,\ u=3/5&5w^2-3=0&6&\operatorname{rank}=5\\
H=0,\ u=9/11&11w^2-9=0&6&
  \operatorname{rank}=4,\ \text{non-Veronese kernel}\\
D=H=0,\ J(u)=0&J(w^2)=0&6&
  \operatorname{rank}=4,\ \text{non-Veronese kernel}.
\end{array}                                      \tag{28}
\]
All four field polynomials are irreducible over \(\mathbb Q\), so
each row covers all conjugates.  No numerical root is chosen.

Finally, the constant \(E_6\) block has the uniform decisive
determinant
\[
72(u-1)^2(u-3)E^2FG,                             \tag{29}
\]
nonzero on (2), including all four rows of (28).  Once the contact
tangent is excluded, every nonlinear term is binary.  The established
degree-four plane-field theorem, generic-degree descent, and
birational Keller theorem make the map a polynomial automorphism.
No form of the full plane Jacobian Conjecture is used.

This proves the theorem.

## Verification

Run

```text
./verify_delta2_11_interior_fixed_contact_strict.sh
```

The strict wrapper requires exact whitelisted transcripts from SymPy
and PARI/GP.  Both engines independently reconstruct the boundary
gcds, generic tangent and contact minors, fresh \(D=0\) and \(H=0\)
charts, primitive and irreducible quartic field, the two exact
resultants in (21) and (26), the top-only \(E_5\) coefficient, the
four singular-basis fields, and the constant block.  The all-binary
exit is recorded in `../../WORKING_FIXED_CUBIC_LINE_ROW.md`,
Section 4.

This proof was developed with AI assistance.
