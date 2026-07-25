# Working theorem: the scalar-aligned nodal-cubic leading stratum

**Status:** proved and independently adversarially confirmed from the raw
determinant identities.  This is not peer reviewed.  The source-specific
priority search found no exact prior statement and is not a guarantee of
worldwide priority.

**Recorded:** 2026-07-25T02:30:00Z.

## 1. Statement

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
be a total-degree-four Keller map.  Suppose its leading projective image is
an irreducible nodal cubic, its normalization map is unramified, and its
linear fixed divisor belongs to the minimal source pencil.  After independent
linear source and target changes this says
\[
H_4=h(p,q)A(p,q),\qquad
A=(p^2q,\;pq^2,\;p^3+q^3)^T,
\tag{1}
\]
where \(h\) is a nonzero binary linear form and \(r\) is a complementary
source coordinate.

### Theorem

Every such Keller map is a polynomial automorphism.  In particular, no
Keller counterexample lies in this stratum.

Together with `WORKING_NODAL_CUBIC_CURVE_EXIT.md`, this excludes the entire
nodal row
\[
(e,a,b,\delta,\nu)=(1,1,3,3,1)
\]
of `WORKING_QUARTIC_CURVE_TAXONOMY.md`.  It does not address a cuspidal
cubic image.

## 2. Degree eight

Put
\[
A_p=\partial_pA,\qquad A_q=\partial_qA,\qquad
\Delta=A_p\times A_q.
\]
Euler's identity and the homogeneity of \(h\) give
\[
(H_4)_p\times(H_4)_q=\frac43h^2\Delta.
\tag{2}
\]
The three components
\[
\Delta=
\bigl(-3q(2p^3-q^3),\;3p(p^3-2q^3),\;3p^2q^2\bigr)^T
\tag{3}
\]
have gcd one.  Their Hilbert--Burch syzygy module is generated in degree
two by \(A_p,A_q\).

The degree-eight Keller identity is
\[
\bigl((H_4)_p\times(H_4)_q\bigr)\mathbin{\cdot}\partial_rH_3=0.
\]
Since \(\partial_rH_3\) is quadratic, (2)--(3) and the syzygy resolution
force
\[
\partial_rH_3=\alpha A_p+\beta A_q.
\]
Thus
\[
\boxed{H_3=V(p,q)+r(\alpha A_p+\beta A_q)}
\tag{4}
\]
for an arbitrary binary cubic vector \(V\).

## 3. A marked-point calculation, with no hidden normalization

After possibly interchanging \(p,q\), scale \(h\) so that
\[
h=p+kq
\tag{5}
\]
for an arbitrary \(k\in\mathbb C\).  It is important not to set \(k=-1\):
the zero of \(h\) is a marked point on the normalization of the embedded
nodal cubic, and the smooth marked points are not a priori one projective
orbit.

Write a completely general binary cubic vector \(V\) (twelve coefficients)
and a completely general quadratic vector \(H_2\) (eighteen coefficients).
Substitution of (4)--(5) into the full degree-seven determinant coefficient
is linear in these thirty nuisance coefficients.  Exact elimination gives
the following four necessary compatibility equations:
\[
\begin{aligned}
C_0={}&k\alpha^2+2k^2\alpha\beta+(k^3-3)\beta^2=0,\\
C_1={}&2k^2\alpha^2+(4k^3+6)\alpha\beta
       +(2k^4-9k)\beta^2=0,\\
C_2={}&\alpha^2-4k\alpha\beta+k^2\beta^2=0,\\
C_3={}&k(-2\alpha^2+2k\alpha\beta+k^2\beta^2)=0.
\end{aligned}
\tag{6}
\]

These are not inferred from sample ranks.  For completeness, order the
nonzero degree-seven coefficient rows by
\[
\begin{split}
&(p^7,p^6q,p^6r,p^5q^2,p^5qr,p^4q^3,p^4q^2r,
  p^3q^4,p^3q^3r,\\
&\hspace{35mm}p^2q^5,p^2q^4r,pq^6,pq^5r,q^7,q^6r).
\end{split}
\tag{7}
\]
Four polynomial left-null rows of the \(15\times30\) nuisance-coefficient
matrix are
\[
\begin{aligned}
&(0,0,-2(2k^3-1),0,3k^2,0,-2k,0,1,0,0,0,0,0,0),\\
&(0,0,-3k(k-1)(k^2+k+1),0,(4k^3+1)/2,0,-k^2,0,0,0,1,0,0,0,0),\\
&(0,0,0,0,k,0,0,0,0,0,0,0,1,0,0),\\
&(0,0,-k^3,0,k^2/2,0,0,0,0,0,0,0,0,0,1).
\end{aligned}
\tag{8}
\]
Pairing them with the inhomogeneous side gives respectively
\(-8C_0,-4C_1,8C_2,-4C_3\).  Equations (7)--(8) are an exact certificate
valid at every specialization of \(k\), including rank-jump values.

If \(k=0\), then \(C_0=-3\beta^2\) and \(C_2=\alpha^2\), so
\(\alpha=\beta=0\).  Suppose \(k\ne0\).  If \(\beta=0\), \(C_2=0\) again
gives \(\alpha=0\).  Otherwise put \(t=\alpha/(k\beta)\).  The last two
equations in (6) become
\[
t^2-4t+1=0,\qquad -2t^2+2t+1=0.
\]
Twice the first plus the second gives \(t=1/2\), which does not satisfy
the first.  Hence in all cases
\[
\boxed{\alpha=\beta=0.}
\tag{9}
\]
The omitted chart \(h=q\) is carried to \(h=p\) by interchanging \(p,q\)
and the first two target coordinates.

## 4. The binary collapse

By (9), \(H_3=V(p,q)\) is binary.  The complete degree-seven identity now
reduces to
\[
\frac43h^2\Delta\mathbin{\cdot}\partial_rH_2=0.
\tag{10}
\]
The vector \(\partial_rH_2\) is homogeneous linear.  But (3) has no
syzygy below degree two, so (10) forces
\[
\partial_rH_2=0.
\tag{11}
\]
Consequently every nonlinear homogeneous part of \(F\) depends only on
\(p,q\).

The constant term of the determinant identity is
\(\det L_0=\det JF\ne0\).  Let \(v=L_0(\partial_r)\), and make a target
linear change sending \(v\) to the third coordinate vector.  The first two
components of the transformed map are then a plane Keller map
\[
G:\mathbb A^2_{p,q}\longrightarrow\mathbb A^2
\]
of degree at most four.  The unconditional plane degree bound makes \(G\)
an automorphism.  The third component is a nonzero scalar multiple of
\(r\) plus a polynomial in \(p,q\), so \(F\) is an automorphism as well.
This proves the theorem.

## 5. Verification boundary and disclosure

`verify_scalar_aligned_nodal_sympy.py` constructs the general twelve-
coefficient \(V\), general eighteen-coefficient \(H_2\), and arbitrary
marked-point parameter \(k\).  It verifies (2), the full \(15\times30\)
degree-seven system, the four polynomial left-null certificates (8), the
compatibility ideal (6), the absence of a linear syzygy of \(\Delta\), and
the reduction (10).  The \(k=0\) and \(k=-1\) specializations are retained
as regressions.

The geometric normalization of an irreducible nodal plane cubic and the
Hilbert--Burch interpretation are mathematical inputs rather than computer
checks.  The independent audit began from raw Jacobian columns and recovered
\[
E_7=\operatorname{tr}(\operatorname{adj}(JH_4)JH_2)
   +\operatorname{tr}(\operatorname{adj}(JH_3)JH_4).
\]
It then reconstructed the complete thirty-coefficient system, checked that
the rows (8) are division-free at every specialization of \(k\), and
independently verified the Hilbert--Burch shifts, the omitted \(h=q\) chart,
the no-linear-syzygy step, and the plane-plus-shear exit.  No scope gap or
counterexample was found.

This proof was developed with AI assistance.  Exact computer algebra is
evidence about the encoded identities, not peer review.  The theorem has
not been peer reviewed.
