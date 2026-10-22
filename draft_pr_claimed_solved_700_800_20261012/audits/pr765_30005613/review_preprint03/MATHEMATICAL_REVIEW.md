# Independent reconstruction and attempted falsification

This is the third fresh whole-preprint review. The exact paper is identified in CHECKED_INPUTS.json. INITIAL_POSITION.md was written from the actual current paper before inherited mathematical reports, preprint verdicts or root repair dispositions were read. The reconstruction below is an independent argument check. No favorable inherited verdict is a proof premise. Within the stated existential theorem I find no central gap or required mathematical repair. This is ordinary AI-assisted mathematical review, not a formal certificate.

## Claim, geometry and quantifiers

For each fixed integer d>=2 the construction chooses some expanding cube tower and positive shrinking zero-thickness face windows. It does not keep an arbitrary prescribed width sequence. The form on H_0^1 defines the nonnegative self-adjoint Dirichlet operator without a boundary regularity assumption. The claimed complete eigenbasis is a spectral-type assertion; the spectral set is the closure of the eigenvalue set, the full essential half-line, with zero excluded as an eigenvalue.

At p=(x_n+a_n)e_1, a connector point below the interface has first coordinate in the final old cube and every transverse coordinate has absolute value <delta<a_n. A connector point above p is similarly in the new larger cube. Thus D_delta minus D_0 is exactly the middle-face patch. It is null for d-dimensional measure but changes the form domain. Openness follows from the full connector cube in the union, and connectedness from its nonempty open overlaps with both components. The disconnected form splits over its two components by splitting smooth compact approximants; the associated operator is the direct sum. None of these assertions follows merely from equality of closures or from a null change of domain.

The recurrence a_(n+1)>a_n+1, x_(n+1)=x_n+a_n+a_(n+1), with a_1=x_1=1, gives expanding balls and an infinite-volume domain. It also makes the interfaces escape to infinity. Countably many interface patches add no L2 summand; the final L2 is the direct sum of cube L2 spaces. Bases are fixed at cube birth and only used as L2 probes. No claim that their extensions satisfy the final operator boundary conditions is required.

## H_0^1 intersection and the d=2 cutoff

For any fixed finite earlier tower, with every old aperture held fixed, zero extension embeds each V_delta=H_0^1(D_delta) as a closed subspace of H_0^1(B), for a single enclosing box B. This uses the definition by C_c^infinity approximation and no trace/extension theorem for the irregular screens. The same box gives Poincare positivity and Rellich compactness. Unrestricted H^1 of an irregular domain could behave differently; it is not used.

V_0 is contained in every V_delta. To prove the reverse intersection inclusion, take bounded u belonging to every V_delta. For fixed r choose a smooth cutoff zeta_r vanishing on a ball about p and equal to one outside a shrinking larger ball. Choose delta sufficiently small that the entire connector lies strictly in its zero neighborhood. If phi_m in C_c^infinity(D_delta) tends to u in H1, then zeta_r phi_m has compact support in D_0. Multiplication by the fixed smooth cutoff is continuous in H1. Thus zeta_r u is in V_0 even when earlier screens or window edges are irregular.

For d>=3 the radial transition on r<rho<2r has gradient energy C r^(d-2). For d=2 put L=log(1/r) and t=log(rho/r^2)/L. A smooth theta flat at 0 and1 gives derivative theta'(t)/(rho L). Polar integration, using d(rho)/rho=L dt, yields exactly

    integral_R2 |gradient zeta_r|^2 = (2*pi/L) integral_0^1 |theta'(t)|^2 dt ->0.

The support of 1-zeta_r shrinks to p. In the H1 product error, the terms (1-zeta_r)u and (1-zeta_r)gradient u vanish by dominated convergence; u gradient zeta_r is bounded by ||u||infinity ||gradient zeta_r||2. Hence zeta_r u->u in H1. For general complex u, truncate real and imaginary parts by zero-fixing Lipschitz truncations, which preserve every H_0^1(D_delta) and converge in H1. Apply the bounded argument, then close V_0. Therefore intersection V_delta=V_0.

A naive linear annular cutoff has constant gradient energy in d2 and would fail. The paper uses the necessary logarithmic scale. In d1, the union of (0,1),(1,2) with every positive connector is (0,2). Its first eigenvalue is pi^2/4, whereas the disconnected union has first eigenvalue pi^2. Hence the disconnected norm-resolvent conclusion is false there. Point capacity and the dimension restriction are substantive, not cosmetic.

## Finite-window norm convergence with varying inputs

For delta_j->0, including nonmonotone sequences, any weak H1 limit of u_j in V_delta_j lies in every fixed V_s: eventually delta_j<s and V_s is weakly closed. The intersection puts it in V_0; each v in V_0 is its own recovery sequence.

Let R_delta=(A_Ddelta+1)^(-1). The variational equation gives a uniform H_0^1(B) bound on R_delta f when ||f||2<=1. Suppose norm convergence to R_0 failed. Choose delta_j->0 and unit inputs f_j with a discrepancy bounded below. Pass to weak f_j->f and, by Rellich and the uniform H1 bound, strong L2 and weak H1 convergence of R_delta_j f_j to u. The preceding intersection gives u in V_0. Testing against any v in V_0 identifies u=R_0 f. Compactness of R_0 also gives R_0 f_j->R_0 f. This contradicts the discrepancy. The proof therefore supplies the operator norm convergence needed for spectral clusters; fixed-input strong convergence alone would be insufficient. There is no quantitative aperture estimate or uniform-in-stage assertion.

## Finite nonresonance, cluster splitting and induction order

The old protected finite positive set S_n is determined by already fixed O_n. For a in (a_n+1,a_n+2), a resonance forces sum(m_i^2)=4 a^2 lambda/pi^2. Bounded a and finite S_n bound all integer coordinates. Each pair (multiindex,lambda) excludes at most one width, so only finitely many widths are forbidden. Width is fixed first, isolating intervals second, a positive aperture third, and the new birth cutoff last. Future probe bases and future eigenvalues do not enter earlier choices.

Nonresonance ensures that each old protected eigenvalue has exactly its complete old eigenspace in the disconnected enlargement. Compact resolvent isolates it. Under t->(1+t)^(-1), the protected values are isolated nonzero eigenvalues of the bounded resolvent. Fixed contours and the resolvent identity give norm convergence of their Riesz projections. Because there are finitely many contours and nested sums at this stage, one aperture meets every requested error bound. No gap bound uniform in n is needed.

If orthogonal projections P,Q satisfy ||P-Q||<1, Q restricted to Ran P and P restricted to Ran Q are injective: a nonzero vector in either kernel would give a norm discrepancy at least one. Their finite ranks therefore agree. Disjoint intervals retain all split eigenspaces in each old cluster; the smaller protected sums select subsets of the same intervals. This preserves complete-eigenspace status, nesting and ranks despite degeneracy. A sufficiently high new finite cutoff includes all transported clusters and approximates the finite F_(n+1). Previously born projections may cease to be low-energy cutoffs, as the paper explicitly allows.

A branch-only replacement is false. Rotate the first two coordinates with c=20/29,s=21/29 and split an old repeated resolvent value1/2 into1/2 +/-t. The operator distance to the old resolvent is exactly t, tending to zero, but one branch projection stays at distance21/29 from the original first-coordinate projection. The complete rank-two cluster stays unchanged. EXACT_CONTROLS.json checks this different exact rational witness, nested rank2/rank3 rotations, a d4 finite forbidden-width set with140 squared widths and admissible17/7, and17,199 rational geometry grid points in d2,3,5. These are illustrative finite controls, not PDE proofs.

## Genuine final resolvent and the two different limits

Let V=H_0^1(Omega), b=q+inner-product. The zero-extended V_n=H_0^1(O_n) are closed increasing subspaces. Every compact support in the increasing open cover is contained in one O_N by a finite subcover. Hence their union is form-dense in V. If R=(A_Omega+1)^(-1), the zero-extended R_n f is exactly the b-orthogonal projection of Rf onto V_n. Thus R_n->R strongly, even in form norm on each input, with norms<=1.

Finite extended R_n vanish on future cube summands and are not genuine resolvents on all final H. The limiting R is identified independently as the actual whole-domain resolvent, and is injective. This prevents a hidden assumption about the limiting operator. The finite-window norm limit and the final strong exhaustion are distinct arguments.

In fact ||R-R_n||=1 for each fixed n. Take normalized smooth low-energy bumps u_j in later expanding cubes. R_n u_j=0, whereas Ru_j-u_j=-R A u_j->0. This gives the lower bound1; positivity and contraction bounds give the upper bound1. The paper never uses the false stronger norm exhaustion.

## Norm-limit finite subspaces, commutation and energy escape

For fixed k, summable errors produce a norm limit P^k with

    ||P^k-P_n^k|| <= sum_(j=n)^infinity 2^(-j-2) =2^(-n-1).

Adjoints and multiplication pass in norm, so P^k is an orthogonal projection. Its distance from a late P_n^k is below1, so it has the same finite rank; nesting passes to limits. For any f,

    ||R_n P_n^k f-R P^k f||
      <= ||R_n|| ||P_n^k-P^k|| ||f||+||(R_n-R)P^k f|| ->0,

and the opposite product has bound ||P_n^k-P^k|| ||R_n f||+||P^k(R_n-R)f||. Hence RP^k=P^kR. No unbounded commutator is passed to a limit.

The finite-dimensional reducing restriction of positive injective R has an ON eigenbasis with mu>0. For Rv=mu v, v=mu^(-1)Rv belongs to dom A and Av=(mu^(-1)-1)v. Thus every limiting range is in the closed pure-point span. A uniform lower bound on mu over all k is unnecessary.

Injectivity matters: on ell2 let genuine resolvents R_n e1=n^(-1)e1 and R_n e_j=(j+1)^(-1)e_j for j>=2. Fixed finite coordinate projections transport exactly and exhaust the space, but the limit kills e1; its energy escaped to infinity. Such a limit is not a whole-space self-adjoint resolvent. The paper separately constructs the genuine R and therefore excludes this counterexample. Likewise rank-one projections onto e_n converge strongly to zero while losing rank; this cannot happen to a fixed trajectory converging in norm.

## Completeness and the possible singular-continuous complement

Every fixed f_(j,l) belongs to F_n for every n>=max(j,l). The trajectory born at each such n satisfies

    ||(I-P^n)f_(j,l)|| <2^(-n)+2^(-n-1)=3*2^(-n-1)->0.

The explicit tail is valid for every trajectory, including the moving birth index k=n; no unjustified interchange of pointwise limits occurs. Each P^n f is in the closed eigenvector span, so every cube-basis vector is in that span and H_pp(A)=H. The finite-dimensional orthogonal differences of the nested limiting ranges can then be diagonalized to obtain a complete ON eigenbasis.

Without the exhaustive probes, dense eigenvalues and noAC leave a real gap. Direct-sum a diagonal operator listing all positive rationals with multiplication by x on L2 of an atomless Cantor measure. The positive point eigenvalues are dense in the half-line and there is no AC, but a nonzero SC subspace remains. Exactly transported finite coordinate projections confined to the diagonal summand miss it. The paper revisits every vector in an actual basis of the whole H and closes this gap. Trace-class stability is not used to eliminate SC.

## Weyl half-line, zero, and strongest result

For lambda>=0 choose |xi|^2=lambda and a unit chi in C_c^infinity(B1). Its scaled plane-wave translate in the ball of radius r_n=a_n/2 lies in C_c^infinity(Omega) and hence the form-defined operator domain, where the operator is -Delta. The product rule gives residual <=r_n^(-2)||Delta chi||+2 sqrt(lambda)r_n^(-1)||gradient chi||, tending to zero. Disjoint supports give orthonormality and weak convergence to zero. Weyl's criterion gives every nonnegative energy, including zero, in the essential spectrum. Nonnegativity gives equality with the half-line. Completeness identifies it with closure(point spectrum).

A zero eigenfunction has q[u]=0, hence zero weak gradient. It is constant on connected Omega and vanishes by infinite volume and L2 integrability. Consequently every eigenvalue is positive and these positive eigenvalues are dense; zero remains a spectral endpoint without an eigenvector.

The strongest verified result is precisely the theorem stated in INITIAL_POSITION: some chosen-width, chosen-positive-window Dirichlet tower for every integer d>=2, with complete ON eigenbasis, spectrum=essential spectrum=closure(point spectrum)=[0,infinity), no zero mode and no AC/SC. Arbitrary prescribed widths, smoothing, Neumann conditions, positive-length passages and effective apertures remain outside it. No route is marked successful by transferring the central difficulty to a stronger unsupported statement; each needed analytic limit has been checked above.
