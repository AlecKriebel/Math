# Independent audit: Borda reduction for the line-union problem

Date: 2026-10-20 UTC. Queue position 1825; problem ID 30002421.

## Verdict

**PASS for the axis-parallel interpretation; NOT a resolution of the unrestricted-orientation interpretation.**

The construction and reduction in `ATTEMPT_2.md` are mathematically sound. They produce admissible finite unions of distinct full affine-line chords with total length tending to infinity and normalized discrepancy at most a fixed constant divided by total length, uniformly over every axis-parallel box. Consequently the proposed universal logarithmic lower bound is false for axis-parallel cubes.

No gap was found involving rational independence, the time/length normalization, distinctness, full chords, endpoints, or closed boundaries. The unresolved issue is the original problem's test-class scope, not a defect in the restricted counterexample. The original report says cubes without explicitly specifying their orientation. It is not permissible to infer an unrestricted-orientation counterexample from Borda's axis-parallel theorem.

This is an independent acceptance audit of the stated reduction using an established external theorem, not an independent proof of that external theorem.

## 1. Source and theorem checks

The inspected primary source is Bence Borda, *Bounded error uniformity of the linear flow on the torus*, arXiv:1803.06968v1, submitted 19 March 2018. The arXiv bibliographic record gives Monatsh. Math. 189 (2019), 221–237. The theorem statement was checked in the retrieved author PDF, its rendered printed page 4, and arXiv's HTML transcription. The typeset journal article was not independently inspected.

Public sources:

- https://arxiv.org/abs/1803.06968
- https://arxiv.org/html/1803.06968
- https://real.mtak.hu/98617/2/180306968v1.pdf

The exact aspects of Corollary 2 needed here all check out:

1. The direction's coordinates must be real algebraic numbers and linearly independent over Q. The continuous-flow theorem does not require independence of those coordinates together with an additional 1. The paper explicitly distinguishes that latter condition for discrete translations. In particular, a direction whose last coordinate equals 1 is allowed and is adopted in Section 2 of the paper.
2. The discrepancy there is the unnormalized time integral minus T times volume. It has not already been divided by T.
3. There is one finite bound depending only on the fixed direction. It applies to every starting point and every T > 0, uniformly over all axis-parallel boxes in the unit cube.
4. The theorem is not restricted to anchored boxes. Its box definition is a product of intervals, with freely chosen lower and upper endpoints.
5. The paper's definition uses closed intervals. In any event, for the present direction every coordinate boundary has zero occupation time.
6. Its big-O convention is a uniform inequality for every T > 0, not a bound along an unspecified subsequence. The contradiction here would also need only eventual uniformity.

The inspected Borda PDF is 222149 bytes, SHA-256 `fddef4d3a9f17befc11ab06e9d65c86e7db1bd18a7ba8893ed5da400065ad1b9`.

The full text contains no occurrence of Steinerberger. Borda's explicitly identified disproved conjecture is Drmota's continuous-curve conjecture. Thus the Borda citation supplies the theorem for this reduction, not direct historical evidence of Steinerberger's intended convention or an explicit published resolution of his question.

## 2. Independent verification of admissibility

Fix C = [0,1]^3 and alpha = (sqrt(2), sqrt(3), 1). Its speed is v = sqrt(6). All coordinates are positive and algebraic. Their Q-linear independence follows, for example, by applying the sign-changing automorphisms of Q(sqrt(2),sqrt(3)) to a purported rational linear relation.

For a positive integer n, split 0 <= t <= n at every time when a coordinate of t alpha is an integer. Let K_n consist of the integer vectors k for the positive-length intervals on which floor(t alpha) = k. For every such k, take the entire affine line ell_k = R alpha - k, and set

    A_n = C intersect union_{k in K_n} ell_k.

There are only finitely many breakpoints and hence finitely many lines.

### Complete-chord check

The full parameter interval defining ell_k intersect C is exactly

    I_k = [ max_j(k_j / alpha_j), min_j((k_j+1) / alpha_j) ].

It contains the chosen open interval and has that interval as its interior. A useful direct check rules out truncation at both ends: each visited k has k_j >= 0 and 0 <= k_3 <= n-1. Therefore the lower endpoint of I_k is at least 0 and its upper endpoint is at most k_3+1 <= n. Thus the entire chord lies within the chosen parameter duration. There are no hidden extensions beyond 0 or n.

Equivalently, the initial chord starts at the origin, and the last chord exits through the z face at t=n. Interior breaks are ordinary complete exits and entries of adjacent lattice cells. No truncated interior segment has been substituted for a full chord.

### Distinctness and set measure

If ell_k = ell_l, then k-l = r alpha for some real r. The third coordinate forces r to be an integer; the first then forces r sqrt(2) to be an integer. Hence r=0 and k=l. The supporting lines are parallel and distinct, so they are pairwise disjoint, not merely disjoint up to positive-length overlaps.

Consequently the arclength of the union is the sum of the chord lengths. Repetitions and multiplicity are absent. The I_k partition [0,n] up to finitely many endpoints, giving exactly

    L_n = H^1(A_n) = v sum_k |I_k| = v n = sqrt(6) n.

The optional count in the attempt is also correct:

    N_n = floor(n sqrt(2)) + floor(n sqrt(3)) + n.

This follows by counting interior crossings and adding one interval. Positive crossing times from different coordinate families never coincide, since the coordinate ratios are irrational. The count is not needed to replace or estimate L; L has already been computed exactly.

### Integral and boundary check

For every bounded Borel function f on C, the piecewise-affine parameterizations give

    integral_{A_n} f dH^1 = v integral_0^n f({t alpha}) dt.

At a wrap, the closed endpoint of one chord may have coordinate 1 while the representative in the next cell has coordinate 0. The resulting differences involve only finitely many parameter values and image points and do not affect either integral. This identity itself is not restricted to axis-parallel test sets.

For an axis-parallel box R, each of its faces meets each chord in at most one point, because no coordinate of alpha is zero. All box boundaries therefore have zero arclength on A_n. Open, closed, and half-open conventions give the same discrepancy for this construction. Degenerate axis-parallel boxes also carry zero arclength and volume.

Dividing by L_n = vn yields the exact identity

    H^1(A_n intersect R) / L_n = (1/n) integral_0^n 1_R({t alpha}) dt.

The factor v cancels before the discrepancy theorem is applied. There is no extra n, speed, or line-count normalization.

## 3. Counterexample conclusion

Let K_alpha be Borda's fixed finite bound. Then

    sup_{axis-parallel boxes R in C} |H^1(A_n intersect R)/L_n - |R||
        <= K_alpha/n = sqrt(6) K_alpha/L_n.

The same upper bound holds for the subclass of axis-parallel cubes. Therefore the ratio of that cube discrepancy to log(L_n)/L_n is at most sqrt(6) K_alpha/log(L_n), which tends to zero. For every proposed positive universal lower-bound constant c, sufficiently large n contradicts the lower bound in this test class.

An explicit numerical value of K_alpha, a finite machine-generated example, or a known effective onset is not needed: the assertion being refuted is a universal asymptotic inequality. This is an existence counterexample sequence with a fully specified geometric construction.

The optional completion argument in the attempt is unnecessary for this exact construction. Its stated bounded endpoint-length correction is also consistent when the supporting lines are distinct and partial endpoint chords are completed as sets, counting any overlap only once.

## 4. Why arbitrary rotations remain separate

Borda's Theorem 1 does allow certain rotated polytopes, but its hypotheses require algebraic facet normals transverse to alpha, and its constant depends on those normals. This proves a bound uniform in translations and dilations of each such fixed polytope. It does not give a common bound over all cube orientations.

The excluded orientations genuinely include cubes. For example,

    nu = (sqrt(3), -sqrt(2), 0)

is an algebraic normal with nu dot alpha = 0. One can complete nu/|nu| and alpha/|alpha| to an algebraic orthonormal cube frame. Any sufficiently small cube in this orientation fits inside C, and some of its faces are parallel to alpha. Its normals fail the required transversality. This example does not itself prove high discrepancy; it pinpoints an actual missing hypothesis.

Even a bound for every fixed admissible algebraic orientation would not imply a uniform bound for their infinite union. Density of such orientations does not supply uniform constants. Conversely, this audit does not claim that the excluded orientations necessarily force logarithmic discrepancy. That requires a separate argument.

The original report at printed p. 2891 was rechecked: it stipulates cubes contained in the unit cube, with no explicit orientation convention. Its comparison with axis-parallel lifts of planar points is consistent with an axis-parallel intended reading, but is not a formal orientation specification. An acceptance report must retain that qualification unless further primary evidence settles it.

## 5. Nearby literature and final scope

A bounded search of Borda/continuous-flow discrepancy and Steinerberger/line/cube formulations found no inspected theorem establishing a uniform O(1/L) bound over all rotated cubes for these full-chord unions, and no inspected published logarithmic lower bound for arbitrary families of full chords. This negative search is not evidence that no such theorem exists or that the original problem remains open.

Borda reports a sharp logarithmic isotropic-discrepancy phenomenon for certain two-dimensional flows and attributes it to Beck. That is a different dimension and a larger class of convex tests, and its stated witness is a parallelogram. It is not a three-dimensional cube theorem and cannot resolve the present question by quotation alone.

A further inspected primary source is Michael Drmota, *Irregularities of continuous distributions*, Annales de l’Institut Fourier 39 (1989), 501–527, https://aif.centre-mersenne.org/article/AIF_1989__39_3_501_0.pdf (DOI https://doi.org/10.5802/aif.1175). Theorem 2 and Remark 3, printed p. 504, were checked in a rendered page image. For continuous curves of length s on the K-dimensional torus, the minimum time-occupation discrepancy for arbitrary-orientation torus cubes is bounded below by a constant times s^(-(1/2+1/(K-1))) and above by a constant times this quantity times sqrt(log(s+1)). In dimension three these are 1/s and sqrt(log(s+1))/s. For rotated cubes contained in the fundamental unit cube, Remark 3 states a lower bound of order s^(-1-epsilon), for any fixed epsilon > 0.

This is useful neighboring literature, but not the requested line-union theorem. Its objects are continuously parametrized curves with time-occupation measures, not necessarily normalized arclength on finite full-chord unions. Joining arbitrary disconnected chords may add length uncontrolled by the original total L. The upper construction in its Lemma 7 approximates point occupation by allowing variable-speed travel and dwelling; it cannot be read as a full-chord counterexample. The distinction between torus-wrapping cubes and contained cubes is also explicit. No logarithmic full-chord lower bound follows automatically.

Drmota retrieval audit: the journal PDF was successfully downloaded, text-extracted, and printed p. 504 rendered. Byte count 1478751; SHA-256 `411f9ae194eeaad20cd3e45200cfb107836bfb7d16676122abae33430b8b9dbc`. A web screenshot request failed with a cache miss; local rendering succeeded. The separate Borda workshop-slide URL returned 404 and was not treated as inspected evidence. These were retrieval errors, not access denials. Raw scholarly PDFs, extracts, and page images are not included in this package.

Recommended outcome label: **Axis-parallel formulation disproved via Borda's theorem; arbitrary-orientation formulation not resolved by this result.** Any unqualified claim of resolving the original as-printed question should be withheld.

## 6. Extension: audit of the weighted-square transfer and Attempts 3–5

Extended on 2026-10-20 UTC after reading `WEIGHTED_SQUARE_ROUTE.md`, `ATTEMPT_3.md`, `ATTEMPT_4.md`, and `ATTEMPT_5.md` in full. **All four mathematical arguments pass with the scopes stated below.** The numerical script and JSON were reviewed only as non-certifying diagnostics.

### 6.1 Weighted-square transfer, including atoms

The four-square indicator identity is correct with the oriented half-open convention. Partitioning both axes at 0, s, t, t+s verifies it cell by cell, including the partition endpoints. Applying it to the pairs of small squares at offsets (0,0), (t,t), and (2t,2t) gives the displayed three-equation elimination. Division by 2 gives a sum of absolute coefficient magnitudes at most 6 across twelve large-square terms.

The fitting calculation is sound: for s<1/10, the greater free gap in each coordinate exceeds 9/20; choosing 1/5<t<21/100 gives 2t<42/100. Consequently all auxiliary squares fit after the coordinatewise reflections. Their smallest side is t-s>1/10. The reflections preserve squares, containment, and the identity, with the inclusion convention reflected as well.

Importantly, the argument does not claim that the half-open identity holds pointwise for closed squares. Its passage to closed-square integrals correctly controls the difference. A finite total-variation measure charges only countably many vertical or horizontal lines with positive mass. After fixing a target with nonexceptional internal edges, one can choose t outside the countable forbidden set. Ambient edges that might carry mass occur only at the included starting edges; every excluded far edge is strictly internal and has zero mass. This justifies replacing all half-open square measures by closed square measures.

For an arbitrary closed target, the proposed slight outer enlargements are still squares because both coordinate intervals increase by the same epsilon. They contain the target, remain inside the ambient square, and converge pointwise to its closed indicator. Internal endpoints move with nonzero slope in epsilon, so one can avoid all countably many exceptional values. Dominated convergence against total variation is valid. This establishes the factor-6 estimate for arbitrary finite signed Borel measures. If side-zero squares are included in the test convention, the same enlargement limit handles them.

The pre-existing ordinary square discrepancy bound was independently checked in Matoušek, *Geometric Discrepancy*, Section 6.3, Theorem 6.3, printed pp. 180–182, at the public PDF linked in the companion note. It is the contained, axis-parallel square theorem, not a theorem for protruding squares or arbitrary rectangles. The book credits Halász and Ruzsa. The present argument separately supplies the side-length weight; no historical novelty is inferred.

The boundary-point removal argument also checks out. Squares tending to the full ambient square from inside detect the k boundary points omitted, giving W_N(P)>=k. For the interior points, the requisite square approximations can preserve all finite point incidences while tending in area and side length and avoiding ambient boundary points. Combining W_N(P)>=W_n(P_0)-k with the first inequality loses at most a factor 2. The finite-small-N adjustment can be made using more than N disjoint subsquare interiors and then shrinking an empty interior cell to remove any boundary atoms. Finally, the full-square test gives |N-T|<=W_T(P), so the arbitrary-reference-coefficient extension W_T(P)>=W_N(P)/2 is valid, even for real T.

### 6.2 Attempt 3: universal rotating-cube bound

The claimed bound

    D_rot(A) >= 1/(16 max(1,L))

is accepted. After removing repetitions and zero-length chords, the chosen face plane contains precisely the selected line and no other line. Each forbidden choice of its normal removes only finitely many points of the normal circle, since parallel directions and nonparallel directions are correctly treated separately.

Selecting a side length in [1/8,1/6] outside a finite exceptional set eliminates other lines contained in the remaining five boundary planes. The cube's furthest corner is at distance sqrt(3/2)a<1/4 from the selected core point, giving a strict containment margin for both signs of small translations.

All other lines have zero arclength on the boundary at the limiting cube, so dominated convergence on their finite chords proves their two-sided continuity. The selected line contributes length a on one side and zero on the other. The signed discrepancy limits differ by a/L, forcing one absolute limit to be at least a/(2L)>=1/(16L). A supremum bounds these approached limits; actual attainment is not needed. No hidden N-dependent estimate is used. The empty-core case and L<1 case cover the remaining range exactly as claimed.

This result genuinely needs orientation freedom. It neither proves the missing logarithm nor contradicts the axis-parallel construction.

### 6.3 Attempt 4: all mutually parallel families

The logarithmic lower bound for mutually parallel families is accepted. Repetitions and zero-length defining lines may be discarded before counting projections, without changing any arclength. This preprocessing makes the subsequent projection count unambiguous.

The cube of side a=1/(2 sqrt(3)) centered at the ambient center is contained in C for every orthonormal frame. In a frame whose third axis is the common line direction, each selected line contributes exactly a to that cube. This remains true for projections on its closed base boundary. Projections of distinct parallel lines are distinct.

The dichotomy supplied by the fixed interior cube is correct: either there is fixed positive discrepancy, or m>La^2/2. The subsequent exact identity is

    |mu_A(Q)-|Q|| = (a/L) t |#(P intersect S)-La^2 t^2|.

In particular, the reference coefficient is La^2, not m. The companion lemma's arbitrary-coefficient extension is precisely what is required. For sufficiently large L, m>La^2/2 implies log m >= (1/2)log L. The earlier 1/L bound handles the bounded interval of L>1 after one universal constant reduction. Thus the constants are independent of the direction and the original total number of lines.

For later use, the large-L proof is valid in any one chosen frame aligned with the line direction. It does not optimize the in-plane rotation. This follows by using discrepancy restricted to that frame in the initial dichotomy: both the fixed interior cube and all subsequent cubes lie in that same frame. Attempt 3 is needed only for the bounded-L extension, not this fixed-frame large-L assertion.

### 6.4 Attempt 5: fixed finite algebraic-flow mixtures

The restricted mixture obstruction is accepted. The required hypotheses are explicitly listed: a fixed finite set of positive algebraic, coordinatewise Q-independent directions, each with a coordinate equal to 1, and no parallel pair. They justify the integer-stop full chords and distinctness within each family. Different families have only point intersections, so both the total length n sum_j||alpha_j|| and the signed error decomposition are exact.

The selected algebraic frame exists. Normalize alpha_1 to obtain e_3, construct an algebraic orthonormal basis f,g of its perpendicular plane, and choose e_1=(f+r g)/sqrt(1+r^2) for a rational r outside finitely many forbidden values. Then e_2=e_3 cross e_1 is algebraic. Nonparallelity ensures that none of the relevant forbidden equations is identically zero in r. Positivity ensures e_3 dot alpha_j>0. All other face-normal scalar products can therefore be made nonzero simultaneously.

The first family's fixed-frame unnormalized error is at least c_0 log(n||alpha_1||), by the preceding large-L fixed-frame reduction. For every other family, Borda's Theorem 1 applies to every positive-side cube in this same frame. Its six normals are fixed, algebraic, and transverse. Thus its bound is uniform in center, side length, and n. Passing from time discrepancy to unnormalized arclength multiplies the bound by the fixed speed; this can be absorbed into B_j.

The supremum inequality used to prevent cancellation is valid even without attainment:

    sup_Q |sum_j E_j(Q)| >= sup_Q |E_1(Q)| - sum_{j>1} sup_Q |E_j(Q)|.

The right side is c_0 log(n||alpha_1||)-sum_{j>1}B_j. For a fixed family the subtracted term and the difference between log(n||alpha_1||) and log L_n are constants. This proves the eventual logarithmic lower bound, with a threshold allowed to depend on the fixed family. It does not give a uniform threshold or bounded error sum for a direction list changing with n. It also says nothing comparable about arbitrary unions whose other directional components lack Borda's bounded-error structure.

The same finite mixtures retain O(1/L_n) discrepancy for axis-parallel cubes by summing Corollary 2 bounds. This further emphasizes, rather than removes, the orientation distinction.

### 6.5 Numerical scope and consistency

The reported sample count is correct: four special frames with 180 cubes each and 24 additional frames with 50 cubes each give 1920 cubes. The six JSON rows have the correct chord counts, lengths consistent with n sqrt(6), orthonormal maximizing frames within floating-point tolerance, contained maximizing cubes within that tolerance, and internally consistent normalized statistics. The quoted three-direction values agree with the JSON.

No exact-interval error bounds were computed and no supremum upper bound was proved. An exactly evaluated finite sample maximum would be a lower bound on the supremum; the floating-point outputs here are only approximations to such sample maxima, not certified lower bounds. The script's opening comment and the experiment narrative must preserve this distinction. None of the accepted theorems depends on these data.

## 7. Consolidated acceptance and unresolved target

Accepted mathematical conclusions, with no novelty claim:

- The axis-parallel logarithmic statement is false, by the explicit Borda full-chord sequence.
- Arbitrary finite full-line unions satisfy the rotating-cube baseline 1/(16 max(1,L)).
- Every mutually parallel family satisfies the rotating-cube logarithmic lower bound.
- Every fixed finite mixture of the specified nonparallel algebraic-flow families also has the eventual rotating-cube logarithmic lower bound.

**Still unresolved by this work:** the logarithmic lower bound for arbitrary finite full-line unions when all cube rotations are permitted. The original source's missing orientation clause prevents an unqualified original-problem resolution label. No argument above extends the fixed-mixture result to growing direction families or eliminates cancellation for general multidirectional configurations.
