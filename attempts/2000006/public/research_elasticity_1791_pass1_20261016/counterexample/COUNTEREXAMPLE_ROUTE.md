# E-6322 counterexample route, pass 1

Date: 2026-10-16. Frozen target: `recovery_elasticity_1791_20261015/formulation_gate/RESEARCH_TARGET.md`.

## Outcome

**No compliant counterexample has been established.** In particular, none of the maps below is claimed to be a full-class global minimizer. This pass establishes a local replacement obstruction to a substantial family of apparent counterexamples. It does not prove E-6322, nor refute any broader sufficient-condition programme.

The target remains the exact first-gradient density

\[
W(F)=a|F|^6+b|\operatorname{cof}F|^3+c(\det F)^2+d(\det F)^{-2},\qquad a,b,c,d>0,
\]

on positive determinants, with the complete finite-energy Sobolev comparison class and a smooth diffeomorphic trace on the entire smooth boundary.

## 1. Explicit admissible degeneracy is not minimizing degeneracy

On the unit ball, let

\[
y_\alpha(x)=|x|^{\alpha-1}x,\quad y_\alpha(0)=0,\qquad 1<\alpha<3/2.
\]

For \(r=|x|>0\), the singular values are \(\alpha r^{\alpha-1},r^{\alpha-1},r^{\alpha-1}\). Thus

\[
\det Dy_\alpha=\alpha r^{3\alpha-3},\qquad
|Dy_\alpha|^6=(\alpha^2+2)^3r^{6\alpha-6},
\]

\[
|\operatorname{cof}Dy_\alpha|^3=(1+2\alpha^2)^{3/2}r^{6\alpha-6}.
\]

It follows directly that \(y_\alpha\in W^{1,6}\), that its determinant is positive almost everywhere with essential infimum zero, and that its inverse-square determinant is integrable precisely when \(\alpha<3/2\). Its trace is the identity, certified by the globally smooth diffeomorphism \(G(x)=x\).

The exact energy is

\[
I(y_\alpha)=4\pi\left[\frac{a(\alpha^2+2)^3+b(1+2\alpha^2)^{3/2}+c\alpha^2}{6\alpha-3}
+\frac{d\alpha^{-2}}{9-6\alpha}\right].
\]

Nevertheless, this is **not a counterexample**. For any affine trace \(F_0x+q\), \(\det F_0>0\), the integral averages of all first-, second-, and third-order minors are those of \(F_0\). Jensen's inequality applied to the convex function of independent minors proves

\[
I(y)\ge |\Omega|W(F_0).
\]

The term \(a|F|^6\) is strictly convex, so equality forces \(Dy=F_0\) almost everywhere and the trace fixes the additive constant. Consequently the affine map is the unique full-class minimizer. The minors identities hold for the full \(W^{1,6}\) trace class, by approximation in that space and polynomial continuity of the minors; positivity of determinants of the approximating maps is not needed for these identities.

For the radial example, even the inverse-determinant term alone strictly decreases on replacing \(y_\alpha\) by the identity:

\[
\frac{1}{\alpha^2(9-6\alpha)}-\frac13
=\frac{(\alpha-1)^2(2\alpha+1)}{3\alpha^2(3-2\alpha)}>0.
\]

This confirms that finite barrier energy and smooth compatible boundary data do not by themselves make the candidate minimizing.

## 2. Local replacement lemma: all exact isotropic-degree collapses are excluded

**Lemma.** Let \(\Omega\) contain \(\overline B_\rho(x_0)\), and suppose an admissible deformation agrees there with

\[
y(x_0+r\theta)=y_0+r^\alpha\phi(\theta),\qquad 0<r<\rho,\quad \theta\in S^2,
\]

where \(1<\alpha<3/2\), \(\phi\in C^1(S^2;\mathbb R^3)\), and the degree-one cone

\[
h(r\theta)=r\phi(\theta)
\]

has \(\det Dh(r\theta)=j(\theta)>0\) for every \(\theta\in S^2\). Then \(y\) is not a local minimizer in the \(W^{1,6}\) topology, and hence is not a full-class global minimizer.

This statement does not assume affine data on the outer boundary. The angular trace may be nonaffine. Continuity and compactness give \(\min j>0\).

**Proof.** Write \(H(\theta)=Dh(\theta)\) and

\[
H_\alpha(\theta)=H(\theta)+(\alpha-1)\phi(\theta)\otimes\theta.
\]

Since \(H\theta=\phi\),

\[
Dy(x_0+r\theta)=r^{\alpha-1}H_\alpha(\theta),\qquad
\det H_\alpha=\alpha j.
\]

The determinant identity follows either from the matrix determinant lemma or by separating the radial column from the two tangent columns. Define the finite constants

\[
C_\gamma=\int_{S^2}\left(a|H_\gamma|^6+b|\operatorname{cof}H_\gamma|^3+c(\gamma j)^2\right)\,dS,
\quad Q=\int_{S^2}j^{-2}\,dS>0,
\]

for \(\gamma=1,\alpha\). For \(0<R<\rho\), replace the map only in \(B_R(x_0)\) by

\[
v_R(x_0+r\theta)=y_0+R^{\alpha-1}r\phi(\theta).
\]

The traces agree on \(\partial B_R\). The replacement is Lipschitz in the ball, has determinant \(R^{3\alpha-3}j(\theta)>0\) almost everywhere, and has finite barrier energy. Sobolev gluing therefore yields an admissible full-class competitor with the original outer trace. No smoothness or injectivity restriction on competitors is being added.

All three positive terms in \(W\) are homogeneous of degree six in \(F\), whereas the inverse determinant term is homogeneous of degree minus six. Direct radial integration gives

\[
I(y;B_R)-I(v_R;B_R)
=R^{6\alpha-3}\left(\frac{C_\alpha}{6\alpha-3}-\frac{C_1}{3}\right)
+dQ R^{9-6\alpha}\left(\frac{\alpha^{-2}}{9-6\alpha}-\frac13\right).
\]

The second bracket is strictly positive by the displayed factorization in Section 1. Since

\[
(6\alpha-3)-(9-6\alpha)=12(\alpha-1)>0,
\]

the second term dominates the possibly negative first term as \(R\downarrow0\). Thus \(I(v_R)<I(y)\) for every sufficiently small \(R\).

Furthermore,

\[
\|Dv_R-Dy\|_{L^6(B_R)}^6=O(R^{6\alpha-3}),\qquad
\|v_R-y\|_{L^6(B_R)}^6=O(R^{6\alpha+3}),
\]

so \(v_R\to y\) strongly in \(W^{1,6}\). This proves the local claim. \(\square\)

**Scope.** The lemma excludes exact same-degree homogeneous collapse with a positive angular Jacobian, including nonaffine star-shaped angular variants. It does not cover a general asymptotic expansion, anisotropic singularity, non-star-shaped image of small spheres, or boundary-only degeneracy. No such extension is asserted.

## 3. What a viable anisotropic route would still need

Anisotropic maps can satisfy the integrability tests without shrinking all gradient directions. For example, on the punctured unit ball set

\[
y_i(x)=|x|^{\alpha_i-1}x_i,\quad i=1,2,3,\qquad
(\alpha_1,\alpha_2,\alpha_3)=(3/4,3/4,9/4).
\]

The matrix determinant lemma gives

\[
\det Dy=r^{\alpha_1+\alpha_2+\alpha_3-3}\sum_{i=1}^3\alpha_i\theta_i^2
=r^{3/4}\left(\frac34(\theta_1^2+\theta_2^2)+\frac94\theta_3^2\right).
\]

The gradient grows at most like \(r^{-1/4}\), its sixth power at most like \(r^{-3/2}\), and \((\det Dy)^{-2}\) at most like \(r^{-3/2}\); both are integrable in three dimensions. The cofactor-cubic term is integrable as well, either directly or from \(|\operatorname{cof}F|^3\le C|F|^6\). Hence this also gives a finite-energy map with determinant tending to zero.

Its unit-sphere trace is again the identity. Therefore it is again **not minimizing**, by Section 1. The only useful lesson is that the simple homogeneity-dominance argument does not exhaust possible singular scaling: unbounded stretches can balance the inverse-determinant scale. Altering the outer trace does not certify the interior map as stationary or minimizing. A compliant counterexample would still require a constructed admissible boundary datum, a specified full-class minimizer, and a rigorous global comparison or calibration.

## 4. Calibration gap that must not be skipped

Convexity in the independent minors supplies a pointwise supporting inequality at \(F_*(x)\), with coefficients

\[
A_*=6a|F_*|^4F_*,\quad B_*=3b|\operatorname{cof}F_*|\operatorname{cof}F_*,\quad
q_*=2cJ_*-2dJ_*^{-3}.
\]

For a nonconstant candidate, these coefficients depend on \(x\). Integrals of minors with these variable weights are not fixed by the boundary trace. Classical stationarity, even if justified across a singularity, does not make all nonlinear weighted-minor remainders vanish. In particular, \(q_*\to-\infty\) as \(J_*\to0\). A genuine calibration must control the resulting integrals for every admissible Sobolev competitor; merely writing the supporting inequality or the Euler–Lagrange equation is insufficient.

## 5. Literature scope checks

The full frozen target, baseline screen, and formulation adjudication were read. The recovered Bevan–Yan 2008 introduction, definition of its restricted class, and open-question discussion confirm that its double-cover example is not a full-class, three-dimensional, diffeomorphically compatible example. The recovered Bevan–Kabisch introduction likewise distinguishes the barrier law from the zero-permitting law and restricted shear/twist problems from full comparison.

A bounded supplementary search located Guerra–Tione, *A singular minimizer of a smooth strongly polyconvex functional in two dimensions*, arXiv:2609.32404, dated September 26, 2026, https://arxiv.org/abs/2609.32404. Its primary abstract states a Lipschitz non-\(C^1\) unique global minimizer mapping \(\mathbb R^2\) into \(\mathbb R^6\) for a constructed smooth strongly polyconvex functional. That is not the dimension, codimension, fixed singular-barrier density, or determinant conclusion of E-6322. The full paper was not audited in this route.

## Acceptance status

- Actual full-class minimizer with essential determinant infimum zero: **not produced**.
- Frozen benchmark refuted: **no**.
- Exact homogeneous-collapse family excluded as local minimizers: **proved above**.
- Boundary-only or genuinely anisotropic singular minimizer route: **unresolved**.
