# Independent priority-history and citation audit — PR234 / 30002291

Audit date: 2026-10-15 UTC (2026-10-14 America/Los_Angeles). Scope: historical status of the original question, early chronology, surveys and descendants. The frozen candidate was read without modification; hashes are in INPUT_PROVENANCE.json. No sibling reports or verdicts were consulted. All statements below are independently derived in this lane.

## Disposition

**The claim that this is a first solution of a still-unanswered original 2013 problem is not supported.** There is a checkable prior sufficient-conditions answer for a substantial non-Lévy semimartingale class, available in corrected functional form by October 2016 and published in 2018. This is enough to defeat a priority claim tied solely to the source's open-ended request.

**The exact candidate remains a potentially broader theorem, with priority unverified.** None of the inspected model/theorem statements covers its whole arbitrary predictable-kernel and finite-quadratic-rate class. That is a bounded comparison, not a claim that no earlier theorem exists. Under the user's requirement of a genuinely unsolved original mathematical gap, this lane recommends blocking promotion as an original open-problem solution. A separately motivated extension needs its own novelty case.

## Exact original scope

[OWR 09/2013](https://ems.press/content/serial-article-files/46440), Podolskij's full contribution, printed 491–493, states a compound-Poisson fixed-time stable quadratic-variation limit and asks for sufficient conditions for a broader pure-jump semimartingale driver. It supplies no maximal class, no requirement of arbitrary predictable kernels, no BG-index 2 boundary target, and no functional topology. Its formulation does not permit replacing sufficient conditions by a universal quantifier over all pure-jump semimartingales. A deterministic-jump counterexample to that universal assertion therefore does not resolve a previously open obstruction in the stated source.

## Verified chronology

These are earliest located primary records in this lane, not assertions of first-ever discovery.

| Date | Primary record | Historical role |
|---|---|---|
| 10–16 Feb 2013 | OWR 09/2013 meeting; printed 491–493 | Original compound-Poisson display and broader sufficient-conditions question. |
| 7 May 2014 | [arXiv 1405.1531v1](https://arxiv.org/abs/1405.1531v1), Theorem 4.8(i), eq 4.21 | Public Lévy-driver version; references a 2014 working paper. This predates the 2015 dedicated preprint. |
| 22 Jun 2015,17:02:04UTC | [arXiv 1506.06679v1](https://arxiv.org/abs/1506.06679v1), Theorem 1.1(i) | Dedicated preprint, then titled *Limit theorems for stationary increments Lévy driven moving averages*. |
| 8 Apr 2016,11:16:22UTC | [arXiv 1604.02307v1](https://arxiv.org/abs/1604.02307v1), Theorem 1.2(i) | Random-volatility extension already stated, but its functional J1 assertion is not the corrected statement. |
| 14Oct 2016,14:37:46UTC | [arXiv 1604.02307v2](https://arxiv.org/abs/1604.02307v2), Theorem 1.2(i), Remark 1.4 | M1 statement; explicit J1/J2 failure. Use this version for valid functional-history claims. |
| Nov 2017 | [AOP 45(6B),4477–4528](https://doi.org/10.1214/16-AOP1170) | Published Lévy-driver article. |
| Nov 2018 | [Bernoulli 24(4A),3117–3146](https://doi.org/10.3150/17-BEJ956) | Published random-volatility extension. |
| Feb 2026 | [Bernoulli 32(1),24–48](https://doi.org/10.3150/25-BEJ1902) | Recent survey; preprint dates1 Oct 2024 and 30 Oct 2024. |

ArXiv submission histories and Crossref publisher deposits verify the preprint/issue dates. Crossref creation dates are not publication dates. One Aarhus Pure page gives Bernoulli pages 2429–2460; Crossref, official IMS indexing, the 2018 book chapter bibliography and the author publication list support 3117–3146. No conclusion here depends on the erroneous pagination.

## Independent mathematical comparison

The controlling [2016 v2 primary text](https://arxiv.org/pdf/1604.02307v2) defines its driver through a symmetric pure-jump Lévy process relative to the filtration and an adapted càdlàg volatility. Theorem 1.2(i) assumes(A),(B1), β<2, p>β, p≥1 and α<k−1/p, and proves functional stable M1 convergence. No independence between the volatility and Lévy process is required by the model. See SOURCE_READ_LEDGER.md for exact locations.

**Own deduction from those definitions and the theorem:** set k=1,p=2 and define the semimartingale driver

    dY_s = σ_(s−) dL_s.

Then ΔY_T=σ_(T−)ΔL_T. With h(x)=x_+^α−(x−1)_+^α and U'=1−U,

    sum_(l≥0) h(l+U)^2 = sum_(m≥1) h(m−U')^2 = W_α(U').

The old limit is therefore the source's squared-driver-jump limit. Fixed deterministic evaluation times are continuity times almost surely, so the M1 result gives joint fixed-time limits. For a concrete overlapping subcase, take g(x)=x_+^αe^(−x), a symmetric tempered stable L with index in(0,2), and σ_s=2 for s<0, σ_s=2+sin(L_s) for s≥0. This volatility is bounded and adapted: it is constant on negative times and uses adapted Lévy levels only at nonnegative times. Since L_0=0, both definitions agree at 0 and the process is càdlàg. Exponential decay makes the old prehistory integrability conditions finite, and |g′| is eventually decreasing. The driver is a state-dependent pure-jump semimartingale. Thus “semimartingale rather than Lévy” does not by itself identify an unsolved residual.

The candidate has real differences in hypotheses: arbitrary predictable time-dependent jump-measure shape, possible asymmetry, bounded quadratic rate including some BG-index 2 drivers, and no eventual derivative-monotonicity condition. It also imposes global square-integrability/bounded-rate assumptions that the old result does not generally impose. Hence it is not appropriate to say either theorem contains the other in full. A genuine extension should identify an explicit driver outside every controlling earlier theorem and prove why a reduction is unavailable.

The 2014 survey already states arbitrary deterministic meshes tending to zero and independent phases relative to the original sigma field. Those features alone are not a credible new historical contribution. The candidate's full-sigma-field stability should still be checked against each earlier filtration convention before asserting literal all-assumptions containment.

## Citation and recent-literature trace

CITATION_LEDGER.md preserves 30 deduplicated discovery records from a 28-record AOP and 12-record Bernoulli citation snapshot. Index coverage is incomplete and is not used as mathematical evidence.

Full primary texts were obtained for these selected descendants, and their model/assumption/theorem sections were inspected:

- [Ljungdahl–Podolskij 2018](https://doi.org/10.15559/18-VMSTA111): multiple kernel singularities, symmetric Lévy driver, β<2; Theorem 2.2 involves phase subsequences.
- [Basse-O'Connor–Heinrich–Podolskij 2019](https://arxiv.org/abs/1806.10352): more general variation functionals, within a Lévy moving-average model; Theorem 2.1 retains β<2.
- [Basse-O'Connor–Pilipauskaitė–Podolskij 2021](https://arxiv.org/abs/2008.01412): fractional-type random fields with an independently scattered symmetric infinitely divisible random measure and β<2.
- [Mies–Podolskij 2023](https://arxiv.org/abs/2208.07453): superpositions of independent fractional stable motions and multiscale inference; its deterministic-component model does not state the arbitrary predictable-kernel theorem.
- [Benth–Veraart 2024 v2/2026](https://arxiv.org/abs/2410.00566v2), section 2.3: contemporary overview cites the 2017 and 2018 papers among established univariate variation results. It does not certify absence of later generalizations.

The [2018 monograph chapter](https://doi.org/10.1007/978-3-319-94129-5_3) was available only as abstract/reference list; no whole-chapter coverage claim is made. Its statement that some LSS asymptotics remain open cannot be read as reopening every specific sufficient-conditions question.

## Adversarial checks and remaining limits

1. **Could the old theorem still be only a Lévy-driver result?** No: its adapted volatility permits dependence on L's history. The explicit Y construction above is a semimartingale-driver reinterpretation, not an independent-volatility assumption.
2. **Could a candidate outside that class still answer the original question?** Yes, as another sufficient theorem. This does not make it the first answer or establish a genuinely unresolved original target.
3. **Could BG-index 2 be a genuine uncovered boundary?** It is outside the inspected β<2 statements, and finite second moment does not force β<2. Its prior status remains unresolved by this lane.
4. **Could a generic representation theorem collapse the kernel extension?** Possibly; this requires separate scrutiny of scalar versus multidimensional/marked-noise representations. The citation search is not a proof of non-reducibility.
5. **Could J1 failure create the novelty?** No: the source asks fixed-time convergence, and the prior corrected paper already discusses that topology issue.

Primary journal PDF downloads hit 403/HTML wrappers in this lane. Complete arXiv controlling originals and primary metadata were obtained; final-journal-only changes were not exhaustively compared. No absence-of-hits conclusion, first-solution label, universal-class resolution, or comprehensive novelty certification is justified. No external individual was contacted and no outreach was prepared. No Git/index/ref/provider mutation occurred.

**Scoped audit completion: 100%. Exact extension-priority certification: unresolved.** The strongest verified finding is prior substantive satisfaction of the original sufficient-conditions request; the exact remaining task is a separately formulated, independently justified novelty comparison for the arbitrary-kernel/BG 2 extension.
