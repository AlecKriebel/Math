# Working theorem: the genuine line-image \((1,4)\) stratum

**Status:** proved and independently adversarially audited, including the
arbitrary-linear-part correction in Section 3.  This is not peer reviewed.
The source-specific priority search is not a guarantee of worldwide
priority.

**Recorded:** 2026-07-24T23:59:52Z.

## 1. Setup and statement

Use independent source coordinates \((p,q,r)\) and target coordinates in
which
\[
F=L_0X+H_2+H_3+H_4,\qquad
H_4=(P(p,q),Q(p,q),0),
\tag{1}
\]
where \(L_0\in\operatorname{GL}_3(\mathbb C)\), and \(P,Q\) are coprime
binary quartics.  Write
\[
H_3=(U,V,R),\qquad H_2=(A,B,W),
\]
and put
\[
a=J_{p,q}(Q,R),\qquad
b=J_{p,q}(P,R),\qquad
c=J_{p,q}(P,Q).
\tag{2}
\]

### Theorem

If
\[
\gcd(a,b,c)=1,
\tag{3}
\]
then \(F\) is a polynomial automorphism.  Consequently every counterexample
in the \((1,4)\) line-image stratum must have a nonconstant common
ramification factor:
\[
\boxed{
\gcd\bigl(J(P,Q),J(P,R),J(Q,R)\bigr)\ne1.
}
\tag{4}
\]

The condition is nonvacuous.  For example,
\[
\begin{aligned}
P&=p^4+q^4,\\
Q&=p^3q+2pq^3,\\
R&=p^3+pq^2+q^3
\end{aligned}
\]
gives \(\gcd(a,b,c)=1\).

## 2. Degrees eight and seven

The degree-eight determinant coefficient is
\[
c\,\partial_rR=0.
\]
Since \(c\ne0\),
\[
R\in\mathbb C[p,q]_3.
\tag{5}
\]

Direct row replacement in degree seven gives
\[
c\,\partial_rW
+a\,\partial_rU
-b\,\partial_rV=0.
\]
Therefore
\[
cW+aU-bV\in\mathbb C[p,q]_8.
\tag{6}
\]

The signed triple \((a,-b,c)\) consists of the maximal minors of
\[
\begin{pmatrix}
P_p&P_q\\
Q_p&Q_q\\
R_p&R_q
\end{pmatrix}.
\tag{7}
\]
Under (3), its ideal in \(S=\mathbb C[p,q]\) has height two.
Hilbert--Burch gives
\[
0\longrightarrow S(-8)^2
\longrightarrow S(-5)^2\oplus S(-6)
\longrightarrow(a,b,c)\longrightarrow0.
\tag{8}
\]
In particular, every nonzero homogeneous syzygy has total degree at least
\(8\); the two minimal generators have coefficient degrees
\((3,3,2)\).

Expand (6) in powers of \(r\).  The coefficients of \(r^3,r^2,r\) would
give syzygies of total degrees \(5,6,7\), respectively.  They must vanish:
\[
U,V,W\in\mathbb C[p,q].
\tag{9}
\]

## 3. Degree six and the arbitrary linear part

Let
\[
\lambda=(L_0)_{3r}
\]
be the third target component of the linear image of the \(r\)-direction.
Since (9) makes \(JH_3\) binary, \(\det JH_3=0\).  The degree-six
coefficient is exactly
\[
a\,\partial_rA-b\,\partial_rB+c\lambda=0.
\tag{10}
\]
This is a homogeneous syzygy of total degree \(6\), now over
\(S[r]\).  The Hilbert--Burch resolution (8) remains exact after adjoining
\(r\), so (10) forces
\[
\partial_rA=\partial_rB=\lambda=0.
\tag{11}
\]

Tracking \(\lambda\) is essential.  One cannot simultaneously normalize
\(L_0=I\) and retain the independently chosen source pencil and target
value-line coordinates.  An earlier draft that did so would have hidden the
conclusion \(\lambda=0\).

Equations (5), (9), and (11) show that every nonlinear term depends only on
\(p,q\).  The nonzero vector \(L_0(\partial_r)\) lies in the leading target
plane because its third component is zero.  A final target linear change
sends this vector to the third coordinate direction.  The map becomes
\[
\bigl(G_1(p,q),G_2(p,q),\alpha r+h(p,q)\bigr),
\qquad \alpha\ne0,
\tag{12}
\]
with \(\deg G\le4\).  Its Jacobian factors as
\[
\alpha\det JG\in\mathbb C^\times.
\]
The established plane low-degree theorem makes \(G\) an automorphism, and
the third component of (12) is a shear.  Hence \(F\) is an automorphism.

## 4. Scope

The unresolved \((1,4)\) locus is the common-ramification-factor locus
\[
\gcd(a,b,c)\ne1.
\]
The theorem does not assert that every point of that locus is compatible
with the remaining Keller identities.
