# Independent audit: shy reflected-Brownian rigidity partials

## Disposition

Accept the restricted mathematical content after the two local clarifications in `REPORT_CORRECTION.patch`; use `REPORT_CORRECTED.md` as the corrected report. The original frozen report and every original packet byte remain unchanged. There is no complete solution and no novelty claim. The correct mathematical disposition remains **unresolved, exhausted 5/5**.

The substantive correction concerns the final paragraph of Section 7: in the stated regular normal-reflection setting, a singular local-time measure cannot cancel a time-absolutely-continuous covariance drift in an identically constant-distance equation. This also gives a direct global version of the existing constant-distance lemma across boundary visits. That corollary is an audit correction within the fifth existing approach, not a sixth search route. A technical clarification makes joint measurability explicit in the abstract occupation-measure lemma.

This audit contains newly authored reasoning, tests, and public bibliographic metadata. It includes no third-party source bodies, source PDFs, dataset contents, or private coordination material. It does not authorize publication.

## 1. Exact target and coupling hypotheses

The live author page was independently checked. Problem 7 asks an existential implication for a bounded connected Euclidean open set in dimension at least two: a separated reflected-Brownian pair is to imply the existence of another separated pair related by one deterministic, time-independent function. It does not say that the original pair itself must be a function coupling. It does not explicitly impose common-filtration Brownian driving noises, a joint Markov property, a Feller property, a regular boundary, a Borel or smooth function, or a fixed starting distribution. The report preserves these omissions. [Burdzy's author-maintained problem page](https://sites.math.washington.edu/~burdzy/open_mathjax.php).

For continuous paths, rational-time separation suffices to express permanent separation. A random strictly positive minimum distance on an event of positive probability gives a deterministic positive separation level on some positive-probability subevent by a countable union. This operation does not condition the processes and therefore does not change their laws. The source's positive-probability condition is not replaced by an almost-sure one.

The report's analytic lemmas impose ordinary normal reflection on bounded connected C2 domains. This supplies the Skorokhod finite-variation reflection term, the regular Neumann semigroup, full interior transition support, and convergence to normalized volume. Those hypotheses belong to the partial lemmas, not to a claimed solution in the broader source scope. Arbitrary initial laws are allowed within the ordinary reflected-Brownian marginal laws; stationarity is not silently assumed.

The early *Shy couplings* files and Kendall's subsequent paper use stronger coupling conventions than merely specifying two marginal path laws. In particular, Kendall's definition requires the marginal transition law after conditioning on the joint past, but does not require the pair itself to be Markov. The compact-Feller lemma expressly uses the yet narrower joint-Markov class with the right marginal transition kernels from every pair. These distinctions are mathematically important. [Benjamini–Burdzy–Chen preprint](https://arxiv.org/abs/math/0509458), [Kendall](https://arxiv.org/abs/0809.4682).

The CAT(0) paper's Theorems 1–2 require co-adaptedness and uniform exterior-sphere/interior-cone boundary conditions; its Section 5.4 explicitly distinguishes non-co-adapted couplings. Its symmetry conjecture cannot be substituted for the literal author-page question. The rubber-band paper also works in the co-adapted class and has boundary/domain hypotheses encoded in its CL class. The report does not misuse those nonexistence results as statements about every coupling with the same marginals. [CAT(0) paper, v4](https://arxiv.org/abs/1007.3199v4), [rubber-band paper](https://arxiv.org/abs/1207.0597).

## 2. C2 deterministic-map classification and centroid obstruction

Proposition 1 is correct with its stated C2-extension and C2-domain assumptions. Apply Ito to f(X). Its pathwise quadratic covariation is the time integral of Df Df^T along X, while the marginal path law of Y supplies identity quadratic covariation. Equality Y=f(X) identifies the two covariations without requiring Y's Brownian part to remain a martingale in X's filtration. This is a crucial correct choice of argument; treating that Brownian part as a common-filtration martingale without justification would be invalid.

For completeness, if F(x)=Df(x)Df(x)^T-I, then its entries vanish along X for almost every time, almost surely. Tonelli shows that for almost every positive time the integral of |F| against the marginal law is zero. Such a marginal has positive interior density even with a random starting law. Continuity of F forces F=0 at every interior point. Because the matrix is square, row orthogonality also gives column orthogonality.

Let A_abc be the inner product of the second derivative partial_a partial_b f with partial_c f. Mixed derivatives give symmetry in a,b; differentiating orthonormality gives antisymmetry in b,c. The six-step permutation chain returns A to its negative, so every coefficient vanishes. Since the first derivatives form a basis, every second derivative is zero. Connectedness gives one affine isometry Qx+b on all of D, not a collection of componentwise maps.

Both marginal supports at each positive time equal the closure of D. The image under a continuous affine isometry has support equal to the image of that closure. Consequently the isometry preserves the closure. A C2 domain is regular open, so it preserves D itself. No unproved assertion that an arbitrary continuous image commutes with taking interiors is needed; the map is already an ambient homeomorphism.

Proposition 2 is also correct. A fixed-point-free isometry on the compact closure has a positive minimum displacement. If it has a fixed point anywhere in the closure, recurrent visits to every relative neighborhood give arbitrarily small displacement. Boundary fixed points count: every such neighborhood has positive interior volume, and the regular Neumann kernel supplies eventual uniform positive hitting probability at spaced observations. Full support at one time alone would not imply repeated visits; the Markov/minorization argument supplies the missing infinite-horizon step.

The centroid corollary follows by change of variables under a volume-preserving affine isometry. The hypothesis that the centroid lies in the closure is essential. Annuli illustrate why it may fail. Conversely, a domain-preserving isometry carries inward normals and Brownian covariance correctly and produces a co-adapted reflected-Brownian pair. The smooth classification does not extract any function from an arbitrary shy joining and does not establish Borel-map rigidity.

## 3. Stationary separated joining

Proposition 4's main proof is sound. For a bounded continuous g and fixed h>0, the centered increment A_t=g(Z_(t+h))-P_hg(Z_t) has conditional mean zero at time t. If s is at least t+h, A_t is measurable at time s; the covariance with A_s vanishes by conditional expectation. The nonzero covariance region in the square [0,T]^2 has area at most 2hT, giving the stated upper bound 8h||g||²/T for the averaged second moment.

Along T=n², Chebyshev and Borel–Cantelli apply because the bounds are summable. Endpoint errors are at most 2h||g||/T. Compact-metric separability supplies a countable dense collection of test functions; positive rational h also form a countable set. Intersecting the resulting probability-one event with the positive-probability separation event is legitimate. Selecting a path there is not conditioning the semigroup or pretending that a conditioned process remains Brownian.

Compactness yields an occupation-measure subsequential limit. Closedness of K preserves its support. Feller continuity passes the weak-limit identity for P_hg, and strong continuity extends rational h to all nonnegative h. The marginal-kernel property and uniqueness of the marginal invariant law identify both marginals as m. Joint reversibility, ergodicity, and uniqueness of the joint invariant measure are not required.

The corrected statement explicitly assumes a jointly measurable process so the occupation integrals are well-defined. The continuous reflected-diffusion application satisfies this automatically. For that application an invariant measure supported on the closed separation set also gives a stationary separated pair: invariance gives separation at every rational time almost surely, and path continuity gives it at all times. This explains the reduction in the intended setting. It still does not imply that the invariant measure is supported on the graph of a function.

## 4. Finite-state purification obstruction

Proposition 5 is correct. The supplied three-state generator is symmetric, irreducible, and has distinct exit rates. The six-state off-diagonal joint generator has nonnegative jump rates and zero row sums. Testing it on the basis indicators of each coordinate gives the prescribed three-state generator for both coordinates. This generator identity yields the correct marginal semigroup conditional on the joint past, establishing co-adaptedness as well as the joint Markov property. The off-diagonal state space is closed and the discrete distance is always one.

The independent checker verifies exact invariant weights 1/6 on the joint states and 1/3 on both coordinate projections. It enumerates all 27 functions on three states. Exactly six preserve the uniform measure; they are the permutations. Of these, only the identity commutes with the marginal generator.

That finite enumeration agrees with the general proof. For any proposed function coupling, convergence of both marginal distributions to the uniform law forces uniform-measure preservation, hence a permutation. Every state has positive probability at positive time for this irreducible chain. Comparing the two-time transition law therefore forces generator conjugacy. Distinct diagonal entries rule out every nontrivial permutation. Thus no alternative function coupling of these chains can be shy, regardless of whether it is built from the original avoidance pair or from different starting laws.

This is a counterexample to an abstract finite-state purification principle. It is not a reflected-Brownian counterexample in a bounded Euclidean domain. Neither choosing an extreme invariant joining nor selecting partners from its support has been justified in the diffusion problem.

## 5. Borel-map Neumann energy statement

Proposition 6 is valid under its explicit Borel-map and normal-reflection hypotheses. Let mu_s and eta_s be the marginal laws. Both converge in total variation to m, and eta_s=f_*mu_s. Pushforward contracts total variation, so the triangle inequality forces f_*m=m. This does not require continuity or invertibility of f.

For bounded Borel h, the two-time correlation on either side is computed using the relevant coordinate's own Markov law. It does not require that either coordinate be Markov after conditioning on the other. Total-variation convergence passes the bounded measurable integrands to the stationary limit and yields equality of the two quadratic correlations. Measure preservation separately gives equality of squared L2 norms.

The standard Neumann spectral characterization makes the last step precise. If -L has eigenvalues lambda_k and u has coefficients u_k in its orthonormal eigenbasis, then

    (||u||² - <u,P_tu>)/t = sum_k ((1-exp(-t lambda_k))/t) |u_k|².

As t decreases to zero the summands increase to lambda_k |u_k|². The finite limit is exactly the Neumann Dirichlet-form domain condition and energy. Applying this to u=h composed with f proves H1 membership and equality of energies. Any bounded Borel representative of h can be used; because f_*m=m, changing that representative on an m-null set does not change the composition in L2(m).

Taking coordinate functions and polarizing gives the integrated gradient inner products delta_ij with the stated factor 1/2 in the form. These integrated identities do not by themselves give pointwise orthogonality, injectivity, or smoothness. The report correctly stops before such claims and does not invoke a manifold order-isomorphism theorem without its relevant hypotheses. [Diffusion determines the manifold](https://arxiv.org/abs/0806.0437) was checked as a bibliographic scope reference, not as a theorem that resolves this setting.

## 6. Product example and graph-limit caveat

The stored v4 PDF's page 40 was visually inspected independently. Its displayed pair uses one common interval coordinate. Therefore the pair is related by the rigid orthogonal map with diagonal entries (-1,-1,1). The displayed example, as printed, does not prove its asserted non-rigidity. No claim about the authors' intended correction or the correctness of the paper's other proofs is inferred from that local defect. [CAT(0) electronic reprint](https://arxiv.org/pdf/1007.3199v4).

The report's repair uses independent interval Brownian coordinates V and W, also independent of the annular coordinate U. Each pair (U,V) and (-U,W) has the product Neumann law. The joint construction is Markov and co-adapted with deterministic starts. At each positive time W has a continuous distribution and is independent of (U,V); a conditional point mass that a Borel functional relation would require is impossible. The annular coordinate guarantees distance at least twice the inner radius. The product domain has edges and is not C2, but product Neumann reflection is well-defined; the report does not apply its C2 rigidity theorem to this example.

The same domain admits the common-interval rigid pair. Thus the repair proves only that a particular shy coupling need not be a function coupling. It is no counterexample to the source's existence of some function coupling. The distinction is preserved throughout the report.

Likewise, a thin-domain approximation or a deterministic evasion strategy does not supply exact Brownian marginal laws, infinite-horizon survival at one positive width, or exclusion of all deterministic functions. The elementary geometric-killing example correctly demonstrates the order-of-limits obstruction. None of these observations is a new sixth approach.

## 7. Covariance identity and correction

With the report's convention dY=J dB+K dC and JJ^T+KK^T=I, the difference covariance is

    Sigma=(I-J)(I-J)^T+KK^T=2I-J-J^T.

The noise, trace, and two reflection signs in d|X-Y|² are correct. On an interior stochastic interval with an almost-sure constant-distance semimartingale identity, uniqueness of decomposition forces the finite-variation trace term to vanish. Since its trace is ||I-J||_F²+||K||_F², this forces synchrony. Radial zero variance alone is strictly weaker: the diagonal example has radial variance zero but full covariance trace four. This is checked exactly.

The original subsequent sentence about local times needs qualification. In a bounded C2 domain, every positive-time marginal assigns zero mass to the boundary; Tonelli therefore shows that boundary-time sets have Lebesgue measure zero almost surely. Reflection local times are carried by those sets. After a constant-distance identity forces the martingale part to vanish, the Lebesgue decomposition of its finite-variation part prevents the singular reflection measures from canceling the absolutely continuous trace term. The same synchrony conclusion therefore holds even across boundary visits, on the intervals specified in the corrected corollary.

For nonconstant distance, cumulative contributions may offset across a finite interval; there is no claim of pointwise measure cancellation. A lower bound on distance does not imply constant distance, and conditioning on a survival event need not preserve Brownian laws. The correction improves the existing lemma but does not advance the unresolved existential step.

## 8. Reproducibility and exact pins

The independent audit used genuine UID=EUID=1000. The original directory was mode 0555 and its eight files were mode 0444. No permission was relaxed and no frozen byte was changed.

Original externally supplied pins, independently rechecked before and after controls:

- MANIFEST.json: 2007d3d46ab4c0732c93b72c84c3aa7444ac0d7ac088c79aa2e7641eebe179f4
- replay_controls.py: aeb57481d9261e2bc38b846f9d96a20bd80f5dac71b9f067f8d5c5be9d8ed1fc

The original hardened driver passed in all three child interpreter modes with 27 rejected mutants per mode. The new independent checker does not import the original checker and uses separate generator-basis, exact Fraction, and all-function-enumeration checks. Its independent driver tested 29 mutants against both the new and original checkers in normal, -O, and -OO modes: 174 clean negative rejections and six valid-certificate acceptances. Existing-file and new-file write opens were denied in all three modes. Hostile current-directory modules and PYTHONPATH/PYTHONHOME values did not affect isolated subprocesses. Deliberately false external manifest and driver pins were rejected.

All seven downloaded public source files matched their recorded byte counts and SHA-256 values. The live author page and primary arXiv metadata were also checked; a live page-content check is not represented as a fresh byte-identical download. The large public dataset hashes were not independently recomputed in this audit and remain inherited metadata. Source-file hashes establish byte identity, not mathematical truth or worldwide completeness of literature search.

Exact tests substantiate only finite algebra and reproducibility. They cannot certify heat-kernel facts, Ito calculus, measure disintegration, the analytic proofs, novelty, or a complete solution of Problem 7. Those matters are addressed by the preceding mathematical review and the stated source limits.

## Final acceptance boundary

Retain Propositions 1–6, the original interior version of Proposition 7, the corrected boundary-spanning constant-distance corollary, and the finite-state/product warnings with their explicit hypotheses. Use the corrected report rather than the misleading unqualified boundary-compensation sentence. Do not claim that the original broad existential implication is proved or disproved. Keep the five-approach exhausted disposition unchanged.
