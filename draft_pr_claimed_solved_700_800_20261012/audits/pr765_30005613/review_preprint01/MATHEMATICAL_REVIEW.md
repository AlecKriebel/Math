# Independent mathematical adversarial review

Scope: the actual six-page paper, SHA256 dcc9995bfeb4d85541429e5ab0ce62176bca4f6c6a7d9389fe647c6309940c3a. The initial claim and mechanism were recorded before inherited verdicts. Later comparison with inherited audits is separate evidence. No central mathematical repair or counterexample was found. The two required repairs in REPORT.md concern package software.

## Exact geometry and bounded form spaces

Let p=(x_n+a_n)e_1. If y belongs to the connector cube and y_1<p_1, its first coordinate lies in the last old cube and every transverse coordinate has absolute value below delta<a_n. If y_1>p_1, it belongs to the new cube, whose half-width is larger. Only the middle face is new. This proves the common L2 identity from an explicit null difference, rather than from equal closures of arbitrary open sets. Equal closures by themselves would not justify it. The whole open connector cube ensures openness, and its positive-volume overlaps ensure connectedness.

For any fixed earlier irregular tower, zero extension embeds its H0^1 spaces as closed subspaces of H0^1(B) for one containing box. This follows from the definition by smooth compact approximants, with no boundary trace theorem. Box Poincare gives strict positivity at the finite stages; box Rellich gives compactness. The assertion would not be justified for unrestricted H1 spaces on arbitrary bounded irregular sets. The paper consistently uses H0^1.

## Capacity and the exact form intersection

The spaces V_delta decrease. The inclusion V0 into their intersection is immediate. For bounded u in the intersection, use the paper's smooth cutoff zeta_r, then choose delta so the entire connector is in its zero ball. Multiplication of Cc-infinity(D_delta) approximants by that fixed cutoff gives smooth functions supported compactly in D0. Consequently zeta_r u is in V0. The support assertion remains valid at aperture edges because the whole connector lies strictly inside the zero neighborhood.

For d>=3, polar scaling of a smooth radial cutoff on r<rho<2r gives gradient energy C*r^(d-2), with support error O(r^d). For d=2, set L=log(1/r), t=log(rho/r^2)/L. Then d(rho)/rho=L*dt and |gradient zeta|^2=|theta'(t)|^2/(rho^2 L^2). Polar integration gives exactly (2*pi/L)*integral_0^1 |theta'|^2. Both gradient energy and support error tend to zero. Dominated convergence handles (1-zeta_r)u and (1-zeta_r)gradient u; boundedness controls u gradient zeta_r. These are all terms in the H1 product error.

For arbitrary complex u, truncate its real and imaginary parts using Lipschitz truncations fixing zero. They preserve every V_delta and converge in H1; apply the bounded argument to each truncation, then use closedness of V0. No uniform pointwise bound for an arbitrary Sobolev function is assumed. This proves the precise intersection needed. It is not a theorem about arbitrary decreasing open sets without the removable-point geometry.

Dimension-one attack: two touching intervals (0,1) and (1,2), with any positive connector, give (0,2), whereas delta=0 gives the disconnected union. The lowest Dirichlet eigenvalues are pi^2/4 and pi^2. Positive windows therefore cannot tend to the disconnected resolvent in norm. In d=2 a naive linear rescaling also has constant gradient energy; the logarithmic construction is essential. Both attempted failures are excluded in the paper.

## Norm resolvent limit with earlier apertures fixed

For any delta_j->0, weak H1 limits of u_j in V_delta_j lie in every fixed V_s, since eventually delta_j<s. Closed subspaces are weakly closed. The intersection argument puts the limit in V0, and each v in V0 is its own recovery sequence. Nonmonotone delta sequences are permitted.

For unit-bounded f_j, the variational equation gives ||R_delta_j f_j||_H1(B)<=C. A weakly convergent subsequence of f_j and Rellich compactness of the outputs give a strongly L2 convergent subsequence u_j. Testing against V0 identifies its limit as R0 f. Compactness of R0 implies R0 f_j->R0 f. A positive lower bound on ||(R_delta_j-R0)f_j|| is impossible. This independently supplies the operator-norm statement, including arbitrary fixed earlier windows. The proof does not transfer the central difficulty to an unsupported continuity assertion.

## Degeneracy, finite resonance avoidance, and induction order

At stage n, S_n is a finite positive set already fixed by the old operator. If a lies in (a_n+1,a_n+2), a resonance forces sum_i m_i^2=4*a^2*lambda/pi^2. Its right side is bounded uniformly over that finite set and interval. There are finitely many multiindices and each pair excludes at most one positive width. One may select the next width first and then its aperture. Future probes and future eigenvalues enter no earlier constraint.

Every protected eigenvalue of the disconnected enlargement has exactly the old complete eigenspace, since the new cube avoids it. Compactness isolates it. Fixed contours around its nonzero bounded-resolvent eigenvalue give norm-convergent Riesz projections. A finite family of contours remains separated from zero and the rest of the spectrum; no uniform separation over all stages is required. Rank equality follows because projections at norm distance below one inject into each other's ranges.

A multiple eigenvalue can split, but its whole isolating interval is retained. Smaller protected projections select subsets of the same disjoint intervals; their nesting and full-eigenspace status survive. The finite number of norm constraints permits one positive aperture satisfying all of them as well as delta_n<min(a_n/2,2^(-n)). Birth cutoffs can be placed above all transported clusters while approximating a finite L2 test family. An old trajectory is allowed to cease being a low-energy cutoff.

Attack on individual branches: rotate a two-dimensional repeated eigenspace with cosine 5/13 and sine 12/13, then split its resolvent eigenvalues by +/-t. The operator perturbation norm tends to zero with t, but a selected rank-one branch stays at distance 12/13 from the original first coordinate projection. The full rank-two cluster stays fixed. exact_controls.py verifies this exact distance identity, and a different d=3 finite forbidden-width example. The full-cluster condition in the paper addresses the actual obstruction.

## Common Hilbert space and genuine exhaustion

The cubes have disjoint interiors; countably many interface faces add no L2 summand. Their individual sine bases together form a basis of final H. Fixing each such basis only when its cube is chosen is noncircular. It is harmless to identify earlier estimates with the eventual direct sum retrospectively. The probes are L2 vectors and need not be eigenvectors or operator-domain vectors of the final connected domain.

Each compact support in the increasing open cover lies in one O_N by a finite subcover. Thus the zero-extended H0^1(O_n) exhaust H0^1(Omega) in form norm. For every f, R_n f is the b-orthogonal projection of Rf onto that stage, so R_n->R strongly and ||R_n||<=1. Zero-extended R_n have kernels on future cubes. R is independently identified as the actual final resolvent and is injective; these facts are never interchanged.

The stronger operator-norm exhaustion would fail. For fixed n, normalized very-low-energy bumps u_j in later growing cubes satisfy R_n u_j=0 and ||Ru_j-u_j||<=||A u_j||->0. Hence ||R-R_n||>=1. Positivity and contraction bounds give <=1. The paper only uses strong convergence and avoids this invalid stronger claim.

## Protected limits, energy escape, and completeness

For fixed k, the summable errors give a norm limit P^k with distance from P_n^k at most 2^(-n-1). Products/adjoints preserve projection identities; distance below one preserves its finite rank. Nesting passes to limits. On each fixed f,

    ||R_n P_n^k f-RP^k f||
      <= ||R_n|| ||P_n^k-P^k|| ||f|| + ||(R_n-R)P^k f|| ->0,

and the analogous estimate on the opposite product gives commutation with R. No unbounded commutator limit is used. The finite-dimensional reducing restriction of positive injective R diagonalizes with eigenvalues mu>0. Its eigenvectors lie in dom A because v=mu^(-1)Rv, and have eigenvalues mu^(-1)-1 for A. No lower mu bound uniform in k is required.

Without injectivity this could fail: on ell2 let R_n e1=(1/n)e1 and R_n e_j=(1/(j+1))e_j for j>=2. Fixed coordinate projections are exactly transported and exhaustive, yet e1 has energy n-1->infinity; its limiting resolvent coefficient is zero. That limit is not a genuine full-space self-adjoint resolvent. The paper establishes the genuine resolvent before using injectivity, excluding this escape.

For every fixed f_(j,l), all sufficiently late F_n contain it. Therefore its distance to H_pp is at most 2^(-n)+2^(-n-1), uniformly including the trajectory whose birth index is n. This explicit tail bound legitimizes the diagonal use k=n. Every probe is in the closed pure point span, so H_pp=H. The nested finite orthogonal differences yield an orthonormal eigenbasis.

Two weakened claims are false. Projections onto e_n converge strongly to zero and lose their rank, so strong convergence alone is insufficient. A diagonal operator with positive rational eigenvalues can be direct summed with multiplication by x on L2 of an atomless Cantor measure: point eigenvalues remain dense in [0,infinity), no AC is introduced, yet a nonzero SC subspace remains. Exact transport of finite coordinate subspaces in the diagonal summand does not see that complement. The paper's norm transport and exhaustive probes exclude both failures. No trace-class stability argument is used to remove SC.

## Spectral support, endpoint, and boundaries

Plane-wave cutoffs in disjoint expanding cube interiors are in the actual Dirichlet operator domain, with norm one and residual bounded by r_n^(-2)||Delta chi||+2*sqrt(lambda)*r_n^(-1)||gradient chi||. They are orthonormal, hence weakly null by Bessel. Weyl's criterion supplies every lambda>=0 in essential spectrum, including zero; nonnegativity supplies the reverse inclusion. Completeness identifies the spectral set with the closure of its point eigenvalues. A zero eigenvector has zero weak gradient, is constant on connected Omega, and vanishes by infinite volume. No statement that every spectral point is an eigenvalue is made.

The paper supplies an existential zero-thickness Dirichlet example with selectable widths/windows. It does not supply prescribed-width, Neumann, smooth-boundary, positive-length corridor, or effective aperture claims. These boundaries match the proof.

One minor standalone exposition repair is warranted: Section 3 should explicitly set O_1=Q_1(1) alongside a_1=x_1=1. The intended base cube is unambiguous from context and explicit in the preserved original proof. This does not change the theorem or a proof mechanism; the parent independently identified the same clarification.
