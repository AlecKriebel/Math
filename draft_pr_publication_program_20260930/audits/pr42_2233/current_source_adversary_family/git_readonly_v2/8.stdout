# Source and status audit: Erdős Problem 653

Checked 30 September 2026. Numeric upstream ID: **2233**. Problem code: **EP-653**. This is an unresolved attempt with elementary route obstructions; no full solution or new-discovery claim is made.

## Exact statement and primary-source recovery

The pinned record asks whether the maximum number of different pinned-distance counts among n distinct planar points is asymptotic to n. Its raw statement and background are preserved in `source_record.json`, including a malformed imported fragment in the background. That fragment is not part of the mathematical question. The upstream source is the ulamai/UnsolvedMath dataset, pinned at revision `37e53eabe540fb458758e198be61634bd02ee008`, reused from the shared verified cache; attribution is retained under its CC BY 4.0 terms. The corresponding research-results entry is null, with only a dated OPEN-TRIAGE note embedded in the problem background.

Direct requests to [the official problem page](https://www.erdosproblems.com/653) and its LaTeX endpoint returned access failures. The cloud-browser route was also blocked. The indexed official page reports OPEN, gives the asymptotic question, and cites Erdős's 1997 *Some of my favourite unsolved problems*, Math. Japonica 46(3), 527–537. [The publisher contents](https://www.jams.jp/notice/mj/46-3.html) verifies that bibliographic item. A complete copy of that exact 1997 article was not recovered. Indexed status must not be described as a successful live page inspection.

A complete earlier primary source was recovered: Erdős, [*Some of my favourite problems in number theory, combinatorics, and geometry*](https://www.ime.usp.br/~yoshi/resenhas/abstracts/Erdos.pdf), section III.1, manuscript pp.14–15. Page 14 defines the counts for distinct points and credits the two-pin product observation to Erdős and Saldanha. Page 15 asks how many different count values can occur and proposes n−o(n). The page was rendered and visually checked, including the asymptotic expression and surrounding discussion. The [publisher record](https://revistas.usp.br/resenhasimeusp/en/article/view/74798) identifies the article as Resenhas 2(2) (1995), 165–186, DOI 10.11606/resimeusp.v2i2.74798. The downloaded author manuscript has its own page numbering; its p.15 is not being presented as journal p.15.

This direct primary evidence certifies the exact target despite the missing 1997 scan. It does not certify any later bound. A [current formal statement](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/653.lean) uses a finite set of points and labels the research question open; its theorem is unfinished. It is evidence for the formalized scope, not a proof.

## Historical constructions and limitations of access

The pinned record and indexed tracker report lower bounds with coefficients 3/8 (Erdős–Fishburn) and 7/10 (Csizmadia), and an upper bound n−c n^(2/3). The following primary bibliographic records were located:

- P. Erdős and P. Fishburn, [*Distinct distances in finite planar sets*](https://www.sciencedirect.com/science/article/pii/S0012365X96001458), Discrete Mathematics 175 (1997), 97–132, DOI 10.1016/S0012-365X(96)00145-8. The publisher abstract was available and confirms the pinned-distance-vector setting; the complete paper was not recovered.
- Gy. Csizmadia and D. Ismailescu, *Maximum number of different distance counts*, in *Intuitive Geometry*, Bolyai Society Mathematical Studies 6 (1997), 301–309. The [MTMT record](https://m2.mtmt.hu/api/publication/167371) and a primary [Gyárfás article's bibliography](https://users.renyi.hu/~gyarfas/Cikkek/101_Gyarfas_ErdosProblemsOnIrregularitiesOfLineSizesAndPointDegrees.pdf) verify the joint authorship and 1997 publication. The [author-linked abstract](https://www.researchgate.net/publication/2390358_Maximum_Number_of_Different_Distance_Counts) describes the planar 0.7 construction, with damaged formula extraction. Its platform date says 2001, unlike the verified 1997 book publication. Full text was unavailable without requesting it, and no request was sent.

Accordingly the old 0.7 construction and n^(2/3) upper obstruction are recorded as reported literature, not re-proved or fully audited here. In particular the malformed background's phrase suggesting that configurations *give an upper bound on g* is not adopted: a universal upper bound requires a proof for every configuration. Our construction obstructions do not improve the reported 0.7 lower bound.

## Newer public partial claims

A current search found material absent from the pinned August 2026 triage:

1. Idriss Olivier Bado, [*An incidence bound for distinct pinned-distance counts*](https://www.researchgate.net/publication/414001878_An_incidence_bound_for_distinct_pinned-distance_counts), a 2026 public preprint, DOI 10.13140/RG.2.2.12140.94087, claims g(n) ≤ n−c n^(5/7). The full text was readable in the hosting page. It invokes the circle-incidence bound of Janzer, Janzer, Methuku and Tardos. Their [complete arXiv manuscript](https://arxiv.org/abs/2411.07188) was recovered; Corollary 1.12 contains the cited exponents. That input has since appeared in the [Journal of the London Mathematical Society](https://doi.org/10.1112/jlms.70324), 112 (2025), e70324. The locally recovered arXiv file is v1 of 11 November 2024, not a mislabeled copy of the journal version.
2. Bado, [*A Katz–Tardos upgrade for planar distance-count spectra*](https://www.researchgate.net/publication/414000090_A_Katz-Tardos_upgrade_for_planar_distance-count_spectra), another 2026 public preprint, DOI 10.13140/RG.2.2.24723.85285, claims an exponent arbitrarily below (134−39e)/(162−47e), approximately 0.81736. Its full text was readable in the hosting page. It builds on R. Zeraoulia, *Centered-circle incidence bounds for planar distance-count spectra*, [DOI 10.5281/zenodo.21858673](https://doi.org/10.5281/zenodo.21858673), whose complete file was not recovered in this search.
3. An earlier third-party [working report on Problem 653](https://erdosproblemaday.com/report/653) gives exact small examples and an elementary n−2 upper bound for n≥7. The site is a separate author's AI-assisted project, not a prior attempt in this repository. Its finite examples are not an asymptotic solution and no such prior claim is repackaged here as a discovery.

Items 1–2 are **external preprint claims**, not independently reviewed theorems in this package. Reading a preprint and locating its cited input is not a full adversarial validation. No mathematical step of `PARTIAL.md` depends on their claims. Even if valid, all the displayed exponents are below 1 and are compatible with g(n)/n tending to 1. None of these sources claims to resolve the asymptotic question.

The bounded search located no full solution or refutation. This is a dated search conclusion, not a guarantee that no later or unindexed result exists. No assertion of best-known current bounds or historical priority is made.

## Prior-attempt and duplicate checks

Before proof work, the selected main-queue row was queued with 0/5 attempts. Numeric ID, problem code and descriptive searches found no earlier attempt folder, reset/history record, related-target duplicate, or matching all-state PR in this repository. The full pinned dataset had no duplicate of this exact question. Broader distance and Erdős paths found unrelated work. The all-ref attempt-path history and exact remote branch/PR checks also returned no earlier problem-2233 result. The external reports above are recorded as prior literature and claims, not mistaken for the user's own attempted entries.

The isolated branch is `dot/math-2233`. Shared queue/state/history files are managed separately and were not regenerated or edited here. Two substantive attempts are recorded locally, including their failures; source triage is not used to hide additional proof attempts.

## Result status

The original conjecture remains **unsolved in this attempt**. The proved statements are a generic-gluing identity, two restricted-support upper bounds, and a reproduction of a classical two-pin inequality. Their purpose is to make the failed routes and remaining gap checkable. The two routes stop because neither supplies a scalable nongeneric construction or a universal linear-proportion upper obstruction.

The actual research model was gpt-6-astra with xhigh reasoning. Separate adversarial review is pending. Finite checks alone do not supply that review, and no claim of novelty or external peer review is made.
