# Adversarial audit of constant width billiards problem 30002659

Date: 2026-10-03 UTC. Reviewed the frozen five-attempt packet as a fresh, uninvolved mathematical reviewer.

## Verdict and scope

**PASS for the stated partial results and their advertised limitations. HOLD for any claim that the original problem is solved.** No substantive mathematical defect was found in the five arguments. No proof repair is necessary to retain their present, limited conclusions. Small clarification edits are listed below; they do not close the original problem.

The unresolved target is that **every** shortest closed generalized Euclidean billiard trajectory in **every** constant-width body has period two. Proving existence of one two-bounce minimizer, or only the lower bound of twice the width, would not settle the full equality-case target. The packet correctly distinguishes these statements and correctly remains **unsolved after five substantive author attempts**.

This independent AI adversarial review does not certify novelty, exhaustive literature coverage, or human peer review. No new optimization run or additional proof-search attempt was used for this audit.

## Frozen input and verification record

The public packet contains 14 files including its manifest. All 13 listed file hashes match. The manifest itself has SHA-256:

    121186eec27a64d42972f33fd155cf48ad6e6600b45b72cab75d320a7e189896

The author verifier reproduces the saved JSON exactly with SymPy 1.14.0 and reports 156 assertions. I also wrote a separate verifier that reconstructs the existing fixtures from explicit expected normals, checks their supporting-ball inequalities and all pairwise distances, checks the displayed algebra, and reads the saved numerical coordinates without invoking the optimizer. Its 265 checks pass. The check count includes manifest and reproduction checks; it is not a count of independent theorems.

The audit files are separate from the frozen author files, in the `audit/` subfolder:

- `AUDIT_REPORT.md`: this report
- `audit_controls.py`: independent verification of existing controls and saved outputs
- `audit_controls_results.json`: its result
- `SHA256SUMS`: audit-file hashes, excluding itself

Run `python audit_controls.py` from this audit folder to reproduce the supplementary checks. It requires SymPy and NumPy. Neither verifier proves the universal conjecture.

## Source scope verified directly

The 2014 Oberwolfach report states the planar result for any shortest trajectory and asks for the same statement in higher dimensions. Its later Theorem 10 expressly includes the equality classification as a diameter traversed twice. The packet's reading of the target, workshop year, and printed page locations is correct. [Oberwolfach Report 40/2014, printed pp. 2242 and 2258](https://publications.mfo.de/bitstream/handle/mfo/3430/OWR_2014_40.pdf?isAllowed=y&sequence=1)

Bezdek–Bezdek Theorem 1.1 supplies existence and the period bound for **any** shortest generalized trajectory, rather than merely the existence of some minimizer with at most n+1 vertices. Their generalized definition permits self-intersections and supporting hyperplanes at nonsmooth boundary points. Its hypotheses match the use here. [Shortest billiard trajectories, Theorem 1.1](https://arxiv.org/pdf/1110.4324)

For completion, Akin's Theorem 1.3(e) gives an r-maximal containing set; Theorem 0.2(a) ensures compactness, convexity, and nonempty interior in finite-dimensional normed space; Corollary 3.13 identifies Euclidean r-maximal sets with constant-width sets. This independently validates the exact classical input needed in Attempt 2. The alternate Moreno–Schneider DOI did not resolve in this audit, but that does not leave a dependency gap because Akin supplies the needed statements directly. [Maximal r-Diameter Sets and Solids of Constant Width](https://arxiv.org/pdf/1003.5824)

The cited Tsodikovich manuscript, Remarks 2 after Theorem 2 on PDF page 3, does describe the all-dimensional statement as conjectured. I did not repeat an exhaustive 2025–2026 literature or repository-duplicate search, so those historical search records retain the status of author-reported searches, not independently certified completeness. [An analogue of the Blaschke–Santaló inequality for billiard dynamics](https://arxiv.org/pdf/2204.06209)

## Attempt 1 passes

### Antipodes and nonsmooth bodies

The diameter and antipode argument is sound. For a support point x with unit outward normal u and an opposite support point y, constant width gives (x-y)·u=1 and the diameter bound gives |x-y|≤1. Equality forces y=x-u. Applying the same observation with this fixed y to every point in the first support plane proves uniqueness of the supporting contact for the chosen u.

Uniqueness for each support direction proves strict convexity. It does **not** require a unique normal at each boundary point. In particular, corners are allowed, and the antipode identity holds for each selected supporting normal at a corner. The argument does not mistake strict convexity for boundary smoothness.

A two-bounce orbit has its chord perpendicular to supporting planes at both endpoints. The planes have separation one, so its length is two. Conversely the antipodal chord yields such an orbit. This provides the upper bound two on the minimum and the exact length of every two-bounce orbit.

### Projection preserves the required data

Projecting onto the affine span of the vertices fixes every vertex, edge, edge length, and edge direction. The selected reflection normal is a difference of two unit edge directions, so it is parallel to the same affine span. For any z in K, projection therefore preserves (z-x_i)·n_i. The supporting inequality transfers to the projection, placing x_i on its boundary and preserving the generalized reflection law.

The projected body has nonempty relative interior and constant width one. Thus the planar theorem applies, including its equality classification. A planar orbit has length at least two; equality makes it a shortest orbit in that planar body and hence a two-bounce orbit. Higher-period planar orbits are strictly longer than two. In affine dimension one the image is an interval, and the same conclusion follows directly.

Combined with the cited period bound, a three-dimensional counterexample must have an affinely independent four-vertex minimizing orbit. The reduction does not assume every orbit is planar or preserve reflections under an arbitrary lower-dimensional projection.

## Attempt 2 passes

### Exact realization criterion

For nonzero consecutive edges and nonzero reflection differences, define n_i as in the packet and y_i=x_i-n_i. Necessity of diam({x_i,y_i})≤1 follows from the antipode identity.

For sufficiency, the classical completion gives a full-dimensional constant-width-one body K containing all x_i and y_i. For every z in K,

    |z-y_i|²≤1=|x_i-y_i|²

expands to

    2(z-x_i)·n_i+|z-x_i|²≤0.

Therefore n_i supports K at x_i. This works simultaneously for all contacts; no compatibility condition has been omitted. It also gives strict inequality (z-x_i)·n_i<0 for every z≠x_i in K. Convexity places each edge in K, and strict convexity puts its open segment in the interior. Thus the result constructs actual generalized billiard reflections, rather than merely points with formal normals.

The completion theorem preserves the finite data in the same finite-dimensional Euclidean ambient space, including when the data have smaller affine span. The finite set has diameter exactly one because each designated x_i,y_i pair is a unit pair. Neither smoothness nor uniqueness of completion is needed.

### All pair constraints and equality

The XX, ordered XY, and YY polynomial constraints have the correct signs. In particular,

    |t(q_i-q_j)+n_j|²≤1

is the ordered XY condition, and

    |t(q_i-q_j)-(n_i-n_j)|²≤1

is the YY condition. Keeping both orders of XY is essential and the packet does so. At i=j the XY constraint is exactly a unit-pair equality.

The length-two witness dichotomy is correct. A primitive non-two-bounce feasible polygon of length two either attains a minimum equal to two or exists in a completion with a smaller minimum. Both alternatives refute the every-shortest-orbit target. A strict length-below-two witness also refutes it. The equivalence to strict length greater than two for every feasible primitive non-two-bounce polygon is consequently valid.

Primitivity here concerns traversal of a repeated full cycle. It should not be interpreted as permitting arbitrary deletion of repeated contact points or self-intersections, which might change reflection laws. No argument in the packet relies on such deletion.

## Attempt 3 passes

### Symbolic family exclusion

For the stated vertices all four squared side lengths are 4(a²+b²), and the first reflection difference is (a,2b,a)/q. Normalization gives exactly the stated n_0 with r²=2a²+4b². The family is genuinely spatial for a,b>0.

Under L≤2, q≤1/4 and r≤1/2, so the signs used in defining A and B are legitimate. The listed YY distances are correct. The first branch uses positive lower bounds in the correct direction:

    A²≥175/1152>1/8.

For the second branch, decreasing q increases both nonnegative coordinate magnitudes. The formula for F(z), its derivative, and F(1/8)=43/144 are correct. The displayed estimate proves F'(z)>0 throughout [0,1], including the endpoints. Hence A²+B²>1/4 on the second branch. These strict contradictions are enough; no XX or XY constraints need to be used.

The b=0 endpoint is planar. The a=0 endpoint has repeated alternating points, not an affinely independent tetrahedron. If it is realizable, their distance must be one, so the four-edge traversal has length four. These degeneracies cannot create an overlooked length-two higher-period minimizer.

The result is confined to this symmetric family. The packet properly supplies no unjustified symmetrization principle for a general tetrahedral four-orbit.

### Numerical audit

Recomputation from every saved coordinate array, with exact antipodal pairs included in the floating-point distance check and without the optimizer's denominator clipping, gives:

- 80 saved runs with exactly the indices 0 through 79
- 76 diagnostics meeting the tolerance of -10^-7
- best diagnostic run 63, length 2.353276790915113
- its minimum all-pair slack: -1.4526158054195548×10^-12
- maximal discrepancy against saved length and six-volume fields: zero in this environment
- maximal discrepancy in the saved versus recomputed slack field: approximately 7.73×10^-13

The small slack discrepancy is harmless floating-point arithmetic variation and changes no tolerance classification. The best run has a positive edge minimum and positive turn minimum, so denominator clipping does not account for its reported result.

The six-variable gauge and cutoffs omit degenerate limits. Local SLSQP runs cannot give global coverage or an exact feasibility certificate, and the best result has a slightly violated inequality. All of these limitations are correctly disclosed. I did not run new starts or convert these numbers into a purported exact witness or lower bound.

## Attempt 4 passes

With a_i>0, A>0 and lambda_i=a_i/A, weighted normal balance follows by telescoping. The perimeter identity has the correct sign:

    sum_i x_i·(u_(i-1)-u_i)=sum_i (x_(i+1)-x_i)·u_i=L.

The weighted Cauchy–Schwarz step is valid because sum_i lambda_i |n_i|²=1 and sum_i lambda_i n_i=0. The variance identity counts ordered pairs with the necessary factor 1/2. Removing the diagonal terms gives exactly (1-sigma)/2, not 1/2. Therefore the stated moment bound

    L≥A[1-sqrt((1-sigma)/2)]

is correct for every orbit satisfying the finite realization test.

The proof A≥4 is also valid. Closure supplies strictly positive original-edge weights with weighted mean direction zero. For any ball containing the unit edge directions, its radius is at least one by the weighted squared-distance identity. A closed polygonal curve of perimeter A is contained in the ball of radius A/4 centered at the midpoint of two points separated by half its arclength: each point lies on one of the two half-arcs, and Euclidean triangle inequalities give the displayed bound. The direction polygon has exactly perimeter A, so A≥4 follows. No smoothness, simple-polygon assumption, or unproved total-curvature theorem is needed.

The substitutions sigma≥1/m and, for shortest orbits, m≤n+1 have the correct monotonic direction. The four-bounce universal high-turn threshold is approximately 5.15959179422654248, as recorded. Strict inequality in A gives strict L>2. The packet correctly declines to turn equality at the threshold into strictness without additional analysis.

The bound is a necessary filter and remains too weak to prove the conjecture. Small total chordal turn is not excluded.

## Attempt 5 passes

### Weighted antipodal criterion and equality

At a selected supporting normal, x_i·n_i=h(n_i), even if the boundary has a corner. Thus the support-function identity follows from the perimeter identity. Constant width makes h(u)-1/2 odd for every choice of origin. Antipodal symmetry of the **weighted atomic measure**, with coincident atoms aggregated, cancels its odd integral. Unweighted normal symmetry or vector balance alone is not the hypothesis.

The resulting equality analysis is complete. If L=2 under this criterion, then L=A/2 and A≥4 force A=4. Choose a unit direction vertex p and the half-arclength point q on the direction polygon. Its enclosing radius-one ball has center c=(p+q)/2. The strictly positive original-edge weights satisfy

    sum_i (l_i/L)|u_i-c|²=1+|c|².

Since every summand has distance at most one, c=0; hence q=-p. For every unit direction vertex v, the two half-arcs imply |v-p|+|v+p|≤2. The reverse inequality is always two, and equality forces v onto the segment [-p,p]. Since |v|=1, v is p or -p. Nonzero reflection differences then make each consecutive change have length two. Total A=4 permits exactly two such changes, so there are precisely two billiard edges. A repeated traversal would have larger A and larger length.

Consequently a genuinely higher-period realizable orbit with this weighted antipodal symmetry has L>2. There is no equality loophole from corners, repeated directions, a non-vertex choice of q, or a degenerate direction polygon.

### The failed-shortcut example

The proposed support function has h+h''=1/2+(1/4)cos(3theta), bounded between 1/4 and 3/4. It therefore defines a smooth strictly convex constant-width curve. The three stated contacts have h'=0, and direct reflection computation gives the claimed normals and weights. Their balance holds while the odd weighted support sum is -3sqrt(3)/32, not zero. Their orbit length 45sqrt(3)/32 is strictly greater than two.

This is a valid counterexample to the shortcut, not to the original conjecture. The independent checker confirms all six contact/antipode points have pairwise squared distances in {1, 259/1024, 675/1024, 867/1024}.

## Independent feasible control checks

The independent reconstruction confirms positive edge lengths, nonzero turns, the reflection law, diameter one of the enlarged point set, and the supporting-ball inequalities in all four existing examples.

- Diameter: L=2, A=4, sigma=1/2. Squared distances are 0 or 1. This checks the actual two-bounce equality case.
- Square: L=2sqrt(2), A=4sqrt(2), sigma=1/4. Squared distances are 0, 1/2, or 1.
- Spatial four-orbit with a=3/10 and b=1/10: L=4sqrt(10)/5, A=4sqrt(55)/5, sigma=1/4. The expected first normal is (3,2,3)/sqrt(22). The oriented six-volume of its tetrahedron is -18/125, so it is genuinely nonplanar. Every pairwise inequality is established exactly; the explicit radical values are saved in the audit JSON.
- Smooth support triangle: L=45sqrt(3)/32, A=3sqrt(3), sigma=1/3, with the distance values given above.

For the existing infeasible symmetric length-two control, the offending adjacent YY squared distance minus one is exactly 31/12-sqrt(3)>0. Thus this negative control fails decisively, independently of numerical tolerance.

## Suggested precise clarifications before reissue

These are nonblocking wording improvements. They are not additional proof attempts and were not applied to the frozen packet.

1. **Attempt 4, dimension specialization:** replace “In ambient dimension n, using m≤n+1” with “For a shortest orbit in ambient dimension n, the credited theorem gives m≤n+1.” This makes the immediate use of that theorem explicit. The moment inequality itself applies to all feasible orbits.
2. **Definitions, primitive period:** explicitly say that a repeated traversal of a complete orbit is not a new primitive higher-period orbit, and that self-intersections are allowed. Avoid suggesting arbitrary repeated vertices may be deleted while preserving the reflection law.
3. **Attempt 2, completion citation:** add the precise Akin locators Theorem 1.3(e), Theorem 0.2(a), and Corollary 3.13. The source is already sufficient; the improvement makes its hypotheses easier to audit.
4. **Review status on a future authorized reissue:** distinguish “independent AI adversarial audit passed for the partial claims” from “original conjecture solved” and “human peer reviewed.” The current frozen packet correctly records review as pending at its creation time; it should not be silently altered under the existing manifest.

## Final disposition

The finite completion equivalence, planar exclusion, symmetric-family exclusion, weighted moment bound, weighted antipodal-normal criterion, and failed-shortcut example all pass this audit within their stated hypotheses. The equality-case handling needed for the strict conclusions is sound. Nonsmooth bodies have not been excluded by accident.

The remaining low-turn nonplanar configurations with non-antipodally-symmetric weighted normal measure remain untreated. There is no certified counterexample and no proof of the original all-dimensional every-shortest-orbit conjecture. Keep the mathematical status **unsolved, 5/5**.
