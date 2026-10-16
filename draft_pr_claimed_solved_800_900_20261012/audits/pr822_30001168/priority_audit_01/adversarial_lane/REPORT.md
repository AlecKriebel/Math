# Adversarial source-applicability report — PR822 / problem 30001168

Decision: **no earlier explicitly stated resolution of the exact heat-max claim was located in the inspected sources; the candidate's central cylinder mechanism is nevertheless a straightforward derived corollary of a classical published construction, together with an elementary round-sphere heat bound.** This is a material limit on any novelty language. Failure to find an explicit earlier statement does not establish novelty, worldwide priority, or present openness.

The audit is about applicability and priority inference. It accepts the separately reviewed finite-cylinder mathematical result as an input and does not replace its geometry or arithmetic audits. A three-dimensional counterexample negates the universal n >= 3 target; the n >= 4 restriction and the adjacent monotonicity record 30001169 remain outside that deduction.

## Exact target and falsification criteria

The official question is Morpurgo's Conjecture 1 in OWR 2009/06, §9 item (16), printed pp. 421–422. On the unit round S^n, put A = Δ + n(n−2)/4 and Y_W = W^(−1/2) A W^(−1/2), with smooth W > 0 and integral W^(n/2) = |S^n|. The target compares max over t > 0 of t^(n/2) Tr(exp(−tY_W)) with the corresponding round maximum. [Official primary source](https://ems.press/content/serial-article-files/46205).

An earlier theorem directly resolving this target must use this operator (or a verified unitary equivalent), this volume normalization, the smooth compact finite setting, a dimension allowed by the target, and the all-times round maximum. Merely sharing the phrase “conformal spectrum,” a fixed-index conclusion, a determinant, an inverse moment, or a CLR count functional is insufficient.

The accepted local audit proves a finite n = 3 example with heat value > 13/20, while the round heat expression is < 129/200 at every positive time (independently strengthened to 321/500). Those bounds are assumed for the priority comparison, with provenance in the separate [trace report](/Users/alec/Documents/Math/draft_pr_claimed_solved_800_900_20261012/audits/pr822_30001168/trace_audit_01/REPORT.md).

## Adverse novelty finding: the classical construction does supply the mechanism

Ammann–Jammes introduce smooth conformal metrics with a growing cylindrical neck in §3.2; their Example 1 identifies the Yamabe operator's cylinder spectral threshold (n−2)^2/4. The construction is already present in arXiv v1, submitted 3 August 2007, and the author-hosted text dated 8 December 2008; the chapter was published in 2011. Their Theorem 4.1 concerns fixed eigenvalue indices below the cylinder threshold. That theorem does not itself estimate O(L) heat mass, but **the underlying construction plus the ordinary variational principle does.** [Primary preprint and version history](https://arxiv.org/abs/0708.0529), [published chapter DOI](https://doi.org/10.1017/CBO9780511863219.002).

The following is an independent derivation, not a claim that A–J explicitly state the heat-max corollary.

1. Choose a smooth metric g_0 in the round S^3 conformal class that equals the Euclidean metric on a small coordinate ball. This is possible by multiplying the round metric by the reciprocal stereographic factor near the point and extending that positive smooth multiplier to the rest of S^3. The background metric need not be the round representative itself.
2. On the Euclidean annulus e^(−L) <= r <= r_0, use the A–J multiplier F_L = 1/r. The metric F_L^2 g_0 is exactly ds^2 + g_(S^2), with s = −log r. Its length is ell = L + log r_0.
3. A–J's allowed conditions on F_L inside r = e^(−L) do not, by themselves, prove a uniform cap-volume bound for every possible choice. Make the permitted explicit choice F_L(r) = e^L f(e^L r), where f is positive, constant near zero, equals 1/x near x = 1, and is <= 1/x on (0,1]. For example, interpolate smoothly between 1 and 1/x on [1/2,3/4] using a cutoff. This produces a smooth radial core. Its volume is 4π integral_0^1 f(x)^3 x^2 dx, independent of L. The outer complement is fixed. Thus V_L = 4π ell + C for a fixed finite C.
4. On the exact product cylinder, the Yamabe operator is −∂_s^2 + Δ_(S^2) + 1/4. The S^2-constant Dirichlet sine functions have Rayleigh values mu_j = 1/4 + (πj/ell)^2. Extension by zero gives valid global H^1 trial functions. Orthogonality and the variational principle imply lambda_j(Y_(g_L)) <= mu_j for every positive integer j. This simultaneously supplies the required number of modes; it does not use fixed-index limiting convergence.
5. Positivity on the closed manifold follows from membership in the positive round conformal class. No assumption about nonnegative scalar curvature on transition regions is necessary. Normalize h_L = a_L g_L, where a_L = (2π^2/V_L)^(2/3). For h_L = W_L g_round, conformal covariance and the unitary map u -> W_L^(3/4)u give U Y_(h_L) U^(−1) = W_L^(−1/2)(Δ_round+3/4)W_L^(−1/2). Also integral W_L^(3/2) = a_L^(3/2)V_L = 2π^2. This is the exact target operator and normalization.
6. Constant rescaling gives Y_(h_L) = a_L^(−1)Y_(g_L). At the positive time t_L = 4a_L,

       H_L(t_L) >= 8a_L^(3/2)e^(−1)
                    sum_(j>=1) exp(−4π^2 j^2/ell^2).

   For a decreasing Gaussian, the sum is at least ell/(4sqrt(π)) − 1. Consequently

       H_L(t_L) >= (16π^2/(e V_L))
                    (ell/(4sqrt(π)) − 1),
       liminf_(L→∞) H_L(t_L) >= sqrt(π)/e.

   Since sqrt(π)/e > 13/20 > 129/200, the accepted elementary all-time round bound implies that some finite L in this classical family already gives a strict counterexample. Only the finite-L existence follows from this derivation; a specific L = 10000 and rational margin require the explicit cap estimates and certificates in the candidate.

The distinction is consequential: the old geometric construction plus routine min–max and Gaussian integration already supplies the qualitative negative mechanism once the sphere bound is supplied. The candidate may offer an explicit application to the exact question, an explicit finite choice, and reproducible rational certificates. This audit does not establish that any of those applications or certificates are historically first. A substantial new cylinder construction or a new spectral mechanism is not supported by the inspected evidence.

The standard fixed-index objection therefore cannot exclude A–J's construction from the novelty analysis. Nor does the fact that normalized lambda_1 grows contradict the heat argument: the tested time shrinks like L^(−2/3), and O(L) modes contribute at that time.

## Tested direct theorem transfers

| Source and inspected location | Proposed inference tested | Result and exact gap |
| --- | --- | --- |
| Frank, *Cwikel's theorem and the CLR inequality* (2014), §3.2 Theorem 3.2 and Lemma 3.4, pp. 13–17 | General semigroup/count theorem resolves the weighted Yamabe heat maximum | Excluded as a direct resolution. A local heat or spectral bound is an input; a CLR negative-count upper bound is the output. Reversing that implication or replacing its constant by the round maximum needs an additional sharp theorem. It gives neither a lower heat example nor a nonround/round comparison. |
| Frank, *The Lieb–Thirring inequalities: Recent results and open problems* (2020), §4.6 Lemma 15 and Conjecture 16, pp. 20–23 | GGM sphere transformation and d >= 7 counterexamples transfer to the target | Excluded as a direct resolution. The displayed stereographic potentials correspond to constant sphere potentials. A positive constant weight with the target integral is W = 1, which gives the round spectrum. The d >= 7 rejection concerns a different optimal-count conjecture and does not address the n = 3 heat-max witness. The full original GGM paper was not inspected by this lane. |
| Hundertmark–Kunstmann–Ried–Vugalter, *Cwikel's bound reloaded* (2022 online/2023 volume), Theorems 1.1/1.3 and Remark 1.4, pp. 114–117; §7 | Improved CLR constants/weak ideal control give the exact round comparison or contradict it | Excluded as a direct resolution. The statements are upper bounds on negative counts or weak trace ideals in terms of potential norms, with constants that do not equal the sharp target heat functional. No lower example or equivalence of sharp functionals is supplied. |
| Corso–Ried, *On a Variational Problem Related to the CLR and LT Inequalities* (2025), §1.2 Theorem 1.4, Theorem 1.6, Corollary 1.7, Table 2, pp. 4–7 | Solving their variational problem settles the weighted Yamabe heat conjecture | Excluded as a direct resolution. It solves an auxiliary optimization yielding improved upper CLR/LT bounds. The exact best CLR constant and the heat-max functional remain separate. For d = 3, sigma = 1, its method's CLR upper bound is not even the best already known bound; none of this supplies target heat ordering. |
| Ammann–Jammes, Example 1, §3.2, Theorem 4.1 | Published fixed-index eigenvalue theorem alone gives O(L) heat mass | Excluded in that form, **but the construction passes a different direct inference**: the explicitly chosen smooth rescaled core, exact cylinder, variational trial spaces, and volume normalization above supply the qualitative counterexample. |
| Branson (2007), discussion around (26)–(27), pp. 26–27 | A zeta difference sign implies pointwise heat sign or the time-optimized heat maximum | Excluded. A Mellin-weighted/inverse-moment sign does not determine a fixed-time integrand sign or its maximum. The displayed discussion explicitly leaves additional sign/zero information unsupported. |
| Møller–Ørsted (2009), §7 determinant/zeta local-extremal statements | Local determinant or zeta extrema resolve global heat maximum | Excluded. The functional and local/global quantifiers differ. |
| Pascu–Gageonea, arXiv:0807.4726, Theorems 3.8 and 4.3 | A Laugesen–Morpurgo heat result settles this Morpurgo conjecture | Excluded. These are radial diagonal monotonicity statements for Neumann heat kernels on Euclidean disks/balls, not weighted Yamabe heat traces on closed S^n. |

Primary links: [Frank 2014 PDF](https://ems.press/content/serial-article-files/33504), [Frank 2020 preprint](https://arxiv.org/abs/2007.09326), [HKRV DOI](https://doi.org/10.1007/s00222-022-01144-7), [Corso–Ried DOI](https://doi.org/10.1007/s00220-024-05216-y).

The inverse-moment route is not reopened merely by invoking Mellin inversion: an inequality between transforms is not a pointwise order without a further valid positivity/order theorem. Likewise, a CLR upper count can be integrated to some heat upper bound, but replacing that bound by the exact round time maximum is a separate unsupported step. Such routes are blocked at those exact transfer gaps. Distinct route: the A–J construction gives a *lower* count/heat mass by explicit variational trial functions and is not blocked there.

## Evidence and limits

- This lane independently read the relevant theorem statements, assumptions, and surrounding context in the downloaded full primary text for the four synthesis sources and A–J, including the same construction in arXiv v1/v2. The entire long papers were not read end-to-end.
- Local primary hashes are recorded in `SOURCE_HASHES.json`. Raw primary PDFs/text remain in `../private_sources/`; no raw copyrighted downloads were added to this lane.
- Publication/version metadata was cross-checked at the primary arXiv record; no claim about the published chapter's entire proof being identical to a preprint is needed for the older construction inference.
- The broader lane independently checked and agreed with the flat-background/fixed-core construction specialization and its heat implication. This agreement is validation within the project, not outside peer review.
- Direct Morpurgo trace-functional applicability belongs to the separately assigned historical lane; the parent must incorporate that lane's final artifacts. This lane did not inspect the full Morpurgo 2002 paper and does not pretend to be exhaustive across every Morpurgo paper.
- No person was contacted. No remote, branch, PR, sheet, Zenodo, or release mutation was performed. No worldwide priority or openness certificate is issued.

## Remaining gap and recommended disposition

There is no gap in the *qualitative classical-construction deduction* once the independently accepted round all-time bound is supplied. The historical gap is whether an earlier source explicitly recorded this exact heat-max application or its finite certificate. The four synthesis sources do not do so in the inspected relevant portions. A global negative priority claim would require more than this bounded audit.

Recommended parent disposition: retain the independently verified mathematical negative answer; prominently attribute the Pinocchio construction and explain the elementary derived-corollary relationship; restrict any contribution language to what is concretely new and evidenced. Do not label the qualitative cylinder mechanism novel, or infer novelty/openness from the absence of an earlier explicit exact theorem in this corpus.
