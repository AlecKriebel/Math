# Independent correctness, original-scope, and priority audit: PR1371 / 30002723

Pinned head: `186e1e62c002e27b7c67bd6b2381945f496d4cf9`; 45 actual bound paths. Audit date: 22 October 2026. This is a machine-assisted independent mathematical audit, not human peer review or formal verification. The earlier sealed audits were not reopened or edited.

## Verdict and strongest verified result

I found no fatal gap in the final theorem in ATTEMPT_5, using the complete local reduction in ATTEMPT_3 and signed-orbit argument in ATTEMPT_4. The verified claim is a deterministic polynomial **total binary input length** decision procedure for extremality of a one-row, periodic, minimal valid piecewise-linear function specified by sparse all-rational breakpoint, actual point-value, and left/right-limit data, with rational parameter f. Both-sided discontinuities at zero are allowed. Extremality is against all valid functions in the standard Gomory–Johnson definition, with no regularity or common-grid restriction on competitors.

This is a theoretical decision theorem using established BHK and AHT algorithms. A practical compressed solver and a polynomial-size explicitly tabulated perturbation are not required by this claim. Strong polynomiality, irrational representations, and higher dimensions remain outside its stated scope. The implementation fixtures supplied in the PR were not executed and are not the proof of its complexity.

The main potentially missing justification can be filled without a new hypothesis: the complete finite-grid equations first imply additivity at **all real points** of a zero coarse face, by affine interpolation on every refined relative face, including refined edges and singletons. Only then is the bounded interval lemma applied. Merely invoking that lemma from finitely many sampled values would be invalid. The detailed argument below supplies this bridge.

No authenticated earlier publication establishing the entire polynomial-bit theorem was found in the bounded current search. That does not establish novelty or priority. BHK and AHT are genuine dependencies, not publications of the new combined reduction. I do not propose an `already_solved` row or a full-answer DOI on the evidence obtained.

## Original problem and exact interpretation

The primary EMS report is Köppe's contribution “The Gomory–Johnson infinite group problem: A 42-year update,” printed pp.2898–2901 of OWR 2014/51. Printed p.2899 was read in text and visually from the fresh PDF. Within the single-row discussion it describes the first extremality algorithms as pseudo-polynomial and asks whether this is optimal. The adjacent continuous oversampling theorem is another bullet; its continuity assumption does not silently restrict the preceding complexity question. [Primary report](https://ems.press/content/serial-article-files/46541). EMS dates the report's publication to 29 October 2015 and its volume to 2014. [Publisher record](https://ems.press/journals/owr/articles/13353).

OWR does not itself formalize a bit encoding. The cited one-dimensional paper's introductory complexity paragraph explicitly turns to all-rational input and asks for a polynomial, or strongly polynomial, algorithm. Thus the sparse rational-list convention is a precise and legitimate formulation of the original efficient-algorithm question, rather than a verbatim encoding specification in OWR. The final theorem resolves its ordinary polynomial bit-time alternative, without resolving the stronger alternative. “Valid function” retains the original standard nonnegative-function convention; it does not mean an arbitrary signed Hamel-type valid inequality outside that convention. [BHK v2](https://arxiv.org/pdf/1206.2079v2).

The current duplicate check preceded substantive mathematics: 22 October 2026, 13:18:33 UTC, read-only GWS CLI, A:AQ, 191 rows, response SHA-256 `446ba179ebbb49bee9cf4cf5619a09b1ea2e41fdb5c8ce2431ec44b5e8d86371`. Both native hits were read completely: row78 is an unrelated extremal exchangeable-sequence question; row159 is an unrelated Johnson-filtration question. Their bodies and the exact check receipt are in GWS_DUPLICATE_CHECK.json. No service mutation occurred.

## The imported finite system actually has the necessary scope

In the actual BHK v2 PDF, §3.1 defines system (10) in the interval slopes/intercepts **and independent singleton values**, with normalization at 0,1,f and every zero-slack vertex for every incident affine trace. Theorem4.11 explicitly includes possibly discontinuous minimal valid functions and the complete 4q system. Its proof invokes Theorem3.2 and Corollary4.10 to obtain extremality against unrestricted valid competitors. It imposes no one-sided continuity at zero. This is not the continuous finite-group point-value restriction theorem. I read the relevant definitions, system, Theorem3.2 proof, Theorem4.11 proof and assembly, and the interval-lemma patching argument in Lemma4.1. [BHK primary](https://arxiv.org/pdf/1206.2079v2).

Let q be a common denominator of the breakpoints and f and let N=4q. Adding f to the presentation is harmless; minimality already places f among possible breakpoints. A refinement of the given list still qualifies as a breakpoint set for the same function. The BHK system can therefore be considered in the normalized vector space H_N of arbitrary periodic N-grid PL functions h with h(0)=0, after subtracting the input function.

## Independent derivation of the local compression

Write t_k=k/N, with all indices periodic. Let s_i be the slope on (t_i,t_(i+1)), J_k=h(t_k+)-h(t_k-), and P_k=h(t_k)-(h(t_k+)+h(t_k-))/2. Then

    h(0-) = -J_0/2-P_0,       h(0+) = J_0/2-P_0,
    h(t_k-) = h(0+) + N^-1 sum_(i<k) s_i + sum_(1<=j<k) J_j,
    h(t_k) = h(t_k-) + J_k/2 + P_k,
    h(t_k+) = h(t_k-) + J_k.

The sole periodic compatibility equation is N^-1 sum s_i + sum J_k=0. Conversely these formulas construct a unique member of H_N from compatible data. Thus the three independent local families acquire only this one global equation before the other residual constraints. No zero-jump or zero-spike assumption has been inserted at zero.

Form the arrangement of x=b, y=b, x+y=b and their needed periodic translates. Retain genuine relative strata, with simultaneous realizability of the required interval/singleton traces. A formal closed triple intersection with a false trace assignment is not such a stratum. All vertices and projection endpoints lie on the q grid: intersections use x, y, x+y lines, whose relevant determinants are ±1. A quadratic-size arrangement, or even a naive polynomial enumeration of triples, suffices.

For each incident coarse relative face F, its input affine slack is nonnegative on its closure. Its zero locus is empty, a supporting vertex, a supporting edge, or the whole closure. Incidences matter: two faces may assign different traces at the same geometric point. The following equivalences operate inside the finite-dimensional space H_N.

### Whole zero two-face

Every refined relative face whose relative interior lies in the open F has zero input affine slack on all its vertices. The complete tight system makes its h-slack zero there. That slack is affine on the refined face, so it vanishes on the whole relative face. These refined open triangles, edges and points partition F. Consequently h(x)+h(y)=h(x+y) holds at all real points of F, not just at its finite vertices.

The periodic finite PL h is bounded. On any small rectangle inside F, the bounded interval lemma gives affine behavior with a common slope on its three projections. A chain of overlapping rectangles along a line segment inside the convex F patches the slopes and affine expressions. Each interior projected point belongs to one such rectangle. This proves the common affine expression on each entire open projection, including artificial grid points. Equivalently all its cell slopes agree and all interior J and P vanish; slopes also agree across the three projections.

Conversely those equalities make the h-slack constant on the whole open F. An inward endpoint sector relation sets the constant to zero. Other endpoint sector relations preserve the distinct boundary traces. This proves both directions rather than assuming finite sampling forces interval regularity.

### Actual zero one-face

For a translation edge the relation has form h(u+t)-h(u)-h(t)=0. Equal paired slopes make it constant on successive elementary open segments. Its jump at an interior grid point is J_(u+t)-J_u and its actual-point deviation from the mean of the two limits is P_(u+t)-P_u. Pairing both J and P therefore glues the same constant across every interior point; an endpoint sector sets it to zero.

For a diagonal edge h(u)+h(t-u)-h(t)=0, differentiation gives equal slopes. Crossing u upward crosses t-u downward, so the jump is J_u-J_(t-u), again requiring equal jumps. The actual-point deviation is P_u+P_(t-u), requiring opposite spikes. The reflected **cell** index is Nt-i-1, whereas the reflected **point** index is Nt-k. These signs and different index formulas are necessary, not conventions that can be interchanged. Endpoints remain residual equations.

### Zero limiting boundary edge of a two-face

This has stronger regularity than an actual one-face relation. For a vertical edge x=t approached with x>t, at an interior artificial grid point y=u and z=t+u set A=h(t+). The three inward sign patterns give

    A+Y^- -Z^- = 0,   A+Y^+ -Z^+ = 0,   A+Y^- -Z^+ = 0.

Subtracting forces J_u=J_z=0. The ray with y=u exactly and the ray with x+y=z exactly remain inside the coarse open face and give

    A+Y^0-Z^+ = 0,    A+Y^- -Z^0 = 0.

Thus P_u=P_z=0 too. They are genuine finite-system constraints: suitable refined incident faces supply the stated limits. Interchanging x,y proves the horizontal case; reversing the inward normal proves the other side. For a diagonal boundary, (++),(+-),(-+) from above, or their opposites from below, force both jumps to vanish; the x-fixed and y-fixed rays force both spikes to vanish. Paired slopes then make the limiting edge expression constant, and endpoint sectors fix that constant. This includes no assertion about arbitrary non-PL competitors' regularity.

### Endpoint and isolated zero constraints

The three lines dx=0, dy=0, dx+dy=0 give six open cones, six rays and the origin. The 13 directions in ATTEMPT_3 represent exactly these sign types. At each coarse face/zero-vertex incidence, keep only directions entering its relative interior for all sufficiently small positive epsilon. The exact point direction is used for a singleton face. The sign of each directional coordinate chooses its actual value or left/right limit.

All refined active equations are now exhausted. Their base point is in a zero two-face, in the interior of an actual zero coarse edge or incident limiting zero edge, or at a coarse vertex. Nonnegative affine slack cannot have any other zero stratum. The preceding local conditions yield every refined zero-trace relation, and the complete refined system yields all local conditions. Boundary data near x=0 from the left occur at x=1 in the chosen periodic square; they are not dropped. The same observation applies to y and x+y. Thus two-sided origin discontinuities are fully retained.

Each local equality or forced-zero set has a sparse interval-pairing description. To merge all slopes in a projected integer interval [a,b), connect [a,b-2] to [a+1,b-1]; then link three representatives by singleton pairings. Empty and singleton ranges are handled directly. Translation and reflected ranges, including strict interior jump/spike ranges, use a constant number of pieces after modulo-one wrapping. The number and encoded size of these descriptions are polynomial.

## Independent signed-orbit and weighted-output proof

For any one family z_i, let the signed equations be z_(g(i))=sigma z_i, where g is an integer interval isometry and sigma is independent of its geometric orientation. Forget signs to get c underlying components. Lift to two consecutive sheets, with (i,e) connected to (g(i),sigma e), and add sheet flips on forced-zero ranges. These are again integer interval pairings. A balanced unforced component splits into two lifted components and carries one scalar; a negative-cycle or forced component has one lifted component and carries zero. Hence its dimension is exactly d=c_lift-c, a nonnegative integer. Apply this independently to s,J,P and sum the dimensions.

Let K count all residual sector equations, periodic compatibility and f-normalization; it is polynomial. If D>K, rank-nullity on these real vector spaces guarantees a nonzero compatible h. Injectivity of the above trace reconstruction ensures it is a nonzero function. The complete-system equivalence and BHK then prove non-extremality. No explicit list of exponentially many components is used.

If D<=K, maintain a SEARCH graph with original forced flips and singleton flips at already selected representatives. Adding flips on [0,t] kills exactly those remaining free components intersecting the prefix. The dimension drop is monotone in t. At the first t giving a drop, only vertex t was added, so the drop is exactly one. Binary search finds a new free component representative. Repeat at most D times, with O(K log N) orbit-count calls; the graph has only polynomially many extra pairings. The reconstruction graph must revert to the original forced flips. Leaving SEARCH flips in that graph would indeed destroy the desired basis, and is explicitly excluded in the final proof.

For reconstruction, put one nonnegative unit marker at (r,+) for each selected component and separate nonnegative indicator coordinates on each sheet for every queried prefix or singleton. These weights have a polynomial interval partition and polynomial vector dimension. A marker's total weight is one across the whole graph. Therefore any output group carrying that marker has multiplicity one, and uniquely identifies the desired lifted component. Its plus-sheet count minus its minus-sheet count is exactly the signed basis coefficient for a prefix; singletons give the individual coefficient. Arbitrarily many unmarked forced-zero components can remain grouped and need not be enumerated.

The actual AHT §4 permits arbitrary finite increasing/decreasing interval pairings. Theorem12 gives binary-size orbit counting. In §6 the output list explicitly represents equal-weight orbit groups by intervals and multiplicities; Theorem16 and its proof give polynomial dependence on the encoded pairings, constant-weight pieces, vector dimension and binary weight/grid bounds. Thus its output is not an exponentially expanded list despite the theorem's informal single-point-per-orbit wording. Separate nonnegative sheet weights suffice; no signed-weight extension is being imported. [AHT primary](https://arxiv.org/pdf/math/0205057v2).

## Total bit-complexity, including arithmetic height

Let L be total sparse input bit length and k the list length. The lcm calculation has log q<=sum of denominator bit lengths=O(L); no q-long grid is built. Breakpoint differences, slopes, input slack tests, coarse-face vertices and feasibility signs all have polynomial rational height. Polynomially many bounded-dimensional rational operations suffice for the geometry.

All original and lifted pairing endpoints have O(log N) bits. The three orbit counts fit O(log N) bits. Representative search uses polynomially many AHT calls on polynomial descriptions. There are polynomially many reconstruction queries: all projected coarse zero vertices, f, zero, full sums and the neighboring prefix/singleton information required by the displayed formulas. Nonnegative weights are piecewise constant with polynomially many breakpoints. A safe bound on physical total indicator weight is 2N times the polynomial coordinate dimension, so its logarithm is polynomial; this also bounds the smaller list-weight convention in AHT.

For a normalized signed component basis, individual entries are 0,1,-1, and signed prefix sums have absolute value at most N. Every residual matrix coefficient is a constant-size combination of these counts, divided by N or 2 where appropriate. Denominators divide 2N and numerator bit length is O(log N). Clearing 2N gives entries bounded by O(N^2), still O(log N) bits. The K-by-D matrix has polynomial size. Fraction-free exact rank, or standard polynomial-bit rational elimination, has polynomial cost: Hadamard bounds on its minors give bit length O(D(log D+log N)). No uncontrolled rational-height growth or numerical rank oracle is needed.

This supplies the asymptotic argument independently of the small dense validators. A dense explicitly tabulated perturbation could have exponential length; the requested YES/NO output does not.

## Falsifiable controls and limits

`exact_independent_controls.py` is wholly audit-authored, uses exact integers/Fractions and explicit exceptions, and imports no author modules. `EXACT_CONTROLS.json` records:

- 277 local dense/sparse **and joint** row-space comparisons: 36 zero-dimensional, 136 one-dimensional, 105 two-dimensional face/support cases, with wrapped, reflected, limiting and isolated relations.
- Four complete 4q systems: continuous GMI (nullity0), two-sided point-spike input (nullity10), a two-sided input with nonzero interval slopes (nullity10), and the known same-original-grid shortcut counterexample at N=20 (nullity3). These use independent interval endpoint/point-value coordinates, not the manuscript's reconstruction coordinates.
- 384 finite signed interval-pairing systems, comparing lift dimensions with exact linear-algebra nullity, prefix selection and signed prefix reconstruction. They include 217 cases with forced points, 304 with a joined-sheet component, 122 dimension-cutoff examples, and negative signed prefix sums.
- Three incorrect local variants are detected: omitting rays, reversing reflected jumps, and confusing reflected cell and point offsets.

Normal, -O and -OO runs give byte-identical output SHA-256 `03129406add249b0c8ec97f5574d0125661e3e562c6e8aeb102033c0f6ad755e`. These are finite guards, not an AHT implementation, an exhaustive theorem check, a complexity experiment, or formal verification. They supplement the analytic equivalences above.

## Priority and remaining gap

The current search covered exact ID/source-key/title aliases, sparse and binary-size complexity, grid-free algorithms, Parts V–VIII, inverse semigroups, AHT/signed-orbit combinations, the author research index and 2025–2026 leads. Search absence is not a proof of absence. Exact search details and negative-lead qualifications are in PRIORITY_SEARCH_LOG.md.

The actual Part V body describes empirical denominator independence, not a worst-case polynomial-bit bound. Published Part VII Theorem72 proves finite presentation by a finiteness argument, defers the detailed completion algorithm to Part VIII, and imposes one-sided continuity in its perturbation-space decomposition. Its §12.2 explicitly explains failure of that decomposition for two-sided origin discontinuities. The 2025 Part IV main theorem concerns continuous two-dimensional functions on a specified triangulation and its concluding algorithmic observation is polynomial in numerical q. None is authenticated coverage of this final full target. The old weak-NP-hardness statement is a conjecture and supplies no contradiction to the proposed theorem.

The remaining material uncertainty is **priority**, particularly a public or unpublished Part VIII or another full polynomial-bit theorem not recovered by this bounded search. No earlier full-target DOI or deposit was authenticated. Consequently the correct disposition is: full rational-input mathematical decision theorem survives this audit; novelty and historical priority unestablished. This audit creates no row, publication, author contact, or authority to promote the finding.
