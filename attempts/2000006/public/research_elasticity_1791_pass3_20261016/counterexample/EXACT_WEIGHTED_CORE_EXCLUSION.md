# E-6322, pass 3: exclusion of all exact C²-angular weighted-power collapse cores

Date: 2026-10-16. The frozen benchmark is unchanged. This is a necessary-structure result, not a proof of E-6322 and not a counterexample. No originality claim is made.

## 1. Statement

Suppose an admissible deformation agrees in an interior punctured ball, after translating its reference and target origins, with

\[
y_i(r\theta)=r^{\alpha_i}\phi_i(\theta),\qquad
0<r<\rho,\quad\theta\in S^2,\quad i=1,2,3,
\]

where

\[
0<\alpha_1\le\alpha_2\le\alpha_3,\qquad
\phi\in C^2(S^2;\mathbb R^3),\qquad
s:=\alpha_1+\alpha_2+\alpha_3>3.
\]

Then it is not a full-class local or global minimizer for E-6322.

The proof below combines the pass-2 third-component obstruction with a new argument for its complementary exponent range. It also shows that, for these exact cores, angular determinant degeneracy is already incompatible with finite inverse-square determinant energy.

No statement is made about a general asymptotic expansion, less regular angular functions, or a boundary singularity.

## 2. Exact scaling and consequences of admissibility

Set \(m=\alpha_1\), \(\gamma=s-3>0\),

\[
A_i(\theta)=\alpha_i\phi_i(\theta)\theta+\nabla_S\phi_i(\theta),\qquad
p_i:=\nabla y_i=r^{\alpha_i-1}A_i(\theta),
\]

and

\[
j(\theta)=\det\begin{pmatrix}A_1\\A_2\\A_3\end{pmatrix},\qquad
J=\det Dy=r^\gamma j(\theta).
\]

### 2.1 Angular zeros cannot occur in a finite-energy exact core

Because \(J>0\) almost everywhere, \(j>0\) almost everywhere on the sphere. Since \(j\) is continuous, \(j\ge0\) everywhere. Finite barrier energy on any fixed annulus inside the core implies

\[
\int_{S^2}j^{-2}\,dS<\infty.
\]

But \(\phi\in C^2\) implies \(j\in C^1(S^2)\), hence \(j\) is Lipschitz. If \(j(\theta_0)=0\), then \(j(\theta)\le L\operatorname{dist}_{S^2}(\theta,\theta_0)\). Consequently,

\[
\int_{\operatorname{dist}(\theta,\theta_0)<\delta}j(\theta)^{-2}\,dS
\ge c\int_0^\delta t^{-2}\sin t\,dt=+\infty,
\]

a contradiction. Therefore \(\min_{S^2}j>0\).

In particular every row \(A_i\), and every pairwise cross product of rows, is nonzero everywhere. By compactness their norms have positive minima.

### 2.2 Radial integrability restrictions

The exact scaling and the nonzero first row give \(|Dy|\asymp r^{m-1}\) for small \(r\). Finite sixth-power gradient energy therefore forces

\[
m>1/2.
\]

Finite inverse-square determinant energy forces

\[
s<9/2.
\]

Conversely, for smooth angular data with \(\min j>0\), these two restrictions suffice for the energy terms to be integrable, since \(|\operatorname{cof}F|^3\le C|F|^6\).

**Admissibility does not by itself force the pass-2 exponent inequality.** For example,

\[
(\alpha_1,\alpha_2,\alpha_3)=(3/5,5/4,5/4)
\]

has \(s=31/10\), \(m>1/2\), and

\[
\eta:=2(3\alpha_1+\alpha_2+2\alpha_3-6)=-9/10<0.
\]

Taking \(\phi(\theta)=\theta\) gives a finite-energy map. This is only an exponent-feasibility example; it is not a minimizing example.

## 3. Previously established range: η>0

The independently audited pass-2 report proves that these cores cannot satisfy the Euler equation when \(\eta>0\). The key points are:

1. Positive local degree supplies an angle where \(\phi_1=\phi_2=0\).
2. On that ray, the third barrier-stress divergence has a nonzero coefficient and radial exponent \(\alpha_1+\alpha_2-3-3\gamma\).
3. The entire positive-energy third divergence is \(O(r^{4\alpha_1+\alpha_3-6})\).
4. The exponent difference is exactly \(\eta>0\), so cancellation is impossible.

The detailed proof is in the unchanged pass-2 artifact `ANISOTROPIC_STATIONARITY_OBSTRUCTION.md`, SHA-256 `a7c90e5d46dc30e280ef4753437feddf0248184e9f29789c13b35a90cadc44fb`.

It remains to treat \(\eta\le0\).

## 4. The remaining range has a unique lowest exponent

Assume \(\eta\le0\). If \(\alpha_2=m\), direct substitution gives

\[
\eta=4(s-3)>0,
\]

which is impossible. Hence

\[
\alpha_2>m,\qquad\alpha_3>m.
\]

Rewriting the assumed inequality as

\[
s+2m+\alpha_3\le6
\]

also gives

\[
s+3m\le6-(\alpha_3-m)<6,\qquad 1/2<m<1.
\]

The first row is therefore the unique dominant row of the gradient as \(r\downarrow0\).

## 5. The first Euler equation reduces to scalar 6-harmonicity

Suppose for contradiction that the core belongs to a local minimizer. On every compact subset of the punctured ball the map is \(C^2\), with determinant bounded below. Sufficiently small smooth additive variations there are admissible. Thus the usual Euler equation holds classically on the punctured core. No Euler equation across the singular point is assumed.

Write the positive density as

\[
H(F)=a|F|^6+b|\operatorname{cof}F|^3+cJ^2.
\]

The leading first-row stress is

\[
6a|p_1|^4p_1.
\]

Its divergence has radial degree \(5m-6\). The remaining first-row contributions are strictly higher order, as follows.

### 5.1 The sixth-power term's correction

Since \(\alpha_2>m\),

\[
|F|^4p_1-|p_1|^4p_1
=O(r^{3m+2\alpha_2-5}).
\]

After taking divergence, the gap above \(5m-6\) is \(2(\alpha_2-m)>0\). This also follows directly by expanding \((|p_1|^2+|p_2|^2+|p_3|^2)^2p_1\).

### 5.2 Cofactor-cubic contribution

Let \(C_1=p_2\times p_3\), \(C_2=p_3\times p_1\), and \(C_3=p_1\times p_2\). Differentiation with respect to \(p_1\) only involves \(C_2,C_3\). Since

\[
|\operatorname{cof}F|=O(r^{m+\alpha_2-2}),
\]

the first-row cofactor stress is \(O(r^{2m+3\alpha_2-5})\), and its divergence is

\[
O(r^{2m+3\alpha_2-6}).
\]

The gap is \(3(\alpha_2-m)>0\).

### 5.3 Determinant-square contribution

The first stress row is \(2cJC_1\), so its divergence has order

\[
O(r^{\gamma+\alpha_2+\alpha_3-3}).
\]

Its exponent exceeds \(5m-6\) by \(2s-6m>0\).

### 5.4 Barrier contribution

The first barrier stress row is \(-2dJ^{-3}C_1\). Its divergence has order

\[
O(r^{\alpha_2+\alpha_3-3-3\gamma})
=O(r^{6-2s-m}).
\]

The gap above \(5m-6\) is

\[
2(6-s-3m)>0.
\]

All estimates remain valid after one differentiation: the angular coefficients are \(C^1\), with bounded first derivatives, and differentiation loses at most one radial power. The positive lower bound of \(j\) controls the barrier coefficients.

### 5.5 Exact limiting equation

The leading divergence equals \(r^{5m-6}L(\theta)\) for a continuous angular function \(L\). Divide the first Euler equation by \(r^{5m-6}\) and let \(r\downarrow0\) at fixed angle. All other terms tend to zero, so \(L(\theta)=0\). Therefore the scalar function

\[
u(x):=y_1(x)=r^m\phi_1(\theta)
\]

satisfies exactly

\[
\operatorname{div}(|\nabla u|^4\nabla u)=0
\quad\text{on }B_\rho\setminus\{0\}.
\]

Only this scalar reduced equation will be extended across the puncture below; no such extension is asserted for the full elasticity system.

## 6. Scalar homogeneous solutions cannot supply the remaining core

Write \(\varphi=\phi_1\) and

\[
A(\theta)=(m^2\varphi^2+|\nabla_S\varphi|^2)^2.
\]

The scalar equation in spherical variables is

\[
\operatorname{div}_S(A\nabla_S\varphi)+m(5m-3)A\varphi=0.
\]

Multiplying by \(\varphi\) and integrating over the sphere gives

\[
\int_{S^2}A|\nabla_S\varphi|^2\,dS
=m(5m-3)\int_{S^2}A\varphi^2\,dS.
\]

### 6.1 The range 1/2<m<3/5

The right side is nonpositive and has a strictly negative multiplier unless \(A\varphi^2\) vanishes identically. The left side is nonnegative. Thus both integrals vanish and \(\varphi\equiv0\), contradicting the nonzero first row required by \(j>0\).

### 6.2 The critical exponent m=3/5

The identity forces \(\nabla_S\varphi=0\), so \(\varphi\) is constant. A zero constant again contradicts \(j>0\); a nonzero constant makes \(u=r^m\varphi\) have one sign.

That one-sign alternative contradicts positive local degree. For completeness, \(j>0\) implies \(\phi\ne0\) everywhere, so the origin is an isolated zero of the continuous map \(y\). On a small fixed spherical boundary, its image has positive distance from zero. A nearby nonzero regular value in the image has at least one preimage, all with positive Jacobian, so the degree near zero is positive. Therefore sufficiently small target points on both the positive and negative first coordinate axis have preimages. Their first coordinates require \(u\) to take both signs. This rules out the critical case.

### 6.3 The range 3/5<m<1

The scalar stress satisfies

\[
|\nabla u|^4\nabla u=O(r^{5m-5}).
\]

On the sphere of radius \(\epsilon\), its absolute flux is \(O(\epsilon^{5m-3})\to0\). Integrating the punctured scalar equation against any smooth compactly supported test function and letting \(\epsilon\downarrow0\) therefore gives

\[
\int_{B_\rho}|\nabla u|^4\nabla u\cdot\nabla\psi\,dx=0.
\]

The volume integral converges because \(u\in W^{1,6}\). Thus \(u\) is a weak scalar 6-harmonic function on the whole ball.

The classical interior regularity theorem for scalar p-harmonic functions now applies: \(u\) has locally Hölder-continuous, hence bounded, first derivatives. A primary source is Uhlenbeck (1977), printed p.222, the scalar corollary stated for \(d^*(|df|^p df)=0\), with \(f\in W^{1,p+2}\). Taking its parameter \(p=4\) gives precisely the present weak 6-Laplace equation.

But

\[
\nabla u(r\theta)=r^{m-1}\bigl(m\varphi(\theta)\theta+\nabla_S\varphi(\theta)\bigr),
\]

and the angular coefficient is nonzero, since it is the first row of a matrix with positive determinant. With \(m<1\), this is unbounded as \(r\downarrow0\), a contradiction.

All exponent cases are excluded. Together with Section 3, this proves the statement in Section 1.

## 7. Primary source and inspection scope

K. Uhlenbeck, *Regularity for a class of non-linear elliptic systems*, Acta Mathematica 138 (1977), 219–240. DOI: https://doi.org/10.1007/BF02392316

Original-paper PDF, hosted by the Tsinghua Yau Mathematical Sciences Center archive:
https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6219-11511_2006_Article_BF02392316.pdf

Retrieved 2026-10-16: 861,863 bytes; SHA-256 `bb041a82ffd0b1c7e1b694a162aac642c2755dfd3bf00726e443ac8106e7239a`.

The introduction and theorem statements on printed pp.219–222 were inspected in extracted text; p.222 was also rendered and visually inspected to verify the scalar exponent convention and conclusion. The article's full proof was not independently re-audited. Only its scalar interior regularity corollary is used. It is not applied directly to the full polyconvex elasticity system.

The source PDF, extracted text, and rendered page are private inspection material and are not part of an authored public deliverable.

## 8. What remains unresolved

No actual minimizer with essential determinant infimum zero has been produced. The new exclusion depends on an exact weighted-power representation and C² angular data. In particular:

- A lower-order term could restore positivity where a leading angular determinant vanishes; the exact separation used here would then fail.
- Merely C¹ or rougher angular profiles may lack the Lipschitz angular determinant needed by Section 2.1.
- A genuinely nonhomogeneous core may have no scalar homogeneous leading equation of the form derived above.
- Boundary singularities with insufficient regularity remain outside this argument.

These remaining possibilities are not asserted to occur for minimizers. They identify gaps in the counterexample search, not evidence against E-6322. The full benchmark remains unresolved.
