# Quadrisecants of wild knots: five approaches and an unresolved line-count target

Problem 11300004 / AMR-112-0004; rank 1014. Research date: 2026-10-08 UTC.

## Result and exact target

**Unresolved here.** Five distinct mathematical approaches below yield elementary reductions, explicit counterexamples to proposed shortcuts, and a local sufficient condition. None proves the universal assertion or produces a wild counterexample. No novelty or formal-certification claim is made.

The queue target is the following statement, written independently in precise notation. Let K be the image of a continuous embedding of S¹ into Euclidean R³, and suppose K is not ambiently equivalent to a polygonal knot. Define

Q(K) = {unoriented affine lines L in R³ : |L ∩ K| ≥ 4}.

The question is whether Q(K) is necessarily infinite. The four intersection points must be distinct. There is no assumption of smoothness, finite length, finite total curvature, general position, transversality, an alternating cyclic order, exactly four intersections, or finitely many intersections per line. In particular, a line containing a straight subarc counts once. The geometry is Euclidean R³; replacing lines by great circles in S³ or projective lines would change the problem.

### Primary-source and counting distinctions

The published 1994 paper presents Conjecture 21 on p.49 as an infinitude assertion for quadrisecants of every wild knot in Euclidean three-space. Its Definition 5, p.42, uses a segment with two distinguished interior intersection points. The 2002 arXiv revision instead states Conjecture 6.4 for a wild arc. These are different versions and different domains. The primary tame theorem applies to nontrivial tame links without a general-position assumption. Its strengthened conclusion excludes component segments contained in the link. [K94](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Kuperberg/Kuperberg4.pdf), [K02](https://arxiv.org/pdf/math/9712205v2).

The dataset's count of supporting lines must not be silently substituted for a count of marked four-point configurations. Infinitely many configurations on finitely many lines is possible. If every supporting line meets K in finitely many points, these two infinitude assertions agree: a line with m contacts supports at most C(m,4) unordered four-point sets. Without that extra hypothesis, the implication fails.

For example, let D be the union of the upper unit semicircle in the xy-plane and its diameter. It is a tame simple closed curve. Its diameter line contains infinitely many points and hence infinitely many marked quadrisecants. Every other line meets D in at most two points: for a line in the plane, this follows from convexity and the absence of any other straight boundary segment; a line outside the plane has at most one intersection. Thus |Q(D)|=1. This example is not wild and does not disprove the target; it proves why the counting distinction is indispensable.

Denne's 2005 paper defines its “knotted curve” convention at the start to require a nontrivial tame knot. Theorem 27 therefore does not cover wild knots, despite its abbreviated wording. Theorem 27 proves an alternating quadrisecant; Corollary 29 adds essentiality under finite total curvature. The 2016 survey, Theorem 8, retains these two scopes. [D05](https://arxiv.org/pdf/math/0510561), [D16](https://arxiv.org/pdf/1608.02608).

A related polygonal-approximation shortcut is unavailable: Bai, Wang and Wang construct knots whose quadrisecant approximation is self-intersecting or changes knot type. That result concerns a different conjecture and is not a resolution of wild-knot quadrisecants. [BWW16](https://arxiv.org/abs/1605.00538).

A bounded literature check found no verified modern theorem extending the required infinitude statement to all wild knots. This is a report of the search and inspected sources, not proof that no such work exists.

## Approach 1: compactness of approximating quadrisecants

**Idea.** Approximate the wild embedding by tame embeddings, use a quadrisecant theorem for each approximation, and pass to the limit. Separate point collapse from repeated supporting lines.

### Lemma 1 (separated-parameter persistence)

Let f_n:S¹→R³ be embeddings converging uniformly to an embedding f. Suppose f_n has a quadrisecant with parameters t_{n,1},...,t_{n,4}, with pairwise circular distances at least δ>0. A subsequence converges to a four-point collinear configuration on f(S¹).

**Proof.** Compactness of (S¹)⁴ gives a convergent subsequence of the parameter tuples. Their limits remain pairwise δ-separated, hence distinct. Uniform convergence and continuity imply f_n(t_{n,j})→f(t_j). Injectivity of f makes the four image points distinct. Collinearity is closed, for instance because all relevant cross products vanish and cross products are continuous. The limiting configuration is therefore a genuine quadrisecant. □

Represent an unoriented line by (P,c), where P is the orthogonal rank-one projection onto its direction and c is its closest point to the origin. Use the metric ||P−P′||_F+||c−c′||. Secant lines of a bounded compact set lie in a compact family: P lies in a compact projective plane and c is bounded. A line through a convergent pair of distinct points converges continuously in this representation.

### Lemma 2 (escape from every finite line set)

Under the hypotheses of Lemma 1, assume that for every finite family F of affine lines there exist δ,ε>0 and arbitrarily large n with a quadrisecant tuple whose parameters are δ-separated and whose supporting line has distance at least ε from every line in F. Then Q(f(S¹)) is infinite.

**Proof.** Lemma 1 and continuity of the supporting line produce a quadrisecant of the limit outside F. Were Q(f(S¹)) finite, take F equal to it, obtaining a contradiction. □

**Why the naive argument fails.** Four distinct points at every finite stage need not have four distinct limits. Here is an explicit arc example. For 0<ε<1/5, take f_ε(t)=(t,g_ε(t),0), t∈[−1,1]. Outside [−5ε,5ε], set g_ε(t)=t². Inside, linearly interpolate the successive vertices

(−5ε,25ε²), (−3ε,0), (−2ε,ε²), (−ε,0), (0,ε²),
(ε,0), (2ε,ε²), (3ε,0), (5ε,25ε²).

The four parameters −3ε,−ε,ε,3ε give a quadrisecant on the x-axis; none of the interpolation edges is a nontrivial x-axis interval. The functions converge uniformly to t², with error at most 25ε². The limit parabola has no trisecant, because a line meets a nondegenerate parabola at most twice. All four witnesses collapse at the origin. This example concerns arbitrary witnesses, not the essential witnesses of the tame theorem.

**Remaining obstruction.** Wildness supplies neither a common positive δ nor the finite-family escape property. Even an unbounded number of finite-stage quadrisecants can collapse in parameter space or converge to finitely many lines. A wild limit also has no ambient knot-type stability supplied by uniform convergence alone; choosing the approximants to be nontrivial needs justification, and inserting tiny artificial knots would not supply surviving witnesses. An approximation argument needs both protections. Importing a straightening neighborhood at the wild point would assume away the difficulty.

## Approach 2: contrapositive tameness and local projection

**Idea.** Prove that a curve with finitely many quadrisecant lines must be tame. Try local straightening, rather than limits of global knot types.

### Lemma 3 (a monotone coordinate gives a tame arc)

If an embedded compact arc admits a parametrization γ(t)=(t,u(t),v(t)), t∈[a,b], with u,v continuous, then it is tame.

**Proof.** Extend u and v continuously to R, for example constantly beyond each endpoint. The maps H_s(x,y,z)=(x,y−s u(x),z−s v(x)), 0≤s≤1, are an ambient isotopy: their inverses add the same two functions. H_1 takes the arc to [a,b]×{0}×{0}. □

This proves a concrete local sufficient condition. However, “a generic line has at most three intersections” is not a monotone-coordinate condition. It does not give injectivity of one coordinate, and no implication from finitely many quadrisecant lines to such coordinates is established here.

### Lemma 4 (finite-contact reduction to quadrisecant-free local arcs)

Suppose Q(K) is finite and each L∈Q(K) meets K finitely. Every point of K has a compact subarc neighborhood A⊂K with Q(A)=∅.

**Proof.** The union E=⋃_{L∈Q(K)}(L∩K) is finite. For a chosen p∈K, choose a sufficiently small closed parameter interval around its preimage containing no member of f⁻¹(E) other than possibly f⁻¹(p). Its image A meets every exceptional line in at most one point. If a line met A in four points, it would belong to Q(K), contradicting this property. □

The purely local assertion “every quadrisecant-free embedded arc is locally flat at its interior points,” if established, would combine with Lemma 4 to make K locally flat. One would then need to pass from local flatness to a global tame representative. This route is conditional: we do not establish the proposed local assertion, and do not use the global passage in any claimed result. An endpoint version is relevant to wild arcs, and must not be presumed from interior local flatness.

When a quadrisecant line has infinitely many contacts accumulating at a wild point, Lemma 4 no longer applies. The diameter example in the opening section shows that finiteness of Q(K) alone cannot make the contact set finite. Such accumulation is a second, logically separate obstruction for this route.

**Remaining obstruction.** A local tameness theorem derived from absence of four-point collinearities is missing; a proof must also control infinite contact sets on finitely many exceptional lines. No tameness conclusion is claimed.

## Approach 3: local tangles and stable four-arc transversals

**Idea.** Find a quadrisecant inside each of infinitely many small knotted regions, then make the supporting lines distinct. This seeks actual local witnesses instead of passing global witnesses through a limit.

### Lemma 5 (explicit stable local witness)

Consider four short arcs through (i,0,0), i=0,1,2,3. The first two have model parametrizations (i,t,0); the last two have (i,0,t), where t is near 0. These arcs possess a quadrisecant, the x-axis, and a nearby quadrisecant persists under sufficiently small C¹ perturbations of all four parametrizations.

**Proof.** Parametrize a nearby line as (x,A+Bx,C+Dx). For an intersection with an arc r_i(t_i), impose the two equations

r_{i,y}(t_i)−A−B r_{i,x}(t_i)=0,
r_{i,z}(t_i)−C−D r_{i,x}(t_i)=0.

There are eight equations and eight unknowns (t_0,t_1,t_2,t_3,A,B,C,D). At the model, the equations for the first two z-coordinates force C=D=0; the last two y-coordinates force A=B=0; the remaining equations force all t_i=0. The 8×8 Jacobian is invertible (its determinant has absolute value 1). Thus the solution is isolated and nondegenerate.

For completeness, persistence does not require an unmentioned genericity theorem. Let J be this Jacobian. On a sufficiently small closed ball about the origin, and for sufficiently small C¹ perturbations, the map x↦x−J⁻¹F(x) has derivative norm less than 1/2 and moves the origin by less than half the ball's radius. It is a contraction of the ball into itself, hence has a fixed point, a zero of F. Distinctness of the four intersection points persists because their x-coordinates remain near the four distinct integers. □

### Lemma 6 (line-family localization)

Let U_n be pairwise disjoint subsets of affine-line space. If K contains, for each n, four subarcs that have a common transversal L_n∈U_n, meeting them in four distinct points, then Q(K) is infinite.

**Proof.** Each L_n belongs to Q(K), and disjointness of the U_n makes the L_n distinct. □

Lemma 5 can supply the local witnesses for geometrically arranged examples, and translations/dilations can place their line families in disjoint neighborhoods. These are sufficient conditions on a given embedding, not consequences of arbitrary wildness.

**Closure obstruction.** Even when a local arc A can be closed by a single straight segment S to form a nontrivial tame knot (with S meeting A only at the endpoints), applying a global theorem does not in general give four points on A. Even if one has a quadrisecant of A∪S none of whose component segments is contained in the knot, it yields only the following: either its line is the supporting line of S, or it has at most one point in the relative interior of S. In the latter case at least three of its four points lie on A, but a fourth may be supplied by the artificial closure. In the former case the component-segment restriction forces the chosen four points to avoid having two contacts on S, and the same three-point bound holds. More directly, two chosen points on S would have consecutive chosen points between them lying entirely on S, which is forbidden. Three points on A are insufficient.

Moreover, not every wild knot has been shown here to decompose into infinitely many isolated, tame, knotted tangles admitting those closures. Distinct regions alone do not imply distinct supporting lines, since one line can pass through infinitely many shrinking regions.

**Remaining obstruction.** Extract four-point witnesses internal to the actual wild curve, together with separation in line space. Neither general tangle extraction nor closure-point elimination is proved.

## Approach 4: topology of the trisecant configuration space

**Idea.** Work directly with the embedded curve and force a self-intersection in its trisecant locus. This avoids assuming smooth approximants have surviving witnesses.

For a compact embedded arc γ:I→R³ and δ>0, let T_δ consist of parameter triples (a,b,c) with a≤b, all three image-point distances at least δ, and γ(c) in the straight segment between γ(a) and γ(b). Let π(a,b,c)=(a,b).

### Lemma 7 (compact unique-middle-point locus)

If Q(γ(I)) is empty, T_δ is compact and π:T_δ→π(T_δ) is a homeomorphism.

**Proof.** The parameter inequalities and distance bounds are closed. Segment membership is closed: it can be expressed by a parameter λ∈[0,1] with γ(c)=(1−λ)γ(a)+λγ(b), and projected from a compact set. Therefore T_δ is compact. If two different middle parameters c,c′ projected to the same (a,b), the four distinct image points would be collinear. Thus π is injective. It is continuous from a compact space to a Hausdorff space, so is a homeomorphism onto its image. □

This establishes continuity of a unique middle point away from collisions. It does not make π(T_δ) a finite graph or a one-dimensional manifold, provide an essential cycle, or control the union as δ tends to zero. Compact injective images can have complicated topology; those missing conclusions are additional statements, not consequences of compactness.

If one works with finitely many quadrisecant lines instead of none, infinite contact sets can already give entire continua of triples and multiple middle points supported on a single exceptional line. Counting those configurations would again confuse the target.

A disk-based argument also needs its boundary hypotheses checked. Constructing a continuous spanning disk, or invoking the name of Dehn's lemma, does not by itself supply a locally flat collar of a wild boundary. Any use of a standard tame-knot disk criterion must justify that criterion's hypotheses rather than use the desired tameness in the proof.

**Remaining obstruction.** Establish the necessary separation/cycle theorem for the possibly non-manifold trisecant locus, control its collision boundary, and produce a valid local-flatness conclusion. None of these steps is supplied by Lemma 7.

## Approach 5: curvature and integral-geometric forcing

**Idea.** Replace knot topology by geometric complexity near a wild point and try to force many collinear configurations. Test whether unbounded turning, a typical proposed proxy for wild behavior, can be enough.

### Proposition 8 (an infinite-curvature tame unknot with no trisecants)

There exists a rectifiable tame unknot of infinite total curvature and with no three distinct collinear points.

**Construction.** On the angular coordinate θ∈(−π,π), choose a smooth cutoff χ that is 1 on [0,a] and 0 on [b,π), with 0<a<b<π. Set f(θ)=χ(θ)θ³ sin(1/θ²) for θ>0 and f(θ)=0 for θ≤0. Extend periodically. Let

γ(θ)=(cos θ,sin θ,f(θ)).

**Embedding and rectifiability.** Projection to the unit circle is injective modulo the periodic endpoints. Near 0,

f′(θ)=3θ² sin(1/θ²)−2 cos(1/θ²),

so f is Lipschitz; the cutoff region is smooth. The closed curve is rectifiable.

**No trisecants.** A nonvertical line projects to a line in the xy-plane, meeting the unit circle at at most two points. A vertical line projects to one point and meets this graph at at most one point. Thus any line in R³ meets γ in at most two points.

**Tameness.** Extend f from the unit circle to a continuous function F on R² by F(r cosθ,r sinθ)=ρ(r)f(θ), with ρ supported in (1/2,3/2) and ρ(1)=1; set F=0 near the origin. The ambient isotopy (x,y,z)↦(x,y,z−sF(x,y)) flattens γ to the standard circle.

**Infinite total curvature.** For all sufficiently large integers k, put θ_k=(kπ)^(−1/2), inside the region χ=1. The tangent vector there is

v_k=(−sin θ_k, cos θ_k, −2(−1)^k).

Its norm is √5, and consecutive normalized tangent dot products tend to −3/5. Hence their angular separation tends to arccos(−3/5)>0. To connect this with the polygonal definition of total curvature, for any finite string of these parameter values choose sufficiently short, disjoint chord intervals around them. Each selected chord direction approximates the corresponding tangent direction. Include these chord endpoints in an inscribed polygon. By the spherical triangle inequality, the total turning of that polygon is at least the sum of the angular distances between the successive selected directions. This lower bound grows linearly with the length of the string. The supremum of inscribed-polygon total curvatures is infinite. □

The proposition refutes the implication “infinite total curvature forces any quadrisecant,” even among rectifiable tame closed curves. It does not refute the wild-knot target. Plane-intersection or tangent-variation estimates need an additional topological mechanism to force four points onto one line; high turning alone is insufficient.

**Remaining obstruction.** No topologically sensitive lower bound for the number of distinct line quadrisecants has been established for arbitrary wild embeddings. Ropelength or total-curvature results with positive-thickness, smoothness, or finite-curvature hypotheses cannot be imported without those hypotheses.

## Ledger, evidence, and stopping point

The five approaches are, respectively: approximation compactness; local straightening/tameness; stable local-tangle witnesses; topology of the trisecant locus; curvature/integral geometry. Source recovery, literature inspection, duplicate searches, algebraic checks, and packaging count as zero proof turns.

The remaining universal problem is exactly the line-count assertion stated at the beginning. The paper-version distinction and the marked-configuration distinction are preserved. The negative examples above only invalidate shortcuts; none is a wild counterexample. The positive lemmas are elementary conditional statements; none resolves the universal assertion or is claimed as a new research theorem.

The accompanying finite checks verify the displayed transversal Jacobian, line-count arithmetic, collinearity/collapse samples, and tangent-limit algebra. They do not verify every embedding in an infinite family, a literature search's completeness, or a topological theorem. Integrity checks authenticate a particular frozen packet, not mathematical truth.
