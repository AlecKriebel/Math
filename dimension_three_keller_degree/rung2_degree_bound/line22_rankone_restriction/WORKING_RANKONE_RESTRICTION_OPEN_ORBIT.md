# Theorem: the open rank-one-restriction line-\((2,2)\) orbit

**Status:** exact working theorem; independent hostile audit passed at
2026-07-25T07:02:00Z.  This is not peer reviewed.  The source-specific
priority search found no matching statement, but is not a guarantee of
worldwide priority.

**Recorded:** 2026-07-25T06:37:11Z.

## 1. Scope and theorem

Let
\[
F=LX+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow\mathbb A^3_{\mathbb C}
\]
have total degree four and constant nonzero Jacobian.  Work in the
unique-double-line line-image \((2,2)\) row and in the
rank-one-restriction pencil
\[
p=x^2,\qquad q=y^2+xz.                                   \tag{1}
\]
The value \(p=0\) is the marked double-line member.

Assume the two critical points of the degree-two outer map avoid the
marked value.  The exact stabilizer calculation below permits the joint
normal form
\[
H_4=\bigl((p-q)^2,(p+q)^2,0\bigr),                       \tag{2}
\]
\[
R:=(H_3)_3=x(p-cq),                                      \tag{3}
\]
where \(c\in\mathbb C\), with the only residual ambiguity
\(c\leftrightarrow-c\).

### Theorem

If
\[
\boxed{c(c^2-9)\ne0,}                                    \tag{4}
\]
then no Keller map has the leading data (1)--(3).

Thus every finite mixed-companion orbit in the unmarked-critical family is
excluded except the single resonance class \(c^2=9\).  This includes
\(c^2=1\), where the companion equals one of the two outer critical points.
The triple \(c=0\), the resonance \(c^2=9\), and the companion
\(c=\infty\) are not claimed here.

## 2. Exact source stabilizer

The member \(p=x^2\) is the unique double line of the pencil.  Indeed, a
member \(q+\lambda p\), restricted to \(x=0\), equals \(y^2\).  If it were
the square of a linear form, that form would be \(y+\mu x\) up to sign,
whose square has no \(xz\)-term.

Let a source linear transformation preserve the pencil.  Uniqueness of the
double line first gives \(x'=\alpha x\).  Restriction of \(q'\) to \(x=0\)
then forces \(y'=\gamma x+\beta y\).  Comparing the \(xy,xz,x^2\)
coefficients gives the complete form
\[
\begin{aligned}
x'&=\alpha x,\\
y'&=\gamma x+\beta y,\\
z'&=\delta x-\frac{2\beta\gamma}{\alpha}y
             +\frac{\beta^2}{\alpha}z,
\end{aligned}                                             \tag{5}
\]
with \(\alpha\beta\ne0\).  Conversely every transformation (5) preserves
the pencil, since
\[
p'=\alpha^2p,\qquad
q'=\beta^2q+(\gamma^2+\alpha\delta)p.                     \tag{6}
\]
Its determinant is \(\beta^3\).

In the base coordinate \(u=p/q\), (6) induces
\[
u\longmapsto
\frac{\alpha^2u}{\beta^2+(\gamma^2+\alpha\delta)u}.        \tag{7}
\]
Over \(\mathbb C\), every Möbius transformation fixing \(u=0\) occurs in
(7).  Thus the induced group is exactly the full Borel subgroup fixing the
marked double-line value.  This is strictly larger than the scaling group
for the other pencil \(\langle x^2,yz\rangle\); its orbit taxonomy cannot
be imported from that pencil.

## 3. Complete joint-moduli taxonomy

A separable degree-two map of \(\mathbb P^1\) has two distinct critical
points.  After a target change, if those points are \(r,s\), its two
coordinates are the squares of linear forms vanishing at \(r,s\).
The degree-eight first-integral result for the line-\((2,2)\) row says that
the cubic companion is either \(x^3\), corresponding to the marked point
\(0\), or \(x\) times another pencil member, corresponding to a point
\(c\in\mathbb P^1\).

The Borel action (7) gives exactly the following orbits.

| Outer critical pair | Companion orbit | Joint normal form |
|---|---|---|
| contains \(0\) | triple at \(0\) | \(H_4=(p^2,q^2,0),\ R=x^3\) |
| contains \(0\) | mixed at the other critical point | \(H_4=(p^2,q^2,0),\ R=xq\) |
| contains \(0\) | mixed and distinct from both | \(H_4=(p^2,q^2,0),\ R=x(p-q)\) |
| avoids \(0\) | triple at \(0\) | (2), \(R=x^3\) |
| avoids \(0\) | finite mixed | (2), \(R=x(p-cq)\), \(c\in\mathbb C^\times/\{\pm1\}\) |
| avoids \(0\) | mixed at infinity | (2), \(R=xq\) |

For the first three rows, normalize the critical pair to
\(\{0,\infty\}\).  Its residual scaling is transitive on
\(\mathbb P^1\setminus\{0,\infty\}\).  For the last three rows, sharp
two-transitivity of the Borel on
\(\mathbb P^1\setminus\{0\}\) normalizes the unordered critical pair to
\(\{1,-1\}\).  The only transformations preserving
\(\{0,\{1,-1\}\}\) are \(u\mapsto u\) and \(u\mapsto-u\), giving precisely
\(c\sim-c\).  In particular, the table retains every critical-companion
incidence and the generic cross-ratio; there is no hidden finite-chart
normalization.

## 4. Complete raw \(E_7\) stratification

Put
\[
U=(H_3)_1,\qquad V=(H_3)_2,\qquad W=(H_2)_3,
\]
and define
\[
\partial:=2y\partial_z-x\partial_y.
\]
Since
\(\nabla p\times\nabla q=2x(0,-x,2y)\), the degree-seven identity for
(2)--(3) is exactly
\[
\begin{split}
E_7=2\{&
8x(p-q)(p+q)\partial W\\
&+(p+q)((-3-2c)p+cq)\partial U\\
&+(p-q)((2c-3)p+cq)\partial V\}=0.                       \tag{8}
\end{split}
\]
This is a linear map from the \(26\) coefficients of two cubics and one
quadratic to degree-seven forms.  Exact row reduction gives:

| Joint orbit | Raw \(E_7\) rank | Nullity |
|---|---:|---:|
| marked critical pair, triple | \(8\) | \(18\) |
| marked critical pair, mixed at other critical point | \(18\) | \(8\) |
| marked critical pair, mixed distinct | \(18\) | \(8\) |
| unmarked critical pair, triple \(c=0\) | \(16\) | \(10\) |
| unmarked, finite \(c^2=9\) | \(14\) | \(12\) |
| unmarked, finite \(c(c^2-9)\ne0\) | \(18\) | \(8\) |
| unmarked, companion \(c=\infty\) | \(18\) | \(8\) |

The resonance \(c=3\) and \(c=-3\) is one joint orbit because
\(c\sim-c\).

The open rank assertion has a compact exact certificate.  In the monomial
orders recorded in the verifier, an \(18\times18\) minor is
\[
-769482217582755840\,c^6(c-3)^4(c+3)^4.                  \tag{9}
\]
There are also eight independent universal kernel directions.  Six are
\[
\begin{gathered}
(x^3,0,0),\ (xq,0,0),\ (0,x^3,0),\ (0,xq,0),\\
(0,0,p),\ (0,0,q),
\end{gathered}                                            \tag{10}
\]
and two are the source-translation jets
\[
\tau_x=(\partial_xH_{4,1},\partial_xH_{4,2},\partial_xR),
\quad
\tau_y=(\partial_yH_{4,1},\partial_yH_{4,2},\partial_yR). \tag{11}
\]
Their displayed coefficient matrix has a constant minor \(-8\).  The
third translation jet is not missing; it satisfies the exact relation
\[
\tau_z+2(x^3,0,0)-2(xq,0,0)-2(0,x^3,0)-2(0,xq,0)
 +c(0,0,p)=0.                                            \tag{12}
\]
Equations (9)--(12) prove, without a generic-rank assumption, that (10)--(11)
are the complete kernel under (4).

Affine source translations in \(x,y\) remove (11).  Target shears adding
the third component to the first two remove their \(x^3\)-terms, because
\(R=x^3-cxq\).  All lower coefficients are merely relabelled, so the
complete open normal form is
\[
H_3=(A\,xq,B\,xq,x(p-cq)),\qquad
W=w_0p+w_1q.                                             \tag{13}
\]

## 5. Degree-six forcing

Write a general quadratic in the basis adapted to (1):
\[
\begin{aligned}
U_2&=u_0p+u_qq+\widehat u_1xy+\widehat u_2xz
                 +\widehat u_3yz+\widehat u_4z^2,\\
V_2&=v_0p+v_qq+\widehat v_1xy+\widehat v_2xz
                 +\widehat v_3yz+\widehat v_4z^2.
\end{aligned}                                            \tag{14}
\]
Let \(L=(\ell_{ij})\).  After (13), the complete degree-six identity is
linear in exactly the ten variables
\[
\ell_{32},\ell_{33},
\widehat u_1,\ldots,\widehat u_4,
\widehat v_1,\ldots,\widehat v_4,                         \tag{15}
\]
and is independent of every other coefficient in (14) and \(L\).
A specialization-safe \(10\times10\) minor is
\[
-10871635968\,c^2(c-3)^2(c+3)^2.                         \tag{16}
\]
Consequently (4) forces
\[
\ell_{32}=\ell_{33}=0,\qquad
U_2,V_2\in\langle p,q\rangle.                            \tag{17}
\]
Substitution of (17) into every coefficient of \(E_6\) gives zero, so
(17) is the complete degree-six solution rather than a list of selected
necessary equations.

## 6. Degree-five exit

After (17), four coefficients of \(E_5\) are
\[
\begin{aligned}
[x^3z^2]E_5&=-2c(\ell_{12}-\ell_{22}),\\
[y^5]E_5&=4c(\ell_{13}-\ell_{23}),\\
[x^5]E_5&=2((2c+3)\ell_{12}+(3-2c)\ell_{22}),\\
[x^4y]E_5&=-4((2c+3)\ell_{13}+(3-2c)\ell_{23}).
\end{aligned}                                            \tag{18}
\]
Since \(c\ne0\), the first two equations identify the corresponding
entries.  The last two then become \(12\ell_{12}=0\) and
\(-24\ell_{13}=0\).  Hence
\[
\ell_{12}=\ell_{13}=\ell_{22}=\ell_{23}=0.               \tag{19}
\]
Together with (17), the second and third columns of \(L\) vanish.  Thus
\(\det L=0\), contradicting the Keller condition.  This proves the theorem.

## 7. Exact frontier and leading witnesses

Relative to the exhaustive taxonomy in Section 3, this package leaves:

1. the three marked-critical-pair companion orbits;
2. the unmarked triple \(c=0\);
3. the unmarked resonance \(c^2=9\); and
4. the unmarked companion \(c=\infty\).

The raw ranks in Section 4 show that none of these was silently merged into
the open orbit.  Each has an immediate leading witness: set
\((H_3)_1=(H_3)_2=H_2=0\) and use the displayed \(H_4,R\).  Then
\(E_8=\operatorname{Jac}(H_{4,1},H_{4,2},R)=0\) and \(E_7=0\).
These are witnesses only to survival of the two top homogeneous
identities, not Keller maps.

## 8. Verification and disclosure

`verify_rankone_restriction_sympy.py` reconstructs the stabilizer, the full
raw coefficient matrices, the open kernel and maximal minor, all special
raw ranks, the degree-six forcing minor and converse, and the degree-five
exit.

`verify_rankone_restriction_pari.gp` separately rebuilds those
coefficient matrices and decisive identities in PARI/GP.
`verify_rankone_restriction_pari_strict.sh` rejects PARI diagnostics and
requires the exact expected transcript.  `test_verifier_guards.sh`
confirms rejection of optimized Python, forged diagnostics, unexpected
output, missing output, and nonzero exits.  These are independent
implementations of the same coefficient-matrix method, not
methodologically distinct algorithms.

The result was developed with AI assistance.  Exact checks are evidence
about the encoded algebra; they are not peer review.  This note has not
been peer reviewed.  The clean-room hostile reconstruction in
`audit_hostile/REPORT.md` confirms the stabilizer, complete orbit ledger,
alternate raw and lower minors, gauge relations, and determinant exit.
