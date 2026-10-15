# Independent audit of planar valuation covariogram partial results

Target 30000630 / OWR-1394-006, rank 1095. Audit date 8 October 2026.

## Verdict

**Accept the scoped partial results, with the proof-detail strengthening in `REVIEWED.patch`. The full arbitrary-body determination problem remains unresolved in this packet, after five of five substantive approaches.** No substantive mathematical error was found in the frozen authored conclusions. The patch makes two compressed steps explicit: preservation of monotonicity after Euler-characteristic normalization, and exact local body-germ matching plus uniform lens localization in Proposition 5.1. It does not change the propositions, introduce a sixth approach, or assert equality of the full interior covariograms.

This is a mathematical audit with finite regression evidence, not a formal proof-assistant verification or novelty assessment. The classical valuation-classification theorems, mixed-area representation, and Brunn–Minkowski equality case remain identified external dependencies. The arbitrary-body theorem and a full-covariogram counterexample are both absent.

## Material bound to this audit

The six authored originals were frozen before this audit and compared byte-for-byte with the authored directory on resumption. `FROZEN_EVIDENCE.json` records their lengths and SHA-256 hashes. The original report has SHA-256 `8fd31d8a4e362825d40feba7a283390257e90ddfeb273d6c17f3fadc9eb06b7c`. The checker has SHA-256 `7169a26fab2cbc3a59cea1139b69357b6bc0fd49d5439862b84eacbb60ab037e`.

The reviewed directory preserves the same checker, routes, source interfaces, and original test receipt. Only the mathematical report and its manifest change. The contextual patch applies to the frozen copy. Source PDFs, source transcriptions, dataset bodies, and private coordination material are not in this audit delivery.

## Exact source and scope

The original target occurs in Bianchi's contribution to OWR 56/2006, printed pages 3343–3344, corresponding to PDF pages 23–24. The relevant pages were inspected as text and rendered images. The general valuation question and the separate proposed polygon result are distinct. The target does not expressly impose evenness or homogeneity. The report's distinction between full-dimensional bodies and their possibly lower-dimensional intersections is necessary. [Primary report](https://ems.press/content/serial-article-files/46086).

The controlling later source is Averkov–Bianchi's inspected arXiv:1307.1529v2 manuscript dated 10 November 2014. The classification argument was inspected on manuscript page 7, the lower-dimensional convention on page 6, and the normalization and boundary-edge formulas on pages 7 and 15. Theorem statements on pages 2–3 distinguish centrally symmetric bodies, strictly monotone polygon data, and directional-width polygon data. The arbitrary-convex-competitor quantifier must be retained. Section 7 separately formulates the arbitrary-body and outside-class questions. The original report's treatment is accurate. [Versioned primary manuscript](https://arxiv.org/pdf/1307.1529v2).

A polygonal difference body forces both summands to be polygons. One way to see the relevant fact in the plane is through support functions: on each open normal interval where the sum is linear as a homogeneous support function, convexity prevents nonlinearity of one summand being canceled by the other. Equivalently, the nonnegative planar surface-area measures of both summands are supported on the finitely many normals of their polygonal sum. This justifies the all-convex-competitor scope of the credited polygon theorem; it gives no passage to curved bodies.

The publisher DOI was checked again but its full article was not accessible through the reader. No conclusion below asserts that its typeset version retains the manuscript discrepancies. The cited ordinary-area theorem is verified as determining all planar convex bodies, but is used only for pure area or when extra observations recover area-covariogram data. [Ordinary-area primary article](https://ems.press/journals/jems/articles/1922).

## Source normalization checks

### Strict monotonicity

The v2 page 2 definition quantifies over nonempty proper inclusions in the full compact-convex domain. Its page 3 positive-area-coefficient sufficiency statement cannot hold under that definition. Two nested nondegenerate segments have the same area zero. Pure area is therefore body-strict but not strongly strict. Adding a degenerate directional-width term need not repair strictness on segments in its kernel. These are direct geometric counterexamples to the unqualified sufficiency sentence, not to the paper's stated polygon uniqueness theorem.

For positive area coefficient and two full-dimensional properly nested bodies, the area difference is strictly positive, so the narrower sufficiency statement is correct. Euclidean perimeter itself is strongly strict: the support-function gap for a proper inclusion is nonnegative everywhere and positive on an open set; the associated width gap is then positive on an open set. The Cauchy width integral, including its segment extension, is strictly larger. Thus the report's principal perimeter application is unaffected.

### Segments and the factor two

On v2 page 6, a lower-dimensional set receives twice its seminorm length. At the midpoint of an edge of the difference body, the opposing faces of a polygon are centered against each other. Their overlap segment has seminorm length equal to the smaller opposing edge length. Its valuation contribution is consequently twice that minimum. The area contribution is zero. The page 15 display in Claim 5.2.1 omits this factor.

For a rectangle of horizontal side length 2 and vertical side length 1, translation by (0,1) leaves a horizontal segment of length 2. Its continuous convex perimeter is 4. This also shows why ambient boundary length of a segment, which counts it only once, is the wrong extension. Restoring the known factor two still recovers the smaller face length, so this local correction does not defeat that recovery step.

### Singleton normalization

Subtracting the singleton value from every set including the empty set would destroy the zero empty-set value. The correct operation is subtraction of the Euler valuation, which equals one exactly on nonempty compact convex sets. The intersection is nonempty exactly on the closed difference body. Thus its covariogram contribution is the singleton coefficient times that closed-set indicator, including the boundary. Outside the difference body, both original and normalized covariograms must vanish. The report already uses the correct formula; the patch supplies a detailed preservation argument.

## Classification without evenness

The accepted domain is real-valued valuations on all compact convex subsets, with zero value at the empty set, monotonicity including that set, and translation invariance. This is stronger and more precise than a functional specified only on full-dimensional bodies. The classification cannot be applied to an unspecified lower-dimensional extension.

Translation invariance gives a common singleton value c0. Monotonicity gives c0 ≥ 0 and φ(C) ≥ c0 for every nonempty C. Therefore ψ = φ − c0χ is a valuation, is zero on singletons and the empty set, and remains monotone. For two nonempty nested sets the same constant is subtracted; for the empty-set comparison, ψ is nonnegative.

The cited continuity theorem concerns Hausdorff continuity on nonempty compact convex sets. The empty set is treated separately; no claimed limit from nonempty sets to the empty set is needed. Apply continuous translation-invariant homogeneous decomposition. The degree-zero component is determined by the limit as a nonempty body shrinks to a point and hence vanishes after normalization. In dimension two, only degrees one and two remain. Their small- and large-scale limit formulas inherit monotonicity. The degree-two classification gives αA with α ≥ 0. The monotone degree-one classification gives V(·,H) for nonempty compact convex H, including a segment or singleton.

Evenness is used only to symmetrize H after these steps. It is unnecessary for the preceding classification. The mixed-area functional determines H modulo translation; first-harmonic additions to its support function are precisely translations and vanish against every planar surface-area measure. The zero degree-one term corresponds to singleton H. At least one of nonsingleton H and α > 0 is required in the nonzero normalized class.

The v2 proof identifies McMullen's continuity and homogeneous-decomposition results, the degree-two volume classification, and the degree-one mixed-volume classification. I checked the use and hypotheses in that proof. The original proofs of all these classical theorems were not independently re-proved or fully inspected. The publisher abstract for Firey's classification was independently checked and is consistent with the non-even mixed-volume interface, but is not substituted for inspection of its complete proof. [Firey's primary publisher record](https://link.springer.com/article/10.1007/BF02834758). This dependency limit does not affect the directly stated results for a given valuation V(·,H) + αA.

## Reflection and the triangle example

For any translation-invariant valuation, the overlap for −x is a translate of the overlap for x, so the function of x is even. Reflecting the unknown body changes the valuation applied to the overlap to C ↦ φ(−C). These are different statements. If reflected bodies always had identical data, evaluation at zero would force the valuation to be even on those bodies.

For T = conv{(0,0),(1,0),(0,1)}, area is 1/2 and the difference hexagon has area 3. The mixed-area polarization gives V(T,T) = 1/2 and V(−T,T) = 1. Adding perimeter gives a strongly strict, monotone, translation-invariant valuation whose data at zero distinguish T and −T. This pair does not have equal covariograms, so it is not a counterexample to the equality-implies-equivalence target. The report correctly limits its role to clarification of the symmetry assumption.

The exact triangle arithmetic was reproduced both through the authored convex-hull calculation and through an independent polygon edge-normal formula. For a counterclockwise polygon, twice its mixed area with H is the sum of h_H(dy,−dx) over its directed edges. This latter calculation includes nonsymmetric H, a translated H, a segment, and a singleton.

## Support integral and reconstruction

For a full-dimensional body K, the intersection has interior whenever x is in the interior of K−K. This follows from int(K−K) = int K − int K. A nonsingleton H has positive mixed area with a disk: it is proportional to the disk radius times the continuous convex perimeter of H, which is positive even for a nondegenerate segment. Putting a translated disk inside the overlap therefore proves positivity of the mixed-area term there. If H is a singleton, the positive area coefficient supplies positivity. Off K−K the overlap is empty. The closure of the nonzero set is thus exactly K−K. No global boundary continuity is needed.

For the integral identity, translate H to contain the origin. The weighted boundary density is one half its support function at the outer normal. Its total mass on ∂K is V(K,H). For almost every x, ∂K and ∂(K+x) have intersection of length zero: integrating the common length in x gives zero by Fubini since ∂K has planar measure zero. Up to such a null set and the lower-dimensional overlap translations on the difference-body boundary, the overlap boundary is the union of one boundary portion from K and one from K+x, with the inherited outward normals. Both contributions integrate to A(K)V(K,H). Their orientation does not require h_H(u) = h_H(−u). The ordinary indicator convolution gives the αA(K)^2 contribution.

Hence, writing a = A(K), p = V(K,H), c = p + αa and I = 2ap + αa²,

c² − αI = p²,

and I / (c + sqrt(c² − αI)) = a. The denominator is 2p + αa and is positive under the nonzero/full-dimensional hypotheses. With α = 0 this is I/(2c); with p = 0 it remains valid at discriminant zero. If α > 0 and p > 0, the other quadratic root makes c − αa negative and violates p ≥ 0. The report correctly chooses the admissible root and includes the degenerate cases.

For an original c0χ term, the observed support and known c0 allow the entire Euler contribution to be subtracted without an extra measurement. A strictly monotone valuation cannot reduce to c0χ alone, since that functional is constant on every pair of nonempty nested bodies.

## Centrally symmetric determination

The support and reconstruction formula recover the difference body and total area for every full-dimensional competitor. If the original body is centrally symmetric, its difference-body area is four times its own area. Equality of the reconstructed areas puts the competitor and its negative in the equality case of the planar Brunn–Minkowski inequality. Full dimensionality is indispensable for the standard equality characterization. The two sets are positively homothetic; their equal areas force ratio one, so the competitor is centrally symmetric. A centered centrally symmetric body is one half of its difference body. The resulting equality is up to translation, among all full-dimensional convex competitors, with no evenness assumption on H.

This is a valid scoped consequence of the earlier invariants. It is not an argument for general nonsymmetric bodies: equal area and difference body do not generally recover their support functions.

## Smooth lens coefficients and analytic continuation

A C² support function with positive h+h'' yields a regular strictly convex boundary with continuous positive curvature. The two graph expansions at opposite support points have curvatures κ+ and κ− and gap ε − (κ+ + κ−)s²/2 + o(s²). Compactness forces the whole lens into those graphs as ε decreases to zero. Its tangent half-width is sqrt(2ε/(κ+ + κ−))(1+o(1)). Positive curvature also ensures exactly two nearby crossing endpoints for sufficiently small positive ε.

Each boundary arc has length twice that half-width to leading order. Its weighted mixed-area mass is one half of that arc length times the appropriate limiting support-function value. Adding the two arcs gives

w_H(u) sqrt(2/(κ+ + κ−)) sqrt(ε).

Integrating the parabolic gap gives area coefficient (4/3)sqrt(2/(κ+ + κ−)) at order ε^(3/2), so an area term cannot change the leading square-root coefficient. Euclidean perimeter corresponds to H = 2B, whose width is 4. For a disk of radius R, κ+ + κ− = 2/R, giving 4sqrt(R). The exact circular-lens perimeter, 4R arccos(1−ε/(2R)), independently confirms it.

The difference body determines the sum s of opposite curvature radii. If the measured leading coefficient is L and w = w_H(u) > 0, the curvature sum is q = 2w²/L². Consequently the radius product is s/q, and the roots of z² − sz + s/q recover the unordered pair. A nondegenerate segment H has zero width in exactly one antipodal pair of normal directions; continuity fills those two missing directions. A singleton H requires the separate pure-area case. The report handles both degeneracies correctly.

For the analytic theorem, both unknown competitors have analytic support functions and positive curvature. Their radius functions are analytic. The identity (b−a)(b−a shifted by π) = 0 holds pointwise by the unordered-pair recovery. If the first factor is not identically zero, it is nonzero on an interval, so the second factor vanishes there and then everywhere by analytic continuation on the connected circle. The resulting radius equality makes the support-function difference solve d''+d=0, exactly the first harmonics corresponding to translations. The antipodal branch is a point reflection followed by translation.

No regularization of arbitrary competitors follows from this argument. Replacing “both competitors analytic” by “the original body analytic” is not justified. The report states and emphasizes the correct restricted competitor class.

## Exact smooth switching obstruction

For separated antipodally odd smooth bumps f and g, h± = R+f±g have positive values and positive curvature radii under the displayed strict bound on R. Oddness makes the widths 2R and the integrals of both bumps zero. Consequently both difference bodies are the radius-2R disk and both perimeters are 2πR.

The support-function area identity contains cross terms fg and f'g'. They vanish identically because the closed supports are separated and derivatives vanish off the original support. The remaining g terms are quadratic, hence invariant under its sign change; linear terms integrate to zero. Thus areas agree exactly. The same disjointness applies to F = f+f'' and G = g+g'', giving unordered pairs {R±(F+G)} and {R±(F−G)}; at each direction at least one of F,G is zero. Both pairs agree.

The difference of the two support functions is 2g, a nonzero function vanishing on an open interval. It cannot solve d''+d=0, so there is no translation. Comparing one support function with the other's antipodal translate instead gives 2f, excluding point reflection followed by translation.

The exact collar argument needs more than equality of curvature pairs or leading asymptotics. The reviewed proof supplies the following four steps in full.

1. Equality of support functions on a normal interval implies equality of the bodies inside a small Euclidean ball about the common support point. Smoothness makes all support inequalities for complementary normals uniformly slack there; the remaining inequalities coincide. Repeat this at the opposite normal.
2. Positive support separation gives an antipodal pair of intervals on which either g is zero, so K− locally agrees with K+, or f is zero, so K− locally agrees with −K+. The signs and antipodal derivative values agree as support functions, so the actual support points agree, not only their curvatures.
3. At x0 = 2Ru, each contact intersection is a singleton. Any sequence of points in nearby nonempty overlap lenses has its limit in that singleton, by compactness and closedness. Their translated-back points converge to the opposite contact point. This localizes the entire intersection for both bodies, uniformly in all translation directions approaching the chosen x0. Applying the two body-germ equalities gives exact equality of the localized lens sets. In the switched case the map z ↦ x−z sends the K+ lens to the −K+ lens and preserves perimeter.
4. The translation neighborhoods in which equality holds form an open cover of the compact difference-body boundary. A finite subcover has positive distance from that boundary to its closed complement, yielding one collar width valid for all directions, inward and outward. Empty and singleton intersections cause no exception.

Thus exact boundary-collar equality is accepted. No claim that these bodies have identical full covariograms is accepted. Nor does the audit assert an interior inequality that has not been established. The common full integral follows only from the common area and perimeter via the integral identity. Equal integrals cannot replace pointwise equality in the unobserved interior.

## Two scale identity and the stopping point

For a supplied second observation of tK, the overlap at tx is t times the original overlap at x. The degree-one term scales by t and area by t². Subtracting t times the first observation therefore isolates αt(t−1) times the ordinary area covariogram. Division is allowed exactly when α > 0, t > 0, and t ≠ 1.

Evaluating the original observed function at tx changes the displacement while keeping the body K fixed. It does not produce the covariogram of tK. The extra observation is genuinely absent from the original problem, and in the pure degree-one case it would be redundant. The report does not make the invalid single-measurement reduction.

The five approaches remain the non-even symmetry analysis, invariant integration, smooth lens and analytic analysis, smooth switching obstruction, and two-scale decomposition. The audit only checks and clarifies their results. Full interior propagation, arbitrary nonsmooth competitors, and a full equal-covariogram pair are still missing. No sixth proof route was attempted.

## Independent computations and mutation evidence

The original standard-library checker was inspected before execution. Its guards use explicit exceptions, not Python assertions. Direct normal, -O, and -OO executions each passed 61 checks, including its 16 invalid-input checks. An independent checker reproduced those tests and added 54 checks per mode, including unfamiliar rational fixtures, the edge-normal mixed-area formula, rectangle integration, parabolic-lens area constants, three disk radii, supported Euler normalization, and degenerate domains.

All tested processes actually ran with UID 1000 and EUID 1000. The replica files had mode 0444 and directories 0555. Opening the candidate for append and creating a new file in its directory both raised PermissionError. Tree content hashes and modes agreed before and after the runs. Bytecode writes were disabled. These are verified read-only filesystem conditions, not a claim of a hostile-code sandbox: the owner could deliberately change modes, but the reviewed checker does not do so.

Twelve single-source mutations were run in every mode, for 36 rejected mutation executions:

- wrong discriminant sign, wrong quadratic root, and extra factor two in the reconstruction denominator;
- multiplying rather than dividing to recover the radius product, and a wrong factor in the quadratic roots;
- omitting the dilation factor from the degree-one subtraction and changing the dilation determinant;
- omitting the mixed-area polarization factor one half;
- admitting booleans, admitting negative area coefficient, and admitting negative dilation;
- halving the exact circular-lens perimeter.

The negative-area-coefficient mutation is particularly useful: the authored invalid fixture can still fail indirectly at its nonrational square root after the domain guard is removed. The independent fixture c=1, I=3, α=−1 instead has perfect-square discriminant 4 and specifically detects the missing coefficient guard. The original checker rejects it correctly. This is a regression-coverage strengthening, not a defect in the original implementation.

The exact geometric propositions are supported by the mathematical arguments above and in the reviewed report. None is inferred from these finite checks. The rational-square-root helper intentionally rejects nonsquare rational discriminants; it is a fixture evaluator, not a numerical inversion package for arbitrary measured data.

## Acceptance boundaries

Accepted: normalization and class distinctions; the non-even reflection clarification; support, integrated mass, area reconstruction, and centrally symmetric determination; smooth curvature-pair recovery; analytic uniqueness with both analytic competitors; the exact uniform boundary-collar obstruction; and two-scale inversion with an additional observation.

Not established: arbitrary-body uniqueness for a single perimeter or general strictly monotone valuation covariogram; analytic-body uniqueness among arbitrary competitors; full interior equality for the switching pair; independence from the classical classification dependencies; publisher-version errata; novelty; or worldwide current openness.

`ACCEPTANCE.json` binds this verdict to the frozen input and reviewed output. No repository or queue operation is part of the audit.
