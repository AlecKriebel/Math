# Working theorem: unramified composite quotient pencils in the rank-one stratum

**Status:** proved and independently adversarially audited.  The audit found
and repaired an omitted arbitrary-linear-part syzygy in degree five.  This
is not peer reviewed.  The source-specific priority search found no exact
prior statement and is not a guarantee of worldwide priority.

**Recorded:** 2026-07-25T01:41:00Z.

## 1. Statement

Use the rank-one setup of
`WORKING_RANK_ONE_QUOTIENT_CUBIC.md`.  Thus
\[
F=L_0X+H_2+H_3+H_4
\]
is a total-degree-four Keller map over \(\mathbb C\),
\[
H_4=a\,h,
\]
and \(P,Q\) are two independent cubic components of \(H_3\) modulo the
line \(\mathbb Ca\).

Assume:

1. \(\gcd(P,Q)=1\);
2. \(\mathbb C(P/Q)\) is not relatively algebraically closed in
   \(\mathbb C(\mathbb P^2)\); and
3. after the binary normalization below,
   \[
   \gcd\bigl(J(P,Q),J(P,h),J(Q,h)\bigr)=1.
   \tag{1}
   \]

### Theorem

Then \(F\) is a polynomial automorphism.

Consequently, after the primitive quotient-pencil theorem is included, a
rank-one-leading quartic counterexample with a fixed-component-free
projected cubic pencil must lie in the explicit common-ramification locus
where the gcd in (1) is nonconstant.

## 2. A nonprimitive cubic pencil is binary

Put \(u=P/Q\), and let \(\mathbb C(v)\) be the relative algebraic closure
of \(\mathbb C(u)\) in \(\mathbb C(\mathbb P^2)\).  The generalized
Lüroth theorem (equivalently, rationality of a curve dominated by
\(\mathbb P^2\)) gives
\[
u=\phi(v),\qquad \deg\phi=r>1.
\tag{2}
\]
Write
\[
v=A/B
\]
with coprime homogeneous forms \(A,B\) of the same degree \(e\), and write
\(\phi=[\phi_0:\phi_1]\) with coprime binary forms of degree \(r\).
Because both pairs
\[
(P,Q),\qquad
(\phi_0(A,B),\phi_1(A,B))
\]
are coprime presentations of the same rational function, they differ by a
nonzero scalar.  Hence
\[
re=3.
\tag{3}
\]
Since \(r>1\), (3) forces
\[
r=3,\qquad e=1.
\tag{4}
\]
Thus \(A,B\) are independent linear forms and
\[
P,Q\in\mathbb C[A,B]_3.
\tag{5}
\]

The degree-seven Keller identity is
\[
\operatorname{Jac}(P,Q,h)=0.
\tag{6}
\]
Choose source coordinates \(x=A,y=B,z\).  Since \(P/Q\) is nonconstant,
\(J_{x,y}(P,Q)\ne0\), and (6) becomes
\[
J_{x,y}(P,Q)h_z=0.
\]
Therefore
\[
h\in\mathbb C[x,y]_4.
\tag{7}
\]

Choose target coordinates with
\[
H_4=(0,0,h),\qquad
H_3=(P,Q,R),\qquad
H_2=(S,T,U).
\tag{8}
\]
The linear part remains arbitrary and invertible.

## 3. The degree-six Hilbert--Burch obstruction

Set
\[
a=J_{x,y}(Q,h),\qquad
b=J_{x,y}(P,h),\qquad
c=J_{x,y}(P,Q).
\tag{9}
\]
Their degrees are \(5,5,4\).  The degree-six determinant coefficient is
exactly
\[
aS_z-bT_z+cR_z=0.
\tag{10}
\]
Here the coefficient degrees are \(1,1,2\), so (10) is a homogeneous
syzygy of total degree six.

Under (1), the ideal \((a,b,c)\subset\mathbb C[x,y]\) has height two.  Its
Hilbert--Burch matrix is
\[
\begin{pmatrix}
P_x&P_y\\
Q_x&Q_y\\
h_x&h_y
\end{pmatrix}.
\tag{11}
\]
The two columns are independent because their first two maximal minor is
\(c\ne0\).  Both column syzygies have total degree seven, and the sum of
the two Hilbert--Burch shifts is
\[
5+5+4=14.
\]
Thus they are a minimal basis and there is no nonzero syzygy of total
degree six.  The resolution remains exact after the flat extension
\(\mathbb C[x,y]\subset\mathbb C[x,y,z]\), so this conclusion also applies
to the \(z\)-dependent coefficients in (10).  Equation (10) forces
\[
S_z=T_z=R_z=0.
\tag{12}
\]

## 4. Degree five and the plane exit

Write
\[
L_0(\partial_z)=(v_1,v_2,v_3)^T.
\]
After (12), the homogeneous degree-five determinant coefficient is
\[
a v_1-b v_2+cU_z=0.
\tag{13}
\]
The first two terms are the surviving
\(6\Delta(L_0,JH_3,JH_4)\) contribution; they cannot be discarded while
the independently chosen source and target normalizations leave \(L_0\)
arbitrary.

Equation (13) is a syzygy of total degree five for the same triple
\((a,-b,c)\).  The Hilbert--Burch basis starts in total degree seven, even
after adjoining \(z\), so
\[
v_1=v_2=U_z=0.
\tag{14}
\]
Equations (5), (7), (8), (12), and (14) say that every nonlinear term of
\(F\) depends only on \(x,y\).

Moreover \(v_3\ne0\), because \(L_0\) is invertible.  The map already has
the block form
\[
\bigl(G_1(x,y),G_2(x,y),\alpha z+\psi(x,y)\bigr),
\qquad \alpha\ne0,
\tag{15}
\]
where \(G:\mathbb A^2\to\mathbb A^2\) is Keller of degree at most four.
The unconditional plane low-degree theorem makes \(G\) an automorphism;
the last component is a shear.  Hence \(F\) is an automorphism.

## 5. Verification boundary and disclosure

The accompanying exact scripts verify the signs and completeness of the
degree-six and degree-five coefficients with an arbitrary linear part.
They do not verify the generalized Lüroth theorem, the coprime-presentation
degree calculation, or exactness of the Hilbert--Burch resolution.

The adversarial audit independently reconstructed those three
noncomputational steps.  It also caught that an earlier draft discarded
the mixed \(6\Delta(L_0,JH_3,JH_4)\) term in degree five.  The corrected
term is the lower-total-degree syzygy (13), which strengthens rather than
weakens the exit by forcing the first two entries of
\(L_0(\partial_z)\) to vanish.

This proof was developed with AI assistance.  Exact computer algebra is
evidence about the encoded identities, not peer review.  This theorem has
not been peer reviewed.
