# Independent geometry and smoothing audit: PR932 / problem 30003471

## Verdict and exact scope

The geometric mechanism in original PROOF.md Sections 3–6 and the degree component of Section 7 survives this independent adversarial reconstruction. I found no required mathematical repair within that scope. The proof does allow nonsimple vertices. Its constants and the phrase “sufficiently large lambda” depend on the fixed polytopes; no uniformity over all realizations or all combinatorial types is established or needed.

This is a conditional family verdict, not acceptance of the whole candidate. The specialized smooth-domain Dirac existence/energy statement (2.1), including applicability to smooth convex bodies with flat patches, is an explicit outside dependency. I did not verify its source, index sign, representation conventions, or analytic limit/Clifford argument. No historical audit verdict or metadata status is a premise. No novelty, current-open, priority, or journal-acceptance conclusion is drawn.

The strongest independently verified geometric statement is:

> For fixed compact full-dimensional convex 3-polytopes P,Q with a fixed face-lattice correspondence and interior dihedral angles theta_P <= theta_Q at every corresponding edge, there are smooth convex inner bodies P_lambda tending to P by uniformly bi-Lipschitz radial maps, and smooth degree-one maps eta_lambda: boundary P_lambda -> S^2, such that W_lambda=(||d eta_lambda||_tr-H_lambda)_+ tends to zero in L^2 of the actual smoothed boundary. The trace quadratic-form bound (6.5) follows with constants independent of lambda. These furnish the geometric hypotheses and vanishing boundary error needed by precisely the conditional analytic statement (2.1).

The original OWR question is weaker than the candidate normal-Gram rigidity theorem. It asks for some corresponding edge with theta_P <= theta_Q; strict domination at every edge is its negation. This audit does not add equality of face metrics, equal edge lengths, simplicity, or a vertex-smooth boundary equivalence.

## Pins, independence, and sources actually inspected

- Original immutable Git head: `c09ef9df8b1f4642be0396ba6343344be8fa25b0`.
- Original proof SHA256: `6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415` (21,855 bytes).
- Original outer publication-manifest SHA256: `d1b3a0528bf518640a117c2cfecff5bc81d21f58632f7b4f647ae998eb4dcedd`.
- All 29 selected original regular files were compared byte-for-byte with their actual Git blobs at that head and the audit's original disk copy. Start/end authentication records are public here. Historical audit files were hashed for authentication, but their text/verdicts were never read.
- Read in full: RESEARCH_CHARTER.md; source_record_private.txt (exact cached target, including its supplied original statement); the complete original public/PROOF.md. Wrote INITIAL_RECONSTRUCTION.md before consulting any historical audit verdict. No historical verdict or current sibling family folder was consulted at any point.
- Charter SHA256: `5c485826b0eda9e28a18797bcb3ea0c586314e3aac4da46cf9094413f788bd71`.
- Private cached source-record SHA256: `aa4d1332349687f3e0eee690f8a5ad26f81e298425afd4d9b0baea349a8a2355` (4,411 bytes). The body is excluded from this family's public map.
- Supplied primary target URL: https://publications.mfo.de/bitstream/handle/mfo/3583/OWR_2017_19.pdf?isAllowed=y&sequence=1 (OWR 2017/19, printed p.1198, problem 4). This family inspected the full supplied cached statement, not the external PDF or page pixels. Exact external-source authentication belongs to the root/source family.
- The proof names Brendle arXiv:2301.05087v4 / DOI 10.1007/s00222-023-01229-x for (2.1). This family did not inspect that paper or use it as a proved premise beyond the explicit conditional assumption. Bi and Wang–Xie–Yu are not dependencies of the independent geometric deductions below. No external pages, source bodies, or rendered page images were downloaded by this family.

Original author proof-search accounting remains recorded 1/5. This audit adds 0 author proof-search turns. It supplies detailed verification and finite falsification controls for the already proposed mechanism, without introducing a materially new discovery route. No person, other shard, or other agent was contacted; communication was only to the parent/root audit.

## 1. Face correspondence, simultaneous hemispheres, and orientation

For each proper nonempty face choose an interior point, and cone its already triangulated boundary to that point. Induction over dimension gives the face-chain triangulation of the boundary. The identical abstract face-chain complex for Q gives a simplicial homeomorphism f. Every top-dimensional simplex is nondegenerate. There are finitely many simplices, so f and its piecewise-affine inverse are Lipschitz in intrinsic boundary length. A fixed convex polyhedral boundary has intrinsic and ambient distances comparable; equivalently one can use a finite Lipschitz chart cover and compactness away from the diagonal. Thus the asserted ambient bi-Lipschitz property is valid. In fact only continuity and face preservation are needed for the later hemisphere construction.

A boundary homeomorphism has orientation degree +1 or -1. A Euclidean reflection of Q reverses that sign. Its action on facet normals is the same orthogonal reflection, preserving every target Gram entry and dihedral angle. It therefore does not alter the proposed conclusion or the hypothesis. After this correction, radial projection of Q to S^2 is orientation preserving and q_0=f/|f| has degree +1.

Translate the origins into both interiors. For x in the whole closed facet F_i, f(x) is in G_i, so

    m_i . q_0(x) = k_i / |f(x)| >= min_i k_i / max_Q |y| > 0.

There is no requirement to select one incident facet at a vertex. The same inequality holds simultaneously for every incident facet, including all four side facets of a square-pyramid apex or an arbitrary finite number of facets at a high-valence vertex. This directly avoids the potential incompatibility of choosing unrelated target-normal directions at vertices.

The source radial projection rho_P is Lipschitz on a fixed collar disjoint from the origin. To see this directly, write rho_P(r u)=rho(u)u. The reciprocal radial function is the support function of the polar body and is Lipschitz and positively bounded; hence rho is Lipschitz. The extension q_0 composed with rho_P is therefore continuous (indeed Lipschitz). Smooth approximation can be performed in ambient R^3 before normalization. Uniform approximation within less than the fixed positive hemisphere margin keeps the vector norms away from zero. Finite compact closed facets yield one neighborhood size and one positive lower margin. Normalized straight interpolation gives the homotopy on a fixed smaller collar. This does not assert differentiability of the PL map at a vertex.

All q derivatives needed later are bounded on one compact subcollar, independent of lambda. The simultaneous inequalities apply to every active facet once the face-distance estimate below places x within O(1/lambda) of that facet.

## 2. Cutoff, regular smooth inner bodies, and actual radial displacement

A concrete valid cutoff is obtained from

    Phi''(s) = C exp(-1/(s+2)) for s>-2,
    Phi''(s) = 0 for s<=-2,

by integrating twice with Phi(-2)=Phi'(-2)=0 and choosing C so Phi(0)=1. Every derivative is flat at -2. Phi'>0 for s>-2 and Phi''>=0. It follows that F_lambda is smooth convex, and F_lambda<=1 forces all u_i<=0. A fixed ball about the origin has all u_i bounded above by a fixed negative number; for large lambda its F_lambda is zero. Thus the bodies are compact, full dimensional, convex, and contained in the original P.

Let h_min=min_i h_i and let R be an outer radius of P. For active facets at x in P,

    x . n_i >= h_min - 2/lambda >= h_min/2.

For any nonnegative coefficients a_i on the active set,

    |sum a_i n_i| >= (h_min/(2R)) sum a_i.

On F_lambda=1, replace inactive arguments by -2. The vector of arguments lies in the compact set [-2,0]^N subject to sum Phi=1. On that set sum Phi' has positive minimum: if it vanished every argument would be -2, contradicting sum Phi=1. Therefore |grad F_lambda|>=c lambda. This proves regularity of the entire level set, including the boundaries of flat patches. Smoothness does not require a positive definite shape operator.

For y in boundary P and a>=2/h_min,

    u_i((1-a/lambda)y)
      = (1-a/lambda)u_i(y) - (a/lambda)h_i <= -2/lambda.

This contracted point is in P_lambda. The point y lies outside or on its radial boundary because some u_i(y)=0 gives F_lambda(y)>=1. Convexity and the interior ball give one radial boundary point Pi_lambda(y), between these two points. Consequently

    |Pi_lambda(y)-y| <= a R/lambda.

This establishes the claimed displacement for the actual radial map, rather than an arbitrary nearby correspondence. The raywise extension T_lambda has the same bound throughout P.

## 3. Uniform global bi-Lipschitz maps, surface Jacobians, and trace transport

If every K lies between B_r and B_R, then K's polar lies between B_(1/R) and B_(1/r). On S^2, its support function h_(K polar)=1/rho_K is Lipschitz with constant at most 1/r and lies in [1/R,1/r]. It follows that rho_K has a uniform positive lower bound and a uniform Lipschitz bound, for example R^2/r. This applies to both P and every sufficiently large P_lambda.

The angular ratio a_lambda(u)=rho_(P_lambda)(u)/rho_P(u) and its reciprocal have uniform positive bounds and uniform Lipschitz constants. The maps

    T_lambda(su)=s a_lambda(u)u,  s>=0,

are uniformly Lipschitz on all R^3: for x=s u, y=t v with s>=t, the difference is bounded by a_max|x-y|+Lip(a)t|u-v|, and t|u-v|<=|x-y|. The identical argument for 1/a proves a uniform Lipschitz inverse. The formula is valid at the origin by continuity, despite the lack of differentiability there. Sobolev composition only needs bi-Lipschitz regularity.

A bi-Lipschitz boundary map has area Jacobian bounded above and below almost everywhere by constants determined by its Lipschitz bounds. Thus transporting the fixed Lipschitz-domain H1-to-L4 trace inequality from P gives (4.2). Composing a fixed H1 extension from P with the global radial inverse gives the asserted uniformly bounded H1 extension from P_lambda to a common ball. The volume and surface Jacobian bounds used in this reasoning do not require convergence of derivatives of T_lambda.

For an independent local check, at a regular source facet point y, put x=Pi_lambda(y)=t y and u=y/|y|. Its exact area ratio is

    J_surface = t^2 (n_i . u)/(nu_lambda . u).

The denominator is positive because the common interior ball separates all supporting planes from zero. The controls compare this formula with finite differences on flat and genuinely rounded patches; this check supplements rather than replaces the global argument.

## 4. Error bound for every face type, empty intersections, and nonsimple vertices

Here is a fully expanded version of the proof's linear-inequality error bound. Fix J with nonempty F_J. For x in P choose its nearest point y in F_J and let v=x-y. Let L be the other inequalities active at y. The normal cone is

    N_(F_J)(y) = span{n_j:j in J} + cone{n_l:l in L}.

This cone is closed: it is generated by finitely many vectors, allowing both signs of the equality normals. Finite generated cones in finite dimension are closed; one may reduce every representation to linearly independent generators and take the finite union of the resulting closed cones. The normal-cone formula also follows directly by separation: a vector outside the displayed cone is separated by w satisfying n_j.w=0 and n_l.w<=0, so y+epsilon w is feasible for sufficiently small epsilon; this contradicts the nearest-point projection inequality. Thus no constraint qualification or simple-vertex assumption has been smuggled in.

For l in L, feasibility of x gives n_l.v=u_l(x)<=0. At each fixed active face type consider unit w in that cone satisfying these same feasible inequalities. If all n_j.w vanished, its cone representation would give

    1=|w|^2=sum a_j(n_j.w)+sum b_l(n_l.w)<=0,

where a_j are arbitrary real numbers and b_l>=0. This is impossible. Compactness of the intersection with the unit sphere gives a strictly positive minimum of max_j |n_j.w|. There are finitely many active face types and finitely many J, giving fixed constants. Since n_j.v=u_j(x), this proves exactly

    dist(x,F_J) <= C_J max_(j in J) |u_j(x)|,  x in P.

For empty F_J, continuity on compact P gives a positive minimum of max_j |u_j|. There are finitely many J. Hence, beyond one threshold depending on P, the active set I_lambda has nonempty common intersection. This is not valid for every finite lambda or uniformly over all polytopes, and the proof does not assert either stronger statement.

Every actual ridge of a 3-polytope lies in exactly two facets. A transverse planar section at its relative interior is a wedge with two boundary rays; every facet through the ridge supplies one of those rays. Therefore three or more distinct active facets have common intersection at a vertex. The distance bound puts x within C/lambda of that vertex. Two active facets that meet only at a vertex obey the same bound; empty intersections have already been excluded. Thus outside those neighborhoods there is one facet, or exactly one adjacent pair. This applies to non-simple vertices without choosing three preferred facets or inverting a possibly dependent 3-by-3 matrix of normals.

The controls deliberately retain 32 finite-scale samples on a valence-32 pyramid with empty active common intersection at lambda=64. The sampled obstruction disappears at the tested larger scales. This is a useful falsification of an incorrect uniform-scale reading, not a counterexample to the stated asymptotic localization. The universal proof is the finite-face compactness argument above.

## 5. Exact two-facet nuclear norm and smooth global gluing

Adjacent normals have exterior angles alpha,beta in (0,pi), and theta_P<=theta_Q means beta<=alpha. A positive combination of the two source normals follows the unique minor great-circle arc. Use the fixed basis

    e=(n_j-cos(alpha)n_i)/sin(alpha),
    nu=cos(a)n_i+sin(a)e,  0<=a<=alpha.

The fractional coordinate is s=a/alpha. The target map is

    zeta=cos((beta/alpha)a)m_i + sin((beta/alpha)a)E,
    E=(m_j-cos(beta)m_i)/sin(beta).

Along the source arc, a is a smooth atan2 coordinate. The closed arc excludes the atan2 branch cut at -n_i since alpha<pi. Near the initial endpoint one can use

    a=atan2(b sin(alpha), a_i+b cos(alpha)),

with a_i=Phi'(lambda u_i)>0 and b=Phi'(lambda u_j)>=0. This is smooth in b near b=0. Reverse the roles near the other endpoint. No differentiation of arccos(n_i.nu) at 1 is needed.

The Hessian of F is a nonnegative sum of the two normal tensors. On the two-dimensional tangent plane its restriction has the edge direction as kernel, so the shape operator d nu is positive semidefinite of rank at most one. Thus ||d nu||_tr=tr(d nu)=H. The displayed arc parametrizations give

    ||d zeta||_tr = beta |ds| = (beta/alpha) H <= H,

including points with H=0. This is an equality for the nuclear norm, not merely an operator-norm estimate incorrectly substituted for it. With one active facet both maps are constant and H=0.

A possible concern is gluing many different pair formulas at a one-active point. There a_i stays positively bounded in a neighborhood. For each potentially activating j, the difference between its pair formula and the constant m_i is a smooth function of a_i and the flat function b_j=Phi'(lambda u_j), vanishing to all orders where lambda u_j=-2. Locally sum these finitely many differences with m_i. On the actual boundary outside the removed vertex neighborhoods at most one b_j is positive, so this smooth local expression equals exactly the prescribed pair/constant map. This proves smoothness even where several pair-chart closures meet at one-active points. At two-active points the pair is locally fixed; at three-active points the construction has already been removed. Order independence follows from reversing both fractional arc coordinates. This supplies the compatibility needed for one global smooth zeta on the complement.

For fixed P,Q, possibly small sin(alpha) or sin(beta) does not cause a mathematical singularity: both are nonzero for an actual adjacent pair, and there are finitely many pairs. Constants need not remain bounded as a sequence of different polytopes degenerates. Exact alpha=0 or pi is outside the facet/edge hypotheses.

The target arc is a positive sine-weighted sum of m_i,m_j. The weights sum to at least one (its unit norm is at most their sum). Consequently q.zeta>=c whenever q has the simultaneous margin against the endpoints. This verifies the hemisphere hypothesis using the same global q, including edge endpoints.

## 6. Geodesic cutoff, its exact contraction, and all endpoint smoothness

Choose delta=lambda^-1/4. Then delta^2=lambda^-1/2 and (1/lambda)/(delta^2)=lambda^-1/2 tends to zero. Distinct fixed vertices have disjoint 2delta balls for large lambda. All regions with three or more active facets lie strictly inside the inner delta^2 balls.

The proposed cutoff t(r), obtained by a fixed smooth flat step of log(r/delta^2)/|log delta|, satisfies the stated derivative bound. It is smooth at the two annular boundaries and is constant near r=0. The geodesic map G(q,z,t)=exp_q(t log_q z) is smooth whenever z is not antipodal to q, including q=z. Here q.z>=c implies theta<=arccos(c)<pi/2, a compact subset of that domain.

For fixed q, variation of z in the radial and transverse spherical directions has factors

    t,  sin(t theta)/sin(theta).

At theta=0 both factors have limit t. For 0<=theta<pi/2 and 0<=t<=1, monotonicity of sin on [0,pi/2] bounds the second factor by one. Therefore ||D_zG||_op<=1. The derivative in q is uniformly bounded by smoothness on the compact parameter set, and |D_tG|=theta<=pi/2. The nuclear norm ideal inequality gives

    ||d eta||_tr <= ||d zeta||_tr + C + C/(r |log delta|)

on the annulus, with tangential |dr|<=1. Inside, eta=q has bounded derivative and H>=0. Outside, eta=zeta has no positive error. This proves (6.2).

Flatness of t removes every derivative mismatch at its endpoints. Zeta is defined on an open neighborhood of each annular boundary because delta^2 is much larger than C/lambda. The inner construction q is globally smooth; the outer construction has the gluing just checked. Thus eta is one smooth map across every face/edge, chart overlap, and annular boundary. The expression involving theta is not taken as a nonsmooth formula at q=z: the smooth exp/log map or its smooth sinc extension defines that value and derivatives.

The hemisphere restriction is essential to this simple contraction claim. The negative control theta=2.4, t=0.65 gives sin(t theta)/sin(theta)=1.480379..., exceeding one. It is excluded here by the verified simultaneous hemisphere margin.

## 7. Actual-boundary L2 norm and form estimate

Set d_lambda=sup|Pi_lambda(y)-y|<=C/lambda. For large lambda, d_lambda<=delta^2/2. If x=Pi_lambda(y) is in the transition annulus, then

    delta^2/2 < |y-v| < 2delta,
    1/|x-v| <= C/|y-v|.

The indicator support r_x<delta also pulls back inside |y-v|<2delta. Only facets containing v meet this small source neighborhood, because every other closed facet is a positive distance from v. Uniform surface Jacobians reduce the integrals to planar source facets. On each such plane, polar integration centered at v yields

    integral_(c delta^2<r<C delta) 1/(r^2 |log delta|^2) dS
      <= 2pi log(C/(c delta))/|log delta|^2
      <= C/|log delta|.

The unweighted support has area O(delta^2), hence indicator L2 norm O(delta). Summing over finitely many vertices and facets proves

    ||W_lambda||_(L2(Sigma_lambda))
       <= C (delta + |log delta|^-1/2) -> 0.

This calculation is on the actual smooth boundary via the actual Pi_lambda map. It does not replace a boundary norm by small volume. It does not require pointwise bounds on analytic matrix fields. Hölder and the uniform H1-to-L4 trace bound give (6.5) exactly. A fixed relative-width cutoff would leave a nonzero limiting squared L2 norm: the model weight 1/delta on delta<r<2delta has planar integral 3pi. The logarithmic construction addresses this critical exponent.

The same reasoning is specifically a three-dimensional proof. In a four-dimensional cube three facets can meet along an edge, leaving an unremoved rank-two smoothing region outside vertex balls. A vertex-only cutoff and the rank-one pair formula therefore do not justify a general-dimensional version. The controls verify this simple obstruction to that extrapolation; it is not a counterexample to a separate higher-dimensional conjecture.

## 8. Global degree and the conditional analytic interface

Eta is globally homotopic to q restricted to Sigma_lambda. In the inner balls eta=q. Elsewhere every interpolant is within the verified open hemisphere about q. Normalized straight interpolation from eta to q is therefore a global homotopy, compatible at all boundaries.

The fixed collar homotopy from q to q_0 restricts to every sufficiently large Sigma_lambda. Radial projection Sigma_lambda -> boundary P preserves its boundary orientation; q_0 has degree one by construction. Thus eta has degree one on each smooth approximating sphere, not merely in a limiting sense.

The outward Gauss map also has degree one. The common interior ball implies nu(x).x>=r>0 at every boundary point. Consequently its normalized straight interpolation to x/|x| is defined everywhere. The radial map has degree one, including when the Gauss map is constant on flat patches. Since Sigma_lambda is a sphere, the usual degree classification of S^2 -> S^2 identifies eta and the Gauss map up to homotopy. Strict convexity is unnecessary for this topological argument.

This finishes the assigned geometric verification. If and only if the precise smooth-domain statement (2.1) is independently established with its stated hypotheses, these bodies/maps are admissible inputs and their boundary error is absorbable using (6.5). Whether that analytic result holds with the exact representation and orientation is not settled by this family. The later nonzero parallel limit and Gram conclusion are outside this family's assigned verification.

## Controls, reproduction, and honest limits

`geometry_controls.py` uses NumPy/SciPy with fixed seed 93230003471. The recorded run used Python 3.14.6, NumPy 2.3.5, SciPy 1.17.0, with the already existing shared scientific runtime; no runtime was installed or altered. It checks a cube, regular tetrahedron, nonsimple square pyramid, and valence-12 and valence-32 pyramids at lambda=64,256,1024,4096. Vertex rays force the nonsimple active sets. A nonorthogonal positive-determinant affine shear supplies independently realized target normals to test simultaneous incident-facet margins; no global angle-dominance conclusion is inferred from that shear.

The sealed controls include 369 two-active samples and 446 genuinely curved radial-Jacobian samples. The maximum recorded edge nuclear-norm relative residual is 2.09e-14, radial-Jacobian finite-difference error 1.71e-8, and spherical derivative singular-value error 3.18e-11. These are numerical consistency residuals, not certified error enclosures.

Further controls compare edge nuclear norms, radial area Jacobians including curved patches, arc coordinates at endpoint/near-degenerate fixed angles, geodesic endpoint derivative singular values (including q=z), the scale separation, and exact planar logarithmic integrals. False statements are explicitly detected by removing the hemisphere, reversing angle comparison, replacing logarithmic transition by a fixed relative width, or extrapolating vertex-only smoothing to dimension four.

These are ordinary floating-point diagnostics, not interval enclosures, formal proofs, exhaustive searches, or validated numerical certification of a universal claim. Their purpose is to falsify wrong formulas and test implementation consistency. The universal claims rest on the checkable deductions above. The JSON records roundoff residuals and the finite-lambda empty-intersection examples. Initial harness runs exposed an antipodal zero test direction and a floating-point root-bracket endpoint; both were fixed as harness issues before the sealed run. The coarse-lambda empty-intersection case was retained as an intentional boundary test.

To reproduce with the recorded existing runtime, from this folder run:

    /Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python geometry_controls.py

Any compatible Python with NumPy/SciPy can instead run the script; do not expect byte-identical floating-point JSON across versions/platforms. Original authentication and public-map verification use Python standard library only. Run:

    python3 VERIFY_ORIGINAL.py
    python3 VERIFY.py --manifest-sha256 EXTERNALLY_SUPPLIED_MANIFEST_SHA256

The map verifier requires an external digest and checks its fixed explicit allowlist before trusting any mapped executable file. MANIFEST.json is self-excluded. Private sources, rendered pages, tmp files, caches, and any unmapped files are excluded from the public packet. Do not infer a publication allowlist by scanning this folder.

No required issue or internal mathematical gap remains in the assigned conditional geometric lemma. The exact remaining whole-proof dependency is the independently unverified analytic statement (2.1) and the unassigned later analytic/algebraic steps. This report authorizes no acceptance, solved classification, publication, PR change, release, or external communication.
