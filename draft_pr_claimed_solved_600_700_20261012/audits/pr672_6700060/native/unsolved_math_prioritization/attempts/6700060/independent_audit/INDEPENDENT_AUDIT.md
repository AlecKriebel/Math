# Independent adversarial audit: AMR-066-0060

Audit date: 2026-10-05 (UTC). Target ID: 6700060. Supplied rank: 702.

## 1. Verdict and exact boundary

**Qualified mathematical pass for the explicitly stated smooth, face-preserving, ambient-up-to-corners category.** I independently checked the proof of the needed angle conclusion in Yuchen Bi's arXiv:2608.06320v1, including the smoothing geometry, critical logarithmic trace estimate, smooth-boundary Dirac existence input, nonvanishing limit, and recovery at closed corners. I found no unresolved analytic gap in that route. The application to Euclidean competitors and the separate planar argument also pass in this category.

This is a credited preprint-based resolution with an independent mathematical audit. It is not a new proof of priority, formal verification, human peer review, journal acceptance, or evidence that the mathematical community has settled the source manuscript. Bi's work remains a recent preprint in the checked public sources. It should not be relabeled simply `already_solved` without retaining both the source-status and category qualifications. A descriptive disposition would be `credited_preprint_resolution_independently_audited_smooth_category`; this report does not prescribe or alter a repository's status vocabulary.

The distinction is substantive: the audit did not merely read Theorem 1.1 and apply it. Sections 4–9 below supply independent checks of its difficult steps and identify precisely which established smooth analytic theorems remain imported. No singular-polyhedral-boundary Fredholm theorem from Wang–Xie–Yu is used.

For a category that allows a facewise-smooth or interior diffeomorphism with degenerate differential at higher corners, the result remains **unverified by this packet**. A broader statement would require an additional reduction or another theorem. No such broadening is approved here.

## 2. Frozen input and reproducibility

The exact frozen packet contains 11 regular files, including its manifest. Its archive also contains exactly those 11 files; every archived member was compared directly with the corresponding frozen file and matched.

- Frozen manifest SHA-256: `7ef81a33a9b5d235039cd0d8cee912d23f6fa3bb1e4f67a5e2217ef8c5e1e650`
- Frozen archive: `polyhedra_6700060_FROZEN_PUBLIC_PACKET.zip`
- Archive size: 20,036 bytes
- Archive SHA-256: `7affd5efe893c17d4478f742491b6ec354c72019f85b4f879408020ebafb470d`
- Proof application SHA-256: `099b7a42a4decef9e518ded104acd437b66282fd2cb904c8e08c5fc17b2d393d`
- Author verification SHA-256: `6e4e6154a2b4c67b2d320b14669ca1f3791db7530d8c2ea666f9eda44f4a46a3`

The supplied inventory/replay verifier passed under normal Python and optimized Python, and all seven supplied corruption controls were rejected in both modes. The 4,293 supplied finite controls were also replayed directly under both normal and optimized Python, with output matching the frozen result. This direct optimized replay matters because the verifier's subprocess does not itself inherit its parent's `-O` flag.

Four decisive PDFs were independently retrieved afresh from their public, version-pinned URLs: Bi, Brendle, Bär–Hanke–Schick, and the 2017 Gromov problem list. All four freshly retrieved byte sequences matched the supplied PDF hashes and sizes. Fresh `pdftotext -layout` extractions matched the supplied text extractions. Critical displayed formulas were additionally checked visually: Bi pp.15–17, Brendle pp.11–12, and Gromov printed p.60. Bi's complete 18-page argument was read; Brendle's relevant Section 2 definitions, estimates, and Propositions 2.14–2.15 were read. The complete four-page Bär–Hanke–Schick note was read.

The independent controls accompanying this report check exact Clifford boundary algebra in dimensions three and five, the odd/even distinction, the logarithmic integral and adverse scaling variants, and the necessity of a nonsingular corner map. Their finite successes do not certify an index theorem, a Sobolev theorem, compactness, or the manuscript's proof. The mathematical assessment is the authored argument below.

All frozen inputs were preserved. No remote writes or queue changes were made.

## 3. Original question, smoothness, and pullback

### 3.1 What the primary source supports

Gromov's 2017 problem list, Section 22, printed p.60, compares compact full-dimensional convex Euclidean polyhedra. Convex extremality is formulated for combinatorially corresponding convex competitors. Mean-convex extremality uses a diffeomorphic Euclidean domain with corresponding faces, nonnegative face mean curvature, all corresponding dihedral angles no larger than the reference angles, and strict inequality somewhere on a codimension-two face. It does not demand a prescribed boundary metric, a length-decreasing map, fixed volume, or fixed edge lengths. The strict inequality need occur at only one point.

The 2017 paragraph does not separately define the word “diffeomorphic” at a nonsimple corner. I therefore checked Gromov's earlier primary treatment, *Dirac and Plateau Billiards in Domains with Corners*, author manuscript dated September 20, 2013, Section 1, pp.2–3. There a cornered smooth structure is supplied by an ambient smooth manifold extension, and the tangent bundle is the ambient tangent bundle restricted to the domain. This supports the ambient smooth interpretation used in the packet. It does not license replacing that interpretation with mere combinatorial equivalence or an arbitrary interior diffeomorphism.

Accordingly, the accepted statement here requires a face-preserving map F:P→P' whose map and inverse are smooth in the ambient-extension sense. Equivalently for the pullback argument, the map must give a smooth positive-definite pullback metric through every stratum. This is a natural, source-supported smooth convention, but the explicit qualifier should remain attached to the conclusion. At a nonsimple vertex it is a real restriction, not a consequence of combinatorial equivalence alone.

Minor bibliographic correction: the 2017 PDF's title uses **“around Scalar Curvature”**, with an incomplete/unedited-version qualifier. The packet repeatedly uses “about Scalar Curvature.” Its URL, content, and hash identify the correct source; this is a title correction, not a mathematical mismatch.

### 3.2 Pullback without hidden metric assumptions

Let g=F*e, with e the Euclidean metric on P'. Since F and its inverse extend smoothly locally, the chain rule on the interior and continuity at the boundary give an invertible derivative at every point of P. Thus g is smooth and positive definite up to every corner.

To meet the precise neighborhood hypothesis of Bi, extend the locally defined tensors to small open neighborhoods, shrink them until each tensor remains positive definite, and use a finite subordinate smooth partition of unity. The tensors agree on P; their convex combination is positive definite and agrees with g on P. The extension's curvature outside P is irrelevant.

On the interior, F is an isometry to a Euclidean domain, so the scalar curvature is exactly zero. The smooth extension makes the same equality hold on P by continuity. Face preservation also preserves the outward side, hence the outward unit normals and the second fundamental forms; face mean curvature is carried to the given nonnegative mean curvature of P'. No comparison between the reference Euclidean metric on P and the pullback metric has been introduced.

For interior wedge angle theta and outward-normal angle alpha, theta=pi-alpha and the outward-normal inner product is -cos(theta). Consequently, theta'≤theta is exactly alpha_g≥alpha_0. The direction of this reversal is essential in Section 5.

The tangent bundle is the restriction of the trivial ambient tangent bundle. A smooth g-orthonormal frame can be chosen on a sufficiently small contractible neighborhood of P, giving the ordinary spin structure used by the argument. There is no extra nonspin competitor excluded after the pullback. Orientation can be fixed on P independently of whether the chosen F preserves the reference orientation.

## 4. Smoothing and higher-corner geometry

Use an irredundant description P={u_a≤0} with affine defining functions having unit Euclidean gradient N_a. Let p be an interior point, d0=min_a(-u_a(p))>0, and let R bound |x-p| on P. For an active index with u_a(x)>-2/lambda and lambda≥4/d0,

    du_a(x-p) ≥ d0/2.

Thus, for nonnegative coefficients t_a,

    |sum_a t_a du_a| ≥ (d0/(2R)) sum_a t_a.

Uniform equivalence of g with the Euclidean metric gives the analogous g-covector estimate. This is a noncancellation estimate, not a claim that all facet normals lie in a globally fixed hemisphere.

With a smooth convex cutoff Phi that is flat on (-infinity,-2], has positive derivative afterwards, and satisfies Phi(0)=1, put F_lambda=sum_a Phi(lambda u_a). The set P_lambda={F_lambda≤1} is convex, contained in P, and contains a fixed interior ball for large lambda. On its level set, at least one cutoff derivative is bounded below uniformly in the finite collection of cutoff arguments: restrict each argument to [-2,0], with their Phi-values summing to one. The noncancellation estimate then gives |dF_lambda|_g≥c lambda. Its boundary is therefore smooth even though it may contain flat open facet patches.

Convex bodies between two fixed concentric balls have uniformly Lipschitz radial functions: their gauges are uniformly Lipschitz, and the gauges stay uniformly positive on the unit sphere. Consequently the radial maps from the unit ball, and between P and P_lambda, are uniformly bi-Lipschitz. Moving a point of P toward p by a fixed multiple of lambda^-1 makes every defining function less than -2/lambda, so the radial discrepancy is O(lambda^-1). In particular, each fixed compact subset of the interior is eventually in P_lambda.

The face-distance error bound is linear. If y is the Euclidean projection of x∈P to an intersection face F_I, the displacement belongs to the normal cone generated by active inequality normals together with the span of the equality normals in I. If unit displacements of this type could annihilate all equality normals while satisfying the remaining nonpositive inequality pairings, a limiting displacement w would satisfy

    |w|^2 = sum_j mu_j du_j(w) + sum_a ell_a du_a(w) ≤ 0,

contradicting |w|=1. There are finitely many face types, giving a uniform constant. This yields dist(x,F_I)≤C max_{a∈I}|u_a(x)|. It is applicable at nonsimple vertices and does not assume independent normals for every active set.

Let E be the union of pairwise facet intersections and K the union of triple intersections. Irredundancy ensures every nonempty triple intersection has ambient codimension at least three. At a point in a ridge interior, the transverse two-dimensional pointed cone has precisely two boundary rays; only two facets can contain the ridge. An extra supporting plane through the same ridge that lay between the two defining planes would be redundant. Therefore the use of two transverse variables near K is legitimate for every polytope in the stated class.

Near a point where at least three cutoff terms are active, the face-distance estimate places the point within O(lambda^-1) of K. Hence outside that neighborhood only one or two indices can be active. On a fixed compact subset of a facet interior all other cutoffs vanish for sufficiently large lambda; the smooth boundary agrees exactly with the original facet there. These exact fixed patches will be needed for the limit boundary condition.

## 5. Two-face normal interpolation and degree

Suppose exactly two indices a,b are active away from K. The common tangent subspace L=ker du_a∩ker du_b has dimension n-2. Its g-orthogonal complement in the smoothed boundary tangent space is a line, with unit vector e oriented toward increasing u_b. Expanding the level-set second fundamental form gives

    II_lambda = kappa e* tensor e* + B_lambda,
    kappa ≥ 0,  kappa ≤ C lambda,  |B_lambda| ≤ C.

Only the second derivatives of the cutoff produce the leading term; all metric derivatives enter the uniformly bounded remainder. Thus H_lambda=kappa+O(1), and tangential derivatives of the normal in directions of L are O(1).

Project x onto the affine ridge plane. If that projection were outside the ridge, a nearest ridge point would lie on its relative boundary, which is contained in K; this contradicts the assumed distance from K. The projection x_ab is therefore on the actual ridge. Transport its two g-unit normals to x. Their difference from the current normals is O(lambda^-1), with uniformly bounded first derivatives. Differentiating the cutoff weights costs O(lambda), so the difference between the actual rounded normal derivative and the transported rounded normal derivative is still O(1). This closes a potentially dangerous small-error-times-large-derivative step.

Let alpha be the angle between the transported normals and let s be the position of their weighted normalized combination along the minor spherical arc. Smooth positive definiteness, compactness of each closed ridge, and independence of its two defining covectors keep alpha uniformly in (0,pi). Differentiation in the transverse direction gives ds(e)=kappa+O(1); derivatives along L and derivatives of alpha are bounded. Send the fractional arc parameter s/alpha to the reference normal arc of length alpha_0. The hypothesis alpha≥alpha_0 makes its leading transverse derivative at most kappa. The trace norm of the full derivative is therefore at most H_lambda+C.

This estimate has the correct interior/exterior convention. Reversing it would produce a leading factor alpha_0/alpha>1 and an uncontrolled positive error of order lambda.

At the transition from two active facets to one, the vanishing cutoff derivative is flat. The arc coordinate can be written locally as an arctangent whose denominator remains positive. Thus the interpolation joins the constant facet-normal map smoothly; no hidden arccos endpoint singularity remains.

For the extension across K, put q(x)=(x-p)/|x-p|. The initial noncancellation estimate gives q·N_a≥c>0 for every active facet. A reference minor-arc point is a positive sine-weighted sum of its endpoint normals, and the sum of its weights is at least one. Thus q has uniformly positive inner product with the interpolated normal zeta.

Choose a smooth regularized distance r to K with r comparable to dist_g(.,K) and bounded first derivative. Set delta=lambda^-1/4. Transition from q to zeta across delta^2<r<delta using a smooth cutoff with derivative bounded by C/(r |log delta|). The transition is along the unique minor sphere geodesic. Holding q fixed, this contraction maps polar coordinates (theta,omega) to (t theta,omega). On the verified hemisphere theta<pi/2 its differential has norms t and sin(t theta)/sin(theta), both at most one. Moving q contributes only O(1); differentiating the cutoff contributes the stated logarithmic weight.

The resulting smooth map eta_lambda is homotopic to q, hence has degree one. The homotopy has no antipodal singularity because the positive hemisphere margin is uniform. It equals the reference normal on each eventual fixed facet patch. The construction does not require a globally defined corner Gauss map.

## 6. The critical trace estimate, rederived

This is the central analytic check. A shrinking support by itself would be insufficient because the spinor could concentrate there.

Let W_lambda=(||d eta_lambda||_tr-H_lambda)_+. Convexity of the cutoff gives a nonnegative leading Hessian term; bounded derivatives of g and the gradient lower bound give H_lambda≥-C globally. Combining this with Section 5 yields a pointwise majorant consisting of:

1. a bounded weight on an O(lambda^-1) neighborhood of E;
2. a bounded weight on an O(delta) neighborhood of K;
3. the weight 1/(r |log delta|) on delta^2<r<delta.

Uniform radial bi-Lipschitz maps give uniform W^(1,2) extension constants. Kato's inequality reduces bundle estimates to scalar estimates of the norm. Poincare with an interior ball B controlling the constant mode, followed by the usual boundary trace theorem, gives

    ||psi||^2_L2(P_lambda) + ||psi||^2_Lq(boundary P_lambda)
        ≤ C ( ||nabla psi||^2_L2(P_lambda) + ||psi||^2_L2(B) ),
    q = 2(n-1)/(n-2).

The ridge strip has surface measure O(lambda^-1), by pulling it back to the finite facets of P. Holder therefore supplies the small factor lambda^-1/(n-1) for its bounded contribution.

To handle K, first pull the boundary back radially to the fixed boundary of P. The displacement O(lambda^-1)=O(delta^4) is negligible compared with the annulus's inner radius delta^2. Distances and annulus endpoints remain comparable by fixed constants; volume and surface Jacobians remain bounded above and below almost everywhere.

On a fixed facet F_a, a nearest triple-intersection face sufficiently close to F_a must intersect F_a. Applying the finite face-distance bound to its intersection with F_a shows that distance to K is comparable to the minimum of distances to triple-intersection faces incident with F_a. A finite sum of weights for these faces therefore dominates the pulled-back weight. This avoids assuming that the nearest higher corner is automatically contained in the current facet.

Fix one such face G. Rotate and translate Euclidean coordinates to (y,z,t)∈R^(n-3)×R^2×R, with F_a in t=0 and G in z=t=0. This remains possible if G has smaller dimension. Write a(y)=dist((y,0,0),G). Then

    dist((y,z,0),G)^2 = a(y)^2 + |z|^2.

For positive fixed constants c,C define

    b_delta(y,z) = 1_{c delta^2 < sqrt(a(y)^2+|z|^2) < C delta}
                    / (sqrt(a(y)^2+|z|^2) |log delta|).

For each fixed y, polar coordinates rho=|z| and s=sqrt(a(y)^2+rho^2) give rho d rho=s ds. Consequently,

    integral_R2 b_delta(y,z)^2 dz
        ≤ (2 pi / |log delta|^2) integral_(c delta^2)^(C delta) ds/s
        ≤ C' / |log delta|.

This bound is uniform in y, including y outside the face projection and a(y)=0. The bounded neighborhood indicator has L2_z norm at most C delta.

For a scalar extension v∈W^(1,2)(R^n), almost every three-dimensional slice v(y,.,.) belongs to W^(1,2)(R^3). The three-dimensional Sobolev trace inequality gives

    ||v(y,.,0)||^2_L4(R2) ≤ C ||v(y,.,.)||^2_W1,2(R3).

By Holder in z and then integration in y,

    integral b_delta |v(y,z,0)|^2 dz dy
        ≤ C |log delta|^-1/2 ||v||^2_W1,2(Rn).

The same argument gives C delta for the bounded neighborhood weight. The compatibility of slicing and traces follows first for smooth functions and then by density and the continuous trace estimate; it is not an assumption of pointwise smoothness for arbitrary W^(1,2) sections.

Using the uniform extension estimate and the interior-ball Poincare bound yields

    integral_(boundary P_lambda) W_lambda |psi|^2
        ≤ epsilon_lambda ( integral_Plambda |nabla psi|^2 + integral_B |psi|^2 ),

where one may take

    epsilon_lambda = C [lambda^-1/(n-1) + delta + |log delta|^-1/2] → 0.

Every constant here depends on the fixed polytope, metric, finite charts, and interior ball, not on lambda or the tested section. In dimension three the y-factor has dimension zero and the same argument applies directly. No higher-dimensional Sobolev exponent is incorrectly used in place of the three-dimensional slice exponent.

### Adverse controls for this step

If one uses an ordinary cutoff changing over delta/2<r<delta with derivative O(1/delta), its squared L2 norm in the two transverse boundary directions stays of constant order. Concentrating test functions at that scale prevents this method from giving a vanishing form bound. If the corner set had ambient codimension two, the analogous one-dimensional transverse L2 calculation for 1/(r |log delta|) would diverge. The logarithmic scale and the codimension-three statement are therefore essential. Neither can be replaced by a small-area slogan.

## 7. Smooth-boundary Dirac existence and conventions

The smooth existence input can be checked in its own setting, independently of any assertion about operators on a polyhedral boundary.

For odd n≥3 use matching irreducible complex Clifford modules with c(v)^2=-|v|^2 and normalized volume element i^((n+1)/2)c(e_1)...c(e_n)=I on both sides. On Hom(Delta,S), define

    chi A = -c(nu) A omega(eta),
    D_boundary A = sum_j c(nu)c(e_j)nabla_ej A + (H/2) A.

Both c(nu) and omega(eta) are skew-adjoint. Hence chi is self-adjoint and chi^2=I. The plus boundary condition is chi A=A, equivalently c(nu)A=A omega(eta). In Euclidean geometry with eta=nu, the constant identity homomorphism has chi I=I. This explicit check prevents a silent flip to the other boundary convention.

For a nonzero tangential covector xi, the inward decaying principal solutions have initial data in the positive eigenspace of L=i c(nu)c(xi). This L is self-adjoint, squares to |xi|^2, and anticommutes with chi. The positive L eigenspace has half the total dimension, as does the negative chi eigenspace. Its intersection with the positive chi eigenspace is zero: applying anticommutation to a common positive eigenvector gives inconsistent signs. Therefore (I-chi) maps the decaying-symbol subspace isomorphically to the prescribed boundary target. This is the smooth complementing boundary condition.

The imported foundational theorem is the ordinary smooth elliptic boundary-value theorem: this condition yields a Fredholm map H1→L2 plus H1/2 boundary data, smooth kernel/cokernel representatives, and homotopy invariance of the index. Brendle's Proposition 2.14 explicitly supplies this theorem in exactly the relevant setting, with the symbol argument above. This audit does not formally reconstruct the general elliptic regularity machinery from first principles.

At the Euclidean Gauss-map base point, the identity gives a nonzero plus kernel. For a cokernel element, Green's formula yields a harmonic section satisfying the minus boundary condition; normal Clifford multiplication commutes with chi, so the sign does not flip at this step. Convexity gives H=||d nu||_tr. The boundary energy inequality, also valid for the minus condition by replacing eta with -eta, forces this harmonic section to be parallel. Its constant matrix must anticommute with every Clifford generator because the Gauss map of a smooth compact convex body covers the unit sphere. In odd dimension it then anticommutes with the nonzero scalar Clifford volume element, and so it is zero. The cokernel vanishes and the index is positive (indeed the plus parallel commutant is scalar, giving index one).

For arbitrary g and eta homotopic to the Euclidean Gauss map, interpolate the positive metric smoothly and use the given sphere-map homotopy. There is no curvature condition required during this index homotopy. The varying boundary targets can be identified: with P_t=(I-chi_t)/2, a smooth unitary transport generated by [dot P_t,P_t] identifies their ranges. Thus the family is a continuous family between fixed Sobolev spaces, after smooth bundle identifications, and the index remains positive.

The smoothed domains here are Euclidean-convex and smooth, with sphere boundary, and eta_lambda has degree one. Maps S^(n-1)→S^(n-1) of the same degree are homotopic, so Brendle Proposition 2.15 applies. Strict convexity is unnecessary: the Gauss map is still surjective and homotopic to the radial map. The smooth metric extends over a neighborhood, and the ordinary ambient spin structure is available.

This verifies the precise content of Bi's Proposition 3.5. It supplies a nonzero harmonic A_lambda satisfying the plus condition on each smooth domain. No assertion about a limiting Dirac operator's self-adjoint extension, domain, or Fredholm index on P is needed.

## 8. Boundary energy, compactness, and nonzero limit

A direct differentiation gives

    chi D_boundary A + D_boundary(chi A)
        = -sum_j c(e_j) A omega(d eta(e_j)).

The derivatives of nu contribute H c(nu)A omega(eta), which cancels the two H/2 terms. Choosing singular-vector bases for d eta and using unitarity of Clifford multiplication bounds its inner product with A by ||d eta||_tr |A|^2. The integrated Schrodinger–Lichnerowicz identity for a harmonic section therefore gives

    integral |nabla A|^2 + (1/4) integral R |A|^2
        ≤ (1/2) integral_boundary W_lambda |A|^2.

Normalize each nonzero A_lambda by integral_Plambda |A_lambda|^2=1. For the fixed ball B, its mass is at most one. Combining the energy and trace bounds and using R≥0 gives, once epsilon_lambda<2,

    integral_Plambda |nabla A_lambda|^2 ≤ epsilon_lambda/(2-epsilon_lambda) → 0.

Uniform extension operators to one fixed smooth bounded neighborhood give an H1-bounded sequence. Rellich compactness produces a subsequence converging weakly in H1 and strongly in L2 to A on that neighborhood. Every compact subset of P's interior is eventually contained in P_lambda; hence the vanishing connection gradients imply nabla A=0 there. The smooth first-order parallel equation gives a smooth parallel interior section.

Normalization survives the varying domains. With E_lambda denoting the actual extensions,

    |integral_Plambda |E_lambda|^2 - integral_P |A|^2|
        ≤ || |E_lambda|^2 - |A|^2 ||_L1
           + integral_(P minus P_lambda) |A|^2.

The first term tends to zero by strong L2 convergence and bounded L2 norms. The second tends to zero by interior exhaustion and absolute continuity (equivalently dominated convergence). Consequently integral_P |A|^2=1. A mere assertion of weak convergence would not suffice; the proof has the required strong convergence.

On a fixed compact facet-interior patch, the boundaries and the reference normals eventually agree exactly. The extensions' traces there agree with the interior-domain traces, because they are genuine H1 extensions. The compact trace map H1→L2 on a fixed smooth patch, or interpolation to H^s for 1/2<s<1 followed by trace, passes the boundary relation to A. A finite local cover and a diagonal subsequence suffice if needed.

Finally, choose a small convex neighborhood of P contained in the metric's domain. Parallel transport A(p) along straight radial segments from a fixed interior point p defines a smooth section there, by smooth parameter dependence of the transport ODE. It agrees with A inside P because A is parallel, and thus extends A through every corner. It need not remain parallel outside P. On P itself parallelness and the boundary relations extend by continuity. Since |A| is constant and positive in the connected interior, its smooth extension is nonzero at every boundary point as well.

There is no uncontrolled passage across a shrinking boundary layer, no assumption of uniform higher elliptic estimates for P_lambda, and no loss of normalization in this limit.

## 9. Angle recovery, rigidity, and dimensions

For any two closed intersecting facets, the limit relation gives

    c(nu_a)c(nu_b) A = A omega(N_a)omega(N_b).

Adding the reversed order and using the Clifford anticommutators gives

    -2 <nu_a,nu_b>_g A = -2 <N_a,N_b> A.

The positive norm of A at that point permits cancellation of this scalar multiple, even without first proving that A is invertible. Therefore the normal inner products, and hence the interior dihedral angles, agree at every point of the closed intersections. This short alternative makes clear why the required angle conclusion survives at lower-dimensional corners.

For the full source theorem, the additional argument also checks out. Parallelness makes A* A constant. Its boundary relations show that it commutes with omega(N_a) for all facets. These normals span R^n; otherwise P would be invariant under a nonzero translation and could not be bounded. Irreducibility then makes A* A a positive scalar multiple of the identity. Equal spinor ranks make A invertible. A parallel spinor frame trivializes the spin connection; the faithful spin Lie-algebra representation for n≥3 forces the Riemannian curvature to vanish. Differentiating the facet relation tangentially forces the facet second fundamental form to vanish. These stronger conclusions are not needed for the Euclidean application, whose pullback metric was already flat.

Odd dimensionality is essential in the base index argument: in even dimension the Clifford volume operator gives a nonzero matrix anticommuting with all generators. For an even n≥4, apply the odd-dimensional argument to P×[-1,1] with the product metric. Scalar curvature is unchanged; the side mean curvatures are unchanged; the end faces are totally geodesic; and all new adjacent angles are pi/2 for both metrics. The full-dimensional compact convex hypothesis and neighborhood smoothness persist. The resulting old-angle equalities restrict to P×{0}.

Dimension two is independent. A face-preserving smooth planar competitor is an embedded disk with a piecewise-smooth Jordan boundary. With counterclockwise orientation and the specified outward-normal convention, the signed turning curvature k equals the face mean curvature (positive for a circle). Gauss–Bonnet/turning gives

    sum_i (pi-theta'_i) + integral_boundary k ds = 2 pi.

The reference convex polygon has sum_i(pi-theta_i)=2 pi. Since every theta'_i≤theta_i and k≥0, all inequalities must be equalities. Continuity then gives k=0 along every smooth edge, though only angle equality is required. The angle comparison also excludes reflex competitor corners. In dimension one there is no codimension-two face at which the required strict inequality could occur.

Thus all dimensions covered by the original Euclidean problem are handled without a hidden dimension upper bound. Simplicity and acute reference angles are not required.

## 10. Source-status and provenance limits

The accepted route is Bi's new smooth-approximation proof with Brendle's published smooth-boundary input. The fact that WXY has a similarly sufficient theorem is not an independent certificate. Bär–Hanke–Schick arXiv:2202.05180v2 explicitly targets WXY version 2 in its counterexamples and states that version 6 remains under verification. Both distinctions were checked against the actual note. This neither refutes WXY version 6 nor validates it. WXY's full proof was not independently audited here and is not a dependency of this verdict.

Bi's version-pinned arXiv page and its current unversioned page showed only v1 dated August 6, 2026. The author's publication page listed this item by arXiv identifier. No journal acceptance was verified. A bounded search did not identify a correction relevant to the checked proof; this is not a comprehensive literature-clearance claim. Brendle's publication details were independently confirmed by both the author's publication page and the publisher's article landing page. The inspected proof was the author final arXiv v4 PDF, not the publisher PDF.

The current UnsolvedMath detail page, full raw AI corpora, target-specific AI reports, repository-wide branch contents, and all historical attempts were not reverified by this independent audit. The target mapping and rank are supplied identifiers. The primary Gromov source establishes the mathematical question, while the frozen packet establishes exactly what was submitted for review. The audit does not turn earlier retrieval failures or partial prior-attempt searches into affirmative evidence of full provenance clearance.

Suggested source/copy edits to a future packet revision:

1. Keep the explicit ambient smooth-up-to-corners category in the title/status and conclusion; add Gromov's earlier ambient-extension definition as supporting context.
2. Correct the 2017 source title from “about” to “around.”
3. State that the mathematical review found no remaining gap in the specified route, while separately preserving the recent-preprint, non-peer-review, and non-formal-verification status.
4. Keep uninspected dataset/detail-page and prior-attempt boundaries separate from the proof verdict.

No required mathematical repair to Bi's argument or to the packet's conditional application was identified. Broader smoothness interpretations remain outside the proven scope.

## 11. Public source bindings

The separate `AUDIT_SOURCE_BINDINGS.json` records exact fresh retrieval hashes, sizes, match results, and inspection scope. Principal public links:

- Gromov, *101 Questions, Problems and Conjectures around Scalar Curvature*, October 1, 2017, Section 22, printed p.60: https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf
- Bi, *Dihedral Rigidity for Convex Polytopes by Smooth Approximation*, arXiv:2608.06320v1: https://arxiv.org/abs/2608.06320v1
- Brendle, *Scalar curvature rigidity of convex polytopes*, arXiv:2301.05087v4: https://arxiv.org/abs/2301.05087v4
- Brendle publisher metadata, Inventiones Mathematicae 235 (2024), 669–708: https://link.springer.com/article/10.1007/s00222-023-01229-x
- Bär–Hanke–Schick, remarks on the WXY paper, arXiv:2202.05180v2: https://arxiv.org/abs/2202.05180v2
- Gromov, *Dirac and Plateau Billiards in Domains with Corners*, September 20, 2013 author manuscript, Section 1, pp.2–3: https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/Plateauhedra_modified_apr23.pdf

This authored report contains review conclusions and independently explained mathematical derivations. It includes no source PDF, source transcription, source image, raw dataset record, or private coordination file.
