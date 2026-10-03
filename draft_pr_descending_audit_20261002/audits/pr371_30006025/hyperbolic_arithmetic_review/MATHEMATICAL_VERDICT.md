# Independent mathematical verdict before computational review

Sealed UTC: 2026-10-03T10:48:19.583717+00:00. Frozen head 51fddd150e8da33f4cf17b1a642a0ffd3466bf5d. This verdict is based on independent primary-source reading and full TURN_1.md through TURN_5.md proof reading. Candidate verifier code, stored checks, state/result files and all earlier/root/sibling mathematical verdicts remain unread.

**Verdict: the five scoped deductions are mathematically supported as written. The original source Question4 remains unresolved. No historical novelty claim is verified.** The strongest geometric result is the angle-independent necessary perimeter P≥4pi sqrt(g(g−1)), with its direct-realization hypotheses retained. The triangle replacement is a valid classical construction, but its distribution fails a fixed short-geodesic test for every input law. The arithmetic arguments correctly obstruct only exact length-preserving algebraic-angle palettes.

## Reconstruction and active falsification

### T1: analytic null set

At fixed cubic size E=6g−3, N=2E, source P=12g means sum edge lengths=P/2. Every side word contains each edge twice, so its equal edge point assigns side length x=P/N. For a positively oriented geodesic frame, moving by x and turning by exterior beta is right multiplication T(x)R(beta); rotation R(beta) has cosine/sine of beta/2. In PSL2(R), smooth framed closure means identity, and SL2 lifts give ±I; trace²−4=0 is only a necessary condition. It is permissible to include nonclosing parabolics.

At the equal point for beta=pi/3, tr(T(x)R)=sqrt3 cosh(P/(2N)). If cosh(a) were algebraic, exp(a) would solve t²−2cosh(a)t+1=0 over algebraic numbers, contradicting Hermite–Lindemann for nonzero algebraic a. Chebyshev trace recurrence C_N is monic and integral; C_N(z)²−4 cannot vanish at transcendental z. Hence a real-analytic function on the (E−1)-dimensional connected open simplex is not identically zero; its zero set is null. Finite pairings/orderings preserve nullity. Conditional densities suffice, without independent pairing choices. This verifies all g≥2, not an empirical finite-g inference.

Falsifications considered: wrong factor2 in perimeter, trace=±2 being sufficient for closure, unproved simple polygon closure, equal-angle assumption being forced by cubic smoothness, equal-perimeter assumption being silently dropped. All are avoided. P algebraic is essential to this particular witness argument; no theorem for all positive P is obtained here.

### T2: Lindemann–Weierstrass maximum exponent

For 0<alpha_j<2pi, beta_j=pi−alpha_j∈(−pi,pi), hence c_j=cos(beta_j/2)=sin(alpha_j/2)>0. Algebraic cos(alpha_j) makes both c_j and signed s_j algebraic. Expanding tr(product T(l_j)R_j) in cyclic matrix indices produces algebraic coefficients times exp(½ sum epsilon_j l_j). Because every l_j>0, the maximum exponent ½sum l_j is unique (all indices1), with coefficient product c_j>0. Thus subtracting either constant ±2 still leaves a nontrivial relation among exponentials of distinct algebraic numbers after grouping exponents. Classical Theorem C rules it out. This covers straight corners and concave corners, but not zero-length sides, zero/full/ideal corners.

For continuously varying lengths at an algebraic fixed perimeter, at the equal point the trace is a Laurent polynomial in q=exp(P/(2N)), with nonzero highest coefficient. q is transcendental; the trace cannot be ±2. Each fixed angle profile gives a null analytic zero set. Algebraic cosines give countably many finite profiles, so selecting the palette adaptively after observing lengths still cannot avoid the null set. The unrestricted uncountable real palette is not excluded.

The Janson–Louf factor sqrt(12g/n) is algebraic. Suppressing degree2 paths gives integer multiples of it, so the finite-core application is sound. Leaves are removed, and retained degrees≥2 give allowable equal-sharing angles. No contradiction to the conjectural polygon/coupling interpretation is inferred.

Additional arithmetic control, independent of the candidate proof: the standard (2,3,N) group admits algebraic matrices. Set u=cos(pi/N), v=sqrt(u²−3/4), A=[[0,−1],[1,0]], B=[[1/2,u+v],[−u+v,1/2]]. Both determinants are1; tr A=0, tr B=1, tr AB=2u. These are the standard rotation-pair invariants of the triangle group, with v real for N>6. Every group word therefore has algebraic trace. For a hyperbolic word with t=|tr|>2, exp(length/2)=(t+sqrt(t²−4))/2 is algebraic. Any positive algebraic length would contradict Hermite–Lindemann. This supports the arithmetic nature of the replacement, but transcendence of support alone is not an obstruction to asymptotic random laws.

### T3: triangle realization and persistent count gap

Cubic Euler equations 3V=2E and V−E+1=2−2g give V=4g−2, E=6g−3, N=12g−6≥18. A regular hyperbolic N-gon with alpha=2pi/3 exists for N>6. Its right-triangle decomposition gives cosh(ell/2)=2cos(pi/N)/sqrt3 and area=(N−2)pi−Nalpha=4pi(g−1). Reverse-endpoint orientation-compatible side pairings produce an oriented closed quotient, and each cubic vertex sees exactly three corners, total2pi; midpoint and face-center sums are also2pi. Thus there are no hidden cone singularities.

Subdividing E original edges produces N clean dessin edges/darts. Their monodromy cycle types are2,3,N. The stabilizer-preimage subgroup has indexN and is torsion-free: any nonidentity finite-order triangle element is conjugate to a nontrivial power of an elliptic generator, and its permutation has no fixed dart because every cycle has full signature length. By contrast, using a multiple signature or only divisibility could introduce fixed darts and torsion; this candidate uses the full lengths correctly. The orientation-preserving group has orbifold area2pi(1−1/2−1/3−1/N), whose quotient into4pi(g−1) is exactlyN. The group need not be normal. Recoverability is claimed only with retained graph/root/rotation marking.

Philippe Cor5.2 is explicitly for the orientation-preserving group (not reflections); its p=3 formula is b_N=2arcosh(2cos²(pi/N)−1/2). Subgroups cannot contain translations shorter than the parent minimum, even if they do not attain that minimum. For N≥18, the argument of arcosh exceeds (1+sqrt3)/2>4/3, while cosh(1/2)≤53/47<4/3. Therefore sys>1. (The first strict inequality uses N>12; no N=7 exception is relevant.) Every replacement count on[1/2,1] is exactly0.

The WP theorem's exact display gives mu=integral_(1/2)^1 (cosh t−1)/t dt>3/16. As counts are integer-valued, weak convergence to the stated Poisson law implies P(count0)→exp(−mu); total variation to the replacement's delta0 is exactly1−P(count0), tending to1−exp(−mu)>3/19. Neither weighting input maps nor choosing another CFF matching can change this support gap. A deterministic length scale with positive lower bound still yields a fixed shorter forbidden interval. A scale tending to0, variable geometries or alternative correspondences remain outside the claim. Finite atomicity at each g alone would be insufficient to establish the asymptotic failure.

CFF multiplicity remains2^(E+1) on any graph-preserved restriction, so uniform restricted signed trees push to uniform rooted cubic maps. This is an existence consequence of the known bijection, not an efficient algorithm or naive inverse rotation prescription. The finite unmarked surface law is weighted by input multiplicities. Exact WP law cannot arise from this finite support (WP is smooth on positive-dimensional moduli), and the independent systolic argument gives the stronger asymptotic obstruction.

### T4: intrinsic cut disk and perimeter

For a finite cellular one-face graph embedded in a smooth closed hyperbolic surface with disjoint positive piecewise-geodesic edge interiors and positive incident sectors, cut along every edge and separate repeated vertex occurrences. The intrinsic completion is a compact topological disk. Subdivide bends. Interior curvature is−1; boundary sectors may be reentrant or2pi at a leaf. Izmestiev's cone-disk definition permits all positive boundary sector angles; there are no interior cone points, so its negative-cone-curvature condition is vacuous. This does not rely on an injective development into H², an invalid shortcut explicitly warned about in that source.

Cutting a finite graph removes zero area and duplicates every edge, including bridges: A=4pi(g−1), P=2sum length. P²≥4piA+A² gives P≥4pi sqrt(g(g−1)). With P=12g this is pi²(g−1)≤9g. At g12, pi>157/50 violates it; pi²−9>0 extends violation to all larger g. At g11, pi<22/7 makes it hold, and the same monotonicity gives all g2–11. No existence theorem is claimed for those lower genera.

Taking sum output≥6g s_g, s_g=(pi/3)sqrt(1−1/g), gives a positive total increase6g(s_g−1) for g≥12. Triangle inequality, a weighted mean of ratios, and max absolute change≥sum absolute change/E yield the stated four deformation bounds. Their lower bounds tend to pi/3−1, so a vanishing uniform relative change or vanishing relative l1 cost is impossible in this class. Genus0/1, changed curvature, positive interior cone curvature, multiple faces and topology changes cannot be imported into this formula.

### T5: adaptive repair and exact Dirichlet law

The independently fetched published BGL PDF section1.2/page5 states P=2sum edge lengths and normalized coordinates 2ell/P~Dirichlet(1^(6g−3)); section6 fixes P=12g. Its download is dynamically watermarked and has a different byte hash from the candidate's older copy; the mathematical text agrees. This source was completed during proof verification, before code or stored-check reading. The baseline's complete Chapuy1006 trisection excerpt was read in the invocation immediately preceding candidate proof reading; source baseline already used the independently read CFF reconstruction of that theorem.

The exponential change of variables gives S independent of X and E[S]=E. Largest-j exponential mean is H_E−H_(j−1), from spacing rates E,E−1,…,1. Summing j1…k gives k(1+H_E−H_k). Since the top-k exponential sum is S times top-k Dirichlet mass T, E[T]=(k/E)(1+H_E−H_k). This is an all-E deduction, including E1; simulation is irrelevant.

For any adaptive subset I with at mostk changed edges and capC≥1, total normalized increase≤(C−1)sum_(I)X≤(C−1)T. Thus success implies (C−1)T≥delta_g>0. Markov yields min(1,(C−1)E[T]/delta_g), uniformly over adaptive choices and auxiliary data. k0/C1 cannot succeed. Set containment also proves the outer-probability statement if geometric existence is not measurable. Conditional Dirichlet laws suffice even with arbitrary graph sampling.

H_E−H_k≤log(E/k) and r(1+log(1/r))→0 as r→0 prove bounded-cap k=o(g) failure, since delta_g→pi/3−1>0. For almost-sure success without a cap, C≥1+delta_g/T pointwise; Jensen gives E[C]≥1+delta_g/E[T], with infinite expectations allowed. This establishes only necessary costs, not existence of any successful repair.

## Strongest verified result and exact gap

Accepted partial package: algebraic-palette exact/null-set obstructions; valid known triangle/dessin construction with a universal short-geodesic discrepancy; intrinsic perimeter lower bound excluding P=12g direct realizations for every g≥12; and adaptive sparse bounded-stretch failure under the established source law. This package is internally consistent. It supplies no geometric sufficiency theorem, WP pushforward law, asymptotic coupling, full response to the broad source question, efficient CFF algorithm, or verified historical novelty. No mathematical blocker found in the five proof files at this stage.
