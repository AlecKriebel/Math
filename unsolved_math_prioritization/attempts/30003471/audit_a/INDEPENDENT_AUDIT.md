# Independent mathematical audit: three-dimensional dihedral comparison

Date: 2026-10-08 UTC. Target: 30003471 / OWR-15427-013, rank 999.

## Verdict and exact audited version

**PASS.** The complete proof establishes its stated strengthening for arbitrary combinatorially equivalent, compact, full-dimensional convex three-polytopes, including nonsimple vertices. I found no mathematical gap requiring correction. Its conclusion implies the exact OWR question. This acceptance is conditional only on the explicitly imported standard analytic foundations and Brendle's verified smooth-boundary propositions, as is ordinary for a proof using established theorems.

The audited `PROOF.md` is 21,855 bytes, SHA-256:

`6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415`.

The full frozen author packet contains ten files, including its manifest. Its `MANIFEST.json` SHA-256 is:

`1cd8291f2025524b351c5cc3cb5780b35ba5fa4c4afde78c6e288daddd350e9f`.

All nine payload entries were independently checked against that externally supplied manifest pin. The proof and author packet were not edited. Their original pending-audit status remains a historical property of the frozen candidate; this separate report supplies the mathematical audit decision.

This is a mathematical audit, not formal verification, journal acceptance, a priority determination, or a claim of exhaustive literature review. No other mathematical audit was used. No recent WXY or Bi theorem was used as a substitute for checking the candidate's argument.

## 1. Claim, quantifiers, and original target

The correspondence is a fixed face-lattice isomorphism. Consequently it identifies adjacent facet pairs and corresponding edges; no optimization over matchings is hidden in the statement. Actual facets, rather than redundant inequalities or coplanar subdivisions, are used.

The candidate proves that weak domination of all corresponding interior dihedral angles implies equality of the complete outward-normal Gram matrices. The OWR question only requires one corresponding weak inequality. If that conclusion failed, every source angle would be strictly greater than its target angle. Applying the candidate with the polytopes reversed would force equality, a contradiction. The equality alternative in the original question adds no additional case to the weak-inequality conclusion.

Full dimension and boundedness are used at identifiable points: an interior origin and positive support numbers, nondegenerate adjacent normal arcs, uniform radial parametrization, and spanning of the facet normals. The proof makes no assumption of simplicity or of a smooth face-preserving map at a nonsimple vertex.

## 2. Smooth Dirac input and matrix convention

The relevant statements were checked in Brendle's final author manuscript, arXiv:2301.05087v4, Section 2. Proposition 2.14 provides Fredholmness and smooth kernel; Proposition 2.15 supplies positive index for a smooth sphere-valued map homotopic to the Euclidean Gauss map on a compact smooth convex domain. Proposition 2.9 supplies the required energy bound. Strict convexity is not among these hypotheses, so the flat patches of the approximation are allowed. The matching-angle assumption belongs to Brendle's separate polytope theorem and is not a restriction on these propositions. Publication metadata were independently verified with the publisher. The publisher PDF itself was not inspected.

I separately checked the translation rather than identifying an array of spinors with a matrix informally. Let the columns of A be the spinors s_alpha in a fixed Cartesian spinor frame. With Brendle's coefficient convention, c(e_j)e_alpha = sum_beta omega[j,alpha,beta] e_beta. His boundary involution therefore sends A to -c(nu) A c(eta), since its alpha-th column is the corresponding sum over beta. Multiplication by c(nu) shows that the +1 eigenspace is precisely

    c(nu) A = A c(eta).

The same irreducible two-dimensional representation is used on both sides; c(e_j) = -i sigma_j has the required Clifford relations and volume convention. The Euclidean connection is the ordinary componentwise derivative, and the sum of squared spinor-column norms is the Hilbert-Schmidt squared norm of A. Thus there is no hidden transpose, conjugation, orientation reversal, multiplicity, or norm factor in the candidate's application.

For harmonic A satisfying this boundary condition, the boundary terms involving A-chi(A) vanish. Scalar curvature is zero. Replacing the remaining signed integrand by its positive part only weakens the inequality and gives (2.1), including its factor 1/2. Positive Fredholm index ensures a nonzero kernel element without a normalization or boundary metric assumption beyond those already stated.

## 3. Degree-one hemisphere data

The barycentric face-chain construction gives a compatible finite piecewise-linear boundary homeomorphism. Each closed source facet maps onto the corresponding target facet, including every incidence at a nonsimple vertex. Reflecting the target if necessary changes the boundary degree by a sign and preserves every normal inner product and dihedral angle. This legitimately reduces to degree +1.

After translation of an interior point to the origin, the radial target map has positive dot product with every incident target normal. The bound is uniform because all target support numbers are positive and the target is bounded. At a nonsimple source vertex, one and the same vector satisfies the positivity inequalities for all its incident facets; no choice of a preferred triple is made.

The radial extension to a collar is Lipschitz. A sufficiently close smooth approximation, followed by normalization, preserves a common positive margin. Compactness of the finitely many source facets supplies one neighborhood size valid for all facets. The normalized straight-line homotopy stays defined. The fixed smooth map q therefore has bounded derivatives on the compact subcollar used subsequently and has the required degree. It need not extend through the interior of P, and the analytic theorem does not require such an extension.

## 4. Convex approximation and uniform functional analysis

The proposed cutoff exists. Twice integrating the stated smooth function produces a nonnegative smooth convex function, flat on the inactive side, strictly increasing on the active side, and normalizable at zero. The level domains lie inside P, since a violated defining inequality alone gives a summand greater than one. They contain a common ball for all sufficiently large lambda.

Let R bound |x| on P and let h_* be the least source support number. For active indices at a boundary point and sufficiently large lambda,

    |sum_i a_i n_i| >= h_*/(2R) sum_i a_i,  a_i >= 0.

This follows by dotting with x. On the level set, the active cutoff arguments lie in [-2,0], their cutoff values sum to one, and their derivative sum has a positive lower bound by compactness. Thus the level gradient cannot vanish. The implicit-function theorem applies even at transitions to a flat patch. Convexity makes the second fundamental form positive semidefinite.

Contracting every boundary point a factor 1-O(1/lambda) toward the origin makes all defining inequalities at most -2/lambda. This proves the uniform radial displacement estimate. The radial maps and their inverses have uniformly bounded Lipschitz constants: for bodies between the same two balls, the reciprocal radial functions are uniformly positive Lipschitz support functions of their polar bodies. Their ratios give the required raywise maps. Their homogeneous extensions to all of R^3 remain uniformly bi-Lipschitz, including at zero.

The functional-analytic transport is valid. Compose a field on P_lambda with T_lambda to obtain a field on the fixed Lipschitz domain P. The H^1 norm changes by a uniform factor under a bi-Lipschitz map. Boundary surface measures change by uniformly bounded positive factors, by the area formula and the inverse Lipschitz bound. The fixed-domain H^1-to-L^4 trace inequality therefore gives (4.2) with a uniform constant. A fixed H^1 extension operator on P, followed by composition with T_lambda inverse, gives uniformly bounded extensions to a fixed ball. No uniform bound on curvature or on second derivatives of T_lambda is needed.

## 5. Active-facet localization, including nonsimple vertices

I checked the argument for (4.3), including the role of feasibility. If y is the closest point to x in the common face, v=x-y lies in its polyhedral normal cone. That cone is the sum of the span of equality normals and the cone generated by the other constraints active at y. Feasibility of x gives nonpositive pairing of v with those other active normals. If a limiting unit vector in this cone annihilated every equality normal, pairing its cone representation with itself would give a nonpositive squared norm, a contradiction. There are finitely many face types, so this gives a uniform constant for each fixed facet set. These cones are closed polyhedral cones, so taking the limiting unit vector is legitimate.

An empty common intersection has uniformly positive residual on compact P. Accordingly, for large lambda every active collection has a nonempty common face. Three distinct actual facets cannot share a ridge of a three-polytope. All collections of at least three active facets are therefore O(1/lambda) from a vertex. A pair that meets only at a vertex is excluded from the edge region by the same estimate. This checks both asserted uses of localization: the hemisphere margin for every active target normal and the reduction to an adjacent pair outside the vertex neighborhoods.

## 6. Edge contraction and smooth transitions

For two active adjacent facets, the outward normal lies on the minor arc between their normals. The interior-angle hypothesis becomes beta <= alpha for the corresponding target and source normal-arc lengths. Both lengths lie strictly between zero and pi. Fractional arclength, rather than a shared linear coefficient, is the correct contraction parameter.

The smoothed surface is locally invariant in the edge direction. Its nonnegative shape operator has rank at most one. Consequently the normal differential has trace norm H, and rescaling its arc parameter by beta/alpha gives

    ||d zeta||_tr = (beta/alpha) H <= H.

This statement includes points where the curvature is zero. At a one-active point, the level equation puts the surface exactly in the source facet plane and zeta is exactly the corresponding target normal.

The vanishing cutoff derivative is flat at the activation threshold. An angle coordinate defined by atan2 in the two-normal plane is smooth at either endpoint and proves smooth joining to the constant one-facet value. The construction is independent of the order of the two indices. Any competing pair configurations that genuinely require three nearby facets are localized at a vertex and excluded from the region where zeta is used. No singular differentiation of arccos at one is needed.

The sine coefficients of a minor-arc interpolant are positive and their sum is at least one. Thus q dot zeta retains the same positive lower bound as the two endpoint bounds. This is essential: it places the entire interpolation in a fixed hemisphere, rather than merely making an arbitrary global extension of normal data.

## 7. Vertex interpolation and critical boundary error

The scales are ordered correctly:

    lambda^(-1) = o(delta^2),  delta^2 = lambda^(-1/2),
    delta = lambda^(-1/4) -> 0.

Hence zeta is defined throughout every transition annulus, while the balls about distinct vertices are disjoint. Flatness of the logarithmic cutoff at both endpoints makes the piecewise definition of eta globally smooth. The core contains every potential multiple-facet singularity, regardless of vertex valence.

For fixed q, the spherical radial contraction z -> exp_q(t log_q z) has differential singular values t and sin(t theta)/sin(theta). On the verified range theta < pi/2, both are at most one. This range is not optional: it is what prevents expansion of the large edge derivative. The derivative with respect to q is uniformly bounded on the compact allowed parameter range, and the derivative with respect to t has length theta. The trace-norm ideal inequality and triangle inequality therefore yield the candidate's estimate with coefficient exactly one on ||d zeta||_tr. Differentiating r along the boundary introduces no extra factor larger than one.

Inside the inner ball, bounded dq and nonnegative H give bounded positive error. Outside the outer balls, the error vanishes. In the annuli, the error is bounded by a constant plus C/(r |log delta|). Pulling back to the polytope boundary changes the distances by O(1/lambda), which is negligible relative to delta^2, and changes area by a bounded factor. On each incident planar facet the squared weight has integral bounded by

    C |log delta|^(-2) integral_(c delta^2)^(C delta) dr/r
      <= C/|log delta|.

The indicator part has L^2 norm O(delta). Summing over the finite vertex and facet sets proves the actual-boundary L^2 estimate (6.4). This is not merely an estimate on an unsmoothed comparison surface or an appeal to small area.

Finally, Holder pairs W in L^2 with |A|^2 in L^2, and the uniform trace estimate controls the latter by the interior H^1 norm. This proves the needed quadratic-form estimate for every H^1 matrix field, with a coefficient tending to zero. The critical exponents are correct specifically in dimension three.

## 8. Homotopy, harmonic fields, and limiting mass

Every eta value remains in the hemisphere centered at q, so interpolation with q provides a global homotopy, including the core where eta=q. Its degree is therefore one. Radial projection between the two nested star-shaped boundaries preserves orientation. The outward Gauss map of the smooth convex approximation is homotopic to its radial map because its normal has positive dot product with the position vector; a common interior ball even gives a uniform positive support bound. The Gauss map also has degree one. Classification of maps from a sphere to itself now verifies the exact homotopy hypothesis of the smooth theorem.

The normalized nonzero harmonic matrix fields satisfy E_lambda <= o(1)(E_lambda+1), so E_lambda tends to zero after absorption. Uniform extension and Rellich provide a strong L^2 subsequential limit on a fixed ball. Every compact interior subset of P eventually lies in P_lambda, so the limit has zero weak gradient in the connected interior and is a constant C there.

The nonvanishing argument is complete. Strong L^2 convergence implies L^1 convergence of squared norms; the domain indicators converge almost everywhere. Their product integrals therefore converge to the integral on P. The normalization gives vol(P)|C|^2=1. No mass can disappear into a varying boundary layer, and no extension is assumed to be constant outside P.

For each facet, choose a fixed patch a positive distance from all its edges. In a sufficiently small interior half-ball touching that patch, every other facet inequality stays uniformly negative. For large lambda only the one cutoff can be nonzero there. Thus the smoothed domain contains the half-ball and its boundary agrees exactly with that facet on the flat disk. The vertex cutoff is already one on the disk. Strong L^2 convergence plus vanishing gradient energy yields strong H^1 convergence on this fixed half-ball. Continuity of its trace passes the boundary relation to C. This obtains c(n_i)C=Cc(m_i) separately for every actual facet without taking traces on a corner or using pointwise bounds on A_lambda.

## 9. Final algebra and scope

Taking adjoints of each intertwining equation yields C* c(n_i)=c(m_i) C*. Hence C*C commutes with every c(m_i). The target normals span R^3, because otherwise their common orthogonal direction would make Q unbounded. Irreducibility then makes C*C a positive scalar multiple of the identity; C is invertible. Applying the intertwining identities to both orders of a product and using the Clifford anticommutator proves equality of n_i dot n_j and m_i dot m_j for every pair, including nonadjacent facets.

The adjoint and cancellation steps are correct. In fact, for the Gram conclusion alone, cancellation of the scalar multiple of nonzero C would suffice, so this part is not vulnerable to an unnecessary invertibility assumption. Reflection in the initial orientation adjustment preserves the final Gram equality for the original target as well.

The result established by this proof concerns dihedral comparison and normal Gram data. It does not assert that all support numbers or edge lengths are fixed, and no such additional rigidity is needed for the original problem.

## 10. Source verification and limitations

The exact OWR problem was checked in text and a rendered page at printed page 1198, problem 4. Akopyan-Karasev Conjecture 5.1 was checked in text and a rendered page at printed page 5. The strengthened statement is appropriately distinguished from those formulations.

Brendle Section 2 was read through the relevant definitions, energy estimate, regularity theorem and positive-index proof. Local renderings of printed pages 3, 8, 10, 11 and 12 were visually checked. The official version-specific PDF and abstract page were opened independently; the publisher page confirms the journal, volume, pages and publication record. A web screenshot route failed, so visual inspection used the local pinned PDF instead. That tool limitation did not limit the source text or rendered-page inspection.

Local source witness metadata, independently recomputed:

- Brendle v4 PDF: 350,306 bytes; SHA-256 `f1f9f24fdad32e0f5fcb81ddacb14ee988afd50dc8cd325cf04b77cb6bd7d9ea`.
- OWR report PDF: 753,616 bytes; SHA-256 `47630a7d50e12e5ea3b88ef7dfaf6e7d6fc2f1d7c4fadf82785c97ff25dc5c0d`.
- Akopyan-Karasev v2 PDF: 128,195 bytes; SHA-256 `7a71f71a02b0d15058be8de0d9513f6f2835ae8743126aad41bb635a9e666918`.

The Bi and WXY current version-specific abstract pages were opened for the existence and qualification of the credited recent sources. Their full theorems are not analytic dependencies of this audit. No assertion that these recent manuscripts have been accepted by a journal is made. The author's repository-history and dataset duplicate-search ledger was read as background; its external historical searches were not independently repeated and are not part of this mathematical acceptance.

Public sources:

- [OWR report, printed page 1198](https://publications.mfo.de/bitstream/handle/mfo/3583/OWR_2017_19.pdf?isAllowed=y&sequence=1)
- [Akopyan-Karasev, version 2](https://arxiv.org/pdf/1505.05263v2)
- [Brendle, version 4](https://arxiv.org/pdf/2301.05087v4)
- [Brendle publisher record](https://link.springer.com/article/10.1007/s00222-023-01229-x)
- [Bi, version 1](https://arxiv.org/abs/2608.06320v1)
- [Wang-Xie-Yu, version 1](https://arxiv.org/abs/2606.30130v1)

## 11. Packet controls and final decision

The verifier and finite controls were inspected, then replayed in ordinary Python, -O, and -OO modes against the external manifest pin. Each run passed all 5,066 diagnostics, rejected all 19 negative cases, and passed the read-only relocation check. These tests verify finite algebraic diagnostics and fail-closed packaging behavior. Their own output correctly declines mathematical certification. They were not used to establish any Sobolev estimate, elliptic result, limiting argument, or universal geometric claim.

This audit contains authored mathematical analysis and public verification metadata only. It contains no source PDF, source extract, dataset record, or private coordination material. No mathematical patch is required. The frozen proof is accepted for the exact stated generality, with the usual imported-theorem dependencies and the qualification limits above.
