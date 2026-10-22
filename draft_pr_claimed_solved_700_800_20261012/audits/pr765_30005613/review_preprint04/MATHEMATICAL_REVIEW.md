# Independent whole-argument reconstruction and attempted falsification

The initial position was saved at 2026-10-16T06:20:30.613470Z from the selected record, original proof, current paper and package before opening inherited reports or dispositions. The theorem was treated as a hypothesis. This review finds no unresolved central mathematical gap within its exact existential scope. The arguments below, rather than finite assertion counts or inherited approvals, support that conclusion.

## Exact claim and geometry

For every fixed integer d>=2, choose both expanding cube widths and positive window widths tending to zero. The resulting connected open quasi-conical tower has a form-defined Dirichlet Laplacian A with complete ON eigenbasis, sigma(A)=sigma_ess(A)=closure sigma_p(A)=[0,infinity), no zero eigenfunction, and zero AC/SC spectral subspaces. An interval as the spectral set is compatible with countably many dense eigenvalues. The theorem makes no arbitrary-prescribed-width, boundary regularity, Neumann, positive-length-passage or effective-aperture assertion.

At p=(x_n+a_n)e_1, take a connector cube of half-width delta<a_n. Its points below the interface already lie in the last old cube; their transverse coordinates are smaller than a_n and their longitudinal coordinates lie strictly inside that cube. Points above the interface similarly lie in the new larger cube. Exactly the relatively open middle-face patch is added. This is a null change of the d-dimensional measure, not an equality of Dirichlet form domains. Openness follows from the full open connector cube, and connectedness follows from its open overlaps with both neighbors. Equality of closures alone would not establish the required L2 identity for arbitrary sets; the explicit geometry does.

With a_1=x_1=1 and O_1=Q_1(1), the recurrence gives a_n>=n and longitudinal interfaces 2 sum_{j<=n}a_j escaping to infinity. Finite stages are bounded, the union is open and connected, and inscribed balls have unbounded radii. The union has infinite volume. Countably many added face patches add no L2 component, so the final H is the Hilbert direct sum of the cube L2 spaces. Each cube basis is fixed at its birth. Its zero-extended vectors are L2 probes and need not satisfy final operator boundary conditions.

## Capacity, form intersection and the planar endpoint

Fix all earlier geometry and the next cube. Zero extension realizes V_delta=H_0^1(D_delta) as a closed subspace of H_0^1(B) for one bounded containing box B. This follows from the defining smooth compact approximation and uses no extension or trace theorem on a slit boundary. The same box gives Poincare positivity and Rellich compactness. Unrestricted H1 on arbitrary irregular bounded sets would not justify the same conclusion.

The spaces decrease as delta decreases, and V_0 is contained in every V_delta. To prove the reverse intersection inclusion, take a bounded u in the intersection and a smooth cutoff zeta_r vanishing near p. Choose delta with the whole connector strictly inside its zero neighborhood. Multiply C_c^infinity(D_delta) approximants by zeta_r. Their remaining supports are compact subsets of D_0, so zeta_r u lies in V_0.

In d>=3 a transition between radii r and 2r gives squared gradient norm C r^(d-2). In d=2 set L=log(1/r) and t=log(rho/r^2)/L and use a smooth profile theta flat at both endpoints. Since zeta'_r=theta'(t)/(rho L) and d rho/rho=L dt,

    integral_R2 |gradient zeta_r|^2 = (2*pi/L) integral_0^1 |theta'(t)|^2 dt ->0.

The support of 1-zeta_r shrinks to the point. Dominated convergence controls (1-zeta_r)u and (1-zeta_r)gradient u. The remaining H1 product term satisfies ||u gradient zeta_r||_2<=||u||_infinity ||gradient zeta_r||_2->0. Thus zeta_r u->u in H1. For general complex u, zero-fixing Sobolev truncations of its real and imaginary parts preserve every V_delta and converge in H1. Apply the bounded argument, then use closedness of V_0. This proves intersection_delta V_delta=V_0 with all old apertures fixed.

A linearly rescaled annular cutoff in d=2 has nonvanishing energy and would fail. The actual proof uses logarithmic scale. In d=1, two touching intervals plus any positive connector give one interval, while removal of the midpoint gives two. Their first eigenvalues pi^2/4 and pi^2 show that the disconnected norm-resolvent conclusion is false there. The dimension restriction is substantive.

## The finite norm-resolvent step

For any delta_j->0, without monotonicity, a weak H1 limit from V_delta_j belongs to every fixed V_s because eventually delta_j<s and V_s is weakly closed. It therefore lies in V_0. Every v in V_0 is its own recovery sequence.

For bounded inputs f_j, the +1 variational equations bound R_delta_j f_j uniformly in H_0^1(B). If norm convergence to R_0 failed, take unit inputs with discrepancy bounded below. Extract weak f_j->f and, by Rellich, strong L2 and weak H1 convergence of the outputs to u. The preceding form argument places u in V_0. Testing against V_0 gives u=R_0 f. Compactness gives R_0 f_j->R_0 f as well, contradicting the discrepancy. This checks variable inputs, which is essential for operator norm rather than fixed-input strong convergence. No uniform-in-stage modulus or effective aperture is claimed.

## Nonresonance, multiplicity and the order of choices

The protected set S_n is finite, positive, and determined by the already fixed old operator. A new cube resonance at a in (a_n+1,a_n+2) forces sum m_i^2=4 a^2 lambda/pi^2 with lambda in S_n. The right side is bounded over this finite set and bounded interval. Only finitely many positive-integer multiindices occur, each excluding at most one width for each lambda. Therefore admissible widths exist. The old operator is fixed first, next width second, isolating intervals third, aperture fourth and birth cutoff last. Future spectral data enter no earlier constraint.

Nonresonance makes each protected disconnected eigenvalue have precisely its old complete eigenspace. Compact resolvent isolates it. Its bounded-resolvent value (1+lambda)^(-1) is nonzero and isolated. Fixed contours, the resolvent identity and Neumann inversion yield norm convergence of the Riesz projections. A split multiple eigenvalue is retained as a whole cluster, including all new eigenspaces in its interval. Distinct old intervals remain disjoint. Smaller protected sums select subsets of the same intervals, preserving nesting and complete-eigenspace status.

If projections P,Q have ||P-Q||<1, Q is injective on Ran P and P is injective on Ran Q; otherwise a nonzero kernel vector contradicts that inequality. Hence their finite ranks agree. Finitely many projection constraints allow one positive aperture satisfying all of them and the geometric upper bounds. A high new spectral cutoff includes every transported cluster and approximates the finite current probe family. Old projections need not remain low-energy cutoffs. There is no uniform gap or simple-spectrum assumption.

An independently checked branch counterexample rotates a repeated two-dimensional space with c=8/17 and s=15/17, then splits its two resolvent eigenvalues by +/-t. The operator perturbation tends to zero, while one branch projection stays at distance 15/17 from the old coordinate projection. The whole cluster stays fixed. Thus selecting arbitrary individual branches would invalidate the argument; the paper retains complete clusters.

## Genuine final resolvent versus finite-stage extensions

The zero-extended V_n=H_0^1(O_n) are closed increasing subspaces of V=H_0^1(Omega) for b=q+inner product. Any compact support in the increasing open cover lies in one O_N by a finite subcover. Thus their union is form-dense. For f in H, the extended finite-stage solution R_n f is the b-orthogonal projection of Rf onto V_n, where R=(A_Omega+1)^(-1). It converges in form norm and in H. Also ||R_n||<=1.

The extended R_n have kernels on future cube summands. They are not full-H genuine resolvents. R is independently identified as the actual final-domain resolvent and is injective. Norm convergence of the exhaustion is false: for fixed n take normalized smooth low-energy bumps u_j in later expanding cubes. R_n u_j=0 and Ru_j-u_j=-R A u_j->0. Thus ||R-R_n||>=1; positivity and contraction bounds give equality. The proof requires only strong convergence here and correctly distinguishes it from the finite-window norm limit.

## Norm-persistent finite spaces, energy escape and completeness

For each fixed k, summability gives a norm limit P^k and ||P^k-P_n^k||<=2^(-n-1). Adjoints and products pass in norm, preserving projection identities; the distance-below-one argument preserves finite rank. Nesting passes likewise. For each f,

    ||R_n P_n^k f-RP^k f||
      <= ||R_n|| ||P_n^k-P^k|| ||f|| + ||(R_n-R)P^k f|| ->0,

and the reverse product is bounded by ||P_n^k-P^k|| ||R_n f||+||P^k(R_n-R)f||. Commutation follows. No unbounded-operator commutator is passed through a limit.

Each finite range reduces the positive injective R. It diagonalizes with eigenvalues mu>0. For Rv=mu v, v=mu^(-1)Rv belongs to dom A and Av=(mu^(-1)-1)v. Thus the range lies in the closed pure-point span. No lower bound uniform over all k is needed.

The injectivity hypothesis cannot be omitted. On ell2 take R_n e_1=n^(-1)e_1 and R_n e_j=(j+1)^(-1)e_j for j>=2. Coordinate projections are perfectly transported and exhaustive, yet e_1 escapes to infinite energy and the limit kills it. This limit is not a genuine full-space self-adjoint resolvent. Likewise projections onto e_n converge strongly to zero and lose rank. The actual proof separately establishes genuine R and norm convergence of each trajectory.

For every fixed cube basis probe f_(j,l), every n>=max(j,l) revisits it. The trajectory born at that n satisfies

    ||(I-P^n)f_(j,l)|| <2^(-n)+2^(-n-1)=3*2^(-n-1)->0.

The tail estimate holds explicitly for every trajectory, including k=n; there is no uncontrolled moving-index limit. Each P^n f is in the closed eigenvector span. Hence every basis vector, then all H, lies there. Nested finite-dimensional orthogonal differences diagonalize to the asserted complete ON eigenbasis.

Dense point spectrum or noAC alone is insufficient: direct-sum a diagonal operator listing the positive rationals with multiplication by x on L2 of an atomless Cantor measure. There is a nonzero SC subspace, despite dense point spectrum, noAC, and exact preservation of all finite coordinate projections on the diagonal summand. The exhaustive cube probes rule out precisely this hidden complement.

## Spectral support and zero

The scaled plane-wave cutoffs lie compactly inside disjoint expanding cubes and therefore in C_c^infinity(Omega) and the actual Dirichlet operator domain. The product rule gives residual <=r_n^(-2)||Delta chi||+2 sqrt(lambda) r_n^(-1)||gradient chi||. Norms are one, supports disjoint, and Bessel gives weak nullity. Weyl's criterion supplies every lambda>=0 in essential spectrum, including zero. Nonnegativity gives the reverse inclusion. Completeness identifies the spectral set with closure of eigenvalues.

A zero eigenfunction has q[u]=0 and zero weak gradient. It is constant on connected Omega and vanishes by infinite volume and L2 integrability. All eigenvalues are positive and dense in the half-line. None of these steps requires boundary regularity.

## Fresh controls and strongest verified result

exact_controls.py supplies different rational rank2/rank4 rotations at four scales, the 15/17 branch witness, a d5 forbidden-width enumeration with 283 squared widths and choice 19/8, 2,457 exact connector samples in d3,5,7, and 160 exact tail/birth pairs. A quintic C2 profile has derivative-squared integral 10/7; it is an auxiliary integration diagnostic, not the proof's smooth flat cutoff. Both normal and -O execution retain explicit checks. These finite controls certify no PDE convergence, infinite theorem, aperture modulus or priority.

The strongest verified result is exactly the chosen-width, positive shrinking zero-thickness Dirichlet tower theorem stated above. The review found no unsupported equivalent claim to which a central step was transferred. No proof repair or remaining central gap is identified in this scope. This is internal AI mathematical review, not formal proof or external human peer review.
