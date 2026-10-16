# PR 883 / PID 9900008: bounded recent priority audit

Audit date and cutoff: **2026-10-15 UTC**. Frozen candidate head: `af25d26e21945a1a132aace5e600485152777070`. Family: recent primary papers, final editions, and bounded citation trails. This is an independent priority assessment, not a package approval or a new proof search. Other audit families' outputs were not read before this verdict.

## Verdict

**The claimed unrestricted negative answer is a complete elementary corollary of published prior results, rather than merely a construction sharing old ingredients. A claim to a new resolution should fail the priority gate.** This audit did **not** locate an earlier primary paper explicitly announcing “Problem 7.5 has a negative answer” in the exact conventions. That historical bibliographic question remains open within this bounded audit. The particular periodic weights `(1,2)` realization was not located verbatim.

The distinction matters: an unlocated explicit announcement is not evidence that the mathematical conclusion is new. The derivation below closes the missing implication from the existing atomic counterexample through the established Lebesgue product. It requires no conjectural classification theorem. The final 2025 Khezeli–Mellick body supplies particularly direct confirmation that the atomic quotient obstruction survives a continuous Lebesgue factor; its main theorem alone would not settle this audit.

## Exact claim and boundary

The target is existence on `R²` of a nonzero locally finite diffuse measure, with constant `X`, such that every original-pair measurable, pointwise-covariant preserving allocation leaves the rooted distribution unchanged, although the **joint** mass-stationarity identity fails. The candidate uses horizontal Lebesgue lines, vertical period one, weights one and two, and a root on a weight-one line.

This is the unrestricted question in Thorisson, *Some Open Probability Problems*, §4 Problem 4.1, and Last–Thorisson (2009), Problem 7.5. It is not a question about added independent spatial randomness, a free action, exclusion of invariant directions, positive planar densities, dimension one, or invariance under general Markovian kernels. [Thorisson primary](https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf), [Last–Thorisson primary](https://arxiv.org/pdf/0906.2062).

## Decisive implication audit

Two prior facts suffice as input. Last–Thorisson (2009), Example 7.1, printed manuscript pp. 22–23, constructs an atomic random measure `η` and probability `Q` invariant under every preserving allocation, but not mass-stationary. The example uses two Poisson components with unequal irrationally related masses. Last–Thorisson (2015), §8 Proposition 1, printed manuscript pp. 14–15, proves that adjoining a Lebesgue coordinate preserves **and reflects** mass-stationarity, with that new coordinate acting trivially on the original state. [2009 body](https://arxiv.org/pdf/0906.2062), [2015 body](https://arxiv.org/pdf/1405.7566v2).

Here is the full bridge, recorded as an inference from these published inputs. It is included to distinguish a complete corollary from a superficial resemblance.

Take the 2009 example on `R`, keep its state space and law, and set

```
η̃ = η ⊗ λ,
θ̃_(t,v) ω = θ_t ω,
```

where `λ` is Lebesgue measure on the added coordinate. Let `τ` be **any** original-state measurable pointwise-covariant allocation of this lift. Covariance in the added coordinate gives

```
τ_ω(s,u+v) = τ_ω(s,u) + (0,v).
```

Consequently there are measurable maps `a_ω(s)` and `b_ω(s)` with

```
τ_ω(s,u) = (a_ω(s), u + b_ω(s)).
```

Covariance in the original coordinate makes `a` a covariant allocation for `η`. For Borel `B,C` with `0 < λ(C) < ∞`, Tonelli's theorem and translation invariance of `λ` yield

```
τ_*η̃(B×C)
 = ∫ 1{a(s)∈B} [∫ 1{u+b(s)∈C} du] η(ds)
 = λ(C) (a_*η)(B).
```

Thus `τ_*η̃=η̃` implies `a_*η=η`. The rooted action of `τ` on the lift is exactly the original action by `a(0)` because the second coordinate acts trivially. The allocation invariance established in Example 7.1 therefore proves the required invariance for **every** preserving allocation of the lift. This argument allows collisions; it assumes no injectivity.

The lift is locally finite, nonzero and diffuse: each singleton has zero Lebesgue-coordinate mass. Proposition 1 then transfers the verified failure of full mass-stationarity to the lift. Constant `X` suffices, since only the random measure and its shift action are needed; the 2009 statement already tests the larger class of measurable state-dependent allocations. Restricting to allocations measurable from the measure cannot weaken the example's verified invariance.

This closes all three logical parts of the **same existential negative conclusion**: diffuse hypothesis, universal preserving-allocation invariance, and failure of full mass-stationarity. It does not assert that the periodic formula itself appeared in 2009 or 2015, or that those authors explicitly advertised this consequence at that time. No newly unsupported statement is substituted for the central difficulty.

## Recent primary body findings

| Primary and edition verified | Precise body locus | Finding and exact relation |
|---|---|---|
| Khezeli–Mellick, *On the Existence of Balancing Allocations and Factor Point Processes*, **ALEA 22 (2025), 1327–1334**, DOI `10.30757/ALEA.v22-51`; received 2024-04-25, accepted 2025-11-25 | Theorems 1.1–1.2, pp. 1328–1329; proof and Remark 3.2, pp. 1333–1334 | Nontrivial invariant directions prevent a nonempty factor point process. Remark 3.2 explicitly identifies product measures with atomic quotients as remaining cases and states equivalence of the corresponding balancing-allocation existence problem with the quotient problem. It points to LT2023 §8 and handles noninjective atomic images. This is strong mechanism-level priority evidence. The paper does not state the exact self-preserving characterization counterexample. [Final primary](https://alea.impa.br/articles/v22/22-51.pdf). |
| Last–Thorisson, *Transportation of diffuse random measures on R^d*, **ALEA 20 (2023), 577–592**, DOI `10.30757/ALEA.v20-21`; latest arXiv is 2112.13053v2, 2023-03-08 | Theorem 1.1, p. 579; §8 pp. 589–590; Remarks 8.1 and 9.2, p. 590 | Canonical Poisson parallel horizontal lines cannot be allocated to planar Lebesgue measure without external randomness. This establishes nonexistence of a balancing allocation between **two** stationary measures. It does not assert failure of the self-preserving characterization. Remark 8.1 expressly singles out invariant directions; reversing source/destination in Remark 9.2 changes existence. [Final primary](https://alea.impa.br/articles/v20/20-21.pdf). |
| Huesmann–Müller, *Transportation of stationary random measures not charging small sets*, **ALEA 21 (2024), 1903–1913**, DOI `10.30757/ALEA.v21-72`; received 2023-03-07, accepted 2024-10-17 | Theorem 1.2, p. 1904; Corollary 1.3, p. 1905; proof §3 | A source charging no `(d−1)`-rectifiable set admits a balancing factor allocation. The candidate charges horizontal line segments and fails this hypothesis. The corollary shifts a stationary measure to its Palm version; it does not characterize arbitrary rooted laws by self-preserving allocations. The paper credits LT2023's obstruction and the independent Khezeli–Mellick route. [Final primary](https://alea.impa.br/articles/v21/21-72.pdf). |
| Last, *Tail processes and tail measures: An approach via Palm calculus*, **Extremes 26 (2023), 715–746**, final version published 2023-06-27 | §3, especially Theorem 3.2, pp. 720–721; Theorem 5.2, pp. 723–725 | Uses the Mecke identity for general mass-stationarity and a spectral shift formula for special exceedance measures. These are integral/randomized conditions; no removal of background randomness from the exact allocation-only question is established in the inspected loci. [Final primary](https://link.springer.com/article/10.1007/s10687-023-00472-y). |

### Final 2025 body versus pinned 2024v2

The final was actually retrieved and all eight pages read, including visual verification of pp. 1333–1334. The pinned arXiv v2 remains dated 2024-04-25; it is not the final body. The final strengthens Remark 3.2 with an explicit quotient-equivalence assertion, a reference to LT2023 §8, and a warning that atomic maps need not be injective or surjective. It also makes stationarity, positive finite sample intensities, uniform separation and distribution-independent constructions more explicit in its main statements. These changes strengthen the priority relevance of the closing discussion; they do not turn the main theorem into an unrestricted mass-stationarity characterization. [Pinned primary](https://arxiv.org/pdf/2303.05137v2), [final primary](https://alea.impa.br/articles/v22/22-51.pdf).

## Descendant and citation-trail screen

Two successful bounded citation-index lookups were used **only for discovery**. They returned two citing entries for 2303.05137 and five for 2112.13053, including a duplicate final/preprint entry. Those counts are not comprehensive citation totals. Technical statements below come from primary bodies, not index summaries.

- Khezeli, [2304.02863v1](https://arxiv.org/pdf/2304.02863), 2023-04-06: §4.1, p. 14, interprets mass-stationary measures as unimodular measured spaces; §5.2 treats equivariant Markovian rerooting kernels. These are different invariance classes. Relevant body loci and the reference to Khezeli–Mellick were inspected; this 50-page manuscript was not exhaustively line-read.
- Erbar–Huesmann–Jalowy–Müller, [2304.11145v2](https://arxiv.org/pdf/2304.11145), 2024-02-01: introduction p. 8 discusses precisely the balancing-factor obstruction and credits HM/KM. Primary publication metadata identifies **JFA 289(4) (2025), 110974**, DOI `10.1016/j.jfa.2025.110974`; the publisher body returned 403. Only the preprint's relevant body and references were screened. [Publisher metadata](https://www.sciencedirect.com/science/article/pii/S0022123625001569).
- Huesmann–Müller, [2402.04842v1](https://arxiv.org/pdf/2402.04842), 2024-02-07: introduction §§1.1–1.2 and §2 concern Palm reformulations of transport distances and a continuity equation, not the exact characterization. The index supplied a 2025 final DOI `10.1016/j.spa.2025.104633`; the DOI route was inaccessible, so no final-body comparison is claimed. [DOI route](https://doi.org/10.1016/j.spa.2025.104633).
- Klatt–Last–Lotz–Yogeshwaran, [2506.05907v1](https://arxiv.org/pdf/2506.05907), 2025-06-06, 78 pages: introduction and §§2–3 define stationary transports and persistence of asymptotic variance; whole-text term and reference screening found the older 2009 citation, not an allocation characterization. This is a relevant title/citation near-hit, not a fully audited proof corpus.

The successful primary descendants did not provide an explicit named negative answer or an implication invalidating the bridge above. The 2016 Persian Khezeli thesis cited by the modern papers was not obtained or translated. It may be useful for historical credit; this is a recorded evidence gap, with no outreach prepared or initiated.

## Retrieval and reproducibility

The exact 36 search strings, cutoff, and citation-index URLs are in `SEARCH_LOG.json`. Unrelated search-engine results, misleading crawl dates, and aggregator labels were not used to establish technical claims or publication dates.

| Final primary | Retrieval result | SHA-256 |
|---|---|---|
| KM2025 | Bare URL: HTTP 400 in direct downloader; `?download=1`: HTTP 200, 551159 bytes | `3130b8bc7eeef04f7203fd2f5e7c4160c3101f40d12f54249e30d3d41c5aa95e` |
| LT2023 | HTTP 200, 535237 bytes | `e410d8be2920be1ad127f7d1a554fb185b4ab956429763ab97e0e03e3fe9c681` |
| HM2024 | Bare and `?download=1`: HTTP 400; `?x=20261015`: HTTP 200, 611832 bytes | `d95118d9e427a796b500fd16479501c6bc74ee1211470877905c9a9c47de91a3` |
| Last2023 tail | Springer PDF HTTP 200 with cookie-query redirect, 5576011 bytes | `36bae06c2426a10c7b50e161a1860b157190be29f09bad3011957c8c7c0709e5` |

Raw PDFs, text extractions, citation-index responses and page images are only in ignored `private_sources/`. Exact timestamps and additional hashes are recorded there. No raw source corpus is in the public allowlist. Central final bodies (KM2025, LT2023, HM2024) were read across all sections; the longer descendants were explicitly scope-screened rather than represented as fully proof-audited.

## Required global credit wording

> The unequal-atom obstruction is due to Last and Thorisson (2009), Example 7.1. Their 2015 §8 Proposition 1 supplies the Lebesgue-product mass-stationarity reduction. The invariant-direction and atomic-quotient allocation mechanism is also explicit in Last–Thorisson (2023), §8, and Khezeli–Mellick (2025), Remark 3.2. The periodic construction is an elementary explicit illustration of these established mechanisms. No new-resolution, novelty, firstness, or exhaustive literature-clearance claim is made.

This wording should govern titles, abstracts, summaries, metadata, and any claimed-solved description, not be isolated in an addendum beside stronger promotional wording. The already present novelty disclaimer is appropriate but does not, by itself, establish priority clearance.

## Strongest verified finding and remaining gap

**Verified:** prior published results plus the displayed elementary covariance calculation already imply the exact unrestricted negative existential answer. Recent final literature explicitly recognizes its structural obstruction. The candidate may be useful as a transparent periodic worked example, but a new mathematical resolution has not been established.

**Not verified:** the date and author of the first explicit written recognition of this particular corollary, uniqueness or novelty of the periodic realization, exhaustive absence of another counterexample, or the status of stronger free/no-invariant-direction/one-dimensional/kernel questions. The bounded queries cannot prove any global absence or historical firstness claim. This audit makes no final package-release recommendation beyond its priority finding.
