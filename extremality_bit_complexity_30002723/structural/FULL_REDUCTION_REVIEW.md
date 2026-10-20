# Independent review of the full discontinuous orbit-compression reduction

20 October 2026. Review of the candidate polynomial-bit-time algorithm, using the direct 4q finite system rather than a coverage assumption.

## Verdict

**No mathematical gap identified in the specified reduction.** The local signed relations, their sufficiency together with coarse sector equations, the polynomial-time dimension computation, and the output-sensitive basis/integral recovery have each been checked independently. The argument now addresses the full rational sparse-list input model, including two-sided discontinuity at the origin, and retains unrestricted valid-function competitors through the published finite-system equivalence.

This is a review of an authored candidate theorem, not a claim that the theorem is already in the literature or that a weighted AHT implementation has been completed. The full mathematical manuscript must explicitly include the local factorization and the signed-orbit recovery arguments below. Omitting point-fixed directions, treating reflected jumps as signed, or retaining an exponential orbit list would invalidate a shortened proof.

## 1. Exact finite target: no coverage or continuity assumption

Let q clear the denominators of all input breakpoints and f, and set N=4q. Basu–Hildebrand–Köppe, Part I, Theorem 4.11 states that extremality is equivalent to uniqueness in their active-equality system for functions piecewise linear over the N grid, with arbitrary point values at grid points. Their theorem explicitly allows discontinuous input. Thus it is legitimate to analyze this finite system even though actual competitors in the definition of extremality are unrestricted.

No inference that arbitrary competitors are continuous, piecewise linear on the original sparse partition, or even regular at the origin is being made. The known 4q theorem supplies the entire bridge to unrestricted competitors.

The binary length of q is polynomial in the input length, but q itself need not be polynomial. The algorithm therefore must not expand the N grid.

Primary source: https://arxiv.org/html/1206.2079v2 , Theorem 4.11 and the active system (10).

## 2. An exact coordinate system

For an N-grid piecewise-linear perturbation h, use:

- s_i, its slope on (i/N,(i+1)/N);
- J_k=h(k/N+)-h(k/N-), its jump;
- P_k=h(k/N)-(h(k/N+)+h(k/N-))/2, its isolated point displacement;
- a=h(0+).

The cyclic compatibility equation is

sum_i s_i/N + sum_k J_k = 0.

For 1<=k<N, reconstruction is

R_k = a + sum_{i<k}s_i/N + sum_{1<=j<=k}J_j,
L_k = R_k-J_k,
h(k/N)=R_k-J_k/2+P_k.

At zero use R_0=a, L_0=a-J_0 and h(0)=a-J_0/2+P_0. The compatibility equation makes L_0 the actual limit from the final cell. Consequently these 3N+1 variables with one cyclic equation represent exactly the 3N-dimensional space of periodic N-grid functions. There is no gauge freedom: after compatibility, zero function means all these coordinates are zero.

This detail matters for the later dimension-count rejection: the cyclic equation must be counted among the residual equations.

## 3. Exhaustive local factorization

Consider the sparse arrangement of x=b, y=b and x+y=b+k from the original breakpoints. Every coarse face carries a nonnegative affine actual or limiting slack. The following relations are necessary and sufficient, together with the residual equations in Section 4, to encode the fine N-grid active-equality system.

### 3.1 Fully additive coarse 2-faces

The bounded interval lemma makes h affine with the same slope on all three open projection intervals. Therefore:

- all cell slopes in each projection, and across its three projections, are equal;
- J and P vanish at all grid points strictly inside each projection.

Conversely, precisely these conditions make h affine with a common slope on the three open projections, hence make Delta h constant on the coarse face. A corresponding coarse-vertex sector equation sets that constant to zero.

Slope equality over a long interval has a succinct pairing presentation: identify adjacent cell indices by one shift-by-one interval pairing, and join representatives of the three projections with singleton pairings. This does not expand the interval.

### 3.2 Actual additive coarse 1-faces

For a translation edge, cell slopes agree, jumps agree, and point displacements agree under the induced pairing.

For a reflection edge x+y=t, cell slopes agree, jumps agree without a sign change, and point displacements have opposite signs. In symbols,

J(x)=J(t-x),   P(x)=-P(t-x).

The signs were checked directly from the left-limit, right-limit and pointwise additivity equations. In an implementation, the reflected cell index is Nt-i-1, but the reflected point index is Nt-k. The difference of one is essential.

These constraints make Delta h constant throughout the open edge, including at artificial fine-grid points: derivative zero makes it constant on each fine segment; paired J removes changes between left and right constants; paired P makes the actual point value equal the same constant. One endpoint sector equation sets the constant to zero. Thus no independent fine-cell intercept constraints are missing.

### 3.3 Zero limiting edges of coarse 2-faces

These impose equal paired slopes, but stronger singular constraints: J=P=0 separately on both nonfixed open projections.

For an explicit audit, let F lie to the right of x=t, and let (t,u) be an interior grid point of its limiting zero edge, with z=t+u. Write A=h(t+), Y^e=h(u^e), Z^e=h(z^e). Approaches within relint(F) give

A+Y^- -Z^-=0,
A+Y^+ -Z^+=0,
A+Y^- -Z^+=0.

They force both jumps to vanish. The additional paths y=u exactly and x+y=z exactly give

A+Y^0-Z^+=0,
A+Y^- -Z^0=0,

forcing both point displacements to vanish. These paths remain within the coarse 2-face because u and z are interior to their coarse projections, even though they are fine-grid points. Horizontal and diagonal cases are changes of coordinates.

Once these singularities vanish, equal paired slopes make the boundary limit constant; one endpoint sector equation fixes it.

## 4. Residual coarse-vertex equations are complete

Retain periodic compatibility, normalization h(0)=0 and h(f)=0, and every actual or directional coarse-vertex equality whose corresponding slack for pi is zero.

At each vertex, the lines delta x=0, delta y=0 and delta x+delta y=0 give six open cones, six rays, and the exact point. The six open cones need representatives such as (1,1), (2,-1), (1,-2), (-1,-1), (-2,1), (-1,2). Considering only coordinate directions in {-1,0,1} would miss some mixed-sign cones. The rays with delta x=0, delta y=0 or delta(x+y)=0 must be included because they use an actual point value for that coordinate, not a one-sided limit.

There are only polynomially many coarse vertices and constant many sectors per vertex. Periodic extension allows all sectors at a boundary vertex to be considered; alternatively one must explicitly retain the equivalent sectors at its opposite fundamental-domain copies.

To check sufficiency, classify a fine-grid zero equality by the location of its base point:

- Interior of a coarse 2-face: its nonnegative affine slack can vanish only if that entire coarse face is additive. Section 3.1 applies.
- Interior of a coarse 1-face: any vanishing actual or incident limiting affine slack must vanish on the whole edge. Section 3.2 or 3.3 applies, including the boundary of a fully additive face.
- Coarse vertex: the equation is among the retained sector equations.

These cases exhaust all fine-grid active equations and their limits. Conversely, every proposed local relation follows from those fine active equations, by the same interval and limit arguments. Thus the factorization is an equality of kernels, not only a sufficient condition.

## 5. Polynomial counting before any enumeration

The local relations split into three independent systems:

- unsigned interval-pairing equalities for slopes;
- unsigned interval-pairing equalities and forced-zero ranges for jumps;
- signed interval-pairing equalities and forced-zero ranges for point displacements.

Let their dimensions be d_s,d_J,d_P. Before the residual equations, the total dimension is D=1+d_s+d_J+d_P, including the baseline a.

For an unsigned pairing graph, dimension is its orbit count. For signed variables, take two sheets and lift each signed edge; force zero by adding sheet-flip pairings over forced-zero intervals. If c is the underlying orbit count and c_lift the doubled orbit count, the dimension is c_lift-c. Each balanced unforced component contributes 2-1=1; each inconsistent or forced-zero component contributes 1-1=0.

All these counts are computable using ordinary AHT. The answer is a binary integer even if exponentially large. If D exceeds K, the number of residual scalar equations, the residual system cannot have trivial kernel. Therefore the algorithm can immediately return non-extreme without enumerating variables or orbits. This dimension cutoff is necessary now that the proof no longer assumes coverage.

## 6. Recover only polynomially many free components

If D<=K, free-component representatives can be extracted with polynomially many AHT calls, even when there are exponentially many zero components.

For a signed point system, maintain the originally forced-zero graph plus temporary singleton flips for components already found. Binary-search the least t for which forcing the prefix [0,t] to zero reduces the free dimension. At this least t, exactly one new free component is hit. Record t and permanently add a temporary flip at t, then repeat. There are at most K iterations and O(K log N) orbit-count calls.

For later coefficient recovery, remove these temporary enumeration flips and return to the original graph. Mark each representative separately. In the signed lift, mark its + copy (and optionally its - copy). Weighted AHT with sheet-specific prefix indicators and singleton indicators gives every required signed prefix sum and point coefficient by subtracting minus-sheet counts from plus-sheet counts. Nonnegative weights suffice. Tagged free orbits are unique; untagged zero orbits may remain compressed in the algorithm's grouped output and are never expanded.

The ordinary slope system can use the same signed machinery with all signs positive, or a simpler unsigned version.

## 7. Residual rank and bit bounds

All residual evaluations of h at a coarse vertex coordinate use only the reconstruction formula of Section 2, hence slope and jump prefix sums, the local J and P value, and the baseline. The required coordinates form a polynomial-size set because they are projections of coarse vertices.

The resulting residual matrix has at most K columns and polynomially many rows. Its entries are integers or rational numbers with denominator dividing 2N; numerator magnitudes are polynomial multiples of N. Clearing denominators gives an integer matrix with polynomially bounded bit lengths. Exact rational/integer rank is polynomial-time.

All arrangement coordinates, pairing endpoints, counters and orbit weights have polynomial bit length. The number of pairing intervals, forced-zero intervals, marker weights and query breakpoints is polynomial in the sparse input size and K. The AHT and weighted AHT theorem interfaces therefore yield a polynomial bit bound, not merely a polynomial bound in N.

A nonzero kernel vector establishes a finite N-grid perturbation through BHK's active-system theorem. A zero kernel establishes extremality through Theorem 4.11. It is unnecessary to print the potentially exponential conventional N-grid witness.

Primary orbit-counting source: Agol–Hass–Thurston, *The Computational Complexity of Knot Genus and Spanning Area*, arXiv:math/0205057v2, Theorems 12 and 16, with the grouped-output specification in Section 6: https://arxiv.org/html/math/0205057v2 . The signed lift, dimension cutoff, representative extraction and coefficient recovery are authored reductions here.

## 8. Review boundaries and required presentation details

No uncovered-interval test is required in the direct N=4q version. No one-sided continuity condition is required. No competing function has been restricted without a published equivalence theorem.

The independently checked finite tests for the earlier continuous specialization agreed with dense 4q references, but they do not establish the full discontinuous theorem or the AHT complexity. Other independently generated dense-versus-structured checks should be reported separately with their exact inputs and scope.

Before a final theorem is published, the manuscript should retain these specifics:

1. the point-fixed rays and all six open sectors;
2. distinction between actual and limiting zero edges;
3. unsigned reflected jumps versus signed reflected point displacements;
4. cell/point reflection index offset;
5. cyclic compatibility in both reconstruction and the residual dimension count;
6. grouped weighted-AHT output and unique representative markers;
7. removal of temporary enumeration flips before coefficient recovery;
8. the direct 4q equivalence for unrestricted discontinuous competitors.

With these included, this review leaves no unresolved mathematical step in the candidate reduction. Further independent review and implementation are appropriate because the conclusion would resolve the specified binary-complexity question rather than merely improve a numerical-denominator bound.
