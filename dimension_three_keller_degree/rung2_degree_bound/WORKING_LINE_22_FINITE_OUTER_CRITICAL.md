# Theorem: finite-outer-critical, finite-companion chart in the unique-double-line line \((2,2)\) row

**Status:** exact working theorem, independently hostile-audited in the
stated chart.  This note keeps the relative-position moduli which were lost
in the earlier simultaneous-normal-form charts.  The audit confirmed the
finite-outer-critical calculations and found a separate
one-critical-point-at-infinity chart.  Consequently this is not a theorem
for the whole unique-double-line row.  It is not peer reviewed.

**Recorded:** 2026-07-25T05:12:56Z.

**Promoted after scope correction and audit:** 2026-07-25T06:06:25Z.

## 1. Valid joint coordinates

Consider the rank-two-restriction quadratic pencil
\[
 p=x^2,\qquad q=yz.
\tag{1}
\]
The member \(p=0\) is the unique double line and \(q=0\) is the unique
rank-two singular member.  A source linear transformation preserving this
pencil induces only a scaling of
\[
 u=\frac pq.
\tag{2}
\]

If both critical points of the degree-two outer map are finite, a target
change gives
\[
 H_4=\bigl((p-aq)^2,(p-bq)^2,0\bigr),\qquad a\ne b.
\tag{3}
\]
Indeed, in this chart a degree-two cover of \(\mathbb P^1\) is determined up to target
automorphism by its unordered pair of critical points, and (3) has critical
pair \(\{a,b\}\) in the \(u\)-coordinate.  A finite-companion mixed cubic is
\[
 R_3=x(p-cq).
\tag{4}
\]
The simultaneous scaling
\[
 (a,b,c)\longmapsto(\lambda a,\lambda b,\lambda c)
\tag{5}
\]
is the only remaining pencil action.  Thus the ratios among \(a,b,c\) are
genuine relative-position invariants.  The value \(c=0\) is the triple
branch \(R_3=x^3\); the companion \(c=\infty\) is \(R_3=xq\).

The stabilizer fixes \(u=\infty\).  Therefore the additional outer chart
\[
\boxed{H_4=((p-aq)^2,q^2,0)}                              \tag{5a}
\]
cannot be moved into (3).  This chart is outside Sections 2--5 below.

For reference put
\[
 \delta=z\partial_z-y\partial_y,\qquad
 F=3ab-2ac-bc,\qquad G=3ab-ac-2bc.
\tag{6}
\]

## 2. The exact open \(E_7\) stratification

Write
\[
 H_3=(U_3,V_3,R_3),\qquad H_2=(U_2,V_2,W_2).
\]
The degree-seven identity is
\[
\begin{split}
0=E_7=2\{&
4x(a-b)(p-aq)(p-bq)\delta(W_2)\\
&+(p-bq)((3b-2c)p-bcq)\delta(U_3)\\
&+(p-aq)((2c-3a)p+acq)\delta(V_3)\}.
\end{split}
\tag{7}
\]
Because every coefficient outside the three \(\delta\)-derivatives lies in
\(\mathbb C[x,q]\), (7) splits by the \(z-y\) weight.  On weights
\(-3,-2,-1,0,1,2,3\), the full coefficient matrix has generic ranks
\[
2,\ 3,\ 4,\ 0,\ 4,\ 3,\ 2.
\tag{8}
\]
The two square weight-\(\pm2\) determinants are, up to nonzero constants,
\[
(a-b)^2FG,
\tag{9}
\]
and the gcd of the maximal weight-\(\pm1\) minors is, up to a nonzero
constant,
\[
c(a-b)^2FG.
\tag{10}
\]

Consequently, on
\[
\boxed{cFG\ne0,}
\tag{11}
\]
the kernel has dimension eight.  Six dimensions are the evident invariant
terms
\[
U_3,V_3\in\langle x^3,xq\rangle,\qquad
W_2\in\langle p,q\rangle.
\tag{12}
\]
The remaining two dimensions are exactly the jets produced by translations
in \(y,z\):
\[
\bigl(\partial_y(H_4)_1,\partial_y(H_4)_2,\partial_yR_3\bigr),
\quad
\bigl(\partial_z(H_4)_1,\partial_z(H_4)_2,\partial_zR_3\bigr).
\tag{13}
\]
Affine source translations remove (13).  Target shears adding the third
component to the first two remove the \(x^3\)-coefficients in (12).  Thus
every point of the open locus is affine-equivalent to
\[
\boxed{
H_3=(A\,xq,B\,xq,x(p-cq)),\qquad W_2=w_0p+w_1q.
}
\tag{14}
\]
This normalization uses the full joint orbit and does not change
\((a,b,c)\).

## 3. The open-locus exit

Keep completely general quadratic first two components \(U_2,V_2\) and an
arbitrary row-major linear part \(L_0=(\ell_{ij})\).  Substitution of (14)
in \(E_6\) has constant rank ten and forces
\[
\begin{gathered}
(L_0)_{32}=(L_0)_{33}=0,\\
U_2,V_2\in\langle p,q\rangle.
\end{gathered}
\tag{15}
\]
No entry in the first two rows of \(L_0\) has been normalized.

The six nonzero coefficients of \(E_5\) split into identical systems for
\[
(r,s)=((L_0)_{12},(L_0)_{22})
\quad\hbox{and}\quad
(r,s)=((L_0)_{13},(L_0)_{23}):
\]
\[
\begin{pmatrix}
-3b+2c&3a-2c\\
b(3b-c)&-a(3a-c)\\
-cb^2&ca^2
\end{pmatrix}
\binom r s=0.
\tag{16}
\]
For \(a\ne b\), this matrix has rank at least one: its first row could
vanish only if \(a=b\).  Hence both column pairs in (16) lie in the same
at-most-one-dimensional kernel, so
\[
(L_0)_{12}(L_0)_{23}-(L_0)_{13}(L_0)_{22}=0.
\tag{17}
\]
Together with the zero third-row entries in (15),
\[
\det L_0=(L_0)_{31}
\bigl((L_0)_{12}(L_0)_{23}
      -(L_0)_{13}(L_0)_{22}\bigr)=0.
\tag{18}
\]
This contradicts the Keller condition.

### Open finite-outer-critical-chart theorem

No Keller map occurs in the rank-two-restriction unique-double-line locus
with finite companion and \(cFG\ne0\).

The same normalized \(E_6,E_5\) exit is valid for
\[
p=x^2,\qquad q=y^2+xz.
\tag{19}
\]
For that pencil the induced group on \(u=p/q\) is the full Borel subgroup
fixing \(u=0\), because \(q\mapsto\mu q+\nu p\) is induced by source
linear changes.  The exact dense-rank certificate for its larger raw
\(E_7\) matrix is being packaged separately; (19) is not included in the
formal theorem above yet.

## 4. The noncritical triple branch

Set \(c=0\) and suppose \(ab\ne0\), so the marked double-line value is not
critical for the outer cover.  Scale \(b=1\), write \(a=t\), with
\[
t\ne0,1.
\tag{20}
\]
After the same target shears and \(y,z\)-translations, the only two
non-invariant \(E_7\) parameters are \(s_y,s_z\).  The exact \(E_6\)
compatibilities are
\[
\boxed{
-\frac83t(t-1)s_y^2=0,\qquad
\frac83t(t-1)s_z^2=0.
}
\tag{21}
\]
Thus both vanish.  The remaining data have the form (14) with \(c=0\), and
(16) again makes \(\det L_0=0\).

For completeness, the specialized \(E_7\) weight ranks are
\[
2,\ 3,\ 3,\ 0,\ 3,\ 3,\ 2.
\]
Thus its nullity is exactly ten.  An exact \(10\times10\) determinant shows
that the six invariant terms, the two translation jets, and \(s_y,s_z\)
span that kernel for every \(t\ne0,1\).  No additional \(E_7\) mode is being
suppressed in (21).

### Noncritical-triple theorem in the finite-outer-critical chart

No Keller map occurs in the \(c=0,\ ab\ne0\) branch.

## 5. Marked-critical triple branch with finite other critical point

The relative orbit with critical pair \(\{0,1\}\) has the valid joint form
\[
H_4=(p^2,(p-q)^2,0),\qquad R_3=x^3.
\tag{22}
\]
Here the full \(E_7\) equation is
\[
\delta(3U_3-4xW_2)=0.
\tag{23}
\]
Hence, without discarding any coefficient,
\[
U_3=\frac43xW_2+\sigma x^3+\tau xq,
\qquad V_3\ \hbox{arbitrary}.
\tag{24}
\]
A target shear removes \(\sigma x^3\).

The raw \(E_6\) compatibilities first force the \(y^2,z^2\) coefficients
of \(W_2\) to vanish.  Put
\[
W_2=w_0p+w_yxy+w_zxz+w_qq.
\tag{25}
\]
If the total \(xq\)-coefficient in \(U_3\) is nonzero, \(E_6\) forces
\(w_y=w_z=0\).  If that coefficient is zero, the resonant \(E_5\)
coefficients are
\[
[y^4z]E_5=\frac89w_y^3,\qquad
[yz^4]E_5=-\frac89w_z^3.
\tag{26}
\]
They again force \(w_y=w_z=0\).

There is a specialization in the reduction of \(V_3\) which must be kept.
Write
\[
\begin{split}
V_3={}&v_0x^3+v_1x^2y+v_2x^2z+v_3xy^2+v_4xyz+v_5xz^2\\
&+v_6y^3+v_7y^2z+v_8yz^2+v_9z^3,
\end{split}
\tag{27}
\]
and let \(B=\tau\) in (24).  If \(B\ne0\), the raw \(E_6\)
compatibilities give
\[
v_3=v_5=v_6=v_9=0,\qquad v_7=-v_1,\quad v_8=-v_2.
\tag{28}
\]
The last two modes are precisely the \(y,z\)-translation jets of
\((p-q)^2\), so an affine source translation removes them.  Target shears
then leave \(V_3=D xq\).

Suppose \(B=0\).  If \(w_q=0\), \(V_3\) is initially arbitrary.  The lower
identities give (35), hence \(u_y=u_z=0\).  If the \(q\)-coefficient
\(u_q\) of \(U_2\) is zero, \(E_5\) makes the relevant first-row entries
of \(L_0\) zero directly.  If \(u_q\ne0\), its remaining coefficients
force (28), after which the same translation normalization applies.  If
\(w_q\ne0\), \(E_5\) first gives
\[
\begin{gathered}
v_3=v_5=v_6=v_9=0,\\
u_y=\frac23v_7w_q,\qquad u_z=\frac23v_8w_q,
\end{gathered}
\tag{29}
\]
and the two exact eliminants
\[
\Delta(v_1+v_7)=0,\qquad \Delta(v_2+v_8)=0,\qquad
\Delta=9u_q+8w_0w_q-4w_q^2.
\tag{30}
\]
When \(\Delta\ne0\), (28) follows.  On \(\Delta=0\), put
\[
S_y=v_1+v_7,\qquad S_z=v_2+v_8.
\]
If either \(S_y\) or \(S_z\) is nonzero, the \(E_4\) equations uniquely
give the needed lower coefficients and one further linear compatibility.
After those exact substitutions, two \(E_3\) coefficients are
\[
[xy^2]E_3=\frac49w_q^3S_y^2,\qquad
[xz^2]E_3=-\frac49w_q^3S_z^2.
\tag{31}
\]
Thus \(S_y=S_z=0\), a contradiction to the exceptional assumption.  This
closes the specialization which would be lost by dividing by \(\Delta\).

It remains to treat the normalized form
\[
H_3=(A xq,D xq,x^3),\qquad W_2=w_0p+w_qq.
\tag{32}
\]
The \(E_6\) equations give
\[
(L_0)_{32}=\frac34u_y,\qquad
(L_0)_{33}=\frac34u_z,
\tag{33}
\]
and kill the \(y^2,z^2\) coefficients of \(U_2\).  If \(A\ne0\), \(E_5\)
contains
\[
[y^3z^2]E_5=-\frac32Au_y,\qquad
[y^2z^3]E_5=\frac32Au_z.
\tag{34}
\]
If \(A=0\), instead
\[
[y^3z]E_4=-\frac32u_y^2,\qquad
[yz^3]E_4=\frac32u_z^2.
\tag{35}
\]
In either case \(u_y=u_z=0\).  The remaining \(E_5\) relations then give
\((L_0)_{12}=(L_0)_{13}=0\).  The \(E_6\) solution has
\((L_0)_{32}=(L_0)_{33}=0\), so \(\det L_0=0\).

### Finite-other-critical theorem in the finite-outer-critical chart

No Keller map occurs in the marked-critical triple orbit (22).

## 6. Corrected unresolved boundary

The finite-companion resonance hypersurfaces \(F=0\) and \(G=0\) in the
finite-outer-critical chart (3) are closed in
`WORKING_LINE_22_FG_RESONANCE.md`.  A hostile stabilizer audit found that
the following is the exhaustive remaining frontier relative to the
theorems encoded here.

1. Both outer critical points finite, companion at infinity:
   \[
   H_4=((p-aq)^2,(p-bq)^2,0),\quad a\ne b,\qquad R_3=xq.
   \]
2. One outer critical point at infinity:
   \[
   H_4=((p-aq)^2,q^2,0).
   \]
   For \(R_3=x(p-cq)\), the common-scaling class of \((a,c)\) is genuine.
   Its raw-\(E_7\) strata are
   \[
   \begin{gathered}
   c(3a-c)(3a-2c)\ne0,\qquad
   c=3a\ne0,\qquad 2c=3a\ne0,\\
   c=0,\ a\ne0,\qquad
   a=0,\ c\ne0,\qquad
   a=c=0.
   \end{gathered}
   \]
   The independently audited package
   `line22_marked_critical_infinity/` closes only the last point
   \(a=c=0\).  For \(R_3=xq\), the
   \(a=0\) and \(a\ne0\) orbits remain.
3. The rank-one-restriction pencil
   \[
   p=x^2,\qquad q=y^2+xz,
   \]
   until its full symbolic joint-moduli certificate is recorded.

In particular, the earlier three-item boundary list was not exhaustive.
The exact witness
\[
H_4=((p-q)^2,q^2,0),\qquad R_3=x(p-2q),\qquad
(H_3)_1=(H_3)_2=H_2=0
\]
satisfies \(E_8=E_7=0\) and lies in the omitted chart (5a).  It is a
counterexample to chart exhaustion, not a claimed Keller map.

## 7. Verification and disclosure

`verify_line_22_finite_outer_critical_sympy.py` reconstructs the finite-chart \(E_7\) weight
blocks, their exact minors, the affine-jet kernel, the normalized \(E_6\)
and \(E_5\) exits, the noncritical-triple square compatibilities, and the
complete marked-critical case split through the exceptional \(E_3\)
coefficients (31).

`verify_line_22_finite_outer_critical_pari.gp` independently recomputes the displayed
determinant identities in PARI/GP, including (21), (26), (31), and the
normalized exit (34)--(35).  It does not replace the SymPy rank/minor
certificate; it is a second implementation of the decisive polynomial
identities.  `run_verify_line_22_finite_outer_critical_pari.sh` rejects
PARI diagnostics and requires the exact final success sentinel.

These exact calculations are evidence about the encoded identities, not
peer review.  A `__debug__` guard rejects optimized Python, under which
assertions would otherwise disappear.  The result was developed with AI
assistance and has not been peer reviewed.
