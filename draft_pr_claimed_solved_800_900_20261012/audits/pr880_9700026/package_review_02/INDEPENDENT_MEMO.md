# Independent reconstruction and falsification memo

Written 2026-10-15T10:42:55.653101+00:00 before opening the candidate proof, candidate TeX/PDF, or any prior package review. Sources read first: Aldous 2007 rough notes, pp. 2, 9, 36–37, 40, and Aldous–Huang 2012 arXiv v1 in full extracted text. This is a fresh bounded review, not additional central proof search; original proof effort remains 2/5.

## Exact source claim and model boundary

The 2007 notes allow alpha>0, beta>0 globally and specify, on p.40, finitely many fixed sites, positive initial shares, hard maximum cells, and dz_i/dt=A_i(z)-z_i. Conjecture 32(a) says alpha>1 OR 0<beta<2alpha implies one share tends to one, under an undefined general-position condition. Part (b) additionally claims convergence, positive limits and initial independence for 0<alpha<1,beta>2alpha. The 2012 v1 model is stochastic founding, explicitly restricts alpha<=1, and supplies heuristics; it is not a substitute statement of the fixed-site ODE conjecture. Its boundary heuristic beta=2alpha agrees with the exponent below but does not prove persistence of the ODE.

## Reconstructed persistence mechanism

Let n>=2, distinct sites x_i in the open square, alpha,beta>0. Put q=alpha/beta and p=2q. Set R_i=min{dist(x_i,boundary square), (1/2)min_{j!=i}|x_i-x_j|}>0. For any positive probability vector z, the entire open disk D(x_i,R_i z_i^q) lies in the square. For a point y in it, |y-x_i|/z_i^q<R_i, whereas for EVERY competitor j, |y-x_j|>=|x_i-x_j|-|y-x_i|>2R_i-R_i=R_i>=R_i z_j^q. Thus city i strictly wins against every j. Consequently A_i(z)>=c_i z_i^p, c_i=pi R_i^2>0. This does not use the nearest competitor's weight as a proxy for others. The open disk avoids any tie-boundary issue.

If p<1, u_i=z_i^(1-p) obeys u_i'>=(1-p)(c_i-u_i). Integrating gives
z_i(t)>=[c_i+(z_i(0)^(1-p)-c_i)exp(-(1-p)t)]^(1/(1-p)).
Hence z_i(t)>=min{z_i(0),c_i^(1/(1-p))}>0, and liminf z_i(t)>=c_i^(1/(1-p)), independently of initial shares. These are bounds, not an assertion that the liminf is attained. An initial-independent bound valid at t=0 for ALL positive initial vectors is impossible. The time-dependent bound correctly retains initial data.

For alpha=2,beta=5 (p=4/5), this holds for every distinct interior configuration and every positive initial vector. All n coordinates persist, so none can tend to one when n>=2: use any other coordinate's positive liminf. This disproves the unrestricted alpha>1 disjunct on an open parameter/site region. Merely observing ratio invariance would only show inconsistency among conjectural cases, and would not select the false clause; the independent area and scalar proof does select it.

## Local regularity and ODE existence

Continuity of A is by dominated convergence outside pairwise ties. A pair tie is a circle or a line: after squared weighted-distance comparison it is a nonzero quadratic polynomial with scalar quadratic part; equal weights give a nonzero affine function because sites differ. Such sets have planar measure zero. A finite union remains null; hence sum A_i=1.

For local Lipschitzness, with positive weights on a compact set write G(y)=a|y-x_i|^2-b|y-x_j|^2. The exact identity |grad G|^2=4(a-b)G+4ab|x_i-x_j|^2 gives a uniform nonzero gradient on a sufficiently thin zero slab. The level sets are circles or lines with uniformly bounded length inside the square (e.g. split arcs by quadrants and use monotonicity of x,y to bound total length by a universal square-dependent constant). The coarea formula then gives area{|G|<=epsilon}<=C epsilon. Coefficient variation is Lipschitz in z away from zero, so symmetric differences of pairwise regions have area O(||z-z'||); the cell symmetric difference is contained in the union of pairwise changes. This proves local Lipschitzness without assuming a fixed diagram topology or unequal weights.

The vector field is locally Lipschitz on the positive orthant. In a positive-simplex local solution, sum z remains one and z_i'>=-z_i, so z_i(t)>=z_i(0)e^-t. On any finite horizon these estimates keep the solution in a compact subset of the positive orthant, permitting unique global continuation. Thus the scalar division by positive z_i is justified. Boundary or coincident-site extensions need their own conventions; they are not needed to refute a generic interior claim.

## Falsification attempts / restrictions

* p=1: comparison only gives exponential behavior, not a positive asymptotic lower bound; no persistence conclusion at criticality follows.
* p>1: the power transformation reverses important signs; this argument cannot establish persistence or collapse there.
* Zero initial coordinate: excluded; no claim that a zero weight revives. Coincident sites can create positive-area ties; excluded.
* Sites approaching each other or the boundary: constants tend to zero, so no uniform configuration-independent positive constant is claimed.
* beta/alpha near 2 from above: the exponent 1/(1-p) is singular, and bounds can vanish extremely rapidly. This is consistent with no critical-case conclusion.
* n=1: excluded for collapse contradiction.
* Persistence supplies neither convergence, uniqueness of positive equilibria nor stochastic founding asymptotics.

## Source/priority cautions before inspecting modern treatments

The 2007 Lemma 3 already proves a related pairwise distance-ratio outer containment and the area exponent 2alpha/beta (upper bound for a small city). Its unfinished Proposition 30 explicitly uses a protected disk centered at a newly founded city and the same area exponent for lower growth. Thus the protected-neighborhood device and exponent should not be presented as first invented here. The still-needed comparison is quantitative all-n/all-positive-start ODE persistence, not new weighted-Voronoi geometry or a first negative answer claim. I have not yet read the 1984 or 2026 priority sources or candidate's attribution.

Provisional analytic verdict: the stated scoped persistence theorem is plausibly fully provable by the deductions above. Actual candidate correctness, exact constants, priority credit, disclosures, artifact completeness, execution safety, replay claims, and archive privacy are unreviewed at this checkpoint.
