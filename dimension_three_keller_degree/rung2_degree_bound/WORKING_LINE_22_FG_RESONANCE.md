# Working theorem: the finite-outer-critical \(F=0\) and \(G=0\) line-\((2,2)\) resonances

**Status:** exact theorem independently hostile-audited inside the chart
where both outer critical points are finite.  The audit found no algebraic
or specialization error in this chart, but rejected any extension to the
separate one-critical-point-at-infinity chart.  This is not peer reviewed.

**Recorded:** 2026-07-25T05:27:08Z.

**Promoted after scope correction and audit:** 2026-07-25T06:00:55Z.

This note closes the two resonance hypersurfaces left open in the
finite-outer-critical chart of `WORKING_LINE_22_FINITE_OUTER_CRITICAL.md`.  It uses
the valid joint coordinates
\[
p=x^2,\qquad q=yz,
\]
\[
H_4=((p-aq)^2,(p-bq)^2,0),\qquad R_3=x(p-cq),
\]
and
\[
F=3ab-2ac-bc,\qquad G=3ab-ac-2bc.
\]
The theorem does not cover
\[
H_4=((p-aq)^2,q^2,0),
\]
because the pencil stabilizer fixes \(u=\infty\).

## 1. Reduction of \(F=0\)

The intersection with \(c=0\) is a marked-critical triple branch already
covered in the finite-outer-critical note.  Suppose \(c\ne0\).  If \(F=0\) and
\(a\ne b\), then \(a,b\ne0\): if \(b=0\), then
\(F=-2ac\), which would force \(a=0\), contradicting \(a\ne b\).  Scale
\(b=1\) and put \(a=t\).  Necessarily
\[
c=\frac{3t}{2t+1},\qquad
t\ne0,1,-\frac12.
\tag{1}
\]
Here \(t=0\) is precisely the already-covered \(c=0\) marked-critical
endpoint, \(t=1\) violates \(a\ne b\), and at \(t=-\frac12\) one has
\(F=-\frac32\) for every finite \(c\).  Thus no parameter value was lost
when deriving (1).

The value \(t=\frac12\) will be treated in a separate chart.  No finite
affine \(t\)-value is lost here; the projective value \(b=\infty\) is the
separate outer chart just excluded from the theorem's scope.

Write
\[
W_2=w_0p+rxy+sxz+my^2+w_qq+nz^2
\tag{2}
\]
and \(D=(t-1)(2t+1)\).  Target shears remove the \(x^3\)-coefficients of
the first two components of \(H_3\).  For \(t\ne\frac12\), translations in
\(y,z\) validly set the \(x^2y,x^2z\)-coefficients of the first component
to zero.  The complete gauge-fixed \(E_7\) kernel is
\[
\begin{split}
U_3={}&A xq-\frac43D(mxy^2+nxz^2)
 -\frac{4tD}{3(2t-1)}(r y^2z+s yz^2),\\
V_3={}&B xq+\frac{4D}{3t(2t-1)}
\{r(x^2y-y^2z)+s(x^2z-yz^2)\},\\
(H_3)_3={}&x\left(p-\frac{3t}{2t+1}q\right).
\end{split}
\tag{3}
\]
This is not merely a displayed family.  The coefficient matrix of \(E_7\)
before gauge has exact rank fourteen; a \(14\times14\) minor is, up to a
nonzero rational constant,
\[
\frac{t^6(t-1)^6}{(2t+1)^{14}}.
\tag{4}
\]
Thus the raw kernel has dimension twelve.  The coefficient matrix together
with the four gauge equations has an exact \(18\times18\) minor,
up to a nonzero rational constant,
\[
\frac{t^8(t-1)^6(2t-1)^2}{(2t+1)^{14}}.
\tag{5}
\]
The two omitted columns are exactly the free \(A,B\) directions.  Thus
(3), together with the six coefficients of \(W_2\), is the entire
gauge-fixed kernel.

## 2. The four resonance modes die in \(E_6\)

For (3), the \(E_6\) coefficient matrix in the quadratic and linear
unknowns has rank exactly eight.  A fixed \(8\times8\) minor is, up to a
nonzero rational constant,
\[
\frac{t^4(t-1)^4}{(2t+1)^8}.
\tag{6}
\]
Its exact left-kernel compatibilities include nonzero multiples of
\[
D m^2,\qquad D n^2.
\tag{7}
\]
Hence \(m=n=0\).  After this substitution, two further compatibilities are
nonzero multiples of
\[
\frac{t(t-1)^2(2t+1)}{(2t-1)^2}r^2,\qquad
\frac{t(t-1)^2(2t+1)}{(2t-1)^2}s^2.
\tag{8}
\]
Thus \(r=s=0\).

The apparent hole at \(t=\frac12\) is only a gauge failure in (3).  Instead
set the \(x^2y,x^2z\)-coefficients of \(V_3\) to zero.  The complete
gauge-fixed kernel becomes
\[
\begin{split}
U_3={}&A xq+\frac43
(r x^2y+s x^2z+mxy^2+nxz^2),\\
V_3={}&B xq,\qquad
(H_3)_3=x\left(p-\frac34q\right).
\end{split}
\tag{9}
\]
The corresponding raw \(14\times14\) and gauged \(18\times18\)
\(E_7\) minors both evaluate to
\[
-\frac{387420489}{256},
\tag{10}
\]
and the \(E_6\) rank-eight minor is
\[
\frac{6561}{16}.
\tag{11}
\]
The left-kernel compatibilities successively contain nonzero multiples of
\[
m^2,\quad n^2,\quad r^2,\quad s^2.
\tag{12}
\]
So (8) also reduces to invariant terms only.

Consequently, on every point of \(F=0\) under consideration,
\[
H_3=(A xq,B xq,x(p-cq)),\qquad W_2=w_0p+w_qq.
\tag{13}
\]

## 3. Common-kernel exit

Let \(U_2,V_2\) be completely general quadratics and let
\(L_0=(\ell_{ij})\) be completely general.  The rank-eight \(E_6\) system
for (12) is equivalent to
\[
\begin{gathered}
[xy]U_2=-\frac43D\,\ell_{32},\qquad
[xz]U_2=-\frac43D\,\ell_{33},\\
[y^2]U_2=[z^2]U_2=0,\\
[xy]V_2=[xz]V_2=[y^2]V_2=[z^2]V_2=0.
\end{gathered}
\tag{14}
\]
No entry of \(L_0\) has been divided out.

After (13), the six \(E_5\) coefficients split into two homogeneous
systems with the same \(3\times3\) coefficient matrix \(M\), up to an
irrelevant overall sign:
\[
M
\begin{pmatrix}\ell_{12}\\ \ell_{22}\\ \ell_{32}\end{pmatrix}=0,
\qquad
M
\begin{pmatrix}\ell_{13}\\ \ell_{23}\\ \ell_{33}\end{pmatrix}=0.
\tag{15}
\]
The upper-left \(2\times2\) minor of \(M\) is exactly
\[
-\frac{36t(t-1)}{(2t+1)^2},
\tag{16}
\]
which is nonzero throughout (1), including \(t=\frac12\).  Hence
\(\dim\ker M\le1\).  The second and third columns of \(L_0\) are therefore
proportional, and
\[
\det L_0=0.
\tag{17}
\]
This contradicts the Keller condition.

### \(F\)-resonance theorem

No Keller map occurs on the \(F=0\) resonance in the
finite-outer-critical chart of the rank-two-restriction unique-double-line
line-\((2,2)\) locus.

## 4. The \(G=0\) resonance

Interchanging the first two outer components sends
\[
(a,U_3,U_2,\text{row}_1 L_0)
\longleftrightarrow
(b,V_3,V_2,\text{row}_2 L_0)
\]
and sends \(F\) exactly to \(G\).  It preserves the condition that the
Jacobian determinant be a nonzero constant.  Thus the \(F=0\) proof gives:

### \(G\)-resonance theorem

No Keller map occurs on the \(G=0\) resonance in the same
finite-outer-critical chart.

## 5. Verification and disclosure

`verify_line_22_fg_resonance_sympy.py` reconstructs the two complete
\(E_7\) gauges, checks the raw ranks and the specialization-safe minors,
derives the exact \(E_6\) square compatibilities, and verifies the
common-kernel exit (14)--(16).

`verify_line_22_fg_resonance_pari.gp` independently reconstructs the raw
\(E_7\) minor, both \(E_6\) square systems, both rank-eight minors, and all
nine entries of the common \(E_5\) kernel matrix.  It is run through
`run_verify_line_22_fg_resonance_pari.sh`, which rejects any PARI parser or
runtime diagnostic and requires an exact final success sentinel.  This is
a genuinely separate CAS implementation, not a second interpreter running
the SymPy algorithm.

The calculations are exact evidence about the encoded algebra, not peer
review.  The hostile audit independently reconstructed the raw kernels,
all special \(t\)-values, the square obstructions, and the common-kernel
exit.  It also exhibited the omitted outer-infinity chart that delimits
the theorem.  This result was developed with AI assistance and has not
been peer reviewed.
