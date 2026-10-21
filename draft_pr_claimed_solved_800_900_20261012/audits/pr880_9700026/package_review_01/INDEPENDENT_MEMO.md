# Independent reconstruction before candidate proof

Timestamp: 2026-10-15T10:23:55.257470+00:00

I read the complete primary 2007 p.40 statement and 2012v1 model/paper, plus 2007 Lemma 3 p.9 and unfinished Proposition 30 pp.36–37, before opening the candidate proof or prior auditor verdicts. The 2007 target expressly uses the hard maximum, fixed sites, positive normalized populations, general position, and the disjunctive clause alpha>1 OR 0<beta<2alpha. The 2012 stochastic paper restricts its defining parameters to 0<alpha<=1, beta>0. These are distinct scopes.

## Claim reconstructed
For distinct fixed interior sites xi in the unit square, n>=2, positive simplex weights, alpha,beta>0 with beta>2alpha, let a=alpha/beta and q=2a<1. Let delta_i=min_{j!=i}|xi-xj|>0, h_i=dist(xi,boundary)>0, and R_i=min(h_i,delta_i/2)>0. Because every z_j<=1, the disk centered at xi of radius R_i z_i^a is contained in i's cell: the own weighted distance is <=R_i, while all competitor weighted distances are >=|y-xj|>=delta_i-R_i z_i^a>=delta_i/2>=R_i. Therefore A_i(z)>=c_i z_i^q, c_i=pi R_i^2. This compares against every competitor, not a chosen one. Boundary equality has no area effect.

The ODE satisfies z_i'>=-z_i+c_i z_i^q. Comparing with the exact scalar solution y_i(t)=[c_i+(z_i(0)^(1-q)-c_i)exp(-(1-q)t)]^(1/(1-q)) gives a uniform strictly positive lower bound min(z_i(0),c_i^(1/(1-q))) and positive liminf. Since all coordinates persist, no one coordinate approaches 1. Choosing alpha>1 and beta>2alpha refutes the literal unrestricted 2007 (a) disjunction, even with general position, but says nothing decisive about the 2012 restricted alpha domain, full classification, convergence, or stochastic growth.

## Wellposedness reconstructed
Pairwise equality is an Apollonius circle or line with distinct foci, so every tie set has planar measure zero. The equal-weight line case is harmless. For squared weighted-distance difference g_ij(y,z), no y can satisfy both g=0 and grad_y g=0 when xi!=xj and weights>0 (the circle cannot have radius zero). On any compact interior parameter neighborhood, regularity and compactness give a uniform measure O(epsilon) for the strip |g|<=epsilon, via finite implicit-function charts. Smooth dependence of g on z then bounds cell symmetric differences by a finite union of strips, proving local Lipschitz of areas. Thus local uniqueness holds. Sum A_i=1, so sum z_i remains 1. Moreover z_i'>=-z_i gives z_i>=z_i(0)e^-t on any finite interval. Combined with bounded simplex and local Lipschitz in its interior, this prevents finite-time loss of existence. The stronger barrier gives uniform interior compactness.

## Adversarial boundaries
No argument covers beta=2alpha, zero initial coordinates, coincident sites, or infinitely many sites; constants collapse as site separation or boundary distance tends to zero and as q approaches 1. General position is unnecessary beyond distinctness. A symmetric witness alone would not dispose of the stated general-position qualification, but this all-site theorem does. Finite sampling is not a proof of any of these analytic facts.

## Antecedents already seen
The original Lemma 3 is a two-city Apollonius upper-area argument with exponent 2alpha/beta. Proposition 30 is explicitly unfinished and stochastic but already uses a protected neighborhood and the same exponent to compare growth. Consequently, neither the basic weighted geometry nor recognition of that exponent should be represented as new. The likely defensible contribution is an explicit finite-system quantitative persistence statement and checkable packaging, subject to the direct prior-paper review still to come.

Completion estimate at this checkpoint: 20%. This memo fixes an independent mechanism before candidate comparison.

## Later candidate comparison (separate phase)

2026-10-15T10:35:53.568121+00:00 — After freezing the reconstruction above, I compared the current square-based theorem, explicit slice-band local-Lipschitz proof, original proof, exact witness, and current credit statements. The square constants differ from my disk constants but the mechanisms agree. The candidate supplies a complete quantitative band proof rather than relying on implicit-function compactness. I independently checked its coordinate-slice constants and all-time comparison. No circularity or missing competitor was found. Ferudun’s proved derivative and continuity lemmas imply a qualitative two-city noncollapse result in the same p<1 regime, and every current narrative credits that stronger overlap. This comparison does not change the chronology of the initial memo. Completion estimate: 90%.
