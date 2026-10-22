# Fresh independent audit: full rational extremality theorem

Date: 20 October 2026.

## Disposition

**PASS: the theorem in Attempt 5 follows from the imported BHK and AHT theorems and the reductions in Attempts 3–4.** This audit found no mathematical obstruction or missing complexity factor. The result is for the promised all-rational sparse-list input, allows arbitrary discontinuities, and tests extremality against unrestricted valid competitors.

The verdict is a proof audit, not a claim of external peer review, established novelty, an implemented polynomial-time solver, or a resolution of strong polynomiality. The original source gate was a literature finding, not a proof against this new reduction. No queue change or publication is part of this audit.

I reviewed Attempts 3–5 directly before using supporting notes. I independently checked the primary theorem interfaces, rederived the local and signed-graph arguments, and wrote independent finite validators. Prior provisional audit dispositions were not used as premises.

## 1. Primary-source interface checks

### BHK: PASS

Basu–Hildebrand–Köppe, Part I, Theorem 4.11, expressly permits discontinuous rational-breakpoint minimal valid functions. Its uniqueness test is the complete periodic point/interval-affine system (10) on the 1/(4q) grid, not a point-value-only finite-group restriction. Section 3 supplies the normalization and tight limiting-face equations. The proof of Theorem 4.11 connects this finite system with unrestricted extremality. Theorem 3.2 supplies the nonextremality direction from a nonzero kernel. I checked the downloaded primary text and the public primary rendering.

Source: https://arxiv.org/html/1206.2079v2, §§3.1–3.3 and Theorem 4.11.

In particular, no one-sided-continuity hypothesis from later perturbation-decomposition results is being imported here. Adding redundant breakpoints, including f, is legitimate in the piecewise-linear representation. The complete 4q system, rather than same-grid rigidity, is essential.

### AHT: PASS

Agol–Hass–Thurston Theorem 12 handles increasing and decreasing integer interval pairings in polynomial time in the number of pairings and log N. Theorem 16 additionally handles a polynomial-size piecewise-constant vector-weight description. Section 6 defines the output as weighted intervals encoding multiplicities of equal-weight orbits, so exponentially many unmarked orbits need not be listed. Its stated bound is polynomial in k, m, d, log D and log N. The reduction uses only nonnegative input weights. Overlapping domains and ranges, reflections and singleton pairings are within the stated framework.

Source: https://arxiv.org/html/math/0205057v2, §4, Theorem 12, and §6 through Theorem 16. Checked directly on the primary rendering.

The signed lift, free-component extraction and marker interpretation below are new deductions being audited, not assertions that AHT already states the extremality reduction.

## 2. Exact finite target and all thirteen traces: PASS

Let V_N be the space of periodic functions affine on every open N-grid interval, with independent values at all N-grid points. It has dimension 3N before normalization. At a grid vertex (u,v), a fine-face germ is determined by the signs of

    d_x, d_y, d_x+d_y.

The three lines through the origin partition the direction plane into six open cones, six rays and the origin. There are exactly thirteen realizable sign triples. The thirteen representatives in Attempt 3 hit them all. A zero directional coordinate means the actual value, not an arbitrarily selected one-sided limit.

For the uniform grid, every fine face is a point, edge or triangle, and its vertices have both coordinates on the grid. Consequently all equations of the fine system are exactly the active trace equations at these vertices. When a fundamental-square boundary excludes a direction, a periodic translate of that vertex supplies the same equation. Thus using grid indices modulo N and all thirteen states is equivalent to the periodic fine-face system.

This also explains why the six rays cannot be discarded: they detect point spikes. Six open cones alone are not a complete discontinuous test.

## 3. Genuine coarse strata and zero-set classification: PASS

For sparse cells I, J, K, use the relative stratum

    S = { (x,y): x in relint(I), y in relint(J), x+y in relint(K) }.

Retain it only when nonempty, and use F = closure(S). On S the input slack has one specified affine formula, extending to F. Empty simultaneous relative interiors must not be assigned arbitrary interval traces merely because the closed intersection is nonempty.

This qualification is necessary. For example, closed intervals can meet the equation x+y=t only at an endpoint where the proposed open-interval states cannot occur simultaneously. Such a triple does not define an additional limiting slack. BHK's trace convention must likewise be read using the actual relative stratum: its claimed equality with the function on relint(F) would otherwise be false for discontinuous functions.

For a genuine stratum, nonnegativity of the input slack implies that its zero set in F is a face of F: empty, one vertex, an edge, or the whole polygon. For a one-dimensional F it is empty, an endpoint, or all of F. Hence no zero curve or zero line in the interior of a nonzero two-dimensional affine slack has been omitted.

All boundaries lie on vertical, horizontal or slope-minus-one lines. Their vertices, and every projected vertex coordinate, lie on the q grid. This includes differences of sparse breakpoints, not just listed breakpoints. Each required coordinate therefore also lies on the N=4q grid.

## 4. Local factorization: PASS

The argument here is entirely inside V_N. It does not assume regularity of arbitrary competing valid functions.

### 4.1 Entirely zero two-dimensional face

The complete fine equations imply actual additivity throughout the open coarse face, including artificial fine-grid lines: the input is affine there, and every incident fine-face slack is zero. The bounded interval lemma on small rectangles inside the face makes h affine with a common slope on their three projections. Overlapping rectangles propagate this slope over the connected projections of the convex open face.

Equivalently, all slope cells in each projection have one common slope, shared across the three projections; all interior jumps and spikes vanish. Conversely these conditions make h affine on each entire open projection with the same slope. Its slack is then one constant throughout the coarse face. Any retained endpoint sector entering that face sets the constant to zero. Boundary sectors with different original point/limit data are processed separately, not conflated with this constant.

### 4.2 Entirely zero actual one-dimensional face

On a translation edge the expression is h(x)+h(t)-h(x+t). Equality of paired slopes makes its derivative zero within each fine segment. Equality of paired jumps makes the constants on successive segments agree. Equality of paired spikes makes the actual grid-point expression agree with that same constant.

On a reflection edge the expression is h(x)+h(t-x)-h(t). Differentiation gives equality, not negation, of paired slopes. The right-minus-left difference is J(x)-J(t-x), so the jumps also have positive character. The point value minus the average of the two limiting expressions is P(x)+P(t-x), so spikes have negative character.

Thus an endpoint sector determines the one remaining constant. The distinct reflection formulas i -> Nt-i-1 for cells and k -> Nt-k for points are correct. At a fixed reflected point, negative spike character correctly forces that spike to zero; it does not incorrectly force the jump to zero.

### 4.3 Zero limiting boundary edge of a two-dimensional face

This case is not the same as an actual additive edge. At an interior boundary grid point, both nonfixed projections are interior to their original coarse cells, so the input has the same trace in their three states. The perturbation need not initially have that property.

For a vertical edge with the incident face to the right, set A=h(t+), Y^e=h(u^e), Z^e=h((t+u)^e). Three realizable fine sectors impose

    A+Y^-−Z^-=0,  A+Y^+−Z^+=0,  A+Y^-−Z^+=0.

Their differences force both jumps to vanish. The rays keeping y=u and x+y=t+u respectively impose

    A+Y^0−Z^+=0,  A+Y^-−Z^0=0,

forcing both spikes to vanish. These rays remain inside the original open coarse face because their fixed fine coordinates are not original coarse boundaries. This is precisely the distinction needed for discontinuous perturbations at artificial grid points.

The left-side case reverses the relevant signs; exchanging x and y gives horizontal edges. The invertible change to coordinates (x,x+y) gives the diagonal cases. Equality of paired slopes is then necessary and sufficient to make the limiting edge expression constant between endpoints. The endpoint sector equations fix that constant.

There is no additional mixed slope/jump constraint: regularity eliminates point changes, paired slopes eliminate variation along the edge, and an endpoint equation supplies its value.

### 4.4 Exhaustion of all fine equations

Take any active fine-face vertex equation, including its trace sector. A sufficiently short path along that sector lies in a unique genuine coarse relative stratum S; its input trace equals that stratum's affine slack evaluated at the base point. The base point is therefore in its zero face.

If it lies in the relative interior of a two-dimensional zero face, §4.1 applies. In the relative interior of a zero edge, either §4.2 or §4.3 applies, according to the dimension of the incident coarse stratum. Otherwise it is a coarse zero vertex, and the explicitly retained feasible sector equation applies. This includes isolated zeros and all endpoint traces.

Conversely every imposed local relation follows from these active fine equations by the arguments above, and every residual endpoint equation is itself an active fine equation. This proves equality of the two solution spaces, not merely one inclusion or agreement on a finite sample.

## 5. Sparse presentation of local relations: PASS

A projected coarse interval has grid endpoints aN and bN. Equality of its slopes is represented by the adjacent pairing [aN,bN−2] to [aN+1,bN−1], omitting an empty interval. Singleton links join the three projections. Its regularity constraints use the strict-interior point interval [aN+1,bN−1].

Translation and reflection edges induce interval isometries on the relevant cells and strict-interior points. Modulo-one wrap is split at the finitely many wrap locations in both domain and image, giving only a constant number of pieces per relation. Empty and singleton cases cause no blowup.

Thus there are polynomially many interval-pairing descriptions and forced-zero ranges in each of the slope, jump and spike systems. No fine-grid enumeration is needed to produce their endpoints.

## 6. Signed lift, dimension and representatives: PASS

For an underlying connected component, signed propagation either consistently assigns every value to plus or minus one representative scalar, or an inconsistent cycle forces that scalar to zero. An imposed zero also kills exactly its whole component.

In the two-sheet lift, a consistent unforced component splits into two components, one for each sign of the representative. An inconsistent or forced component has one connected lift. Adding flips at zero ranges changes no underlying components. Subtracting the underlying component count from the lifted component count therefore gives exactly the number of free scalars, including isolated vertices and negative self-relations.

To extract representatives, killing a prefix lowers this dimension by the number of still-free underlying components intersecting that prefix. It is a monotone integer function. At the first index where it decreases, only one new vertex has entered, so the drop is exactly one. Binary search identifies a new free component. Permanently killing its representative in a separate search copy prevents reselection.

The search adds at most one singleton per selected component plus one temporary prefix. If the total dimension is at most K, at most K iterations and O(K log N) counting calls are needed. Underlying component counts can be cached. Crucially, reconstruction uses the original graph, not the search graph with its newly killed representatives. The candidate explicitly makes this distinction.

## 7. Weighted coefficient recovery and grouped output: PASS

For each free component, put one distinct marker coordinate at its positive lifted representative. Its containing lift component is the positive normalized basis orbit. A vertex k has basis value +1 if (k,+) lies in that orbit, −1 if (k,−) lies in it, and zero otherwise.

Therefore its basis coefficient in a prefix sum is exactly the positive-sheet prefix count minus the negative-sheet prefix count. Singleton weights give point evaluations. Separate nonnegative indicator coordinates suffice; no signed-weight extension is assumed.

A marker has total mass one in the entire graph. Accordingly any output group whose vector contains that marker must have multiplicity one. Distinct representatives lie in distinct underlying components, so their marker signatures cannot coincide. This identifies all needed orbit weights without asking AHT for original vertex identities or expanding its unmarked output groups.

All marker and query weights change only at explicitly listed endpoints. The number of pieces and vector coordinates is polynomial even when N is exponential. Counts are bounded by N per sheet; every component needed for reconstruction is individually marked. The grouped-output interface is consequently sufficient.

## 8. Reconstruction, normalization and the cutoff: PASS

For k>0, normalized reconstruction is

    h(k/N−)=J_0/2−P_0+(1/N) sum_{i<k} s_i+sum_{1<=j<k} J_j,
    h(k/N)=h(k/N−)+J_k/2+P_k,
    h(k/N+)=h(k/N−)+J_k.

At zero, h(0)=0, h(0−)=−J_0/2−P_0 and h(0+)=J_0/2−P_0. The necessary and sufficient closing condition is

    (1/N) sum_i s_i+sum_k J_k=0.

It makes the reconstructed left limit at 1 agree with h(0−). Thus normalized periodic functions correspond bijectively to compatible parameter vectors. Before imposing compatibility, the raw parameters are not automatically a periodic function with those slopes; the candidate correctly retains compatibility as a residual equation.

All traces at projected coarse vertices can be reconstructed by the finitely many prefix/singleton queries. Coordinates above one are reduced periodically. The residual equations also include h(f)=0. There is no missing h(1)=0 constraint once periodicity and h(0)=0 are enforced.

Let D be the total local free dimension and K the actual number of retained residual rows, including compatibility and f-normalization. If D>K, rank-nullity gives a nonzero compatible parameter vector. Injectivity on the compatible subspace gives a nonzero h. Thus the cutoff certifies nonextremality without listing the free components. It does not require the K rows to be independent.

If D<=K, representative extraction and weighted reconstruction produce the entire K-by-D residual matrix. Its nullity is the nullity of the full normalized fine system. BHK then gives both directions of the claimed extremality decision.

## 9. Bit complexity: PASS

Let L denote the total binary length of the explicit rational input. The number of listed intervals is at most L, and log q is bounded by the sum of denominator bit lengths. Computing q and N=4q is polynomial-time integer arithmetic; their values need not be small.

The sparse arrangement has polynomially many faces and incidences. Even enumeration of all sparse cell triples is polynomial, with only a fixed number of bounding lines per triple. Relative-stratum feasibility, zero-slack tests and direction feasibility are exact rational comparisons of polynomial bit length.

The number of local pairings, residual rows and projected-vertex queries is polynomial in L. Their integer endpoints have O(log N) bits. Dimension queries and the O(K log N) search calls consequently have polynomial encoded input size. Weighted reconstruction has polynomially many weight pieces and coordinates, with 0/1 initial entries and polynomial-bit orbit sums.

The final trace coefficients have denominators dividing 2N. A trace coefficient need not have numerator bounded by N: a jump-prefix count of order N becomes a numerator of order N squared after clearing 2N. Its bit length is still O(log N), exactly what the theorem requires. Sums of the bounded number of traces per row preserve polynomial bit length. Exact rational rank of the polynomial-size matrix is polynomial bit time.

No step scans q or N, lists all orbits, lists every fine value, or outputs a full perturbation table. The decision claim, unlike an explicit-table output claim, is therefore justified.

## 10. Fresh finite checks

These tests supplement the proof; they do not establish the asymptotic bound and are not implementations of AHT.

### Local factorization checker

Files: `fresh_audit/test_local_factorization.py` and `fresh_audit/test_local_factorization.json`.

This checker imports no candidate implementation. It independently enumerates all thirteen sign states and genuine coarse relative strata on three sparse arrangements, then tests every possible zero face of a nonnegative affine slack. For each, it compares exact row spaces of all fine-grid active traces and the proposed local relations plus endpoint sectors.

Result: **739 exact row-space comparisons passed** on N=4, 6 and 8. Categories include 50 full zero polygons, 168 limiting zero edges, 100 actual zero edges, and all isolated-zero and endpoint cases. It discarded 1,296 closed triples with no simultaneous relative-interior realization.

### Compressed-decision simulation

Files: `fresh_audit/test_compressed_decision.py` and `fresh_audit/test_compressed_decision.json`.

This checker uses only the fresh local geometry helper, not the candidate checker. It independently builds the three signed relation systems, constructs their lifts, performs prefix-kill representative searches on separate graph copies, reconstructs normalized traces, and compares residual nullity with the complete dense thirteen-sector matrix. It uses stored rational sample functions only as input data, not as evidence of correctness.

Result: **20 exact nullity comparisons passed**. They include N=4q instances with N=20 and 36, both zero and positive nullities, and a two-sided-discontinuous constant-half family. The N=32 constant-half case has local dimension 50 and K=30, exercises the D>K rejection branch, and has full/structured nullity 46. The N=36 two-sided example with positive nullity has value 2 in both computations.

The local checker can be replayed directly with Python and SymPy. The compressed-decision checker additionally reads the authored rational samples in `checks/discontinuous_reduction_results.json`. Neither fresh checker relies on floating-point arithmetic for its assertions.

## 11. Corrections and limits

No blocking correction to Attempts 3–5 was identified. The following are essential qualifications to preserve in any consolidated manuscript:

1. Treat a coarse face as a genuine relative stratum with its trace data, not every closed triple intersection.
2. Preserve all thirteen trace states, especially rays, and keep actual additive edges distinct from limiting boundary edges.
3. Use the original signed graph for weighted reconstruction after representative search.
4. Include projected arrangement-vertex coordinates, compatibility and f-normalization in the residual reconstruction.
5. State bit bounds for numerators, rather than incorrectly claiming every cleared numerator is at most N.
6. Label the dense validators as finite checks, not a fast AHT implementation.
7. Retain the all-rational sparse representation, one-row scope, minimality promise and unrestricted-competitor definition. Strong polynomiality, arbitrary irrational encodings, higher-dimensional input and literature novelty are not established.

With those already-stated qualifications retained, this audit's final mathematical disposition is **PASS for the full theorem**, not merely the continuous subclass.
