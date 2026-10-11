# Local tangent-line models of symplectic surfaces

## Identification and scope

Problem 6000010 / AMR-059-0010 is the local tangent-bundle characterization proposed by Takashi Kurose in item 3(d), printed p. 126, of H. Furuhata, H. Matsuzoe and H. Urakawa, *Open Problems in Affine Differential Geometry and Related Topics*, Interdisciplinary Information Sciences 4 (1998), 125-127. [Original source](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en).

The following is a self-contained, bounded result in **real dimension two** (one-dimensional base), under the explicit canonical symplectic/statistical Codazzi interpretation specified below. The original item uses the word compatible without defining it there. This result does not settle the unrestricted-dimensional question or other unspecified interpretations and makes no novelty claim. The original asks about both the symplectic form and almost complex structure. A metric-only local isometry must therefore also have the correct orientation.

## 1. Conventions and statistical compatibility

Let \(h\) be a positive-definite metric and \(\nabla\) a torsion-free affine connection on a manifold \(M\). Statistical, or Codazzi, compatibility means
\[
 (\nabla_Xh)(Y,Z)=(\nabla_Yh)(X,Z).
\]
Since \(h\) is symmetric, this is equivalent to total symmetry of the cubic tensor \(\nabla h\). It does **not** mean \(\nabla h=0\). The latter, together with torsion-freeness, forces the Levi-Civita connection.

The natural tangent-bundle construction uses the connection splitting into horizontal and vertical subspaces and
\[
 JX^H=X^V,\qquad JX^V=-X^H.
\]
The symplectic form is \(\Omega=(h^\flat)^*(-d\lambda)\), where \(\lambda=p_i\,dx^i\) is the cotangent tautological form and \(h^\flat(v)=h(v,\cdot)\). Our induced metric convention is \(G(U,V)=\Omega(U,JV)\).

For a direct compatibility check, write \(H_i=\partial_{x^i}-\Gamma^k_{ij}y^j\partial_{y^k}\), \(V_i=\partial_{y^i}\), and \(\delta y^i=dy^i+\Gamma^i_{jk}y^kdx^j\). The natural positive metric is
\[
 G_0=h_{ij}\,dx^i dx^j+h_{ij}\,\delta y^i\delta y^j.
\]
Its fundamental form is \(\Omega_0=h_{ij}\,dx^i\wedge\delta y^j\). On coordinate pairs the only possible difference between \(\Omega\) and \(\Omega_0\) is the horizontal-horizontal block:
\[
 \begin{split}
 \Omega(\partial_{x^i},\partial_{x^j})
 &= (\partial_jh_{ik}-\partial_ih_{jk})y^k,\\
 \Omega_0(\partial_{x^i},\partial_{x^j})
 &= (h_{i\ell}\Gamma^\ell_{jk}-h_{j\ell}\Gamma^\ell_{ik})y^k.
 \end{split}
\]
Equality is exactly the displayed Codazzi condition when \(\Gamma^k_{ij}=\Gamma^k_{ji}\). Also, \(\Omega\) is \(J\)-invariant only if its horizontal-horizontal block in the \((H,V)\) frame vanishes, since its vertical-vertical block is zero and \(JH=V\). Thus, under this explicit canonical-form and positive J-compatibility interpretation, the relevant condition is statistical Codazzi compatibility. The original item does not itself supply this tensor definition; Levi-Civita compatibility would be an additional restriction.

As a primary-source cross-check, H. Satoh, *Almost Hermitian structures on tangent bundles*, [arXiv:1908.10824v2](https://arxiv.org/pdf/1908.10824v2), Definition 2.1 and (2.3), p. 4, and Theorem 3.1, p. 8, give the same lift convention, dual-torsion/Codazzi relation, and canonical-form criterion. The paper is a revised version of the 2007 proceedings article; this audit uses the explicitly pinned 21 March 2025 version. The calculations here are reproduced independently.

On a one-manifold with coordinate \(x\), set
\[
 h=a(x)\,dx^2,\quad a>0,\qquad
 \nabla_{\partial_x}\partial_x=\Gamma(x)\partial_x.
\]
Every smooth \(\Gamma\) is torsion-free and statistically compatible: \(\nabla h=(a'-2a\Gamma)\,dx^{\otimes3}\) is automatically symmetric. Its curvature also vanishes by dimension. The dual coefficient is \(\Gamma^*=a'/a-\Gamma\); no constraint on \(\Gamma\) is introduced.

## 2. Precise theorem

Let \(N\) be a smooth real surface, \(\omega\) a symplectic form, and \(J\) an \(\omega\)-compatible almost complex structure; compatibility includes positive definiteness of
\[
 g(X,Y)=\omega(X,JY).
\]
Fix \(p\in N\). The following are equivalent:

1. There are a neighborhood \(U\) of \(p\), an interval \(I\) with positive metric \(h\) and statistically compatible torsion-free affine connection \(\nabla\), an open subset \(W\subset TI\), and a diffeomorphism \(F:U\to W\) satisfying \(F^*\Omega=\omega\) and \(dF\circ J=J_\nabla\circ dF\).
2. There is a smooth Killing field \(X\) on a neighborhood of \(p\) such that \(X(p)\ne0\).

Condition 2 is equivalent, after shrinking the neighborhood, to the existence of an everywhere nonvanishing local Killing field. No preselected bundle projection, zero section, completeness, or global topology is part of the assertion.

## 3. Forward implication, including nondegeneracy

In tangent coordinates \((x,y)\), put
\[
 H=\partial_x-\Gamma y\partial_y,\qquad V=\partial_y.
\]
Then \(JH=V\), \(JV=-H\), and
\[
 \Omega=-d(ay\,dx)=a\,dx\wedge dy,
 \qquad
 G=a\{dx^2+(dy+\Gamma y\,dx)^2\}.
\]
The coframe \((dx,dy+\Gamma ydx)\) is everywhere independent. Consequently \(G\) is positive definite; in coordinate form
\[
 [G]=a\begin{pmatrix}1+\Gamma^2y^2&\Gamma y\\\Gamma y&1\end{pmatrix},
 \qquad \det G=a^2>0.
\]
The matrix
\[
 [J]=\begin{pmatrix}-\Gamma y&-1\\1+\Gamma^2y^2&\Gamma y\end{pmatrix}
\]
satisfies \(J^2=-\mathrm{Id}\), and \([\Omega][J]=[G]\).

Choose \(f>0\) solving \(f'=\Gamma f\), for example \(f(x)=\exp(\int_{x_0}^x\Gamma(t)dt)\), and set \(z=f(x)y\). This is a local diffeomorphism with positive Jacobian \(f\). Since
\[
 dy+\Gamma ydx=f^{-1}dz,
\]
one obtains
\[
 G=a(x)dx^2+a(x)f(x)^{-2}dz^2.
\]
Thus \(\partial_z=f^{-1}\partial_y\) is Killing and nowhere zero. This argument works at every point of every open tangent-bundle patch, including nonzero vectors, and needs only a local flow. Pulling it back by \(F\) proves condition 2.

## 4. Converse, including all mixed terms

Assume \(X(p)\ne0\). The flow-box theorem gives coordinates \((x,t)\) with \(X=\partial_t\). The equation \(\mathcal L_Xg=0\) says each metric coefficient is independent of \(t\), so
\[
 g=A(x)dx^2+2C(x)dxdt+B(x)dt^2,
 \qquad B>0,\quad AB-C^2>0.
\]
Choose the transverse coordinate sign so \(dx\wedge dt\) has the orientation of \(\omega\). Set
\[
 z=t+\psi(x),\qquad \psi'(x)=C(x)/B(x).
\]
This has Jacobian 1 and preserves \(X=\partial_z\). Substitution \(dt=dz-(C/B)dx\) gives
\[
 \begin{split}
 g={}&[A-2C(C/B)+B(C/B)^2]dx^2\\
 &+2[C-B(C/B)]dxdz+Bdz^2\\
 ={}&a(x)dx^2+b(x)dz^2,
 \end{split}
\]
where \(a=A-C^2/B=(AB-C^2)/B>0\) and \(b=B>0\).

For a compatible pair in real dimension two, \(\omega\) is exactly the positively oriented area form of \(g\). Hence
\[
 \omega=\sqrt{ab}\,dx\wedge dz.
\]
Let \(q=\sqrt{b/a}>0\), define \(y=q(x)z\), and equip the interval in the \(x\) variable with
\[
 h=a(x)dx^2,\qquad \Gamma=-q'/q.
\]
The map \(F(x,z)=(x,y)\) has determinant \(q>0\), so its image is open and it is a diffeomorphism after restriction. Explicitly,
\[
 dy=q\,dz+q'z\,dx,
 \qquad
 \Gamma ydx=-q'z\,dx,
 \qquad
 dy+\Gamma ydx=q\,dz.
\]
It follows that
\[
 F^*G=a dx^2+aq^2dz^2=g,
 \qquad
 F^*\Omega=aq\,dx\wedge dz=\sqrt{ab}\,dx\wedge dz=\omega.
\]
All terms involving \(q'z\) cancel, including the mixed and quadratic terms. The base connection is allowed by Section 1. Finally \(J\) is uniquely determined by \(g\) and \(\omega\): \(\omega(U,JV)=g(U,V)\) and nondegeneracy of \(\omega\) determine \(JV\) for each \(V\). Therefore the displayed pullback identities also intertwine \(J\). This proves condition 1.

A constant translation of \(z\) can arrange \(z(p)=0\), if desired. Thus a model may be chosen taking the distinguished point into the zero section, but no such choice is needed for the theorem.

## 5. Locality at zeros and a curvature obstruction

A Killing flow consists of local isometries, so it preserves Gaussian curvature \(K\) and \(S=|\operatorname{grad}K|_g^2\). Thus \(XK=XS=0\). On a surface, the annihilator of a nonzero tangent vector is one-dimensional; therefore
\[
 dK\wedge dS=0
\]
wherever \(X\ne0\). A point at which this two-form is nonzero cannot have a model neighborhood. This is a necessary test, not a sufficient criterion.

For a concrete obstruction, on the plane take
\[
 \phi(u,v)=u^2+v^3,\quad
 g=e^{2\phi}(du^2+dv^2),\quad
 \omega=e^{2\phi}du\wedge dv,\quad
 J\partial_u=\partial_v.
\]
The conformal-curvature formula, or direct Christoffel calculation, gives \(K=-(2+6v)e^{-2\phi}\). At \((1,0)\),
\[
 (K_u,K_v)=(8,-6)e^{-2},\qquad
 (S_u,S_v)=(-1072,384)e^{-6}.
\]
Hence \((dK\wedge dS)_{(1,0)}=-3360e^{-8}du\wedge dv\ne0\), and no local model exists there.

The requirement \(X(p)\ne0\) cannot be weakened to existence of a nontrivial Killing field near \(p\). On the plane let
\[
 g=e^{2(u^2+v^2)}(du^2+dv^2).
\]
The rotation field \(R=-v\partial_u+u\partial_v\) is Killing but vanishes at the origin. Here \(K=-4e^{-2(u^2+v^2)}\), \(dK(0)=0\), and \(\operatorname{Hess}K(0)=16\mathrm{Id}\) in these coordinates. For **any** Killing field \(X\), differentiating \(XK=0\) at 0 gives \(\operatorname{Hess}K(0)(X(0),\cdot)=0\); thus \(X(0)=0\). The origin has no model neighborhood, although every nearby non-origin point does. Both \(K\) and \(S\) are radial, so \(dK\wedge dS=0\) throughout this example. It simultaneously proves that the scalar obstruction is not sufficient.

## 6. Levi-Civita and constant-curvature checks

If the base connection is constrained to be Levi-Civita, \(\Gamma=a'/(2a)\). With \(v=\sqrt a\,y\) and \(s=\int\sqrt a\,dx\), the model becomes
\[
 G=ds^2+dv^2,\qquad\Omega=ds\wedge dv.
\]
So the Levi-Civita-only subclass is exactly the locally flat oriented surface subclass. It is much smaller than the theorem's statistical class.

For example, \(h=dx^2\) and \(\Gamma=-1\) give
\[
 G=dx^2+(dy-y\,dx)^2=dx^2+e^{2x}dz^2,
 \quad z=e^{-x}y,
\]
which has \(K=-1\). The connection has \(\nabla h=2dx^{\otimes3}\ne0\), but is statistically compatible. This rules out a hidden Levi-Civita restriction.

More generally, \(G=ds^2+F(s)^2dt^2\), with \(F>0\), has \(K=-F''/F\) and is realized by \(h=ds^2\), \(y=F(s)t\), \(\Gamma=-F'/F\). Thus
\[
 F(s)=\cos(\sqrt\kappa\,s)\ (\kappa>0),\quad
 F(s)=1\ (\kappa=0),\quad
 F(s)=\cosh(\sqrt{-\kappa}\,s)\ (\kappa<0)
\]
produce all constant signs, on intervals where \(F>0\).

Every smooth surface of constant curvature \(\kappa\) is locally represented near **each** point, including points at which a particular rotational Killing field vanishes. One elementary proof takes a unit-speed geodesic through the point and its normal geodesic variation. Gauss's lemma and the Jacobi equation give Fermi-coordinate metric \(ds^2+c_\kappa(s)^2dt^2\), where \(c_\kappa''+\kappa c_\kappa=0\), \(c_\kappa(0)=1\), and \(c_\kappa'(0)=0\). The explicit functions just displayed are positive near \(s=0\), and \(\partial_t\) is nonvanishing there. The opposite orientation, if needed, is accommodated by reversing \(t\).

## 7. Higher-dimensional boundary

With curvature convention \(R(X,Y)Z=\nabla_X\nabla_YZ-\nabla_Y\nabla_XZ-\nabla_{[X,Y]}Z\) and
\[
 N_J(A,B)=[JA,JB]-J[JA,B]-J[A,JB]-[A,B],
\]
the lift-bracket identities give
\[
 N_J(X^H,Y^H)=(T^\nabla(X,Y))^H+(R^\nabla(X,Y)y)^V.
\]
For torsion-free \(\nabla\), this is precisely the curvature term stated in the candidate. Flatness makes \(J\) integrable; statistical compatibility alone does not force flatness in base dimension at least two (a curved Riemannian base with its Levi-Civita connection already supplies an example). In one base dimension curvature vanishes automatically, in agreement with integrability of every smooth almost complex structure on a real surface.

This verifies the candidate's boundary calculation. It supplies no necessary-and-sufficient characterization in higher dimensions, no global tangent-bundle recognition theorem, and no claim about the present literature status of Kurose's full problem.
