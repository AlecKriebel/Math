# Independent priority audit of PR 764

Audit completed on 14 October 2026 (UTC). Target: problem 30005453,
OWR-12697708-006. Reviewed head:
`88acf20cdd5b4fe8605dab7eb27733b7deda1c47`.
The frozen author-v2 proof has SHA-256
`4ab6831e31f2c55969d17089a2cefacdd3d173a54f4b00e8244a5f8a635616f4`.

## Outcome and necessary publication framing

**Conditional pass for publishing a fully credited alternative proof.** No
retrieved source demonstrates a full resolution predating the server record of
this PR's creation. There is, however, a complete overlapping October 2026
preprint, and an additional independently reported manuscript whose public date
and complete contents were not obtained. Publishing the result as an exclusive
first solution, or saying that the positive homogenization conjecture remains
unresolved today, would contradict the available evidence.

No mathematical repair is requested. Before a preprint can pass its own package
reviews, the paper, metadata, README, tracker notes and acceptance text must all:

1. Separate the false unrestricted nonnegative uniqueness assertion from the
   proved strictly positive theorem. State bounded degree, bounded above positive
   rates, countability, `0 <= alpha < 1`, positive integer initial counts and
   simultaneous coordinatewise almost-sure convergence.
2. Cite Qin's full contemporaneous theorem, acknowledge that it covers the
   substantive positive theorem, and describe this proof's different mechanism.
   Do not claim an improvement in the initialization class.
3. Record the Angel--Hermon--Yao work as reported by Qin, rather than presenting
   an unread manuscript as a independently verified theorem with a known date.
4. Describe only the established repository chronology. Avoid claiming that Git
   author dates certify public upload time, or that a bounded search establishes
   universal priority.
5. Credit the earlier finite WARM boundary-equilibrium construction and the
   Couzinié--Hirsch/2018 thesis baselines. The alternating boundary example alone
   is not an independently established novel construction.

The user authorized publication after rigorous review; no new permission or
external communication is required by this finding. No outreach was prepared or
initiated. This audit does not change a PR or its queue status.

## Exact target and older baseline

The PR's theorem concerns edge weights reinforced at vertex clocks. It is not a
vertex-weight urn reinforced at edge clocks, a finite stochastic approximation
theorem, an interacting-urn synchronization theorem, or a result only on trees.
The problem is resolved in two explicitly distinguished senses: the literal
unrestricted uniqueness assertion is false, while the positive homogenization
formulation has a full proof under the stated model assumptions.

The [original Oberwolfach report](https://ems.press/content/serial-article-files/47008?nt=1),
printed pp. 653--655, defines bounded positive heterogeneous firing rates and
bounded degrees, then states Conjecture 1 without a positivity restriction on
equilibria. The [official MATRIX-hosted chapter draft](https://www.matrix-inst.org.au/wp_Matrix2016/wp-content/uploads/2023/Aletti.pdf),
§5, PDF pp. 8--10, retains that wording. Its
[publisher record](https://link.springer.com/chapter/10.1007/978-3-031-76738-8_29)
identifies the 2025 chapter, first online 3 July 2025, pp. 477--498. The hosted
draft was inspected; the subscription-only final publisher PDF was not obtained.
No assertion of byte identity to that final PDF is made.

The [2021 Couzinié--Hirsch author manuscript](https://arxiv.org/pdf/2010.03347v2)
specifies unit initial weights and unit rates. Theorem 2.2 supplies the general
bounded-degree case below one half, regular-graph extensions slightly above one
half, and the full subcritical range on the integer line. Its positive-equilibrium
existence and persistence lemmas are genuine earlier ingredients, not the full
general-range convergence theorem. The published identity is
[ECP 26, paper 35](https://doi.org/10.1214/21-ECP404).

The [2018 Couzinié thesis](https://www.theorie.physik.uni-muenchen.de/TMP/theses/couziniethesis.pdf),
printed pp. 2--5, already admits heterogeneous rates bounded below away from zero
and bounded positive random initialization. Theorem 1.2 covers general graphs
below one half; Theorems 1.3--1.4 handle special homogeneous graphs. Conjecture 1.5
expressly retains the all-subcritical general-graph gap. Its scope neither proves
the PR's complete theorem nor permits withholding credit for heterogeneous-rate
work.

The [2014 finite WARM manuscript](https://arxiv.org/pdf/1406.0449v1),
§3.6, printed p. 28, displays the alternating cycle allocation
`2(1,0,1,0,...)/n` in its normalized finite model. Its stability discussion concerns
strong reinforcement. Direct substitution extends the equilibrium identity to
every positive exponent; that observation is a deduction, not a quotation of a
subcritical theorem in that paper. The PR's infinite-path `2,0` construction is
the same local matching mechanism with vertex rates one. Finite boundary
equilibria therefore deserve credit, although they do not prove the infinite
positive homogenization result.

## Current overlapping result and unresolved bibliographic lead

[Qin, arXiv:2610.11780v1](https://arxiv.org/abs/2610.11780v1), submitted
8 October 2026, Theorem 1.1, proves positive-equilibrium uniqueness and
coordinatewise homogenization for all subcritical exponents, bounded-degree
graphs and positive bounded rates without a lower bound. It allows arbitrary
finite positive real initial weights. Connected components extend its connected
statement to the PR's disconnected setting. All 14 PDF pages were read; the
Liouville comparison and stochastic passage have no identified substantive gap.
Its proof uses a power transform, row-balanced logarithmic-norm comparison of
complete trajectories, pure-birth persistence and time-shift extraction. These
overlap conceptually with the PR; the PR's exact jump compensator, finite-volume
vertex minimization and approximate space-time maximum principle differ. Qin's
Remark 1.3 includes the same infinite matching boundary example. Remark 1.2
reports a separate Angel--Hermon--Yao resolution. Their unread manuscript cannot
be assigned a verified public date or full heterogeneous-rate scope here.

The precise mathematical checks and an independent comparison derivation are
in `COMPARISON_DERIVATION.md`; the scope mapping is in `THEOREM_COMPARISON.json`.

The three-author lead is entitled *Long-time behavior of graph-based weakly
reinforced Pólya urns*, dated 2026 in Qin's bibliography, with no persistent
identifier there. Qin's related-work paragraph also describes a vertex-weight,
edge-clock tree result from that work. This does **not** justify concluding that
the complete manuscript concerns only trees: the separate reported resolution of
the original urn conjecture must also be respected.

[Dong Yao's primary research page](https://sites.google.com/view/dongyao/home/research)
lists an in-preparation five-author work with Angel, Hermon, Xiangyu Huang, Yao
and Yiyue Zhang. It supplies no downloadable proof/date for the three-author
work. Angel's and Hermon's available primary pages are visibly dated/incomplete.
They are bounded search venues, not exhaustive publication catalogues. A public
conference schedule naming a related Yao talk supplies neither a theorem nor a
proof. This unresolved bibliographic lead prevents a first-solution certificate,
but is not evidence of a demonstrated earlier equivalent full theorem.

## Chronology and its limits

Independent authenticated and unauthenticated GitHub reads agree:

| Observation | Evidence | Interpretation |
| --- | --- | --- |
| PR created and last updated `2026-10-05T22:58:53Z` | GitHub server metadata | PR record predates Qin's submission |
| Current PR contains one commit, exact reviewed head | Commit list and current PR | Current candidate is identified |
| Commit author/committer `2026-10-05T22:56:44Z` | Git object/API | Author-controlled timestamps, not upload receipts |
| Timeline contains one committed event and no force-push event | Current timeline endpoint | No recorded head replacement was observed |
| Repository and frozen proof accessible without authentication now | Ordinary public HTTP 200; exact proof hash | Confirms present public access and byte identity |
| Qin v1 submitted `2026-10-08T11:59:26Z` | arXiv history and DataCite metadata | Verified submission date |
| Qin DataCite record registered `2026-10-09T02:55:13Z` | Official registry | Additional server timestamp |

These observations support the repository's earlier recorded chronology. They
do not prove historic repository visibility, rule out unrecorded external
circulation, or prove when every current file first became public. No archival
October 5 HTTP capture or server-stamped first-upload receipt binding every
current byte was obtained. The note may identify its proof as recorded in the
October 5 PR and its current hash, while explicitly declining a universal
priority claim. The later arXiv result is not, by its submission date alone, a
reason to label this earlier recorded candidate a rediscovery or close it.

## Search coverage and reproducibility

The frozen October 5 source review was read and its important primary sources
were independently retrieved, not merely repeated. This fresh audit used 32
indexed queries and 19 ordinary official-registry requests across Zenodo,
DataCite, Crossref and arXiv, plus primary author pages. No requests failed and no
access/rate bypass was attempted. All selected bibliographic hits were inspected.
Crossref's relevance-ranked twenty-hit lists and the broad Yao query's first
twenty-five hits are expressly non-exhaustive; the disambiguated author/title
queries supplement them. Other bounded registry queries returned at most their
requested twenty-five hits. Search-engine snippets are leads only.

The exact query strings and retrieved primary URLs are recorded in
`INDEXED_SEARCH.json`, `REGISTRY_SEARCH.json`,
`TARGETED_REGISTRY_SEARCH.json`, `DISAMBIGUATED_ARXIV_SEARCH.json`,
`PRIMARY_RETRIEVALS.json`, `PUBLIC_HTML_RETRIEVALS.json`,
`MATRIX_CHAPTER_RETRIEVAL.json` and `FINITE_WARM_RETRIEVAL.json`.
Receipts preserve timestamps, status, byte counts and SHA-256 hashes without
redistributing downloaded source bodies. `GITHUB_CHRONOLOGY.json` preserves the
selected server observations. The offline manifest verifier checks artifact
closure; it does not simulate a priority search or a mathematical proof.

The strongest verified priority result is a complete known contemporaneous
overlap with distinct proof details, with no retrieved demonstrated full
predecessor to the October 5 PR record. The exact remaining gap is exhaustive
priority/public-disclosure chronology, especially the inaccessible full
Angel--Hermon--Yao manuscript. This uncertainty can be disclosed accurately and
does not require contacting anyone or abandoning the independently verified
alternative proof.
