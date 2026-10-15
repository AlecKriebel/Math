# PR239: focused BMP archival-source result

**Status: target full primary source not acquired.** This pass authenticates institutional metadata and extends the recorded public-archive coverage. It does not authenticate a theorem or proof, certify a spatial range, resolve the known exponent/display ambiguity, or support an absence/novelty conclusion.

Task scope: BMP1999, *Central limit theorem for a random walk in dynamical environment: integral and local*, Theory of Stochastic Processes 5(21), no. 3-4 (1999), 16-28; or the authors' 2007 survey *Random walks in a random (fluctuating) environment*, Russian Mathematical Surveys 62(4), 663-712, DOI 10.1070/RM2007v062n04ABEH004428. No manuscript, Git/index/ref, or remote-provider mutations occurred. No person was contacted and no outreach was prepared.

## Strongest verified content

The author's institution exposes complete BMP1999 **metadata**, including the abstract, through its unauthenticated OAI-PMH service:

- [Sapienza record](https://iris.uniroma1.it/handle/11573/28307).
- [Sapienza OAI GetRecord](https://iris.uniroma1.it/oai/request?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:iris.uniroma1.it:11573/28307).
- Retrieved OAI response: 2913 bytes, SHA256 `46cc83874dd00868b8a3e8fd0438bc180d651c812c7a69f47a124bec83e2ea98`; retrieval UTC 2026-10-15 04:46:50.

Paraphrase of the authenticated abstract: the model is a walk on Z^d, d>=1, in a space-time iid environment taking values in a finite set. A small stochastic perturbation gives an almost-sure central limit theorem with the averaged walk's parameters. The leading local asymptotic term includes a factor determined by the environment viewed from the final point. The metadata also confirms 1999, volume 5, pages 16-28, and 13 pages. It does **not** contain the smallness threshold, the complete assumptions, the local theorem, a residual norm/rate, or a spatial range.

Both independent author-institution landing records explicitly say that no files are attached:

- [Sapienza BMP1999](https://iris.uniroma1.it/handle/11573/28307).
- [Roma Tre BMP1999](https://iris.uniroma3.it/handle/11590/116583), newly located in this pass.
- [Sapienza survey](https://iris.uniroma1.it/handle/11573/27966).
- [Roma Tre survey](https://iris.uniroma3.it/handle/11590/150170), newly located in this pass.

The 2007 survey's author-institution abstract covers iid or temporally Markov quenched environments, almost-everywhere quenched CLTs, and annealed CLTs. That broad abstract does not identify the scope of any particular local theorem. Crossref independently confirms the survey's authors, title, journal, English pagination and DOI; its deposited PDF link leads to the publisher bot challenge in this environment. Crossref metadata is saved privately as 2226 bytes, SHA256 `532969833ab7383696ac8e1abff29de35c82b026cd40b1a7334b1835b1dfea35`.

## Finite archival coverage and access limits

| Route | Exact observed coverage/result | Interpretation |
| --- | --- | --- |
| MathNet official English static PDF | Supplied URL retrieved once by standard HTTP client; 20-second timeout | Full bytes unavailable here. Search-index excerpts are not a complete-source copy. |
| MathNet official aliases | `mi.mathnet.ru/eng/rm6849` and `mathnet.ru/eng/rm6849`, each one 20-second timeout | No materially different source obtained. These failures do not establish that the article is unavailable publicly. |
| IOP standard deposited link | Crossref `https://stacks.iop.org/0036-0279/62/i=4/a=R02/pdf` redirects to publisher bot verification | No PDF. Challenge not bypassed; route stopped. |
| mp_arc Austin | Full public year-index HTML files for 1991 through 2008 saved and searched | No target entry among the checked name/title spellings. Unrelated Minlos records found. This is finite index coverage, not an exhaustive absence proof. |
| mp_arc public search | Ordinary author query to its documented search CGI returns HTTP500 | Search-service failure; no claim about unsearched holdings. |
| BiBoS | Four candidate public year-index routes (1998, 1999, 2006, 2007) return HTTP404 in direct retrieval | Did not obtain full target source. Cached search results for 2007 show an unrelated 2008 random-jumps preprint. No exhaustive absence claim. |
| Vernadsky National Library of Ukraine | Public DSpace search API query `Boldrighini` returns three objects, all associated with a 2008 Condensed Matter Physics paper; public Atom search returns two item records | No target among those search results. Public API used normally without credentials or challenge bypass. |
| Vernadsky TSP community | Complete direct child listing contains exactly four annual communities, 2005, 2006, 2007, 2008 | No 1999 annual child in the listed community. 7421 response bytes; SHA256 `deabcfbb7f1f9b9a82b738fc0d4c8cca326cae252a6a3a371a8ba759623010b5`. |
| TSP official published-paper list | Oldest displayed item is volume 11(27), no. 3-4, 2005 | Does not supply 1999 issue. No claim about offline/other holdings. |
| OpenAlex survey DOI | Three locations: publisher DOI plus Sapienza and Roma Tre metadata; no PDF URL, no OA location | Discovery-service record, not proof of global absence. |
| Semantic Scholar survey DOI | `openAccessPdf.url` empty and status CLOSED | Same limitation. |
| Mathdoc Geodesic | Target article record and bibliography only; links back to MathNet | No attachment. Its journal label is inconsistent with DOI/institution metadata and must not override the latter. |
| Wayback CDX | One public PDF-URL lookup timed out after 20 seconds | No archive inventory was obtained; holdings remain unknown. |
| Author home-page candidates | One Sapienza candidate timed out; one Roma Tre candidate had a client TLS certificate error; other user-directory candidates inaccessible via browser tool | No author-hosted copy located. Do not infer that none exists. |
| Public scispace target page | Browser receives HTTP429, direct request HTTP403 | No source; stopped without trying to bypass restrictions. |

Machine-readable retrieval attempts, with UTC, URL, response/error, elapsed time and saved-byte paths, are in `access_attempts.jsonl`. Full remote responses and index HTML are for private reading under `private_sources/`; they are excluded from the authored deliverable manifest.

## Exact remaining authentication gap

The target comparison concerns a fixed iid scalar transition-probability law supported in (0,1), nearest-neighbor +/-1 steps, every deterministic diverging coarse-graining width, and a superpolynomial environmental tail for coarse L1 error. The institutional abstract establishes a finite-state perturbative prior model, but it cannot decide whether the full 1999 theorem, proof, or 2007 restatement extends beyond that model, treats periodic support explicitly, or yields the target quantifiers or tail conclusion by an argument not described in the abstract.

The unresolved questions are:

1. Exact environment state space, perturbation threshold, ellipticity, finite-range and aperiodicity assumptions, and whether the +/-1 periodicity is treated in the theorem or a remark.
2. Definition and normalization of the endpoint factor, and which moments/stationarity/convergence statements are available for it.
3. Exact residual: additive or relative, pointwise or uniform, convergence almost surely/in probability/in Lp, any rate, and every associated spatial/time restriction.
4. Whether the known normalized coordinate `u=(x-bT)/sqrt(T)` is used in the range restriction at the disputed display. Conditional algebra only: `|u|=o(T^(1/6))` means `|x-bT|=o(T^(2/3))`; an unnormalized `|x-bT|=o(T^(1/6))` would instead mean `|u|=o(T^(-1/3))`. Neither interpretation is authenticated by this pass.
5. Whether a prior result for a restricted environment law gives a full environmental tail and could be combined with other ingredients to reach the current theorem. No tail or all-width claim is certified or ruled out by these metadata.

The blocked route is acquisition, not a mathematical disproof or proof of priority. Reopening should use a materially new complete public/author/library source or restored ordinary access to the known official full text. Asking another person for a copy is outside the project's independent-research policy; no such request was drafted.
