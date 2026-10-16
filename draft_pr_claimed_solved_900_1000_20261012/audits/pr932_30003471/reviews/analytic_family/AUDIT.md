# Independent analytic/Dirac/compactness audit: PR932 / problem 30003471

Audit date: 2026-10-15 UTC. Immutable candidate: Git `c09ef9df8b1f4642be0396ba6343344be8fa25b0`; proof SHA256 `6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415`. The original author record remains 1/5, and this audit adds zero author proof-search turns. All work is confined to this family's folder. No original file, index, checkout, branch, service, tracker or publication was changed. No outside person or other current family was contacted. No historical audit/acceptance verdict was read. `INITIAL_RECONSTRUCTION.md` was written before source checking and verdict formation.

## Verdict and exact scope

**Analytic family: PASS, with two optional exposition/provenance clarifications and no identified mathematical gap.** This is an independent mathematical audit within the assigned family, not a novelty, priority, journal-body, formal-verification or whole-project acceptance claim. The strongest checked conclusion is that the candidate's construction implies the full normal-Gram rigidity statement under precisely its stated full-dimensional bounded convex three-polytope hypotheses. In particular the exact OWR target follows by reversal of the ordered pair. No matching face metrics, vertex-smooth map, simple-vertex assumption, strict convexity, or uniform geometric nondegeneracy across varying polytopes was introduced.

The smooth Dirac specialization is verified against an actual pinned author v4 body. The publisher verifies the journal bibliography; its version-of-record body was unavailable in this audit. No assertion of byte equality or theorem-by-theorem identity between that body and v4 is made. The source's separate polytope theorem is not used.

## Primary body and page inspection

Primary body: Simon Brendle, [arXiv:2301.05087v4](https://arxiv.org/abs/2301.05087v4), revised 28 November 2023; [version-pinned PDF](https://arxiv.org/pdf/2301.05087v4), 40 pages, 350306 bytes, SHA256 `f1f9f24fdad32e0f5fcb81ddacb14ee988afd50dc8cd325cf04b77cb6bd7d9ea`. Actual local full-page PNG pixels for printed p.1 and pp.3-12 were viewed; this includes the definitions, proofs and hypotheses, not just theorem snippets. Per-page image hashes and sizes are recorded in `SOURCE_PINS.json`. Text extraction was supplementary.

The [publisher](https://link.springer.com/article/10.1007/s00222-023-01229-x) and [Crossref deposit](https://api.crossref.org/works/10.1007/s00222-023-01229-x) authenticate author/title, DOI `10.1007/s00222-023-01229-x`, Inventiones mathematicae 235(2), 669-708 (2024), online 29 November 2023 and February 2024 issue date. The advertised journal-PDF URL returned HTML at the subscription preview. The fulltext URL was inaccessible through the web tool. No journal mathematical body was inspected. Raw PDF, HTML, extractions and renders are private and excluded from this audit's curated public map.

Concise source assertions used: Section 2 concerns odd dimension and a compact smooth domain with a metric on a neighborhood. Definition 2.2 defines the tuple boundary involution; Definition 2.7 and Lemma 2.8 use the sum of singular values. Proposition 2.9 supplies the boundary energy estimate. Proposition 2.14 supplies Fredholmness and smooth kernel. Proposition 2.15 gives positive index for a convex smooth domain when the sphere map is homotopic to its Euclidean Gauss map. Its proof includes the Euclidean base case and index deformation. All subsequent calculations below are this audit's specialization and independent checks of those assertions.

## 1. Exact tuple-to-matrix translation and orientation

Choose the standard oriented Euclidean spin trivialization and the ordinary **column** matrices

\[
c_j=-i\sigma_j,\qquad c_j^*=-c_j,\qquad
c_jc_k+c_kc_j=-2\delta_{jk}I,\qquad c_1c_2c_3=-I.
\]

This satisfies the source's chosen spinor volume convention in dimension three because \(i^2c_1c_2c_3=I\). A tuple \(s=(s_1,s_2)\) is represented by the matrix \(A=[s_1\ s_2]\), with each column a spinor in this trivialization. Let \(\omega_{j\alpha\beta}\) be the source's coefficient array. Its explicit expansion on printed p.12 is

\[
c_j\widehat s_\alpha=\sum_\beta\omega_{j\alpha\beta}\widehat s_\beta.
\]

Thus \(\omega_j=c_j^T\) when the array is written as an ordinary row-indexed matrix. For the source's Definition 2.2, its alpha-th tuple component is exactly the alpha-th column of

\[
-c(\nu)A\omega(\eta)^T=-c(\nu)A c(\eta).
\]

Consequently \(\chi A=A\) is equivalent to \(c(\nu)A=A c(\eta)\), with precisely the same Clifford representation on both sides. No complex conjugate, dual representation, extra minus sign, target reflection, or unnoticed chirality swap is needed. Since the trivialization is Euclidean and parallel, the source Dirac operator is columnwise \(D A=\sum_jc_j\partial_jA\); the source tuple norm and connection norm are exactly the Hilbert-Schmidt norms \(|A|^2=\operatorname{tr}A^*A\) and \(|\nabla A|^2\).

A convention trap is material here. Under ordinary column matrix multiplication,

\[
\omega_1\omega_2\omega_3=(c_3c_2c_1)^T=+I,
\]

while the actual spinor matrices have product \(-I\). It is unsafe to copy a row-array volume identity into a column-action convention and then identify \(\omega=c\). If the printed omega-volume assertion on p.3 and the coefficient expansion on p.12 are both read with ordinary column-array multiplication, they have a sign discrepancy in dimension three. This audit does not use that printed omega-volume sign. Its needed index proof uses the nonzero scalar nature of the odd volume product, not its sign; the explicit spinor/right-action translation above and the independently reconstructed base-index argument below fix all signs that matter. More decisively, the explicit coefficient expansion and boundary formula above directly fix the translation. The executable exact controls find a one-complex-dimensional constant plus kernel with the correct translation, zero constant minus kernel, and **zero** constant plus kernel for the wrong untransposed \(\omega\) action. Thus the transpose concern was tested and resolved, not dismissed by naming the Pauli model.

For a round ball of radius \(R\) with \(\eta=\nu\), \(A=I\) is harmonic and \(-c(\nu)Ic(\nu)=I\). The mean curvature is \(H=2/R\), and \(\|d\nu\|_{\mathrm{tr}}=2/R\); energy and defect are zero. This fixes the sign of the selected eigenspace and the sum, rather than average, mean-curvature convention. A global change \(c\mapsto-c\) changes \(D\) by a harmless sign and leaves this boundary involution unchanged, but mixing the two inequivalent odd Clifford actions across the two sides would invalidate the argument.

## 2. Why the smooth analytic input applies

The exact operator is

\[
\mathcal L_\eta:H^1(\Omega,\operatorname{Mat}_2\mathbb C)
 \longrightarrow L^2(\Omega,\operatorname{Mat}_2\mathbb C)
 \oplus H^{1/2}(\Sigma,F^-_\eta),\qquad
 A\longmapsto(DA,A-\chi_\eta A),
\]

where \(F^-_\eta=\ker(I+\chi_\eta)\), \(\chi_\eta A=-c(\nu)Ac(\eta)\). Smoothness of \(\Sigma,\eta\) gives smooth boundary subbundles. Left and right Clifford multiplication commute; both are skew-adjoint, so \(\chi\) is self-adjoint and \(\chi^2=I\). For nonzero tangent covector/vector \(\xi\), the normal boundary symbol \(L=i c(\nu)c(\xi)\) acting on columns is self-adjoint, has square \(|\xi|^2I\), and anticommutes with \(\chi\). Therefore its positive eigenspace has dimension two and meets the plus eigenspace of \(\chi\) only at zero. The map \(I-\chi\) from decaying normal modes to \(F^-\) is injective between two-dimensional spaces, hence bijective. This independently checks the local elliptic mechanism behind Proposition 2.14. The imported elliptic regularity is that proposition's **smooth kernel up to the smooth boundary**; the audit does not replace it by an interior regularity assertion.

The index sign can be reconstructed without a singular-boundary index theorem. At \(\eta=\nu\) on the given smooth Euclidean convex domain, \(H=\|d\nu\|_{\mathrm{tr}}\), including flat points. The energy identity forces every harmonic plus solution to be constant. The Euclidean Gauss map is onto: maximizing \(x\mapsto v\cdot x\) over the compact convex domain produces outward normal \(v\) at a smooth support point. A constant plus solution commutes with every \(c(v)\), and hence is a scalar identity. Its space has complex dimension one. A smooth cokernel solution satisfies the opposite boundary condition, because \(c(\nu)\) commutes with \(\chi\); integration by parts gives the minus space. Applying the energy argument with \(-\eta\) again makes it constant. It must anticommute with every \(c(v)\), hence with \(c_1,c_2,c_3\). Their product is a nonzero scalar and the dimension is odd, so such a constant is zero. Thus the base index is actually one and in particular positive.

A smooth homotopy of \(\eta\) preserves this index. The changing boundary target bundles are no obstruction: with \(P_t=(I-\chi_t)/2\), the smooth unitary evolution generated by \([\dot P_t,P_t]\) identifies \(\operatorname{im}P_0\) with \(\operatorname{im}P_t\). This puts the Fredholm family in fixed spaces. Continuous sphere-map homotopies on compact smooth boundaries can be smoothed relative to their smooth endpoints. No metric homotopy is necessary in this Euclidean specialization. Positive index gives a nonzero kernel, and Proposition 2.14 makes that kernel smooth.

There is no missing positive-curvature or strictly-convex-domain hypothesis in the actual proposition statements. The metric is Euclidean on all of space; dimension three is odd and at least three; every approximation is compact, convex, smooth, and has interior. The sphere map need only be smooth and homotopic to the Euclidean Gauss map. It need not extend inside as a sphere map, be injective, be a Gauss map, be pointwise nonexpanding, preserve facet metrics, or match angles. The separate introduction's Matching Angle Hypothesis is not a Section 2 hypothesis.

For completeness, the energy inequality can also be checked in this matrix convention. The source's boundary endomorphism becomes

\[
\mathcal B A=\sum_{k=1}^2 c(e_k)A c(d\eta(e_k)).
\]

In singular-vector frames this is a sum of two unitary left/right Clifford products weighted by the nonnegative singular values of \(d\eta\). Its operator norm on Hilbert-Schmidt matrices is at most their sum. Using \(\chi A=A\) in the boundary Dirac anticommutation identity gives

\[
\int_\Omega|\nabla A|^2
=-\frac12\int_\Sigma\langle\mathcal BA,A\rangle
 -\frac12\int_\Sigma H|A|^2
\le\frac12\int_\Sigma(\|d\eta\|_{\mathrm{tr}}-H)|A|^2.
\]

Replacing the signed coefficient by its positive part only increases the right side. This is exactly (2.1), with no hidden dimension/rank factor. On the round ball, \(\mathcal BI=-(2/R)I\), another direct sign check.

## 3. Independent checks of the geometry needed by analysis

The fixed face correspondence supplies a boundary PL homeomorphism via face barycentric subdivisions. Reflection of the target if necessary changes its orientation degree without changing any normal Gram entries. Radial projection of the target boundary has degree one, and at every point of every closed corresponding facet its target-normal dot product is at least \(\min k_i/\max_Q|y|>0\). This is simultaneous at a nonsimple vertex. Smooth approximation on a fixed radial collar preserves a smaller positive margin for every nearby facet; finitely many compact facets give one neighborhood and one margin. All derivatives of the resulting fixed \(q\) are bounded on the smaller compact collar.

The cutoff domains do have smooth boundary. On \(F_\lambda=1\), arguments lie in \([-2,0]\) for active terms. Their derivative sum is bounded below by compactness and \(\Phi'>0\) wherever \(\Phi>0\). For every active facet, \(n_i\cdot x\ge h_{\min}/2\) for large \(\lambda\). Hence \(x\cdot\nabla F_\lambda\ge(h_{\min}/2)\lambda\sum\Phi'\), which rules out zero gradient. Convexity of \(\Phi\) makes the second fundamental form positive semidefinite. Where only one term is active, \(\Phi(\lambda u_i)=1=\Phi(0)\) forces \(u_i=0\); these are genuine flat facet patches.

The localization estimate is a finite polyhedral error bound, not an assumption about closeness of supporting planes. At a nearest point in a nonempty intersection face, its displacement is in the polyhedral normal cone. A sequence of normalized displacements annihilating the equality normals would also satisfy the remaining feasible directional inequalities. Pairing its equality-span/inequality-cone representation with itself gives a nonpositive squared norm, a contradiction. Finitely many face types give uniform constants for this fixed polytope. Empty intersections are excluded by a positive compactness minimum. In dimension three a ridge is in two facets; any intersection of at least three facets is a vertex. A two-facet intersection that is only a vertex is localized there as well. Thus the two-active-facet normal-arc construction is used only at actual edges outside the removed vertex neighborhoods.

For two active facets, the tangent edge direction annihilates both normals and is in the kernel of the Hessian restricted to the tangent plane. The nonnegative shape operator has rank at most one, so \(H=\|d\nu\|_{\mathrm{tr}}\). The normal runs along the minor source great-circle arc; shortening the fractional arclength parameter to its target arc multiplies its only nonzero derivative singular value by \(\beta/\alpha\le1\). Both arc lengths lie in \((0,\pi)\) for distinct actual adjacent facets of the stated bounded full-dimensional polytopes. The flat cutoff at the active threshold gives smooth endpoint jets, most cleanly in a local atan2 coordinate, not an arccos derivative. Charts for different pairs agree on their one-active overlaps; intersections needing more charts have already been localized at vertices.

The short target arc is a positive sine-weighted combination of its endpoint normals, with weight sum at least one. The simultaneous \(q\)-margin therefore implies \(q\cdot\zeta\ge c>0\). This is what prevents geodesic-interpolation singularities. It is a proved property, not an arbitrary extension of a contraction to the whole sphere.

A concrete nonsimple check is a square pyramid of height \(t>0\) over the square \((\pm1,\pm1,0)\), translated by \((0,0,t/3)\). Its four side normals are \((\pm t,0,1)/\sqrt{1+t^2}\) and \((0,\pm t,1)/\sqrt{1+t^2}\). All four meet at the apex; their dot product with the apex radial direction is \(1/\sqrt{1+t^2}>0\). Nonnegative active combinations cannot cancel. The four-active part is localized at scale \(1/\lambda\), strictly inside the cutoff core of radius \(\lambda^{-1/2}\). This verifies that the construction does not secretly triangulate or require a simple apex. As \(t\to0\) or \(t\to\infty\), some constants deteriorate; the theorem fixes each polytope first and makes no uniform assertion over those degenerate limits. A zero-height pyramid is excluded by full dimensionality.

## 4. Uniform trace and extension from radial maps

There are fixed radii \(0<r<R<\infty\) with \(B_r\subset P_\lambda\subset P\subset B_R\) for every sufficiently large \(\lambda\). For any convex body \(K\) between these balls, its gauge on the sphere is \(p_K(\omega)=1/\rho_K(\omega)=h_{K^\circ}(\omega)\). Since \(K^\circ\subset B_{1/r}\), this support function has Lipschitz constant at most \(1/r\), and its values are between \(1/R\) and \(1/r\). Reciprocals and ratios thus have uniform positive bounds and Lipschitz constants. Consequently

\[
T_\lambda(x)=\frac{\rho_{P_\lambda}(x/|x|)}{\rho_P(x/|x|)}x
\]

and its inverse extend to all of \(\mathbb R^3\) as uniformly bi-Lipschitz maps. At the origin they are continuous and the possible exceptional derivative is irrelevant to Sobolev transport. The radial inward displacement \(O(1/\lambda)\) follows by making every \(u_i\le-2/\lambda\). This gives uniform convergence \(T_\lambda\to I\) on \(P\).

For \(a\in H^1(P_\lambda)\), set \(\widetilde a=a\circ T_\lambda\) on \(P\). Change of variables, a.e. chain rules and uniform Jacobian bounds give \(\|\widetilde a\|_{H^1(P)}\le C\|a\|_{H^1(P_\lambda)}\). The area formula bounds the two-dimensional boundary Jacobians above and below. The fixed polytope is a bounded Lipschitz domain, so its trace inequality transports to

\[
\|a\|_{L^4(\Sigma_\lambda)}^2\le
C(\|\nabla a\|_{L^2(P_\lambda)}^2+\|a\|_{L^2(P_\lambda)}^2),
\]

with \(C\) independent of \(\lambda\). This also holds for the finite matrix components, or by the Sobolev norm inequality for \(|A|\). There is no curvature bound in this argument. Curvatures can and do diverge near edges.

If \(E_P\) is a fixed bounded Lipschitz-domain extension, then

\[
B_\lambda=\big[E_P(a\circ T_\lambda)\big]\circ T_\lambda^{-1}
\]

is an extension of \(a\) to space, with uniformly bounded \(H^1\) norm on a fixed ball containing \(P\). The global radial maps make the last composition legitimate. The same fixed ball suffices for Rellich. No nonexistent curvature-uniform smooth-domain extension theorem is being assumed.

## 5. Exact nuclear-norm chain rule and logarithmic error

Let \(G(q,z,t)=\exp_q(t\log_qz)\), with \(q\cdot z\ge c>0\). At fixed \(q\), its derivative in \(z\) has singular values \(t\) and \(\sin(t\theta)/\sin\theta\), \(\theta=\operatorname{dist}(q,z)<\pi/2\). Both are at most one for \(0\le t\le1\). The derivative in \(q\) is bounded on this compact range, including the removable polar-coordinate diagonal \(q=z\), and \(|\partial_tG|=\theta\le\pi/2\). The ideal norm property \(\|LM\|_{\mathrm{tr}}\le\|L\|_{\mathrm{op}}\|M\|_{\mathrm{tr}}\), followed by its triangle inequality, therefore gives

\[
\|d\eta\|_{\mathrm{tr}}\le \|d\zeta\|_{\mathrm{tr}}+C+C|dt|.
\]

The rank-one \(dt\) term has nuclear norm equal to its length product. There is no factor greater than one multiplying \(\|d\zeta\|\), which would have destroyed the argument near edges.

Choose \(\delta=\lambda^{-1/4}\). Then the core radius \(\delta^2=\lambda^{-1/2}\) is much larger than the vertex-localization scale, so \(\zeta\) is defined everywhere it is used in the transition annuli. Smooth flat-ended logarithmic cutoffs have \(|dt|\le C/(r|\log\delta|)\). Inside the core \(\eta=q\), so convexity and bounded \(dq\) give \(W\le C\). Outside the outer cutoff, \(\eta=\zeta\) and \(W=0\). All joins are smooth because the cutoffs have constant endpoint jets.

On the actual smoothed surface, pullback by the radial boundary map changes distances by \(O(1/\lambda)=o(\delta^2)\) and area by a uniformly bounded factor. Hence the pulled-back annular weight is bounded by \(C/(r|\log\delta|)\) on \(c\delta^2<r<C\delta\) on facets incident to the vertex. On each planar sector of angle \(\gamma\le2\pi\), its squared integral is

\[
\frac{\gamma}{|\log\delta|^2}
\int_{c\delta^2}^{C\delta}\frac{dr}{r}
=O(|\log\delta|^{-1}).
\]

The indicator's squared integral is \(O(\delta^2)\). Finite facets and vertices give exactly

\[
\|W_\lambda\|_{L^2(\Sigma_\lambda)}
\le C(\delta+|\log\delta|^{-1/2})\longrightarrow0.
\]

This uses the actual boundary measure. Small volume alone would not suffice. Holder with exponents two and two, plus the uniform trace, gives

\[
\int_{\Sigma_\lambda}W_\lambda|A|^2
\le\|W_\lambda\|_2\|A\|_4^2
\le C\varepsilon_\lambda(\|\nabla A\|_2^2+\|A\|_2^2).
\]

The critical matching \(H^1(3\text{-volume})\to L^4(2\text{-boundary})\) and \(W\in L^2\) is dimension-specific. Nothing here proves the all-dimensional analogue.

## 6. Homotopy, normalization, compactness and no mass loss

The hemisphere condition gives a global homotopy from \(\eta_\lambda\) to \(q\) on each boundary, including the core where they are equal. Restriction of the fixed collar homotopy and radial projection shows \(\deg q|_{\Sigma_\lambda}=1\). A smooth convex boundary enclosing the fixed inner ball has \(\nu(x)\cdot x\ge r>0\). Normalized straight interpolation between its normal and radial map is everywhere defined, hence its Gauss map has degree one even with flat patches. Since \(\Sigma_\lambda\) is a sphere, equality of degrees supplies the required homotopy class. Reflection was applied to the target once at the start, so orientation is consistent.

Normalize each nonzero smooth kernel matrix by \(\int_{P_\lambda}|A_\lambda|^2=1\). The energy and form estimates give

\[
E_\lambda\le C\varepsilon_\lambda(E_\lambda+1),\qquad
E_\lambda\le\frac{C\varepsilon_\lambda}{1-C\varepsilon_\lambda}\to0.
\]

Uniform extensions \(B_\lambda\) are bounded in \(H^1\) on a fixed ball. A subsequence converges strongly in \(L^2\) and weakly in \(H^1\) to \(B\). Every compact subset of \(\operatorname{int}P\) is eventually inside \(P_\lambda\); the extension equals \(A_\lambda\) there and its gradient tends to zero. Thus \(B=C\), a single constant matrix, on the connected interior.

For every interior point all cutoff arguments eventually fall below \(-2\), so it is eventually in \(P_\lambda\); exterior points are never in \(P_\lambda\). The boundary of a polytope has zero three-dimensional measure. Thus \(1_{P_\lambda}\to1_P\) a.e. Strong \(L^2\) yields

\[
\big\||B_\lambda|^2-|B|^2\big\|_1
\le(\|B_\lambda\|_2+\|B\|_2)\|B_\lambda-B\|_2\to0.
\]

It follows by splitting the difference and dominated convergence that

\[
1=\lim\int1_{P_\lambda}|B_\lambda|^2
=\int1_P|B|^2=\operatorname{vol}(P)|C|^2.
\]

This is a complete no-boundary-layer-mass-loss argument. Weak \(H^1\) convergence alone would not have established nonvanishing, but the strong \(L^2\) extension convergence does. No pointwise control of \(A_\lambda\) or extension gradients outside \(P\) is needed.

## 7. Fixed facet traces and Clifford closure

Choose a point in the relative interior of a facet and a small fixed half-ball on its interior side. Shrink it until all other facet inequalities have a fixed negative margin on its closure. For large \(\lambda\), only this facet is active near its flat disk; \(\Phi(\lambda u_i)\le1\) throughout the half-ball, so the entire half-ball is in \(P_\lambda\). Its disk is an unchanged patch of \(\Sigma_\lambda\). The shrinking vertex balls are eventually disjoint from it and \(\eta_\lambda=m_i\) there.

On the half-ball, strong \(L^2\) convergence plus \(E_\lambda\to0\) gives strong \(H^1\) convergence to \(C\). The fixed half-ball trace map is continuous into \(L^2\) (indeed \(H^{1/2}\)). Passing the smooth boundary identity on this disk therefore gives

\[
c(n_i)C=Cc(m_i)\quad\text{for every facet }i.
\]

Taking adjoints with skew-adjoint Clifford matrices gives \(C^*c(n_i)=c(m_i)C^*\). Hence \(C^*C\) commutes with each \(c(m_i)\). The target normals span \(\mathbb R^3\): otherwise any vector orthogonal to all of them would be a lineality direction of the bounded intersection of halfspaces. Thus \(C^*C\) commutes with every Pauli matrix, whose joint commutant is the scalar matrices. Positivity and nonvanishing yield \(C^*C=aI\), \(a=1/(2\operatorname{vol}P)>0\), so \(C\) is invertible. No rank-one escape is possible.

Anticommuting each pair of facet relations gives

\[
-2(n_i\cdot n_j)C=-2(m_i\cdot m_j)C.
\]

Cancellation proves all normal Gram entries equal. In fact nonzero \(C\) already suffices for this last scalar cancellation; invertibility is a stronger checked conclusion. No adjacency assumption is needed in this last step. If the original ordered pair had all strict inequalities in the opposite direction, reversing it would meet weak dominance and yield equality, a contradiction. The stronger assertion therefore proves the exact target, even though it does not assert congruence of the polytopes themselves.

## 8. Executed controls, issues and limitations

`analytic_checks.py` was executed using the existing shared Python runtime, without installing anything. `CHECK_RESULTS.json` records exact SymPy checks of the Clifford relations, correct and incorrect row/column volume signs, plus/minus constant kernel dimensions, ball identity, self-adjoint involution, boundary-symbol anticommutation and zero stable/plus intersection, the nuclear bound in a model with singular values 2 and 3, and the exact logarithmic annulus integral. All expected controls passed. These finite controls are checks on algebra and formulas, not numerical proofs of the index, Sobolev transport or compactness statements. Those statements were checked by the derivations and the explicit primary input above.

Required mathematical issues: **none identified**. Exact remaining mathematical gap in this family's reconstruction: **none identified**, relative to the explicitly imported smooth elliptic/Fredholm theory and standard bounded-Lipschitz Sobolev/extension and Rellich foundations. No route is marked blocked: no link has merely assumed an equivalent polyhedral angle theorem.

Optional issues:

1. Add the explicit coefficient relation \(\omega_j^T=c_j\) when explaining the source-to-matrix translation. In odd dimension this guards against a real chirality/sign mistake; do not rely on the printed omega-volume sign as a column-array identity. The candidate's final displayed matrix equation is correct; this audit resolves the omitted coordinate detail.
2. State plainly that the actual mathematical body inspected was author arXiv v4, with journal metadata separately verified. The version-of-record PDF was unavailable here. This provenance limit does not invalidate the v4-based proof, but the audit cannot certify the uninspected journal body.

Limits: this family did not investigate novelty or current literature status; did not use the Bi or Wang-Xie-Yu preprints to establish any link; did not verify the full underlying textbook foundations from first principles; did not prove a theorem in dimensions other than three or for unbounded, lower-dimensional or degenerate limiting bodies; and did not claim formal proof verification. The immutable candidate's original bytes were authenticated at the start and end against actual Git blobs and root record pins. Public-map verification and its externally reported digest cover only this audit family's curated artifacts, with raw primary bodies and rendering caches excluded.
