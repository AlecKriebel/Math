# Abstract binary-quartic Hilbert--Burch and \(E_6\) lemma

**Status:** proved algebraically and checked by the exact block verifier.
This is an abstract lemma, not a classification of either application.

Let \(P,Q\in\mathbb C[p,q]_4\) satisfy \(J(P,Q)\ne0\), let
\[
H_4=(P,Q,0),\qquad H_3=(U,V,R),\qquad H_2=(A,B,T),
\]
where \(U,V,R\) are homogeneous cubics and \(A,B,T\) are homogeneous
quadratics.  For an invertible linear part \(L_0\), all weighted
identities below are the coefficients of
\[
\det\!\left(L_0+zJH_2+z^2JH_3+z^3JH_4\right).
\]
Suppose \(R\in\mathbb C[p,q]_3\), and put
\[
\alpha=J(Q,R),\qquad\beta=-J(P,R),\qquad
\gamma=J(P,Q).
\]
No coprimality assumption on \(P,Q\) is made.

There is one boundary that must be removed before the Hilbert--Burch
analysis: if \(R=0\), then the third component has degree at most two.
The quadratic-component coordinate lemma and the plane low-degree exit
then make the Keller map an automorphism.  Thus the remainder of the
Hilbert--Burch and power-fibre discussion assumes \(R\ne0\).

## Top identities

For the standard weighted determinant,
\[
E_8=\gamma R_r.
\]
Thus a Keller map makes \(R\) binary.  The next identity is
\[
\boxed{E_7=\alpha U_r+\beta V_r+\gamma T_r.}
\]

Let \(g=\gcd(\alpha,\beta,\gamma)\), \(\delta=\deg g\), and assume
\(\alpha,\beta\) are constant-linearly independent.  After division by
\(g\), the generator degrees are
\[
(d,d,d+1),\qquad d=5-\delta.
\]
Here \(d\ge1\): if \(\delta=5\), the two reduced degree-zero forms
\(\alpha_0,\beta_0\) would be constant-linearly dependent.  The reduced
ideal
\[
I=(\alpha_0,\beta_0,\gamma_0)\subset\mathbb C[p,q]
\]
is therefore proper, and gcd one excludes every height-one prime over
\(I\).  Hence \(\operatorname{ht}I=2\), which is the precise
Hilbert--Burch hypothesis.
If \(e_1,e_2\) are the two minimal total syzygy degrees, Hilbert--Burch
gives \(e_1+e_2=3d+1\).  The two gradient columns
\[
(P_p,Q_p,R_p)^T,\qquad(P_q,Q_q,R_q)^T
\]
are independent syzygies of total degree \(d+3\).  Constant independence
of \(\alpha,\beta\) rules out total degree at most \(d\).  Hence
\[
k_i=d+3-e_i\in\{0,1,2\}.
\]
To obtain the sum, let \(N_1,N_2\) be a minimal Hilbert--Burch basis and
write the two gradient columns as
\[
(\nabla_p,\nabla_q)=(N_1,N_2)C.
\]
Their wedge is
\[
\nabla_p\wedge\nabla_q=(\alpha,\beta,\gamma)
   =g(\alpha_0,\beta_0,\gamma_0),
\]
whereas \(N_1\wedge N_2\) is a nonzero scalar multiple of the reduced
row \((\alpha_0,\beta_0,\gamma_0)\).  Consequently
\(\det C\) is a nonzero scalar multiple of \(g\).  Row \(i\) of \(C\)
has degree \(k_i\), so
\[
k_1+k_2=\deg\det C=\deg g=\delta.
\]
In particular \(\delta\le4\), and the \(E_7\) block nullities are
\[
\begin{array}{c|c|c}
\delta&\{k_1,k_2\}&(r^2,r^1,r^0)\text{ nullities}\\ \hline
0&\{0,0\}&(0,0,0)\\
1&\{1,0\}&(0,0,1)\\
2&\{1,1\}&(0,0,2)\\
2&\{2,0\}&(0,1,2)\\
3&\{2,1\}&(0,1,3)\\
4&\{2,2\}&(0,2,4).
\end{array}
\]

If \(R\ne0\) and \(\alpha,\beta\) are constant-linearly dependent, then
\[
\lambda P+\mu Q=L^4,\qquad R=L^3
\]
for some linear \(L\).  This is the abstract power-fibre exception.  Its
further normalization depends on the application.

For clarity, the scalar normalization is part of the argument.  With
\(S=\lambda P+\mu Q\ne0\), Euler's identities and \(J(S,R)=0\) give
\[
3RS_p-4SR_p=0,\qquad3RS_q-4SR_q=0,
\]
so \(S^3/R^4\in\mathbb C^\times\).  Unique factorization and
\(\gcd(3,4)=1\) give \(S=a\ell^4,R=b\ell^3\) with \(a,b\ne0\).
Replacing \(\ell\) by \(b^{1/3}\ell\) and rescaling
\((\lambda,\mu)\) produces the displayed normalization
\(R=L^3,S=L^4\).

## Signed \(E_6\)

Let \(D\) be the binary Jacobian matrix of \((P,Q)\), \(C\) that of
\((U,V)\), and set
\[
u=(U_r,V_r)^T,\quad v=(A_r,B_r)^T,\quad
w=\nabla R,\quad t=\nabla T,\quad\tau=T_r.
\]
Then
\[
\boxed{
E_6=(\det D)(L_0)_{33}
+\operatorname{tr}(\operatorname{adj}C\,D)\tau
-w\operatorname{adj}D\,v
-t\operatorname{adj}D\,u
-w\operatorname{adj}C\,u.}
\]
Equivalently,
\[
E_6=\alpha A_r+\beta B_r+\gamma(L_0)_{33}
+\det(dP,dV,dT)+\det(dU,dQ,dT)+\det(dU,dV,dR).
\]

On the \(\delta=0\) stratum, \(E_7\) makes \(U,V,T\) binary.  The curvature
terms vanish, and the remaining \(E_6\) equation is the same injective
syzygy problem in degrees \((1,1,0)\) and \((0,0,-1)\).  Hence \(A,B\) are
binary as well.  For a degree-four Keller map, all nonlinear terms are then
binary, so the established plane degree bound and triangular shear give a
polynomial automorphism.

## Application boundary

The following facts are **not** abstract:

- the four stabilizer orbits for
  \(P=hp^2,Q=hq^2\);
- the determinant factorization in equation (11) of
  `WORKING_BINARY_LOCUS.md`;
- the assertion that the power fibre is uniquely
  \(h=p^2,R=p^3\) in that row; and
- every lower contact factor obtained after inserting the squaring-cover
  normal forms.

The abstract lemma applies unchanged to the binary fixed-linear
triple-cover row \(P=pA_3,Q=pB_3\); its orbit and lower-factor analysis
remain separate.

An independent hostile reconstruction, including the full height-two
argument, scalar normalization, weighted-degree bookkeeping, and
fail-closed mutations, is recorded in
`audit_abstract_hb_e6_hostile/REPORT.md`.
