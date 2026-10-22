# Independent adversarial priority and scope report

PR 218 / problem 30006020. Independent evidence cutoff: 2026-10-15 UTC. This is a priority gate, assuming the separately reviewed mathematical proof is sound. No root or sibling review was consulted before sealing this report.

**Verdict:** the checked primary literature does not falsify a new solution of the original *intermediate area* question in the principal quadratic, iterated limit ensemble. It does strongly narrow the contribution: the geometry, the weighted permutation assembly, and the uniform density mechanism are prior work. Candidate Theorem A is a short corollary extracted from those old inputs; the potentially new result is the explicit geometric mesoscopic limit at every admissible rate, with window moments. No checked source already states or proves that same result. This is **novelty not falsified by the bounded audit**, not a certified claim of first priority and not an `already_solved` finding.

The exact unresolved priority lead is Delecroix-Liu's announced *Small components of random multicurves on large genus hyperbolic surfaces*. Its complete text was not located. A claim of universal first priority cannot be certified without public evidence settling what that work contains. No external communication was prepared or initiated.

## Frozen original target and scope

The controlling source is Delecroix's contribution to [OWR 41/2024](https://doi.org/10.4171/owr/2024/41), printed pp. 2384-2387, Problem 2 p. 2387. A fresh full institutional PDF matches the frozen hash. The contribution defines area by whole surface normalization and takes N to infinity at fixed genus before taking genus to infinity. Problem 2 follows Theorem 2, which is expressly about the principal holomorphic quadratic stratum. The source's concrete count window is [1/sqrt(g), 2/sqrt(g)]. See `ORIGINAL_PROBLEM_FREEZE.md` for the independent freeze and normalization reservation.

The candidate does answer that exact window and the intervening mesoscopic family, conditional on its proof. Theorem A also gives an entire finite multiset model in total variation. The source's informal aspiration to understand a full spectrum should not be promoted to a theorem for every stratum, every N(g), or simultaneous cross scale laws: these are different statements. The all strata conjectures and diagonal limit question are separately discussed in the report; they are not silently resolved here.

## Controlling earlier primary results and dates

[DL, final JEMS](https://doi.org/10.4171/JEMS/1469), 27 (2025), 5093-5131, is the complete 39 page publisher version, freshly retrieved and read. The publisher records submission 4 March 2022, acceptance 26 February 2024, and online publication 7 June 2024. arXiv:2202.10255 v1 was submitted 21 February 2022; its numbering is not used to control the candidate's citations. The final edition's Theorem 1.4 identifies the fixed genus square tiled cylinder area law, and Theorem 3.2 gives its exact weighted stable graph mixture. Its Theorem 1.2 / Corollary 1.5 gives weak convergence of the normalized ranked vector to PD(1/2). The space is equipped with product topology.

Crucially, DL printed p. 5098 expressly explains that o(1) components are invisible to this PD convergence and announces further microscopic work in progress. Section 4 conditions on one vertex graphs with O(log g) loops. Equation (6.1), definition (6.2), and the positive monomial expansion in the proof of Lemma 6.4 (pp. 5116-5117) are uniform over all compositions; equation (6.7) simplifies the remaining prefactor. The complete paper supplies no stated moving mesoscopic window theorem and no explicit total variation theorem for the candidate's marked assembly.

[DGZZ, Inventiones](https://doi.org/10.1007/s00222-022-01123-y), 230 (2022), 123-224, was checked in the full author hosted publisher PDF, including all relevant actual theorem statements and comparison proofs. The publisher dates its version of record 20 June 2022; arXiv v1 is 9 July 2020 and v2 is 5 July 2022. Theorem 1.7 transfers cylinder number statistics from multicurves to surfaces. Theorem 1.12 gives the generating function asymptotic for total K on |t|<8/7 with quantitative error on compact sets. Theorem 1.14 concerns moments of this *total* count. Section 3.2, especially Lemma 3.6 and (3.20)-(3.23), already defines the candidate's unmarked assembly as the cycles of a weighted permutation with θ_j=ζ(2j)/2. Theorem 3.7 gives its coefficient asymptotics. Lemma 3.5 controls correlator coefficients uniformly; Theorem 5.2 gives the low k graph comparison used by the candidate. These are not cylinder area window theorems.

The OWR workshop ran 8-13 September 2024, after DL's online publication. Its contribution cites DL and nonetheless poses Problem 2. This is direct contemporary evidence that the cited macroscopic theorem was not being represented as an answer to the intermediate area problem. It is not evidence excluding a later solution or an unpublished result.

## Technical coverage matrix

| Candidate claim or ingredient | What earlier primary material gives | Assessment |
|---|---|---|
| Same fixed genus area ensemble, m=infinity | DL 1.4 and 3.2; principal stratum has the full fixed genus leading count | Match. No new ensemble construction |
| ζ(2j)/(2j) composition weights | DGZZ §3.2, θ_j=ζ(2j)/2 | Exactly prior as an unmarked partition law |
| Dirichlet(2j_i) given composition | DL Lemma 6.4 proof has the positive simplex monomials; normalization is the elementary Dirichlet identity | Prior exact density reinterpreted as marks |
| Uniform ctilde=1+o(1) for k=O(log g) | DL (6.1)-(6.2); already grounded in Aggarwal and DGZZ | Entirely prior geometric estimate |
| One vertex logarithmic truncation | DL Theorem 2.7 and Section 4; quantitative DGZZ 1.12/5.2 | Prior concentration mechanism |
| Full multiset TV approximation to the *marked* composition model | Follows from the previous uniform positive comparison and conditioning, with DL (6.7) or a short prefactor ratio calculation | Not stated explicitly in checked papers; a short corollary of old inputs, not a new geometric theorem |
| Poisson limit for unmarked example scale q_n proportional to sqrt(n) | Nikeghbali-Storm-Zeindler actual Theorem 3.3, applied to these weights and moving sets | Standard older probabilistic tool covers this part |
| Unmarked all q_n to infinity, q_n=o(n) | Elementary assembly factorial moment extraction; broader logarithmic assembly literature is an older lead | Candidate proof is checkable; first probabilistic novelty is not established |
| All-rate geometric Gamma smoothing, including arbitrarily slow q_n growth | No same assertion found in checked DL/DGZZ or later relevant primary material | Candidate supplies the integrated tail argument needed beyond a naive global union bound |
| All fixed joint area window moments | DL fixed size biased moments and DGZZ total K moments do not imply these alone | Candidate adds window uniform integrability and exceptional event transfer |
| Exact OWR window Poisson(log(2)/2), mean and variance | No same ensemble theorem found | Candidate covers the original concrete request if proof is sound |
| All strata, a diagonal N(g), or literal OWR microscopic formula | Neither candidate theorem claims these | Outside accepted coverage; 4g-4 versus 6g-6 is not equated |

`PRIOR_COVERAGE_DERIVATION.md` gives checkable equations behind the overlap and two non-implication witnesses.

## Strongest coverage objection

The candidate's presentation must not suggest a newly discovered surface to permutation correspondence or a new large genus correlator estimate. Those are the hard geometric inputs already proved by DL/DGZZ and Aggarwal. Even the stronger uniform control needed for the full multiset approximation is present in DL's proof, not only its macroscopic conclusion. Positive monomial mixtures make the passage from uniform coefficient estimates to uniform density comparison immediate. The model's cycle weights are exactly DGZZ's old model. Thus a reviewer can fairly describe Theorem A as a useful reformulation or corollary of prior work.

There is also older ready made probability theory for the source example. In [Nikeghbali-Storm-Zeindler, arXiv:1302.5938](https://arxiv.org/abs/1302.5938), actual Theorem 3.3 handles characteristic functions for finitely many moving sets of cycle lengths, under C log n - n/d_n to minus infinity for every real C. The candidate weights meet its analytic hypotheses. At q_n proportional to sqrt(n), it gives the unmarked Poisson means directly. Its stated restriction is stronger than arbitrary q_n=o(n), so it does not by itself subsume the candidate's entire mesoscopic statement. More general older assembly TV results may do so; their complete hypotheses were not verified here.

This objection narrows the intellectual contribution and affects how substantial it is. It does **not** justify `already_solved` just because a new consequence has a proof assembled from older theorems. The original question was deliberately posed in a source already aware of those inputs.

## Strongest novelty saving argument

The candidate makes a precise, genus dependent observation that neither weak macroscopic convergence nor fixed compact microscopic convergence controls. Its uniform marked model justifies passing to such observations, and its integrated Gamma estimates retain every rate g s_g to infinity without imposing an artificial lower rate. Its separate moment argument is necessary: total variation alone does not control moments of an unbounded window count. If no earlier geometric paper states or proves this conclusion, the exact original window and all mesoscopic rates are a legitimate new corollary solving a stated problem, even with classical ingredients.

There are concrete reasons not to collapse this distinction. A discrete cycle partition and a continuously marked area partition can be mutually singular in total variation while sharing a PD limit. Similarly, the large x tail of a microscopic intensity cannot be substituted into a genus dependent window escaping to infinity without a uniform argument. The candidate addresses both missing links rather than citing endpoint convergence as sufficient.

## Fresh literature challenges and unresolved leads

1. **Announced Small components paper.** OWR reference [5] is directly relevant and remains the main priority uncertainty. Current author pages and indexed primary searches did not locate its complete public text. That is not proof of absence.
2. **Later author talk.** Liu's [Durham February 2025 slides](https://www.math.univ-paris13.fr/~mingkun.liu/talks/Durham.pdf), visual slide 195, label a microscopic multicurve count in [a/(6g),b/(6g)] as a conjecture, with density e^(-x)(cosh x-1)/x and note the large x asymptotic 1/(2x). The exact multiplicity convention is not reconstructed from that slide alone. It is neither a proved moving mesoscopic theorem nor a resolution of the OWR normalization discrepancy. It strengthens the case that the 1/(2x) intensity was anticipated; it does not supply the missing uniformity.
3. **2025 random metric maps paper.** [Barazer-Giacchetto-Liu, DOI 10.1017/fms.2025.31](https://doi.org/10.1017/fms.2025.31), Theorems A-B, gives PPP statistics for short cycles on uniform metric ribbon graphs with fixed n faces and total perimeter asymptotic to 12g. The ensemble, counted objects, and fixed scale differ; it cannot be relabelled as a cylinder area theorem. Its intensity (cosh(l)-1)/l is also a different function. The actual definitions and theorem assumptions were read.
4. **Current 2026 work.** Liu's list includes recent preprints through September 2026. The May 2026 non-simple curve frequency paper is a different counting problem by its primary abstract. No claim that its complete proof has been checked is made.
5. **Older general assembly results.** Stark 1997, DOI 10.1017/S0963548396002775, and ABT's 2003 book are a precise probabilistic overlap lead. Their publisher abstract/preface describes sublinear component Poisson approximation. The complete relevant theorem and all conditions were not accessible in the checked publisher pages, so they are not promoted to a verified all-rate prior theorem. Even full applicability would cover the unmarked assembly; the same geometric marked conclusion would still need to be exhibited.

The strongest verified outcome is therefore a scoped solution claim with prior work explicitly credited. The exact remaining gap is priority certification against the announced Small components work and any unindexed same ensemble theorem, plus exact general assembly theorem coverage if novelty of the probability argument itself is claimed. This lane found no evidence warranting a declaration that the original question had already been solved. It also does not support an unqualified declaration that every meaning of the full cylinder spectrum is now resolved.
