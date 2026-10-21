# Independent priority audit: general semimartingale and Volterra lane

PR234 / 30002291. Audit date: 2026-10-15 UTC. No mathematical-validity verdict is offered here; this is a priority and implication audit.

## Disposition

**No retrieved theorem was verified to imply the entire candidate statement. Novelty remains unverified.** Substantial prior coverage is certain. A material addition to the candidate's bibliography is the general-functional original **C** below: a claim that nonsymmetry by itself distinguishes the proposed result from prior moving-average theory is untenable.

The defensible residual question is whether the precise bounded-characteristic theorem for an arbitrary predictable jump kernel, including the finite-second-moment activity-index-2 boundary, already appears in a general Volterra, martingale-convolution, or predictable-mark stochastic-integral theorem. This search did not settle that question. Search failure supplies no evidence of nonexistence. Full-text access gaps are recorded below.

The independent coverage criteria were written in `SCOPE.md` before the candidate's files were read. No sibling audit reports or root priority conclusions were consulted. The later inbound lead to the Liu–Zhang–Fang article had already appeared independently in this lane's search 021. No outreach, Git mutation, provider mutation, or cross-chat/shard coordination was performed.

## Exact target tested

The candidate concerns the all-compensated L2 convolution with deterministic kernel g(x)=x_+^alpha f(x), 0<alpha<1/2, with f,f' exponentially decaying, f in C1, and f(0) nonzero. The driver on the real line has no continuous martingale part, bounded predictable drift, simple jumps, and compensator nu_s(dz) ds with a uniform deterministic bound on its quadratic rate. The target conclusion is the limit of Delta^(-2alpha) times the uncentered squared-increment sum, jointly at finitely many deterministic positive times, for every deterministic sequence of uniform spacings tending to zero, stable relative to the entire original sigma field.

Exact coverage requires the assumptions and conclusion together. A theorem about the driver’s ordinary variation, the smoothed process’s zero ordinary variation, Brownian or continuous martingale noise, large-time averages, changing the driving model, or adjusted increments is insufficient.

## Controlling originals and precise implications

The source-specific descriptions in this section are deliberately concise. Full source files and provider responses are private; exact hashes and reading locations are in `READ_EVIDENCE.md` and `SOURCE_HASHES.json`.

### A. Published moving-average antecedent

Basse-O'Connor–Lachièze-Rey–Podolskij, [Annals of Probability 45(6B), 4477–4528 (2017), DOI 10.1214/16-AOP1170](https://doi.org/10.1214/16-AOP1170); [accessible original arXiv:1506.06679, first public 2015-06-22](https://arxiv.org/abs/1506.06679). Read Theorem 1.1(i), model (1.1), (A)/(A-log), and the full-space stable definition plus finite-jump argument. The original treats a symmetric pure-jump Lévy driver with beta<2. At k=1,p=2,alpha<1/2 it gives the same marked jump-series limit at the stated reciprocal-integer grid. Tail monotonicity is among its kernel conditions. Its definition of stability uses every original F-measurable random variable; the natural filtration used to enumerate jumps must not be confused with this definition. **Substantial strict-subclass coverage.** The accessible author original, rather than a successfully downloaded version of record, controls this reading.

### B. Random-volatility semimartingale antecedent

Basse-O'Connor–Heinrich–Podolskij, [Bernoulli 24(4A), 3117–3146 (2018), DOI 10.3150/17-BEJ956](https://doi.org/10.3150/17-BEJ956); [original arXiv:1604.02307, first public 2016-04-08](https://arxiv.org/abs/1604.02307). Model (1.2) uses sigma_- dL with adapted càdlàg sigma and a symmetric pure-jump Lévy L relative to the supplied filtration; sigma need not be independent of L. Theorem 1.2(i), under (A),(B1), beta<2,p>beta,p>=1,alpha<k-1/p, yields functional F-stable M1 convergence. The k=1,p=2 specialization supplies the target formula on this genuine non-Lévy semimartingale subclass. Lemma 4.3 and the paragraph following its proof explicitly use all F-measurable variables. Remark 1.4 excludes J1/J2. Kernel-tail monotonicity and prehistory integrability remain assumptions. **A prior sufficient-conditions semimartingale answer; no implication for arbitrary predictable mark kernels.** Journal metadata at the university has a conflicting page range; the publisher-indexed range above is used. The accessible original is the read text.

### C. Nonsymmetric Lévy coverage omitted by the candidate

Basse-O'Connor–Heinrich–Podolskij, [arXiv:1806.10352, public 2018-06-27](https://arxiv.org/abs/1806.10352), published [Electronic Journal of Probability 24, article 79 (2019), DOI 10.1214/19-EJP336](https://doi.org/10.1214/19-EJP336). The original's model (1.1) allows a two-sided pure-jump Lévy driver without symmetry. Theorem 2.1(i) and Proposition 2.3(i), with (A), beta<2, provide ambient stable finite-dimensional convergence and M1 convergence under the sign condition (FC).

For the quadratic test F(x)=x², choose the theorem's auxiliary regularity exponent

    max{beta, 1/(1-alpha)} < q < 2.

Such q exists whenever beta<2 and alpha<1/2. Then F is C^q, F(0)=F'(0)=0, alpha<1-1/q, and (FC) holds. The normalizations a_n=1,b_n=n^alpha give exactly n^(2alpha) times the quadratic statistic. **Verified nonsymmetric deterministic-Lévy prior coverage**, subject to the source's tail/kernel assumptions and stated grid. Publication metadata gives September 2019, while Crossref supplies only a generic January date; priority already follows from the dated public original. Final publisher PDF access failed.

### D. Broad martingale-convolution antecedent

Coquet–Jakubowski–Mémin–Słomiński, [Natural decomposition of processes and weak Dirichlet processes, arXiv:math/0403461, public 2004-03-26](https://arxiv.org/abs/math/0403461). Section 4 allows a quasileft-continuous square-integrable martingale, including discontinuous and nonsymmetric drivers, and deterministic two-variable kernels. Theorems 4.1–4.2 establish weak-Dirichlet/Dirichlet and ordinary quadratic-variation conclusions under (H0)–(H6). In the bounded-variation-kernel case, the continuous remainder has zero ordinary quadratic variation; the martingale component is the diagonal-kernel integral. Where its path hypotheses hold, g(0)=0 makes that ordinary variation zero. **This does not provide the candidate's nonzero rescaled stable limit or independent jump phases.** A zero unscaled limit cannot determine a finer scaling limit. This is the closest verified broad general-martingale antecedent in the early search.

### E. Later general predictable-mark convolution theorem

Schroers, [Robust Functional Data Analysis for Stochastic Evolution Equations in Infinite Dimensions, arXiv:2401.16286, first public 2024-01-29; read v3 dated 2025-09-05](https://arxiv.org/abs/2401.16286). Section 2 permits Hilbert-space Itô semimartingales with arbitrary predictable mark-dependent coefficient gamma_s(z) against compensated homogeneous Poisson noise. Theorem 3.1 proves that semigroup-adjusted tensor-increment sums converge u.c.p. to the latent driver's quadratic covariation. This is genuinely broader than scalar-volatility Lévy noise. However, the adjusted increment f_(i Delta)-S(Delta)f_((i-1)Delta), Hilbert tensor statistic, and unscaled probability limit are different from the singular scalar raw-increment statistic and marked stable limit here. **No direct coverage implication was verified.** Invoking an unspecified lift or singular observation map would leave the central statistical limit unproved.

## Other checked families

| Original read | Controlling location and decisive scope difference |
|---|---|
| [Hu–Nualart–Song, fractional martingales (2009); arXiv:0711.1313](https://arxiv.org/abs/0711.1313) | Definition 2.1 and Theorem 2.6 require continuous local martingales. Their variation order is 2/(1+2alpha), with an integrated volatility limit. They do not cover jump-driver phases. |
| [Russo–Viens (2015), DOI 10.1051/ps/2014031](https://www.numdam.org/item/PS_2015__19__414_0/) | Published Section 4 and Theorem 4.1 use continuous martingales and odd power variations via regularization. The older preprint wording “martingale” alone is misleading for this target. |
| [Basse-O'Connor–Podolskij, critical cases, original dated 2015-12-01](https://repec.econ.au.dk/repec/creates/rp/15/rp15_57.pdf) | Theorem 1.2 retains beta<2 and treats critical alpha=k-1/p or alpha=k-1/beta with logarithmic normalizations. It does not add beta=2 coverage. |
| [Ljungdahl–Podolskij (2018), DOI 10.15559/18-VMSTA111](https://www.vmsta.org/journal/VMSTA/article/122/text) | Model (1.1), (B), and Theorem 2.2 retain a symmetric Lévy driver and beta<2. Multiple singularities, including subsequence phase effects, broaden the kernel direction rather than predictable driver characteristics. |
| [Basse-O'Connor–Pilipauskaitė–Podolskij (2021), arXiv:2008.01412](https://arxiv.org/abs/2008.01412) | Model (2.1), assumptions (beta),(theta),(g), and Theorems 3.1–3.2 use a symmetric independently scattered infinitely divisible random measure with deterministic control and beta<2. No arbitrary predictable kernel. |
| [Abi Jaber–Cuchiero–Larsson–Pulido (2021), arXiv:1909.01166](https://arxiv.org/abs/1909.01166) | Theorems 1.2 and 1.6 address weak existence and stability for convolution equations, allowing state-dependent jump kernels. Their “stability” concerns convergence of solution laws, not the candidate's stable high-frequency statistic. |
| [Jacod (2008), arXiv:math/0604450](https://arxiv.org/abs/math/0604450) | Section 2 studies statistics of observed semimartingale increments. Its broad predictable-characteristic assumptions cannot be applied to the smoothed observation without checking that observation's semimartingale regime and required statistic. No convolution implication found. |
| [Todorov–Tauchen, author original dated 2010-03-18](https://www.kellogg.northwestern.edu/faculty/todorov/htm/papers/tse.pdf) | Main results concern pure-jump Itô semimartingale observations and low-power, locally stable regimes. No fractional convolution or singular jump-phase statistic. |
| [Corcuera, Abel Symposium original](https://abelsymposium.no/symp2005/preprints/corcuera.pdf) | Section 2, Theorem 1 concerns pathwise integrals against fractional Brownian motion with H>1/2. The stochastic integral's integrator is not an arbitrary jump semimartingale. |
| [Di Nunno–Fiacco–Karlsen (2019), arXiv:1809.04011](https://arxiv.org/abs/1809.04011) | Theorems on kernel perturbations and fractional-integral approximation do not identify the candidate's high-frequency stable law. Driver remains Lévy. |
| [Basse-O'Connor–Podolskij (2024), arXiv:2302.14034](https://arxiv.org/abs/2302.14034) | Model (1.1), Theorem 1.1 use harmonizable complex isotropic stable noise and a nonergodic quadratic-statistic limit. Different spectral model, statistic regime, and limit. |
| [Friesen–Gerhold–Wiedermann, original arXiv:2412.15971](https://arxiv.org/abs/2412.15971) | Model (1.2), Theorem 2.2 and functional extension are Brownian-driven small-time process CLTs. The “realized variance” application is a time average of a variance process, not this increment statistic. |
| [Bianchi–Bonaccorsi–Cañadas–Friesen, original arXiv:2509.08466](https://arxiv.org/abs/2509.08466) | Sections 3–4, Corollary 4.3, and Theorem 4.5 concern long-time distributions and time averages for Gaussian-driven Markovian lifts, not fixed-horizon mesh refinement. |
| [Benth–Veraart, original arXiv:2410.00566](https://arxiv.org/abs/2410.00566) | Section 2.3 and bibliography supplied later citation leads. A survey's failure to list a further theorem is not a priority result. |

## What remains different from verified prior coverage

The distinction is the **joint package** of arbitrary predictable compensator kernels, no symmetry or fixed scalar Lévy structure, only a bounded second-moment rate, a diffuse time compensator, the all-compensated real-line prehistory construction, and the exact rescaled stable conclusion. Removing one condition from a theorem is not established merely because its proof uses familiar truncation.

There are concrete reasons the package is not a formal substitution in A–C:

- A scalar dilation of a symmetric Lévy measure is conditionally symmetric. A genuinely asymmetric predictable kernel cannot belong to that driver class. Even among symmetric kernels, a time-varying mixture of differently shaped jump laws need not be a scalar dilation of a single law.
- Finite quadratic rate does not imply beta<2. For the symmetric measure with density 1/(|z|³ log²(1/|z|)) on 0<|z|<e^(-1), the quadratic integral equals 2. Substituting |z|=e^(-v) shows every smaller power integral diverges. The auxiliary q used in C cannot be chosen at this boundary.
- Exponential bounds on f,f' do not by themselves assert eventual monotonicity of |g'|. Therefore even the kernel classes should not be called identical without an additional reduction.
- The retrieved limit statements use reciprocal-integer uniform grids. Their equidistribution mechanisms strongly suggest arbitrary deterministic spacings are a routine extension, but a suggestion about proof portability is not a theorem-level implication. This audit does not present a grid-extension proof or claim that mesh generality is independently novel.

The weights agree: with h1(x)=x_+^alpha-(x-1)_+^alpha, the candidate uses sum over l>=1 of h1(l-u)²; changing U to 1-U and setting j=l-1 gives sum over j>=0 of h1(j+U)². The uniform mark law is unchanged. The script `scope_checks.py` reproduces finite-series indexing and rational auxiliary-exponent checks; it does not test stochastic convergence or establish novelty.

## Unclosed original-access leads

1. [Liu–Zhang, Power variation of fractional integral processes with jumps, DOI 10.1016/j.spl.2011.01.016](https://doi.org/10.1016/j.spl.2011.01.016). Correct PII is S0167715211000319, verified through primary Crossref/Elsevier metadata. The API returned only metadata, and publisher full-text access failed. No theorem-level coverage or noncoverage verdict is assigned.
2. [Liu–Zhang–Fang, Multipower variation from generalized difference for fractional integral processes with jumps, DOI 10.1080/03610926.2016.1217019](https://www.tandfonline.com/doi/abs/10.1080/03610926.2016.1217019). The publisher dates the accepted-author posting 2016-09-20 and final online publication 2017-06-20. Full-text requests returned 403. No theorem-level verdict is assigned from its abstract.
3. [Liu–Tang–Zhang, Central limit theorems for power variation of Gaussian integral processes with jumps, DOI 10.1007/s11425-013-4736-4](https://link.springer.com/article/10.1007/s11425-013-4736-4). Publisher preview describes additive Lévy jumps and a Gaussian-integral component, but the full controlling theorems were unavailable. This is a triaged lead, not a verified exclusion.

No purchase, author request, external communication, or access-control circumvention was initiated. Legitimate full originals could further reduce the uncertainty; that observation is recorded solely as a research need.

## Promotion guidance

The candidate can be described as an explicit sufficient-conditions theorem **under review for novelty**, with the full driver class stated. Its literature section should add C and avoid presenting either the jump-weight formula, random-volatility semimartingale extension, ambient stability, nonsymmetry alone, or the truncation method as new. The original OWR request was open-ended about sufficient conditions; a broad “first semimartingale answer” claim would ignore B.

This lane supports neither “already fully covered” nor “certified new.” The strongest verified result is broad prior coverage of strict subclasses plus ordinary general-martingale convolution theory. The exact remaining priority issue is the full predictable-kernel, index-2-capable rescaled stable theorem. Resolving that issue requires a controlling earlier theorem or a more complete source audit, not an argument from missing search hits.
