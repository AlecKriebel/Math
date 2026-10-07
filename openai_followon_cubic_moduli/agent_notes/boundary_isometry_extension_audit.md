# Boundary isometry and polarization audit

Checkpoint: 2026-10-06 22:43 PDT (2026-10-07 05:43 UTC). Estimated completion of this scoped audit: 95%. Publication novelty is not established. No outside individual was contacted, and no Git operation or publication operation was performed. This agent created only this original note.

## Verdict and scope

For normal klt KE cubic n-folds in the polarized GH closure of smooth KE cubics, n>=5, the extension and polarization steps have no unresolved mathematical obstruction identified here. Conditional on the independently checked high-Cartier-index consequence of Druel–Guenancia–Păun (DGP), every metric isometry is holomorphic or antiholomorphic, extends over the singularities, and preserves the cubic hyperplane line bundle in the appropriate conjugate complex structure. This is a deduction from established geometry, not an assertion of novelty or a complete independent verification of every cited foundational theorem.

The GH-limit hypothesis is used for the exact Donaldson–Sun metric/algebraic regular-locus identification. Do not silently cite that proposition for an arbitrary metric completion outside its stated limit-space setting. No completeness of the regular locus, simple connectedness of the regular locus, full U(n) holonomy, or uniqueness of arbitrary anticanonical roots is assumed.

## 1. A metric isometry acts smoothly on the regular locus

In the cached original [Donaldson–Sun II, arXiv:1507.05082v1](https://arxiv.org/abs/1507.05082), Proposition 2.14, printed pp.9–10, identifies the metric singular set with the complex analytic singular set. Section 2.1 specifies smooth KE geometry on the metric regular locus. Consequently an isometry F of two such limit spaces preserves their algebraic regular loci.

Smoothness is local. Near a regular point p, choose small relatively compact regular neighborhoods of p and F(p). On sufficiently small neighborhoods the completion's distance equals the local Riemannian distance: paths that leave the larger regular neighborhood have a fixed positive length cost, whereas sufficiently short local geodesics remain inside it. Choose nearby target points q_1,...,q_{2n} so that their distance functions are smooth local coordinates near F(p); choose them close enough that the corresponding source distances to F^{-1}(q_j) are also smooth. The identity

    d_Y(q_j,F(x)) = d_X(F^{-1}(q_j),x)

then expresses F in smooth coordinates. Its inverse is smooth by the same argument, and infinitesimal distances give F^*g_Y=g_X. This is the usual local Myers–Steenrod argument; it does not require the incomplete regular locus to have the same *global* intrinsic distance as its completion.

## 2. A pointwise curvature shortcut removes the reflexive-form input

Put I=F^*J_Y on X_reg. It is a parallel orthogonal real complex structure for g_X. Let J be the original complex structure. A parallel endomorphism commutes with every curvature operator:

    [I,R(u,v)] = 0.

For a Kähler metric and a real orthonormal frame e_a,Je_a, the Kähler curvature symmetries give

    S := sum_a R(e_a,Je_a) = - Ric^sharp o J

with the opposite overall sign under the opposite convention for R. Explicitly, set Z_a=(e_a-iJe_a)/sqrt(2). Then R(Z_a,conjugate(Z_a))=iR(e_a,Je_a), and the Kähler curvature symmetries identify sum_a R(Z_a,conjugate(Z_a)) on T^(1,0) with Ric^sharp=lambda*Id. Hence S=-i*lambda*Id on T^(1,0), and by reality S=+i*lambda*Id on T^(0,1), which is S=-lambda*J. Thus for a KE metric with lambda!=0, S is a nonzero scalar multiple of J. Since I commutes with S, it commutes with J.

An equivalent form-based check is that the (2,0) component of g(I.,.) is parallel. The curvature contraction on Lambda^p(T^(1,0))* is -p*lambda times the identity, up to sign convention, so a parallel (p,0)-form must vanish when lambda!=0. This is a pointwise curvature argument and uses no integration, boundedness, compactness, completeness, or global extension of differential forms.

The former reflexive-form route is also supported by exact primary statements: [Hacon–McKernan, arXiv:math/0504330v2](https://arxiv.org/pdf/math/0504330), Corollary 1.13, gives rational connectedness for projective klt pairs with big and nef negative log canonical divisor (Corollary 1.4 already gives rational chain connectedness in the Fano case); [GKKP](https://sites.math.washington.edu/~kovacs/current/papers/Greb_Kebekus_Kovacs_Peternell__Differential_forms_on_log_canonical_spaces.pdf), Theorem 5.1, gives vanishing of reflexive positive-degree forms on rationally chain connected klt spaces. The arXiv numbering of Hacon–McKernan differs from the published numbering quoted by GKKP. Neither result is necessary for the curvature shortcut.

## 3. The exact remaining algebraic input and use of stability

Since I commutes with J, I is a complex-linear parallel endomorphism of T_X on X_reg; it is holomorphic because the Levi-Civita connection of a Kähler metric is its Chern connection. The analytic tangent sheaf is reflexive on normal X. Its Hom sheaf is reflexive as well, so sections of End(T_X) extend uniquely across the codimension-at-least-two singular locus. The extension is algebraic by [Serre, GAGA](https://www.numdam.org/article/AIF_1956__6__1_0.pdf), Theorem 2, printed p.19, which algebraizes analytic homomorphisms of coherent algebraic sheaves on a projective variety.

One may work upstairs and avoid proving stability descends through a finite cover. [DGP, arXiv:2008.05352v1](https://arxiv.org/html/2008.05352), Theorem A, supplies a finite quasi-étale cover f:W->X with an algebraic and isometric product decomposition into klt KE Fano factors having stable tangent sheaves. The independent index argument must show that only one factor is possible when -K_X=rH with H Cartier ample and r>n/2+1. For cubics, r=n-1 satisfies this strictly for n>=5.

Pull back I on f^{-1}(X_reg), where f is étale. This is a big open subset of W; reflexivity extends the resulting holomorphic endomorphism to T_W, and GAGA algebraizes it. Its square is -Id because that equality holds on the big open set. Since T_W is stable, it admits no nontrivial direct-sum decomposition: if I has both eigenvalues +i and -i, its two polynomial eigenprojections give nonzero proper direct summands, and the weighted average of their slopes is mu(T_W), so they cannot both have slope strictly smaller than mu(T_W). Therefore I=+J or -J upstairs, hence downstairs on X_reg. This yields holomorphicity or antiholomorphicity of F there.

This section uses the high-index product exclusion as an explicit separately audited input, rather than assuming that a stable decomposition of the incomplete regular locus automatically integrates to a global product.

## 4. Extension of the isometry across the singularities

For the holomorphic case, fix p in X and a local analytic embedding of a neighborhood of F(p) in C^N. Continuity of F lets us shrink a neighborhood U of p so that F(U) stays in this chart. Every chart-coordinate function composed with F is continuous on U, holomorphic on U intersect X_reg, and locally bounded. Normality extends it holomorphically to U. The local defining equations of Y hold on the dense regular subset, hence hold on U. These coordinate extensions are precisely the existing continuous map F, so F is holomorphic everywhere. Applying the same argument to F^{-1} proves that F is biholomorphic.

The requisite locally bounded removable-singularity statement is explicitly used and proved for these limit charts in Donaldson–Sun II, Proposition 2.4 and its proof, printed pp.6–7. Algebraicity then follows from Serre GAGA, Proposition 15, printed p.29: a holomorphic map from a compact algebraic variety to an algebraic variety is regular. For the antiholomorphic case apply the same argument to F:X->conjugate(Y).

Continuity is essential here. A birational map holomorphic only on a big open set cannot be assumed to extend merely because X is normal; a flop is an immediate warning against that weakened assertion.

## 5. The hyperplane root is unique in the singular boundary scope

The original [SGA 2](https://wstein.org/sga/circle/SGA2.pdf), Exposé XII, Corollary 3.7, printed p.121 (zero-indexed PDF page 128), states that a global complete intersection in projective space of dimension at least three has Picard group freely generated by O_X(1). It has no nonsingularity hypothesis. Remark 3.8 expressly explains the removal of that hypothesis; invoking only the smooth topological Lefschetz theorem would leave a boundary gap.

Thus Pic(X)=Z[H_X] and Pic(Y)=Z[H_Y]. Adjunction gives -K_X=(n-1)H_X and -K_Y=(n-1)H_Y. A biholomorphic algebraic isomorphism preserves the canonical bundle, so

    (n-1)(F^*H_Y-H_X)=0.

The torsion-free Picard group gives F^*H_Y=H_X. An antiholomorphic map is treated as a holomorphic map to conjugate(Y), preserving the conjugate hyperplane bundle. No assumption about arbitrary Fano anticanonical roots is used.

The exact sequence for a cubic hypersurface shows h^0(X,H_X)=n+2 and the complete linear system gives its ambient embedding. Therefore a polarized isomorphism is induced by a projective linear transformation, including for singular normal cubics. This is the needed bridge from abstract algebraic isomorphism to equality of closed cubic GIT orbits.

## Adversarial checks and boundaries

- The curvature commutation step fails at lambda=0, as hyperkähler metrics illustrate. This does not affect positive KE cubics.
- Commutation alone does not give I=+J or -J. On P^(m-1) times P^(m-1), partial conjugation is an isometry with I=J_1 direct-sum (-J_2); both tangent eigenbundles are nonzero. Its Cartier index is m=n/2+1, exactly the equality excluded by the strict index hypothesis.
- Do not replace the Cartier H by a merely Q-Cartier root when applying the Hilbert-polynomial factor-dimension bound. That would destroy the integral negative twists used in vanishing.
- The regular locus need not be complete or simply connected. Neither condition entered the argument.
- Normality and continuity provide the map extension; codimension-two reflexivity provides the endomorphism extension. These are distinct steps and neither should be substituted for the other.
- No statement of first-public priority, a genuinely new proof mechanism, a quantitative GH-distance estimate, or a new publication candidate follows from this audit.

Strongest scoped conclusion: the proposed boundary metric-rigidity route has concrete exact-source justification for regular-locus preservation, local smoothness, complex-structure commutation, analytic/algebraic extension, and singular cubic polarization uniqueness, conditional on the separately verified high-Cartier-index product exclusion. No mathematical obstruction was identified in those steps.
