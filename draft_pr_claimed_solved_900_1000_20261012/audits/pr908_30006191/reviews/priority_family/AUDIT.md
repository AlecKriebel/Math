# PR #908 primary-source priority audit

**Outcome: priority is not cleared for a novel resolution of the existential question.** The candidate remains a checkable, self-contained bounded-region construction. The inspected earlier source does not state the literal cutoff theorem, but its proof directly adapts to the candidate's kernel and yields the requested existential norm discontinuity. The precise maximal-norm localization sharpening is not shown to be already stated, and its novelty is not certified.

This audit concerns only the current `bounded_region_v2` for problem 30006191, original head `a35667b1bb0bafed69916709997a4684223ecc93`. The author proof was independently hashed as `2b7c22cfc54049a9e51fe5eb4eb283ba911e6f27e8b6e4dc9557927bc04d7350`. No other candidate/legacy packet, historical priority conclusion, or unrelated shard was consulted. The candidate, queue, PR, Git history, and remote were not changed. Publication decisions belong to the parent audit and the human user.

## Exact question and decision standard

The authenticated [OWR 7/2025](https://ems.press/content/serial-article-files/51350), DOI `10.4171/owr/2025/7`, distinguishes pointwise norm continuity from strong operator continuity on printed p. 365. The literal question on p. 371 asks for a particular interaction and states exhibiting failure for an unregularized interaction restricted to one bounded `Lambda x Lambda`, with all-space free kinetic energy. It is an existential question. Fixed density, fixed energy, one fixed normal state, and all potentials/dimensions are not its requirements.

The priority audit distinguishes four levels: a literally applicable earlier theorem; a direct deduction/adaptation of an earlier proof; a similar mechanism requiring a substantive new estimate; and a conjecture or heuristic. Failed searches and absent indexed citations cannot establish firstness or current openness.

## Critical earlier source and the cutoff test

[Siebert, arXiv:2609.34402v1](https://arxiv.org/pdf/2609.34402v1) was submitted on 28 September 2026, before the candidate's 7 October date. The current arXiv record still identifies v1. The entire 21-page paper was read, including assumptions A-D, all results, proof sections 3.1-3.5, and references; critical pages were also visually checked.

Theorem 2.4 is stated for full-space difference potentials; Proposition 2.6 treats the total-number constant interaction. Neither is literally the local-number cutoff Hamiltonian. Nevertheless, the symmetric bounded kernel substitution is checked step by step in [ADAPTATION.md](ADAPTATION.md):

\[
K(x,y)=1_\Lambda(x)1_\Lambda(y),\qquad
h_\sigma=-\Delta+(1-\sigma)1_\Lambda,
\]

\[
H^{(\sigma)}_n=\sum_j h_{\sigma,j}+\sum_{i\ne j}K(x_i,x_j)
 =T_n+L_n(L_n-\sigma).
\]

This is the actual candidate for both ordering conventions. Choose a cluster and one test mode strictly inside the cutoff, and another test mode strictly outside. The cross-interaction values are exactly 1 and 0. The packed initial energy, multiplication-operator commutator cancellation, local antisymmetrization, and cross-phase estimates remain valid. For the diagonal convention, the bounded external potential is locally constant on all test supports and satisfies the required local `H^2` propagation estimate.

The resulting fixed gauge-invariant observable has a lower bound

\[
\liminf_n\|\tau_{\theta/n}(a^*(f_1)a(f_2))-a^*(f_1)a(f_2)\|
 \geq 2|\sin\theta|-C\theta^2>0
\]

for small fixed positive `theta`. Polarization then gives a fixed creation/annihilation observable and varying state witnesses. This is an **audit deduction by direct proof adaptation**, not a cutoff theorem attributed to the source. It suffices for the existential question. The cutoff qualifier alone therefore cannot support a claim to a novel resolution.

## What remains distinct in this candidate

The candidate supplies an explicitly prescribed annihilation orbital, concrete packed Slaters, exact times `pi/(2N+1-sigma)`, operator and vector norm limits of 2, and state witnesses tending to 4. Its free-Slater leakage/variance comparison has a vanishing error `O(N^{-1/6}+N^{-1/3})`. The preceding adaptation only has a small fixed `O(theta^2)` error at `t=theta/n`, so it does not prove those maximal limits.

Maximal discontinuity of the total-number reference is already in Proposition 2.6, pp. 7 and 17-18. Transferring that limit to the spatially restricted interaction is the concrete extra estimate here. A quantitative sharpening can be described accurately without claiming that it is new. This audit has not established either prior publication or novelty of that exact sharpening.

The algebraic observation that a potential constant on the cutoff's difference set gives `L^2` or `L(L-1)` is elementary. An unbounded commutator or unbounded number generator alone does not prove discontinuity with the all-space kinetic energy. The localization comparison is the relevant checkable content. All fixed vectors and normal states remain continuous; the claim concerns norm and particle-number-dependent witnesses.

## Earlier and neighboring primary sources

| Source and inspected location | Priority relevance |
|---|---|
| [Bratteli-Robinson, 1997, Sec. 6.3, pp. 353-354](https://page-one.springer.com/pdf/preview/10.1007/978-3-662-03444-6_7); full relevant p. 354 visually inspected | A physical expectation about high density/energy, without a displayed counterexample proof. |
| [Gebert-Nachtergaele-Reschke-Sims, arXiv:1912.12552v2](https://arxiv.org/pdf/1912.12552v2), pp. 1-5, Theorems 2.5/2.7 and Appendix A | The finite spatial cutoff is explicit, but the positive continuity result retains Gaussian UV smearing. The introduction's unbounded-commutator reasoning is not a proof of the target negative statement. |
| [Hinrichs-Lemm-Siebert, arXiv:2310.17736v2](https://arxiv.org/pdf/2310.17736v2), model (2.4), Remark 2.6, Theorem 2.7, Corollary 2.11; [published DOI](https://doi.org/10.1007/s00023-024-01453-y) body also checked | Regularized interaction with fixed smearing. It does not supply the unregularized cutoff conclusion. |
| [Siebert, arXiv:2409.10495v2](https://arxiv.org/pdf/2409.10495v2), Introduction, model (2.5)-(2.6), Theorem 2.1, Corollary 2.2, Example 3.8, Sections 4-5; [published DOI](https://doi.org/10.1007/s11005-025-01919-y) body reconciled | Sector-norm continuity on an extended CAR algebra and norm continuity after time averaging. Strict algebra inclusion does not itself prove discontinuity of the original dynamics. |
| [Buchholz, arXiv:1709.08107v7](https://arxiv.org/pdf/1709.08107v7), Theorem 4.6 and closing fermion discussion; [arXiv:1807.07885v2](https://arxiv.org/pdf/1807.07885v2), Theorem 5.3 and dynamics framework | Bose/resolvent and extended algebra constructions. The algebra/topology differs; these results do not imply the target negative CAR theorem. |
| [Radin 1977, author-hosted article](https://web.ma.utexas.edu/users/radin/papers/instability.pdf), pp. 69-71 and 77-79, full scanned body privately OCRed | A distinguishable-particle 1D hard-core model and a broader heuristic argument. Single-species indistinguishability is explicitly discussed as an obstruction; no calculation in a particular quasi-local C*-algebra is given. |
| [Bachmann-De Nittis, arXiv:2406.15670v2](https://arxiv.org/pdf/2406.15670v2), Introduction and localized-frame model | Neighboring continuum dynamics using localized frame interactions; not the candidate's unregularized kernel. |
| [Pachon, arXiv:2604.26267v2](https://arxiv.org/pdf/2604.26267v2), Introduction, Fermi-field results and Corollary 8 | A forward-reference lead about unequal-time commutation, including norm-continuous free/regularized systems. Noncommutation does not imply norm discontinuity; it is not an equivalent target result. |
| [Narnhofer-Thirring 1990, official APS abstract](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.64.1863) | The abstract specifies a momentum cutoff. Full article/review bodies were not authenticated; no theorem-level absence conclusion is drawn from them. |

## Discovery coverage and limits

Current arXiv versions and author publication pages were refreshed. Backward references were followed through the primary sources above. Indexed forward references to the 2020/2025 papers were screened; relevant continuum leads were inspected in primary bodies. Search batches included exact identifiers/titles, cutoff variants, local-number-square language, and norm-discontinuity terminology. Raw search/API datasets are private; [SEARCH_MANIFEST.json](SEARCH_MANIFEST.json) records only curated queries, routes, and limits.

The citation index demonstrably omits a known edge: the inspected 2026 paper cites the 2025 paper, but the fetched 2025 citation list did not include it. Consequently even a displayed zero citation count for the recent preprint has no priority-certifying force. The 2020 publisher PDF route returned HTML instead of a PDF; its current author arXiv version was authenticated. A university thesis landing page returned an empty body. Some older subscription bodies and unindexed/unpublished work remain outside verified coverage. These gaps do not undermine the checkable 2026 adaptation, but they prevent universal novelty certification, especially for the maximal-norm sharpening.

## Recommended concrete framing

Suggested title: **An explicit bounded-region counterexample for continuum fermion dynamics**.

Suggested literature paragraph:

> We give a self-contained construction for the spatially restricted Hamiltonian in OWR 7/2025. Siebert's earlier high-density cluster and phase argument establishes norm discontinuity for full-space difference potentials. Its proof adapts directly to the bounded symmetric cutoff kernel, yielding the existential discontinuity conclusion. The calculation here specifies one annihilation mode and Slater states for which the norm differences tend to 2, using a quantitative free-leakage comparison. We make no priority claim for this localization sharpening.

The original author proof already disclaims priority; the recommendation is to make the proof-level relationship explicit. Retain the bounded-region theorem and all verified scope restrictions. Do not describe this as the first resolution, as a currently open question newly settled, or as a novel theorem on the strength of cutoff geometry alone. No outreach has been prepared or initiated.
