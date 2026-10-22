# PR932 / 30003471: independent source, model and adversarial audit

## Verdict and scope

**The exact three-dimensional target is aligned with the primary sources. The original candidate's mathematical route passes this independent source/model audit, using the explicitly pinned Brendle v4 smooth-domain propositions and ordinary Sobolev/elliptic foundations. No unresolved mathematical gap was found.** This is a human-checkable mathematical audit, not formal verification, an independent priority certificate, or a claim that the current journal body was accessible.

The publication record of Brendle's article is verified, but equality of the inspected author manuscript with the subscription journal main text was not verified. That access/version limit is distinct from the mathematical scope of the actually inspected manuscript. Recent Bi and Wang-Xie-Yu claims are not dependencies of the checked deduction and are deferred to the separate priority stage.

Original author proof-search record: **1/5**. This family adds **0** author proof-search turns. All work verifies and explicates the existing route. No substantively new approach was attempted. No outside person, other shard or other current agent was contacted. No original file, Git index, branch, service, tracker or publication state was changed. No historical audit/acceptance verdict or other current family's report was read.

## Immutable object and independent chronology

The audited immutable head is `c09ef9df8b1f4642be0396ba6343344be8fa25b0`. The selected actual Git program is `unsolved_math_prioritization/attempts/30003471`; it contains **29 blobs**. `ORIGINAL_AUTH_START.json` and `ORIGINAL_AUTH_END.json` compare every selected Git blob with its provided disk copy. Both report complete byte equality. This is authentication against actual Git objects, not trust in a supplied digest table.

The original proof has **21855 bytes**, SHA256 `6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415`, independently obtained from both actual Git and copied disk. The supplied outer-manifest anchor is `d1b3a0528bf518640a117c2cfecff5bc81d21f58632f7b4f647ae998eb4dcedd`; the root audit owns that outer artifact. This family does not claim to have reauthenticated unrelated outer contents.

The complete charter, private cached statement and original proof were read first. `INITIAL_RECONSTRUCTION.md` was written before primary-source conclusions and before any historical verdict. The public audit includes only the reconstruction, independent analysis, controlled diagnostics, authentication records and source metadata; downloaded bodies, text extracts, response headers and page renders remain under excluded `private/`.

## Exact problem model

Write a bounded, full-dimensional convex three-polytope as an intersection of its actual facet half-spaces. Each actual facet appears once. Fix an arbitrary face-lattice isomorphism between P and Q, hence a fixed correspondence of facets and edges. A ridge in dimension three is an edge and is incident to exactly two facets. Nonsimple vertices, with four or more incident facets, remain in scope.

Let `theta_P(e), theta_Q(e)` be the **interior** dihedral angles at corresponding edges. Each is strictly between zero and pi. If n_i,n_j are the outward unit normals of adjacent source facets, then

    alpha_ij = arccos(n_i . n_j) = pi - theta_P(i,j).

This is seen in a transverse planar wedge: rotating from one outward normal to the other uses the supplement of the interior wedge angle. The target normals m_i,m_j obey the corresponding identity with beta and theta_Q.

The source question is

    for every such ordered pair and fixed correspondence,
    there exists e with theta_P(e) <= theta_Q(e).

The additional all-equal alternative in OWR has no effect: equality at all edges already supplies an edge satisfying the weak inequality. Its precise negation is **strict** `theta_P(e) > theta_Q(e)` at every corresponding edge. Weak first-greater-or-equal with some equality is not this negation.

The candidate proves the stronger implication

    [theta_P(e) <= theta_Q(e) for every corresponding edge]
        => [n_i . n_j = m_i . m_j for all facet pairs i,j].

All-pair equality includes pairs whose facets do not meet. Applying that implication to the reversed ordered pair of a purported strict counterexample forces equality at its edges, a contradiction. The reduction is correct. The strengthening is not equivalent to the original question, and it does not claim congruence of support offsets or face metrics. Distinct rectangular boxes already illustrate why equal normal Gram matrices do not imply congruent polytopes.

The source wording does not separately spell out full dimension; its three-dimensional dihedral-angle question presupposes that ordinary interpretation. A polytope is bounded by the usual definition. Unbounded polyhedra, flattened bodies, redundant inequalities counted as facets, and nonconvex realizations are not being silently added.

## Primary problem provenance and date resolution

The [MFO report](https://publications.mfo.de/bitstream/handle/mfo/3583/OWR_2017_19.pdf?isAllowed=y&sequence=1) was downloaded independently and its cover and actual **printed page 1198** (PDF page 64) were rendered and viewed. Problem **4**, attributed there to Akopyan, is precisely the three-dimensional corresponding-edge comparison described above. The cached problem statement preserves its mathematical direction and weak inequality. No source email address was used or retained in the curated analysis.

The [official EMS article](https://ems.press/journals/owr/articles/15427) gives the citation **Oberwolfach Reports 14 (2017), no. 2, 1135-1205**, DOI **10.4171/OWR/2017/19**, and separately records **28 April 2018** as publication date. The report cover states workshop dates 9-15 April 2017. Thus volume/report year 2017 and publication year 2018 are compatible; choosing one from third-party metadata was unnecessary. The cached short citation should retain both roles if later edited.

The complete [Akopyan-Karasev v2](https://arxiv.org/abs/1505.05263v2) text was read, and printed pages **1, 3, 4 and 5** were rendered and viewed. Conjecture **5.1** asks the corresponding codimension-two-face comparison in **R^d**. The immediately preceding context fixes numbered vertices for the simplex comparison and then passes to combinatorial correspondence. It reports the simplex case with reference [10]. This audit does not reverify that cited simplex paper or use it as a novelty/current-openness certificate. The surrounding usage and convex wedge convention are interior angles. The v2 conjecture has the weak inequality and no extra equality alternative. The current candidate addresses its d=3 specialization, not every dimension.

Source file pins are independently computed:

| Download | Bytes | SHA256 |
| --- | ---: | --- |
| MFO OWR report | 753616 | `47630a7d50e12e5ea3b88ef7dfaf6e7d6fc2f1d7c4fadf82785c97ff25dc5c0d` |
| Akopyan-Karasev 1505.05263v2 | 128195 | `7a71f71a02b0d15058be8de0d9513f6f2835ae8743126aad41bb635a9e666918` |
| Brendle 2301.05087v4 | 350306 | `f1f9f24fdad32e0f5fcb81ddacb14ee988afd50dc8cd325cf04b77cb6bd7d9ea` |

`SOURCE_RECORDS.json` records URLs, versions, local private-body hashes and hashes of the exact page images actually viewed. No page-image existence alone is being counted as inspection.

## Analytic source: what was actually established

The [arXiv v4 primary record](https://arxiv.org/abs/2301.05087v4) identifies a revision dated **28 November 2023** and labels it the final version intended for Inventiones. The independently downloaded 40-page PDF was inspected directly. Actual printed pages **1-12** were rendered and viewed, including the distinction between the introductory polytope theorem and Section 2's smooth-domain setup. The definitions and material formulas were checked from pixels, not only text extraction.

The following compact source synopsis identifies the imported content. Section 2 uses odd dimension at least three, a smooth compact domain, and a metric on a neighborhood. Definition 2.2 supplies the boundary involution. Definition 2.7 and Lemma 2.8 use the sum of singular values for the boundary derivative norm. Proposition 2.9 gives the integrated spinor energy inequality. Proposition 2.14 makes the boundary problem Fredholm with smooth kernel. Proposition 2.15 adds convexity and homotopy of the sphere map to the Euclidean Gauss map and gives index at least one. The introductory polytope matching-angle hypothesis does not occur in these smooth-domain propositions. Neither strict convexity nor a polyhedral face map is required there.

The [Springer primary article record](https://link.springer.com/article/10.1007/s00222-023-01229-x) confirms **Simon Brendle, Inventiones mathematicae 235 (2024), 669-708**, DOI **10.1007/s00222-023-01229-x**; acceptance 25 October 2023, online/version-of-record date 29 November 2023, and February 2024 issue. Its accessible page is a subscription preview. The direct content-PDF request returned HTML despite HTTP 200. Accordingly, the **current journal main text was not read or compared**. Available appendix text does not establish main-text identity. The candidate's specialized input is authenticated in the pinned final author manuscript; journal-body equivalence remains a separate access limit.

### Independent matrix translation

This derivation fixes a potentially consequential transpose. Let gamma_j be the ordinary column-coordinate matrix of Clifford multiplication by e_j on the fixed spinor basis. The source's displayed basis expansion on printed page 12 is

    rho_hat(e_j) shat_alpha = sum_beta omega_j[alpha,beta] shat_beta.

Therefore `gamma_j[beta,alpha] = omega_j[alpha,beta]`, or `gamma_j = omega_j^T`. Put the spinors s_alpha in the **columns** of a matrix A. Directly applying Definition 2.2 gives

    chi(A) = -gamma(nu) A omega(eta)^T
           = -gamma(nu) A gamma(eta).

Consequently `chi(A)=A` is exactly

    gamma(nu) A = A gamma(eta),

because gamma(nu)^2=-I. The Dirac operator acts on each column. The tuple norm is exactly the Hilbert-Schmidt norm. No additional complex conjugation, transpose of A, or reversal of eta is necessary.

One may take `c(e_j)=-i sigma_j` on both sides. These matrices are skew-adjoint, satisfy the Clifford relation, and have `c(e_1)c(e_2)c(e_3)=-I`. The exact standard-library diagnostic `convention_controls.py` checks the full coefficient-to-column formula for all 9 coordinate choices and 4 matrix basis elements, plus the involution, Gauss identity kernel and commutant dimensions. A naive right multiplication by omega without its transpose fails already for the second Pauli axis. These finite controls expose an index/convention error if one is made; they do not prove elliptic theory.

There is a **harmless source ordering-sign caveat**: under the ordinary row-coefficient convention just displayed, `omega_1 omega_2 omega_3=+I` in this Pauli example, opposite to the column product. The normalized ordered-volume sentence for omega on printed page 3 should not be transferred literally under this coordinate convention. Transposition reverses three factors and contributes a minus sign. All required Clifford relations still hold. Lemma 2.1 and the index argument require only that the odd ordered volume is a nonzero scalar, which holds with either sign. The boundary condition, energy inequality, ellipticity argument and index positivity do not use the disputed scalar sign. Thus this is a resolved convention note, not a missing theorem premise or a new rigidity mechanism.

### Independent energy and index-sign checks

For the present Euclidean three-dimensional domain, scalar curvature is zero and spin connection is the ordinary derivative. In the positive boundary kernel, the two terms containing `s-chi(s)` in Proposition 2.9 vanish. Thus

    integral_Omega |grad A|^2
      <= (1/2) integral_Sigma (||d eta||_tr-H) |A|^2
      <= (1/2) integral_Sigma (||d eta||_tr-H)_+ |A|^2.

This establishes exactly the sign, factor and norm needed by the candidate. H is the sum of principal curvatures for the outward normal, positive on a round sphere. For a convex smooth boundary, including flat patches, `H=||d nu||_tr`.

The positive index has the needed sign: at eta=nu the constant matrix I satisfies `chi(I)=-c(nu)^2=I`. For the adjoint/cokernel boundary condition the sign is negative. The Gauss-case energy estimate forces that solution to be constant. A constant C with `c(nu)C=-C c(nu)` for every boundary normal anticommutes with all three generators because the Gauss map of a smooth compact convex body is onto. Its odd Clifford volume is a nonzero scalar, so anticommutation with that product forces C=0. This is the elementary algebra behind the zero cokernel in the source proof. Ellipticity, regularity and deformation invariance remain imported foundations, rather than falsely represented as finite-dimensional computations.

Convex smooth boundaries enclosing a fixed ball may have flat patches; surjectivity of their Gauss map follows by maximizing each linear functional and using smoothness at a maximizer. Strict convexity is unnecessary. Positive index of the full Fredholm operator implies a nonzero kernel. Proposition 2.14 then supplies smoothness through the boundary. This supplies a nonzero smooth matrix for each approximating domain, without assuming the final polyhedral theorem.

## Independent check of every original bridge

### Fixed correspondence, orientation and simultaneous hemispheres

For each proper nonempty face choose an interior point; coning its subdivided boundary to that point triangulates the face. Chains of nested faces give compatible barycentric subdivisions. A fixed face-lattice isomorphism sends each simplex to its corresponding simplex affinely. It gives a finite piecewise affine boundary homeomorphism f, hence a bi-Lipschitz map; its differentiability at vertices is neither asserted nor needed.

Orient each boundary by the ambient orientation and its outward normal. Its radial projection to S^2 has degree +1 because the origin is inside. The degree of f is either +1 or -1. In the latter case, reflecting the entire Q reverses boundary degree. The reflected normals have exactly the same pairwise Gram matrix and dihedral angles. The original fixed labels are retained. Thus reflection is a change of realization by an isometry, not a new matching chosen to evade the fixed correspondence.

After translating interior points to zero, `q0(x)=f(x)/|f(x)|` has degree +1. If x lies in F_i, then f(x) lies in its corresponding closed facet G_i and

    q0(x) . m_i = k_i/|f(x)| >= min_i(k_i)/max_Q|y| > 0.

This is simultaneous for **every** incident facet, also at a nonsimple vertex. The common margin comes from a supporting-plane identity, not an arbitrary selection of edge maps. A radial collar extension is Lipschitz. Uniform smooth approximation in a compact smaller collar, followed by normalization, preserves a positive margin in uniform neighborhoods of all finitely many facets. The normalized straight interpolation provides the homotopy to q0. No target metric is pulled back and no smooth vertex equivalence is assumed.

### Smooth domains, uniform constants and active sets

The candidate's flat cutoff Phi has positive first derivative after -2, is convex and smooth, and has Phi(0)=1. The function `sum_i Phi(lambda u_i)` is convex. Its level-one domain lies inside P and contains a fixed ball for large lambda. On that boundary at least one Phi value is uniformly bounded below; its derivative therefore is bounded below. The active normal combination cannot vanish, since every active n_i has a uniformly positive dot product with the boundary position vector. This proves the claimed gradient lower bound and smoothness, including one-facet flat patches.

Moving any boundary point radially inward by C/lambda kills every cutoff term. Hence the radial boundary displacement is O(1/lambda). For convex bodies uniformly between two concentric balls, the reciprocal radial function is the polar support function on the sphere. Its uniform positive lower bound and Lipschitz bound imply uniform bi-Lipschitz constants for the radial transports and their homogeneous extensions to all of R^3. Transport of the fixed-domain H1-to-L4 trace estimate, with the area formula for the boundary map, gives the candidate's uniform trace estimate. Composing a fixed Lipschitz-domain extension with these maps likewise gives a uniformly bounded extension to one ambient ball. No convergence of derivatives of the transports to identity is needed.

The affine error bound for the actual common facet face is valid. To verify its stated cone argument, fix the face type of a nearest point y in the common intersection. The displacement x-y lies in its polyhedral normal cone and satisfies every other active feasible inequality. A hypothetical limiting unit direction w annihilating the equality normals would be both in that cone and feasible to first order; pairing its cone representation with w gives `|w|^2<=0`. There are finitely many face types. Empty common intersections are excluded uniformly by compactness. Thus any at-least-three-active set is O(1/lambda) from a vertex. Two nonadjacent facets sharing only a vertex are covered by the same exclusion. This explicitly handles nonsimple vertices and does not assume every pair of facets is adjacent.

### Edge contraction and gluing

Outside those vertex neighborhoods only one or two facets are active. In a two-facet region the source Gauss normal is a positive normalized combination of the two source normals, hence lies on their minor spherical arc. Both source and target arc lengths lie in (0,pi). The interior-angle assumption gives `beta<=alpha`, the correct direction. Fractional arc-length correspondence has derivative ratio beta/alpha. The surface has a straight edge direction in the kernel of its second fundamental form, so its normal differential has rank at most one and trace norm H. Consequently `||d zeta||_tr=(beta/alpha)H<=H` exactly. Curvature-zero points are included.

The fractional arc coordinate is smooth near either endpoint using an oriented planar angle coordinate, rather than differentiating arccos at one. Flatness of Phi' at its zero endpoint makes the pair definition match the adjacent constant facet definition to all orders. Pair charts are order-independent. Distinct pair charts cannot disagree except near an excluded multi-active vertex or at the common constant one-active value.

The target minor arc is a positive sine-weighted sum of its endpoints. The weights sum to `cos((1/2-s)beta)/cos(beta/2)>=1`. The auxiliary q therefore has positive dot product, with a uniform fixed-pair margin, against zeta. This is the simultaneous compatibility needed for vertex interpolation.

### Cutoff estimate on the actual boundary

For `delta=lambda^(-1/4)`, the inner cutoff radius delta^2 is much larger than 1/lambda. The outer radius tends to zero and distinct vertex balls become disjoint. Therefore the edge construction is defined on the entire transition annulus, including for nonsimple vertices.

With `theta=dist(q,zeta)<pi/2`, the derivative of geodesic interpolation with respect to its second endpoint has singular values t and `sin(t theta)/sin(theta)`, both at most one. Its first-endpoint derivative is bounded on the compact margin range; its t derivative is bounded as well. The trace norm ideal property and triangle inequality give precisely the claimed excess bound by a bounded term plus `C/(r|log delta|)` in the annulus. Inside the inner ball eta=q and its excess is bounded. Flat radial cutoffs supply smooth gluing; no limiting vertex trace is required.

Pulling back to the polytope moves r by O(1/lambda)=o(delta^2). The weight is thus comparable to `1/(r|log delta|)` on an annulus with radii fixed multiples of delta^2 and delta. Only facets incident to the vertex remain for small delta. On each planar facet, even if its angular sector is smaller than a full disk,

    integral weight^2 dS
      <= (2pi/|log delta|^2) log(C delta/(c delta^2))
      = O(1/|log delta|).

Uniform surface Jacobian bounds preserve this estimate on the actual smooth boundary. The bounded inner error has L2 norm O(delta). Thus `||W_lambda||_L2 -> 0`. Holder with the uniform trace inequality gives exactly the quadratic form needed for absorption. This is not merely a small-volume assertion. The exponent H1-to-L4 and the L2 boundary norm are specific to dimension three; the proof does not silently settle the higher-dimensional source conjecture.

### Homotopy, nonvanishing and facet traces

Every eta is in the verified hemisphere about q. Normalized straight interpolation from eta to q is consequently a globally continuous homotopy, including inside the vertex balls where they agree. The collar homotopy and orientation-preserving radial map imply degree(q restricted to Sigma_lambda)=+1. The outward normal of a smooth convex body containing zero satisfies `nu(x).x>0`, by its supporting plane and an interior ball. Therefore its Gauss map is homotopic to the radial map and also has degree +1. Since Sigma_lambda is a sphere, the maps eta and nu are homotopic. All hypotheses of the verified smooth-domain propositions hold for each large lambda.

Normalize the nonzero harmonic matrix to have L2 mass one. The energy inequality and quadratic-form estimate yield `E_lambda<=C epsilon_lambda(E_lambda+1)` with epsilon tending to zero. Absorption gives E_lambda tending to zero. Uniform H1 extension and Rellich compactness give a strong L2 limit on a fixed ball. On every compact interior subset its derivative vanishes, so connectedness of int(P) gives a single constant C there.

There is no hidden boundary-layer mass loss. Strong L2 convergence implies convergence of squared norms in L1; the characteristic functions of P_lambda converge almost everywhere to that of P. Their product integrals therefore converge and give `vol(P)|C|^2=1`. In particular C is nonzero.

Every actual facet has a relatively compact interior patch. For large lambda, all other cutoffs vanish there, the surface is exactly the original facet plane, eta is exactly m_i, and a fixed interior half-ball can be used. On that half-ball the L2 convergence and vanishing gradient energy imply strong H1 convergence to C. Continuous traces pass the boundary condition to `c(n_i)C=C c(m_i)`. Only such fixed flat patches are used; no assertion about traces at vertices or moving pointwise boundary values is needed.

### Final algebra

Taking adjoints correctly gives `C* c(n_i)=c(m_i) C*`. Hence C*C commutes with every target normal Clifford matrix. Boundedness of Q forces its facet normals to span R^3; otherwise a nonzero common orthogonal direction would translate Q into itself for every real distance. The Pauli representation is irreducible, so C*C is a scalar positive multiple of I and C is invertible. Anticommuting the two facet identities gives equality of every pairwise normal inner product, as claimed.

There is an optional simplification: after anticommuting, the equation is already a scalar multiple of the nonzero matrix C. Nonzeroness alone forces that scalar to vanish; invertibility is not required for Gram equality. The original stronger invertibility argument is valid.

## Adversarial boundary controls and exact remaining limits

- **Nonsimple apex:** for the square pyramid with apex (0,0,h), side normals have z-component `1/sqrt(1+h^2)`. After an interior translation, its apex radial direction is upward and has this strictly positive dot product with all four incident side normals. Opposite side facets meet at the apex but not an edge and are excluded by the active-set localization. The code records h=10^-6,1,10^6 only as diagnostics; the displayed formula is the general check.
- **Nearly flat angles:** constants may deteriorate as a sequence of fixed polytopes degenerates, e.g. h tends to zero or infinity in the pyramid. The theorem needs constants for each fixed nondegenerate P,Q, not uniformity over a degenerating class. No endpoint angle zero or pi is included.
- **Reflection:** all target normals are reflected simultaneously and labels preserved. Gram products and comparison hypotheses survive. A face-lattice map that reverses orientation is therefore covered without changing the fixed correspondence.
- **Equal-angle cases:** boxes with different side lengths remain admissible and have the same normal Gram matrix; no false congruence conclusion is made.
- **Redundancy:** adding an inequality that is not an actual facet is outside the labeling convention and would damage facet-interior trace extraction. The original expressly uses each actual facet once.
- **No all-dimensional promotion:** vertex neighborhoods exhaust multi-active regions only because dimension is three, and the critical trace exponent also uses dimension three.
- **No circularity:** the face-preserving homeomorphism uses the face lattice only; the smooth-domain index input has no angle comparison assumption; the logarithmic estimate is supplied directly. None of these bridges assumes the target theorem in renamed form. No route was marked blocked because none transferred the central difficulty to an unsupported equivalent assertion.

The strongest verified mathematical result is exactly the candidate's all-normal-Gram rigidity implication in dimension three, and consequently the original ordered-pair corresponding-edge comparison, conditional only on the named, actually inspected Brendle v4 propositions and standard Sobolev/elliptic foundations. Those foundational results are imported, not formally reproved. **Mathematical remaining gap: none found.** Finite diagnostics neither establish universal geometry nor substitute for the analytic theorems.

**Required issues:** none for the checked mathematical deduction and exact model.

**Optional documentation issues:**

1. In any promoted exposition distinguish verified publication metadata from inspected final author-manuscript content; the present audit has not established current journal-main-text equality.
2. Add the coefficient-to-column transpose derivation to avoid the wrong target representation; if discussing ordered Clifford volume, state the row/column convention explicitly. The source ordering-sign caveat above is resolved and has no theorem effect.
3. The final Schur/invertibility step may be shortened to cancellation of a nonzero matrix after the scalar anticommutator identity.
4. Keep the 2017 volume/report year and 2018 publication date distinct in bibliography.

**Deferred, not mathematical blockers here:** firstness, current openness, the recent Bi/Wang-Xie-Yu claims, community verification, and publication/merge/DOI decisions. No conclusion about them is certified by this family.

## Reproduction and release boundary

Run from this family directory:

    python3 convention_controls.py
    python3 authenticate_originals.py --output /tmp/pr932-source-original-auth.json
    python3 verify_manifest.py --manifest MANIFEST.json --manifest-sha256 <pin in VERIFY.md>

The first operation regenerates finite convention controls; the second reads only the selected immutable Git program and disk copies; the third verifies only the explicitly curated files against an externally supplied map hash. No command needs network access, a package install, Git mutation or external communication.

For primary-source reinspection, use the exact URLs/versions in `SOURCE_RECORDS.json`, verify their bytes against the recorded hashes, render the specified page numbers with Poppler, and inspect the material formulas from page pixels. The stored raw PDFs, extracted text, HTML, response headers, temporary files and renders are all private evidence and explicitly excluded from the public map. A re-downloaded PDF may be byte-different after provider reprocessing; that is not a license to claim it is the inspected version without comparison.

`MANIFEST.json` is deliberately self-excluded. `VERIFY.md` is a separate external map anchor and cannot be included in the map it anchors without a hash cycle. The root audit must separately authenticate both metadata files and include whatever final curated files it releases in its own explicit outer map. This family performs no publication action.
