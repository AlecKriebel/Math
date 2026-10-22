# E-6322 pass 2: targeted regularity and higher-integrability screen

16 October 2026. The pass-1 audit was read before this investigation. This screen addresses the missing unconditional gradient/inverse regularity, rather than repeating the existence and a.e.-injectivity literature review.

## Outcome

A genuine known-theorem improvement was found: every admitted map has an a.e. inverse in W^{1,9/5}(G(Ω)), with cofactors in L^{9/4}, determinant in L^3, and the prescribed full inverse trace. The primary theorem and its exact application are in `INVERSE_SOBOLEV_BASELINE.md`.

No inspected regularity theorem supplies global C^{1,β} regularity, bounded inverse determinant, or an integrability bootstrap closing E-6322 for arbitrary large smooth diffeomorphic data. This is a bounded, targeted search conclusion, not a proof of novelty or an exhaustive current-status claim.

## 1. The exact structure does not meet standard upper-growth assumptions

Write W_+(F)=a|F|^6+b|cof F|^3+c(det F)^2. It is important that **only W_+ is degree-six homogeneous**:

\[
W(tF)=t^6W_+(F)+dt^{-6}(\det F)^{-2}\qquad(t>0).
\]

The complete density is autonomous (independent of the material point), but not homogeneous of degree six as a function of F. Its common positive degree does not eliminate the singular barrier.

Direct obstructions to several possible hypotheses are:

1. Along F_ε=diag(1,1,ε), the norm stays bounded while W(F_ε)≥dε^{-2}. Thus the complete density is not locally bounded on matrix space and has no global finite polynomial upper bound in |F|.
2. Even at large norm, F_L=diag(L,L,L^{-m}), m>5, gives |F_L|≈L and W(F_L)/|F_L|^6≥cL^{2m-10}→∞. Consequently the barrier is not a uniformly lower-order perturbation at infinity. Restricting attention to scalar dilations tF with fixed invertible F misses these anisotropic paths.
3. The other positive terms also have degree six: along tI their ratios to |tI|^6 are nonzero constants. They are not strictly lower-order perturbations of the |F|^6 term merely because the minors have exponents 3 and 2.
4. Frame indifference and isotropy are not the radial-gradient structure W(F)=f(|F|). Matrices diag(sqrt(3−2ε²),ε,ε) have the same Frobenius norm as I but unbounded W as ε→0. Therefore an Uhlenbeck-type structure cannot be inferred from isotropy alone.

These are direct calculations for the frozen law, not statements that no different regularity argument can work. Likewise, trimming the barrier or restricting to J≥δ changes the energy or assumes the property that needs to be proved.

## 2. An exact higher-integrability theorem and its failed hypotheses

Christoph Scheven and Thomas Schmidt, *Asymptotically regular problems I: Higher integrability*, author preprint, November 2009; published J. Differential Equations 248 (2010), 745–791:

https://cvgmt.sns.it/media/doc/paper/1765/asyI.pdf

Definition 2.1 (preprint p.6) specifies a globally C² comparison density g with two-sided ellipticity and p-growth Hessian bounds. Theorem 2.4 (p.7) assumes a finite, locally bounded Borel density f on all matrix space and |f−g|/|F|^p→0 at infinity. It gives local higher gradient integrability; the resulting global polynomial upper bound is explicit in (2.12), p.8. Theorem 2.3 (pp.6–7) is the corresponding ordinary weak-system result and likewise assumes a locally bounded vector field with p−1 growth.

E-6322 fails the finite/local-boundedness and upper-growth assumptions by §1, even when only positive determinants are approached. The weak-system version additionally cannot be invoked before ordinary Piola-stress integrability and admissible additive stationarity are justified. Pass 1 established composed variations, not that ordinary system.

For context only, the primary institutional abstract of Dougherty's thesis explicitly describes the Dougherty–Phillips bootstrap as requiring a perturbation of strictly smaller growth than the leading gradient power. The original 1997 journal theorem was not retrieved in full; its publisher synopsis alone is not treated as an applicability certificate. The source locations are https://docs.lib.purdue.edu/dissertations/AAI9601489/ and https://doi.org/10.1137/S0036141095293384 .

## 3. Three-dimensional partial regularity with minor growth

Menita Carozza and Antonia Passarelli di Napoli, *Model problems from nonlinear elasticity: partial regularity results*, author manuscript, Theorems A and B, pp.2–3:

https://cvgmt.sns.it/media/doc/paper/1559/antomeni0304.pdf

The model is |Du|²+f(Adj Du)+g(det Du), with f and g finite C² convex functions on their full Euclidean spaces. Theorem A has minor exponents 1<q<p<2 and global two-sided Hessian bounds (H1)–(H2). Theorem B treats p=q≤2 for already locally Lipschitz weak local minimizers with an additional oscillation condition. Conclusions are C^{1,α} on an interior open full-measure set.

E-6322 has a different leading exponent and cofactor exponent, and its determinant density is infinite for J≤0 and has h''(J)=2c+6dJ^{-4}. This violates the stated full-line finite/smooth and Hessian hypotheses. Even a valid partial regularity theorem would leave exceptional points and boundary collars to control. It must not be promoted to the whole-domain estimate needed here.

## 4. Everywhere regularity titles with different structure

### Dengler, 2022

Marcel Dengler, *Everywhere regularity results for a polyconvex functional in finite elasticity*, arXiv:2205.07694v2, 18 May 2022, equations (1)–(2) and Theorems 1.2–1.4, pp.1–3:

https://arxiv.org/pdf/2205.07694v2

The domain and target are two-dimensional. The determinant density ρ is smooth and finite on all R, zero for negative arguments, and affine for sufficiently large positive arguments, so its first derivative is bounded. The W^{2,2} result assumes its parameter γ<1. The higher-order result assumes W^{2,2} and Hölder continuity of the Jacobian. Neither the determinant barrier nor the missing initial regularity in E-6322 fits these hypotheses. Its conclusions are local, not whole-boundary estimates for arbitrary three-dimensional data.

### Guerra–Tione, June 2026

André Guerra and Riccardo Tione, *Stationary points of conformally invariant polyconvex energies*, arXiv:2606.10586v1, 9 June 2026, equations (1.7)–(1.8), Theorems 1.1 and 1.7, Lemma 2.1:

https://arxiv.org/html/2606.10586v1

This is a planar theory for finite C¹ integrands F(A)=f(|A|²,det A), with f one-homogeneous in its two arguments, even in determinant, and satisfying the stated strong polyconvexity conditions. Lemma 2.1 identifies conformal invariance with degree-two homogeneity in A and rotation invariance. Theorem 1.7 gives interior C¹ regularity for orientation-preserving stationary points. E-6322 is three-dimensional, has both positive and negative degree-six terms, and has an infinite determinant barrier. Its common positive degree is not the conformal invariance used in this theorem.

### Gangbo–Jacobs–Kim, 2023

Wilfrid Gangbo, Matt Jacobs and Inwon Kim, *Well-posedness and regularity for a polyconvex energy*, author manuscript, Theorems 2.1, 2.2 and 2.5, pp.4–5:

https://www.math.ucla.edu/~wgangbo/publications/Final-GJK.pdf

The actual energy is an H¹ projection onto volume-preserving diffeomorphisms with identity boundary data. The existence/regularity result assumes the prescribed S is sufficiently close to identity in W^{2,r}, r>dimension. The uniqueness criterion assumes a positive lower bound for singular values and a small L∞ pressure oscillation. It supplies neither an arbitrary compressible-data theorem nor a route to infer those bounds here.

## 5. Genuine determinant barriers still carry extra assumptions

Jonathan J. Bevan, *A Condition for the Hölder Regularity of Local Minimizers of a Nonlinear Elastic Energy in Two Dimensions*, DOI 10.1007/s00205-017-1104-5, full primary manuscript, introduction and Theorem 2 (PDF p.25), with energy (3.1), barrier (3.2) and twist functional (3.4):

https://d-nb.info/1129061833/34

The energy is planar, quadratic in gradient, with a logarithmic barrier near J=0 and linear determinant growth at infinity. The local continuity theorem assumes a positive-twist/star-shaped-image condition on the map; that condition is not deduced from arbitrary smooth full trace. It yields Hölder continuity of y, already available for E-6322 from W^{1,6}, rather than Hölder continuity of Dy.

The introduction also describes Foss's inverse-square-barrier partial regularity theorem as conditional on an extra relative equiintegrability property (REP), with p>8 in dimension two. That Foss theorem was not retrieved directly in this pass; no independent theorem-hypothesis verification of it is claimed. It cannot be used here by dropping REP or by reading equiintegrability from finite energy alone.

## 6. The inverse-square barrier in recent inverse-Sobolev results

Panas Kalayanamit, *Sobolev regularity of the inverse for minimizers of the neo-Hookean energy satisfying condition INV*, arXiv:2405.12156v2, 17 July 2024, §1 p.3 and Theorem 2.5 pp.12–13:

https://arxiv.org/pdf/2405.12156v2

The theorem's three-dimensional barrier threshold includes H(t)≥Ct^{-2}, but its setting is the |Du|²+H(J) neo-Hookean energy, thick boundary data, and a weak closure of homeomorphisms. The conclusion is the INV/divergence identities and a W^{1,1} inverse, not uniform Jacobian positivity. Its exponent 2 is a threshold for that inverse/topological closure mechanism; it must not be relabelled a positive-Jacobian threshold for the frozen full W^{1,6} class.

For E-6322 the simpler p>3 inverse theorem checked in the companion report already provides more precise quantitative inverse estimates without changing the comparison class.

## 7. Exact remaining bridge

The positive conclusion of this screen closes only the distinction between an algebraic inverse matrix field and a weak inverse derivative. It supplies no new gradient integrability above the energy coercivity for an arbitrary primal minimizer.

Pass 1's conditional pressure argument remains usable if a separate global C^{1,β} estimate is obtained. Merely obtaining every finite inverse-Jacobian moment without a modulus of continuity would still require an additional step for an essential lower bound. The new inverse formulation likewise still requires either bounded det Dv or a legitimate comparison/regularity theorem in its actual inverse-image class.

No inspected theorem supplies those missing hypotheses. In particular, no passage from full Sobolev competitors to a closure of diffeomorphisms, constrained symmetry class, or unconstrained inverse competitor class has been made.
