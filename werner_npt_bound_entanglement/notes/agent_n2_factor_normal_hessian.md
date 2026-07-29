# Exact factor-normal Hessian and a global qualitative second-kernel modulus

## Status

Let
\[
 \langle W,H_{\cal U}W\rangle=Q_2(UW^\dagger),
 \qquad U^\dagger U=I_2,
 \tag{1}
\]
for a two-plane
\({\cal U}\subset\mathbb C^3\otimes\mathbb C^3\).  This note proves
that the second fixed-left eigenvalue has a uniformly positive
quadratic normal Hessian along the complete factor-plane manifold.
More precisely, if a unit-speed Grassmann geodesic leaves a factor
plane orthogonally, then
\[
 \boxed{\qquad
 \lambda_2(H_{{\cal U}(t)})
 \geq \frac14t^2+o(t^2).
 \qquad}
 \tag{2}
\]
The coefficient \(1/4\) is uniform over both factor rulings.

Tracking the Taylor remainder gives the explicit local estimate
\[
 \boxed{\qquad
 d_{\rm Gr}({\cal U},{\sf Fac})\leq\frac1{4096}
 \quad\Longrightarrow\quad
 \lambda_2(H_{\cal U})
 \geq\frac1{10}d_{\rm Gr}({\cal U},{\sf Fac})^2
 \geq\frac1{20}\operatorname{dist}_2({\cal U},{\sf Fac})^2 .
 \qquad}
 \tag{3}
\]
Here \(d_{\rm Gr}\) is Grassmann geodesic distance and
\(\operatorname{dist}_2\) is Frobenius distance between projections.

Together with the exact fixed-left nullity classification, (3)
has an important compactness consequence:
\[
 \boxed{\qquad
 \text{there exists a universal }c_*>0\text{ such that }\quad
 \lambda_2(H_{\cal U})
 \geq c_*\operatorname{dist}_2({\cal U},{\sf Fac})^2
 \quad\text{for every }{\cal U}.
 \qquad}
 \tag{4}
\]
Consequently the desired global quartic modulus also exists, with
constant \(c_*/4\).  The compactness constant in (4) is not made
effective here.  Thus this closes the qualitative global modulus
but does not yet prove the proposed explicit constant \(1/1280\).

## 1. Canonical normal coordinates

Local unitaries reduce either factor ruling to
\[
 {\cal F}
 =
 \operatorname{span}\{E_{11},E_{12}\},
 \qquad
 U_0=(E_{11},E_{12}).
 \tag{5}
\]
Its fixed-left kernel has the orthonormal basis
\[
 k_p=\frac1{\sqrt2}
 \bigl(E_{p1},E_{p2}\bigr),
 \qquad p=1,2,3,
 \tag{6}
\]
and the spectrum of \(H_0:=H_{\cal F}\) is
\[
 0^{(3)},\qquad (1/2)^{(5)},\qquad 1^{(10)}.
 \tag{7}
\]

The horizontal tangent space to the Grassmannian at \({\cal F}\)
is
\[
 \operatorname{Hom}\bigl(
 e_1\otimes\operatorname{span}\{f_1,f_2\},
 {\cal F}^{\perp}\bigr).
 \tag{8}
\]
The tangent space to the factor ruling consists of:

1. arbitrary motion from
   \(e_1\otimes\operatorname{span}\{f_1,f_2\}\) into
   \(e_1\otimes f_3\);
2. for each \(p=2,3\), a scalar multiple of the identity map from
   the code plane into
   \(e_p\otimes\operatorname{span}\{f_1,f_2\}\).

An orthogonal normal vector is consequently specified by
\[
 A,D\in M_2^0,\qquad b,c\in\mathbb C^{1\times2},
 \tag{9}
\]
where \(A,b\) are the components with first local output \(e_2\),
and \(D,c\) those with output \(e_3\).  Write
\[
 A=
 \begin{pmatrix}x&y\\z&-x\end{pmatrix},
 \qquad
 D=
 \begin{pmatrix}r&s\\t&-r\end{pmatrix},
 \tag{10}
\]
and identify
\[
 a=(\sqrt2x,y,z),\qquad d=(\sqrt2r,s,t).
 \tag{11}
\]
Put
\[
\begin{aligned}
 A_0&=\|a\|^2=\|A\|_2^2,&
 D_0&=\|d\|^2=\|D\|_2^2,\\
 B_0&=\|b\|^2,&
 C_0&=\|c\|^2,\\
 N&=A_0+D_0+B_0+C_0=\|V\|_2^2.
\end{aligned}
\tag{12}
\]

## 2. The exact Schur Hessian

Let \(P_0\) project onto the kernel (6), \(Q_0=I-P_0\), and let
\[
 U(t)=U_0+tV-\frac{t^2}{2}U_0V^\dagger V+O(t^3)
 \tag{13}
\]
be the horizontal Grassmann geodesic.  Expand
\[
 H(t)=H_0+tH_1+t^2H_2+O(t^3).
 \tag{14}
\]
Because \(H(t)\succeq0\) for positive and negative \(t\),
\[
 P_0H_1P_0=0.
 \tag{15}
\]
The effective quadratic form on the three-dimensional zero cluster is
the Schur Hessian
\[
 {\cal M}(V)
 =
 P_0H_2P_0
 -
 P_0H_1Q_0
 (Q_0H_0Q_0)^{-1}
 Q_0H_1P_0.
 \tag{16}
\]

### Theorem 1 (exact normal Hessian)

In the kernel basis (6),
\[
 \boxed{
 {\cal M}(V)=
 \begin{pmatrix}
 \frac{A_0+D_0}{2}+\frac{3(B_0+C_0)}8&0&0\\[1mm]
 0&\frac{D_0}{2}+\frac{B_0}{4}+\frac{C_0}{2}
   &-\frac12\langle a,d\rangle-\frac14\langle b,c\rangle\\[1mm]
 0&-\frac12\langle d,a\rangle-\frac14\langle c,b\rangle
   &\frac{A_0}{2}+\frac{B_0}{2}+\frac{C_0}{4}
 \end{pmatrix}.
 }
 \tag{17}
\]
It obeys
\[
 \boxed{\qquad
 \operatorname{Tr}{\cal M}
 =N+\frac{B_0+C_0}{8}\geq N,
 \qquad
 0\preceq{\cal M}\preceq\frac N2I_3.
 \qquad}
 \tag{18}
\]
Consequently
\[
 \boxed{\qquad
 \lambda_2({\cal M}(V))\geq\frac N4.
 \qquad}
 \tag{19}
\]

### Proof

The coefficient-matrix identity
\[
 Q_2(C)
 =
 \|C\|_2^2
 -\frac12\left(
 \|\operatorname{Tr}_1C\|_2^2+
 \|\operatorname{Tr}_2C\|_2^2\right)
 +\frac14|\operatorname{Tr}C|^2
 \tag{20}
\]
is sesquilinearized and substituted into (16).  The five positive
eigenvalues \(1/2\) and the ten eigenvalues \(1\) in (7) make the
inverse in (16) elementary.  Collecting the coefficients of the
two traceless blocks and the two transverse rows gives (17).
This is a direct contraction; the independent exact checker
`verification/verify_n2_factor_normal_hessian.py` audits it by
coefficient polarization.

The trace identity in (18) follows immediately from (17).  The
upper-left scalar entry is at most \(N/2\).  Subtracting the lower
\(2\times2\) block from \(NI_2/2\) gives
\[
 \begin{pmatrix}
 A_0/2+B_0/4&
 \frac12\langle a,d\rangle+\frac14\langle b,c\rangle\\
 \frac12\langle d,a\rangle+\frac14\langle c,b\rangle&
 D_0/2+C_0/4
 \end{pmatrix}.
 \tag{21}
\]
Its off-diagonal entry has modulus at most
\[
 \frac12\sqrt{A_0D_0}+\frac14\sqrt{B_0C_0}
 \leq
 \sqrt{
   (A_0/2+B_0/4)(D_0/2+C_0/4)},
 \tag{22}
\]
where the second inequality is Cauchy--Schwarz in \(\mathbb R^2\).
Thus (21) is positive semidefinite and
\({\cal M}\preceq NI/2\).

Write the eigenvalues of \({\cal M}\) increasingly as
\(\mu_1\leq\mu_2\leq\mu_3\).  Equations (18) give
\[
 \mu_2
 \geq\frac{\mu_1+\mu_2}{2}
 =\frac{\operatorname{Tr}{\cal M}-\mu_3}{2}
 \geq\frac{N-N/2}{2}
 =\frac N4.
 \tag{23}
\]
This proves (19).  Positivity of \({\cal M}\) also follows from
the positive family \(H(t)\), or directly from (17)--(22).
\(\square\)

For a unit-speed normal geodesic \(N=1\).  Standard finite-dimensional
degenerate perturbation, or the explicit Schur estimate in the next
section, gives
\[
 \lambda_j(H(t))
 =t^2\lambda_j({\cal M})+O(t^3),
 \qquad j=1,2,3.
 \tag{24}
\]
Equations (19) and (24) prove (2).

## 3. An effective tubular estimate

We include constants to make the local assertion independently
checkable.  Let \(U(s)\), \(0\leq s\leq t\), be a unit-speed normal
Grassmann geodesic.  Write
\[
 H(s)=J(s)^\dagger({\cal L}^{\otimes2})J(s),
 \qquad J(s)W=U(s)W^\dagger.
 \tag{25}
\]
Since \(\|{\cal L}^{\otimes2}\|_{\rm op}=1\), and every derivative
of a unit-speed Grassmann geodesic frame through order three has
operator norm at most one,
\[
 \|H'(s)\|\leq2,\qquad
 \|H''(s)\|\leq4,\qquad
 \|H'''(s)\|\leq8.
 \tag{26}
\]
Taylor's formula therefore gives
\[
 H(t)=H_0+tH_1+t^2H_2+R_3,
\quad
 \|H_1\|\leq2,\quad
 \|H_2\|\leq2,\quad
 \|R_3\|\leq\frac43t^3.
 \tag{27}
\]

Use the \(P_0\oplus Q_0\) block decomposition.  The lower-right block
\(D(t)\) obeys
\[
 D(t)\succeq(1/2-3t)I.
 \tag{28}
\]
For \(t\leq1/4096\), it is invertible and
\(\|D(t)^{-1}\|\leq4\).  Its Schur complement \(\Sigma(t)\) satisfies
\[
 \left\|\Sigma(t)-t^2{\cal M}(V)\right\|
 \leq146t^3.
 \tag{29}
\]
For completeness, the four contributions are bounded by
\[
 \frac43t^3,\qquad
 96t^3,\qquad
 48t^3,\qquad
 36t^4,
 \tag{30}
\]
respectively: the Taylor remainder in the upper-left block, the
inverse perturbation in the quadratic Schur term, the two cross
terms, and the square of the higher-order off-diagonal block.
Their sum is less than \(146t^3\).

Theorem 1 and (29) give
\[
 \lambda_2(\Sigma(t))
 \geq\left(\frac14-\frac{146}{4096}\right)t^2
 >\frac15t^2.
 \tag{31}
\]
Completing the block square is a triangular congruence whose inverse
has norm at most
\[
 1+\|D(t)^{-1}Q_0H(t)P_0\|
 \leq1+12t.
 \tag{32}
\]
The second eigenvalue of the block diagonal matrix
\(\Sigma(t)\oplus D(t)\) is \(\lambda_2(\Sigma(t))\), because
\(D(t)\succeq I/4\).  Congruence and (31)--(32) therefore give
\[
 \lambda_2(H(t))
 \geq\frac{t^2/5}{(1+12t)^2}
 \geq\frac1{10}t^2.
 \tag{33}
\]

A shortest Grassmann geodesic from a sufficiently close plane to the
factor manifold meets that manifold orthogonally by the first
variation formula.  Its principal angles \(\theta_1,\theta_2\) obey
\[
 t^2=\theta_1^2+\theta_2^2,\qquad
 \|P_{\cal U}-P_{\cal F}\|_2^2
 =2(\sin^2\theta_1+\sin^2\theta_2)
 \leq2t^2.
 \tag{34}
\]
Equations (33)--(34) prove (3).  The other factor ruling is identical
after swapping the two qutrits.

## 4. Compactness corollary

The two factor rulings are disjoint compact smooth submanifolds of
the compact Grassmannian \(\operatorname{Gr}(2,9)\).  The exact
fixed-left nullity classification says
\[
 \lambda_2(H_{\cal U})=0
 \quad\Longleftrightarrow\quad
 {\cal U}\in{\sf Fac}.
 \tag{35}
\]
Outside the geodesic \(1/4096\)-tube, both
\(\lambda_2(H_{\cal U})\) and
\(\operatorname{dist}_2({\cal U},{\sf Fac})\) are continuous, and
the latter is positive.  Hence
\[
 c_{\rm far}
 :=
 \min_{\,
 d_{\rm Gr}({\cal U},{\sf Fac})\geq1/4096}
 \frac{\lambda_2(H_{\cal U})}
      {\operatorname{dist}_2({\cal U},{\sf Fac})^2}
 >0.
 \tag{36}
\]
Taking
\[
 c_*=\min\{1/20,c_{\rm far}\}
 \tag{37}
\]
proves (4).  Finally, two rank-two projections have Frobenius
distance squared at most four, so
\[
 \operatorname{dist}_2^2
 \geq\frac14\operatorname{dist}_2^4.
 \tag{38}
\]
Thus (4) also gives a global quartic modulus \(c_*/4>0\).

The only non-effective element is the far-region minimum (36).
Obtaining a simple explicit lower bound for it remains the exact
finite-dimensional frontier.

