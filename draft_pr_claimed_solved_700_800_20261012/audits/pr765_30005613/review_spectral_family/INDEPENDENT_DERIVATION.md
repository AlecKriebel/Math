# Independent spectral-family derivation

Initial position recorded UTC: 2026-10-16T04:41:50.106258+00:00.

## Independence and claim

I first read the full selected record (including the empty prior report) and the 14,044-byte author/PROOF.md, whose SHA256 is 5d1bab0b62ac5f78c69b0d82babd0b79fa4944097470fa760fdb3c485e362a20. I have not read historical audit reports, their favorable verdicts, or README claims. This independent position is recorded before those materials and before receiving another family’s mathematics. The assignment is verification of the existing candidate, not a new attempt or an extension to fixed widths.

The exact mathematical assertion is existential in both expanding cube half-widths and positive shrinking windows for each integer d >= 2. The connected open domain has a Dirichlet Laplacian A >= 0 with a complete orthonormal eigenbasis and spectral set [0,infinity). Its absolutely and singular continuous spectral subspaces vanish. Zero is not an eigenvalue. No result for a prescribed width sequence, smooth boundaries, or positive-length corridors is asserted.

## Independent abstract reduction

Let H be a separable Hilbert space. Suppose R_n are bounded self-adjoint operators, uniformly bounded, converging strongly to an injective nonnegative self-adjoint R. Suppose for 1 <= k <= n there are finite-rank orthogonal projections P_n^k commuting with R_n. Assume they are nested for fixed n and that ||P_(n+1)^k-P_n^k|| <= e_n with sum(e_n) finite. Suppose the initial ranks for each k are finite and the ranks are preserved in n. Then P_n^k converge in norm for each fixed k to a finite-rank orthogonal projection P^k. The proof uses the norm Cauchy estimate, multiplication continuity, and the fact that projections at distance less than 1 have equal finite rank. Nesting survives norm limits.

For each fixed vector f, R_n P_n^k f converges to R P^k f because ||R_n|| is uniformly bounded, while P_n^k R_n f converges to P^k Rf. Thus [R,P^k]=0. Each finite-dimensional range is reducing for R. Nonnegativity and injectivity of R imply all eigenvalues of the finite restriction are positive. If R=(A+1)^(-1), Rv=mu v with mu>0 implies v=mu^(-1)Rv is in dom(A), and Av=(mu^(-1)-1)v. Hence each limiting range lies in H_pp(A).

Crucially, fixed-k convergence by itself does not imply completeness. Let f_m be an orthonormal basis of H. If the birth projection P_n^n approximates all f_m in an increasing exhaustive finite probe family F_n with error eta_n -> 0 and ||P^n-P_n^n|| <= sum_(j>=n)e_j -> 0, then for every fixed f_m, dist(f_m,H_pp(A)) <= eta_n+sum_(j>=n)e_j -> 0. Since H_pp(A) is closed, every f_m lies in it. This proves H_pp(A)=H and independently excludes both H_ac and H_sc. The use of diagonal n=k is valid because the uniform tail estimate depends on n alone and applies to every k<=n, including the newly born k=n.

## Application to the candidate

For a finite connected partial tower O_n and next disjoint cube, the disconnected Dirichlet operator is a direct sum on a common L2 space. Protect the entire finite collection of eigenvalues in P_n^n. For each protected lambda, cube resonance occurs only at widths a=pi*sqrt(sum m_i^2)/(2*sqrt(lambda)). In the bounded candidate interval (a_n+1,a_n+2), only finitely many integer multi-indices can yield such a resonance. A nonresonant width therefore exists; this is stronger than simply invoking countability.

Assuming finite-window norm-resolvent convergence, isolated full cluster projections converge in operator norm, including all multiplicities. For the finitely many protected families at stage n, select one sufficiently small positive aperture to meet every requested operator-norm bound. A cluster may split internally, but protecting the full spectral projection and transporting sums of full clusters preserves rank and nesting. The next birth cutoff can include all previously protected eigenvalues and approximate finitely many probes because the finite-domain resolvent is compact.

The L2 common-space identification is exact modulo Lebesgue-null interface faces. The aperture cubes add no positive measure outside the adjacent large cubes when aperture < min(adjacent half-widths). Hence the countable cube sine bases form a basis of the final H. These sine probes need only be L2 vectors; their zero extensions need not lie in the final operator domain.

For O_n increasing to O, V_n=H_0^1(O_n) extended by zero are closed subspaces of V=H_0^1(O) in the norm induced by integral(|grad u|^2+|u|^2). Every compact subset of O lies in some O_N by increasing openness and compactness. Thus the union of V_n is dense in V. The zero-extended resolvents are the form-orthogonal Galerkin projections of Rf, proving strong convergence R_n -> R. There is no unjustified norm-resolvent assertion in the unbounded exhaustion.

## Initial judgment and unresolved checks

The above mechanism is internally sound on the stated hypotheses. I see no missing spectral completeness step, multiplicity problem, or hidden infinite-energy escape after injectivity of the genuine final resolvent is used. The external analytic input is the finite-window norm-resolvent convergence with fixed earlier windows. This remains explicitly conditional in this initial position pending primary-source verification. The original-source question must also permit inductive cube widths; that scope check is pending.

The Weyl sequence and zero-mode arguments still require final detailed checking. Counterexamples to weakened hypotheses (strong projection convergence, missing exhaustive probes, noninjective limits) are planned diagnostics; they cannot certify the PDE theorem. Current completion estimate for this spectral-family audit: 35%.

## Final verification addendum (2026-10-16T04:47:32.396112+00:00)

The pending checks in the initial position are complete. Primary-source pages were independently read and visually inspected; KL v2 explicitly gives later-center freedom and the fixed-earlier-windows norm-resolvent input. OWR printed pp.2077–2078 and K26 PDF p.16 support the target scope. The source PDFs and renders were deleted from this family’s temporary directory after their hashes and page scopes were retained. Detailed Weyl sequence, weak escape, no-zero-mode and spectral completeness checks appear in REPORT.md. Analytic counterexamples to weakened hypotheses appear in ADVERSARIAL_CHECKS.md; independent exact rational controls all passed. No inherited audit or verdict was consulted. Final spectral-family verdict: PASS, zero issues and no repairs. The established finite-window theorem is an explicit external dependency, and the separate geometry/capacity family remains independent. This is a verified existential statement, with no historical priority claim. Completion estimate: 100% for this family’s audit.
