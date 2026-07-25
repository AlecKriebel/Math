# External hostile audit: rank-one fixed-divisor triple companion

**Completed:** 2026-07-25T10:42:11Z.
**Verdict:** **PASS, after externally closing two certificate/prose gaps.**
**Scope:** the full \(A=0\) branch is reconstructed here.  The previously
completed `aopen_independent/` audit is used only in the final
\(A=0\)/\(A\ne0\) coverage ledger.

This is not peer review.  Exact computation checks the encoded algebra; it
does not substitute for mathematical review.

## 1. Audited statement

Put
\[
q=y^2+xz,\qquad
H_4=(x^4,x^2q,0),\qquad (H_3)_3=R=x^3.
\]
The theorem under audit says that no degree-four map with these leading
pieces has constant nonzero Jacobian.

The raw \(E_7\) system has rank \(8\) in \(26\) variables.  Its
eighteen-dimensional kernel is spanned by four independent legal gauges
and fourteen normal directions.  The four gauges are:

1. the two determinant-one target shears adding the third component to
   the first or second;
2. source translation in \(x\);
3. source translation in \(y\).

Source translation in \(z\) gives the same top direction as the second
target shear.  Thus five transformations are available, but their
effective top-gauge space has dimension exactly four.

After quotienting by these gauges, the complete normal form is
\[
\begin{aligned}
W={}&w_1xy+w_2xz+w_3y^2+w_4yz+w_5z^2,\\
U={}&Axq+\frac43xW,\\
V={}&C_0x^2z+C_1xy^2+C_2xyz+C_3xz^2\\
 &\quad+C_4y^3+C_5y^2z+C_6yz^2+C_7z^3.
\end{aligned}
\]
The external raw maximal minor is \(-7558272\), and the eighteen kernel
vectors have independence minor \(-512/27\).

## 2. Exhaustive \(A=0\) branch cover

The lower-variable \(E_6\) matrix has constant rank \(4\) and constant
pivot \(-1296\).  Denominator-free polynomial left syzygies successively
give
\[
w_5^2=0,\qquad w_4^2=0,\qquad
w_3w_1=0,\qquad w_3(w_3-w_2)=0.
\]
Consequently every \(A=0\) point lies in exactly the following cover:

- \(w_3=s\ne0\), where \(W=sq\);
- \(w_3=0\) and \(w_1=w_2=0\), the origin;
- \(w_3=0\), \(w_2\ne0\), reduced legally to \(W=sxz\);
- \(w_3=0\), \(w_2=0\), \(w_1\ne0\), giving \(W=sxy\).

No generic-rank assertion is used to specialize into one of these leaves.

## 3. The \(w_3\ne0\) leaf

Polynomial \(E_5\) syzygies force
\[
C_2=C_3=C_4=C_5=C_6=C_7=0.
\]
Writing \(D=C_0-C_1\), the \(D=0\) matrix is rebuilt before solving.
Its \(E_5\) pivot is \(64s^2\), and it forces
\[
\ell_{12}=\ell_{13}=\ell_{32}=\ell_{33}=0.
\]

For \(D\ne0\), the \(E_5\) pivot is supported on \(Ds^2\).  Put
\(r=a_3\).  The complete \(E_6/E_5\) solution has
\[
\begin{gathered}
a_1=a_4=a_5=\ell_{12}=\ell_{32}=0,\\
a_2=r+\frac43sD,\qquad
\ell_{13}=Dr,\qquad \ell_{33}=sD.
\end{gathered}
\]
The external monomial order finds a four-variable \(E_4\) pivot
\[
\frac{4096}{81}s^8,
\]
which is safe uniformly in \(r\).  The formerly hidden \(r=0\) leaf was
also rebuilt separately; its five-variable rank-four system has pivot
\[
-\frac{4096}{81}s^8
\]
and complete solution
\[
b_1=b_4=b_5=0,\qquad b_2=C_1D+b_3.
\]
Then \(E_3\) contains
\[
\frac43s^2\ell_{22}
\]
as the \(x^2z\)-coefficient, while
\[
\det L=D\,s\,\ell_{11}\ell_{22}.
\]
Thus the \(r=0\) specialization is singular.  For \(r\ne0\), the same
coefficient kills \(\ell_{22}\), and
\[
\det L=D\ell_{22}(s\ell_{11}-r\ell_{31})=0.
\]

## 4. The origin

The complete literal \(E_5\) polynomial is reconstructed.  On \(a_3=0\)
it first forces \(\ell_{12}=\ell_{13}=0\); two \(E_4\) coefficients are
\[
\frac83\ell_{33}^2,\qquad
\frac43(3a_0\ell_{33}-2\ell_{31}\ell_{33}-\ell_{32}^2).
\]
Hence \(\ell_{33}=\ell_{32}=0\), and \(\det L=0\).

On \(a_3=r\ne0\), the literal \(E_5\) rows force
\[
C_2=\cdots=C_7=0.
\]
A fresh \(E_4\) pivot is supported on \(r^4\), including \(D=0\).
After the complete solve,
\[
[x^3]E_3=-3r\ell_{22},\qquad
3\det L=D\ell_{31}[x^3]E_3.
\]
This closes both \(D\)-specializations.

## 5. Legal reduction to the axis charts

The source shear
\[
(x,y,z)\longmapsto
(x,\ y+\alpha x,\ z-2\alpha y-\alpha^2x)
\]
has determinant \(1\) and preserves \(q\).  It acts on the relevant
part of \(W\) by
\[
x(w_1y+w_2z)\longmapsto
x\!\left((w_1-2\alpha w_2)y+w_2z+
(\alpha w_1-\alpha^2w_2)x\right).
\]
If \(w_2\ne0\), take \(\alpha=w_1/(2w_2)\).  The new \(xy\)-coefficient
vanishes and the \(x^2\)-residue is \(k=w_1^2/(4w_2)\).

The exact legal compensation is not the target shear described in an
early comment.  One third of the source \(x\)-translation has top
direction
\[
\left(\frac43x^3,\ \frac23xy^2+x^2z,\ x^2\right).
\]
Subtracting \(k\) times this direction removes the correlated
\((\frac43kx^3,kx^2)\) residue; its middle component merely relabels the
free \(C_0,C_1\) coefficients of \(V\).  This proves legality without
changing \(A\) and without division outside the declared \(w_2\ne0\)
chart.

## 6. The \(xz\) axis

Every \(E_5\) rank drop is recomputed through augmented minors:
\[
\begin{array}{c|c}
\text{open parameter}&\text{inconsistent augmented minor}\\ \hline
C_6&\text{unit}\cdot s^6C_6\\
3C_5-2s&\text{unit}\cdot s^6(3C_5-2s)\\
C_4&\text{unit}\cdot s^6C_4.
\end{array}
\]
Thus only
\[
C_6=C_4=0,\qquad C_5=\frac23s
\]
survives.  On \(C_7\ne0\), the complete \(E_5\) pivot is supported on
\(s^3C_7\), after which
\[
[yz^3]E_4=-\frac8{27}s^4\ne0.
\]
The specialization \(C_7=0\) is rebuilt and already has a
denominator-free \(s^3\) incompatibility at \(E_5\).

## 7. The \(xy\) axis

Successive augmented minors force
\[
C_7=C_6=C_5=C_3=0
\]
without specializing a generic solve.  Put
\[
h=2s-3C_4.
\]
The leaf \(h=0\) is freshly inconsistent at \(E_5\).  On \(h\ne0\), the
complete \(E_5\) pivot is supported on \(hs^2\), and the selected
\(E_4\) pivot is supported on \(s^{10}/h^3\).  The full \(E_4\)
compatibility is
\[
\begin{aligned}
C_1s^2(s-h)+(3h^2+2s^2)\ell_{32}&=0,\\
(3h+2s)(-6C_2-3h+4s)&=0.
\end{aligned}
\]

For \(3h+2s=0\), one obtains
\[
\ell_{32}=-\frac12C_1s,\qquad C_2=s,
\]
and the complete \(E_3\) residual is
\[
\frac29C_1s^3(2C_0-3C_1)xy^2.
\]
The \(C_1=0\) descendant closes by the square chain
\[
C_0^2,\quad \ell_{31}^2,\quad b_1^2,
\]
followed by \(\det L=0\).  The other descendant
\(2C_0=3C_1\), with \(C_1\ne0\), closes by the displayed \(E_2\)
relations and \(\det L=0\).  Their intersection is the \(C_1=0\) leaf
already handled.

For the second factor,
\[
C_2=\frac{4s-3h}{6},\qquad G=3h^2+2s^2.
\]
If \(G\ne0\), solving the other \(E_4\) equation makes an \(E_3\)
coefficient
\[
\frac{s^4(3h+2s)^2}{243h},
\]
so the branch lands in the first factor.  At that intersection its
\(C_2\) and \(\ell_{32}\) values agree exactly with the first-factor
solve.

If \(G=0\), the exact resultant
\[
\operatorname{Res}_h(G,s-h)=5s^2
\]
forces \(C_1=0\).  The complete \(E_4\) remainder is a multiple of
\(G\), while the same \(E_3\) square and
\[
(3h+2s)^2-3G=-2s(s-6h),\qquad G(6h,h)=75h^2
\]
contradict \(s\ne0\).  Thus every \(h\)-, factor-, \(G\)-, and
intersection leaf is closed.

## 8. Defects found and disposition

No theorem counterexample or surviving algebraic leaf was found.  Three
verification/exposition issues were found:

1. At the start of this audit, the supplied PARI replay incorrectly
   required a full \(E_3\) residual to vanish before imposing the genuine
   compatibility \(C_1(2C_0-3C_1)=0\).  That snapshot failed when run.
2. The primary SymPy presentation verified an \(E_4\) parametrization on
   the \(w_3\ne0,D\ne0\) leaf but did not certify completeness at
   \(r=a_3=0\); its selected minor carried \(r^4\).  The external
   \(s^8\) pivots above close this gap, both uniformly and after a fresh
   \(r=0\) rebuild.
3. An early comment attributed the axis-compensation step to a
   coordinate-two target shear.  The exact legal mechanism is the
   \(x\)-translation plus free-\(V\)-tail relabeling recorded in
   Section 5.

These are certificate/prose defects, not defects in the theorem after the
external repairs.

## 9. Full theorem coverage

The normal coefficient \(A\) gives the exhaustive split
\[
A=0\quad\text{or}\quad A\ne0.
\]
This package independently reconstructs the first branch.  The sibling
`aopen_independent/` package already gives a strict, fail-closed PARI
audit of the second.  `verify_full_coverage_strict.sh` runs both packages
and their fault guards.  Therefore the scoped verdict for the full
rank-one fixed-divisor \(e=2\) triple-companion theorem is **PASS**.

Seven mutations of the external certificate are rejected: the raw
minor, \(E_6\) branch equation, \(r=0\) pivot, shear compensation,
\(xz\) terminal coefficient, \(xy\) terminal factor, and final
attestation.
