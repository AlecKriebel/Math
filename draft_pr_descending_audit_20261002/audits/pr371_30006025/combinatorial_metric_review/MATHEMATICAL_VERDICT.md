# Independent mathematical verdict: combinatorial maps and metric constructions

Scope: frozen PR 371 head `51fddd150e8da33f4cf17b1a642a0ffd3466bf5d`, `problems/30006025_geometric_chapuy`, all five TURN manuscripts. This verdict was formed from the primary sources and full mathematical arguments before reading verifier code, numerical/check JSON, author states, final-result files, prior reviews, or parent/sibling verdicts. Exact source receipts and the prior source-first seal accompany it.

## Verdict and exact gap

The combinatorial and metric claims survive this independent adversarial audit under their stated hypotheses. The original OWR Question 4 remains unanswered by the packet: no controlled tree-based construction with the desired random-surface law is supplied, and the narrow obstructions do not exclude all geometric adaptations. Thus the packet's unsolved disposition is justified by checking its contents; it is not an assumed label or a conclusion from green replays. I found no blocking mathematical defect in this family. No historical novelty of the scoped deductions has been established.

The strongest useful deduction is the angle-independent constraint on a direct one-face embedding in a smooth closed curvature -1 surface:

    P >= 4 pi sqrt(g(g-1)).

For P=12g it excludes g>=12, and demands asymptotic relative total length change at least pi/3-1. Under the specified Dirichlet law, this prevents every adaptive repair of o(g) edges with bounded multiplicative stretch from succeeding with nonvanishing probability. This remains an obstruction to a particular kind of correspondence. A metric-graph comparison need not control the total arclength of an embedded cut graph, and the original question does not require that control.

## 1. Independent combinatorial reconstruction

For a cubic one-face orientable map, 3V=2E and V-E+1=2-2g give V=4g-2, E=6g-3 and N=2E=12g-6. Loops and repeated edges are counted by darts, so these equations do not silently require a simple graph. A connected n-edge tree has n+1 vertices. Identifying each cycle of an odd permutation produces an abstract graph with n edges and n+1-2g vertices, hence graph Betti number 2g. This count alone gives neither a rotation system nor an embedding genus.

A concrete counterexample to naive concatenation is the two-edge tree with darts a,b at its central vertex and x,y at its leaves; alpha=(a x)(b y). After identifying all three vertices, use sigma_A=(a b x y) or sigma_B=(a b y x). Both give the same bouquet of two labelled loops. With face convention sigma alpha, the first has the single cycle (a y x b), hence genus 1; the second has cycles (a)(y)(b x), hence three faces and genus 0. Therefore an arbitrary cyclic splice is not the inverse of CFF. The candidate expressly uses a fixed established CFF correspondence and avoids this false shortcut.

For signed CFF trees, the bijection is between 2^(n+1) copies of rooted maps and decorated trees, with a specified underlying graph correspondence. Restricting both sides to cubic graphs preserves the constant copy count. Uniform finite sampling therefore projects to uniform rooted cubic maps. Each cycle has a sign and the cycle count is n+1-2g; forgetting those signs yields the usual 2^(2g) multiplicity. For cubic quotients, every merged degree is three: each nontrivial cycle must consist of three tree leaves, and each singleton must be a tree vertex of degree three. Thus no cycles of length five or longer can survive the cubic restriction, and the tree's degrees are one or three.

The signed CFF existence theorem uses a perfect matching and is not claimed by the packet as a naive efficient deterministic sampler. Given its graph correspondence, edge lengths can be transported by a graph isomorphism; their exchangeable Dirichlet law is unaffected by an edge relabelling. The corresponding graph metric is still distinct from the surface path metric. Rooting is also material: uniform rooted maps push to unrooted combinatorial maps with weights proportional to 1/|Aut|, since n is fixed and the number of root corners is 2n/|Aut|. One cannot silently call this uniform on unmarked isometry classes.

These mechanisms agree with [CFF Sections 2.1-2.5](https://arxiv.org/pdf/1202.3252). The exact original Chapuy construction in [PTRF 2010 Sections 3-5](https://arxiv.org/pdf/0804.0546) has a fixed-genus dominant-map hypothesis, while the later trisection refinement is a different paper. The candidate's use of CFF for all cubic maps is legitimate and does not extrapolate the original dominant-map asymptotic uniformly in g.

## 2. Regular polygon and triangle covering: all sizes

At g>=2, N>=18, so a regular curvature -1 N-gon with interior angles 2pi/3 exists. Its orthoscheme has angles pi/2, pi/3, pi/N. The hyperbolic right-triangle cosine law gives cosh(ell_N/2)=2 cos(pi/N)/sqrt(3). The area is (N-2)pi-(2pi/3)N=4pi(g-1).

For every cubic one-face orientation-compatible side pairing, equal lengths permit the unique endpoint-compatible side isometry. Local edge interiors are smooth, and every vertex link consists of exactly three sectors totalling 2pi. The resulting topological quotient is an orientable closed genus-g surface by Euler characteristic. This is an actual smooth hyperbolic surface, not merely a quotient graph. Markings retain the graph and its cyclic order, allowing recovery of the input; forgetting markings may collapse inputs.

In the triangle-group action on N darts, the edge involution has all cycles of length two, the vertex permutation all cycles of length three, and their product has one N-cycle. Transitivity follows from the one-face condition. These give a degree-N cover of the oriented orbifold (2,3,N). Any nontrivial power of a conjugate of a torsion generator acts without fixed darts, so the dart stabilizer subgroup has no torsion. This matches [the uniform-dessin construction and Lemma 1](https://arxiv.org/pdf/2306.09543). The N polygon-center sectors and paired midpoint sectors also close with full angle 2pi. The orbifold area is pi/3-2pi/N, so its product with N is again 4pi(g-1).

Philippe's orientation-preserving group is exactly the one used here, and its [Corollary 5.2, printed 2686](https://aif.centre-mersenne.org/item/10.5802/aif.2424.pdf) gives minimum hyperbolic translation length 2 arcosh(2 cos^2(pi/N)-1/2). Passing to a subgroup can only increase this minimum. For N>=18, its arcosh argument is larger than (1+sqrt(3))/2, which is larger than 4/3; cosh(1/2)<=53/47<4/3, since the Taylor tail after 1/8 has successive ratio <=1/48. Thus every produced surface has systole >1. This depends on an established classification theorem, not on bounded word enumeration. No claim that the subgroup attains the parent minimum is needed.

For the count on [1/2,1], all these outputs give zero. Under normalized WP law, [Mirzakhani-Petri Theorem 4.1](https://webusers.imj-prg.fr/~bram.petri/RandSurf.pdf) gives a Poisson limit of mean mu=int_(1/2)^1 (cosh(t)-1)/t dt. The probability of zero therefore tends to exp(-mu), and total variation from the deterministic-zero count law tends to 1-exp(-mu). Since cosh(t)-1>t^2/2, mu>3/16; exp(3/16)>1+3/16 gives 1-exp(-mu)>3/19. This persistent statistic rules out that model's WP short-curve law for every input weighting. Finite support at each genus would not by itself prove such an asymptotic failure.

## 3. Intrinsic cut disk and deformation: all embeddings in the declared class

For an embedded finite one-face graph, combinatorial cutting duplicates each edge side and separates its incident vertex sectors. Its complement is a disk by the cellular one-face assumption. The resulting compact cut surface remains a manifold with boundary even when a face word repeats a vertex or edge: those occurrences are distinct boundary occurrences unless they are the endpoints of the same local sector. A bridge still contributes two boundary sides. A leaf supplies a full 2pi boundary sector; it is permitted rather than silently treated as convex. Finitely many bends can be subdivided, with no change to total length.

The cut disk has area 4pi(g-1), perimeter 2 sum ell'_e, curvature -1 everywhere in its interior, and positive sector angles at all boundary points. It has no interior cone point. [Izmestiev Theorem 1](https://arxiv.org/pdf/1409.7681) applies to these intrinsic disks; its boundary-sector definition has no upper bound, and its interior negative-cone-curvature condition is vacuous here. Injectivity of planar development is not needed. These observations address the central possible hidden assumption in Turn 4.

Substituting into P^2>=4pi A+A^2 gives P^2>=16pi^2 g(g-1). At P=12g the necessary condition is pi^2(g-1)<=9g. Its left-minus-right slope is pi^2-9>0. At g=12, (157/50)^2*11>108; at g=11, (22/7)^2*10<99. Therefore the exact integer threshold of this inequality is 12, while genera 2-11 are merely not excluded by it. Smooth closed genus 0 and 1 curvature -1 surfaces do not exist and are explicitly outside the candidate's class.

Let s_g=(pi/3)sqrt(1-1/g). Then sum ell'_e>=6g s_g, so sum(ell'_e-ell_e)>=6g(s_g-1), sum|ell'_e-ell_e|>=6g(s_g-1), and the weighted mean of ell'_e/ell_e is >=s_g. This proves the maximum relative change claim. For cubic maps, averaging absolute changes over E=6g-3 proves the absolute maximum bound. These are necessary lower bounds, not achievable minima. They have asymptotic lower bound pi/3-1. Replacing 12g by any input perimeter asymptotic to 12g leaves the same limiting ratio. For g>=100, (157/150)^2*99/100>(26/25)^2 proves s_g-1>1/25.

## 4. Dirichlet sparse repair: independent all-E proof

[BGL, printed 5 and Section 6](https://doi.org/10.1017/fms.2025.31), confirms that L=2 sum ell_e and X_e=2ell_e/L have the uniform Dirichlet law conditional on the map and L. At L=12g this is ell_e/(6g). Lower-dimensional noncubic cells have zero volume. The one-face length simplex is not a surface-area normalization. The independently fetched Cambridge PDF contains a dynamic download footer, explaining its byte hash difference from the earlier bound PDF; mathematical statements were checked directly and visually.

Independently set Y_i~Exp(1), S=sum Y_i. The change of variables Y_i=S X_i has Jacobian S^(E-1), so S and X are independent and E[S]=E. Successive increasing order-statistic spacings have rates E,E-1,...,1 by memorylessness. The expected j-th largest Y is H_E-H_(j-1); summing j=1,...,k gives k(1+H_E-H_k). Since ordering is invariant under the positive scaling by S, the sum of the k largest Y equals S times T_(E,k). Independence yields E[T]=(k/E)(1+H_E-H_k), including E=1 and k=E; k=0 is deterministic zero.

For every input vector and every adaptive set I of at most k edges, the stretch cap gives total normalized increase <=(C-1)sum_(I)X_i<=(C-1)T. No independence of I is needed. The perimeter obstruction puts success inside {(C-1)T>=delta_g}. Markov therefore gives the claimed cap for measurable rules, and also an outer-probability cap for the possible-success set. C=1 or k=0 gives zero success when g>=12. For k/E->0, (k/E)(1+log(E/k))->0, so bounded C forces probability zero asymptotically, uniformly in the rule. If almost-sure success is required with random unbounded C, pointwise C>=1+delta_g/T followed by Jensen gives the stated expected-stretch bound. Infinite expectations are harmless. No independence between C and X is used.

## 5. Holonomy claims checked at the universal mechanism level

The framed polygon product must be identity in PSL2, hence trace +/-2 in SL2. Trace +/-2 alone is not sufficient; the candidate uses only necessity. At positive algebraic equiangular perimeter, the barycenter product is (T(P/N)R)^N. Cayley-Hamilton gives the nonzero monic trace polynomial, and Hermite-Lindemann makes its trace argument transcendental. Thus the analytic necessary condition is genuinely nonzero on the length simplex; its zero set has measure zero. Finite pairings/orderings and absolutely continuous conditional length laws preserve the conclusion.

With arbitrary fixed algebraic-cosine angles in (0,2pi), all rotation entries are algebraic and the diagonal cosines are positive. In the cyclic binary expansion, strict positivity of every side makes the maximal exponent unique, with coefficient product c_j>0. Grouping repeated exponents cannot cancel that term. Moving a constant trace +/-2 to exponent zero yields a forbidden relation between exponentials of distinct algebraic numbers. [Delaygue's introductory Theorems A/C](https://arxiv.org/pdf/2210.12046v2) state exactly these classical inputs; no new E-function theorem is invoked. At the barycenter this also gives a nonzero Laurent polynomial. Algebraic cosine profiles form a countable set with at most two angles per value on (0,2pi), so a countable union is still null. This does not exclude unrestricted real angle choices. Strictly positive finite sides and the excluded zero/full/ideal angles are essential boundaries, explicitly stated.

## Adversarial challenge ledger

| Challenge | Mechanism tested | Status and residual gap |
|---|---|---|
| Does vertex identification itself give a genus-g embedding? | Two-dart-loop rotation counterexample above | False in general; candidate avoids it by invoking fixed CFF. No new inverse supplied. |
| Can cubic restriction change the copy weight? | Graph-preserving property and constant n | No; copy factor remains constant. Unmarked output weighting is not uniform. |
| Do loops/bridges/repeated vertices invalidate the cut disk or P=2 sum lengths? | Separate occurrences and local sectors | No within stated finite cellular embedded class. Noncellular/multiple-face cases remain outside. |
| Are concave sectors or noninjective development forbidden by the isoperimetric input? | Primary theorem and boundary definitions | No; allowed. Curvature/area/topology changes remain outside. |
| Can a subgroup contain geodesics shorter than the orbifold's minimum? | Translation-length inclusion | No. Equality with parent minimum is not asserted. |
| Can arbitrary input reweighting repair the short-geodesic gap? | Every output has sys>1 | No for the fixed regular-polygon construction. Deformations remain possible. |
| Can adaptive sparse choices defeat the expectation bound? | Pointwise top-k domination | No; independence of repair sites is unnecessary. Large unbounded stretch remains possible. |
| Do finite controls prove solve status or novelty? | Universal mechanisms and exact original target | No. Neither solve nor historical novelty follows from any finite replay. |

Conclusion sealed before replay: scoped necessary results accepted conditional on explicitly credited established theorems; the original construction/law gap remains.
