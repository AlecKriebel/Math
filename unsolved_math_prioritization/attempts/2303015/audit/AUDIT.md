# Independent adversarial audit: Function Theory 3.15

Date: 2026-10-04 UTC. Target: rank 570, numeric ID 2303015, code AMR-022-3015.

## Verdict

**PASS for the stated partial results, within the packet's explicit boundary-limit and nondegenerate-annulus/Jordan-ring scope. The original extremal problem remains unresolved.**

No material mathematical correction was found. In particular, RESULTS.md Section 5 proves a genuinely uniform positive gap over every admissible continuous path, including paths with loops, retracing, or self-intersections. This is stronger than merely proving that each individual admissible function is strictly below the harmonic majorant, and the proof does establish the claimed uniformity.

The audit does not certify historical priority, a current open-status classification, attainment of the original supremum, or the complete sharp answer. The five approaches remain an unfinished five-approach attempt; this audit performs verification rather than further extremal-curve search.

Frozen input manifest SHA-256:

`337e5c6e1e319556d4ce3148a4fe9f6e3ceef6d6bcc3b07a9632296ec638942c`

All seven entries in that manifest were verified before and after the audit. The frozen public directory was not edited. No remote writes were performed, and no source PDF or source corpus is included in this audit directory.

## 1. Exact target and primary-source gate

The primary PDF was independently opened through the web tool and the supplied private page image was visually inspected. Problem and Update 3.15 are indeed at printed page 65, physical PDF page 66, in arXiv:1809.07200v2. The problem fixes a doubly connected domain, its two boundary curves, two interior points, and two arbitrary real boundary constants; it asks to maximize the subharmonic function at the first point subject to a nonpositive path from the second point to the designated boundary. It is attributed to Baernstein. The update reports no progress known to the editors. The wording does not explicitly define the boundary-limit convention or require Jordan boundaries. The packet's additional regularity scope is therefore an explicit restriction, not a proven interpretation covering every possible generalized meaning of the source. [Primary PDF](https://arxiv.org/pdf/1809.07200v2)

The original problem is not replaced by the radial subclass or the isolated-point relaxation: the packet calls these partial results and retains the free-curve optimization as the remaining gap. The source update is historical evidence, not proof of current open status.

The private primary PDF is 1,706,228 bytes with SHA-256 `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`, matching provenance.json. The private Solynin PDF is 689,450 bytes with SHA-256 `9cb6c30562e2bb51e311c07f3f6c637cac6b965c1af5e16f509cdd6e4c7577af`, also matching provenance.json. These bytes stay private.

The selected upstream numeric record and complete prior generated report were read locally. They agree on the target; the latter is only a literature-triage report and supplies no mathematical proof. This audit did not redownload the large full upstream corpora or independently recertify their whole-file hashes. The direct catalogue page failed in this audit's web tool; the primary PDF establishes the mathematical target regardless.

## 2. Scope, normalization, and boundary assumptions

The working hypotheses are a bounded annulus `0 < r < |z| < R < infinity`, finite limits at every boundary point, and a continuous path reaching the specified boundary. Interior values of negative infinity are allowed for a nontrivial subharmonic function.

These hypotheses justify comparison with the finite continuous harmonic interpolant h. The upper-semicontinuous function u−h has boundary limsup zero at every boundary point and is locally bounded above inside; bounded-domain maximum comparison gives u≤h. No unmentioned lower bound on u is needed.

A conformal map between a nondegenerate Jordan ring and a circular annulus extends homeomorphically to the two boundary components. Pullback preserves subharmonicity, the finite boundary limits, and the continuous-path condition. Swapping which boundary becomes inner is legitimate by annular inversion. Thus the transfer to the stated Jordan setting is sound. Here a Jordan ring means the doubly connected region between two disjoint nested Jordan curves; degenerate punctured domains and arbitrary irregular boundaries are outside the asserted scope.

The radial subclass is radial in the selected circular-annulus coordinate. The explicit Euclidean constants delta and R0 in Section 5 are likewise computed in that normalized coordinate if one transfers the result to a Jordan ring. No assertion that they are conformally invariant Euclidean constants is needed.

Finite boundary limits are essential to the stated feasibility result. Merely assigning symbols A and B to boundary points, without requiring the corresponding interior limits, would not support the proof. The packet correctly excludes that interpretation. Likewise, no result for only almost-everywhere, quasi-everywhere, or unspecified nontangential boundary data is claimed.

## 3. Audit of the exact special cases and radial envelope

### 3.1 Feasibility and easy signs

If A>0, a path of nonpositive values approaching its attachment point on alpha contradicts the finite boundary limit A. This is independent of B.

If A≤0 and h(z1)≤0, the harmonic interpolant is nonpositive on the inward radial segment ending at z1, since all its values there are affine interpolations of A and h(z1). It is therefore admissible and saturates the general upper bound at every z0. This argument includes, but is not limited to, the case A≤0 and B≤0; no ordering of A and B has been silently imposed.

If A≤0 and h(z1)>0, then B>0. Set s=x(z1). The two pieces of W have derivatives −A/s and B/(1−s) with jump

`B/(1−s) + A/s = h(z1)/(s(1−s)) > 0`.

They match at value zero and have the prescribed endpoint values. In the logarithmic coordinate, the positive derivative jump gives a nonnegative distributional Laplacian supported on the interface circle. This proves subharmonicity and gives a finite continuous admissible competitor. Consequently the feasibility equivalence A≤0 is correct under the stated scope.

### 3.2 Radial optimality, with the restriction retained

For a radial subharmonic function, annular harmonic comparison yields the convex-chord inequality in log radius. Conversely, convexity in log radius gives subharmonicity. Finite endpoint limits extend the chord inequalities to x=0 and x=1. If the radial function is admissible, its value at s is at most zero; comparison with the two endpoint-to-knot chords bounds it above by W when h(z1)>0. W attains both bounds. When h(z1)≤0, the ordinary endpoint chord h is admissible and largest.

Allowing interior negative infinity does not create a counterexample to this argument. A nontrivial radial subharmonic function with finite boundary limits cannot be negative infinity on a whole interior circle: alternatively, one can use local integrability/circular means, or the convex radial representative. In any event, the upper chord bounds remain the relevant direction, and the exhibited finite competitors attain them.

This is a solution of the explicitly restricted class, not a symmetrization proof for the original class.

### 3.3 Coincident marked points

At z0=z1, the path constraint gives u(z1)≤0 while comparison gives u(z1)≤h(z1). The harmonic competitor or W attains the smaller value. Thus the formula `M(z1,z1;A,B)=min(h(z1),0)` is correct for A≤0, including h(z1)=0. There is no claimed value of M for the empty A>0 class.

## 4. Audit of the point relaxation and fixed slit

### 4.1 Truncated Green potentials

With the positive Dirichlet normalization used in the packet, G(·,z1) is superharmonic and diverges to positive infinity at its pole. The minimum with a finite positive constant is superharmonic. It equals the constant in a neighborhood of the pole and is continuous across the truncation level and at the pole. Subtracting the scaled truncation from h therefore yields a finite continuous subharmonic function with the original boundary values and value zero at z1.

At a fixed distinct z0 the Green value is finite, so the penalty tends to zero as T grows. This proves the point-only relaxed supremum equals h(z0). If an admissible relaxed function attained h(z0), its nonnegative superharmonic difference from h would have an interior zero, forcing that difference to vanish identically; that would contradict the positive value required at z1. The nonattainment statement is correct for distinct points in the positive-knot regime.

The construction does not supply a nonpositive connection to alpha, and the packet correctly does not treat it as a competitor family for the original problem.

### 4.2 Radial slit when A=0

A partial radial slit from the inner boundary to the interior point leaves a connected domain. The boundary is Dirichlet regular: ordinary arc points and the attachment have standard local barriers, while the interior slit tip has a square-root barrier. The prescribed zero values agree where the slit meets alpha, so the Dirichlet solution extends continuously there as well.

The harmonic solution has values between zero and B and is strictly positive off the slit by the strong maximum principle. Its zero extension on the slit satisfies the submean inequality at slit points simply because all surrounding values are nonnegative, and it is harmonic locally elsewhere. The local submean criterion and continuity prove subharmonicity in the original annulus.

For an arbitrary subharmonic u constrained on this same slit, upper semicontinuity ensures boundary limsup at a slit point is at most u there, hence at most zero. The other boundary limits are the prescribed constants. Comparison on the slit domain therefore proves the asserted fixed-slit maximality, including for discontinuous interior subharmonic competitors.

Taking z0 off the slit with x(z0)≤s gives a strictly positive slit value, whereas the radial W equals zero. Such points exist. This is a valid counterexample to general radial optimality.

For A<0, an identically zero slit cannot meet alpha while respecting its finite limit A. The warning about the need for an obstacle formulation is correct and does not itself assert that the resulting fixed-path or free-path problem has been solved.

## 5. Detailed adversarial audit of the uniform-gap theorem

This is the principal mathematical audit target.

### 5.1 Choice of constants

Because h(z1)>0 and h is continuous, a sufficiently small closed disk K0 around z1 has h≥c>0. The radius can also make K0 compactly contained in D and exclude z0. Positivity and continuity of G(z0,·) on this compact set yield m>0. A surrounding disk with radius R0 exists because the annulus is bounded. The stated C is positive and finite.

All these constants depend only on the fixed data and the chosen neighborhood, not on the admissible curve or function. This independence is what makes the final penalty uniform.

### 5.2 First-hit measurability and compact support

Parametrize the path from z1 by a continuous gamma. It must leave K0 before reaching alpha. Let T be its first hit of the radius-delta circle and use the compact image K=gamma([0,T]). For `0≤t≤delta`, define

`tau(t)=min{q in [0,T] : |gamma(q)−z1|=t}`.

The minimum exists by continuity and compactness. If t1<t2, the intermediate-value theorem forces a hit of radius t1 before the first hit of t2, so tau(t1)≤tau(t2). Therefore tau is Borel measurable. The selected map w(t)=gamma(tau(t)) is Borel and obeys `|w(t)−z1|=t` exactly. Its pushforward of normalized Lebesgue measure is a probability measure supported on K.

No injectivity, rectifiability, differentiability, or radial monotonicity of the original path is assumed. Jumps in tau are harmless. Repeated visits to a radius and arbitrarily many loops are handled by the first-hit selection.

### 5.3 Ball mass and logarithmic upper bound

For any z and any epsilon>0, if w(t) lies in B(z,epsilon), then the reverse triangle inequality forces t into the interval centered at |z−z1| with radius epsilon. Its intersection with [0,delta] has length at most 2epsilon. Hence the linear ball-mass bound follows, even if the selected set is highly irregular. In particular the measure has no atoms.

Green-kernel domain monotonicity and the containing-disk formula give

`0≤G_D(z,w)≤log(2R0/|z−w|)`.

The numerator in the disk formula is at most 2R0 after division by R0; the distance is less than 2R0, so this is a nonnegative upper bound. Substituting `|z−w(t)|≥||z−z1|−t|` gives the one-dimensional integral bound with no reversed inequality.

For an independent scalar check, put q=a/delta, a=|z−z1|. When 0≤q≤1,

`−(1/delta) integral_0^delta log|a−t| dt = 1−log(delta)−q log(q)−(1−q) log(1−q)`,

where 0 log 0 means zero. The binary-entropy term is maximal at q=1/2 with value log 2. For q>1 the expression is `1−log(delta)+(q−1)log(q−1)−q log(q)`, whose derivative is negative. Thus the claimed C=`1+log(4R0/delta)` is correct, including both endpoints of the scalar interval. The apparent singularity at t=a is integrable.

### 5.4 Continuity and boundary behavior of U

The linear ball-mass estimate implies uniformly in z, for sufficiently small epsilon,

`integral_{|z−w|<epsilon} log(2R0/|z−w|) dnu(w) ≤ (2epsilon/delta)[log(2R0/epsilon)+1]`.

This follows directly by the layer-cake/Stieltjes-integral identity: the boundary mass term is bounded by `(2epsilon/delta)log(2R0/epsilon)` and the remaining integral by `2epsilon/delta`. The right side tends to zero. A continuous cutoff of the Green kernel away from the diagonal gives a continuous truncated potential; the displayed bound gives uniform convergence to U. Thus U is continuous, including at points of K. The argument is stronger than mere finite energy or pointwise finiteness, so there is no hidden quasi-everywhere-only conclusion.

Since K lies a positive distance from the annulus boundary, the regular Green kernel tends to zero there uniformly for w in K. Thus U has zero limits on **both** boundary circles. It is harmonic on D\K by local integration of a kernel harmonic away from its support.

### 5.5 Comparison on arbitrary components

Set v=h−u. It is nonnegative, lower semicontinuous, and superharmonic, possibly positive infinity at interior points. On K the path condition gives v≥h≥c, while U≤C. For every p in K, lower semicontinuity gives

`liminf_{z→p} v(z) ≥ v(p) ≥ c`.

Together with continuity of U, this supplies the required boundary inequality for `cU/C−v` when approached through any component of D\K. At a point of either original boundary curve, v tends to zero and U tends to zero. These are every possible boundary point of a component.

The function `cU/C−v` is subharmonic off K and bounded above by c. Its boundary limsup is nonpositive at every boundary point. The bounded-domain maximum principle therefore applies on each component, irrespective of whether that component has regular boundary, narrow fjords, holes, or many boundary components. No Dirichlet solvability on D\K is being assumed. Values v=positive infinity cause no problem: the comparison function then takes negative infinity, which is permitted for a subharmonic function.

Consequently `v≥cU/C` throughout D. Because z0 is outside K0 and nu is a probability measure supported in K0, `U(z0)≥m`. The claimed bound follows exactly. There is no sign error, missing normalization factor, circular use of a desired extremal curve, or dependence of c,m,C on the arbitrary path.

### 5.6 Consequences and limitations

The strict uniform inequality for the supremum follows, rather than just strict inequality for each individual u. The admissible W supplies the lower bound. Neither argument determines the optimizer or shows that the supremum is attained, and the packet correctly says so.

Only an editorial clarification is suggested: the phrase “outer boundary of D” in the comparison paragraph should preferably say “both boundary components of D.” The earlier assumptions and boundary discussion already supply the needed facts, so this is not a mathematical failure. A second optional clarification is to insert the lower-semicontinuity argument above when invoking comparison along K.

## 6. Computational audit and what it does not prove

The original `python3 public/verify.py` run exactly reproduced the saved verification.json:

- 2,184 rational parameter-point checks and the negative slope-jump control;
- a 22-unknown Dirichlet system, with every exact residual zero;
- slit target value `54206789/412704788`, strictly between zero and 1/4.

A separate implementation in independent_verify.py does not import the author's code or use its solver. It assembles the graph matrix from undirected edge energies and solves it by exact LDL-transpose factorization. All 22 pivots are positive, every residual is exactly zero, the reflected graph values agree, and the target is independently reproduced. The full rational value-vector hash is recorded in INDEPENDENT_CHECKS.json.

The independent radial implementation uses h minus a triangular penalty, with fractional positive and negative boundary data and all knot regimes. It passes 11,000 exact point checks over 440 feasible parameter triples; 176 A>0 triples are separately classified as empty by the analytic feasibility result. A total of 6,161 exact scalar interval-mass controls and 6,404 floating-point scalar logarithmic-integral diagnostics also pass.

These computations audit algebra, the finite graph, and the scalar formula only. They do not numerically establish the continuum theorem, approximate the continuum with a proved error bound, search for an extremal curve, establish attainment, or certify a literature search. The continuum claims were checked analytically in Sections 2–5 of this audit.

## 7. Literature and provenance limits

Solynin's 2021 paper was independently opened at the publisher; its abstract, introductory formulation, and final discussion were checked against the private text. It concerns boundary-connected wires and harmonic measure, with its main resolved configuration a disk and two symmetric control points. Its final section still poses general existence and quadratic-differential questions. This is relevant context, but the article has not been identified as a theorem settling the complete annular two-boundary-constant target here. The packet correctly uses none of its theorems in the partial proofs. [Publisher PDF](https://afm.journal.fi/article/download/110574/65029/203266)

The Cambridge publisher record independently confirms Baernstein's 1974 chapter, pp. 11–16. Its full theorem content was not available in this audit, so no implication for the target follows merely from its title. [Publisher record](https://www.cambridge.org/core/books/abs/proceedings-of-the-symposium-on-complex-analysis-canterbury-1973/some-extremal-problems-for-univalent-functions-harmonic-measures-and-subharmonic-functions/5F8852FA90F03AEFBF930243B8099B26)

The Hummel–Pinchuk full primary article and the 1998 Solynin paper were not independently checked theorem by theorem. This audit endorses the packet's explicit limitation rather than elevating bibliographic leads into solution evidence. No historical-priority conclusion is justified by this limited review.

Live repository duplication checks recorded in SOURCES.md are historical observations from the author, with stated search-index limitations. This audit did not repeat them or certify that the remote repository remained unchanged. They are not mathematical premises of the results.

## 8. Final disposition

- Accept the stated exact easy-sign and coincident-point formulas within the explicit classical scope.
- Accept the radial-class extremal and the A=0 slit counterexample to unrestricted radial optimality.
- Accept the point-only relaxation and its nonattainment result.
- Accept the uniform positive-gap theorem for every continuous admissible path in the stated scope.
- Retain the full problem as unresolved after five approaches; do not promote the packet to a solved result.
- Preserve the uncomputed sharp value, unknown optimal curve, unproved attainment/uniqueness, arbitrary-boundary extensions, and literature completeness as open limitations of this attempt.
- Keep the frozen files intact; optional clarifications are recorded separately in CORRECTIONS.md and are not prerequisites for the mathematical pass.

The separate SHA256SUMS file binds this audit's report, clarification record, independent verifier, numerical output, and status record. Source bytes have not been redistributed.
