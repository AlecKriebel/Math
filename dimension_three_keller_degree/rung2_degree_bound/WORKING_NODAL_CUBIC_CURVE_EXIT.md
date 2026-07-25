# Working theorem: the transverse nodal-cubic leading stratum

**Status:** proved and independently adversarially confirmed from raw
coefficient systems.  This is not peer reviewed.  The source-specific
priority search found no exact prior statement and is not a guarantee of
worldwide priority.

**Recorded:** 2026-07-25T02:00:00Z.

## 1. Statement

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
be a total-degree-four Keller map.  Suppose its leading projective image is
an irreducible nodal cubic, its linear fixed divisor is transverse to the
minimal source pencil, and the normalization map is unramified.  Equivalently,
after independent linear source and target changes,
\[
H_4=rA(p,q),\qquad
A=(p^2q,\;pq^2,\;p^3+q^3)^T,
\tag{1}
\]
where \(p,q,r\) are source coordinates.

### Theorem

No such Keller map exists.

Thus the transverse nodal row
\[
(e,a,b,\delta,\nu)=(1,1,3,3,1)
\]
in `WORKING_QUARTIC_CURVE_TAXONOMY.md` is empty.  The cuspidal
normal-minor branch and the locus where the fixed linear factor belongs to
\(\langle p,q\rangle\) are not covered.

## 2. Degree eight

Write
\[
A_p=\partial_pA,\qquad A_q=\partial_qA,\qquad
\Delta=A_p\times A_q.
\]
The three components of \(\Delta\) have gcd one.  The taxonomy theorem's
degree-eight Hilbert--Burch calculation gives
\[
H_3=A_p(\ell+\alpha r)+A_q(m+\beta r),
\tag{2}
\]
where \(\ell,m\) are binary linear forms and
\(\alpha,\beta\in\mathbb C\).

## 3. The first degree-seven obstruction

Put
\[
\ell=ap+bq,\qquad m=cp+dq,\qquad
V=\ell A_p+mA_q.
\]
Specializing the degree-seven Keller identity at \(r=0\) gives
\[
\det(V_p,V_q,A)=0.
\]
For (1), exact expansion factors this determinant as
\[
\boxed{
\det(V_p,V_q,A)=
6(p^3+q^3)
\bigl(cp^2+(d-a)pq-bq^2\bigr)^2.
}
\tag{3}
\]
Therefore
\[
b=c=0,\qquad d=a.
\]
Euler's identity \(pA_p+qA_q=3A\) turns (2) into
\[
H_3=\lambda A+rD A,\qquad
D=\alpha\partial_p+\beta\partial_q
\tag{4}
\]
for a scalar \(\lambda\).

## 4. The full degree-seven identity

Let \(u,v\in\mathbb C\).  Substituting (4) into the complete degree-seven
coefficient gives a rank-sixteen linear system in the eighteen coefficients
of \(H_2\).  Its exact solution is
\[
\boxed{
H_2=\frac13(uA_p+vA_q)+\frac r2D^2A.
}
\tag{5}
\]
No normalization of the arbitrary invertible linear part \(L_0\) is made
here.

## 5. Degrees six and five

The degree-six coefficient is linear in the nine entries of \(L_0\).  It
has rank nine and forces
\[
\boxed{
L_0=
\begin{pmatrix}
-2\alpha\beta\lambda+\frac23(\alpha v+\beta u)&
-\alpha^2\lambda+\frac23\alpha u&
\alpha^2\beta\\
-\beta^2\lambda+\frac23\beta v&
-2\alpha\beta\lambda+\frac23(\alpha v+\beta u)&
\alpha\beta^2\\
-3\alpha^2\lambda+2\alpha u&
-3\beta^2\lambda+2\beta v&
\alpha^3+\beta^3
\end{pmatrix}.
}
\tag{6}
\]
In particular,
\[
\det L_0=
\frac49(\alpha^3+\beta^3)(\alpha v-\beta u)^2.
\tag{7}
\]

With (5)--(6) imposed, the entire degree-five coefficient factors as
\[
\boxed{
E_5=\frac49(p^3+q^3)
\bigl((3\beta\lambda-v)p+(u-3\alpha\lambda)q\bigr)^2.
}
\tag{8}
\]
The Keller condition makes \(E_5=0\), hence
\[
u=3\alpha\lambda,\qquad v=3\beta\lambda.
\tag{9}
\]
But (9) makes \(\alpha v-\beta u=0\), so (7) gives
\[
\det L_0=0,
\]
contrary to the Keller hypothesis.  This proves the theorem.

## 6. Verification boundary and disclosure

The accompanying SymPy and PARI/GP regressions check (3), solve the complete
degree-seven and degree-six coefficient systems, and verify (5)--(8) by
direct determinant expansion.  These computations concern the displayed
nodal normal form; projective equivalence of irreducible nodal plane cubics
is a geometric input rather than a computer check.

The adversarial audit began again with a general eighteen-coefficient
\(H_2\) and general nine-entry \(L_0\).  It independently obtained ranks
sixteen and nine, respectively, and reproduced every sign and factor in
(3), (5)--(8).  In particular it confirmed the plus sign in
\(\frac r2D^2A\), which is easy to reverse if the inhomogeneous side of the
linear system is encoded with the wrong sign.

This proof was developed with AI assistance.  Exact computer algebra is
evidence about the encoded identities, not peer review.  The theorem has
not been peer reviewed.
