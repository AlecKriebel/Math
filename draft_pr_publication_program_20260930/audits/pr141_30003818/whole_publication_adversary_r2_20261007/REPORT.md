# PR141 round 2: fresh independent whole-publication adversarial review

**Verdict: no mandatory mathematical, attribution, reproducibility, or publication-package defect found in the exact frozen package.** This is an independent AI review, not conventional human peer review or a provider/publication/native-integration authorization. Review assignment completion estimate: 100%; overall program completion is not inferred.

Actual report writer PID: 48222. UTC: 2026-10-07T21:49:08.666382+00:00.

I formed the mathematical conclusions from the frozen manuscript and primary mathematical sources before reading the packaged earlier reviewers' reports. I did not consult round 1's report or verdict. Later I inspected the initial mathematical and priority audits as historical contents of the package, without using their verdicts as evidence for my decision.

## Authority and exact scope

The authority is `publication_package_v1/PACKAGE_MANIFEST.json`, 10,275 bytes, mode 0644, SHA256 `05d50f2a24abf580e90bf2bc61e5a0367f03d8edc0fd9fa395a36ceb476372d2`. Initial authentication read every full body and mode, checked the exact closed inventory of 54 declared files plus the self-excluded manifest and explicitly excluded compiler log, and safely extracted all 52 support ZIP members. No duplicate name, absolute/traversal path, directory member, or symlink was admitted. Every extracted byte and mode equals its package counterpart.

PDF: 88,322 bytes, SHA256 `acf262d707c9faa466f30a86a8347ae7cbff0ad5a48fbb38893e460c0e3ec2e5`. TeX: 18,848 bytes, SHA256 `f5a71902a30c386de29a372427d928273ea50e3ff833bd8b6e74ce5f34e9fd9f`. ZIP: 141,902 bytes, SHA256 `8835f8ea3be4e25eb25b7663a2da0d56ee4afbc3dbe60843b02436a66dc237ab`.

I rendered that exact PDF locally at 90 dpi and visually inspected all six pages. The title, equations, theorem, proof, disclosures, and references are readable, with no clipping or overlap observed. The standalone TeX and PDF text/metadata are consistent. The root-level historical preview images have an older title; the exact frozen PDF was used for this review. Parent clarification identifies the v2 subfolder as the previously inspected current render. This historical preview distinction is not a defect in the upload pair.

The original [problem](https://ems.press/content/serial-article-files/46745), PDF page 72 / printed 1452, requests the complete vector law for independent Brownian particles on the circle with uniform-random or equidistant starts. It imposes no density, asymptotic, or efficiency format. The [publisher record](https://ems.press/journals/owr/articles/16164) independently confirms the 2018 volume and publication on 2019-04-12. The package treats particles as continuing independently through encounters and visited territory, on a circle of mass one with common generator one-half the second derivative. It supplies every finite k >= 1, arbitrary fixed distinct labeled seeds, and both original starting schemes.

## Independent mathematical falsification attempts

### Exit kernels and signs

Let H be the killed interval kernel and let v0(beta)=1-beta/ell. The survival-and-eventual-left-exit probability is F0(t)=integral H(t;alpha,beta)v0(beta) d beta. The heat equation gives

    F0'(t) = (1/2) integral H_beta_beta v0
            = -H_beta(t;alpha,0)/2.

The two integrations by parts use H=0 at both endpoints. Thus f0=-F0' is nonnegative, and differentiating the sine kernel gives exactly pi/ell^2 times n sin(n*pi*alpha/ell). With v1(beta)=beta/ell, the right flux is -H_beta(t;alpha,ell)/2 and its sign factor is (-1)^(n+1). The eigenvalue n^2*pi^2/(2*ell^2), both boundary signs, and the factor of two therefore agree with the stated Brownian convention.

For an interior start, continuity precludes a zero-time exit atom. Applying B_t^2-t at bounded stopped times bounds E(tau wedge t), proving finite interval exit; bounded optional stopping for the coordinate gives left/right masses 1-alpha/ell and alpha/ell. As t tends to infinity the survival event vanishes. These facts prove normalization of the *summed* kernels. They do not rely on termwise improper integration of signed Fourier summands. Positive-time derivatives converge locally uniformly by Gaussian eigenvalue decay. The printed warning against an unjustified near-zero-time Fourier interchange is appropriate.

I checked Lalley's primary Exercise 6(A)-(C) for the killed unit-interval sine expansion and the actual Mörters--Peres Theorem 2.16 and its proof, printed 43-44 (PDF 53-54), for finite stopping times. These are the correct classical dependencies. The two exit Laplace transforms solve u''/2=su with the stated boundary data. A singleton circle target has both lifted endpoints identified with the same point; summing f0+f1 is necessary and present.

### Target orders and cumulative clocks

Before reaching a still-unvisited finite target set, the circle walker is in one complementary arc. A lift is ordinary interval Brownian motion until its exit. Only that arc's endpoints can be the next query target. Integer winding offsets leave the kernel unchanged. Removing the just-hit query from the auxiliary target set makes it traversable again; the physical particle is never killed or coalesced. The last-stage singleton is correctly covered.

The next hit is a finite stopping time. On each finite target-order prefix, the remaining set and current point are deterministic. Strong Markov iteration therefore gives the displayed product as the **joint order-and-increment subdensity**, rather than a product formed by conditioning on a future order event. Positive separation of distinct queries makes successive increments strictly positive. Iterated normalization over all possible next targets gives total order mass one; impossible orders receive a zero factor.

Different walkers' full increment vectors are independent. Within one walker, query hitting times remain dependent and are reconstructed by cumulative sums through that query's position in its own order. The strict ownership inequalities compare those cumulative sums. An equality between different walker rows is a proper hyperplane, so its product-density measure is zero. Equivalently, fixed-query singleton hitting times are atomless and independent across walkers. The owner cones partition all admissible increment vectors up to these boundaries. No unknown conditional Brownian law or additional winding state survives.

### Measurability, spatial diagonals, and seed laws

For continuous paths, hitting by t is equivalent to zero distance from the compact range on [0,t]. That distance is a countable infimum over rational times plus t, so (path,x) -> T_i(x) is measurable. The least-index minimizer and its spatial integral are consequently measurable. For each fixed nonseed x, all hitting times are finite and inter-walker ties have zero probability. Fubini yields an almost surely spatially null exceptional set; no simultaneous absence of all uncountably many ties is claimed.

Uniform seeds can be coupled as W_i(t)=p_i+B_i(t) modulo 1 with independent canonical increments. This map is jointly measurable in seed and increment path. Alternatively, the explicitly sorted-arc kernel definitions are Borel off finitely many diagonals. Thus the seed integrals are legitimate; their measurability is not inferred from uniform bounds alone. Coincident seeds, repeated query points, and query/seed coincidences form null diagonals in the appropriate product Lebesgue spaces. Arbitrary bounded modifications on those completed-measure null sets have no effect. Approaching such diagonals may make individual kernels singular, but summed ownership probabilities remain bounded by one, which is the integrability bound actually used.

### Complete deterministic law and uniqueness

For each finite m, the coefficient uses only explicit scalar kernels, finite permutations and label sums, and finite-dimensional Lebesgue integrals over displayed integer-coefficient linear inequalities. The kernels are summed at positive times before integration. Normalization proves their nonnegative combined integrals are finite. The resulting coefficient contains no unknown Brownian functional, implicit potential kernel, or unsolved integral equation. This is a deterministic transform characterization of the full requested probability measure, although it can be computationally enormous.

Let Z=sum(theta_i L_i). The measurable partition gives 0 <= Z <= theta_* and Tonelli gives E[Z^m]=M_m. Absolute domination by exp(theta_*) justifies the outer exponential expansion. Taylor's remainder for exp(-z) on z >= 0 is at most z^(N+1)/(N+1)!, since its relevant derivative has absolute value at most one. The claimed factorial bound therefore needs no omitted exponential multiplier. It controls the outer series, not kernel truncation or coefficient quadrature.

For |nu|=m, the coefficient of theta^nu in M_m is

    m! / product(nu_i!) * E[product(L_i^nu_i)].

Knowing the homogeneous polynomials on the positive orthant determines all these coefficients. The coordinate polynomial algebra separates points of the compact simplex, so Stone--Weierstrass and uniqueness against continuous test functions determine the entire joint Borel probability measure. Separate marginal determinacy is not substituted for joint determinacy. The uniform bounds in distinct p permit averaging over independent uniform labeled seeds.

I checked k=1 (exp(-theta_1)), m=0, all-zero and partially-zero theta, all-equal theta (exp(-t)), singleton remaining targets, irregular and nearly coincident distinct seeds/queries, impossible target orders, and common circumference/diffusivity scaling. Equidistant seeds have cyclic/dihedral symmetry rather than arbitrary label permutations; independent uniform labels are exchangeable. Circularly ordered labels use a different seed law, as the paper acknowledges. Unequal particle diffusivities, infinite k, compact named densities, certified inner quadrature, and a finite-chain Brownian limit are not claimed.

## Prior work, attribution, and bounded priority

I independently checked relevant primary statements rather than accepting exclusion from titles. [Miller](https://arxiv.org/html/1003.2168v1), Theorems 1.1/1.3, studies two-walker final painting correlations and volume variance in transient graph families. Its hypotheses and output do not directly yield this finite-k Brownian circle law. [Chatterjee--Nabahi--Terlov](https://arxiv.org/html/2608.21312v1), Theorem 1.1, estimates expected discrete-cycle interface size. [Baccara](https://arxiv.org/html/2607.02406v1), Section 6 Proposition 8, does give **joint** convergence to a real-line finite-horizon Brownian hitting-time functional. The package correctly does not downgrade it to a marginal result, and distinguishes its remaining functional definition. [Si](https://arxiv.org/html/2608.24837v1), Section 7 Theorem 7.1, addresses a target-integrated expected strategic payoff for two reflected interval Brownian motions, rather than the full random territory vector.

Fitzsimmons--Pitman's primary pp.117-120 supply Kac moments/transforms for temporal additive functionals through a killed-process potential kernel. Enlarging a state to a history field would still require that kernel, so this generic formula is not itself the package's deterministic finite-query coefficients. Régnier et al.'s primary pp.064104-1--4, especially equations 8-11, describe multitime single-walker spans via exit increments. A span is not the location-wise cross-walker competition observable. Both classical precedents are credited.

The [Gomes publisher indexed abstract](https://www.sciencedirect.com/science/article/pii/0378437195004246) identifies two-walker periodic coloring, a one-point scaling probability, and simulated interfaces. Direct opening again returned 403. The UPenn Dicker index also returned 403 in this review. Neither fulltext is claimed to have been excluded. The recorded registry 403 failures likewise do not become registry-wide clearance. The package's query inventories contain exactly 74 and 23 documented queries; they are bounded search records, not raw exhaustive search exports.

Fresh generic-method searches additionally inspected [Grebenkov](https://arxiv.org/html/2008.12986v1), Sections II and IV, on single reflected-particle boundary local times and associated reaction/threshold passage laws. This is a different observable and does not directly provide the circle competition coefficients. A Chevalier et al.2011 multi-target first-passage method was identified in a [primary author index](https://www.lptmc.jussieu.fr/files/Benichou/Publications.pdf), but its publisher is robots-blocked; no complete fulltext exclusion is claimed. No concrete unread general target-resolution theorem was identified by these additional searches. The independent query/inspection inventory is retained separately.

The manuscript and metadata credit the painting model and standard kernel/Markov/moment methods, describe the contribution narrowly, disclose unread texts and registry access failures, and make no absolute priority or independent-discovery claim. That wording matches the evidence. The initial audit requests are historical; their required attribution repairs are present in the current manuscript. No substantiated prior full-resolution counterexample was found. Historical priority must reopen if such a theorem is later identified.

## Reproduction and publication package

I read all five portable diagnostic sources, their full originals and exact derivative diffs, the source-custody record, real baselines, source manifest, runner, and extracted real guard controls. I reproduced directly from the authenticated support archive into a new directory outside the source tree, using the specified existing Python interpreters and library versions, without installation. The runner completed 22 children. I then independently read all actual stdout/stderr bytes, verified their hashes and sizes, compared complete scientific objects against the actual original baseline bodies and specification objects, recomputed count relations, and independently probed every child's process group as absent. All children exited zero and were reaped; every real guard accepted True and rejected False normally and under -O.

The five actual counts are 8,520 author diagnostics; 46,056 earlier diagnostics; 11,777 joint-clock checks including 2,052 independently enumerated weighted CTMC configurations; 61 global-race checks; and 180 scalar cases plus 120 Laplace identities. These distinct counts are not a proof score. The finite checks test the stated identities; the scalar comparisons at 105 digits attain maximum scaled error about 2.34e-101 and conditional relative error about 5.44e-73. Their scope remains finite diagnostics with no certified truncation, quadrature, or numerical-error theorem. The mathematical proof stands separately.

The source-history changes are exactly disclosed paths/output/PID changes plus the optimization-safe author guard and bounded runner cleanup. The original 20-file archive matches its full-body/mode manifest and computed Git blob addresses; the submitted verifier is byte-identical to its historical stored copy. The original head was not in either local Git object database, so read-only object lookup could not independently reconstruct the head's tree; no ref/index/network Git mutation was attempted. This does not alter the verified archived-file identity. The historical proof SHA256 is `f5445282b2044937620acd7f273e9ac21ac0dae0b42edd1050ced91e2a29fddf`.

`zenodo-deposit.json.metadata` equals `metadata.json` exactly as an object, and the upload list is exactly PDF plus support ZIP. The authored-material CC BY 4.0 statement distinguishes cited third-party rights. No full third-party paper, private cache, or screenshot is in the archive. Extensive AI involvement, unrefereed status, and absence of conventional human peer review are conspicuous and consistent. Dated preparation records with approval flags false are labeled historical; this fresh review is separate. I found no upload-metadata or source/PDF/support inconsistency.

Mandatory corrections: none. Optional refinements are not required for the stated result. This review performs no publication, DOI, comment, tracker, acceptance, merge, native integration, or provider action. No external person was contacted. Only this new review directory was written. The exact package is reauthenticated at final sealing below; the root owns subsequent gates and authorized decisions.
