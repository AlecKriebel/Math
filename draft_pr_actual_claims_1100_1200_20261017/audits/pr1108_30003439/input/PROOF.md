# A one-sided cubic power cone with a negative-curvature normal barrier

**Problem:** 30003439 / OWR-15219-008.
**Status:** complete constructive solution accepted by the accompanying [mathematical audit](MATHEMATICAL_AUDIT.md).
**Date:** 2026-10-10. No novelty or priority claim is made.

This AI-assisted manuscript and audit are unrefereed. Acceptance does not mean external human peer review, journal acceptance, or formal proof-assistant certification. The cone is pre-existing and credited to Hildebrand below.

## 1. Statement and scope

Consider the cone in the original three-dimensional space

\[
 K=\{(x,y,z)\in\mathbb R^3:x\ge0,\ y\ge0,\ z\ge0,\ xy^2-z^3\ge0\}.
\]

Put \(p(x,y,z)=xy^2-z^3\), and, on \(\operatorname{int}K\), define

\[
 f(x,y,z)=-\log p(x,y,z)-\log z,
 \qquad F=25f.
\]

**Theorem.** The cone \(K\) is closed, pointed, full dimensional, convex, and defined by homogeneous polynomial inequalities. The function \(F\), extended by \(+\infty\) outside \(\operatorname{int}K\), is a normal barrier with parameter \(100\): it is logarithmically homogeneous, self-concordant, and blows up at every finite boundary point. Moreover,

\[
 D^3F(a)[h,u,u]\le0
 \quad(a\in\operatorname{int}K,\ h\in K,\ u\in\mathbb R^3).
\]

Nevertheless, \(K\) is not the hyperbolicity cone of **any** homogeneous polynomial in \(\mathbb R^3\).

Here negative curvature refers to the directional third-derivative matrix, exactly as in Tunçel's question [1] and Nesterov–Tunçel [2]. It is not sectional curvature. The cone's extra facet \(z=0\) and the barrier term \(-\log z\) are essential to this construction. The theorem is about this one-sided cone, not the usual signed power cone.

## 2. Geometry and algebraicity

The four displayed inequalities are homogeneous polynomial inequalities, so \(K\) is closed and conic. It lies in the nonnegative orthant, hence is pointed. The point \((2,1,1)\) satisfies all inequalities strictly, so \(K\) is full dimensional, and

\[
 \operatorname{int}K=\{x>0,\ y>0,\ z>0,\ xy^2>z^3\}.
\]

The function \(m(x,y)=x^{1/3}y^{2/3}\) is concave on the nonnegative orthant. For positive \(x,y\), its Hessian is

\[
 \nabla^2m=-\frac{2}{9}x^{-5/3}y^{-4/3}
 \begin{pmatrix}y^2&-xy\\-xy&x^2\end{pmatrix}\preceq0;
\]

concavity extends to the boundary by continuity. Thus \(K\), the portion \(z\ge0\) of the hypograph \(z\le m(x,y)\), is convex.

## 3. Barrier and self-concordance certificates

In the interior, write

\[
 g=\frac{z^3}{y^2},\qquad \delta=x-g>0.
\]

Then

\[
 f=-\log\delta-2\log y-\log z.
\]

For any direction \(u=(u_x,u_y,u_z)\), set

\[
 b=\frac{u_y}{y},\qquad c=\frac{u_z}{z},\qquad
 w=\frac{u_x-g(3c-2b)}{\delta},\qquad
 v^2=\frac{6g(c-b)^2}{\delta},\qquad Q=2b^2+c^2.
\]

The derivatives of \(g\) along this line are

\[
 Dg[u]=g(3c-2b),\quad D^2g[u,u]=6g(c-b)^2,
 \quad D^3g[u,u,u]=6g(c-b)^2(c-4b).
\]

Differentiation therefore gives the exact identities

\[
 S:=D^2f[u,u]=w^2+v^2+Q,
\]

\[
 D^3f[u,u,u]=-2w^3-3wv^2+(c-4b)v^2-4b^3-2c^3. \tag{SC1}
\]

The Hessian is positive definite: if \(S=0\), then \(b=c=0\), and subsequently \(w=u_x/\delta=0\), so \(u=0\).

Weighted Cauchy–Schwarz gives

\[
 |c-4b|\le3\sqrt Q.
\]

Also

\[
 |4b^3+2c^3|\le2(2|b|^3+|c|^3)\le2Q^{3/2}.
\]

Since \(|w|\le\sqrt S\), \(v^2\le S\), and \(Q\le S\), equation (SC1) yields the deliberately loose but uniform estimate

\[
 |D^3f[u,u,u]|\le(2+3+3+2)S^{3/2}=10S^{3/2}.
\]

Consequently

\[
 |D^3F[u,u,u]|\le250S^{3/2}
 =2(25S)^{3/2}=2(D^2F[u,u])^{3/2}.
\]

This is standard self-concordance. Optimizing the scale factor is unnecessary here.

### 3.1 Direct mixed self-concordance bound

At a fixed base point, write \(b_a,c_a,w_a\) for the preceding linear expressions evaluated in a direction \(a\), and set \(\|a\|_F^2=D^2F[a,a]=25\|a\|_f^2\). Define the signed linear functional \(v_u\) and auxiliary functional \(\ell_u\) by

\[
v_u=\sqrt{6g/\delta}\,(c_u-b_u),\qquad \ell_u=c_u-4b_u,
\qquad \|u\|_f^2=w_u^2+v_u^2+2b_u^2+c_u^2.
\]

Polarizing the exact cubic, or directly contracting the independently derived tensor, gives

\[
\begin{aligned}
D^3f[h,u,u]={}&-2w_h w_u^2
-w_hv_u^2-2w_uv_hv_u\\
&+\tfrac13(\ell_hv_u^2+2\ell_uv_hv_u)
-4b_hb_u^2-2c_hc_u^2.
\end{aligned}
\]

The four groups are bounded in absolute value by respectively \(2,3,3,2\) times \(\|h\|_f\|u\|_f^2\). For the third group use \(|\ell_a|\le3\|a\|_f\). For the last, Cauchy–Schwarz gives

\[
|4b_hb_u^2+2c_hc_u^2|
\le2\sqrt{2b_h^2+c_h^2}\sqrt{2b_u^4+c_u^4}
\le2\|h\|_f\|u\|_f^2.
\]

It follows directly that \(|D^3F[h,u,u]|\le2\|h\|_F\|u\|_F^2\). This direct mixed bound also matches the matrix self-concordance convention of [3, §2.2]. It is an expository strengthening supplied by the accompanying audit; the scalar argument already proves the convention needed for the 2017 target.

### 3.2 Normality and boundary behavior

Because \(p\) is homogeneous of degree three,

\[
 F(ta)=F(a)-100\log t\qquad(t>0).
\]

Differentiating logarithmic homogeneity yields

\[
 \nabla^2F(a)a=-\nabla F(a),\qquad
 \langle\nabla^2F(a)a,a\rangle=100.
\]

Thus the barrier-gradient bound holds with parameter 100, indeed with equality:

\[
 \langle\nabla F(a),\nabla^2F(a)^{-1}\nabla F(a)\rangle=100.
\]

At every finite boundary point of \(K\), either \(z=0\) or \(p=0\). Hence along every interior sequence converging to that point, \(zp\to0^+\), and \(F=-25\log(zp)\to+\infty\). This also makes the extended function closed. Together with convexity of the domain and positive definite Hessian, these facts establish all the normal-barrier requirements.

## 4. Exact negative-curvature certificate

### 4.1 Reduction of base points and directions

The diagonal maps

\[
 D=\operatorname{diag}(a,b,c),\qquad a,b,c>0,\qquad ab^2=c^3,
\]

are automorphisms of \(K\), and \(f(Dq)=f(q)-4\log c\). For an arbitrary interior point \((x,y,z)\), use

\[
 D=\operatorname{diag}(y^2/z^3,1/y,1/z)
\]

to take it to \((r,1,1)\), where \(r=xy^2/z^3>1\). Differentiating the displayed identity for \(f\) shows that the third-derivative inequality is invariant under this change of coordinates. It suffices to work at \((r,1,1)\).

Every \(h=(h_x,h_y,h_z)\in K\) with \(h_y>0\) decomposes as

\[
 h=h_y(t^3,1,t)+\left(h_x-\frac{h_z^3}{h_y^2}\right)e_x,
 \qquad t=h_z/h_y\ge0.
\]

The coefficient of \(e_x\) is nonnegative. If \(h_y=0\), then \(h_z=0\), so \(h\) is already a nonnegative multiple of \(e_x\). It suffices to check the boundary directions \(h(t)=(t^3,1,t)\), \(t\ge0\), and \(e_x\).

### 4.2 Matrix and minors

Let \(s=r-1>0\) and

\[
 M(r,t)=-s^3D^3f(r,1,1)[h(t)].
\]

This is a symmetric matrix. Its entries, obtainable by ordinary differentiation, are

\[
\begin{aligned}
 M_{11}&=2(t-1)^2(t+2),\\
 M_{12}&=2(t-1)(2t^2+2t-1-3r),\\
 M_{13}&=6(t-1)(r-t^2-t+1),\\
 M_{22}&=4r^3+12r^2-18r^2t+6rt^3-6rt+2t^3,\\
 M_{23}&=12r^2t-18r^2-6rt^3+24rt-6r-6t^3,\\
 M_{33}&=6(r+2)t^3+2(r^3-6r^2-18r-4)t+12r(r+2).
\end{aligned} \tag{NC1}
\]

The leading two-by-two minor and determinant factor as

\[
 \det M_{[1,2],[1,2]}=4s(t-1)^2P(s,t), \tag{NC2}
\]

\[
 \det M=8s^4(t-1)^2R(s,t), \tag{NC3}
\]

where

\[
 P=2(t+2)s^2-3(t-1)(3t+5)s+3(t-1)^2(t+2)^2,
\]

\[
 R=(t+2)\{2ts^2-3(t-1)(3t+1)s+3(t-1)^2(t^2+4t+1)\}.
\]

The accompanying audit records independent exact symbolic reproduction of these polynomial identities. Their positivity is analytic, not inferred from sampling; the displayed proof requires no omitted program or raw output.

For \(0\le t\le1\), every displayed term of \(P\) and \(R\) is nonnegative after replacing \(-(t-1)\) by \(1-t\). In fact both are strictly positive for \(s>0\): for \(t<1\) their constant terms are positive, and at \(t=1\) both equal \(6s^2\).

For \(t\ge1\), the following exact square certificates apply:

\[
 8(t+2)P=
 \{4(t+2)s-3(t-1)(3t+5)\}^2
 +3(t-1)^2(8t^3+21t^2+6t-11), \tag{NC4}
\]

\[
 \frac{8tR}{t+2}=
 \{4ts-3(t-1)(3t+1)\}^2
 +3(t-1)^3(8t^2+13t+3). \tag{NC5}
\]

In (NC4), putting \(t=1+u\) gives

\[
 8t^3+21t^2+6t-11=8u^3+45u^2+72u+24>0
 \quad(u\ge0).
\]

Thus \(P,R>0\) also for \(t\ge1\). For \(t\ne1\), (NC1)–(NC3) and Sylvester's criterion imply \(M(r,t)\succ0\).

The exceptional direction \(t=1\) must not be omitted. Direct substitution gives

\[
 M(r,1)=2s^2
 \begin{pmatrix}
 0&0&0\\0&2r+1&-3\\0&-3&r+2
 \end{pmatrix}\succeq0,
\]

because the lower block has positive diagonal and determinant

\[
 (2r+1)(r+2)-9=(r-1)(2r+7)>0.
\]

Finally, \(h(t)/t^3\to e_x\) as \(t\to\infty\). The cone of positive semidefinite matrices is closed, so \(-D^3f(r,1,1)[e_x]\succeq0\) follows by taking the limit.

The same endpoint also has the explicit certificate

\[
-s^3D^3f(r,1,1)[e_x]
=2aa^T+6sbb^T,\qquad
 a=\begin{pmatrix}1\\2\\-3\end{pmatrix},\quad
 b=\begin{pmatrix}0\\1\\-1\end{pmatrix}.
\]

Both summands are positive semidefinite. Since \(a,b\) are linearly independent and \(s>0\), this matrix has rank two and kernel \(\mathbb R(1,1,1)\). This audit-supplied identity verifies the endpoint directly as well.

Linearity in the directional argument and the decomposition in §4.1 now prove the inequality for every \(h\in K\). Multiplication by 25 preserves it, proving negative curvature for \(F\).

## 5. The cone is genuinely not hyperbolic

The polynomial \(p=xy^2-z^3\) is irreducible in \(\mathbb R[x,y,z]\). Indeed, as a polynomial in \(x\) over \(\mathbb R[y,z]\), it is primitive since \(\gcd(y^2,z^3)=1\), and it is linear and irreducible over the fraction field \(\mathbb R(y,z)\). Gauss's lemma applies.

Suppose a homogeneous polynomial \(H\), hyperbolic in some direction \(e\), had hyperbolicity cone exactly \(K\). Then \(e\in\operatorname{int}K\), and \(H\) vanishes at every boundary point of \(K\). In particular,

\[
 H(z^3/y^2,y,z)=0\qquad(y>0,z>0).
\]

After multiplication by a sufficiently large power of \(y\), the left side is a polynomial in \(y,z\), vanishing on an open set, so is identically zero. The kernel of the substitution \(x\mapsto z^3/y^2\) over \(\mathbb R(y,z)\) is generated by \(x-z^3/y^2\). Primitivity/Gauss's lemma therefore gives \(p\mid H\) in \(\mathbb R[x,y,z]\).

Write \(e=(e_x,e_y,e_z)\), set

\[
 a=(e_xe_y^2)^{1/3}>e_z=:b>0,
\]

and consider \(v=(0,0,1)\). Along the line \(v+te\),

\[
 p(v+te)=a^3t^3-(1+bt)^3
 =\big((a-b)t-1\big)
 \big((a^2+ab+b^2)t^2+(a+2b)t+1\big).
\]

The quadratic factor has discriminant

\[
 (a+2b)^2-4(a^2+ab+b^2)=-3a^2<0.
\]

Thus \(p(v+te)\) has nonreal roots. Since \(p\mid H\), these roots are also roots of \(H(v+te)\), contradicting hyperbolicity in \(e\). The sign convention \(v-te\) instead of \(v+te\) makes no difference to real-rootedness. This excludes every defining hyperbolic polynomial, not just \(p\).

## 6. Relation to the sources and limitations of the claim

[1] states the exact existential problem. [2] supplies the standard negative-curvature definition and explains why dualizing a known barrier is not a legitimate shortcut; its Hankel example has its negative-curvature barrier on the dual spectrahedral cone. The present calculation neither uses that example nor projects a lifted log-determinant barrier.

Dahl–Tunçel–Vandenberghe [3, Definition 3.1 and §6] use the equivalent concavity of directional gradients and, in the inspected 2026 version, still ask the broader question whether every regular cone admits such a barrier. This construction does not answer that universal question.

The cone itself is already present in Hildebrand [4, Theorem 3.2, family 5], with exponents 1/3 and 2/3 and the coordinate identification (x₁,x₂,x₃)=(x,z,y). No claim is made that the cone is new. That work concerns hyperbolic affine spheres, a different use of the word “hyperbolic.” The proof above is an authored direct certificate for this specific pair \((K,F)\). The accompanying independent mathematical audit **accepts the complete solution** at this exact scope. The bounded source check is not a guarantee of novelty or worldwide literature coverage. Recorded computations verified exact identities and deliberately chosen controls; they do not replace the universal analytic arguments. This proof-only edition preserves the complete proof and adds the audit-supplied mixed self-concordance bridge and explicit endpoint PSD certificate. Programs, raw outputs, datasets and copied source documents are not distributed. Edition preparation rechecked frozen byte identities and publication integrity but did not rerun the original mathematical programs or perform new scholarly retrieval, source-text inspection, or literature search.

## References

1. Levent Tunçel, “Polynomial optimization with a focus on hyperbolic polynomials,” Oberwolfach Report 14/2017, pp. 797–800; question on p. 799. [Report DOI](https://doi.org/10.4171/owr/2017/14); [author-hosted contribution](https://www.math.uwaterloo.ca/~ltuncel/publications/OWR-2017-14.pdf).
2. Yu. Nesterov and L. Tunçel, “Local Superlinear Convergence of Polynomial-Time Interior-Point Methods for Hyperbolic Cone Optimization Problems,” arXiv:1412.1857v1, 4 December 2014; published SIAM Journal on Optimization 26 (2016), 139–170. Inspected definitions and §§6, 9.2. [arXiv](https://arxiv.org/abs/1412.1857).
3. Joachim Dahl, Levent Tunçel and Lieven Vandenberghe, “New complexity bounds for primal–dual interior-point algorithms in conic optimization,” arXiv:2509.10263v2, 12 June 2026; inspected author-hosted PDF internally dated revised 16 June 2026. Definitions §2.2 and §3.1; concluding questions p. 25; references through final p. 27. [arXiv](https://arxiv.org/abs/2509.10263); [inspected author-hosted PDF](https://www.math.uwaterloo.ca/~ltuncel/publications/2509.10263.pdf).

4. Roland Hildebrand, “Analytic formulas for complete hyperbolic affine spheres,” arXiv:1305.4814; Theorem 3.2, family 5, pp. 4–5, and §4.2. Used only to credit the pre-existing cone family, not as a curvature-barrier theorem. [arXiv](https://arxiv.org/abs/1305.4814).
