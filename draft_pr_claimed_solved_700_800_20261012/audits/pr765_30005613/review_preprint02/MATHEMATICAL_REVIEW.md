# Independent mathematical reconstruction and falsification attempts

The input theorem is the one specified in INITIAL_POSITION.md and CHECKED_INPUTS.json. I read the actual repaired paper before inherited verdicts. This review finds no central mathematical gap within its exact existential, chosen-width, zero-thickness Dirichlet scope. This is an ordinary mathematical audit, not proof-assistant certification. The one unresolved package issue is described separately in COMPRESSION_ISSUE.json.

## Geometry, form spaces and the removable point

At the next interface p, every connector point with first coordinate below p lies in the last old cube: its longitudinal distance to that cube center is below a_n and its transverse coordinates have size below delta<a_n. Every connector point above p lies in the new, larger cube. The only added points lie on the middle face. That face patch is null in d-dimensional Lebesgue measure, while the full connector cube makes the union open and connects its two overlapping open portions. Equal L2 spaces here follow from this exact null difference; equal closures of general open sets would not suffice.

The boxes remain bounded at each finite stage. Extension by zero is an isometry for the H1 norm on H01, by its compactly supported smooth approximation definition. Its image is a closed subspace of H01(B). This uses no Lipschitz-boundary or H1 extension theorem for the irregular screens. Box Rellich and Poincare respectively supply compact resolvents and strictly positive finite-stage eigenvalues. Confusing H01 with unrestricted H1 on an irregular bounded open set would invalidate these steps; the paper consistently uses H01.

The key intersection is exact. The spaces V_delta decrease as delta decreases and contain V0. For a bounded intersection element u, choose a cutoff vanishing on a neighborhood of p large enough to contain the entire connector for a sufficiently small delta. Multiplying a compactly supported smooth approximation in D_delta by this cutoff gives an approximation compactly supported in D0. The strict containment in the zero neighborhood prevents support accumulating against the removed aperture edge. Hence zeta_r u belongs to V0.

For d>=3, radial scaling on the annulus (r,2r) makes the squared gradient energy C r^(d-2). For d=2, let L=log(1/r), t=log(rho/r^2)/L and zeta=theta(t). Polar coordinates give

    integral |gradient zeta|^2 = (2*pi/L) integral_0^1 |theta'(t)|^2 dt.

The support error shrinks to the point. In the H1 product difference, (1-zeta)u and (1-zeta)gradient u vanish by dominated convergence; the remaining term is bounded by ||u||infinity ||gradient zeta||2 and vanishes by the energy formula. A real/imaginary Sobolev truncation fixing zero preserves every V_delta and converges in H1. Applying the bounded argument to each truncation and closing V0 proves the intersection for arbitrary complex u.

Boundary attacks: naive radial scaling in d=2 gives a nonvanishing energy and cannot replace the logarithmic cutoff. In d=1, (0,1) and (1,2) plus every positive connector give (0,2), while the disconnected limit has a new midpoint Dirichlet trace. The first eigenvalues pi^2/4 and pi^2 show the resolvents do not converge to the claimed disconnected operator. The stated dimensional exclusion is necessary.

## Finite-window norm convergence

For any sequence delta_j->0, not necessarily monotone, weak H1 limits from V_delta_j belong to every fixed V_s: eventually delta_j<s, and a closed linear subspace is weakly closed. The preceding intersection puts the limit in V0. Each element of V0 is already a recovery sequence.

For bounded inputs f_j, the resolvent variational equation gives uniformly bounded H01(B) solutions. If operator-norm convergence failed, select unit inputs with discrepancy bounded below, take a weakly convergent input subsequence, and use Rellich to get a strongly L2 convergent solution subsequence. Testing against V0 identifies its limit with R0 f. Compactness of R0 also gives R0 f_j->R0 f. The positive discrepancy is impossible. This is the needed varying-input argument, stronger than proving convergence for fixed inputs. Earlier windows remain fixed throughout; no uniform boundary regularity or quantitative aperture estimate enters.

## Nonresonance, whole clusters and stage order

At stage n the finite protected set S_n is determined before the next cube. A resonance in a bounded width interval forces

    sum m_i^2 = 4*a^2*lambda/pi^2.

The right side is bounded uniformly over that interval and finite set. There are finitely many positive integer multiindices, and each pair (lambda,m) forbids at most one positive width. Selecting a width outside this finite set is legitimate and does not alter earlier geometry. Width selection precedes window selection; there is no dependence on unknown future eigenvalues or future test bases.

In the disconnected enlargement, each selected eigenvalue has exactly its old full eigenspace, because the new cube avoids it. Compact resolvent isolates these finitely many levels. Mapping them to nonzero eigenvalues of the bounded resolvent allows fixed disjoint Riesz contours. Norm-resolvent continuity gives norm-continuous whole-cluster projections. If two projections have norm distance below one, each is injective on the other's range; their finite ranks coincide.

Each smaller protected sum uses a subset of the same disjoint intervals. Thus nesting, full-eigenspace status and ranks survive even when an old repeated eigenvalue splits. There are only finitely many constraints at this stage, so a single positive delta satisfies them and delta<min(a_n/2,2^-n). A new complete spectral cutoff can contain every transported cluster and approximate the finite F_(n+1), by the finite-stage compact-resolvent eigenbasis. The old sums need not remain low-energy cutoffs. No uniform spectral gap and no simple spectrum are required.

Attack on individual eigenvectors: rotate a repeated two-dimensional eigenspace by rational cosine7/25 and sine24/25, then split its two eigenvalues by +/-t. The operator perturbation tends to zero as t->0, but a selected rank-one branch stays at projection distance24/25 from a chosen old coordinate. The full two-dimensional cluster is unchanged. exact_controls.py verifies this different rational example and a three-dimensional finite forbidden-width choice. These finite examples expose why branches would fail; they do not certify the infinite PDE construction.

## Common space and final exhaustion

The interiors of all cubes are disjoint and their interface patches add no L2 summand. Their individual sine bases therefore form an orthonormal basis of the final H. Defining a cube basis at its birth does not assume future widths, and the final common-space identifications preserve all previous norms. Probes need only be L2 vectors; they need not satisfy the final operator boundary conditions.

The increasing open stages cover Omega. A compact support admits a finite subcover and hence lies in one stage. Thus their H01 form domains exhaust H01(Omega). For b=q+inner-product, R_n f is the b-orthogonal projection of Rf onto V_n; density proves convergence in form norm and therefore strong convergence in H. Only the final R is identified as a genuine full-space resolvent. Extended finite-stage R_n vanish on future cube summands and are not invertible on H.

Norm exhaustion is false and unnecessary. Unit low-energy bumps in later, larger cubes have R_n u_j=0 for fixed n, whereas ||Ru_j-u_j||<=||A u_j||->0. Consequently ||R-R_n|| has lower bound1. The proof correctly separates this strong exhaustion from the bounded-window norm limit.

## Protected limits, energy escape and completeness

For fixed k, the sum of transport errors from n onward is exactly 2^(-n-1). The norm limit P^k is self-adjoint and idempotent by multiplication/adjoint continuity. Once its distance from some finite-stage projection is below one, the injection argument gives the same finite rank. Nestedness also passes in norm. For every f,

    ||R_n P_n^k f - R P^k f||
      <= ||R_n|| ||P_n^k-P^k|| ||f|| + ||(R_n-R)P^k f|| -> 0.

The corresponding reverse product estimate gives RP^k=P^kR. No commutator of unbounded Laplacians is passed through a limit.

A finite-dimensional reducing restriction of the positive injective R diagonalizes with strictly positive eigenvalues mu. For Rv=mu v, v=mu^-1 Rv lies in dom A and Av=(mu^-1-1)v. A uniform lower bound on all mu across k is unnecessary. Positivity plus injectivity on each finite-dimensional space is enough.

The injectivity is indispensable. On ell2, let R_n e1=n^-1 e1 and R_n e_j=(j+1)^-1 e_j for j>=2. Fixed finite coordinate projections are perfectly transported and exhaustive, but the e1 energy escapes to infinity and the limiting bounded operator kills e1. That limit is not a genuine self-adjoint resolvent on the entire space. The paper independently identifies its final resolvent before using injectivity, so this counterexample does not apply. Likewise, rank-one projections onto e_n converge strongly to zero and lose their rank; using norm projection convergence is essential.

For each fixed cube-basis probe f_(j,l), every late F_n contains it. Applying the birth bound and the tail estimate to the trajectory born at that same n gives

    ||(I-P^n)f_(j,l)|| < 2^-n + 2^(-n-1) = 3*2^(-n-1) ->0.

This explicitly justifies the diagonal use of changing birth index. Each approximant is in the closed pure-point span. Every probe, and hence all of H, lies in that span. Diagonalizing the finite orthogonal differences of the nested limiting ranges gives a complete ON eigenbasis. Dense positive eigenvalues alone would not do this: direct-sum a rational diagonal operator with multiplication by x on a Cantor-measure L2 space. The diagonal eigenvalues can be dense in the half-line while an SC component survives. The repeated dense probes prevent such an unseen complement.

## Spectrum, zero and exact claim boundaries

The expanding widths tend to infinity, so Omega has arbitrarily large interior balls and infinite volume. The plane-wave cutoff on radius a_n/2 lies compactly inside cube n. It belongs to Cc-infinity(Omega) and to the form-defined operator domain, with Laplacian equal to the ordinary smooth Laplacian. The product rule gives the displayed residual bound of order r_n^-2+sqrt(lambda)r_n^-1. Its unit norms, disjoint supports and Bessel inequality give a weakly null Weyl sequence at every lambda>=0, including zero. Thus all of the half-line is essential spectrum; nonnegativity gives the reverse inclusion. Completeness identifies the spectrum with the closure of eigenvalues. A zero eigenfunction has zero weak gradient, is constant on connected Omega, and its infinite volume forces that L2 constant to vanish. Therefore the eigenvalues are positive and dense, while zero remains a noneigenvalue spectral endpoint.

The proof does not provide an arbitrary prescribed-width theorem, Neumann or smooth-boundary version, positive-length passages, or effective window sizes. It proves an existence result with chosen widths and positive shrinking face windows for every fixed integer d>=2. The repaired base definition O1=Q1(1) and the downward delta direction now make the standalone induction explicit. No mathematical repair remains identified within this scope.

## Relation to inherited evidence

After the independent initial position, I read the full prior preprint REPORT/VERDICT/MATHEMATICAL_REVIEW and repair disposition. Their mathematical checks agree with the above derivation. The original first review's stale opening count is superseded explicitly by the root disposition; its closed bytes remain unchanged. Four software defects and one exposition clarification were the prior issues. The independent physical tests here confirm their repairs in the fixed current inputs. None of those old PASS statements is used as a premise of this proof audit.
