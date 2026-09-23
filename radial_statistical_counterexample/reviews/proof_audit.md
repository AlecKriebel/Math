# Independent adversarial proof audit

**Checkpoint:** 2026-09-23 03:32:36 UTC. **Completion estimate:** 100% of the mathematical verification assigned to this review. This percentage concerns the proof, not the literature-priority audit or publication package.

**Verdict:** The proposed product example is a complete counterexample to the implication printed in item 3(e) of the 1998 source. The non-self-dual extension is also correct. No mathematical gap was found. Novelty, historical priority, and whether the question remains regarded as open are separate questions and are not certified by this review.

## Source and claim alignment

I independently downloaded and visually inspected the original printed pages rather than relying on the database paraphrase or the candidate's malformed citation markers:

- H. Furuhata, H. Matsuzoe and H. Urakawa, *Open Problems in Affine Differential Geometry and Related Topics*, Interdisciplinary Information Sciences **4** (1998), 125–127, [original PDF](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en). Item 3(e), p.126, asks whether integrability of all the radial orthogonal distributions implies 1-conformal flatness of the dual structure. The center is excluded from the distribution's domain. No nonzero-cubic-tensor, compactness, or completeness condition is imposed. Item 3(a), p.125, expressly treats a Riemannian metric with its Levi–Civita connection as a statistical manifold.
- T. Kurose, *On the divergences of 1-conformally flat statistical manifolds*, Tohoku Mathematical Journal **46** (1994), 427–433, [original PDF](https://www.jstage.jst.go.jp/article/tmj1949/46/3/46_3_427/_pdf). Pages 427–428 give the statistical and dual-connection definitions. Setting alpha equal to 1 in the displayed equivalence formula on p.428 gives exactly the connection change used below. The flatness notion is local flatness of that affine connection.

The precise falsified assertion is universal over statistical manifolds: integrability for every center and every local convex neighborhood under consideration is claimed to force local 1-conformal flatness of the dual. A single three-dimensional statistical manifold satisfying the premise and failing the conclusion at every point suffices.

## Independent analytic checks

### Statistical structure and duality

Let \(g=g_{S^2(1)}+dt^2\) and let \(D\) be its Levi–Civita connection. Torsion vanishes and \(Dg=0\), so the statistical condition holds. Substitution into the defining duality identity gives \(D^*=D\). Thus there is no distinction between the tested connection and its dual in the main example.

### Radial distribution, all centers, and neighborhoods

Fix a center \(p\). On a convex normal neighborhood, smoothly choose the unique geodesic \(\gamma_q:[0,1]\to M\) from \(p\) to \(q\), affinely parameterized. The first variation of

\[
E_p(q)=\tfrac12\int_0^1g(\dot\gamma_q,\dot\gamma_q)\,du
\]

is \(dE_p(w)=g(\dot\gamma_q(1),w)\): metric compatibility differentiates the integrand, torsion-freeness interchanges the two variation derivatives, the geodesic equation removes the integral term, and the fixed initial endpoint removes the initial boundary term. Consequently the distribution is \(\ker dE_p\). For \(q\ne p\), positive definiteness gives \(dE_p(\dot\gamma_q(1))>0\), so regular level hypersurfaces integrate the distribution.

This is local and applies at every center. It also applies to any larger convex neighborhood whose geodesic choice defines the smooth distribution in the problem: the same endpoint-variation identity applies locally along that choice. One need not assert that the entire sphere product has unique geodesics, or extend the distribution through its excluded center. Replacing the affine parameter by another regular affine parameter multiplies the terminal velocity by a nonzero scalar and leaves its orthogonal complement unchanged. Calling the leaves distance spheres is justified on a sufficiently small normal neighborhood; the proof needs only the energy identity.

### Direct curvature obstruction

The verified alpha=1 formula is

\[
\widehat g=e^\varphi g,\qquad
\widehat D_XY=D_XY-g(X,Y)V,\qquad V=\operatorname{grad}_g\varphi.
\]

I recomputed its curvature using the difference tensor \(B(X,Y)=-g(X,Y)V\). With \(R(X,Y)Z=D_XD_YZ-D_YD_XZ-D_{[X,Y]}Z\), the derivative and quadratic terms are

\[
(D_XB)(Y,Z)=-g(Y,Z)D_XV,
\quad B(X,B(Y,Z))=g(Y,Z)g(X,V)V.
\]

Hence, for \(A(X)=D_XV-g(X,V)V\),

\[
\widehat R(X,Y)Z=R(X,Y)Z-g(Y,Z)A(X)+g(X,Z)A(Y).
\]

Flatness would require

\[
R(X,Y)Z=g(Y,Z)A(X)-g(X,Z)A(Y).
\]

At an arbitrary point choose orthonormal \(e_1,e_2\) tangent to the unit sphere and \(e_3=\partial_t\). Product curvature gives
\(R(e_1,e_2)e_2=e_1\) and \(R(e_1,e_3)e_3=0\). The necessary identity yields both \(A(e_1)=e_1\) and \(A(e_1)=0\). This contradiction permits *arbitrary* \(A\), so no differential assumption on the putative conformal factor has been overlooked. It occurs at every point and defeats every local choice of factor.

An independent contraction gives \(\operatorname{Ric}=\operatorname{diag}(1,1,0)\) and \(W(e_3,e_1)e_1=-e_3/2\) for the projective Weyl tensor. This agrees with Kurose's projective-flatness criterion, but that criterion is not needed for the direct proof.

### Non-self-dual extension

Put \(a=dt\), \(g_1=e^tg\), and \(D^1_XY=D_XY+a(X)Y+a(Y)X\). Direct differentiation gives

\[
(D^1_Xg_1)(Y,Z)=-a(X)g_1(Y,Z)-a(Y)g_1(X,Z)-a(Z)g_1(X,Y),
\]

which is totally symmetric. Its value on three copies of \(\partial_t\) is \(-3e^t\), everywhere nonzero. The duality identity gives
\((D^1)^*_XY=D_XY-g(X,Y)\partial_t\).

For full parametrization control, if \(\gamma(u)\) is a \(D\)-geodesic, then \(\gamma(u(s))\) is a \(D^1\)-geodesic exactly when

\[
u''+2\frac{d(t\circ\gamma)}{du}(u')^2=0.
\]

Locally this has the positive solution \(u'=C e^{-2t\circ\gamma}\), with \(C>0\) chosen to fit the endpoints. Thus the two connections have the same unparameterized geodesic segments; the terminal velocities differ only by a nonzero scalar. The conformal metrics have the same orthogonality. Their radial distributions therefore coincide locally and are integrable.

Finally, a 1-conformal change of the dual structure with factor \(\psi\) has connection

\[
D_XY-g(X,Y)\operatorname{grad}_g(t+\psi).
\]

If flat, this would be a forbidden 1-conformal flattening of the original Levi–Civita structure. The extension is valid and shows that requiring a nonzero cubic tensor alone does not repair the implication.

## Boundary and falsification checks

- The construction works for every dimension \(n\ge3\) on \(S^2(1)\times\mathbb R^{n-2}\), using just the same three frame vectors. It does not claim a three-vector obstruction in dimension two.
- Positive definiteness is available, so no null-vector or rank-drop issue enters the radial regularity argument.
- The center is excluded exactly as in the original question. Requiring regularity at the center would change the question and would also invalidate the proposed radial rank condition generally.
- The main example is connected, simply connected, smooth, positive definite, and complete. None of these extra properties is needed for the local counterexample. Completeness is not asserted for the non-self-dual deformation.
- Ordinary Riemannian conformal flatness is a different condition; replacing the printed statistical definition by it would change the problem.
- The argument proves a universal negative answer, not a classification of all structures with integrable radial distributions. Such a classification is unnecessary for resolving the printed yes/no question.
- The filenames `gradient_path_counterexample.py` and `gradient_path_counterexample_output.txt` are not evidence for this geometry claim. No conclusion here relies on those unrelated computational artifacts.

**Strongest verified result:** Both stated statistical structures satisfy the printed integrability premise for every center and fail the printed local conclusion everywhere. **Exact remaining mathematical gap:** none found. **Remaining gap outside this audit:** a bounded search can assess prior publication, but cannot prove that no earlier resolution exists.
