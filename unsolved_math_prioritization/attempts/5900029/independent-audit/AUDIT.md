# Independent adversarial audit: finite-total-curvature planarity

## Verdict

**Pass as a source-qualified unsuccessful five-route investigation. The full target is not resolved.** No false auxiliary mathematical claim requiring a substantive correction was found in the frozen packet. The Moore two-end theorem must retain the packet's proof-dependency qualification. No novelty, priority, complete-proof, or global-current-literature certification is given.

This review binds exactly to `FROZEN_MANIFEST.json` with SHA-256
`4ec513d83ee59af8d053982926ab62054a363da10abb82d8e0d4254a2f84d7ff`.
All eight listed input files match their sizes and hashes. The author verifier runs successfully and its parsed result equals the stored `CHECKS.json`. Hashes were checked again after execution. The originals have not been edited. All new work is audit material, not an additional attempt to settle the exhausted target.

The main unresolved statement remains: for connected smooth complete boundaryless area-minimizing real k-submanifolds of Euclidean n-space with 2 <= n-k < k, does integral |A|^k < infinity force flatness? Area minimization is interpreted in the oriented integral-current category as explicitly stated by the packet. Different coefficient/orientability conventions are not silently resolved by this review.

## 1. Statement, attribution, and boundary cases

Problem 29 on author-manuscript page 6 of Sullivan and Morgan's *Open Problems in Soap Bubble Geometry* was independently inspected in text and in its rendered page. Its mathematical target, the strict dimension inequality, and the surrounding completeness context agree with the submitted normalization. Helen Moore is the appropriate attribution. The original terse wording does not fully specify connectedness and the coefficient category; the packet openly states those conventions instead of exploiting omissions.

For H=trace A, the Gauss equation gives Scal=|H|^2-|A|^2. Thus minimality yields Scal=-|A|^2 and integral |A|^k=integral (-Scal)^(k/2). An unpowered integral of scalar curvature is not the higher-dimensional hypothesis. A fixed normalization factor in scalar curvature is harmless for finiteness, but changing the exponent is not.

The flatness-to-planarity step is sound. If A=0, the tangent space is fixed along the connected immersion. Its image lies in one affine k-plane, and the map is a complete local isometry to that plane. A complete local isometry covers its connected target; Euclidean space is simply connected. Completeness and connectedness therefore matter. Codimension zero and k=1 do not leave hidden nontrivial cases; k=2 with positive codimension below k is the hypersurface case.

The source note about complex examples is not a license to assert that every complete holomorphic curve has finite total curvature. The packet appropriately uses a directly checked polynomial graph. Its conclusions do not rely on that overbroad reading of the original surrounding note.

## 2. Prior affirmative cases and source scope

Anderson's Theorem 5.1 supplies multiplicity one for ends in real dimension k>=3, and Theorem 5.2 supplies one-end rigidity. The relevant argument was read: the end link is a connected covering of the simply connected sphere S^(k-1), hence has covering degree one. Monotonicity then forces a one-ended immersion to be a plane. Finiteness of the end set comes from the earlier compactification results, notably Theorem 3.2. For exact citation hygiene, the first sentence of PROOF.md Section 2 could cite Theorems 3.2, 5.1, and 5.2 together. This is an optional attribution refinement, not a failure of the result.

Shen and Zhu's primary-PDF indexed Main Theorem independently confirms the complete oriented stable hypersurface conclusion with integral |A|^k finite, without a dimension upper bound. The direct PDF open failed; the indexed first-page statement was readable. No full-proof reconstruction or locally archived Shen-Zhu PDF is claimed by this audit. The packet itself already qualifies its inspection correctly. Area minimization implies the requisite normal stability in the stated category, so this is a valid credited special case, including k=2,n=3.

Wang's 2003 publisher abstract imposes super stability, not ordinary normal stability. A further primary-source check, Wang's 2006 paper *Harmonic maps and the topology of complete submanifolds*, Definition 1.1 on p.420, states the exact scalar inequality used in the packet and distinguishes it from normal stability. This supports the qualification; it does not remove it. The 2003 full proof was not reconstructed.

The inspected 2026 Ding-Zhang Theorem 1.1 bounds the number of diffeomorphism types under uniform critical-curvature and volume-growth bounds. It does not state the requested area-minimizing rigidity theorem. Castro-Urbano's introduction and Proposition 1 confirm complete calibrated finite-curvature examples at the excluded equality threshold. None of these checks establishes an exhaustive current-literature search.

## 3. Ordinary catenoid instability

The arclength identities and all signs were recomputed. With f=r^(1-k), the radial Laplacian is f''+(k-1)(r'/r)f'. Substituting r'^2=1-r^(-2k+2), r''=(k-1)r^(-2k+1), and |A|^2=k(k-1)r^(-2k) gives

    (Delta+|A|^2)f=(k-1)r^(-k-1).

The coefficient of r^(1-3k) cancels exactly; the remaining coefficient is k-1. The added verifier checks these identities as polynomials in k, separately from the author's rational samples.

The compact-support passage is essential and is handled correctly. Expanding Q(chi f), integrating by parts against the compactly supported chi^2 f, and collecting cross terms gives

    Q(chi f)=integral f^2|grad chi|^2
             -integral chi^2 f(Delta+|A|^2)f.

Since r(s) is comparable with 1+|s|, the first integral on the two cutoff shells is O(R^(-k)) for k>2 and O(R^(-2)) for k=2. Multiplying the second integrand by r^(k-1) gives (k-1)r^(-k-1), which is integrable and has strictly positive integral. Bounded cutoffs converging pointwise to one permit dominated convergence. Thus there are genuinely compactly supported negative variations. Their normal direction inside the original (k+1)-dimensional span remains an admissible normal direction after adding ambient dimensions.

As a quantitative audit check at k=2, r(s)=sqrt(1+s^2). Use a Lipschitz cutoff equal to one on |s|<=R, linear on R<|s|<2R, and zero outside. Its error is at most 4*pi/R^2. For R>=1 the potential on |s|<=1 alone is at least pi, since r^(-3)>=1/4 there. R=3 therefore gives Q<=-5*pi/9. Smooth compactly supported approximations preserve strict negativity. This checks the cutoff mechanism without assuming that the positive uncut f is itself an allowed variation.

## 4. Moore's published two-end theorem and its dependency

The journal PDF has 23 pages and 270,482 bytes, matching the submitted SHA-256. Section 2 was inspected, with pp.1027-1028 also independently read as page images. The published Theorem 1 does state the k>=3, k>n/2, two-ended catenoid classification described by the packet.

The proof of Lemma 1 infers transverse intersection of nearby disjoint end links from C^1 convergence to distinct intersecting great spheres. The dimension inequality guarantees positive-dimensional intersection of the underlying linear planes, but it does not guarantee their sum fills the ambient space. The latter is the transversality condition.

The submitted countermodel is correct. In R^6, the direction spaces

    P1=span(e1,e2,e3,e4), P2=span(e1,e2,e3,e5)

have dimensions 4,4, sum dimension 5, and intersection dimension 3. L1=P1 and L2=e6+P2 are disjoint because their sixth coordinates differ. Their rescaled links are disjoint, while their limits are distinct great S^3s meeting in S^2. The convergence is smooth, and the limiting intersection is nontransverse. Independent exact rank and rational-latitude checks reproduce this.

This refutes the local inference under those local facts alone. It is **not** a counterexample to the full connected minimal two-ended theorem. The packet is correct to distinguish a published claim from an independently reproduced proof and to avoid announcing the theorem false. A complete repair or refutation of that theorem is outside this audit. The ordinary-catenoid instability gives the asserted two-end exclusion if the classification is accepted; without that input, it does not classify all possible two-ended higher-codimension examples.

Even granting the classification, it does not address three or more ends. The frozen packet's unsolved status therefore does not turn on adjudicating this theorem's ultimate validity.

## 5. Calibrated plane cone

For phi=dt1 wedge ... wedge dt(k-2) wedge (dx1 wedge dy1+dx2 wedge dy2), the complementary Hodge dual is the standard Kahler two-form on the last four coordinates, with zero action on the remaining coordinates. Its skew operator J satisfies J^T J equal to the orthogonal projection onto those four coordinates. Consequently |Jv|<=|v|, and |<Ju,v>|<=1 on every orthonormal pair. Equality occurs on either coordinate complex line. Hodge star preserves the relevant unit simple complementary multivectors, so phi has comass one. The independent tests verify the complementary signs and this projector identity in several dimensions; the preceding argument covers all k>=3.

Both product planes have the calibrated orientation. Their intersection has dimension k-2, so it has zero k-dimensional measure and creates no cancellation of current mass. The sum current is calibrated and minimizes against compactly supported current competitors by closedness and the calibration inequality. The cone is singular at its intersection. Thus it correctly defeats the suggested tangent-cone obstruction but fails the smoothness hypothesis of the source question. No conclusion about realizability by smooth finite-curvature minimizing ends follows from this example.

## 6. Normal-translation cancellation and scalar superstability

For a constant ambient vector a, differentiation of a=a^T+a^perp and normal projection gives nabla_i^perp a^perp=-A(e_i,a^T). Summing over a complete orthonormal ambient basis gives the four pointwise identities in PROOF.md: the normal squared lengths sum to q, mixed tangent-normal projections sum to zero, and each of the two curvature sums equals |A|^2. Expanding Q(f a^perp) therefore cancels both curvature contributions and yields exactly q integral |grad f|^2.

The new verifier repeats the calculation in rationally rotated ambient frames. Individual cross terms are genuinely nonzero in these frames, but their sum is zero, and the two curvature sums still cancel. This guards against an accidental benefit from using only an adapted frame. Neither the identity nor its sign changes when q<k.

There is a direct additional stress test using the packet's own calibrated parabola. Its metric is conformal on C, so scalar Dirichlet energy is the ordinary planar Dirichlet energy. Take psi=1 for r<=1, psi=1-log r for 1<r<e, and psi=0 beyond e. Then

    integral |grad psi|^2 = 2*pi,
    integral_(r<=1) |A|^2 dV = 16*pi/5.

Hence the scalar index form is at most -6*pi/5. Compactly supported smooth approximation preserves negativity. The parabola is nevertheless calibrated and normally stable. Thus ordinary normal stability really does not imply the scalar super-stability inequality, independently of the cancellation test. This is an audit check of an already submitted example at the excluded dimensional threshold, not a new target counterexample or a sixth proof route.

## 7. Parabola, products, and critical scaling

For F(x+iy)=(x+iy,(x+iy)^2), the coordinate derivatives are orthogonal and have common squared length lambda=1+4r^2. Completeness follows from g>=g_Euclidean; properness follows from |F(z)|>=|z|. The Kahler form evaluates to lambda on (Fx,Fy), so the proper complex-oriented image is calibrated. The conformal formula K=-(Delta log lambda)/(2 lambda) gives K=-8/lambda^3 and |A|^2=16/lambda^3. Its curvature mass inside parameter radius R is

    integral_(r<=R) |A|^2 dV = 4*pi - 4*pi/(1+4R^2).

The total is 4*pi. It is nonflat, complete, and minimizing in real dimension 2 and ambient dimension 4, exactly the excluded equality k=n/2. There is no strict-inequality counterexample here.

For N times R^d, d>=1, A is pulled back from N. A nonzero curvature value persists on a positive-volume relatively compact patch. Integrating its positive lower bound over increasing Euclidean cubes proves divergence for the product's critical exponent. This is a Tonelli/positivity argument, independent of whether N's own critical integral is finite. Applying it to the parabola and to nonflat neck products is valid. A flat factor is not a way to import an equality-threshold example into the target.

The dilation exponents cancel: |A|^k acquires lambda^(-k) while dV acquires lambda^k. Finiteness therefore cannot be converted to global smallness by dilation. No claim about the compact core follows from small exterior tails.

## 8. Small-energy constants and exhaustion

The conditional argument was reconstructed rather than inferred from test output. Set

    I=integral eta^2 u^(k-2)|grad u|^2,
    J=integral eta^2 u^(k+2),
    B=integral u^k|grad eta|^2.

Multiplication of u Delta u>=-c u^4 and integration by parts give
(k-1)I<=cJ+2 sqrt(IB). Young's inequality implies
I<=2cJ/(k-1)+4B/(k-1)^2. For v=u^(k/2),
integral |grad(eta v)|^2<=k^2 I/2+2B. Substitution gives exactly the coefficients in the packet. Holder uses exponents k/2 and k/(k-2), yielding the factor T(M)^(2/k). Sobolev then permits absorption under the displayed strict smallness inequality.

For complete M, compactly supported Lipschitz distance cutoffs with gradient O(1/R), followed by smooth approximation as needed, give B<=C R^(-2)T(M). Once the term is absorbed, Sobolev and exhaustion force u=0. Positive regularization handles zeros of u. The argument is expressly conditional on the stated weak Simons and Sobolev inequalities, rather than claiming a proof of those analytic inputs.

A cutoff restricted to an exterior region necessarily retains the inner transition term. Sending its outer radius to infinity does not eliminate that fixed inner contribution. The packet properly refuses this false global rigidity step.

## 9. Corrections, limits, and reproducibility

No mandatory mathematical correction was identified. Optional refinements are:

1. Attribute finite end number to Anderson's earlier compactification result alongside Theorems 5.1 and 5.2.
2. Use the newly corroborated Wang 2006 definition if an explicit primary source for the scalar inequality is desired, while retaining the 2003 abstract/full-proof limitation.
3. In brief status summaries, say that a *nonflat* one-ended example is excluded. Planes of course remain allowed.

The portable audit does not re-query live repository duplicates, regenerate pinned dataset hashes, certify all proofs in all cited papers, establish that the problem remains open everywhere in the 2026 literature, or make a novelty claim. It verifies the exact frozen packet, checks the scope and relevant sources, and challenges every authored auxiliary argument. Source byte/hash checks, inspection locations, and retrieval limits are recorded separately without distributing source text or PDFs.

Run `python3 independent-audit/verify_audit.py` from the portable package root, or pass `--packet /path/to/frozen/public`. Python's standard library is sufficient. `REPLAY.json` records the successful audit replay. `AUDITED_INPUTS.json` binds the input, and `AUDIT_MANIFEST.json` hashes the audit outputs. The hashes establish identity; the written review establishes the stated mathematical assessment. Neither is a proof of the unresolved target.
