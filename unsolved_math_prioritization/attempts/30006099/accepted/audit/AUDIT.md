# Independent mathematical audit: data-driven maximal averages

Problem 30006099 / OWR-14298803-003. Completed 2026-10-07.

## Decision and scope

**Accept the mathematics as partial progress after five substantive approaches, with one required public-metadata correction.** The broad source program is not solved by this packet. The fourth and fifth routes are dual descriptions of the same finite LP, not independent algorithms. This is an independent AI-assisted technical review, not external human peer review or a novelty certification.

The original MANIFEST.json has SHA-256 `a59fb26e06f8fc99027a248a1feaf80a196a2aa490d62c1ad0c4b7c3b5f9daa5`. All original files remain unchanged. CORRECTION.patch records every change in the separately prepared accepted packet: two corpus-match sentences and the consequent SOURCE_METADATA.json byte count/hash in its manifest. The corrected manifest SHA-256 is `19010cb1135f53d157d62882decb37cf9b8ca488a58b637406a5f6a53664f9c2`. RESULTS.md, all proofs, the approach ledger, both executable verifiers, and recorded mathematical checks are unchanged.

The correction is necessary: the submitted metadata claims a target record in research_results.json, but independent inspection of the complete file finds neither target identifier anywhere. The complete problems.json contains exactly one target record. Both submitted dataset sizes and hashes were correct. CORPUS_VERIFICATION.json gives the precise public match results without dataset content.

The reviewer read all of RESULTS.md and both verifiers; independently checked every mathematical route; replayed the tests normally and under Python optimization; added independent symbolic/rational and integrity controls; inspected relevant primary-source passages and the rendered OWR page 3292; and rehashed six source PDFs and both complete datasets. No source PDFs, extracted scholarly text, dataset contents, personal information, or private coordination records are part of this report or the acceptance artifacts. Literature inspection was bounded and is not an exhaustive priority search. Source hashes bind inspected bytes, not publisher-signed authenticity certificates.

## 1. Analytic obstruction and actual snapshots

For f(x)=-x/(1+x²), f'(x)=(x²-1)/(1+x²)² is bounded. The field is globally Lipschitz and bounded, and [-1,1] is forward invariant. Nonzero solutions move monotonically toward zero. Along a positive solution, log(x)+x²/2 has derivative -1; this also verifies that [-1,1] absorbs every bounded initial set in uniformly finite time. Since x(t)² tends to zero, its Cesàro mean tends to zero and beta=0.

The exact certificate is

    L(x²)=-2x²/(1+x²),
    x²+L(x²)=x²(x²-1)/(1+x²)<=0.

Every exact auxiliary residual is zero at the equilibrium, so the exact degree-two optimum is exactly zero. The sole invariant probability is the point mass at zero: invariance implies integral L(x²)=0, while that integrand is strictly negative away from zero.

With r=3-2sqrt(2), the Poisson-kernel expansion of 1/(1+x²) gives the stated Chebyshev coefficients. Hence, with a=floor(m/2),

    q_m=-2+sqrt(2)+2sqrt(2) sum_{j=1}^a (-r)^j T_{2j}.

Each summand satisfies (-r)^j T_{2j}(x)<=r^j, with simultaneous equality at x=0. Summing gives

    max q_m=q_m(0)=-delta_m,
    delta_m=2sqrt(2)r^(a+1)/(1-r)>0.

The omitted absolute coefficient sum is delta_m. It bounds the uniform projection error and is attained at zero. Thus normalization, strict negativity, odd/even indexing, and the all-finite-degree claim are correct. For c>=0, max(x²+cq_m)<=1-c delta_m, proving the unbounded-below infimum. Enlarging an auxiliary space already containing x² cannot remove this direction.

Snapshot transfer is genuine EDMD: full sample rank and inclusion of the auxiliary dictionary in the output span make snapshot regression followed by subtraction/division identical to regression of the difference quotient. Independently,

    L²(x²)=4x²/(1+x²)³,
    16/27-4u/(1+u)³=4(u+4)(2u-1)²/[27(1+u)³]>=0

for u=x² in [0,1]. The norm 16/27 is correct, and the looser time-remainder bound tau/2 suffices. The conservative Chebyshev projection norm 1+2m gives population error at most delta_m/8 at tau_m=delta_m/[4(1+2m)]. For fixed m,tau, the strong law and inversion continuity give uniform sample-regression convergence. Atomless sites are almost surely distinct, yielding polynomial evaluation rank once N>=m+1. Eventual sample error below delta_m/8 preserves the derivative bound -3delta_m/4 everywhere.

The diagonal choice is valid: deterministic increasing N_m can make failure probabilities at most 2^(-m), and Borel-Cantelli needs no independence between stages. The approximate selected derivatives converge uniformly while optimized values are eventually -infinity.

The stated limit-order qualifications are essential and correct. This is a specified fixed-output-degree regime and a failing joint diagonal, not a proof that every iterated order fails. Optimization over unbounded coefficients cannot be exchanged with fixed-observable convergence. The point-mass invariant measure fails the prior nonalgebraic-support/strict-feasibility hypothesis, so no contradiction with the conditional source theorem is claimed.

## 2. Weighted error penalties

For each fixed c, the exact and fitted residuals differ in sup norm by at most sum |c_i|epsilon_i. Adding that penalty dominates the exact auxiliary objective, proving beta<=B; c=0 proves B<=max g. No unrestricted optimizer or bound on its coefficients is assumed.

On an l1 ball of radius R, the perturbation is uniformly at most R epsilon. Taking infima in both directions proves the absolute value estimate and the certified chain in equation (5), including its final factor 2.

The consistency quantifiers are correct: choose one near-optimal exact auxiliary function; approximate it in C1 by one finite dictionary element; then keep its finitely many coefficients fixed as stage errors vanish. Bounded f controls the generator error from C1 approximation. Coordinatewise error convergence suffices for that fixed finite sum. This does not require bounded optimizer sequences or uniform accuracy of every newly added coordinate.

The separate ball condition R_n max_i epsilon_{i,n}->0 is sufficient and properly distinguished. Numerical global maximization and SOS approximations still need separate certified error budgets. This route therefore establishes a robust replacement under explicit uniform-error hypotheses, not unconditional convergence of the original unregularized problem.

## 3. Regression-to-uniform-error estimate

The Hoeffding constants in Theorem 3 are correct. Gram entries lie in [-B²,B²] and response entries in [-BD,BD]. The selected thresholds give failure probabilities alpha/(2p²) and alpha/(2pk) per entry, so the union probability is at most alpha. Independence is required across sites, not among entries or observables.

The bounds ||G_N-G||_2<=p t_G and p t_G<=lambda/2 imply ||G_N^(-1)||_2<=2/lambda. Also ||b_i||_2<=sqrt(p)BD, ||G^(-1)b_i||_2<=sqrt(p)BD/lambda, and ||psi(x)||_2<=sqrt(p)B. Substitution in

    a_N-a=G_N^(-1)[(b_N-b)-(G_N-G)a]

gives precisely equation (6). The population projection norm is bounded by Lambda=pB²/lambda. Splitting Ph_i-Lphi_i into the time-discretization term and best-approximation term, using Pw=w, yields Lambda tau M_i/2 and (1+Lambda)E_m exactly as in equation (7).

Known response bounds, exact sites/endpoints, iid sampling, span inclusion, and Gram conditioning are genuine inputs. Growing Lambda or declining lambda cannot be ignored in a diagonal argument. Summable stage failure budgets give eventual almost-sure validity; fixed-stage probabilities alone do not give simultaneous validity for infinitely many stages. Predictor noise is excluded. The statement is a correct sufficient estimate and does not claim a universal optimized-value rate.

## 4. Coverage-based finite LP

For every x, a nearest grid site incurs observable error at most omega_g(h) and generator/data error at most e_i=ell_i h+tau M_i/2+zeta_i. The LP objective therefore bounds the exact auxiliary residual globally and hence beta. Its infimum is finite because beta bounds it below and the zero coefficient vector supplies a finite feasible value. Nonnegative splitting c_i=c_i^+-c_i^- preserves the infimum, even when penalties vanish.

Equation (8) correctly pays a_i once to replace sampled responses by exact derivatives and once in the certified margin, giving 2a_i+ell_i h. Fixed-certificate approximation proves consistency without convergence or boundedness of fitted coefficients.

The regularity estimates ell_i=K G_i+F H_i and M_i=F ell_i follow by differentiating f·grad phi_i on the stipulated convex neighborhood. Endpoint-observable error nu_i gives zeta_i=nu_i/tau; shrinking tau at fixed noise does not establish consistency.

Equation (9) is a correct missing-ball union bound on an r/2-net. If every net ball contains a sample, the triangle inequality gives fill distance at most r. Full support and compactness give eventual coverage at every fixed radius almost surely; a countable sequence of radii then yields h_N->0. Supplied regularity and coverage information remain necessary assumptions and are not learned automatically from arbitrary trajectory data.

## 5. Primal compactness and duality

Theorem 5 works without strict feasibility. A nearest-site map with deterministic tie-breaking is Borel measurable. Pushing an invariant measure onto the grid yields probability weights with moment residual at most e_i. Pushing a maximizing invariant measure yields objective at least beta, including omega_g(h). Each finite feasible set is a nonempty closed subset of a simplex, so its maximum exists.

Compactness of X yields weakly convergent subsequences of discrete maximizing measures. For each fixed test,

    |integral Lphi_i dnu_n|<=e_{i,n}+a_{i,n}->0.

Since Lphi_i is continuous, weak convergence passes this relation to the limit. C1 density and bounded f extend it to every C1 test. For fixed t, the semigroup identity gives

    d/dt integral psi(Phi_t x) dnu
      =integral L(psi composed with Phi_t) dnu=0.

A C1 neighborhood extension exists for each fixed finite time interval by local flow theory and compactness; it also supplies uniform domination for differentiating. Smooth restrictions, including polynomials, are dense in C(X), so the resulting identity establishes invariance for continuous tests. Continuity of g and omega_g(h_n)->0 then bound every subsequential limiting objective by beta. Combined with the finite-stage inequality Q_n>=beta, this proves convergence. Uniqueness of the limiting measure is neither asserted nor needed.

For finite LP duality, the two moment inequalities have nonnegative multipliers whose difference is c_i and whose minimum sum is |c_i|. The normalization constraint supplies the free variable t, leaving exactly the inequalities t>=g(z_j)+sum c_i d_ij. Both LPs are feasible and finite, so ordinary finite-dimensional strong duality applies without a Slater condition. Thus route 5 supplies an independent compactness proof but the same numerical relaxation as route 4.

The final information-loss example is also correct. The zero trajectory is identical for -x and -x(1-x), whereas the second system has a fixed point at one with g=x average one and the first has maximal average zero. Even unlimited noiseless observation of that one trajectory cannot distinguish their maximal averages. This is a coverage obstruction, not a specifically non-polynomial one.

## Primary-source boundary checks

- OWR printed pp. 3291–3293 define the snapshot estimator and ask about non-polynomial optimized-value convergence and quantitative errors. Rendered p. 3292 displays N first, output degree second, and sampling step last. The EMS page confirms 19 May 2025 publication. [Report](https://ems.press/content/serial-article-files/50766); [publication record](https://ems.press/journals/owr/articles/14298803).
- The auxiliary-function paper distinguishes population projection, time-step, and dictionary limits. Its Theorems 4.1–4.4 need the applicable domain/span, sampling, density, or exact-representation hypotheses. The packet does not contradict these fixed-observable results. [Bramburger–Fantuzzi v4](https://arxiv.org/abs/2303.01483v4).
- The invariant-measure paper's main Section 4 theorem concerns polynomial discrete-time maps, compact semialgebraic structure, rank/support hypotheses, and strict feasibility. Section 4.4 already discusses perturbation instability. The packet uses it for this boundary and prior credit, not as a ready-made non-polynomial continuous-time theorem. [Bramburger–Fantuzzi v2](https://arxiv.org/abs/2308.15318v2).
- The auxiliary/invariant-measure identity is established prior work, especially Section 5 and equations (17a)–(17d) of Tobasco–Goluskin–Doering. It is properly credited and excluded from the five author approaches. [Version 3](https://arxiv.org/abs/1705.07096v3).
- The later operator-approximation sources have the stated titles and versions in the inspected PDFs. The September 2026 arXiv page independently confirms authors, title and date. These sources support credit for operator approximation theory, not a conclusion that this packet settles all optimized-value questions. [Llamazares-Elias et al. v3](https://arxiv.org/abs/2405.00539v3); [Fassler et al. v1](https://arxiv.org/abs/2609.31817v1).

## Tests and integrity

The author's CHECKS.json reproduced byte-for-byte in normal and optimized Python. Its 367 positive checks consist of 98 symbolic checks, 17 floating quadrature checks, 12 floating snapshot checks, 40 floating LP/grid checks, and 200 exact-rational sensitivity comparisons. Six false controls were rejected. Those rational tests minimize over a finite coefficient list, so they illustrate rather than prove the continuous-ball result. Floating LP and quadrature checks are not exact global certificates.

The separate independent verifier adds differentiation, the rational factorization of the second-generator maximum, an implicit flow-law identity, 30 projected-tail identities, both Hoeffding union-budget identities, and 210 exact-rational primal/dual witness pairs. Normal and optimized runs agree. These finite controls support the analytic audit; they do not prove its infinite-family or compactness results.

In each Python mode the frozen manifest checker accepted the clean packet and rejected ten mutations: changed bytes, same-size changed bytes, missing file, extra file, file symlink, directory symlink, symlinked manifest, duplicate manifest path, parent-traversal path, and absolute path. That is 22 invocations with 20 expected rejections. The separately recorded manifest hash is the external trust anchor. A self-contained checker cannot detect coordinated replacement of itself and its manifest, and no such security claim is made.

## Acceptance conditions and remaining gaps

Use only the explicitly corrected metadata copy, or apply CORRECTION.patch and verify the resulting manifest hash. Preserve the original and this distinction. Preserve **partial progress, 5/5 approaches**. Do not claim every non-polynomial EDMD scheme fails, every limit ordering fails, strict-feasibility theory was disproved, or the modified LP needs no global information.

The original general program is unresolved by this work: necessary-and-sufficient conditions and useful rates for unmodified optimized EDMD; quantitative approximation of near-optimal auxiliary certificates; correlated-data concentration; noisy predictors; certified SOS truncation errors; and infinite-dimensional states remain outside the established results. The accepted contribution is the explicit all-finite-degree obstruction with an exact-snapshot realization and rigorously qualified sufficient convergence conditions for certified alternatives.
