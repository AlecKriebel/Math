# Conlon–Song 1999: bounded primary archival source audit

Audit date: 2026-10-15 UTC. Author metadata for this research project: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.

## Result and limitation

**The original full article was not obtained.** This audit therefore does not authenticate its application theorem, its test-function norms, its moment estimates, or its environment-tail bounds. It does not clear priority for the PR239 target and makes no novelty claim. The bounded retrieval/report task is complete; the source-authentication goal remains unresolved.

The strongest checked indirect evidence is that Conlon–Song's application establishes almost-sure diffusion for a particular space-time random-environment walk in every spatial dimension without a small-randomness restriction. This is a description by later authors in a full primary paper, not an independently checked statement of the 1999 theorem. It is unsafe to narrow the unseen paper to merely a weak CLT, and equally unsafe to attribute the PR239 tail estimate to it.

## Exact comparison target

The claim to be compared is the PR239 coarse quenched–annealed L1 bound: for each fixed iid space-time parameter p in (0,1), with transverse nearest-neighbour increments ±1, every deterministic coarse width M_N tending to infinity at any rate, and all fixed epsilon,K>0,

`P_env{coarse_L1(quenched law at N − annealed law at N; M_N) > epsilon} = O(N^(−K)).`

The three separate demands are the full parameter range, arbitrarily slow diverging width, and every polynomial tail order at fixed parameter. Almost-sure convergence, a fixed smooth-test CLT, or a single L2 rate does not by itself authenticate this full statement. A quantitative smooth-test theorem could still be relevant if its dependence on test-function norms and moment order permits the necessary bridge; those exact dependencies are the unresolved issue here.

## Bibliographic authentication

Joseph G. Conlon and Renming Song, *Gaussian limit theorems for diffusion processes and an application*, Stochastic Processes and their Applications 81(1) (1 May 1999), 103–128, DOI https://doi.org/10.1016/S0304-4149(98)00095-7.

The primary publisher record is https://www.sciencedirect.com/science/article/pii/S0304414998000957. The primary current author list https://www.renmingsong.web.illinois.edu/pages/publ.html and older author list https://rsong.web.illinois.edu/pages/publ.html both list the article; the original HTML around the entry contains no PDF link. Nearby articles do have explicit PDF links, so this is checked in source HTML rather than inferred from rendered link extraction. The separately listed Conlon–Song 2000 paper, *Random Walks Associated with Non-Divergence Form Elliptic Equations*, is a different article and was not substituted for the target.

The publisher's indexed abstract says that the paper studies a uniformly elliptic diffusion, proves Gaussian convergence with rates under a lower-dimensional perturbation condition, and applies the result to a random walk in random environment. The equations are missing in the primary HTML/indexed rendering available here. An indexed ResearchGate abstract restores an operator and a Brownian scaling expression, but this is an OCR-like secondary record, not an authenticated whole manuscript. In particular, this audit does not guess the precise meaning of the dimension condition from the abstract.

## New retrieval mechanisms and their outcomes

1. **Current and older author institutional pages.** Both complete HTML responses were saved and hashed privately. Neither target entry links a copy. The Michigan MCAIM institutional faculty page https://sites.lsa.umich.edu/mcaim/people/faculty/ points to the historical Conlon homepage at `www.math.lsa.umich.edu/~conlon/`; that host failed DNS in the direct retrieval. The corresponding `dept.math.lsa.umich.edu` root was 404. Current indexed individual PDFs under `/~conlon/paper/` concern other papers. No target filename was fabricated or scanned.

2. **Public scholarly location metadata.** OpenAlex work W1982043466 lists the DOI and RePEc publisher pointer, no repository PDF, `any_repository_has_fulltext=false`, and no content PDF. Semantic Scholar paper 389a455168e0fbfcfcaa02cbe5a91217770af91d gives only the DOI as its nominal open-access location. These are discovery metadata, not theorem evidence. Their bronze/open-access labels did not establish actual full-text availability.

3. **OpenAIRE discovery.** The public DOI query https://api.openaire.eu/search/publications?doi=10.1016%2FS0304-4149%2898%2900095-7&format=json contains an Elsevier PDF-like `originalId`, under `/response/results/result/0/metadata/oaf:entity/oaf:result/originalId/7/$`. That publicly listed resource returned HTTP403 and a 162-byte nginx denial page, not a PDF. The request stopped there. No alternate encoding, credential, token, or access-control workaround was attempted. Its metadata mixes open and closed instances and is not evidence that the whole article was read.

4. **Public archival snapshots.** A bounded Wayback CDX request for the historical Conlon homepage timed out. The public archive.org availability API returned no archived snapshot for the queried historical Conlon homepage and the queried historical Song publication-page URL. These are results for those exact URLs, not an assertion that the Internet Archive has no relevant capture anywhere.

5. **Mathematical Physics Preprint Archive.** The official University of Texas archive https://web.ma.utexas.edu/mp_arc/ has a failed author-search CGI (HTTP500). A materially distinct static-index route succeeded: complete yearly index HTML for 1995, 1996, 1997, 1998, and 1999 was saved and searched, case-insensitively, for `Conlon`, `Renming`, and `Gaussian limit`; no hit occurred. This is a bounded negative search in those five indexes, not a universal archive exclusion. No repeated CGI retries were made.

6. **Exact ResearchGate record.** Following the actual article link on Song's public profile yielded https://www.researchgate.net/publication/2320351_Gaussian_Limit_Theorems_For_Diffusion_Processes_And_An_Application. The readable indexed page explicitly states that no full text is available. The direct response was HTTP403. The author-copy request was not used. No external contact occurred.

7. **Publisher access.** The publisher route was already known to have an inaccessible PDF. Its article HTML also returned HTTP403 during this audit. No paywall, captcha, or access control was bypassed. The source gap is retained rather than filled with an abstract, a denial page, or another article.

## Primary later evidence actually read

### Boldrighini–Minlos–Pellegrinotti 2004

*Random walks in quenched i.i.d. space-time random environment are always a.s. diffusive*, Probability Theory and Related Fields 129 (2004), 133–156, DOI https://doi.org/10.1007/s00440-003-0331-x. Full primary publisher PDF: https://link.springer.com/content/pdf/10.1007/s00440-003-0331-x.pdf.

The complete PDF was copied read-only from an already authenticated sibling evidence folder, rehashed, and its relevant pages rendered and visually checked here. Its SHA256 is `f8bd982c1965d69d589b1b236363450062a80e6ceb6a9fb60a5f52ec7338ea49`.

- **Printed p134 / PDF p2**, introductory paragraph immediately before the model definition: these authors describe Conlon–Song [12] as an application to a model of their type and say that no small-randomness condition is needed for almost-sure diffusion in every dimension. The adjacent definition (1.1) is their own model `P(X_(t+1)=y | X_t=x, xi)=P_0(y−x)+c(y−x;xi(t,x))` with iid space-time environment. Their full model hypotheses must not automatically be assigned to the unseen Conlon–Song application.
- **Printed p135 / PDF p3**, last paragraph: their Appendix B is needed in dimensions 1 and 2 because the L2 rate does not support a direct Borel–Cantelli argument; they explicitly say this problem also appears in papers [2,12], where [12] is Conlon–Song.
- **Printed p135 / PDF p3**, displayed main theorem: their own stated conclusion is convergence in distribution to the centered Gaussian for almost every environment, under assumptions I–IV and their nondegeneracy condition (1.3). This provides context for their attribution, not an upper bound on everything that the 1999 paper might prove.

The p135 observation is evidence that a naive low-dimensional L2 summability route is inadequate in the cited context. It does **not** prove that Conlon–Song lacks higher moments, sharper estimates for other observables, or a route to the PR239 target.

### Bolthausen–Sznitman 2002

*On the static and dynamic points of view for certain random walks in random environment*, Methods and Applications of Analysis 9(3) (2002), 345–375. Full primary publisher PDF: https://www.intlpress.com/api/bgcloud-front/resource/pdf/volume/1806623584179167237-1806623584179167237-6ac853c8711bd0149b0a8c1cef32ba0d.pdf.

The complete published PDF was copied read-only from authenticated sibling evidence, rehashed, and the relevant page rendered and visually checked. SHA256: `b45824712f99076e2d1282b2660cc3fca6ac574ad4f82934ba83a1b2a74454ca`.

**Printed p371 / PDF p27, Remark4.3** states that their Theorem4.2 technique can also apply in the directed setting with additional assumption (3.1), in dimension d≥4, and compares this to part of Conlon–Song [5]. This authenticates a direct citation and a related mechanism. It does not specify the unseen 1999 application's theorem, its full range of dimensions, or its tail and derivative-norm constants. The d≥4 restriction belongs to this particular BS remark and must not be imposed on all Conlon–Song results.

### Boldrighini–Pellegrinotti 2001: pointer only

*T^(−1/4)-noise for random walks in dynamic environment on Z*, Moscow Mathematical Journal 1(3) (2001), 365–380, DOI https://doi.org/10.17323/1609-4514-2001-1-3-365-380. Primary metadata: https://www.mathnet.ru/eng/mmj25.

An exact citing passage is visible in the secondary indexed Conlon–Song record: the 1999 walk is described there as a standard walk plus random drift, and as indicating that small randomness is unnecessary for the CLT. This audit's MathNet landing-page attempts timed out and AMS issue access was forbidden. Therefore this particular model description is retained as an **indirect indexed pointer**, not a fresh whole-primary-source verification. It must not supply omitted Conlon–Song hypotheses.

## Exact residual gap and stop rule

Unverified in the original article: the precise application transition kernel and environment law; whether all fixed p∈(0,1) in PR239 is covered; exact theorem number and page; discrete/continuous embedding details; all-moment versus L2 estimates; any dependence of constants or ellipticity requirements on replica/moment order; test-function derivative or support norms; coarse-L1 conversion; and environment-tail quantifiers.

**No conclusion about presence or absence of the PR239 theorem follows from this retrieval failure.** A lawful complete original or author preprint would materially change this source-audit state and is the required new evidence before reopening exact-scope analysis. The checked routes are closed for now because rerunning them would not supply a materially new mechanism. No outreach was prepared or initiated. No manuscript or Git/index/ref/provider mutation was made.

## Artifacts and completion

`source_manifest.json` publishes URLs, retrieval times, response status, byte counts, and SHA256 metadata. Complete third-party bytes, extracted text, denial pages, and rendered pages are under ignored `private/`; they are excluded from the public authored manifest. `QUERY_LOG.md` records the bounded search mechanisms. `VALIDATION_RECEIPT.json` checks stored hashes and the private/public partition.

Completion estimate: **100% of this bounded retrieval and report checkpoint; original full-source authentication unresolved; target priority/novelty clearance not achieved.**
