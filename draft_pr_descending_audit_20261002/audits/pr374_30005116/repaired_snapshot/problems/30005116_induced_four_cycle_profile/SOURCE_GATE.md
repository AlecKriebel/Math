# Source/prior-attempt gate: induced four-cycle profiles

**30005116 / OWR-10252930-028, queue rank 400.** Gate completed 2 October 2026. This source gate consumes zero author turns. The original above-half-density profile is not treated as solved by the known isolated densities or by unrestricted inducibility.

## Exact formulation and normalizations

The complete source contribution is Dhruv Mubayi's Problem 10, Conjecture 11 and Theorem 12, printed **1227**, with the reference on 1228, in *Combinatorics, Probability and Computing*, OWR22/2022. The exact page was visually checked. The report citation is Oberwolfach Reports19(2022),no2,1165–1237; the publisher records actual publication **14 April 2023**. Both years have legitimate distinct meanings.

Primary source: https://ems.press/journals/owr/articles/10252930
DOI: https://doi.org/10.4171/OWR/2022/22
PDF: https://ems.press/content/serial-article-files/46961

The question asks for the asymptotic maximum number of induced four-cycles at prescribed edge density ξ. Above ξ=1/2 the conjectured maximizer is the complete multipartite construction for the triangle-density problem. The nearby sentence saying a problem was solved during the workshop belongs to the preceding Littlewood–Offord contribution, not this four-cycle question. The source's “Theorem 11” in its concluding sentence refers to the displayed Conjecture 11; it records the known ξ=1−1/k cases, not a proof at intermediate densities.

The cited Liu–Mubayi–Reiher paper defines edge density as e(G)/binom(n,2), and induced C4 density as N(C4,G)/binom(n,4), where copies are vertex sets, not labeled embeddings and not non-induced cycles. Their asymptotic feasible-region boundary is denoted I(C4,x). In a graphon, the probability of one fixed labeled induced-C4 edge pattern is one third of this induced density. Complements turn induced C4 into induced 2K2, not into another C4.

## Full imported material and campaign history

The full pinned imported record was read, including its August 2026 literature triage. That triage correctly credits known partials and is background, not an author attempt. The separate upstream research-results entry is null. The campaign's imported individual desk review suggests graphon symmetrization or weighted multipartite tests and explicitly identifies intermediate densities as the gap. Queue status at the gate is queued,0/5. The requested UnsolvedMath URL was attempted but unavailable.

The refreshed all-ref scan examined **411 remote refs** for target ID, code and induced-C4/four-cycle-profile aliases in branches, artifact paths and commit messages. No exact attempt was recovered. Live all-state PR searches for ID, code and “induced C4” returned zero. A broad “four-cycle” search returned PR212,314,319; their full bodies were inspected and concern a Gaussian threshold example, string-algebra surface models and fractional coloring, respectively. None is this target. The current related-target-groups file contains neither the ID nor code. These checks do not exclude uncommitted or unindexed work.

## Primary literature actually checked

1. Xizhi Liu, Dhruv Mubayi and Christian Reiher, *The feasible region of induced graphs*, JCTB158(2023),105–135, DOI https://doi.org/10.1016/j.jctb.2022.09.003 ; arXiv:2106.16203v2, revised7July2022. Author PDF https://homepages.math.uic.edu/~mubayi/papers/XizhiReiherInduced.pdf . Read definitions, Construction1.9, Theorems1.10–1.18, Sections3 and6, and concluding discussion of the conjecture. Page10 was visually checked. Conjecture1.17 is the exact full profile. Known results include I(C4,x)=3x²/2 for x≤1/2 and I(C4,x)≤3x(1−x)², with equality at x=1−1/k. Their complete-multipartite symmetrization theorem gives a **concave-envelope** upper bound; it does not preserve prescribed edge density and cannot be silently promoted to the conjecture.
2. József Balogh, Bernard Lidický, Dhruv Mubayi, Florian Pfender and Jan Volec, *Semi-Inducibility of some small graphs*, author preprint dated **8January2026**, https://homepages.math.uic.edu/~mubayi/papers/Semi_Inducibility.pdf . Read definitions, Theorems1.1/1.3, Question1, and proofs in Sections2/4. Their alternating four-cycle AC4 specifies two edges and two nonedges, leaving two pairs free. This is a different, weaker pattern than induced2K2. They retain the analogous intermediate-density clique-construction question and report numerical flag-algebra gaps. Their labeled-embedding normalization is different. Only the β≤1/2 range is needed for any complement comparison here; symmetry and normalization must be applied explicitly. Numerical bounds in that paper are not adopted as exact certificates.
3. Mubayi's primary publication list was read through 2026: https://homepages.math.uic.edu/~mubayi/papers.html . Targeted current exact-ID, title and conjecture searches found no verified full resolution. The 2026 paper above is materially relevant current work and must be credited. This is a bounded literature check, not proof of the absence of other prior work.

A complete multipartite test, a local variational certificate, a stronger semi-induced necessary condition or a proof at discrete densities is a scoped partial, not the original full answer. No historical novelty is assumed for elementary moment optimization or standard symmetrization mechanisms. Every substantive research response will be counted within the five-turn budget.
