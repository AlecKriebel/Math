# PR932 independent mathematical recheck

Immutable input: `c09ef9df8b1f4642be0396ba6343344be8fa25b0`, prefix `unsolved_math_prioritization/attempts/30003471/`. Review completed 2026-10-21 UTC. The entire 29-file prefix was independently compared byte for byte with this Git object; see `SOURCE_BINDINGS.json` and `EVIDENCE.py`.

## Outcome and exact scope

**No substantive mathematical gap or counterexample was found in this bounded independent review.** I recovered a complete conditional derivation of the proposed three-dimensional implication from Brendle's smooth-domain propositions and the explicitly identified standard functional-analytic foundations. In particular, the vertex cutoff, including nonsimple vertices, has the required norm on the actual smoothed boundary. I did not merely replay the author's finite controls.

The exact proposed theorem is this. Let P and Q be bounded, full-dimensional convex polytopes in R3, with a fixed face-lattice isomorphism, and let n_i and m_i be the corresponding outward unit facet normals. If every corresponding edge satisfies theta_P(i,j) <= theta_Q(i,j), for **interior** dihedral angles, then n_i dot n_j = m_i dot m_j for every pair of facets, including pairs that do not share an edge. No simplicity assumption is needed. The statement does not determine support numbers, face sizes, edge lengths, or overall scale.

This is a mathematical recheck conditional on the imported smooth Dirac result and standard Sobolev/elliptic tools, not a formal proof certificate, human peer review, publication decision, or priority/novelty clearance. The recent Bi and Wang–Xie–Yu manuscripts cited in the candidate are not needed as black boxes for the derivation checked here. Their asserted results were not independently audited by this review.

I read no historical audit conclusions, acceptance files, or closure rationale. `INITIAL_ANALYSIS.md` records the independent attack plan before primary verification. No external communication or shared Git/PR/provider/ledger mutation was performed.

## Original question recovered independently

The primary [OWR report](https://publications.mfo.de/bitstream/handle/mfo/3583/OWR_2017_19.pdf?isAllowed=y&sequence=1), printed p.1198, problem 4, asks whether two combinatorially equivalent convex polytopes in R3 have a corresponding edge pair whose first interior dihedral angle is no larger than the second; it also gives an all-equal alternative. [Akopyan–Karasev v2](https://arxiv.org/pdf/1505.05263v2), Conjecture 5.1, printed p.5, poses the analogous existence assertion for codimension-two faces in Rd. The present proof addresses the dimension-three OWR question, not that full higher-dimensional conjecture. The all-equal alternative adds no logical cases to the weak existence assertion.

Indeed, negating the weak existence assertion gives theta_P(e) > theta_Q(e) for every edge. Apply the proposed theorem to (Q,P); it forces equality and contradicts these strict inequalities. Thus the stronger theorem implies the exact original target.

Primary PDFs were downloaded afresh and their complete bodies are ignored under `private/`. `SOURCE_BINDINGS.json` records URLs, byte counts, and hashes without redistributing those bodies.

## Specialized imported input and conventions

I inspected [Brendle v4](https://arxiv.org/pdf/2301.05087v4), Section 2: Definitions 2.2/2.7, Lemma 2.8, Proposition 2.9 (printed pp.8–9), Proposition 2.14 (pp.10–11), and Proposition 2.15 (pp.11–12). The hypotheses of the last proposition are a compact smooth convex domain, a metric on a neighborhood, odd dimension, and a smooth sphere map homotopic to the Euclidean Gauss map. It gives index at least one. Proposition 2.14 gives a smooth kernel. With zero scalar curvature and a harmonic kernel element, Proposition 2.9 yields

    integral_Omega |grad A|^2
       <= (1/2) integral_boundaryOmega (||d eta||_tr - H)_+ |A|^2.

Its mean curvature is the sum of the principal curvatures and is positive for a sphere. These smooth propositions impose neither strict convexity nor polyhedral angle matching. The separate polytope theorem's matching-angle hypothesis is therefore not being silently imported.

For the matrix translation, write the two spinors as the columns of A. The coefficient identity in the proof of Proposition 2.15 is c(e_a)e_alpha = sum_beta omega_a,alpha,beta e_beta. Hence the tuple-index action transposes when acting on the column matrix, giving

    chi(A) = -c(nu) A c(eta).

Thus chi(A)=A is exactly c(nu)A=A c(eta). One must keep this transpose; identifying the tuple-index array directly with the column action is not the coordinate calculation. The Pauli choice c(e_j)=-i sigma_j satisfies c(v)c(w)+c(w)c(v)=-2(v dot w)I and c(e_1)c(e_2)c(e_3)=-I. Applying the same convention on both sides makes the constant identity matrix satisfy the round-sphere boundary condition. Simultaneously replacing c by -c changes the Dirac operator's sign and leaves this condition and its kernel unchanged. No orientation sign is obtained by mixing conventions.

## Independently checked geometric construction

### A compatible degree-one map, including all incident facets

Translate interior points of both polytopes to zero and write their facet inequalities as n_i dot x <= h_i and m_i dot y <= k_i, with every h_i,k_i positive. The barycentric subdivisions of their boundaries give a PL homeomorphism f sending each closed facet F_i onto G_i. Reflect Q if this homeomorphism reverses orientation. This preserves all target Gram entries and all angles, while making its degree positive.

The sphere map q_0(x)=f(x)/|f(x)| then has degree one. For every x in F_i,

    q_0(x) dot m_i = k_i/|f(x)| >= min_i k_i / max_Q |y| > 0.

At a nonsimple vertex this holds for every incident facet simultaneously. This is the critical compatibility fact; it does not require a spherical triangulation or a short extension of a normal-fan vertex polygon. Radial projection to boundary P gives a Lipschitz collar extension. Uniform smoothing followed by normalization preserves a common positive margin near each closed facet, since the number of facets is finite and the unnormalized map stays away from zero. The homotopy is normalized straight interpolation. The resulting fixed q has bounded derivatives on a compact subcollar.

### Smoothing and uniform transport

For the candidate's flat convex cutoff Phi, let F_lambda=sum_i Phi(lambda(n_i dot x-h_i)) and P_lambda={F_lambda<=1}. If any defining affine function is positive, the corresponding Phi term exceeds one, so P_lambda is contained in P. For sufficiently large lambda, the origin and a fixed ball lie where every summand is zero. Boundedness follows from containment in P.

On its boundary, active arguments lie in (-2,0], and their Phi values sum to one. Compactness of the set of such argument lists gives sum_active Phi' >= b>0. If x is active for i, n_i dot x >= h_min-2/lambda >= h_min/2. Consequently, writing a_i=Phi'(lambda u_i),

    |sum_i a_i n_i| |x| >= (sum_i a_i) h_min/2.

Since |x| is uniformly bounded above, |grad F_lambda| >= c lambda. This proves smoothness even where the boundary has a flat patch.

For y in boundary P, replace y by (1-a/lambda)y. For a fixed a >= 2/h_min and sufficiently large lambda,

    u_i((1-a/lambda)y)
      = (1-a/lambda)u_i(y) - (a/lambda)h_i <= -2/lambda.

Thus the radial location of boundary P_lambda differs from y by O(1/lambda). All bodies stay between the same concentric balls. Their radial functions r(omega) are uniformly positive and Lipschitz: 1/r is the support function of the polar body, whose radius is bounded by the reciprocal inner radius. Therefore s_lambda(omega)=r_lambda(omega)/r_P(omega) and 1/s_lambda are uniformly bounded and Lipschitz. The ray map T_lambda(x)=s_lambda(x/|x|)x, with T_lambda(0)=0, and its inverse are uniformly Lipschitz on all of R3.

The two-dimensional area formula gives uniform upper and lower surface-Jacobian bounds for the induced boundary maps. The H1 chain rule and this area control transport the fixed-polytope trace inequality into

    ||a||_L4(boundary P_lambda)^2
       <= C (||grad a||_L2(P_lambda)^2 + ||a||_L2(P_lambda)^2).

The same maps, a fixed bounded H1 extension from the Lipschitz domain P, and a fixed containing ball supply uniformly bounded extensions for all lambda. These are norm statements, not a claim that the maps or the extensions converge smoothly near corners.

### Active-set localization and nonsimple vertices

For every facet subset J with nonempty F_J, the needed estimate is the finite-dimensional linear error bound

    dist(x,F_J) <= C_J max_j in J |u_j(x)|,  x in P.

Here is a direct check of its mechanism. At a closest point y in F_J, v=x-y belongs to the normal cone of F_J, a span of equality normals plus a nonnegative cone of the remaining active inequality normals. Feasibility gives n_l dot v <=0 for the latter normals. A unit limiting v annihilating all equality normals would have v dot v <=0 after pairing with its cone representation, a contradiction. There are finitely many active face types, giving a uniform positive bound. If F_J is empty, compactness instead gives a positive residual minimum.

For active facets the residual is at most 2/lambda. Hence their common intersection is nonempty, for large lambda, and is O(1/lambda) away. An edge of a convex 3-polytope is incident to exactly two actual facets; three distinct facets with nonempty common intersection meet at a vertex. Pairs that meet only at a vertex are likewise localized there. Enlarge the common finite constant C to cover these pairs as well as triples. Outside the C/lambda vertex balls there are only one-active facet regions and two-active adjacent-facet regions. This argument allows arbitrarily many facets at a vertex.

### Exact edge estimate and smooth gluing

Let alpha=arccos(n_i dot n_j)=pi-theta_P and beta=arccos(m_i dot m_j)=pi-theta_Q. Thus beta<=alpha, with alpha,beta strictly between zero and pi for actual adjacent facets. On a two-active rounded edge, the Gauss normal lies on the minor source great-circle arc; write its fractional arclength as s. Map it to fractional arclength s on the target minor arc. Since both maps depend on the same scalar s,

    ||d zeta||_tr = beta |ds|,
    ||d nu||_tr = alpha |ds| = H,
    ||d zeta||_tr = (beta/alpha)H <= H.

The second equality uses convexity and the rank-at-most-one shape operator in the region invariant along the edge direction. It includes zero curvature. On a one-active patch, zeta is the constant target normal and H=0.

At the cutoff threshold the disappearing Phi' has every derivative zero. Local angle coordinates on the source great circle are smooth at each endpoint, so the edge map glues to the constant facet map with all derivatives. Other pair charts either meet at such a constant patch or in the removed vertex region. For each fixed P,Q, angles can be close to zero or pi; constants may be large but finite, which is enough. No uniform assertion over degenerating families is needed.

Target minor-arc interpolation is a positive sine-weighted sum of the two endpoints. If q dot m_i,q dot m_j >=c, its dot product with zeta is at least c because those weights sum to at least one. Thus q and zeta stay in a common strict hemisphere. This is what permits the next construction without amplifying H.

## Vertex cutoff on the actual rounded boundary

Choose delta=lambda^(-1/4). The inner cutoff radius delta^2=lambda^(-1/2) is much larger than C/lambda; the edge map exists throughout the transition annulus. A flat smooth cutoff in log r changes from zero to one between delta^2 and delta and has |dt/dr|<=C/(r|log delta|).

For G(q,z,t)=exp_q(t log_q z), hold q fixed and set theta=dist(q,z)<pi/2. Its derivative with respect to z has singular values

    t,  sin(t theta)/sin(theta).

Both are at most one: t<=1 and sine is increasing on [0,pi/2]. Its q derivative is uniformly bounded on the fixed strict-hemisphere parameter set, and its t derivative has norm theta. The trace-norm ideal property and triangle inequality consequently give

    ||d eta||_tr <= ||d zeta||_tr + C + C/(r|log delta|).

Subtract H and take the positive part. Outside all vertex delta balls the error is zero; inside the inner balls eta=q and the error is bounded because H>=0. It follows that

    W=(||d eta||_tr-H)_+
      <= C sum_v [1_{r_v<delta}
                  + 1_{delta^2<r_v<delta}/(r_v|log delta|)].

This estimate has no hidden multiple greater than one in front of the large rounded-edge curvature. Such a multiple would destroy the argument. The strict hemisphere and exact arclength contraction prevent it.

To compute the norm, pull back by the radial boundary map Pi_lambda. Its displacement h=O(1/lambda) obeys h=o(delta^2), so on the annular support r=|Pi_lambda(y)-v| and rho=|y-v| differ by at most h and are comparable. Uniform surface Jacobians reduce the squared weighted integral to planar facets through v, where it is bounded by

    C/|log delta|^2 integral_(c delta^2)^(C delta) (d rho/rho)
       <= C/|log delta|.

Facets not incident to v have positive distance from it and eventually do not occur. The squared norm of the indicator is at most C delta^2, so

    ||W||_L2(boundary P_lambda)
       <= C(delta + |log delta|^(-1/2)) ->0.

The key exponent is correct: the boundary has dimension two. Combining this L2 bound with the uniform L4 trace gives

    integral_boundary W|A|^2 <= o(1)(integral_Plambda |grad A|^2
                                     + integral_Plambda |A|^2).

Thus small boundary area alone is not the justification. The actual critical norm and uniform trace inequality provide the required quadratic-form bound.

## Degree, harmonic fields, and nonzero limit

All interpolants stay in the hemisphere centered at q. They give a global homotopy of eta to q, including inner vertex balls where eta=q. The collar homotopy and the orientation-preserving radial identification then give degree one. The Gauss map of smooth boundary P_lambda also has degree one: if a fixed ball of radius r_0 lies inside, its supporting-plane inequality gives nu(x) dot x >=r_0, so it is homotopic by normalized straight interpolation to the radial sphere map. The boundary is a sphere, and maps S2 to S2 of the same degree are homotopic.

The imported index proposition therefore supplies a nonzero smooth harmonic matrix A_lambda with the stated boundary condition. Normalize its squared L2 norm to one. The imported energy inequality and preceding form bound give

    E_lambda <= o(1)(E_lambda+1),

so E_lambda tends to zero by absorption. Uniform extensions B_lambda are H1-bounded on one fixed ball. Rellich gives a subsequence converging strongly in L2. Every compact subset of the interior of P is eventually contained in P_lambda, so the limit has zero weak gradient there and equals one constant matrix C.

This limit is not allowed to vanish by losing all mass near the boundary. Strong L2 convergence implies |B_lambda|^2 -> |B|^2 in L1. Also 1_Plambda -> 1_P almost everywhere: interior points eventually have every cutoff term zero, and P_lambda is contained in P. Dominated convergence against |B|^2 plus the L1 convergence then gives

    1 = lim integral_Plambda |B_lambda|^2
      = integral_P |B|^2 = vol(P)|C|^2.

Thus C is nonzero. This is a global mass argument; no unjustified pointwise spinor bound or trace at a vertex appears.

For any facet choose a relatively compact open patch in its relative interior and a fixed interior half-ball meeting that patch. For all sufficiently large lambda, the other facet terms vanish there, the rounded boundary agrees exactly with the facet plane, eta=m_i, and the half-ball lies inside P_lambda. Strong L2 convergence plus E_lambda ->0 gives strong H1 convergence to C on this fixed half-ball. Continuity of the trace passes the boundary relation to the limit:

    c(n_i)C = C c(m_i), for every facet i.

Every actual facet has such a patch, independently of vertex valence.

## Final Clifford argument and a harmless simplification

The candidate's adjoint calculation is correct: C* c(n_i)=c(m_i) C*, so C*C commutes with every c(m_i). Boundedness of Q makes its normals span R3. The irreducible two-dimensional Clifford representation then gives C*C=aI, a>0, so C is invertible.

In fact invertibility is unnecessary for the asserted conclusion. Directly multiplying the facet identities twice gives

    [c(n_i)c(n_j)+c(n_j)c(n_i)] C
       = C[c(m_i)c(m_j)+c(m_j)c(m_i)],

and therefore

    -2[(n_i dot n_j)-(m_i dot m_j)] C = 0.

Since C is nonzero and the bracket is a scalar, every bracket vanishes. This independently verifies the last inference with less algebraic dependency. It is a simplification, not a required repair.

## Adversarial route ledger and boundary cases

| Attack family | Mechanism tested | Evidence and status | Exact remaining dependency |
|---|---|---|---|
| Counterexample / excessive strength | Prisms, support variations, normal-fan polygon flexibility, nearly degenerate edge angles | No counterexample found. Boxes of different aspect ratios verify why support/length rigidity is not claimed. No arbitrary global Lipschitz extension of vertex polygons is assumed. | No exhaustive numerical counterexample search was undertaken; the proof, rather than sampled geometry, is the evidence for the full claim. |
| Degree / nonsimple compatibility | Orientation-reversing correspondence, many incident facets | Reflection preserves Gram data; the support-number margin applies to all incident target facets simultaneously. | Standard PL barycentric subdivision and degree classification. |
| Smooth analytic input | Wrong boundary branch, index sign, hidden strict convexity or matching angles | Primary hypotheses, boundary relation, norm coefficient, and round-sphere branch checked. | Brendle's Fredholm/elliptic results, including the foundational theory cited there, remain imported. |
| Uniform geometry | Thin rounded layers, flat patches, nonadjacent active pairs | Explicit radial/polar and normal-cone arguments above; constants depend only on the fixed polytopes and cutoff. | Standard Lipschitz chain/area formulas and bounded extension/trace theorem. |
| Critical cutoff | A multiplicative curvature error or wrong surface measure | Nonexpanding spherical interpolation, actual-boundary pullback, and logarithmic integral independently derived. | No unresolved central estimate found. |
| Limit and algebra | Vanishing mass, illegal moving-boundary trace, rank-deficient C | Strong L2 mass identity; fixed half-ball strong H1 trace; scalar anticommutator cancellation. | Rellich compactness and standard trace continuity. |

Excluded cases remain excluded: unbounded bodies, lower-dimensional bodies, redundant duplicate facet inequalities, nonconvex polytopes, and dimensions above three. Near-degenerate but nondegenerate fixed polytopes cause no logical failure, although constants need not remain uniform as a family degenerates. Equal angles are included. Opposite nonadjacent normals are harmless because the minor-arc construction is used only for adjacent facets, whose angles are strictly between zero and pi.

## Checkable finite evidence and limits

`EVIDENCE.py` independently binds all 29 original files to the immutable Git head and compares the entire prefix file set. After full code inspection, it copies the original public control program into the ignored private review area, executes that copy, and requires exact equality with the frozen result: all 5,066 finite diagnostics and all result flags agree. It also performs nine exact independent Clifford generator checks and 72 exact boundary-symbol basis checks.

A negative control exhibits the importance of the chosen edge transport. If one reuses affine weights rather than fractional arclength, the endpoint speed ratio can be sin(1.3)/sin(2.6)=1.8691670635>1 even though 1.3<2.6. That substitute is invalid; the actual candidate uses arclength and passes the mathematical derivative check above.

These computations verify finite algebra and provenance. They do not certify an analytic theorem or validate Brendle's proof by computation. The strongest conclusion of this review is the full conditional three-dimensional derivation above, with no substantive gap found within the reviewed scope. There is no priority, publication, or higher-dimensional clearance.

## Trust boundaries and reproducibility

The initial analysis, this report, evidence source/result, primary-source metadata, and log are sealed by `REVIEW_MANIFEST.json`; `SEAL.txt` gives its detached SHA-256 pin. Independently recomputing every manifest digest and its detached pin checks this review artifact's integrity. The seal is an integrity commitment, not an identity signature or proof certificate. Downloaded primary bodies and the replay copy are excluded from that public projection and ignored under `private/`.

All work stayed inside this review directory. I made no commits, pushes, releases, shared ledger edits, provider mutations, or outreach. The inherited restriction on those actions was honored even though the repository's general workflow normally requests frequent publication. The parent review is responsible for any broader publication/priority decision.
